import React, {useEffect, useRef, useCallback, useMemo, MutableRefObject} from 'react'
import {
  createChart,
  IChartApi,
  ISeriesApi,
  createSeriesMarkers,
  MouseEventParams,
  IPrimitivePaneView,
  IPrimitivePaneRenderer,
  IPanePrimitive,
  PaneAttachedParameter,
  Time
} from 'lightweight-charts'
import {
  ComponentConfig,
  ChartConfig,
  SeriesConfig,
  TradeConfig,
  TradeVisualizationOptions,
  Annotation,
  AnnotationLayer,
  LegendConfig,
  SyncConfig,
  PaneHeightOptions
} from './types'
import {createTradeVisualElements} from './tradeVisualization'
import {RectangleOverlayPlugin} from './rectanglePlugin'
import {createAnnotationVisualElements} from './annotationSystem'
import {SignalSeries} from './signalSeriesPlugin'
import {TradeRectanglePlugin} from './tradeVisualization'

import {cleanLineStyleOptions} from './utils/lineStyle'
import {createSeries} from './utils/seriesFactory'
import {getCachedDOMElement, createOptimizedStyles} from './utils/performance'
import {ErrorBoundary} from './components/ErrorBoundary'
import {ChartCoordinateService} from './services/ChartCoordinateService'
import {PositioningEngine} from './services/PositioningEngine'

// Global type declarations for window extensions
declare global {
  interface Window {
    chartApiMap: {[chartId: string]: IChartApi}
    chartResizeObservers: {[chartId: string]: ResizeObserver}
    legendRefreshCallbacks: {[chartId: string]: (() => void)[]}
    legendPlugins: {[key: string]: any}
  }
}

// Utility function for retrying async operations with exponential backoff
const retryWithBackoff = async (
  operation: () => Promise<any>,
  maxRetries: number = 5,
  baseDelay: number = 100,
  operationName: string = 'operation'
): Promise<any> => {
  let lastError: Error

  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await operation()
    } catch (error) {
      lastError = error as Error

      if (attempt === maxRetries - 1) {
        throw lastError
      }

      // Exponential backoff with jitter
      const delay = baseDelay * Math.pow(2, attempt) + Math.random() * 100
      await new Promise(resolve => setTimeout(resolve, delay))
    }
  }

  throw lastError
}

// ✅ Create Legend Plugin using Pane Primitives for proper pane scoping
const createLegendPlugin = (
  legendConfig: any,
  paneId: number,
  chartId: string,
  legendElementsRef: MutableRefObject<Map<string, HTMLElement>>
) => {
  // Create a proper Pane Primitives plugin that renders DOM elements
  class LegendPanePrimitive implements IPanePrimitive<Time> {
    private _paneViews: LegendPanePrimitivePaneView[]
    private legendElement: HTMLElement | null = null
    private paneId: number
    private seriesList: ISeriesApi<any>[] = []
    private chartApi: IChartApi | null = null
    private resizeObserver: ResizeObserver | null = null
    private resizeTimeout: NodeJS.Timeout | null = null
    private paneSizeCheckInterval: NodeJS.Timeout | null = null

    constructor() {
      this._paneViews = [new LegendPanePrimitivePaneView(this)]
      this.paneId = paneId
    }

    // Required IPanePrimitive interface methods
    attached(param: PaneAttachedParameter<Time>): void {
      this.chartApi = param.chart

      // Store global reference for this plugin instance
      if (!window.legendPlugins) {
        window.legendPlugins = {}
      }
      window.legendPlugins[`pane_${this.paneId}`] = this

      // Create legend element
      this.createPaneLegend()

      // Get initial pane dimensions
      this.updatePaneDimensions()

      // Auto-detect series
      this.autoDetectSeries()

      // Position legend using configuration
      this.positionLegend(legendConfig.position || 'top-left', legendConfig.margin || 8)

      // Set up resize observer for dynamic repositioning
      this.setupResizeObserver()
    }

    detached(): void {
      // Clean up resize observer
      if (this.resizeObserver) {
        this.resizeObserver.disconnect()
        this.resizeObserver = null
      }

      // Clean up resize timeout
      if (this.resizeTimeout) {
        clearTimeout(this.resizeTimeout)
        this.resizeTimeout = null
      }

      // Clean up pane size check interval
      if (this.paneSizeCheckInterval) {
        clearInterval(this.paneSizeCheckInterval)
        this.paneSizeCheckInterval = null
      }

      if (this.legendElement && this.legendElement.parentNode) {
        this.legendElement.parentNode.removeChild(this.legendElement)
      }
      this.legendElement = null
      this.seriesList = []
      this.chartApi = null
    }

    paneViews(): IPrimitivePaneView[] {
      return this._paneViews
    }

    // Add series to this pane's legend
    addSeries(series: ISeriesApi<any>): void {
      // Check if series already exists to prevent duplicates
      if (!this.seriesList.find(s => s === series)) {
        this.seriesList.push(series)
        this.updateLegendContent()
      }
    }

    // Remove series from this pane's legend
    removeSeries(series: ISeriesApi<any>): void {
      const index = this.seriesList.findIndex(s => s === series)
      if (index > -1) {
        this.seriesList.splice(index, 1)
        this.updateLegendContent()
      }
    }

    // Create the actual DOM legend element for the entire pane
    private createPaneLegend(): void {
      // Create legend container
      this.legendElement = document.createElement('div')
      this.legendElement.className = `chart-legend-pane-${this.paneId} pane-legend`

      // Apply styling from configuration
      this.legendElement.style.position = 'absolute'
      this.legendElement.style.zIndex = (legendConfig.zIndex || 1000).toString()
      this.legendElement.style.pointerEvents = 'none'
      this.legendElement.style.backgroundColor =
        legendConfig.backgroundColor || 'rgba(255, 255, 255, 0.95)'
      this.legendElement.style.border = `${legendConfig.borderWidth || 1}px solid ${legendConfig.borderColor || '#e1e3e6'}`
      this.legendElement.style.borderRadius = `${legendConfig.borderRadius || 4}px`
      this.legendElement.style.padding = `${legendConfig.padding || 5}px`
      this.legendElement.style.margin = `${legendConfig.margin || 4}px`
      this.legendElement.style.fontFamily =
        '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
      this.legendElement.style.fontSize = '10px'
      this.legendElement.style.color = '#131722'
      this.legendElement.style.boxShadow = '0 2px 4px rgba(0, 0, 0, 0.1)'
      this.legendElement.style.userSelect = 'none'
      this.legendElement.style.minWidth = '120px'
      this.legendElement.style.fontWeight = '500'

      // Create initial legend content
      this.updateLegendContent()

      // Append to chart element
      try {
        const chartElement =
          document.querySelector(`[data-chart-id="${chartId}"]`) ||
          document.querySelector('.tv-lightweight-charts')

        if (chartElement && this.legendElement) {
          chartElement.appendChild(this.legendElement)

          // Store reference for updates using a unique key
          const legendKey = `${chartId}-pane-${this.paneId}`

          // Store in legendElementsRef for backward compatibility
          if (legendElementsRef.current) {
            legendElementsRef.current.set(legendKey, this.legendElement)
          }

          // Store in global legendPlugins for access
          if (!window.legendPlugins) {
            window.legendPlugins = {}
          }
          window.legendPlugins[legendKey] = this
        } else {
          console.error(`❌ Could not access chart element for pane ${this.paneId}`)
        }
      } catch (error) {
        console.error(`❌ Error adding legend to pane ${this.paneId}:`, error)
      }
    }

    // Simplified positioning method using consolidated services
    private positionLegend(position: string, margin: number): void {
      if (!this.legendElement || !this.chartApi) return

      // Use configuration position if available, otherwise fallback to parameter
      const configPosition = legendConfig.position || position
      const configMargin = legendConfig.margin || margin

      try {
        // Use consolidated services for positioning
        const coordinateService = ChartCoordinateService.getInstance()

        // Get pane coordinates using the service
        const paneCoords = coordinateService.getPaneCoordinates(this.chartApi, this.paneId)
        if (!paneCoords) {
          setTimeout(() => this.positionLegend(configPosition, configMargin), 100)
          return
        }

        // Ensure legend has dimensions
        if (this.legendElement.offsetWidth === 0 || this.legendElement.offsetHeight === 0) {
          // Force reflow
          this.legendElement.style.visibility = 'hidden'
          void this.legendElement.offsetHeight
          this.legendElement.style.visibility = 'visible'
        }

        const legendWidth = this.legendElement.offsetWidth || 120
        const legendHeight = this.legendElement.offsetHeight || 60

        // Use PositioningEngine for legend positioning
        const legendCoords = PositioningEngine.calculateLegendPosition(
          this.chartApi,
          this.paneId,
          configPosition as any, // Cast to ElementPosition
          {
            margins: {
              top: configMargin,
              right: configMargin,
              bottom: configMargin,
              left: configMargin
            },
            dimensions: {width: legendWidth, height: legendHeight}
          }
        )

        if (legendCoords) {
          // Apply positioning using the service
          PositioningEngine.applyPositionToElement(this.legendElement, legendCoords)
        } else {
          // Fallback to manual positioning if service fails
          this.fallbackLegendPositioning(
            configPosition,
            configMargin,
            legendWidth,
            legendHeight,
            paneCoords
          )
        }
      } catch (error) {
        console.error(`❌ Error positioning legend for pane ${this.paneId}:`, error)
        // Fallback positioning
        this.legendElement.style.top = '10px'
        this.legendElement.style.left = '10px'
      }
    }

    // Fallback positioning method if services fail
    private fallbackLegendPositioning(
      position: string,
      margin: number,
      legendWidth: number,
      legendHeight: number,
      paneCoords: any
    ): void {
      // Reset all positions
      this.legendElement.style.top = 'auto'
      this.legendElement.style.left = 'auto'
      this.legendElement.style.right = 'auto'
      this.legendElement.style.bottom = 'auto'
      this.legendElement.style.transform = 'none'

      // Calculate position relative to pane using configuration
      let top: number, left: number

      switch (position) {
        case 'top-left':
          top = paneCoords.bounds.top + margin
          left = paneCoords.bounds.left + margin
          break
        case 'top-right':
          top = paneCoords.bounds.top + margin
          left = paneCoords.bounds.right - legendWidth - margin
          break
        case 'bottom-left':
          top = paneCoords.bounds.bottom - legendHeight - margin
          left = paneCoords.bounds.left + margin
          break
        case 'bottom-right':
          top = paneCoords.bounds.bottom - legendHeight - margin
          left = paneCoords.bounds.right - legendWidth - margin
          break
        case 'center':
          top = paneCoords.bounds.top + paneCoords.bounds.height / 2 - legendHeight / 2
          left = paneCoords.bounds.left + paneCoords.bounds.width / 2 - legendWidth / 2
          break
        default:
          top = paneCoords.bounds.top + margin
          left = paneCoords.bounds.left + margin
      }

      // Apply positioning
      this.legendElement.style.top = `${top}px`
      this.legendElement.style.left = `${left}px`
    }

    // Auto-detect series in this pane
    private autoDetectSeries(): void {
      try {
        if (this.chartApi) {
          const allSeries = (this.chartApi as any).series || []
          const paneSeries = allSeries.filter((series: any) => {
            try {
              const seriesPaneId = (series as any).paneId || 0
              return seriesPaneId === this.paneId
            } catch {
              return false
            }
          })

          if (paneSeries.length > 0) {
            paneSeries.forEach((series: any) => this.addSeries(series))
          }
        }
      } catch (error) {
        console.warn(`⚠️ Error auto-detecting series for pane ${this.paneId}:`, error)
      }
    }

    // Update legend content
    private updateLegendContent(): void {
      if (!this.legendElement) return

      // Use configuration text if available, otherwise show series info
      if (legendConfig.text) {
        this.legendElement.innerHTML = legendConfig.text
        return
      }

      if (this.seriesList.length === 0) {
        this.legendElement.innerHTML =
          '<div style="color: #666; font-style: italic;">No series</div>'
        return
      }

      const legendItems = this.seriesList
        .map(series => {
          try {
            const seriesType = (series as any).seriesType || 'unknown'
            const seriesTitle = (series as any).options?.title || `Series ${seriesType}`

            return `
            <div style="color: #131722; font-size: 10px; margin: 2px 0;">
              ${seriesTitle}
            </div>
          `
          } catch {
            return '<div style="color: #999; font-size: 10px;">Unknown series</div>'
          }
        })
        .join('')

      this.legendElement.innerHTML = legendItems
    }

    // Update pane dimensions using the new utility
    private updatePaneDimensions(): void {
      if (!this.chartApi) return

      try {
        // For now, just log that we're using the chart API directly
        // We can integrate the utility later if needed
        const paneSize = this.chartApi.paneSize(this.paneId)
        if (paneSize) {
          // Pane dimensions retrieved from chart API
        }
      } catch (error) {
        console.warn(`⚠️ Failed to get pane ${this.paneId} dimensions:`, error)
      }
    }

    // Set up resize observer for dynamic legend repositioning
    private setupResizeObserver(): void {
      if (!this.chartApi || typeof ResizeObserver === 'undefined') return

      try {
        // Create resize observer to watch for pane size changes
        this.resizeObserver = new ResizeObserver(entries => {
          entries.forEach(entry => {
            // Check if this is a significant size change
            const {width, height} = entry.contentRect
            if (width > 10 && height > 10) {
              // Debounce the repositioning to avoid excessive updates
              if (this.resizeTimeout) {
                clearTimeout(this.resizeTimeout)
              }

              this.resizeTimeout = setTimeout(() => {
                this.positionLegend(legendConfig.position || 'top-left', legendConfig.margin || 8)
              }, 100)
            }
          })
        })

        // Observe the chart element for size changes
        const chartElement = this.chartApi.chartElement()
        if (chartElement) {
          this.resizeObserver.observe(chartElement)
        }

        // Set up periodic pane size checking for height changes
        this.setupPaneSizeMonitor()
      } catch (error) {
        console.warn(`⚠️ Failed to set up resize observer for pane ${this.paneId}:`, error)
      }
    }

    // Public method to refresh legend position (can be called externally)
    public refreshPosition(): void {
      if (this.chartApi && this.legendElement) {
        this.positionLegend(legendConfig.position || 'top-left', legendConfig.margin || 8)
      }
    }

    // Public method to update position (called from resize handlers)
    updatePosition(position: string, margin: number): void {
      this.positionLegend(position, margin)
    }

    // Set up periodic monitoring of pane size changes
    private setupPaneSizeMonitor(): void {
      if (!this.chartApi) return

      // Store initial pane dimensions
      let lastPaneSize = this.chartApi.paneSize(this.paneId)
      let lastPaneTop = 0

      if (lastPaneSize) {
        // Calculate initial pane top position
        for (let i = 0; i < this.paneId; i++) {
          const prevPaneSize = this.chartApi.paneSize(i)
          if (prevPaneSize) {
            lastPaneTop += prevPaneSize.height
          }
        }
      }

      // Set up interval to check for pane size/position changes
      const checkInterval = setInterval(() => {
        if (!this.chartApi || !this.legendElement) {
          clearInterval(checkInterval)
          return
        }

        try {
          const currentPaneSize = this.chartApi.paneSize(this.paneId)
          if (!currentPaneSize) return

          // Calculate current pane top position
          let currentPaneTop = 0
          for (let i = 0; i < this.paneId; i++) {
            const prevPaneSize = this.chartApi.paneSize(i)
            if (prevPaneSize) {
              currentPaneTop += prevPaneSize.height
            }
          }

          // Check if pane dimensions or position changed
          const sizeChanged =
            !lastPaneSize ||
            lastPaneSize.width !== currentPaneSize.width ||
            lastPaneSize.height !== currentPaneSize.height

          const positionChanged = Math.abs(lastPaneTop - currentPaneTop) > 1

          if (sizeChanged || positionChanged) {
            // Update stored values
            lastPaneSize = currentPaneSize
            lastPaneTop = currentPaneTop

            // Reposition legend
            this.positionLegend(legendConfig.position || 'top-left', legendConfig.margin || 8)
          }
        } catch (error) {
          console.warn(`⚠️ Error checking pane ${this.paneId} size:`, error)
        }
      }, 500) // Check every 500ms

      // Store interval reference for cleanup
      this.paneSizeCheckInterval = checkInterval
    }
  }

  // Create and return the plugin instance
  return new LegendPanePrimitive()
}

// Legend Pane Primitive Pane View implementation
class LegendPanePrimitivePaneView implements IPrimitivePaneView {
  private _source: any

  constructor(source: any) {
    this._source = source
  }

  update(): void {
    // No canvas rendering needed for DOM-based legends
  }

  renderer(): IPrimitivePaneRenderer {
    return new LegendPanePrimitivePaneRenderer()
  }
}

// Legend Pane Primitive Pane Renderer implementation
class LegendPanePrimitivePaneRenderer implements IPrimitivePaneRenderer {
  draw(): void {
    // No canvas drawing needed for DOM-based legends
  }

  drawBackground(): void {
    // No background drawing needed for DOM-based legends
  }
}

interface LightweightChartsProps {
  config: ComponentConfig
  height?: number | null
  width?: number | null
  onChartsReady?: () => void
}

// Performance optimization: Memoize the component to prevent unnecessary re-renders
const LightweightCharts: React.FC<LightweightChartsProps> = React.memo(
  ({config, height = 400, width = null, onChartsReady}) => {
    // Component initialization

    const chartRefs = useRef<{[key: string]: IChartApi}>({})
    const seriesRefs = useRef<{[key: string]: ISeriesApi<any>[]}>({})
    const rectanglePluginRefs = useRef<{[key: string]: any}>({})
    const signalPluginRefs = useRef<{[key: string]: SignalSeries}>({})
    const chartConfigs = useRef<{[key: string]: ChartConfig}>({})
    const resizeObserverRef = useRef<ResizeObserver | null>(null)
    const legendResizeObserverRefs = useRef<{[key: string]: ResizeObserver}>({})
    const isInitializedRef = useRef<boolean>(false)
    const isDisposingRef = useRef<boolean>(false)
    const fitContentTimeoutRef = useRef<NodeJS.Timeout | null>(null)
    const initializationTimeoutRef = useRef<NodeJS.Timeout | null>(null)
    const prevConfigRef = useRef<ComponentConfig | null>(null)
    const chartContainersRef = useRef<{[key: string]: HTMLElement}>({})
    const debounceTimersRef = useRef<{[key: string]: NodeJS.Timeout}>({})

    // Store function references to avoid dependency issues
    const functionRefs = useRef<{
      addTradeVisualization: any
      // addTradeVisualizationWhenReady: any  // Removed - no longer needed
      addAnnotations: any
      addModularTooltip: any
      addAnnotationLayers: any
      addRangeSwitcher: any
      addLegend: any
      updateLegendPositions: any
      setupAutoSizing: any
      setupChartSynchronization: any
      setupFitContent: any
      cleanupCharts: any
    }>({
      addTradeVisualization: null,
      // addTradeVisualizationWhenReady: null,  // Removed - no longer needed
      addAnnotations: null,
      addModularTooltip: null,
      addAnnotationLayers: null,
      addRangeSwitcher: null,
      addLegend: null,
      updateLegendPositions: null,
      setupAutoSizing: null,
      setupChartSynchronization: null,
      setupFitContent: null,
      cleanupCharts: null
    })

    // Performance optimization: Memoize container dimensions calculation
    const getContainerDimensions = useCallback((container: HTMLElement) => {
      const rect = container.getBoundingClientRect()
      return {
        width: rect.width,
        height: rect.height
      }
    }, [])

    // Performance optimization: Debounced resize handler
    const debouncedResizeHandler = useCallback(
      (chartId: string, chart: IChartApi, container: HTMLElement, chartConfig: ChartConfig) => {
        // Clear existing timer
        if (debounceTimersRef.current[chartId]) {
          clearTimeout(debounceTimersRef.current[chartId])
        }

        // Set new timer
        debounceTimersRef.current[chartId] = setTimeout(() => {
          try {
            const dimensions = getContainerDimensions(container)
            const newWidth = chartConfig.autoWidth
              ? dimensions.width
              : chartConfig.chart?.width || width
            const newHeight = chartConfig.autoHeight
              ? dimensions.height
              : chartConfig.chart?.height || height

            chart.resize(newWidth, newHeight)
          } catch (error) {
            // Auto-sizing resize failed
          }
        }, 100) // 100ms debounce
      },
      [width, height, getContainerDimensions]
    )

    // Function to setup auto-sizing for a chart
    const setupAutoSizing = useCallback(
      (chart: IChartApi, container: HTMLElement, chartConfig: ChartConfig) => {
        // Auto-sizing implementation
        if (chartConfig.autoSize || chartConfig.autoWidth || chartConfig.autoHeight) {
          const chartId = chart.chartElement().id || 'default'

          const resizeObserver = new ResizeObserver(() => {
            debouncedResizeHandler(chartId, chart, container, chartConfig)
          })

          resizeObserver.observe(container)
          resizeObserverRef.current = resizeObserver
        }
      },
      [debouncedResizeHandler]
    )

    const setupChartSynchronization = useCallback(
      (chart: IChartApi, chartId: string, syncConfig: SyncConfig) => {
        // Store chart reference for synchronization
        if (!chartRefs.current[chartId]) {
          chartRefs.current[chartId] = chart
        }

        // Setup crosshair synchronization
        if (syncConfig.crosshair) {
          chart.subscribeCrosshairMove(param => {
            // Synchronize crosshair across all charts
            Object.entries(chartRefs.current).forEach(([id, otherChart]) => {
              if (id !== chartId && param.time) {
                try {
                  // TODO: Implement proper crosshair synchronization
                  // The setCrosshairPosition method requires price which is not available in MouseEventParams
                  // For now, we'll skip crosshair synchronization to avoid TypeScript errors
                } catch (error) {
                  // Ignore errors for charts without series
                }
              }
            })
          })
        }

        // Setup time range synchronization
        if (syncConfig.timeRange) {
          const timeScale = chart.timeScale()
          if (timeScale) {
            timeScale.subscribeVisibleTimeRangeChange(timeRange => {
              // Synchronize time range across all charts
              Object.entries(chartRefs.current).forEach(([id, otherChart]) => {
                if (id !== chartId) {
                  try {
                    const otherTimeScale = otherChart.timeScale()
                    if (otherTimeScale && timeRange) {
                      otherTimeScale.setVisibleRange(timeRange)
                    }
                  } catch (error) {
                    // Time range synchronization failed
                  }
                }
              })
            })
          }
        }
      },
      []
    )

    const setupFitContent = useCallback((chart: IChartApi, chartConfig: ChartConfig) => {
      const timeScale = chart.timeScale()
      if (!timeScale) return

      // Track last click time for double-click detection
      let lastClickTime = 0
      const doubleClickThreshold = 300 // milliseconds

      // Check if fitContent on load is enabled
      const shouldFitContentOnLoad =
        chartConfig.chart?.timeScale?.fitContentOnLoad !== false &&
        chartConfig.chart?.fitContentOnLoad !== false

      if (shouldFitContentOnLoad) {
        // Wait for data to be loaded and then fit content
        const handleDataLoaded = async (retryCount = 0) => {
          const maxRetries = 50 // Prevent infinite loops

          if (retryCount >= maxRetries) {
            return
          }

          try {
            // Check if chart has series with data
            const series = Object.values(seriesRefs.current).flat()

            if (series.length === 0) {
              // No series yet, try again after a delay
              setTimeout(() => handleDataLoaded(retryCount + 1), 100)
              return
            }

            // Trade visualization is now handled synchronously in createSeries
            // No need to wait for trade data or call addTradeVisualizationWhenReady

            // Check if chart has a visible range (more reliable than checking series data)
            const visibleRange = timeScale.getVisibleRange()

            if (visibleRange && visibleRange.from && visibleRange.to) {
              timeScale.fitContent()
              // Trade visualization is now handled synchronously in createSeries
            } else {
              // If no visible range, try again after a short delay
              setTimeout(async () => {
                try {
                  timeScale.fitContent()
                  // Trade visualization is now handled synchronously in createSeries
                } catch (error) {
                  // fitContent after delay failed
                }
              }, 100)
            }
          } catch (error) {
            // fitContent failed
          }
        }

        // Clear any existing timeout
        if (fitContentTimeoutRef.current) {
          clearTimeout(fitContentTimeoutRef.current)
        }

        // Call fitContent after a longer delay to ensure data is loaded
        fitContentTimeoutRef.current = setTimeout(async () => {
          await handleDataLoaded()
        }, 1000) // Increased delay to wait for trade data
      }

      // Setup double-click to fit content
      const shouldHandleDoubleClick =
        chartConfig.chart?.timeScale?.handleDoubleClick !== false &&
        chartConfig.chart?.handleDoubleClick !== false

      if (shouldHandleDoubleClick) {
        // Subscribe to chart click events
        chart.subscribeClick(param => {
          const currentTime = Date.now()

          // Check if this is a double-click
          if (currentTime - lastClickTime < doubleClickThreshold) {
            try {
              timeScale.fitContent()
            } catch (error) {
              // fitContent on double-click failed
            }
            lastClickTime = 0 // Reset to prevent triple-click
          } else {
            lastClickTime = currentTime
          }
        })
      }
    }, [])

    // Performance optimization: Enhanced cleanup function with better memory management
    const cleanupCharts = useCallback(() => {
      // Cleanup charts

      // Set disposing flag to prevent async operations
      // But don't set it if this is the initial render
      if (prevConfigRef.current !== null) {
        isDisposingRef.current = true
      }

      // Clear all debounce timers
      Object.values(debounceTimersRef.current).forEach(timer => {
        if (timer) clearTimeout(timer)
      })
      debounceTimersRef.current = {}

      // Clear any pending timeouts
      if (fitContentTimeoutRef.current) {
        clearTimeout(fitContentTimeoutRef.current)
        fitContentTimeoutRef.current = null
      }

      if (initializationTimeoutRef.current) {
        clearTimeout(initializationTimeoutRef.current)
        initializationTimeoutRef.current = null
      }

      // Disconnect resize observer
      if (resizeObserverRef.current) {
        try {
          resizeObserverRef.current.disconnect()
        } catch (error) {
          // ResizeObserver already disconnected
        }
        resizeObserverRef.current = null
      }

      // Clean up signal series plugins
      Object.entries(signalPluginRefs.current).forEach(([key, signalSeries]) => {
        try {
          signalSeries.destroy()
        } catch (error) {
          // Signal series already destroyed
        }
      })

      // Clean up legend resize observers
      Object.values(legendResizeObserverRefs.current).forEach(resizeObserver => {
        try {
          resizeObserver.disconnect()
        } catch (error) {
          // ResizeObserver already disconnected
        }
      })

      // Remove all charts with better error handling
      Object.values(chartRefs.current).forEach(chart => {
        try {
          // Check if chart is still valid before removing
          if (chart && typeof chart.remove === 'function') {
            chart.remove()
          }
        } catch (error) {
          // Chart already removed or disposed
        }
      })

      // Clear references
      chartRefs.current = {}
      seriesRefs.current = {}
      rectanglePluginRefs.current = {}
      signalPluginRefs.current = {}
      chartConfigs.current = {}
      legendResizeObserverRefs.current = {}
      chartContainersRef.current = {}

      // Reset initialization flag
      isInitializedRef.current = false
    }, [])

    const addTradeVisualization = useCallback(
      async (
        chart: IChartApi,
        series: ISeriesApi<any>,
        trades: TradeConfig[],
        options: TradeVisualizationOptions,
        chartData?: any[]
      ) => {
        if (!trades || trades.length === 0) {
          return
        }

        // Verify chart is ready (should be guaranteed by lifecycle method)
        const timeScale = chart.timeScale()
        const visibleRange = timeScale.getVisibleRange()

        if (!visibleRange || !visibleRange.from || !visibleRange.to) {
          return
        }

        try {
          // Use default price scale ID for now
          const priceScaleId = 'right'

          // Create visual elements for trade visualization
          const visualElements = createTradeVisualElements(trades, options, chartData, priceScaleId)

          // Add markers to the series
          if (visualElements.markers.length > 0) {
            try {
              createSeriesMarkers(series, visualElements.markers)
            } catch (error) {
              // Error adding markers
            }
          }

          // Add rectangles using the canvas overlay approach (following official example)
          const chartId = chart.chartElement().id || 'default'

          // Use the RectangleOverlayPlugin instead of TradeRectanglePlugin
          if (!rectanglePluginRefs.current[chartId]) {
            const rectanglePlugin = new RectangleOverlayPlugin()
            rectanglePlugin.setChart(chart, series)
            rectanglePluginRefs.current[chartId] = rectanglePlugin
          }

          const rectanglePlugin = rectanglePluginRefs.current[chartId]

          // Clear existing rectangles and add new ones
          rectanglePlugin.clearRectangles()

          if (visualElements.rectangles.length > 0) {
            visualElements.rectangles.forEach((rect, index) => {
              rectanglePlugin.addRectangle(rect)
            })

            // Force redraw of the canvas overlay
            rectanglePlugin.scheduleRedraw()
          }

          // Add annotations to the series
          if (
            visualElements.annotations &&
            Array.isArray(visualElements.annotations) &&
            visualElements.annotations.length > 0
          ) {
            try {
              visualElements.annotations.forEach(annotation => {
                if ((series as any).addShape) {
                  ;(series as any).addShape(annotation)
                } else if ((series as any).setShapes) {
                  ;(series as any).setShapes([annotation])
                } else if ((series as any).addAnnotation) {
                  ;(series as any).addAnnotation(annotation)
                }
              })
            } catch (error) {
              // Error processing annotations
            }
          }
        } catch (error) {
          console.error('❌ [addTradeVisualization] Error in trade visualization:', error)
        }
      },
      []
    )

    // Trade visualization is now handled synchronously in createSeries function
    // No need for addTradeVisualizationWhenReady anymore

    const addAnnotations = useCallback(
      (chart: IChartApi, annotations: Annotation[] | {layers: any}) => {
        // Handle annotation manager structure from Python side
        let annotationsArray: Annotation[] = []

        if (annotations && typeof annotations === 'object') {
          // Check if this is an annotation manager structure (has layers)
          if ('layers' in annotations && annotations.layers) {
            // Extract annotations from all visible layers
            try {
              const layersArray = Object.values(annotations.layers)
              if (Array.isArray(layersArray)) {
                layersArray.forEach((layer: any) => {
                  if (
                    layer &&
                    layer.visible !== false &&
                    layer.annotations &&
                    Array.isArray(layer.annotations)
                  ) {
                    annotationsArray.push(...layer.annotations)
                  }
                })
              }
            } catch (error) {
              // Error processing annotation layers
            }
          } else if (Array.isArray(annotations)) {
            // Direct array of annotations
            annotationsArray = annotations
          }
        }

        // Validate annotations parameter
        if (!annotationsArray || !Array.isArray(annotationsArray)) {
          return
        }

        // Additional safety check - ensure annotations is actually an array
        try {
          if (typeof annotationsArray.forEach !== 'function') {
            return
          }
        } catch (error) {
          return
        }

        // Filter out invalid annotations
        const validAnnotations = annotationsArray.filter(
          annotation => annotation && typeof annotation === 'object' && annotation.time
        )

        if (validAnnotations.length === 0) {
          return
        }

        // Additional safety check before calling createAnnotationVisualElements
        if (!Array.isArray(validAnnotations) || typeof validAnnotations.forEach !== 'function') {
          console.error(
            'addAnnotations: validAnnotations is still not a proper array:',
            validAnnotations
          )
          return
        }

        const visualElements = createAnnotationVisualElements(validAnnotations)

        // Add markers using the markers plugin
        if (visualElements.markers.length > 0) {
          const seriesList = Object.values(seriesRefs.current).flat()
          if (seriesList.length > 0) {
            createSeriesMarkers(seriesList[0], visualElements.markers)
          }
        }

        // Add shapes using the shapes plugin
        if (visualElements.shapes.length > 0) {
          const seriesList = Object.values(seriesRefs.current).flat()
          if (seriesList.length > 0) {
            visualElements.shapes.forEach(shape => {
              try {
                if ((seriesList[0] as any).addShape) {
                  ;(seriesList[0] as any).addShape(shape)
                } else if ((seriesList[0] as any).setShapes) {
                  ;(seriesList[0] as any).setShapes([shape])
                }
              } catch (error) {
                // Error adding shape
              }
            })
          }
        }
      },
      []
    )

    const addAnnotationLayers = useCallback(
      (chart: IChartApi, layers: AnnotationLayer[] | {layers: any}) => {
        // Handle annotation manager structure from Python side
        let layersArray: AnnotationLayer[] = []

        if (layers && typeof layers === 'object') {
          // Check if this is an annotation manager structure (has layers)
          if ('layers' in layers && layers.layers) {
            // Convert layers object to array
            try {
              const layersValues = Object.values(layers.layers)
              if (Array.isArray(layersValues)) {
                layersArray = layersValues as AnnotationLayer[]
              }
            } catch (error) {
              // Error processing layers object
            }
          } else if (Array.isArray(layers)) {
            // Direct array of layers
            layersArray = layers
          }
        }

        // Validate layers parameter
        if (!layersArray || !Array.isArray(layersArray)) {
          return
        }

        layersArray.forEach((layer, index) => {
          try {
            if (!layer || typeof layer !== 'object') {
              return
            }

            if (layer.visible !== false && layer.annotations) {
              functionRefs.current.addAnnotations(chart, layer.annotations)
            }
          } catch (error) {
            // Error processing layer
          }
        })
      },
      []
    )

    const addModularTooltip = useCallback(
      (
        chart: IChartApi,
        container: HTMLElement,
        seriesList: ISeriesApi<any>[],
        chartConfig: ChartConfig
      ) => {
        if (!chartConfig.tooltipConfigs || Object.keys(chartConfig.tooltipConfigs).length === 0) {
          return
        }

        try {
          // Import tooltip plugin dynamically
          import('./tooltipPlugin')
            .then(({createTooltipPlugin}) => {
              const tooltipPlugin = createTooltipPlugin(
                chart,
                container,
                chartConfig.tooltipConfigs
              )

              // Enable tooltip
              tooltipPlugin.enable()

              // Store plugin reference for cleanup
              if (!window.chartPlugins) {
                window.chartPlugins = new Map()
              }
              window.chartPlugins.set(chart, tooltipPlugin)
            })
            .catch(error => {
              console.error('🎯 [addModularTooltip] Error loading tooltip plugin:', error)
            })
        } catch (error) {
          console.error('🎯 [addModularTooltip] Error setting up tooltip:', error)
        }
      },
      []
    )

    const addRangeSwitcher = useCallback((chart: IChartApi, rangeConfig: any) => {
      // Range switcher implementation will be added here
      // For now, this is a placeholder
    }, [])

    // Function to update legend positions when pane heights change - now handled by plugins
    const updateLegendPositions = useCallback(
      async (chart: IChartApi, legendsConfig: {[paneId: string]: LegendConfig}) => {
        // Check if component is being disposed
        if (isDisposingRef.current) {
          return
        }

        // Check if chart is valid and legends config exists
        if (!chart || !legendsConfig || Object.keys(legendsConfig).length === 0) {
          return
        }

        try {
          // Quick check if chart is still valid
          chart.chartElement()
        } catch (error) {
          return
        }

        // Additional safety check for chart validity
        try {
          chart.timeScale()
        } catch (error) {
          return
        }

        // Additional check to prevent disposal during async operations
        if (isDisposingRef.current) {
          return
        }
      },
      []
    )

    // Store legend element references for dynamic updates
    const legendElementsRef = useRef<Map<string, HTMLElement>>(new Map())
    const legendSeriesDataRef = useRef<
      Map<
        string,
        {
          series: ISeriesApi<any>
          legendConfig: LegendConfig
          paneId: number
          seriesName: string
        }[]
      >
    >(new Map())

    // Function to update legend values based on crosshair position
    const updateLegendValues = useCallback(
      (chart: IChartApi, chartId: string, param: MouseEventParams) => {
        const legendSeriesData = legendSeriesDataRef.current.get(chartId)
        if (!legendSeriesData || !param.time) {
          return
        }

        legendSeriesData.forEach(({series, legendConfig, paneId, seriesName}, index) => {
          try {
            // Safely get series options
            let seriesOptions: any = {}
            try {
              if (typeof series.options === 'function') {
                seriesOptions = series.options()
              } else if (series.options) {
                seriesOptions = series.options
              }
            } catch (error) {
              console.warn('Could not get series options:', error)
            }

            // Safely get series type
            let seriesType = 'Unknown'
            try {
              if (typeof series.seriesType === 'function') {
                seriesType = String(series.seriesType())
              } else if (series.seriesType && typeof series.seriesType === 'string') {
                seriesType = series.seriesType as any
              }
            } catch (error) {
              console.warn('Could not get series type:', error)
            }

            // Get data point at crosshair time
            const data = series.data()

            if (!data || data.length === 0) {
              return
            }

            // Find the data point closest to the crosshair time
            let closestDataPoint: any = null
            let minTimeDiff = Infinity

            for (const point of data) {
              if (
                point.time &&
                param.time &&
                typeof point.time === 'number' &&
                typeof param.time === 'number'
              ) {
                const timeDiff = Math.abs(point.time - param.time)
                if (timeDiff < minTimeDiff) {
                  minTimeDiff = timeDiff
                  closestDataPoint = point
                }
              }
            }

            if (!closestDataPoint) {
              return
            }

            // Use the stored seriesName from when the legend was created
            // This ensures consistency between creation and updates

            // Get series color
            let seriesColor = '#2196f3' // default
            if (seriesOptions.color) {
              seriesColor = seriesOptions.color
            } else if (seriesType === 'Candlestick') {
              seriesColor = '#26a69a'
            } else if (seriesType === 'Histogram') {
              seriesColor = '#ff9800'
            } else if (seriesType === 'Area') {
              seriesColor = seriesOptions.topColor || '#4caf50'
            }

            // Prepare template data with crosshair values
            const templateData = {
              title: seriesName, // Use the stored seriesName
              value:
                closestDataPoint.value || closestDataPoint.close || closestDataPoint.high || '',
              time: closestDataPoint.time || '',
              color: seriesColor,
              type: seriesType,
              ...closestDataPoint // Include all other data fields
            }

            // Find and update the legend element
            const legendElement = legendElementsRef.current.get(`${chartId}-pane-${paneId}`)
            if (!legendElement) {
              return
            }

            // Find the specific series item in the legend
            const seriesItems = legendElement.querySelectorAll('[data-series-name]')

            seriesItems.forEach(item => {
              const itemElement = item as HTMLElement
              const itemSeriesName = itemElement.getAttribute('data-series-name')

              if (itemSeriesName === seriesName) {
                if (legendConfig.text) {
                  // Update custom template with new {series} prefix system
                  let template = legendConfig.text

                  // Replace placeholders in template
                  Object.entries(templateData).forEach(([key, value]) => {
                    // Handle {series}.{key} placeholders
                    const seriesPlaceholder = `{series}.{${key}}`
                    if (template.includes(seriesPlaceholder)) {
                      template = template.replace(
                        new RegExp(seriesPlaceholder.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g'),
                        String(value)
                      )
                    }

                    // Handle fallback {key} placeholders (only for first series)
                    if (index === 0) {
                      const fallbackPlaceholder = `{${key}}`
                      if (template.includes(fallbackPlaceholder)) {
                        template = template.replace(
                          new RegExp(
                            fallbackPlaceholder.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'),
                            'g'
                          ),
                          String(value)
                        )
                      }
                    }
                  })

                  // Set the innerHTML to preserve the text content
                  itemElement.innerHTML = template

                  // Since the template already contains the correct styles, we just need to ensure they persist
                  // by applying them directly to the container and all child elements
                  const targetColor = '#131722'
                  const targetFontFamily =
                    '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
                  const targetFontSize = '10px'
                  const targetLetterSpacing = '2px'
                  const targetTextAlign = 'left'

                  // Apply styles to the container element
                  itemElement.style.setProperty('color', targetColor, 'important')
                  itemElement.style.setProperty('font-family', targetFontFamily, 'important')
                  itemElement.style.setProperty('font-size', targetFontSize, 'important')
                  itemElement.style.setProperty('letter-spacing', targetLetterSpacing, 'important')
                  itemElement.style.setProperty('text-align', targetTextAlign, 'important')

                  // Also apply to all child elements to ensure they inherit the styles
                  const childElements = itemElement.querySelectorAll('*')
                  childElements.forEach(child => {
                    if (child instanceof HTMLElement) {
                      child.style.setProperty('color', targetColor, 'important')
                      child.style.setProperty('font-family', targetFontFamily, 'important')
                      child.style.setProperty('font-size', targetFontSize, 'important')
                      child.style.setProperty('letter-spacing', targetLetterSpacing, 'important')
                      child.style.setProperty('text-align', targetTextAlign, 'important')
                    }
                  })

                  // Styles applied successfully
                } else {
                  // Update default legend format
                  const textContent = itemElement.querySelector('span:last-child') as HTMLElement
                  if (textContent) {
                    const value = templateData.value
                    const displayValue =
                      value !== null && value !== undefined && value !== ''
                        ? typeof value === 'number'
                          ? value.toFixed(2)
                          : String(value)
                        : 'N/A'
                    textContent.textContent = `${seriesName}: ${displayValue}`
                  }
                }
              }
            })
          } catch (error) {
            console.error('❌ Error updating legend for series:', error)
          }
        })
      },
      []
    )

    const addLegend = useCallback(
      async (
        chart: IChartApi,
        legendsConfig: {[paneId: string]: LegendConfig},
        seriesList: ISeriesApi<any>[]
      ) => {
        // Import the positioning engine (not currently used but kept for future use)
        // const { PositioningEngine } = await import('./services/PositioningEngine')

        // Check if component is being disposed
        if (isDisposingRef.current) {
          return
        }

        // Check if chart is valid and legends config exists
        if (
          !chart ||
          !legendsConfig ||
          Object.keys(legendsConfig).length === 0 ||
          seriesList.length === 0
        ) {
          return
        }

        try {
          // Quick check if chart is still valid
          chart.chartElement()
        } catch (error) {
          return
        }

        // Additional safety check for chart validity
        try {
          chart.timeScale()
        } catch (error) {
          return
        }

        // Additional check to prevent disposal during async operations
        if (isDisposingRef.current) {
          return
        }

        // ✅ CRITICAL: Wait for chart API to be ready and get pane information

        try {
          await retryWithBackoff(
            async () => {
              // Check if component is being disposed
              if (isDisposingRef.current) {
                throw new Error('Component disposed during retry')
              }

              // Check if chart has panes available via API
              try {
                const panes = chart.panes()

                // Verify we have enough panes for the legend config
                const maxPaneId = Math.max(...Object.keys(legendsConfig).map(id => parseInt(id)))
                if (panes.length <= maxPaneId) {
                  throw new Error(
                    `Not enough panes in chart API. Found: ${panes.length}, Need: ${maxPaneId + 1}`
                  )
                }

                return panes
              } catch (error) {
                throw new Error(`Chart panes not ready: ${error}`)
              }
            },
            10,
            200,
            'Chart API readiness check'
          ) // 10 retries with 200ms base delay (exponential backoff)
        } catch (error) {
          if (error instanceof Error && error.message === 'Component disposed during retry') {
            // Component disposed during retry
          } else {
            console.error('❌ Failed to wait for chart API:', error)
          }
          return
        }

        // Get chart ID for storing legend references
        const chartId = chart.chartElement().id || 'default'
        const legendSeriesData: {
          series: ISeriesApi<any>
          legendConfig: LegendConfig
          paneId: number
          seriesName: string
        }[] = []

        // Debug: Check for existing legend elements that might be from legacy systems
        const chartElement = chart.chartElement()

        // Check for any elements that might be legends
        const allElements = chartElement.querySelectorAll('*')
        const potentialLegends = Array.from(allElements).filter(el => {
          const text = el.textContent || ''
          return (
            text.includes('Know Sure Thing') ||
            text.includes('KST') ||
            text.includes('Legend') ||
            el.className.includes('legend') ||
            el.id.includes('legend')
          )
        })

        if (potentialLegends.length > 0) {
          // If we find "Know Sure Thing" legend, REMOVE IT from pane 0 and recreate it properly on pane 1
          const kstLegend = potentialLegends.find(el => el.textContent?.includes('Know Sure Thing'))
          if (kstLegend) {
            try {
              // Remove the incorrectly positioned legend
              kstLegend.remove()
            } catch (error) {
              console.error(`❌ Failed to remove "Know Sure Thing" legend:`, error)
            }
          }
        }

        // Group series by pane
        const seriesByPane = new Map<number, ISeriesApi<any>[]>()
        seriesList.forEach((series, index) => {
          // Try to get paneId from series options or fallback to index-based assignment
          let paneId = 0

          // Safely get series options
          let seriesOptions: any = {}
          try {
            if (typeof series.options === 'function') {
              seriesOptions = series.options()
            } else if (series.options) {
              seriesOptions = series.options
            }
          } catch (error) {
            console.warn('Could not get series options:', error)
          }

          // Get the paneId from the series configuration (backend sets this)
          let seriesPaneId: number | undefined = undefined

          // First check if paneId is at the top level of the series (camelCase from backend)
          if ((series as any).paneId !== undefined) {
            seriesPaneId = (series as any).paneId
          }
          // Then check if paneId is in the options
          else if (seriesOptions && (seriesOptions as any).paneId !== undefined) {
            seriesPaneId = (seriesOptions as any).paneId
          }

          if (seriesPaneId !== undefined) {
            // Use the backend-assigned paneId
            paneId = seriesPaneId
          } else {
            // If no paneId from backend, use default pane 0
            paneId = 0
          }

          // Safely get series type
          let seriesType = 'Unknown'
          try {
            if (typeof series.seriesType === 'function') {
              seriesType = String(series.seriesType())
            } else if (series.seriesType && typeof series.seriesType === 'string') {
              seriesType = String(series.seriesType)
            }
          } catch (error) {
            console.warn('Could not get series type:', error)
          }

          // Special handling for KST indicator - ensure it goes to pane 1
          if (
            seriesOptions.title &&
            (seriesOptions.title.includes('KST') || seriesOptions.title.includes('Know Sure Thing'))
          ) {
            paneId = 1
          }

          // Special handling for any indicator series - ensure they don't go to pane 0
          if (paneId === 0 && seriesType !== 'Candlestick' && seriesType !== 'Histogram') {
            paneId = 1
          }

          if (!seriesByPane.has(paneId)) {
            seriesByPane.set(paneId, [])
          }
          seriesByPane.get(paneId)!.push(series)
        })

        // Create legends for each pane that has a config
        seriesByPane.forEach((paneSeries, paneId) => {
          let legendConfig = legendsConfig[paneId.toString()]

          // CRITICAL: Prevent legends on pane 0 (main chart) unless explicitly configured
          if (paneId === 0 && !legendConfig) {
            return
          }

          // If no legend config exists for this pane, create a default one (but only for indicator panes)
          if (!legendConfig && paneId > 0) {
            legendConfig = {
              visible: true,
              position: 'top-left',
              margin: 8,
              backgroundColor: 'rgba(255, 255, 255, 0.95)',
              borderColor: '#e1e3e6',
              borderWidth: 1,
              borderRadius: 4,
              padding: 5,
              zIndex: 1000
            }
          }

          // Only create legend if config is visible
          if (!legendConfig.visible) {
            return
          }

          // ✅ CORRECT: Use Lightweight Charts Drawing Primitives plugin for proper pane-scoped legends
          // Get pane API to verify it exists
          let paneApi
          try {
            paneApi = chart.panes()[paneId]
            if (!paneApi) {
              console.error(`❌ Pane ${paneId} not found in chart API`)
              return
            }
          } catch (error) {
            console.error(`❌ Error accessing pane ${paneId} in chart API:`, error)
            return
          }

          // Create legend using Pane Primitives plugin for proper pane scoping
          const legendPlugin = createLegendPlugin(legendConfig, paneId, chartId, legendElementsRef)

          // Try to attach the legend plugin to the pane directly
          try {
            // Get the pane from the chart
            const pane = chart.panes()[paneId]
            if (pane && typeof pane.attachPrimitive === 'function') {
              pane.attachPrimitive(legendPlugin)
              // legendsCreated++
            } else {
              // Fallback: attach to the first series in the pane
              const firstSeries = paneSeries[0]
              if (firstSeries && typeof firstSeries.attachPrimitive === 'function') {
                firstSeries.attachPrimitive(legendPlugin)
              } else {
                console.error(`❌ Neither pane nor series support primitives for pane ${paneId}`)
                return
              }
            }
          } catch (error) {
            console.error(`❌ Failed to attach legend plugin to pane ${paneId}:`, error)
            return
          }

          // Legend is now handled by the Drawing Primitives plugin
          // No need for manual DOM manipulation

          // Legend positioning is now handled by the Drawing Primitives plugin
          // The plugin automatically positions itself within the pane context

          // Add pane title if there are multiple panes (disabled for custom templates)
          // if (seriesByPane.size > 1) {
          //   const paneTitle = document.createElement('div')
          //   paneTitle.style.cssText = `
          //     font-weight: bold;
          //     margin-bottom: 8px;
          //     border-bottom: 1px solid ${legendConfig.borderColor || '#e1e3e6'};
          //     padding-bottom: 4px;
          //   `
          //   let paneTitleText = ''
          //   if (paneId === 0) {
          //     paneTitleText = 'Main Chart'
          //   } else if (paneId === 1) {
          //     paneTitleText = 'RSI'
          //   } else if (paneId === 2) {
          //     paneTitleText = 'Volume'
          //   } else {
          //     paneTitleText = `Pane ${paneId}`
          //   }

          //   paneTitle.textContent = paneTitleText
          //   legendContainer.appendChild(paneTitle)
          // }

          // Legend items are now handled by the Drawing Primitives plugin
          // Store series data for crosshair updates
          paneSeries.forEach((series, index) => {
            legendSeriesData.push({
              series,
              legendConfig,
              paneId,
              seriesName: `Pane ${paneId}`
            })
          })

          // Legend items are now handled by the Drawing Primitives plugin
          // No need for manual DOM manipulation

          // Legend items are now handled by the Drawing Primitives plugin
          // No need for manual DOM manipulation
        })

        // Store legend series data for updates
        legendSeriesDataRef.current.set(chartId, legendSeriesData)

        // Setup crosshair event handling for legend updates
        chart.subscribeCrosshairMove(param => {
          updateLegendValues(chart, chartId, param)
        })
      },
      [updateLegendValues]
    )

    // Performance optimization: Memoized chart configuration processing
    const processedChartConfigs = useMemo(() => {
      if (!config.charts || config.charts.length === 0) return []

      return config.charts.map((chartConfig: ChartConfig, chartIndex: number) => {
        const chartId = chartConfig.chartId || `chart-${chartIndex}`

        // Chart configuration processed

        return {
          ...chartConfig,
          chartId,
          containerId: `chart-container-${chartId}`,
          chartOptions: cleanLineStyleOptions({
            width: chartConfig.chart?.autoWidth
              ? undefined
              : chartConfig.chart?.width || width || undefined,
            height: chartConfig.chart?.autoHeight
              ? undefined
              : chartConfig.chart?.height || height || undefined,
            ...chartConfig.chart
          })
        }
      })
    }, [config.charts, width, height])

    // Initialize charts
    const initializeCharts = useCallback(
      (isInitialRender = false) => {
        // Prevent re-initialization if already initialized and not disposing
        if (isInitializedRef.current && !isDisposingRef.current) {
          return
        }

        // Additional check to prevent disposal during initialization (but allow initial render)
        if (isDisposingRef.current && !isInitialRender) {
          return
        }

        // Check if we have charts to initialize
        if (!processedChartConfigs || processedChartConfigs.length === 0) {
          return
        }

        // Only clean up existing charts if this is not the initial render
        if (!isInitialRender) {
          functionRefs.current.cleanupCharts()
        }

        if (!processedChartConfigs || processedChartConfigs.length === 0) {
          return
        }

        processedChartConfigs.forEach((chartConfig: ChartConfig, chartIndex: number) => {
          const chartId = chartConfig.chartId!
          const containerId = chartConfig.containerId || `chart-container-${chartId}`

          // Find or create container
          let container = document.getElementById(containerId)
          if (!container) {
            container = document.createElement('div')
            container.id = containerId
            container.style.width = '100%'
            container.style.height = '100%'

            // Find the main chart container - try multiple selectors with caching
            let mainContainer = getCachedDOMElement('[data-testid="stHorizontalBlock"]')
            if (!mainContainer) {
              mainContainer = getCachedDOMElement('.stHorizontalBlock')
            }
            if (!mainContainer) {
              mainContainer = getCachedDOMElement('[data-testid="stVerticalBlock"]')
            }
            if (!mainContainer) {
              mainContainer = getCachedDOMElement('.stVerticalBlock')
            }
            if (!mainContainer) {
              mainContainer = getCachedDOMElement('[data-testid="stBlock"]')
            }
            if (!mainContainer) {
              mainContainer = getCachedDOMElement('.stBlock')
            }
            if (!mainContainer) {
              mainContainer = document.body
            }

            if (mainContainer) {
              mainContainer.appendChild(container)

              // Ensure container has proper dimensions
              container.style.width = '100%'
              container.style.height = '100%'
              container.style.minHeight = '300px'
              container.style.minWidth = '200px'
              container.style.display = 'block'
              container.style.position = 'relative'
              container.style.overflow = 'hidden'

              // Store container reference for performance
              chartContainersRef.current[chartId] = container
            } else {
              return
            }
          } else {
            chartContainersRef.current[chartId] = container
          }

          // Create chart in container
          try {
            // Check if container is still valid
            if (!container || !container.isConnected) {
              return
            }

            // Use pre-processed chart options
            const chartOptions = chartConfig.chartOptions || chartConfig.chart || {}

            let chart: IChartApi
            try {
              chart = createChart(container, chartOptions)
            } catch (chartError) {
              return
            }

            // Check if chart was created successfully
            if (!chart) {
              return
            }

            // Set the chart element's ID so we can retrieve it later
            const chartElement = chart.chartElement()
            if (chartElement) {
              chartElement.id = chartId
            }

            chartRefs.current[chartId] = chart

            // Store chart API reference for legend positioning
            if (!(window as any).chartApiMap) {
              ;(window as any).chartApiMap = {}
            }
            ;(window as any).chartApiMap[chartId] = chart

            // Initialize legend refresh callbacks for this chart
            if (!(window as any).legendRefreshCallbacks) {
              ;(window as any).legendRefreshCallbacks = {}
            }
            if (!(window as any).legendRefreshCallbacks[chartId]) {
              ;(window as any).legendRefreshCallbacks[chartId] = []
            }

            // Add resize observer to reposition legends when container resizes
            const resizeObserver = new ResizeObserver(entries => {
              for (const entry of entries) {
                if (entry.target === container) {
                  // Trigger legend repositioning for all panes
                  setTimeout(() => {
                    const legendElements = legendElementsRef.current
                    if (legendElements) {
                      legendElements.forEach((legendElement, key) => {
                        if (key.startsWith(chartId)) {
                          // Extract pane ID from key (format: chartId-pane-paneId)
                          const parts = key.split('-')
                          if (parts.length >= 3) {
                            const paneId = parseInt(parts[2])
                            const legendConfig = chartConfig.legends?.[paneId]
                            if (legendConfig) {
                              // Force legend to recalculate position
                              if (legendElement.classList.contains('pane-legend')) {
                                // This is a pane legend, trigger repositioning
                                const legendPlugin = (legendElement as any).__legendPlugin
                                if (
                                  legendPlugin &&
                                  typeof legendPlugin.updatePosition === 'function'
                                ) {
                                  legendPlugin.updatePosition(
                                    legendConfig.position,
                                    legendConfig.margin
                                  )
                                }
                              }
                            }
                          }
                        }
                      })
                    }
                  }, 100) // Small delay to ensure resize is complete
                }
              }
            })

            // Start observing the container for size changes
            resizeObserver.observe(container)

            // Store the observer reference for cleanup
            if (!(window as any).chartResizeObservers) {
              ;(window as any).chartResizeObservers = {}
            }
            ;(window as any).chartResizeObservers[chartId] = resizeObserver

            // Calculate chart dimensions once
            const containerRect = container.getBoundingClientRect()
            const chartWidth = chartConfig.autoWidth
              ? containerRect.width
              : chartOptions.width || width || containerRect.width
            const chartHeight = chartConfig.autoHeight
              ? containerRect.height
              : chartOptions.height || height || containerRect.height

            // Ensure minimum dimensions
            const finalWidth = Math.max(chartWidth, 200)
            const finalHeight = Math.max(chartHeight, 200)

            // Resize chart once with calculated dimensions
            chart.resize(finalWidth, finalHeight)

            // Apply layout.panes options if present
            if (chartOptions.layout && chartOptions.layout.panes) {
              chart.applyOptions({layout: {panes: chartOptions.layout.panes}})
            }

            // Create panes if needed for multi-pane charts
            const paneMap = new Map<number, any>()
            let existingPanes = chart.panes()

            // Ensure we have enough panes for the series
            chartConfig.series.forEach((seriesConfig: SeriesConfig) => {
              const paneId = seriesConfig.paneId || 0
              if (!paneMap.has(paneId)) {
                if (paneId < existingPanes.length) {
                  paneMap.set(paneId, existingPanes[paneId])
                } else {
                  // Create new pane if it doesn't exist
                  const newPane = chart.addPane()
                  paneMap.set(paneId, newPane)
                  // Update existingPanes after adding new pane
                  existingPanes = chart.panes()
                }
              }
            })

            // Note: Pane heights will be applied AFTER series creation to ensure all panes exist

            // Configure overlay price scales (volume, indicators, etc.) if they exist
            if (chartConfig.chart?.overlayPriceScales) {
              Object.entries(chartConfig.chart.overlayPriceScales).forEach(
                ([scaleId, scaleConfig]) => {
                  try {
                    // Create overlay price scale - use the scaleId directly
                    const overlayScale = chart.priceScale(scaleId)
                    if (overlayScale) {
                      overlayScale.applyOptions(cleanLineStyleOptions(scaleConfig as any))
                    } else {
                      // Price scale not found, will be created when series uses it
                    }
                  } catch (error) {
                    // Failed to configure price scale
                  }
                }
              )
            }

            // Create series for this chart
            const seriesList: ISeriesApi<any>[] = []

            if (chartConfig.series && Array.isArray(chartConfig.series)) {
              chartConfig.series.forEach((seriesConfig: SeriesConfig, seriesIndex: number) => {
                try {
                  if (!seriesConfig || typeof seriesConfig !== 'object') {
                    return
                  }

                  // Pass trade data to the first series (candlestick series) for marker creation
                  if (
                    seriesIndex === 0 &&
                    chartConfig.trades &&
                    chartConfig.trades.length > 0 &&
                    chartConfig.tradeVisualizationOptions
                  ) {
                    seriesConfig.trades = chartConfig.trades
                    seriesConfig.tradeVisualizationOptions = chartConfig.tradeVisualizationOptions
                  }

                  const series = createSeries(
                    chart,
                    seriesConfig,
                    {signalPluginRefs},
                    chartId,
                    seriesIndex
                  )
                  if (series) {
                    seriesList.push(series)

                    // Apply overlay price scale configuration if this series uses one
                    if (
                      seriesConfig.priceScaleId &&
                      seriesConfig.priceScaleId !== 'right' &&
                      seriesConfig.priceScaleId !== 'left' &&
                      chartConfig.chart?.overlayPriceScales?.[seriesConfig.priceScaleId]
                    ) {
                      const scaleConfig =
                        chartConfig.chart.overlayPriceScales[seriesConfig.priceScaleId]
                      try {
                        const priceScale = series.priceScale()
                        if (priceScale) {
                          priceScale.applyOptions(cleanLineStyleOptions(scaleConfig as any))
                        }
                      } catch (error) {
                        // Failed to apply price scale configuration for series
                      }
                    }

                    // Trade visualization is now handled in createSeries function
                    // No need to call addTradeVisualization here anymore

                    // Add series-level annotations
                    if (seriesConfig.annotations) {
                      functionRefs.current.addAnnotations(chart, seriesConfig.annotations)
                    }
                  } else {
                    // Failed to create series
                  }
                } catch (seriesError) {
                  console.error(
                    `Error creating series at index ${seriesIndex} for chart ${chartId}:`,
                    seriesError
                  )
                }
              })
            } else {
              // No valid series configuration found
            }

            seriesRefs.current[chartId] = seriesList

            // Process pending trade rectangles after all series are created
            if (
              (chart as any)._pendingTradeRectangles &&
              (chart as any)._pendingTradeRectangles.length > 0
            ) {
              ;(chart as any)._pendingTradeRectangles.forEach((pendingData: any, index: number) => {
                try {
                  // Create rectangle plugin for this chart if it doesn't exist
                  const chartId = pendingData.chartId || 'default'
                  // Create TradeRectanglePlugin for this chart if it doesn't exist
                  if (!rectanglePluginRefs.current[chartId]) {
                    const tradeRectanglePlugin = new TradeRectanglePlugin(chart, 'right')
                    tradeRectanglePlugin.setRectangles(pendingData.rectangles)

                    // Attach the primitive to the first series
                    if (seriesList.length > 0) {
                      seriesList[0].attachPrimitive(tradeRectanglePlugin)
                    }

                    rectanglePluginRefs.current[chartId] = tradeRectanglePlugin
                  } else {
                    // Update existing plugin with new rectangles
                    const existingPlugin = rectanglePluginRefs.current[chartId]
                    existingPlugin.setRectangles(pendingData.rectangles)
                  }
                } catch (error) {
                  console.error(
                    '❌ [initializeCharts] Error processing trade rectangles set',
                    index + 1,
                    ':',
                    error
                  )
                }
              })

              // Clear the pending rectangles after processing
              ;(chart as any)._pendingTradeRectangles = []
            }

            // Apply pane heights configuration AFTER series creation to ensure all panes exist
            if (chartConfig.chart?.layout?.paneHeights) {
              // Get all panes after series creation
              const allPanes = chart.panes()

              Object.entries(chartConfig.chart.layout.paneHeights).forEach(
                ([paneIdStr, heightOptions]) => {
                  const paneId = parseInt(paneIdStr)
                  const options = heightOptions as PaneHeightOptions

                  if (paneId < allPanes.length && options.factor) {
                    try {
                      allPanes[paneId].setStretchFactor(options.factor)
                    } catch (error) {
                      // Failed to set stretch factor for pane
                    }
                  } else {
                    // Skipping pane
                  }
                }
              )
            }

            // Add modular tooltip system
            functionRefs.current.addModularTooltip(chart, container, seriesList, chartConfig)

            // Store chart config for trade visualization when chart is ready
            chartConfigs.current[chartId] = chartConfig

            // Add chart-level annotations
            if (chartConfig.annotations) {
              functionRefs.current.addAnnotations(chart, chartConfig.annotations)
            }

            // Add annotation layers
            if (chartConfig.annotationLayers) {
              functionRefs.current.addAnnotationLayers(chart, chartConfig.annotationLayers)
            }

            // Add price lines
            if (chartConfig.priceLines && seriesList.length > 0) {
              chartConfig.priceLines.forEach((priceLine: any) => {
                seriesList[0].createPriceLine(priceLine)
              })
            }

            // Add range switcher if configured
            if (chartConfig.chart?.rangeSwitcher && chartConfig.chart.rangeSwitcher.visible) {
              // Add range switcher after a short delay to ensure chart is fully initialized
              setTimeout(() => {
                functionRefs.current.addRangeSwitcher(chart, chartConfig.chart.rangeSwitcher)
              }, 100)
            }

            // Ensure chart is properly initialized before adding legends and other features
            setTimeout(() => {
              if (!isDisposingRef.current && chartRefs.current[chartId]) {
                try {
                  // Force chart to fit content
                  chart.timeScale().fitContent()

                  // Add legends if configured
                  if (chartConfig.legends && Object.keys(chartConfig.legends).length > 0) {
                    try {
                      functionRefs.current.addLegend(chart, chartConfig.legends, seriesList)
                    } catch (error) {
                      console.error('🎯 Error calling addLegend:', error)
                    }

                    // Add resize listener to update legend positions when pane heights change
                    const resizeObserver = new ResizeObserver(() => {
                      if (!isDisposingRef.current) {
                        functionRefs.current.updateLegendPositions(chart, chartConfig.legends)
                      }
                    })

                    // Observe the chart element for size changes
                    const chartElement = chart.chartElement()
                    if (chartElement) {
                      resizeObserver.observe(chartElement)
                    }

                    // Store the resize observer for cleanup
                    legendResizeObserverRefs.current[chartId] = resizeObserver

                    // Refresh all legends after chart is fully initialized
                    setTimeout(() => {
                      try {
                        // This will trigger legend refresh for all panes
                        if (
                          window.legendRefreshCallbacks &&
                          window.legendRefreshCallbacks[chartId]
                        ) {
                          window.legendRefreshCallbacks[chartId].forEach((callback: () => void) => {
                            callback()
                          })
                        }
                      } catch (error) {
                        console.warn('Error refreshing legends after initialization:', error)
                      }
                    }, 500) // Wait 500ms for legends to be fully created
                  }
                } catch (error) {
                  console.warn('Error during chart initialization:', error)
                }
              }
            }, 200) // Increased delay to ensure chart is fully ready

            // Setup auto-sizing for the chart
            functionRefs.current.setupAutoSizing(chart, container, chartConfig)

            // Setup chart synchronization if enabled
            if (config.syncConfig && config.syncConfig.enabled) {
              functionRefs.current.setupChartSynchronization(chart, chartId, config.syncConfig)
            }

            // Setup fitContent functionality
            functionRefs.current.setupFitContent(chart, chartConfig)

            // Call fitContent after all series are created and data is loaded
            const shouldFitContentOnLoad =
              chartConfig.chart?.timeScale?.fitContentOnLoad !== false &&
              chartConfig.chart?.fitContentOnLoad !== false

            if (shouldFitContentOnLoad && seriesList.length > 0) {
              // Call fitContent after a delay to ensure all data is processed
              setTimeout(() => {
                try {
                  const timeScale = chart.timeScale()
                  if (timeScale) {
                    timeScale.fitContent()
                  }
                } catch (error) {
                  // fitContent failed
                }
              }, 100)
            }
          } catch (error) {
            console.error('Error creating chart:', error)
          }
        })

        isInitializedRef.current = true

        // Small delay to ensure charts are rendered before any cleanup
        setTimeout(() => {
          // Notify parent component that charts are ready
          if (onChartsReady) {
            onChartsReady()
          }
        }, 50)
      },
      [processedChartConfigs, config.syncConfig, width, height, onChartsReady]
    )

    // Update function references to avoid dependency issues
    useEffect(() => {
      functionRefs.current = {
        addTradeVisualization,
        // addTradeVisualizationWhenReady,  // Removed - no longer needed
        addAnnotations,
        addModularTooltip,
        addAnnotationLayers,
        addRangeSwitcher,
        addLegend,
        updateLegendPositions,
        setupAutoSizing,
        setupChartSynchronization,
        setupFitContent,
        cleanupCharts
      }
    }, [
      addTradeVisualization,
      addAnnotations,
      addModularTooltip,
      addAnnotationLayers,
      addRangeSwitcher,
      addLegend,
      updateLegendPositions,
      setupAutoSizing,
      setupChartSynchronization,
      setupFitContent,
      cleanupCharts
    ])

    // Stabilize the config dependency to prevent unnecessary re-initialization
    const stableConfig = useMemo(() => config, [config])

    useEffect(() => {
      if (stableConfig && stableConfig.charts && stableConfig.charts.length > 0) {
        initializeCharts(true)
      }
    }, [stableConfig, initializeCharts])

    // Cleanup on unmount
    useEffect(() => {
      return () => {
        cleanupCharts()
      }
    }, [cleanupCharts])

    // Memoize the chart containers to prevent unnecessary re-renders
    const chartContainers = useMemo(() => {
      if (!config.charts || config.charts.length === 0) {
        return []
      }

      return config.charts.map((chartConfig, index) => {
        const chartId = chartConfig.chartId || `chart-${index}`
        const containerId = `chart-container-${chartId}`

        // Determine container styling based on auto-sizing options
        const shouldAutoSize =
          chartConfig.autoSize || chartConfig.autoWidth || chartConfig.autoHeight
        const chartOptions = chartConfig.chart || {}

        // Use optimized style creation with memoization
        const styles = createOptimizedStyles(width, height, !!shouldAutoSize, chartOptions)
        const containerStyle = {
          ...styles.container,
          minWidth:
            chartOptions.minWidth || chartConfig.minWidth || (shouldAutoSize ? 200 : undefined),
          minHeight:
            chartOptions.minHeight || chartConfig.minHeight || (shouldAutoSize ? 200 : undefined),
          maxWidth: chartOptions.maxWidth || chartConfig.maxWidth,
          maxHeight: chartOptions.maxHeight || chartConfig.maxHeight
        }

        const chartContainerStyle = styles.chartContainer

        return (
          <div key={chartId} style={containerStyle}>
            <div id={containerId} style={chartContainerStyle} />
          </div>
        )
      })
    }, [config.charts, width, height])

    if (!config.charts || config.charts.length === 0) {
      return <div>No charts configured</div>
    }

    return (
      <ErrorBoundary>
        <div style={{display: 'flex', flexDirection: 'column', gap: '20px'}}>{chartContainers}</div>
      </ErrorBoundary>
    )
  }
)

export default LightweightCharts
