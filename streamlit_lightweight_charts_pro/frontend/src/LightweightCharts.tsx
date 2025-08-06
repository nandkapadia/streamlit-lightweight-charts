import React, { useEffect, useRef, useCallback } from 'react'
import {
  createChart,
  IChartApi,
  ISeriesApi,
  createSeriesMarkers,
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

interface LightweightChartsProps {
  config: ComponentConfig
  height?: number | null
  width?: number | null
}

const LightweightCharts: React.FC<LightweightChartsProps> = ({ config, height = 400, width = null }) => {
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

    // Function to get container dimensions
  const getContainerDimensions = (container: HTMLElement) => {
    const rect = container.getBoundingClientRect()
    return {
      width: rect.width,
      height: rect.height
    }
  }



  // Function to setup auto-sizing for a chart
  const setupAutoSizing = useCallback((chart: IChartApi, container: HTMLElement, chartConfig: ChartConfig) => {
    // Auto-sizing implementation
    if (chartConfig.autoSize || chartConfig.autoWidth || chartConfig.autoHeight) {
      const resizeObserver = new ResizeObserver(() => {
        try {
          const dimensions = getContainerDimensions(container)
          const newWidth = chartConfig.autoWidth ? dimensions.width : chartConfig.chart?.width || width
          const newHeight = chartConfig.autoHeight ? dimensions.height : chartConfig.chart?.height || height
          
          chart.resize(newWidth, newHeight)
        } catch (error) {
      // Auto-sizing resize failed
        }
      })
      
      resizeObserver.observe(container)
      resizeObserverRef.current = resizeObserver
    }
  }, [width, height])

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

  // Cleanup function
  const cleanupCharts = useCallback(() => {
    console.log("🧹 [cleanupCharts] Starting cleanup, setting disposal flag")
    // Set disposing flag to prevent async operations
    // But don't set it if this is the initial render
    if (prevConfigRef.current !== null) {
      isDisposingRef.current = true
    } else {
      console.log("🧹 [cleanupCharts] Skipping disposal flag for initial render")
    }
    
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
        console.warn('Error removing chart during cleanup:', error)
      }
    })

    // Clear references
    chartRefs.current = {}
    seriesRefs.current = {}
    rectanglePluginRefs.current = {}
    signalPluginRefs.current = {}
    chartConfigs.current = {}
    legendResizeObserverRefs.current = {}
    
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
          console.warn('Error processing annotation layers:', error)
        }
      } else if (Array.isArray(annotations)) {
        // Direct array of annotations
        annotationsArray = annotations
      }
    }

    // Validate annotations parameter
    if (!annotationsArray || !Array.isArray(annotationsArray)) {
      console.warn('addAnnotations: annotationsArray is not an array:', annotationsArray)
      return
    }

    // Additional safety check - ensure annotations is actually an array
    try {
      if (typeof annotationsArray.forEach !== 'function') {
        console.warn('addAnnotations: annotationsArray.forEach is not a function:', annotationsArray)
        return
      }
    } catch (error) {
      console.warn('addAnnotations: Error checking annotationsArray.forEach:', error)
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
            console.warn('Error adding shape:', error)
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
          console.warn('Error processing layers object:', error)
        }
      } else if (Array.isArray(layers)) {
        // Direct array of layers
        layersArray = layers
      }
    }

    // Validate layers parameter
    if (!layersArray || !Array.isArray(layersArray)) {
      console.warn('addAnnotationLayers: layersArray is not an array:', layersArray)
      return
    }

    layersArray.forEach((layer, index) => {
      try {
        if (!layer || typeof layer !== 'object') {
          console.warn(`Invalid layer at index ${index}:`, layer)
          return
        }

        if (layer.visible !== false && layer.annotations) {
          functionRefs.current.addAnnotations(chart, layer.annotations)
        }
      } catch (error) {
        console.warn(`Error processing layer at index ${index}:`, error, layer)
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
  const updateLegendPositions = useCallback(async (chart: IChartApi, legendConfig: LegendConfig) => {
    // Check if component is being disposed
    if (isDisposingRef.current) {
      console.warn('Component is being disposed, skipping legend position update')
      return
    }
    
    // Check if chart is valid and not disposed
    if (!chart) {
      return
    }
    
    try {
      // Quick check if chart is still valid
      chart.chartElement()
    } catch (error) {
      console.warn('Chart is disposed, skipping legend position update')
      return
    }
    
    // Additional safety check for chart validity
    try {
      chart.timeScale()
    } catch (error) {
      console.warn('Chart timeScale is disposed, skipping legend position update')
      return
    }
    
    // Additional check to prevent disposal during async operations
    if (isDisposingRef.current) {
      console.warn('Component disposal detected during legend position update, aborting')
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
      console.warn('Error accessing chart element for legend positioning:', error)
    }
    
    if (!container) {
      console.warn('Could not find chart container for legend positioning')
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
        const position = legendConfig.position || 'top-right'
        const paneMargin = 20
        
        // Get current pane dimensions with error handling
        let paneHeight: number
        try {
          const paneSize = chart.paneSize(paneId)
          if (!paneSize || typeof paneSize.height !== 'number') {
            console.warn(`Could not get pane size for pane ${paneId}, using default`)
            return // Skip this legend if we can't get pane size
          }
          paneHeight = paneSize.height
        } catch (error) {
          console.warn(`Error getting pane size for pane ${paneId}:`, error)
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
                console.warn(`Could not get pane size for pane ${i}, using default offset`)
                offset += 200 // Default pane height
              }
            } catch (error) {
              console.warn(`Error getting pane size for pane ${i}:`, error)
              offset += 200 // Default pane height
            }
          }
          return offset
        }
        
        const offsetY = getPaneOffsetY(chart, paneId)
        
        // Use the dimensions from the new approach
        const priceScaleWidth = priceScalePositionAndSize.width
        const timeAxisHeight = timeScalePositionAndSize.height
        
        // Calculate the actual pane content area
        const paneContentHeight = paneHeight - timeAxisHeight
        
        // Calculate position relative to the chart container
        const legendTop = offsetY + paneMargin
        const legendLeft = paneMargin + priceScaleWidth // Account for price scale width
        
        // Cast to HTMLElement to access style property
        const legendElement = legendContainer as HTMLElement
        
        // Update legend position
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
      console.warn('Error getting chart dimensions for legend positioning:', error)
    }
  }, [])

  const addLegend = useCallback(async (chart: IChartApi, legendConfig: LegendConfig, seriesList: ISeriesApi<any>[]) => {
    console.log("🎯 [addLegend] Starting legend creation with config:", legendConfig)
    console.log("🎯 [addLegend] Series list length:", seriesList.length)
    console.log("🎯 [addLegend] isDisposingRef.current:", isDisposingRef.current)
    
    // Check if component is being disposed
    if (isDisposingRef.current) {
      console.warn('Component is being disposed, skipping legend creation')
      return
    }
    
    // Check if chart is valid and not disposed
    if (!chart || !legendConfig.visible || seriesList.length === 0) {
      return
    }
    
    try {
      // Quick check if chart is still valid
      chart.chartElement()
    } catch (error) {
      console.warn('Chart is disposed, skipping legend creation')
      return
    }
    
    // Additional safety check for chart validity
    try {
      chart.timeScale()
    } catch (error) {
      console.warn('Chart timeScale is disposed, skipping legend creation')
      return
    }
    
    // Additional check to prevent disposal during async operations
    if (isDisposingRef.current) {
      console.warn('Component disposal detected during legend creation, aborting')
      return
    }

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
      console.warn('Error accessing chart element:', error)
    }
    
    if (!container) {
      console.warn('Could not find chart container for legend creation')
      return
    }

    let chartDimensions: any
    try {
      // Get the first series as the main series for dimension calculation
      const mainSeries = seriesList.length > 0 ? seriesList[0] : undefined
      chartDimensions = await getChartDimensions(chart, container, mainSeries)
    } catch (error) {
      console.warn('Error getting chart dimensions for legend creation:', error)
      return
    }

    // Group series by pane
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
      
      console.log(`🎯 [addLegend] Series ${index} assigned to pane ${paneId}`)
      
      if (!seriesByPane.has(paneId)) {
        seriesByPane.set(paneId, [])
      }
      seriesByPane.get(paneId)!.push(series)
    })

    console.log("🎯 [addLegend] Series by pane:", Object.fromEntries(seriesByPane))

    // Create a legend for each pane
    seriesByPane.forEach((paneSeries, paneId) => {
      console.log(`🎯 [addLegend] Creating legend for pane ${paneId} with ${paneSeries.length} series`)

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
                      padding: ${legendConfig.padding || 8}px;
                      margin: ${legendConfig.margin || 4}px;
                      pointer-events: none;
                      user-select: none;
                      min-width: 120px;
                      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                    `

                  // Position the legend within the specific pane area
                  const position = legendConfig.position || 'top-right'
      const paneMargin = 20 // Increased margin for better visual spacing
            
            // Get pane dimensions for the pane on which the legend is on
            let paneHeight: number
            try {
              const paneSize = chart.paneSize(paneId)
              if (!paneSize || typeof paneSize.height !== 'number') {
                console.warn(`Could not get pane size for pane ${paneId}, using default`)
                paneHeight = 200 // Default pane height
              } else {
                paneHeight = paneSize.height
              }
            } catch (error) {
              console.warn(`Error getting pane size for pane ${paneId}:`, error)
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
                    console.warn(`Could not get pane size for pane ${i}, using default offset`)
                    offset += 200 // Default pane height
                  }
                } catch (error) {
                  console.warn(`Error getting pane size for pane ${i}:`, error)
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

                          // Add pane title using TradingView's style
                    const paneTitle = document.createElement('div')
                    paneTitle.style.cssText = `
                      font-size: 16px;
                      font-weight: 600;
                      margin-bottom: 8px;
                      color: #131722;
                      border-bottom: 1px solid #e1e3e6;
                      padding-bottom: 4px;
                    `
                    
                    // Set descriptive pane titles
                    let paneTitleText = ''
                    switch (paneId) {
                      case 0:
                        paneTitleText = 'Main Chart'
                        break
                      case 1:
                        paneTitleText = 'RSI Indicator'
                        break
                      case 2:
                        paneTitleText = 'Volume'
                        break
                      default:
                        paneTitleText = `Pane ${paneId}`
                    }
                    
                    paneTitle.textContent = paneTitleText
                    legendContainer.appendChild(paneTitle)

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

        // Create legend item
        const item = document.createElement('div')
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
                try {
                  const data = series.data()
                  if (data && data.length > 0) {
                    const lastDataPoint = data[data.length - 1]
                    let lastValue = null
                    
                    // Extract value based on series type
                    if (lastDataPoint && typeof lastDataPoint === 'object') {
                      if ('value' in lastDataPoint) {
                        lastValue = lastDataPoint.value
                      } else if ('close' in lastDataPoint) {
                        lastValue = lastDataPoint.close
                      } else if ('high' in lastDataPoint) {
                        lastValue = lastDataPoint.high
                      }
                    }
                    
                    if (lastValue !== null && lastValue !== undefined) {
                      const valueSpan = document.createElement('span')
                      valueSpan.style.cssText = `
                        margin-left: 8px;
                        color: ${seriesColor};
                        font-weight: bold;
                      `
                      valueSpan.textContent = typeof lastValue === 'number' ? lastValue.toFixed(2) : String(lastValue)
                      item.appendChild(valueSpan)
                    }
                  }
                } catch (error) {
                  console.warn(`Could not get last value for series ${seriesName}:`, error)
                }
              }

        legendContainer.appendChild(item)
      })

      // Add legend to chart container but position it within the specific pane area
      const chartContainer = chart.chartElement()
      if (chartContainer) {
        chartContainer.appendChild(legendContainer)
        console.log(`✅ [addLegend] Legend for pane ${paneId} added to chart container successfully`)
        console.log(`🔍 [addLegend] Legend container HTML for pane ${paneId}:`, legendContainer.outerHTML)
        console.log(`🔍 [addLegend] Legend container computed styles for pane ${paneId}:`, {
          position: window.getComputedStyle(legendContainer).position,
          top: window.getComputedStyle(legendContainer).top,
          right: window.getComputedStyle(legendContainer).right,
          zIndex: window.getComputedStyle(legendContainer).zIndex,
          display: window.getComputedStyle(legendContainer).display,
          visibility: window.getComputedStyle(legendContainer).visibility,
          opacity: window.getComputedStyle(legendContainer).opacity
        })
      } else {
        console.warn(`❌ [addLegend] Could not find chart container for pane ${paneId}`)
      }
    })
  }, [])

  // Initialize charts
  const initializeCharts = useCallback((isInitialRender = false) => {
    console.log("🚀 [initializeCharts] Starting initialization")
    console.log("🚀 [initializeCharts] isInitializedRef.current:", isInitializedRef.current)
    console.log("🚀 [initializeCharts] isDisposingRef.current:", isDisposingRef.current)
    console.log("🚀 [initializeCharts] config.charts.length:", config.charts?.length)
    console.log("🚀 [initializeCharts] isInitialRender:", isInitialRender)
    console.log("🚀 [initializeCharts] About to create charts...")
    
    // Prevent re-initialization if already initialized and not disposing
    if (isInitializedRef.current && !isDisposingRef.current) {
      console.log('Charts already initialized, skipping re-initialization')
      return
    }
    
    // Additional check to prevent disposal during initialization (but allow initial render)
    if (isDisposingRef.current && !isInitialRender) {
      console.log('Component is being disposed, skipping initialization')
      return
    }
    
    // Check if we have charts to initialize
    if (!config.charts || config.charts.length === 0) {
      console.log('No charts to initialize')
      return
    }
    
    // Only clean up existing charts if this is not the initial render
    if (!isInitialRender) {
      console.log("🧹 [initializeCharts] Cleaning up existing charts (not initial render)")
      cleanupCharts()
    } else {
      console.log("🧹 [initializeCharts] Skipping cleanup (initial render)")
    }

    if (!config || !config.charts || config.charts.length === 0) {
      return
    }

    config.charts.forEach((chartConfig: ChartConfig, chartIndex: number) => {
      const chartId = chartConfig.chartId || `chart-${chartIndex}`
      const containerId = `chart-container-${chartId}`
      
      // Find or create container
      let container = document.getElementById(containerId)
      if (!container) {
        console.log(`🔄 [initializeCharts] Container ${containerId} not found, creating it`)
        container = document.createElement('div')
        container.id = containerId
        container.style.width = '100%'
        container.style.height = '100%'
        
        // Find the main chart container - try multiple selectors
        let mainContainer = document.querySelector('[data-testid="stHorizontalBlock"]')
        if (!mainContainer) {
          mainContainer = document.querySelector('.stHorizontalBlock')
        }
        if (!mainContainer) {
          mainContainer = document.querySelector('[data-testid="stVerticalBlock"]')
        }
        if (!mainContainer) {
          mainContainer = document.querySelector('.stVerticalBlock')
        }
        if (!mainContainer) {
          mainContainer = document.querySelector('[data-testid="stBlock"]')
        }
        if (!mainContainer) {
          mainContainer = document.querySelector('.stBlock')
        }
        if (!mainContainer) {
          mainContainer = document.body
        }
        
        if (mainContainer) {
          mainContainer.appendChild(container)
          console.log(`🔄 [initializeCharts] Container ${containerId} created and appended to`, mainContainer.tagName, mainContainer.className)
          
          // Ensure container has proper dimensions
          container.style.width = '100%'
          container.style.height = '100%'
          container.style.minHeight = '300px'
          container.style.display = 'block'
          container.style.position = 'relative'
        } else {
          console.error(`🔄 [initializeCharts] Could not find main container for ${containerId}`)
          return
        }
      } else {
        console.log(`🔄 [initializeCharts] Found existing container ${containerId}`)
      }

              // Create chart in container
        try {
          // Check if container is still valid
          if (!container || !container.isConnected) {
            console.warn(`Container ${containerId} is not connected to DOM, skipping chart creation`)
            return
          }



        // Create chart with proper width/height handling for auto-sizing
        const chartOptions = cleanLineStyleOptions({
          width: chartConfig.chart?.autoWidth ? undefined : (chartConfig.chart?.width || (width || undefined)),
          height: chartConfig.chart?.autoHeight ? undefined : (chartConfig.chart?.height || (height || undefined)),
          ...chartConfig.chart
        })

        console.log(`🔄 [initializeCharts] Creating chart for ${chartId} with options:`, {
          width: chartOptions.width,
          height: chartOptions.height,
          containerDimensions: {
            offsetWidth: container.offsetWidth,
            offsetHeight: container.offsetHeight,
            clientWidth: container.clientWidth,
            clientHeight: container.clientHeight
          }
        })

        let chart: IChartApi
        try {
          chart = createChart(container, chartOptions)
          console.log(`🔄 [initializeCharts] Chart created successfully for ${chartId}`)
        } catch (chartError) {
          console.error(`Failed to create chart for ${chartId}:`, chartError)
          return
        }

        // Check if chart was created successfully
        if (!chart) {
          console.error(`Chart creation returned null for ${chartId}`)
          return
        }

        // Set the chart element's ID so we can retrieve it later
        const chartElement = chart.chartElement()
        if (chartElement) {
          chartElement.id = chartId
        }

        chartRefs.current[chartId] = chart

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
                console.warn(`Price scale with ID '${scaleId}' not found. It will be created when a series uses it.`)
              }
            } catch (error) {
              console.warn(`Failed to configure price scale '${scaleId}':`, error)
            }
          })
        }

        // Create series for this chart
        const seriesList: ISeriesApi<any>[] = []
        
        if (chartConfig.series && Array.isArray(chartConfig.series)) {
          chartConfig.series.forEach((seriesConfig: SeriesConfig, seriesIndex: number) => {
            try {
              if (!seriesConfig || typeof seriesConfig !== 'object') {
                console.warn(`Invalid series config at index ${seriesIndex}:`, seriesConfig)
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
                    console.warn(`Failed to apply price scale configuration for series:`, error)
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
                console.warn(`Failed to create series at index ${seriesIndex} for chart ${chartId}`)
              }
            } catch (seriesError) {
              console.error(`Error creating series at index ${seriesIndex} for chart ${chartId}:`, seriesError)
            }
          })
        } else {
          console.warn(`No valid series configuration found for chart ${chartId}`)
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
                console.warn(`❌ Failed to set stretch factor for pane ${paneId}:`, error)
              }
            } else {
              console.warn(`⚠️ Skipping pane ${paneId}: paneId < allPanes.length = ${paneId < allPanes.length}, factor = ${options.factor}`)
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
        if (chartConfig.chart?.legend && chartConfig.chart.legend.visible) {
          // Store the legend configuration and series list for later creation
          setTimeout(() => {
            if (!isDisposingRef.current && chartRefs.current[chartId]) {
              try {
                functionRefs.current.addLegend(chart, chartConfig.chart.legend, seriesList)
                
                // Add resize listener to update legend positions when pane heights change
                const resizeObserver = new ResizeObserver(() => {
                  if (!isDisposingRef.current) {
                    functionRefs.current.updateLegendPositions(chart, chartConfig.chart.legend)
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
                console.warn('Error creating legend:', error)
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
              console.warn('❌ fitContent after all series failed:', error)
            }
          }, 300)
        }

      } catch (error) {
        console.error('Error creating chart:', error)
      }
    })

    isInitializedRef.current = true
    console.log("🚀 [initializeCharts] Initialization completed successfully")
    
    // Small delay to ensure charts are rendered before any cleanup
    setTimeout(() => {
      console.log("🚀 [initializeCharts] Charts should now be visible")
    }, 100)
  }, [config, width, height])

  // Update function references to avoid dependency issues
  useEffect(() => {
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
  })

  useEffect(() => {
    // Check if this is the initial render (no previous values)
    const isInitialRender = prevConfigRef.current === null
    
    // Check if there are meaningful changes that require re-initialization
    const configChanged = !isInitialRender && JSON.stringify(config) !== JSON.stringify(prevConfigRef.current)
    const widthChanged = !isInitialRender && width !== prevWidthRef.current
    const heightChanged = !isInitialRender && height !== prevHeightRef.current
    
    // Always initialize on first render, or if there are actual changes
    if (!isInitialRender && !configChanged && !widthChanged && !heightChanged) {
      console.log("🔄 [useEffect] No meaningful changes detected, skipping re-initialization")
      return
    }
    
    console.log("🔄 [useEffect] Initializing:", { isInitialRender, configChanged, widthChanged, heightChanged })
    
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
      console.log("🔄 [useEffect] Resetting disposal flag for initial render")
      console.log("🔄 [useEffect] Initializing immediately for initial render")
      initializeCharts(isInitialRender)
    } else {
      // For subsequent renders, use debounced initialization
      initializationTimeoutRef.current = setTimeout(() => {
        if (!isDisposingRef.current) {
          console.log("🔄 [useEffect] Proceeding with initialization")
          initializeCharts(isInitialRender)
        } else {
          console.log("🔄 [useEffect] Skipping initialization due to disposal flag")
        }
      }, 100)
    }
    
    // Cleanup on unmount only
    return () => {
      console.log("🧹 [useEffect] Component unmounting, cleaning up")
      if (initializationTimeoutRef.current) {
        clearTimeout(initializationTimeoutRef.current)
      }
      // Add a small delay to prevent immediate cleanup after chart creation
      setTimeout(() => {
        if (isDisposingRef.current) {
          cleanupCharts()
        }
      }, 50)
    }
  }, [config, width, height])

  if (!config.charts || config.charts.length === 0) {
    return <div>No charts configured</div>
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      {config.charts.map((chartConfig, index) => {
        const chartId = chartConfig.chartId || `chart-${index}`
        const containerId = `chart-container-${chartId}`
        
        // Determine container styling based on auto-sizing options
        const shouldAutoSize = chartConfig.autoSize || chartConfig.autoWidth || chartConfig.autoHeight
        const chartOptions = chartConfig.chart || {}
        
        const containerStyle: React.CSSProperties = {
          position: 'relative',
          border: 'none',
          borderRadius: '0px',
          padding: '0px',
          width: shouldAutoSize || width === null ? '100%' : (typeof width === 'number' ? `${width}px` : width || '100%'), // Use 100% if auto-sizing or width is null
          height: shouldAutoSize ? '100%' : (typeof height === 'number' ? `${height}px` : height || '100%'), // Use height if available, otherwise 100%
          minWidth: chartOptions.minWidth || chartConfig.minWidth || (shouldAutoSize ? 200 : undefined),
          minHeight: chartOptions.minHeight || chartConfig.minHeight || (shouldAutoSize ? 200 : undefined),
          maxWidth: chartOptions.maxWidth || chartConfig.maxWidth,
          maxHeight: chartOptions.maxHeight || chartConfig.maxHeight,
        }
        
        const chartContainerStyle: React.CSSProperties = {
          width: shouldAutoSize || width === null ? '100%' : (typeof width === 'number' ? `${width}px` : width || '100%'), // Use 100% if auto-sizing or width is null
          height: shouldAutoSize ? '100%' : (typeof height === 'number' ? `${height}px` : height || '100%'), // Use height if available, otherwise 100%
          position: 'relative',
        }
        
        return (
          <div key={chartId} style={containerStyle}>
            <div id={containerId} style={chartContainerStyle} />
          </div>
        )
      })}
    </div>
  )
}

export default LightweightCharts