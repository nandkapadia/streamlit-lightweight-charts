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
  perfLog, 
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
    addTradeVisualizationWhenReady: any
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
    addTradeVisualizationWhenReady: null,
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

        if (retryCount >= maxRetries) {
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

          // Check if chart has a visible range (more reliable than checking series data)
          const visibleRange = timeScale.getVisibleRange()

          if (visibleRange && visibleRange.from && visibleRange.to) {
            timeScale.fitContent()

            // Add trade visualization when chart is ready
            await functionRefs.current.addTradeVisualizationWhenReady(chart, chartConfigs.current[currentChartId])
          } else {
            // If no visible range, try again after a short delay
            setTimeout(async () => {
              try {
                timeScale.fitContent()
                // Add trade visualization when chart is ready
                await functionRefs.current.addTradeVisualizationWhenReady(chart, chartConfigs.current[currentChartId])
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
      }, 500)
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
    if (!trades || trades.length === 0) {
      return;
    }

    // Verify chart is ready (should be guaranteed by lifecycle method)
    const timeScale = chart.timeScale();
    const visibleRange = timeScale.getVisibleRange();

    if (!visibleRange || !visibleRange.from || !visibleRange.to) {
      return;
    }

    try {
      // Use default price scale ID for now
      const priceScaleId = 'right';

      // Create visual elements for trade visualization
      const visualElements = createTradeVisualElements(trades, options, chartData, priceScaleId);
      
      // Visual elements created

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
      // Use the RectangleOverlayPlugin instead of TradeRectanglePlugin
      if (!rectanglePluginRefs.current[chartId]) {
        const rectanglePlugin = new RectangleOverlayPlugin();
        rectanglePlugin.setChart(chart, series);
        rectanglePluginRefs.current[chartId] = rectanglePlugin;
      }

      const rectanglePlugin = rectanglePluginRefs.current[chartId];

      // Clear existing rectangles and add new ones
      rectanglePlugin.clearRectangles();

      if (visualElements.rectangles.length > 0) {
        visualElements.rectangles.forEach((rect, index) => {
          rectanglePlugin.addRectangle(rect);
        });

        // Force redraw of the canvas overlay
        rectanglePlugin.scheduleRedraw();
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

  const addTradeVisualizationWhenReady = useCallback(async (chart: IChartApi, chartConfig: ChartConfig) => {
    const chartId = chart.chartElement().id || 'default'

    if (!chartConfig.trades || chartConfig.trades.length === 0) {
      return;
    }

    // Wait for series to be available and find the candlestick series
    let retryCount = 0;
    const maxRetries = 10;

    while (retryCount < maxRetries) {
      const seriesList = seriesRefs.current[chartId];
      if (seriesList && seriesList.length > 0) {
        break;
      }

      await new Promise(resolve => setTimeout(resolve, 100));
      retryCount++;
    }

    // Check if chart is still valid
    if (!chart || !chart.chartElement()) {
      return;
    }

    const seriesList = seriesRefs.current[chartId];
    if (!seriesList || seriesList.length === 0) {
      return;
    }

    // Find the candlestick series specifically
    let candlestickSeries = null;
    let candlestickSeriesIndex = -1;

    for (let i = 0; i < seriesList.length; i++) {
      const series = seriesList[i];
      try {
        // Check if this is a candlestick series by looking at its type
        const seriesType = series.seriesType();
        if (seriesType === 'Candlestick') {
          candlestickSeries = series;
          candlestickSeriesIndex = i;
          break;
        }
      } catch (error) {
        // Series might be disposed, continue to next
        continue;
      }
    }

    if (!candlestickSeries) {
      candlestickSeries = seriesList[0];
      candlestickSeriesIndex = 0;
    }

    // Check if series is still valid
    try {
      candlestickSeries.priceScale();
    } catch (error) {
      return;
    }

    // Use trade visualization options from chart config or default
    const tradeOptions = chartConfig.tradeVisualizationOptions || {
      style: 'markers',
      entryMarkerColorLong: '#2196F3',
      entryMarkerColorShort: '#FF9800',
      exitMarkerColorProfit: '#4CAF50',
      exitMarkerColorLoss: '#F44336'
    };



    // Add trade visualization now that chart is ready - use candlestick series data
    const candlestickSeriesData = chartConfig.series?.[candlestickSeriesIndex]?.data || chartConfig.series?.[0]?.data;
    await functionRefs.current.addTradeVisualization(chart, candlestickSeries, chartConfig.trades, tradeOptions, candlestickSeriesData);
  }, [])

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
  const legendSeriesDataRef = useRef<Map<string, { series: ISeriesApi<any>, legendConfig: LegendConfig, paneId: number }[]>>(new Map())

  // Function to update legend values based on crosshair position
  const updateLegendValues = useCallback((chart: IChartApi, chartId: string, param: MouseEventParams) => {
    console.log('🔄 updateLegendValues called:', { chartId, param })
    
    const legendSeriesData = legendSeriesDataRef.current.get(chartId)
    if (!legendSeriesData || !param.time) {
      console.log('❌ No legend data or time:', { legendSeriesData: !!legendSeriesData, hasTime: !!param.time })
      return
    }

    console.log('✅ Found legend data for chart:', chartId, 'series count:', legendSeriesData.length)

    legendSeriesData.forEach(({ series, legendConfig, paneId }, index) => {
      try {
        console.log(`🔍 Processing series ${index + 1}/${legendSeriesData.length}:`, {
          seriesType: series.seriesType(),
          seriesOptions: series.options()
        })
        
        // Get data point at crosshair time
        console.log('🔍 Getting data for series:', series.seriesType(), 'series object:', series)
        const data = series.data()
        console.log('🔍 Series data result:', data)
        
        if (!data || data.length === 0) {
          console.log('❌ No series data for series:', series.seriesType(), 'data:', data)
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

        // Get series info
        const seriesOptions = series.options()
        const seriesType = series.seriesType()
        const seriesName = seriesOptions.title || `${seriesType}`
        
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
          title: seriesName,
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
            
            if (legendConfig.customTemplate) {
              // Update custom template
              let template = legendConfig.customTemplate
              
              // Replace placeholders in template
              Object.entries(templateData).forEach(([key, value]) => {
                const placeholder = `{${key}}`
                if (template.includes(placeholder)) {
                  template = template.replace(new RegExp(placeholder.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g'), String(value))
                }
              })
              
              console.log('📝 Updated template:', template)
              itemElement.innerHTML = template
            } else {
              // Update default legend format
              const valueSpan = itemElement.querySelector('[data-value]') as HTMLElement
              if (valueSpan && legendConfig.showLastValue) {
                const value = templateData.value
                if (value !== null && value !== undefined && value !== '') {
                  const displayValue = typeof value === 'number' ? value.toFixed(2) : String(value)
                  console.log('📝 Updated value:', displayValue)
                  valueSpan.textContent = displayValue
                }
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
      seriesCount: seriesList.length 
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
    const legendSeriesData: { series: ISeriesApi<any>, legendConfig: LegendConfig, paneId: number }[] = []

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
    const seriesByPane = new Map<number, ISeriesApi<any>[]>()
    seriesList.forEach((series, index) => {
      // Try to get paneId from series options or fallback to index-based assignment
      let paneId = 0

      // Check if series has paneId in its options
      const seriesOptions = series.options()
      if (seriesOptions && (seriesOptions as any).paneId !== undefined) {
        paneId = (seriesOptions as any).paneId
      } else {
        // Fallback: assign based on series index (this should match the Python configuration)
        // Series 0,1,2 -> pane 0 (main chart)
        // Series 3 -> pane 1 (RSI)
        // Series 4,5 -> pane 2 (volume)
        if (index <= 2) paneId = 0
        else if (index === 3) paneId = 1
        else paneId = 2
      }

      console.log(`🔍 Series ${index}: type=${series.seriesType()}, title=${seriesOptions.title}, paneId=${paneId}`)

      if (!seriesByPane.has(paneId)) {
        seriesByPane.set(paneId, [])
      }
      seriesByPane.get(paneId)!.push(series)
    })
    
    console.log('🔍 Series by pane:', Object.fromEntries(seriesByPane.entries()))

    // Create legends for each pane that has a config
    seriesByPane.forEach((paneSeries, paneId) => {
      const legendConfig = legendsConfig[paneId.toString()]
      
      // Only create legend if config exists for this pane and is visible
      if (!legendConfig || !legendConfig.visible) {
        return
      }

      // Create legend container for this pane
      const legendContainer = document.createElement('div')
      legendContainer.className = `chart-legend-pane-${paneId}`
      // Use TradingView's styling approach
      legendContainer.style.cssText = `
                      position: absolute;
                      z-index: ${legendConfig.zIndex || 1};
                      font-family: ${legendConfig.fontFamily || 'sans-serif'};
                      font-size: ${legendConfig.fontSize || 14}px;
                      font-weight: ${legendConfig.fontWeight || '300'};
                      line-height: 18px;
                      color: ${legendConfig.color || '#131722'};
                      background-color: ${legendConfig.backgroundColor || 'rgba(255, 255, 255, 0.95)'};
                      border: ${legendConfig.borderWidth || 1}px solid ${legendConfig.borderColor || '#e1e3e6'};
                      border-radius: ${legendConfig.borderRadius || 4}px;
                      padding: ${legendConfig.padding || 5}px;
                      margin: ${legendConfig.margin || 4}px;
                      pointer-events: none;
                      user-select: none;
                      min-width: 120px;
                      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
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

      // Add pane title if there are multiple panes
      if (seriesByPane.size > 1) {
        const paneTitle = document.createElement('div')
        paneTitle.style.cssText = `
          font-weight: bold;
          margin-bottom: 8px;
          border-bottom: 1px solid ${legendConfig.borderColor || '#e1e3e6'};
          padding-bottom: 4px;
        `
        let paneTitleText = ''
        if (paneId === 0) {
          paneTitleText = 'Main Chart'
        } else if (paneId === 1) {
          paneTitleText = 'RSI'
        } else if (paneId === 2) {
          paneTitleText = 'Volume'
        } else {
          paneTitleText = `Pane ${paneId}`
        }

        paneTitle.textContent = paneTitleText
        legendContainer.appendChild(paneTitle)
      }

      // Create legend items for each series in this pane
      paneSeries.forEach((series, index) => {
        const seriesOptions = series.options()
        const seriesType = series.seriesType()

        // Get series name or generate one
        const seriesName = seriesOptions.title || `${seriesType} ${index + 1}`

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

        // Get series data for template replacement
        let seriesData: any = {}
        try {
          const data = series.data()
          if (data && data.length > 0) {
            const lastDataPoint = data[data.length - 1]
            if (lastDataPoint && typeof lastDataPoint === 'object') {
              seriesData = { ...lastDataPoint }
            }
          }
        } catch (error) {
          // Could not get series data
        }

        // Prepare template data
        const templateData = {
          title: seriesName,
          value: seriesData.value || seriesData.close || seriesData.high || '',
          time: seriesData.time || '',
          color: seriesColor,
          type: seriesType,
          ...seriesData // Include all other data fields
        }

        // Store series data for legend updates
        console.log('💾 Storing series for legend:', {
          seriesType: series.seriesType(),
          seriesTitle: series.options().title,
          paneId
        })
        
        // Only store series that have data
        try {
          const seriesData = series.data()
          if (seriesData && seriesData.length > 0) {
            console.log('✅ Series has data, storing for legend updates')
            legendSeriesData.push({ series, legendConfig, paneId })
          } else {
            console.log('❌ Series has no data, skipping legend updates')
          }
        } catch (error) {
          console.log('❌ Error checking series data, skipping:', error)
        }

        // Create legend item
        let item: HTMLElement

        if (legendConfig.customTemplate) {
          // Use custom HTML template
          item = document.createElement('div')
          item.setAttribute('data-series-name', seriesName)
          let template = legendConfig.customTemplate
          
          // Replace placeholders in template
          Object.entries(templateData).forEach(([key, value]) => {
            const placeholder = `{${key}}`
            if (template.includes(placeholder)) {
              template = template.replace(new RegExp(placeholder.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g'), String(value))
            }
          })
          
          item.innerHTML = template
          item.style.cssText = `
            margin-bottom: 4px;
            white-space: nowrap;
          `
        } else {
          // Use default legend item format
          item = document.createElement('div')
          item.setAttribute('data-series-name', seriesName)
          item.style.cssText = `
            display: flex;
            align-items: center;
            margin-bottom: 4px;
            white-space: nowrap;
          `

          // Color indicator
          const colorIndicator = document.createElement('span')
          colorIndicator.style.cssText = `
            width: 12px;
            height: 2px;
            background-color: ${seriesColor};
            margin-right: 6px;
            display: inline-block;
          `
          item.appendChild(colorIndicator)

          // Series name
          const nameSpan = document.createElement('span')
          nameSpan.textContent = seriesName
          item.appendChild(nameSpan)

          // Add last value if configured
          if (legendConfig.showLastValue) {
            const lastValue = templateData.value
            if (lastValue !== null && lastValue !== undefined && lastValue !== '') {
              const valueSpan = document.createElement('span')
              valueSpan.setAttribute('data-value', 'true')
              valueSpan.style.cssText = `
                margin-left: 8px;
                color: ${seriesColor};
                font-weight: bold;
              `
              valueSpan.textContent = typeof lastValue === 'number' ? lastValue.toFixed(2) : String(lastValue)
              item.appendChild(valueSpan)
            }
          }
        }

        legendContainer.appendChild(item)
      })

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
          // Initialize charts

    // Prevent re-initialization if already initialized and not disposing
    if (isInitializedRef.current && !isDisposingRef.current) {
              // Skipping initialization - already initialized
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
      perfLog.log("🧹 [initializeCharts] Cleaning up existing charts (not initial render)")
      functionRefs.current.cleanupCharts()
    } else {
      perfLog.log("🧹 [initializeCharts] Skipping cleanup (initial render)")
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

                // Add trade visualization if configured
                if (seriesConfig.trades && seriesConfig.tradeVisualizationOptions) {
                  functionRefs.current.addTradeVisualization(chart, series, seriesConfig.trades, seriesConfig.tradeVisualizationOptions, seriesConfig.data)
                }

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

        // Store legend config for later creation
        if (chartConfig.legends && Object.keys(chartConfig.legends).length > 0) {
          console.log('🎯 Setting up legend for chart:', chartId, 'legends:', Object.keys(chartConfig.legends))
          // Store the legend configuration and series list for later creation
          setTimeout(() => {
            if (!isDisposingRef.current && chartRefs.current[chartId]) {
              try {
                console.log('🎯 Calling addLegend for chart:', chartId)
                functionRefs.current.addLegend(chart, chartConfig.legends, seriesList)

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
              } catch (error) {
                // Error creating legend
              }
            }
          }, 0) // Use 0 delay to execute immediately after current execution
        }

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
    console.log('🎯 Setting up function references, addLegend:', typeof addLegend)
    functionRefs.current = {
      addTradeVisualization,
      addTradeVisualizationWhenReady,
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
    console.log('🎯 Function references set up, addLegend ref:', typeof functionRefs.current.addLegend)
  }, [addLegend, addTradeVisualization, addTradeVisualizationWhenReady, addAnnotations, addModularTooltip, addAnnotationLayers, addRangeSwitcher, updateLegendPositions, setupAutoSizing, setupChartSynchronization, setupFitContent, cleanupCharts])

  useEffect(() => {
    // Main useEffect triggered
    
    // Check if this is the initial render (no previous values)
    const isInitialRender = prevConfigRef.current === null

    // Check if there are meaningful changes that require re-initialization
    const configChanged = !isInitialRender && config !== prevConfigRef.current
    const widthChanged = !isInitialRender && width !== prevWidthRef.current
    const heightChanged = !isInitialRender && height !== prevHeightRef.current

    // Changes detected

    // Always initialize on first render, or if there are actual changes
    if (!isInitialRender && !configChanged && !widthChanged && !heightChanged) {
      // No changes detected, skipping initialization
      return
    }

    // Update previous values
    prevConfigRef.current = config
    prevWidthRef.current = width
    prevHeightRef.current = height

    // Clear any pending initialization timeout
    if (initializationTimeoutRef.current) {
      clearTimeout(initializationTimeoutRef.current)
    }

    // For initial render, initialize immediately without setTimeout
    if (isInitialRender) {
      isDisposingRef.current = false
      initializeCharts(isInitialRender)
    } else {
      // For subsequent renders, use debounced initialization
      initializationTimeoutRef.current = setTimeout(() => {
        if (!isDisposingRef.current) {
          initializeCharts(isInitialRender)
        }
      }, 100)
    }

    // Cleanup on unmount only
    return () => {
      if (initializationTimeoutRef.current) {
        clearTimeout(initializationTimeoutRef.current)
      }
      // Add a small delay to prevent immediate cleanup after chart creation
      setTimeout(() => {
        if (isDisposingRef.current) {
          functionRefs.current.cleanupCharts()
        }
      }, 50)
    }
  }, [config, width, height])

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