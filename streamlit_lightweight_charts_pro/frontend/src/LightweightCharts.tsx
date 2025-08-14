import React, { useEffect, useRef, useCallback, useMemo, MutableRefObject } from 'react'
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
  PaneHeightOptions,
} from './types'
import { createTradeVisualElements } from './tradeVisualization'
import { RectangleOverlayPlugin } from './rectanglePlugin'
import { createAnnotationVisualElements } from './annotationSystem'
import { SignalSeries } from './signalSeriesPlugin'

import { cleanLineStyleOptions } from './utils/lineStyle'
import { createSeries } from './utils/seriesFactory'
import {
  getCachedDOMElement,
  createOptimizedStyles
} from './utils/performance'
import { ErrorBoundary } from './components/ErrorBoundary'

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
        console.log(`❌ ${operationName} failed after ${maxRetries} attempts:`, lastError.message)
        throw lastError
      }

      // Exponential backoff with jitter
      const delay = baseDelay * Math.pow(2, attempt) + Math.random() * 100
      console.log(`⏳ ${operationName} attempt ${attempt + 1}/${maxRetries} failed, retrying in ${Math.round(delay)}ms...`)
      await new Promise(resolve => setTimeout(resolve, delay))
    }
  }

  throw lastError
}

// ✅ Create Legend Plugin using Pane Primitives for proper pane scoping
const createLegendPlugin = (legendConfig: any, paneId: number, chartId: string, legendElementsRef: MutableRefObject<Map<string, HTMLElement>>) => {
  // Create a proper Pane Primitives plugin that renders DOM elements
  class LegendPanePrimitive implements IPanePrimitive<Time> {
    private _paneViews: LegendPanePrimitivePaneView[]
    private legendElement: HTMLElement | null = null
    private paneId: number
    private seriesList: ISeriesApi<any>[] = []
    
    constructor() {
      this._paneViews = [new LegendPanePrimitivePaneView(this)]
      this.paneId = paneId
    }
    
    // Required IPanePrimitive interface methods
    attached(param: PaneAttachedParameter<Time>): void {
      console.log(`🎯 Legend pane plugin attached to pane ${this.paneId}`)
      
      // Create the actual DOM element when attached
      this.createPaneLegend()
      
      // Wait for the next chart render cycle to position the legend
      if (param.chart) {
        console.log(`⏳ Waiting for chart render cycle for pane ${this.paneId}`)
        // Use requestAnimationFrame to wait for the next render cycle
        requestAnimationFrame(() => {
          // Then use setTimeout to ensure DOM is fully ready
          setTimeout(() => {
            // console.log(`🎯 Attempting to position legend after render cycle for pane ${this.paneId}`)
            this.retryPositionLegend(legendConfig.position || 'top-left', legendConfig.margin || 4)
          }, 100)
        })
      }
    }
    
    detached(): void {
      console.log(`🎯 Legend pane plugin detached from pane ${this.paneId}`)
      if (this.legendElement && this.legendElement.parentNode) {
        this.legendElement.parentNode.removeChild(this.legendElement)
      }
      this.legendElement = null
      this.seriesList = []
    }
    
    paneViews(): IPrimitivePaneView[] {
      return this._paneViews
    }
    
    // Add series to this pane's legend
    addSeries(series: ISeriesApi<any>): void {
      this.seriesList.push(series)
      this.updateLegendContent()
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
      
      // Apply basic styling (positioning will be handled later)
      this.legendElement.style.position = 'absolute'
      this.legendElement.style.zIndex = (legendConfig.zIndex || 1000).toString()
      this.legendElement.style.pointerEvents = 'none'
      
      // Create initial legend content
      this.updateLegendContent()
      
      // Append to chart element first
      try {
        const chartElement = document.querySelector(`[data-chart-id="${chartId}"]`) || 
                            document.querySelector('.tv-lightweight-charts')
        
        if (chartElement && this.legendElement) {
          chartElement.appendChild(this.legendElement)
          // console.log(`✅ Added legend DOM element to chart for pane ${this.paneId}`)
        } else {
          console.error(`❌ Could not access chart element for pane ${this.paneId}`)
        }
        
        // Store reference for updates using a unique key
        const legendKey = `${chartId}-pane-${this.paneId}`
        console.log(`✅ Legend stored with key: ${legendKey}`)
        
        // Also store in legendElementsRef for backward compatibility with updateLegendValues
        if (legendElementsRef.current) {
          legendElementsRef.current.set(legendKey, this.legendElement)
          console.log(`✅ Stored legend in legendElementsRef for key: ${legendKey}`)
        }
        
        // Legend positioning will be handled by the attached method after render cycle
        console.log(`🚀 Legend creation complete for pane ${this.paneId}, positioning will be handled after render cycle`)
        
      } catch (error) {
        console.error(`❌ Error adding legend to pane ${this.paneId}:`, error)
      }
    }
    
    // Retry positioning with delay to ensure DOM is ready
    private retryPositionLegend(position: string, margin: number, attempts: number = 0): void {
      const maxAttempts = 10 // Increased max attempts
      const delay = 200 * Math.pow(2, attempts) // Longer delays: 200ms, 400ms, 800ms, 1600ms, 3200ms...
      
      console.log(`⏰ Scheduling retry positioning for pane ${this.paneId}, attempt ${attempts + 1}/${maxAttempts}, delay: ${delay}ms`)
      
      setTimeout(() => {
        console.log(`⏰ Executing retry positioning for pane ${this.paneId}, attempt ${attempts + 1}`)
        if (this.calculatePaneRelativePosition(position, margin)) {
          console.log(`✅ Successfully positioned legend for pane ${this.paneId} on attempt ${attempts + 1}`)
        } else if (attempts < maxAttempts) {
          console.log(`⏳ Retrying legend positioning for pane ${this.paneId}, attempt ${attempts + 1}/${maxAttempts}`)
          this.retryPositionLegend(position, margin, attempts + 1)
        } else {
          console.warn(`⚠️ Failed to position legend for pane ${this.paneId} after ${maxAttempts} attempts, using default positioning`)
          this.applyDefaultPosition(position, margin)
        }
      }, delay)
    }
    
    // Unified positioning method - handles all positioning logic
    private positionLegend(position: string, margin: number): void {
      if (!this.legendElement) return
      
      // Reset all positions first
      this.legendElement.style.top = 'auto'
      this.legendElement.style.left = 'auto'
      this.legendElement.style.right = 'auto'
      this.legendElement.style.bottom = 'auto'
      this.legendElement.style.transform = 'none'
      
      // Calculate pane-specific positioning
      this.calculatePaneRelativePosition(position, margin)
      
      console.log(`✅ Positioned legend for pane ${this.paneId} at ${position}`)
    }
    
    // Calculate position relative to the actual pane boundaries
    private calculatePaneRelativePosition(position: string, margin: number): boolean {
      if (!this.legendElement) return false
      
      try {
        // Find the chart element
        const chartElement = document.querySelector(`[data-chart-id="${chartId}"]`) || 
                            document.querySelector('.tv-lightweight-charts')
        
        if (!chartElement) {
          console.warn(`⚠️ Could not find chart element for pane ${this.paneId}, using default positioning`)
          this.applyDefaultPosition(position, margin)
          return false
        }
        
        // Try to get pane information from the chart API instead of DOM
        const chartApi = (window as any).chartApiMap?.[chartId]
        if (chartApi && chartApi.paneSize) {
          try {
            // Get exact pane dimensions and position using chart.paneSize(paneId)
            const paneSize = chartApi.paneSize(this.paneId)
            if (paneSize) {
              console.log(`🔍 Pane ${this.paneId} dimensions from chart.paneSize():`, paneSize)
              
              // Check if pane dimensions are valid (not too small)
              if (paneSize.width < 10 || paneSize.height < 10) {
                console.log(`⏳ Pane ${this.paneId} dimensions too small (${paneSize.width}x${paneSize.height}), waiting for proper sizing...`)
                return false // This will trigger a retry
              }
              
              this.legendElement.style.top = 'auto'
              this.legendElement.style.left = 'auto'
              this.legendElement.style.right = 'auto'
              this.legendElement.style.bottom = 'auto'
              this.legendElement.style.transform = 'none'
              
              switch (position) {
                case 'top-left':
                  this.legendElement.style.top = `${paneSize.top + margin}px`
                  this.legendElement.style.left = `${paneSize.left + margin}px`
                  break
                case 'top-right':
                  this.legendElement.style.top = `${paneSize.top + margin}px`
                  this.legendElement.style.left = `${paneSize.left + paneSize.width - this.legendElement.offsetWidth - margin}px`
                  break
                case 'bottom-left':
                  this.legendElement.style.top = `${paneSize.top + paneSize.height - this.legendElement.offsetHeight - margin}px`
                  this.legendElement.style.left = `${paneSize.left + margin}px`
                  break
                case 'bottom-right':
                  this.legendElement.style.top = `${paneSize.top + paneSize.height - this.legendElement.offsetHeight - margin}px`
                  this.legendElement.style.left = `${paneSize.left + paneSize.width - this.legendElement.offsetWidth - margin}px`
                  break
                case 'center':
                  this.legendElement.style.top = `${paneSize.top + (paneSize.height / 2) - (this.legendElement.offsetHeight / 2)}px`
                  this.legendElement.style.left = `${paneSize.left + (paneSize.width / 2) - (this.legendElement.offsetWidth / 2)}px`
                  break
                default:
                  this.legendElement.style.top = `${paneSize.top + margin}px`
                  this.legendElement.style.left = `${paneSize.left + margin}px`
              }
              
              console.log(`✅ Applied exact pane-relative positioning for pane ${this.paneId} using chart.paneSize()`)
              return true
              
            } else {
              console.warn(`⚠️ chart.paneSize(${this.paneId}) returned null/undefined`)
            }
          } catch (apiError) {
            console.warn(`⚠️ Could not use chart.paneSize(${this.paneId}), falling back to DOM:`, apiError)
          }
        }
        
        // Fallback: try to find pane elements in DOM
        const paneElements = chartElement.querySelectorAll('.tv-lightweight-charts-pane')
        if (paneElements.length <= this.paneId) {
          console.warn(`⚠️ Could not find pane ${this.paneId} element, using default positioning`)
          this.applyDefaultPosition(position, margin)
          return false
        }
        
        const paneElement = paneElements[this.paneId] as HTMLElement
        const paneRect = paneElement.getBoundingClientRect()
        const chartRect = chartElement.getBoundingClientRect()
        
        const relativeTop = paneRect.top - chartRect.top
        const relativeLeft = paneRect.left - chartRect.left
        const paneWidth = paneRect.width
        const paneHeight = paneRect.height
        
        console.log(`🔍 Pane ${this.paneId} dimensions from DOM:`, {
          top: relativeTop,
          left: relativeLeft,
          width: paneWidth,
          height: paneHeight
        })
        
        this.legendElement.style.top = 'auto'
        this.legendElement.style.left = 'auto'
        this.legendElement.style.right = 'auto'
        this.legendElement.style.bottom = 'auto'
        this.legendElement.style.transform = 'none'
        
        switch (position) {
          case 'top-left':
            this.legendElement.style.top = `${relativeTop + margin}px`
            this.legendElement.style.left = `${relativeLeft + margin}px`
            break
          case 'top-right':
            this.legendElement.style.top = `${relativeTop + margin}px`
            this.legendElement.style.left = `${relativeLeft + paneWidth - this.legendElement.offsetWidth - margin}px`
            break
          case 'bottom-left':
            this.legendElement.style.top = `${relativeTop + paneHeight - this.legendElement.offsetHeight - margin}px`
            this.legendElement.style.left = `${relativeLeft + margin}px`
            break
          case 'bottom-right':
            this.legendElement.style.top = `${relativeTop + paneHeight - this.legendElement.offsetHeight - margin}px`
            this.legendElement.style.left = `${relativeLeft + paneWidth - this.legendElement.offsetWidth - margin}px`
            break
          case 'center':
            this.legendElement.style.top = `${relativeTop + (paneHeight / 2) - (this.legendElement.offsetHeight / 2)}px`
            this.legendElement.style.left = `${relativeLeft + (paneWidth / 2) - (this.legendElement.offsetWidth / 2)}px`
            break
          default:
            this.legendElement.style.top = `${relativeTop + margin}px`
            this.legendElement.style.left = `${relativeLeft + margin}px`
        }
        
        console.log(`✅ Applied pane-relative positioning for pane ${this.paneId}`)
        return true
        
      } catch (error) {
        console.error(`❌ Error calculating pane-relative position for pane ${this.paneId}:`, error)
        this.applyDefaultPosition(position, margin)
        return false
      }
    }
    
    // Fallback to default positioning if pane positioning fails
    private applyDefaultPosition(position: string, margin: number): void {
      if (!this.legendElement) return
      
      // Apply position-specific styling relative to chart
      switch (position) {
        case 'top-left':
          this.legendElement.style.top = `${margin}px`
          this.legendElement.style.left = `${margin}px`
          break
        case 'top-right':
          this.legendElement.style.top = `${margin}px`
          this.legendElement.style.right = `${margin}px`
          break
        case 'bottom-left':
          this.legendElement.style.bottom = `${margin}px`
          this.legendElement.style.left = `${margin}px`
          break
        case 'bottom-right':
          this.legendElement.style.bottom = `${margin}px`
          this.legendElement.style.right = `${margin}px`
          break
        case 'center':
          this.legendElement.style.top = '50%'
          this.legendElement.style.left = '50%'
          this.legendElement.style.transform = 'translate(-50%, -50%)'
          break
        default:
          this.legendElement.style.top = `${margin}px`
          this.legendElement.style.left = `${margin}px`
      }
      
      console.log(`⚠️ Applied default positioning for pane ${this.paneId}`)
    }
    
    // Public method to update legend position (can be called externally)
    updatePosition(newPosition: string, newMargin?: number): void {
      const margin = newMargin ?? (legendConfig.margin || 4)
      this.positionLegend(newPosition, margin)
    }
    
    // Update legend content to show all series in this pane
    private updateLegendContent(): void {
      if (!this.legendElement) return
      
      // Get pane title
      let paneTitle = 'Pane'
      if (this.paneId === 0) {
        paneTitle = 'Main Chart'
      } else if (this.paneId === 1) {
        paneTitle = 'RSI'
      } else if (this.paneId === 2) {
        paneTitle = 'Volume'
      } else {
        paneTitle = `Pane ${this.paneId}`
      }
      
      // Create legend content showing all series
      let seriesContent = ''
      this.seriesList.forEach((series, index) => {
        const seriesOptions = series.options()
        const seriesTitle = seriesOptions.title || `Series ${index + 1}`
        const seriesColor = seriesOptions.color || '#2962FF'
        
        seriesContent += `
          <div style="
            display: flex;
            align-items: center;
            margin-bottom: ${index < this.seriesList.length - 1 ? '4px' : '0'};
          ">
            <span style="
              display: inline-block;
              width: 10px;
              height: 10px;
              background-color: ${seriesColor};
              border-radius: 2px;
              margin-right: 6px;
              flex-shrink: 0;
            "></span>
            <span style="
              font-size: 9px;
              color: ${legendConfig.color || '#131722'};
            ">${seriesTitle}</span>
          </div>
        `
      })
      
      this.legendElement.innerHTML = `
        <div style="
          background-color: ${legendConfig.backgroundColor || 'rgba(255, 255, 255, 0.95)'};
          border: ${legendConfig.borderWidth || 1}px solid ${legendConfig.borderColor || '#e1e3e6'};
          border-radius: ${legendConfig.borderRadius || 4}px;
          padding: ${legendConfig.padding || 5}px;
          margin: ${legendConfig.margin || 4}px;
          font-size: ${legendConfig.fontSize || '10px'};
          color: ${legendConfig.color || '#131722'};
          font-family: ${legendConfig.fontFamily || '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'};
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
          pointer-events: auto;
          user-select: none;
          min-width: 120px;
          font-weight: 500;
        ">
          <div style="
            font-weight: 600;
            margin-bottom: 6px;
            padding-bottom: 4px;
            border-bottom: 1px solid ${legendConfig.borderColor || '#e1e3e6'};
            color: ${legendConfig.color || '#131722'};
          ">${paneTitle}</div>
          ${seriesContent || '<div style="color: #999; font-style: italic;">No series</div>'}
        </div>
      `
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
const LightweightCharts: React.FC<LightweightChartsProps> = React.memo(({ config, height = 400, width = null, onChartsReady }) => {
  const chartRefs = useRef<{ [key: string]: IChartApi }>({})
  const seriesRefs = useRef<{ [key: string]: ISeriesApi<any>[] }>({})
  const rectanglePluginRefs = useRef<{ [key: string]: any }>({})
  const signalPluginRefs = useRef<{ [key: string]: SignalSeries }>({})
  const chartConfigs = useRef<{ [key: string]: ChartConfig }>({})
  const resizeObserverRef = useRef<ResizeObserver | null>(null)
  const legendResizeObserverRefs = useRef<{ [key: string]: ResizeObserver }>({})
  const isInitializedRef = useRef<boolean>(false)
  const isDisposingRef = useRef<boolean>(false)
  const fitContentTimeoutRef = useRef<NodeJS.Timeout | null>(null)
  const initializationTimeoutRef = useRef<NodeJS.Timeout | null>(null)
  const prevConfigRef = useRef<ComponentConfig | null>(null)
  const chartContainersRef = useRef<{ [key: string]: HTMLElement }>({})
  const debounceTimersRef = useRef<{ [key: string]: NodeJS.Timeout }>({})

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
  const debouncedResizeHandler = useCallback((chartId: string, chart: IChartApi, container: HTMLElement, chartConfig: ChartConfig) => {
    // Clear existing timer
    if (debounceTimersRef.current[chartId]) {
      clearTimeout(debounceTimersRef.current[chartId])
    }

    // Set new timer
    debounceTimersRef.current[chartId] = setTimeout(() => {
      try {
        const dimensions = getContainerDimensions(container)
        const newWidth = chartConfig.autoWidth ? dimensions.width : chartConfig.chart?.width || width
        const newHeight = chartConfig.autoHeight ? dimensions.height : chartConfig.chart?.height || height

        chart.resize(newWidth, newHeight)
      } catch (error) {
        // Auto-sizing resize failed
      }
    }, 100) // 100ms debounce
  }, [width, height, getContainerDimensions])

  // Function to setup auto-sizing for a chart
  const setupAutoSizing = useCallback((chart: IChartApi, container: HTMLElement, chartConfig: ChartConfig) => {
    // Auto-sizing implementation
    if (chartConfig.autoSize || chartConfig.autoWidth || chartConfig.autoHeight) {
      const chartId = chart.chartElement().id || 'default'

      const resizeObserver = new ResizeObserver(() => {
        debouncedResizeHandler(chartId, chart, container, chartConfig)
      })

      resizeObserver.observe(container)
      resizeObserverRef.current = resizeObserver
    }
  }, [debouncedResizeHandler])

  const setupChartSynchronization = useCallback((chart: IChartApi, chartId: string, syncConfig: SyncConfig) => {
    // Store chart reference for synchronization
    if (!chartRefs.current[chartId]) {
      chartRefs.current[chartId] = chart
    }

    // Setup crosshair synchronization
    if (syncConfig.crosshair) {
      chart.subscribeCrosshairMove((param) => {
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
        timeScale.subscribeVisibleTimeRangeChange((timeRange) => {
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
  }, [])

  const setupFitContent = useCallback((chart: IChartApi, chartConfig: ChartConfig) => {
    const timeScale = chart.timeScale()
    if (!timeScale) return

    // Track last click time for double-click detection
    let lastClickTime = 0
    const doubleClickThreshold = 300 // milliseconds

    // Check if fitContent on load is enabled
    const shouldFitContentOnLoad = chartConfig.chart?.timeScale?.fitContentOnLoad !== false &&
      chartConfig.chart?.fitContentOnLoad !== false

    if (shouldFitContentOnLoad) {
      // Wait for data to be loaded and then fit content
      const handleDataLoaded = async (retryCount = 0) => {
        const maxRetries = 50; // Prevent infinite loops
        const currentChartId = chart.chartElement().id || 'default';

        console.log('🔍 [handleDataLoaded] Called with retryCount:', retryCount, 'chartId:', currentChartId)
        console.log('🔍 [handleDataLoaded] Chart config trades:', chartConfigs.current[currentChartId]?.trades?.length || 0)

        if (retryCount >= maxRetries) {
          console.log('❌ [handleDataLoaded] Max retries reached')
          return;
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
        await handleDataLoaded();
      }, 1000) // Increased delay to wait for trade data
    }

    // Setup double-click to fit content
    const shouldHandleDoubleClick = chartConfig.chart?.timeScale?.handleDoubleClick !== false &&
      chartConfig.chart?.handleDoubleClick !== false

    if (shouldHandleDoubleClick) {
      // Subscribe to chart click events
      chart.subscribeClick((param) => {
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
    Object.values(legendResizeObserverRefs.current).forEach((resizeObserver) => {
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


  const addTradeVisualization = useCallback(async (chart: IChartApi, series: ISeriesApi<any>, trades: TradeConfig[], options: TradeVisualizationOptions, chartData?: any[]) => {
    console.log('🎯 [addTradeVisualization] Called with:', {
      tradesCount: trades?.length || 0,
      hasSeries: !!series,
      hasChartData: !!chartData,
      options: options
    })

    if (!trades || trades.length === 0) {
      console.log('❌ [addTradeVisualization] No trades provided')
      return;
    }

    // Verify chart is ready (should be guaranteed by lifecycle method)
    const timeScale = chart.timeScale();
    const visibleRange = timeScale.getVisibleRange();

    console.log('🎯 [addTradeVisualization] Visible range:', visibleRange)

    if (!visibleRange || !visibleRange.from || !visibleRange.to) {
      console.log('❌ [addTradeVisualization] No visible range, returning')
      return;
    }

    try {
      // Use default price scale ID for now
      const priceScaleId = 'right';

      // Create visual elements for trade visualization
      console.log('🎯 [addTradeVisualization] Creating visual elements...')
      const visualElements = createTradeVisualElements(trades, options, chartData, priceScaleId);

      console.log('🎯 [addTradeVisualization] Visual elements created:', {
        markersCount: visualElements.markers?.length || 0,
        rectanglesCount: visualElements.rectangles?.length || 0,
        annotationsCount: visualElements.annotations?.length || 0
      })

      // Add markers to the series
      if (visualElements.markers.length > 0) {
        try {
          createSeriesMarkers(series, visualElements.markers);
        } catch (error) {
          // Error adding markers
        }
      }

      // Add rectangles using the canvas overlay approach (following official example)
      const chartId = chart.chartElement().id || 'default';
      console.log('🎯 [addTradeVisualization] Setting up rectangle plugin for chart:', chartId)

      // Use the RectangleOverlayPlugin instead of TradeRectanglePlugin
      if (!rectanglePluginRefs.current[chartId]) {
        console.log('🎯 [addTradeVisualization] Creating new rectangle plugin')
        const rectanglePlugin = new RectangleOverlayPlugin();
        rectanglePlugin.setChart(chart, series);
        rectanglePluginRefs.current[chartId] = rectanglePlugin;
      }

      const rectanglePlugin = rectanglePluginRefs.current[chartId];

      // Clear existing rectangles and add new ones
      console.log('🎯 [addTradeVisualization] Clearing existing rectangles')
      rectanglePlugin.clearRectangles();

      if (visualElements.rectangles.length > 0) {
        console.log('🎯 [addTradeVisualization] Adding', visualElements.rectangles.length, 'rectangles')
        visualElements.rectangles.forEach((rect, index) => {
          console.log('🎯 [addTradeVisualization] Adding rectangle', index, ':', rect)
          rectanglePlugin.addRectangle(rect);
        });

        // Force redraw of the canvas overlay
        console.log('🎯 [addTradeVisualization] Scheduling redraw')
        rectanglePlugin.scheduleRedraw();
      } else {
        console.log('❌ [addTradeVisualization] No rectangles to add')
      }

      // Add annotations to the series
      if (visualElements.annotations && Array.isArray(visualElements.annotations) && visualElements.annotations.length > 0) {
        try {
          visualElements.annotations.forEach(annotation => {
            if ((series as any).addShape) {
              (series as any).addShape(annotation);
            } else if ((series as any).setShapes) {
              (series as any).setShapes([annotation]);
            } else if ((series as any).addAnnotation) {
              (series as any).addAnnotation(annotation);
            }
          });
        } catch (error) {
          // Error processing annotations
        }
      }
    } catch (error) {
      console.error('❌ [addTradeVisualization] Error in trade visualization:', error);
    }
  }, [])

  // Trade visualization is now handled synchronously in createSeries function
  // No need for addTradeVisualizationWhenReady anymore

  const addAnnotations = useCallback((chart: IChartApi, annotations: Annotation[] | { layers: any }) => {
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
              if (layer && layer.visible !== false && layer.annotations && Array.isArray(layer.annotations)) {
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
    const validAnnotations = annotationsArray.filter(annotation =>
      annotation && typeof annotation === 'object' && annotation.time
    )

    if (validAnnotations.length === 0) {
      return
    }

    // Additional safety check before calling createAnnotationVisualElements
    if (!Array.isArray(validAnnotations) || typeof validAnnotations.forEach !== 'function') {
      console.error('addAnnotations: validAnnotations is still not a proper array:', validAnnotations)
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
              (seriesList[0] as any).addShape(shape)
            } else if ((seriesList[0] as any).setShapes) {
              (seriesList[0] as any).setShapes([shape])
            }
          } catch (error) {
            // Error adding shape
          }
        })
      }
    }
  }, [])

  const addAnnotationLayers = useCallback((chart: IChartApi, layers: AnnotationLayer[] | { layers: any }) => {
    // Handle annotation manager structure from Python side
    let layersArray: AnnotationLayer[] = []

    if (layers && typeof layers === 'object') {
      // Check if this is an annotation manager structure (has layers)
      if ('layers' in layers && layers.layers) {
        // Convert layers object to array
        try {
          const layersValues = Object.values(layers.layers)
          if (Array.isArray(layersValues)) {
            layersArray = layersValues as AnnotationLayer[];
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
  }, [])

  const addModularTooltip = useCallback((chart: IChartApi, container: HTMLElement, seriesList: ISeriesApi<any>[], chartConfig: ChartConfig) => {


    if (!chartConfig.tooltipConfigs || Object.keys(chartConfig.tooltipConfigs).length === 0) {
      return
    }

    try {
      // Import tooltip plugin dynamically
      import('./tooltipPlugin').then(({ createTooltipPlugin }) => {
        const tooltipPlugin = createTooltipPlugin(chart, container, chartConfig.tooltipConfigs)

        // Enable tooltip
        tooltipPlugin.enable()



        // Store plugin reference for cleanup
        if (!window.chartPlugins) {
          window.chartPlugins = new Map()
        }
        window.chartPlugins.set(chart, tooltipPlugin)
      }).catch(error => {
        console.error("🎯 [addModularTooltip] Error loading tooltip plugin:", error)
      })
    } catch (error) {
      console.error("🎯 [addModularTooltip] Error setting up tooltip:", error)
    }
  }, [])

  const addRangeSwitcher = useCallback((chart: IChartApi, rangeConfig: any) => {
    // Range switcher implementation will be added here
    // For now, this is a placeholder
  }, [])

  // Function to update legend positions when pane heights change - now handled by plugins
  const updateLegendPositions = useCallback(async (chart: IChartApi, legendsConfig: { [paneId: string]: LegendConfig }) => {
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

    console.log('🔄 Updating legend positions for chart - handled by plugins')
    
    // Note: Legend positioning is now handled entirely by the PanePrimitive plugins
    // Each plugin manages its own positioning through the positionLegend() method
    // No external positioning logic is needed - the plugins are self-contained
  }, [])

  // Store legend element references for dynamic updates
  const legendElementsRef = useRef<Map<string, HTMLElement>>(new Map())
  const legendSeriesDataRef = useRef<Map<string, { series: ISeriesApi<any>, legendConfig: LegendConfig, paneId: number, seriesName: string }[]>>(new Map())

  // Function to update legend values based on crosshair position
  const updateLegendValues = useCallback((chart: IChartApi, chartId: string, param: MouseEventParams) => {
    console.log('🔄 updateLegendValues called:', { chartId, param })

    const legendSeriesData = legendSeriesDataRef.current.get(chartId)
    if (!legendSeriesData || !param.time) {
      console.log('❌ No legend data or time:', { legendSeriesData: !!legendSeriesData, hasTime: !!param.time })
      return
    }

    console.log('✅ Found legend data for chart:', chartId, 'series count:', legendSeriesData.length)

    legendSeriesData.forEach(({ series, legendConfig, paneId, seriesName }, index) => {
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

        console.log(`🔍 Processing series ${index + 1}/${legendSeriesData.length}:`, {
          seriesType: seriesType,
          seriesOptions: seriesOptions
        })

        // Get data point at crosshair time
        console.log('🔍 Getting data for series:', seriesType, 'series object:', series)
        const data = series.data()
        console.log('🔍 Series data result:', data)

        if (!data || data.length === 0) {
          console.log('❌ No series data for series:', seriesType, 'data:', data)
          console.log('⚠️ This series should have been filtered out during legend creation')
          return
        }

        console.log('📊 Series data points:', data.length, 'crosshair time:', param.time)

        // Find the data point closest to the crosshair time
        let closestDataPoint: any = null
        let minTimeDiff = Infinity

        for (const point of data) {
          if (point.time && param.time && typeof point.time === 'number' && typeof param.time === 'number') {
            const timeDiff = Math.abs(point.time - param.time)
            if (timeDiff < minTimeDiff) {
              minTimeDiff = timeDiff
              closestDataPoint = point
            }
          }
        }

        if (!closestDataPoint) {
          console.log('❌ No closest data point found')
          return
        }

        console.log('🎯 Closest data point:', closestDataPoint, 'time diff:', minTimeDiff)

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
          value: closestDataPoint.value || closestDataPoint.close || closestDataPoint.high || '',
          time: closestDataPoint.time || '',
          color: seriesColor,
          type: seriesType,
          ...closestDataPoint // Include all other data fields
        }

        console.log('📝 Template data:', templateData)

        // Find and update the legend element
        const legendElement = legendElementsRef.current.get(`${chartId}-pane-${paneId}`)
        if (!legendElement) {
          console.log('❌ No legend element found for:', `${chartId}-pane-${paneId}`)
          return
        }

        console.log('✅ Found legend element for pane:', paneId)

        // Find the specific series item in the legend
        const seriesItems = legendElement.querySelectorAll('[data-series-name]')
        console.log('🔍 Found series items:', seriesItems.length)

        seriesItems.forEach((item) => {
          const itemElement = item as HTMLElement
          const itemSeriesName = itemElement.getAttribute('data-series-name')

          console.log('🔍 Checking series item:', itemSeriesName, 'vs:', seriesName)

          if (itemSeriesName === seriesName) {
            console.log('✅ Updating series item:', seriesName)

            if (legendConfig.text) {
              // Update custom template with new {series} prefix system
              let template = legendConfig.text

              // Replace placeholders in template
              Object.entries(templateData).forEach(([key, value]) => {
                // Handle {series}.{key} placeholders
                const seriesPlaceholder = `{series}.{${key}}`
                if (template.includes(seriesPlaceholder)) {
                  template = template.replace(new RegExp(seriesPlaceholder.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g'), String(value))
                }

                // Handle fallback {key} placeholders (only for first series)
                if (index === 0) {
                  const fallbackPlaceholder = `{${key}}`
                  if (template.includes(fallbackPlaceholder)) {
                    template = template.replace(new RegExp(fallbackPlaceholder.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g'), String(value))
                  }
                }
              })

              console.log('📝 Updated template:', template)

              // Set the innerHTML to preserve the text content
              itemElement.innerHTML = template

              // Since the template already contains the correct styles, we just need to ensure they persist
              // by applying them directly to the container and all child elements
              const targetColor = '#131722'
              const targetFontFamily = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
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

              console.log('🎨 Applied hardcoded styles (update):', {
                color: targetColor,
                fontFamily: targetFontFamily,
                fontSize: targetFontSize,
                letterSpacing: targetLetterSpacing,
                textAlign: targetTextAlign
              })

              console.log('🎨 Final item styles after update:', {
                color: itemElement.style.color || 'not set',
                fontFamily: itemElement.style.fontFamily || 'not set',
                fontSize: itemElement.style.fontSize || 'not set',
                letterSpacing: itemElement.style.letterSpacing || 'not set',
                textAlign: itemElement.style.textAlign || 'not set'
              })
            } else {
              // Update default legend format
              const textContent = itemElement.querySelector('span:last-child') as HTMLElement
              if (textContent) {
                const value = templateData.value
                const displayValue = value !== null && value !== undefined && value !== '' ?
                  (typeof value === 'number' ? value.toFixed(2) : String(value)) : 'N/A'
                textContent.textContent = `${seriesName}: ${displayValue}`
              }
            }
          }
        })
      } catch (error) {
        console.error('❌ Error updating legend for series:', error)
      }
    })
  }, [])

  const addLegend = useCallback(async (chart: IChartApi, legendsConfig: { [paneId: string]: LegendConfig }, seriesList: ISeriesApi<any>[]) => {
    console.log('🎯 addLegend called with:', {
      chartId: chart.chartElement().id,
      legendsCount: Object.keys(legendsConfig).length,
      seriesCount: seriesList.length,
      legendsConfig: legendsConfig,
      timestamp: new Date().toISOString()
    })

          // Import the positioning engine (not currently used but kept for future use)
      // const { PositioningEngine } = await import('./services/PositioningEngine')

    // Check if component is being disposed
    if (isDisposingRef.current) {
      console.log('❌ Component is disposing, skipping legend creation')
      return
    }

    // Check if chart is valid and legends config exists
    if (!chart || !legendsConfig || Object.keys(legendsConfig).length === 0 || seriesList.length === 0) {
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
    console.log('⏳ Waiting for chart API to be ready...')
    console.log('🔍 Legends config keys:', Object.keys(legendsConfig))
    console.log('🔍 Legends config values:', legendsConfig)

    try {
      await retryWithBackoff(async () => {
        // Check if component is being disposed
        if (isDisposingRef.current) {
          throw new Error('Component disposed during retry')
        }

        // Wait for chart to have timeScale and be fully functional
        try {
          const timeScale = chart.timeScale()
          const visibleRange = timeScale.getVisibleRange()
          console.log('🔍 Chart timeScale ready, visible range:', visibleRange)
        } catch (error) {
          throw new Error('Chart timeScale not ready yet')
        }
        
        // Check if chart has panes available via API
        try {
          const panes = chart.panes()
          console.log('🔍 Chart panes available via API:', panes.length)
          
          // Verify we have enough panes for the legend config
          const maxPaneId = Math.max(...Object.keys(legendsConfig).map(id => parseInt(id)))
          if (panes.length <= maxPaneId) {
            throw new Error(`Not enough panes in chart API. Found: ${panes.length}, Need: ${maxPaneId + 1}`)
          }
          
          console.log(`✅ Chart API ready! Found ${panes.length} panes, need up to ${maxPaneId + 1}`)
          return panes
        } catch (error) {
          throw new Error(`Chart panes not ready: ${error}`)
        }
      }, 10, 200, 'Chart API readiness check') // 10 retries with 200ms base delay (exponential backoff)
    } catch (error) {
      if (error instanceof Error && error.message === 'Component disposed during retry') {
        console.log('❌ Component disposed while waiting for chart')
      } else {
        console.error('❌ Failed to wait for chart API:', error)
      }
      return
    }

    // Get chart ID for storing legend references
    const chartId = chart.chartElement().id || 'default'
    const legendSeriesData: { series: ISeriesApi<any>, legendConfig: LegendConfig, paneId: number, seriesName: string }[] = []







    // Group series by pane
    console.log('🔍 Grouping series by pane, total series:', seriesList.length)
    console.log('🔍 Available legend configs:', Object.keys(legendsConfig))
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
        console.log(`🔍 Series ${index}: paneId from top level: ${seriesPaneId}`)
      }
      // Then check if paneId is in the options
      else if (seriesOptions && (seriesOptions as any).paneId !== undefined) {
        seriesPaneId = (seriesOptions as any).paneId
        console.log(`🔍 Series ${index}: paneId from options: ${seriesPaneId}`)
      }

      if (seriesPaneId !== undefined) {
        // Use the backend-assigned paneId
        paneId = seriesPaneId
        console.log(`🔍 Series ${index}: Using backend paneId: ${paneId}`)
      } else {
        // If no paneId from backend, use default pane 0
        paneId = 0
        console.log(`🔍 Series ${index}: No paneId from backend, using default pane 0`)
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

      console.log(`🔍 Series ${index}: type=${seriesType}, title=${seriesOptions.title}, paneId=${paneId}, series.paneId=${(series as any).paneId}, seriesOptions.paneId=${(seriesOptions as any).paneId}`)

      if (!seriesByPane.has(paneId)) {
        seriesByPane.set(paneId, [])
      }
      seriesByPane.get(paneId)!.push(series)
    })

    console.log('🔍 Series by pane:', Object.fromEntries(seriesByPane.entries()))

    // Create legends for each pane that has a config
    let legendsCreated = 0
    seriesByPane.forEach((paneSeries, paneId) => {
      console.log(`🔍 Processing pane ${paneId} with ${paneSeries.length} series`)
      const legendConfig = legendsConfig[paneId.toString()]
      console.log(`🔍 Legend config for pane ${paneId}:`, legendConfig ? 'exists' : 'missing', legendConfig?.visible ? 'visible' : 'not visible')

      // Only create legend if config exists for this pane and is visible
      if (!legendConfig || !legendConfig.visible) {
        console.log(`🔍 Skipping legend for pane ${paneId}: no config or not visible`)
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
        console.log(`✅ Pane ${paneId} found in chart API:`, paneApi)
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
          console.log(`✅ Attached legend plugin to pane ${paneId}`)
          legendsCreated++
        } else {
          // Fallback: attach to the first series in the pane
          const firstSeries = paneSeries[0]
          if (firstSeries && typeof firstSeries.attachPrimitive === 'function') {
            firstSeries.attachPrimitive(legendPlugin)
            console.log(`✅ Attached legend plugin to series in pane ${paneId} (fallback)`)
            legendsCreated++
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
      console.log(`✅ Legend plugin created for pane ${paneId} with position: ${legendConfig.position || 'top-left'}`)

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
      console.log('✅ Storing series for legend updates (data will be available later)')
      paneSeries.forEach((series, index) => {
        legendSeriesData.push({ series, legendConfig, paneId, seriesName: `Pane ${paneId}` })
      })

      // Legend items are now handled by the Drawing Primitives plugin
      // No need for manual DOM manipulation

      // Legend items are now handled by the Drawing Primitives plugin
      // No need for manual DOM manipulation
    })

    // Store legend series data for updates
    console.log('💾 Storing legend series data for chart:', chartId, 'data:', legendSeriesData)
    legendSeriesDataRef.current.set(chartId, legendSeriesData)

    // Setup crosshair event handling for legend updates
    console.log('🎯 Setting up crosshair subscription for chart:', chartId)
    chart.subscribeCrosshairMove((param) => {
      console.log('🎯 Crosshair moved:', { chartId, param })
      updateLegendValues(chart, chartId, param)
    })

    // Summary of legend creation
    console.log(`🎯 Legend creation complete for chart ${chartId}: ${legendsCreated} legends created, ${legendSeriesData.length} series data stored`)
  }, [updateLegendValues])

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
          width: chartConfig.chart?.autoWidth ? undefined : (chartConfig.chart?.width || (width || undefined)),
          height: chartConfig.chart?.autoHeight ? undefined : (chartConfig.chart?.height || (height || undefined)),
          ...chartConfig.chart
        })
      }
    })
  }, [config.charts, width, height])

  // Initialize charts
  const initializeCharts = useCallback((isInitialRender = false) => {
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
          (window as any).chartApiMap = {}
        }
        (window as any).chartApiMap[chartId] = chart

        // Calculate chart dimensions once
        const containerRect = container.getBoundingClientRect()
        const chartWidth = chartConfig.autoWidth ? containerRect.width : (chartOptions.width || width || containerRect.width)
        const chartHeight = chartConfig.autoHeight ? containerRect.height : (chartOptions.height || height || containerRect.height)

        // Ensure minimum dimensions
        const finalWidth = Math.max(chartWidth, 200)
        const finalHeight = Math.max(chartHeight, 200)

        // Resize chart once with calculated dimensions
        chart.resize(finalWidth, finalHeight)

        // Apply layout.panes options if present
        if (chartOptions.layout && chartOptions.layout.panes) {
          chart.applyOptions({ layout: { panes: chartOptions.layout.panes } })
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
          Object.entries(chartConfig.chart.overlayPriceScales).forEach(([scaleId, scaleConfig]) => {
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
          })
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
              if (seriesIndex === 0 && chartConfig.trades && chartConfig.trades.length > 0 && chartConfig.tradeVisualizationOptions) {
                seriesConfig.trades = chartConfig.trades
                seriesConfig.tradeVisualizationOptions = chartConfig.tradeVisualizationOptions
              }

              const series = createSeries(chart, seriesConfig, { signalPluginRefs }, chartId, seriesIndex)
              if (series) {
                seriesList.push(series)

                // Apply overlay price scale configuration if this series uses one
                if (seriesConfig.priceScaleId &&
                  seriesConfig.priceScaleId !== 'right' &&
                  seriesConfig.priceScaleId !== 'left' &&
                  chartConfig.chart?.overlayPriceScales?.[seriesConfig.priceScaleId]) {

                  const scaleConfig = chartConfig.chart.overlayPriceScales[seriesConfig.priceScaleId]
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
              console.error(`Error creating series at index ${seriesIndex} for chart ${chartId}:`, seriesError)
            }
          })
        } else {
          // No valid series configuration found
        }

        seriesRefs.current[chartId] = seriesList

        // Process pending trade rectangles after all series are created
        if ((chart as any)._pendingTradeRectangles && (chart as any)._pendingTradeRectangles.length > 0) {
          (chart as any)._pendingTradeRectangles.forEach((pendingData: any, index: number) => {
            try {
              // Create rectangle plugin for this chart if it doesn't exist
              const chartId = pendingData.chartId || 'default';
              if (!rectanglePluginRefs.current[chartId]) {
                const rectanglePlugin = new RectangleOverlayPlugin();
                rectanglePlugin.setChart(chart, pendingData.series);
                rectanglePluginRefs.current[chartId] = rectanglePlugin;
              }

              const rectanglePlugin = rectanglePluginRefs.current[chartId];

              // Add rectangles to the plugin
              pendingData.rectangles.forEach((rect: any, rectIndex: number) => {
                rectanglePlugin.addRectangle(rect);
              });

              // Force redraw of the canvas overlay
              rectanglePlugin.scheduleRedraw();

            } catch (error) {
              console.error('❌ [initializeCharts] Error processing trade rectangles set', index + 1, ':', error);
            }
          });

          // Clear the pending rectangles after processing
          (chart as any)._pendingTradeRectangles = [];
        }

        // Apply pane heights configuration AFTER series creation to ensure all panes exist
        if (chartConfig.chart?.layout?.paneHeights) {
          // Get all panes after series creation
          const allPanes = chart.panes()

          Object.entries(chartConfig.chart.layout.paneHeights).forEach(([paneIdStr, heightOptions]) => {
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
          })
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
              }
            } catch (error) {
              console.warn('Error during chart initialization:', error)
            }
          }
        }, 200) // Increased delay to ensure chart is fully ready

        // Store legend config for later creation (moved to initialization delay above)
        // if (chartConfig.legends && Object.keys(chartConfig.legends).length > 0) {
        //   console.log('🎯 Legend config stored for chart:', chartId, 'legends:', Object.keys(chartConfig.legends))
        // }

        // Setup auto-sizing for the chart
        functionRefs.current.setupAutoSizing(chart, container, chartConfig)

        // Setup chart synchronization if enabled
        if (config.syncConfig && config.syncConfig.enabled) {
          functionRefs.current.setupChartSynchronization(chart, chartId, config.syncConfig)
        }

        // Setup fitContent functionality
        functionRefs.current.setupFitContent(chart, chartConfig)

        // Call fitContent after all series are created and data is loaded
        const shouldFitContentOnLoad = chartConfig.chart?.timeScale?.fitContentOnLoad !== false &&
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
  }, [processedChartConfigs, config.syncConfig, width, height, onChartsReady])

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
  }, [addLegend, addTradeVisualization, addAnnotations, addModularTooltip, addAnnotationLayers, addRangeSwitcher, updateLegendPositions, setupAutoSizing, setupChartSynchronization, setupFitContent, cleanupCharts])

  useEffect(() => {
    if (config && config.charts && config.charts.length > 0) {
      initializeCharts(true)
    }
  }, [config, initializeCharts])

  // Memoize the chart containers to prevent unnecessary re-renders
  const chartContainers = useMemo(() => {
    if (!config.charts || config.charts.length === 0) {
      return []
    }

    return config.charts.map((chartConfig, index) => {
      const chartId = chartConfig.chartId || `chart-${index}`
      const containerId = `chart-container-${chartId}`

      // Determine container styling based on auto-sizing options
      const shouldAutoSize = chartConfig.autoSize || chartConfig.autoWidth || chartConfig.autoHeight
      const chartOptions = chartConfig.chart || {}

      // Use optimized style creation with memoization
      const styles = createOptimizedStyles(width, height, !!shouldAutoSize, chartOptions)
      const containerStyle = {
        ...styles.container,
        minWidth: chartOptions.minWidth || chartConfig.minWidth || (shouldAutoSize ? 200 : undefined),
        minHeight: chartOptions.minHeight || chartConfig.minHeight || (shouldAutoSize ? 200 : undefined),
        maxWidth: chartOptions.maxWidth || chartConfig.maxWidth,
        maxHeight: chartOptions.maxHeight || chartConfig.maxHeight,
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
      <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
        {chartContainers}
      </div>
    </ErrorBoundary>
  )
})

export default LightweightCharts