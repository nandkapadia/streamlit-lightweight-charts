import React, { useEffect, useRef, useCallback, useMemo } from 'react'
import {
  createChart,
  IChartApi,
  ISeriesApi,
  createSeriesMarkers,
  MouseEventParams,
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
import { getChartDimensions } from './utils/chartDimensions'
import { cleanLineStyleOptions } from './utils/lineStyle'
import { createSeries } from './utils/seriesFactory'
import { 
  getCachedDOMElement, 
  createOptimizedStyles
} from './utils/performance'
import { ErrorBoundary } from './components/ErrorBoundary'

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
  const prevWidthRef = useRef<number | null>(null)
  const prevHeightRef = useRef<number | null>(null)
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

  // Function to update legend positions when pane heights change
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

    const legendContainers = chart.chartElement().querySelectorAll('[class^="chart-legend-pane-"]')

    // Get chart dimensions using the new requestAnimationFrame approach
    let container: HTMLElement | null = null

    try {
      // Try to get the chart element first
      const chartElement = chart.chartElement()
      if (chartElement) {
        container = chartElement.parentElement
      }

      // If still no container, try to find it by looking up the DOM tree
      if (!container && chartElement) {
        let currentElement: HTMLElement | null = chartElement
        while (currentElement && !container) {
          currentElement = currentElement.parentElement
          if (currentElement && currentElement.style && currentElement.style.width) {
            container = currentElement
          }
        }
      }

      // Final fallback - try to find any container with width/height
      if (!container && chartElement) {
        let currentElement: HTMLElement | null = chartElement
        while (currentElement && !container) {
          currentElement = currentElement.parentElement
          if (currentElement && (currentElement.offsetWidth > 0 || currentElement.clientWidth > 0)) {
            container = currentElement
          }
        }
      }
    } catch (error) {
      // Error accessing chart element for legend positioning
    }

    if (!container) {
      return
    }

    try {
      const { timeScalePositionAndSize, priceScalePositionAndSize } =
        await getChartDimensions(chart, container)



      legendContainers.forEach((legendContainer) => {
        const className = legendContainer.className
        const paneIdMatch = className.match(/chart-legend-pane-(\d+)/)
        if (!paneIdMatch) return

        const paneId = parseInt(paneIdMatch[1])
        const legendConfig = legendsConfig[paneId.toString()]
        
        // Skip if no legend config for this pane
        if (!legendConfig) return
        
        const position = legendConfig.position || 'top-right'
        const paneMargin = 20

        // Get current pane dimensions with error handling
        let paneHeight: number
        try {
          const paneSize = chart.paneSize(paneId)
          if (!paneSize || typeof paneSize.height !== 'number') {
            return // Skip this legend if we can't get pane size
          }
          paneHeight = paneSize.height
        } catch (error) {
          return // Skip this legend if there's an error
        }

        // Get the vertical offset of the pane
        function getPaneOffsetY(chart: IChartApi, paneIndex: number) {
          let offset = 0
          for (let i = 0; i < paneIndex; i++) {
            try {
              const paneSize = chart.paneSize(i)
              if (paneSize && typeof paneSize.height === 'number') {
                offset += paneSize.height
              } else {
                offset += 200 // Default pane height
              }
            } catch (error) {
              offset += 200 // Default pane height
            }
          }
          return offset
        }

        const offsetY = getPaneOffsetY(chart, paneId)
        const priceScaleWidth = priceScalePositionAndSize.width
        const timeAxisHeight = timeScalePositionAndSize.height
        const paneContentHeight = paneHeight - timeAxisHeight

        // Calculate position relative to the chart container
        const legendTop = offsetY + paneMargin
        const legendLeft = paneMargin + priceScaleWidth

        // Update legend position
        const legendElement = legendContainer as HTMLElement
        switch (position) {
          case 'top-left':
            legendElement.style.top = `${legendTop}px`
            legendElement.style.left = `${legendLeft}px`
            legendElement.style.right = 'auto'
            break
          case 'top-right':
            legendElement.style.top = `${legendTop}px`
            legendElement.style.left = 'auto'
            legendElement.style.right = `${paneMargin + priceScaleWidth}px`
            break
          case 'bottom-left':
            legendElement.style.top = `${legendTop + paneContentHeight - 80}px`
            legendElement.style.left = `${legendLeft}px`
            legendElement.style.right = 'auto'
            break
          case 'bottom-right':
            legendElement.style.top = `${legendTop + paneContentHeight - 80}px`
            legendElement.style.left = 'auto'
            legendElement.style.right = `${paneMargin + priceScaleWidth}px`
            break
        }
      })
    } catch (error) {
      // Error getting chart dimensions for legend positioning
    }
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
      legendsConfig: legendsConfig
    })
    
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

    // Get chart ID for storing legend references
    const chartId = chart.chartElement().id || 'default'
    const legendSeriesData: { series: ISeriesApi<any>, legendConfig: LegendConfig, paneId: number, seriesName: string }[] = []

    // Get chart dimensions using the new requestAnimationFrame approach
    let container: HTMLElement | null = null

    try {
      // Try to get the chart element first
      const chartElement = chart.chartElement()
      if (chartElement) {
        container = chartElement.parentElement
      }

      // If still no container, try to find it by looking up the DOM tree
      if (!container && chartElement) {
        let currentElement: HTMLElement | null = chartElement
        while (currentElement && !container) {
          currentElement = currentElement.parentElement
          if (currentElement && currentElement.style && currentElement.style.width) {
            container = currentElement
          }
        }
      }

      // Final fallback - try to find any container with width/height
      if (!container && chartElement) {
        let currentElement: HTMLElement | null = chartElement
        while (currentElement && !container) {
          currentElement = currentElement.parentElement
          if (currentElement && (currentElement.offsetWidth > 0 || currentElement.clientWidth > 0)) {
            container = currentElement
          }
        }
      }
    } catch (error) {
      // Error accessing chart element
    }

    if (!container) {
      return
    }

    let chartDimensions: any
    try {
      // Get the first series as the main series for dimension calculation
      const mainSeries = seriesList.length > 0 ? seriesList[0] : undefined
      chartDimensions = await getChartDimensions(chart, container, mainSeries)
    } catch (error) {
      return
    }



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
    seriesByPane.forEach((paneSeries, paneId) => {
      console.log(`🔍 Processing pane ${paneId} with ${paneSeries.length} series`)
      const legendConfig = legendsConfig[paneId.toString()]
      console.log(`🔍 Legend config for pane ${paneId}:`, legendConfig ? 'exists' : 'missing', legendConfig?.visible ? 'visible' : 'not visible')
      
      // Only create legend if config exists for this pane and is visible
      if (!legendConfig || !legendConfig.visible) {
        console.log(`🔍 Skipping legend for pane ${paneId}: no config or not visible`)
        return
      }

      // Create legend container for this pane
      const legendContainer = document.createElement('div')
      legendContainer.className = `chart-legend-pane-${paneId}`
      
      // Add a CSS rule to force legend text color if custom HTML is used
      if (legendConfig.text && legendConfig.text.includes('<span')) {
        const styleId = `legend-style-${chartId}-${paneId}`
        let styleElement = document.getElementById(styleId)
        if (!styleElement) {
          styleElement = document.createElement('style')
          styleElement.id = styleId
          document.head.appendChild(styleElement)
        }
        
        // Force the color for all text within this legend container
        // Use a more specific selector to ensure it overrides everything
        styleElement.textContent = `
          .${legendContainer.className} * {
            color: #131722 !important;
          }
          .${legendContainer.className} span {
            color: #131722 !important;
          }
          .${legendContainer.className} div {
            color: #131722 !important;
          }
        `
        
        console.log('🎨 Injected CSS rule for legend color:', styleElement.textContent)
        
        // Also add a global CSS rule as a backup
        const globalStyleId = 'global-legend-color-override'
        let globalStyleElement = document.getElementById(globalStyleId)
        if (!globalStyleElement) {
          globalStyleElement = document.createElement('style')
          globalStyleElement.id = globalStyleId
          document.head.appendChild(globalStyleElement)
        }
        
        // Add a very specific rule that should override everything
        globalStyleElement.textContent = `
          div[class*="chart-legend-pane-"] * {
            color: #131722 !important;
          }
          div[class*="chart-legend-pane-"] span {
            color: #131722 !important;
          }
          div[class*="chart-legend-pane-"] div {
            color: #131722 !important;
          }
        `
        
        console.log('🎨 Injected global CSS rule for legend color')
      }
      
      // Use TradingView's styling approach
      legendContainer.style.cssText = `
                      position: absolute;
                      z-index: ${legendConfig.zIndex || 1};
                      line-height: 18px;
                      background-color: ${legendConfig.backgroundColor || 'rgba(255, 255, 255, 0.95)'};
                      border: ${legendConfig.borderWidth || 1}px solid ${legendConfig.borderColor || '#e1e3e6'};
                      border-radius: ${legendConfig.borderRadius || 4}px;
                      padding: ${legendConfig.padding || 5}px;
                      margin: ${legendConfig.margin || 4}px;
                      pointer-events: none;
                      user-select: none;
                      min-width: 120px;
                      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                      /* Ensure custom HTML styling is not overridden */
                      color: inherit;
                      font-family: inherit;
                      font-size: inherit;
                      /* Allow pointer events for proper CSS inheritance */
                      pointer-events: auto;
                    `

      // Store legend element reference
      legendElementsRef.current.set(`${chartId}-pane-${paneId}`, legendContainer)

      // Position the legend within the specific pane area
      const position = legendConfig.position || 'top-right'
      const paneMargin = 20 // Increased margin for better visual spacing

      // Get pane dimensions for the pane on which the legend is on
      let paneHeight: number
      try {
        const paneSize = chart.paneSize(paneId)
        if (!paneSize || typeof paneSize.height !== 'number') {
          paneHeight = 200 // Default pane height
        } else {
          paneHeight = paneSize.height
        }
      } catch (error) {
        paneHeight = 200 // Default pane height
      }

      // Get the vertical offset of the pane
      function getPaneOffsetY(chart: IChartApi, paneIndex: number) {
        let offset = 0
        for (let i = 0; i < paneIndex; i++) {
          try {
            const paneSize = chart.paneSize(i)
            if (paneSize && typeof paneSize.height === 'number') {
              offset += paneSize.height
            } else {
              offset += 200 // Default pane height
            }
          } catch (error) {
            offset += 200 // Default pane height
          }
        }
        return offset
      }

      const offsetY = getPaneOffsetY(chart, paneId)

      // Use the dimensions from the new approach
      const priceScaleWidth = chartDimensions.priceScalePositionAndSize.width
      const timeAxisHeight = chartDimensions.timeScalePositionAndSize.height

      // Calculate the actual pane content area
      const paneContentHeight = paneHeight - timeAxisHeight

      // Calculate position relative to the chart container
      const legendTop = offsetY + paneMargin  // Add margin from top of pane
      const legendLeft = paneMargin + priceScaleWidth // Account for price scale width

      // Position legend within the calculated pane boundaries
      switch (position) {
        case 'top-left':
          legendContainer.style.top = `${legendTop}px`
          legendContainer.style.left = `${legendLeft}px`
          legendContainer.style.right = 'auto'
          break
        case 'top-right':
          legendContainer.style.top = `${legendTop}px`
          legendContainer.style.left = 'auto'
          legendContainer.style.right = `${paneMargin + priceScaleWidth}px`
          break
        case 'bottom-left':
          legendContainer.style.top = `${legendTop + paneContentHeight - 80}px` // Fixed height for legend
          legendContainer.style.left = `${legendLeft}px`
          legendContainer.style.right = 'auto'
          break
        case 'bottom-right':
          legendContainer.style.top = `${legendTop + paneContentHeight - 80}px` // Fixed height for legend
          legendContainer.style.left = 'auto'
          legendContainer.style.right = `${paneMargin + priceScaleWidth}px`
          break
      }

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

      // Create ONE legend item per pane (not per series)
      // Get the first series for basic info and color
      const firstSeries = paneSeries[0]
      let firstSeriesOptions: any = {}
      let firstSeriesType = 'Unknown'
      
      try {
        if (typeof firstSeries.options === 'function') {
          firstSeriesOptions = firstSeries.options()
        } else if (firstSeries.options) {
          firstSeriesOptions = firstSeries.options
        }
        
        if (typeof firstSeries.seriesType === 'function') {
          firstSeriesType = String(firstSeries.seriesType())
        } else if (firstSeries.seriesType && typeof firstSeries.seriesType === 'string') {
          firstSeriesType = String(firstSeries.seriesType)
        }
      } catch (error) {
        console.warn('Could not get first series options:', error)
      }

      // Get pane title from legend config or use a default
      let paneTitle = (legendConfig as any).title || ''
      if (!paneTitle) {
        if (paneId === 0) {
          paneTitle = 'Main Chart'
        } else if (paneId === 1) {
          paneTitle = 'RSI'
        } else if (paneId === 2) {
          paneTitle = 'Volume'
        } else {
          paneTitle = `Pane ${paneId}`
        }
      }
      
      // Get representative color from first series
      let seriesColor = '#2196f3' // default
      if (firstSeriesOptions.color) {
        seriesColor = firstSeriesOptions.color
      } else if (firstSeriesType === 'Candlestick') {
        seriesColor = '#26a69a'
      } else if (firstSeriesType === 'Histogram') {
        seriesColor = '#ff9800'
      } else if (firstSeriesType === 'Area') {
        seriesColor = firstSeriesOptions.topColor || '#4caf50'
      }

      // Get representative data from first series for template replacement
      let seriesData: any = {}
      try {
        const data = firstSeries.data()
        if (data && data.length > 0) {
          const lastDataPoint = data[data.length - 1]
          if (lastDataPoint && typeof lastDataPoint === 'object') {
            seriesData = { ...lastDataPoint }
          }
        }
      } catch (error) {
        // Could not get series data
      }

      // Prepare template data with pane-level information
      const templateData = {
        legendTitle: paneTitle, // Use pane title instead of series title
        title: paneTitle, // Keep for backward compatibility
        value: seriesData.value || seriesData.close || seriesData.high || '',
        time: seriesData.time || '',
        color: seriesColor,
        type: firstSeriesType,
        ...seriesData // Include all other data fields
      }

      // Store ALL series for legend updates, regardless of immediate data availability
      // Data will be available when crosshair moves or series are updated
      console.log('✅ Storing series for legend updates (data will be available later)')
      paneSeries.forEach((series, index) => {
        legendSeriesData.push({ series, legendConfig, paneId, seriesName: paneTitle })
      })

      // Create ONE legend item for this pane (not per series)
      let item: HTMLElement

      if (legendConfig.text) {
        // Use custom HTML template
        item = document.createElement('div')
        item.setAttribute('data-pane-id', paneId.toString())
        let template = legendConfig.text
        
        // Check if template contains any placeholders that need processing
        const hasPlaceholders = Object.keys(templateData).some(key => {
          const fallbackPlaceholder = `{${key}}`
          return template.includes(fallbackPlaceholder)
        })
        
        if (hasPlaceholders) {
          // Process placeholders for pane-level data
          Object.entries(templateData).forEach(([key, value]) => {
            const fallbackPlaceholder = `{${key}}`
            if (template.includes(fallbackPlaceholder)) {
              template = template.replace(new RegExp(fallbackPlaceholder.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g'), String(value))
            }
          })
        }
        
        // Don't apply default styling when using custom HTML templates
        // The custom HTML should contain all necessary styling
        // Only apply minimal positioning if needed
        item.style.cssText = `
          margin-bottom: 4px;
        `
        
        // Set the innerHTML first so we can extract styles from the actual element
        item.innerHTML = template
        
        // Since the template already contains the correct styles, we just need to ensure they persist
        // by applying them directly to the container and all child elements
        const targetColor = '#131722'
        const targetFontFamily = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
        const targetFontSize = '10px'
        const targetTextAlign = 'left'
        
        // Apply styles to the container element
        item.style.setProperty('color', targetColor, 'important')
        item.style.setProperty('font-family', targetFontFamily, 'important')
        item.style.setProperty('font-size', targetFontSize, 'important')
        item.style.setProperty('text-align', targetTextAlign, 'important')
        
        // Also apply to all child elements to ensure they inherit the styles
        const childElements = item.querySelectorAll('*')
        childElements.forEach(child => {
          if (child instanceof HTMLElement) {
            child.style.setProperty('color', targetColor, 'important')
            child.style.setProperty('font-family', targetFontFamily, 'important')
            child.style.setProperty('font-size', targetFontSize, 'important')
            child.style.setProperty('text-align', targetTextAlign, 'important')
          }
        })
        
        console.log('🎨 Applied hardcoded styles for pane legend:', {
          color: targetColor,
          fontFamily: targetFontFamily,
          fontSize: targetFontSize,
          textAlign: targetTextAlign
        })
        
        console.log('🎨 Final pane legend styles after application:', {
          color: item.style.color || 'not set',
          fontFamily: item.style.fontFamily || 'not set',
          fontSize: item.style.fontSize || 'not set',
          textAlign: item.style.textAlign || 'not set'
        })
      } else {
        // Default legend item for pane
        item = document.createElement('div')
        item.setAttribute('data-pane-id', paneId.toString())
        item.style.cssText = `
          display: flex;
          align-items: center;
          margin-bottom: 4px;
          padding: 2px 4px;
          border-radius: 2px;
          background-color: ${seriesColor}20;
          border-left: 3px solid ${seriesColor};
        `
        
        // Create color indicator
        const colorIndicator = document.createElement('span')
        colorIndicator.style.cssText = `
          width: 12px;
          height: 12px;
          background-color: ${seriesColor};
          border-radius: 2px;
          margin-right: 8px;
          flex-shrink: 0;
        `
        
        // Create text content
        const textContent = document.createElement('span')
        textContent.textContent = `${paneTitle}: ${templateData.value || 'N/A'}`
        textContent.style.cssText = `
          font-size: 12px;
          color: #131722;
        `
        
        item.appendChild(colorIndicator)
        item.appendChild(textContent)
      }

      // Add the single legend item to the container
      legendContainer.appendChild(item)
      
      // Add legend to chart container but position it within the specific pane area
      const chartContainer = chart.chartElement()
      if (chartContainer) {
        chartContainer.appendChild(legendContainer)
      } else {
        // Could not find chart container for pane
      }
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