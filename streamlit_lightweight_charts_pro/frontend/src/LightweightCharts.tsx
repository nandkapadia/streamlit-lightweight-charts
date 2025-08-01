import React, { useEffect, useRef, useCallback } from 'react'
import { 
  createChart, 
  IChartApi, 
  ISeriesApi, 
  AreaSeries,
  LineSeries,
  BarSeries,
  CandlestickSeries,
  HistogramSeries,
  BaselineSeries,
  createSeriesMarkers,
  LineStyle
} from 'lightweight-charts'
import { ComponentConfig, ChartConfig, SeriesConfig, TradeConfig, TradeVisualizationOptions, Annotation, AnnotationLayer, LegendConfig, SyncConfig, PaneHeightOptions } from './types'
import { createTradeVisualElements, TradeRectanglePlugin } from './tradeVisualization'
import { createAnnotationVisualElements } from './annotationSystem'
import { createBandSeries, BandData } from './bandSeriesPlugin'
import { createSignalSeriesPlugin, SignalSeries } from './signalSeriesPlugin'

interface LightweightChartsProps {
  config: ComponentConfig
  height?: number | null
  width?: number | null
}

const LightweightCharts: React.FC<LightweightChartsProps> = ({ config, height = 400, width = null }) => {
  const chartRefs = useRef<{ [key: string]: IChartApi }>({})
  const seriesRefs = useRef<{ [key: string]: ISeriesApi<any>[] }>({})
  const rectanglePluginRefs = useRef<{ [key: string]: TradeRectanglePlugin }>({})
  const signalPluginRefs = useRef<{ [key: string]: SignalSeries }>({})
  const resizeObserverRef = useRef<ResizeObserver | null>(null)
  const isInitializedRef = useRef<boolean>(false)
  const fitContentTimeoutRef = useRef<NodeJS.Timeout | null>(null)

  // Utility function to validate and convert line styles
  const validateLineStyle = (lineStyle: any): LineStyle | undefined => {
    if (!lineStyle) return undefined
    
    // If it's already a valid LineStyle enum value, return it
    if (typeof lineStyle === 'number' && Object.values(LineStyle).includes(lineStyle)) {
      return lineStyle
    }
    
    // If it's a string, try to convert it
    if (typeof lineStyle === 'string') {
      const styleMap: { [key: string]: LineStyle } = {
        'solid': LineStyle.Solid,
        'dotted': LineStyle.Dotted,
        'dashed': LineStyle.Dashed,
        'large-dashed': LineStyle.LargeDashed,
        'sparse-dotted': LineStyle.SparseDotted
      }
      return styleMap[lineStyle.toLowerCase()]
    }
    
    // If it's an array (for custom dash patterns), validate it
    if (Array.isArray(lineStyle)) {
      // Ensure all values are numbers
      if (lineStyle.every(val => typeof val === 'number' && val >= 0)) {
        // For custom dash patterns, we need to handle this differently
        // as LineStyle enum doesn't support custom arrays
        console.warn('Custom dash patterns not supported in this version, using solid line.')
        return LineStyle.Solid
      }
    }
    
    // Invalid line style, return undefined to use default
    console.warn('Invalid line style provided:', lineStyle, 'Using default solid line.')
    return undefined
  }

  // Utility function to clean up line style options
  const cleanLineStyleOptions = useCallback((options: any): any => {
    if (!options) return options
    
    const cleaned = { ...options }
    
    // Clean lineStyle property
    if (cleaned.lineStyle !== undefined) {
      const validLineStyle = validateLineStyle(cleaned.lineStyle)
      if (validLineStyle !== undefined) {
        cleaned.lineStyle = validLineStyle
      } else {
        delete cleaned.lineStyle
      }
    }
    
    // Clean other style properties that might cause issues
    if (cleaned.style && typeof cleaned.style === 'object') {
      cleaned.style = cleanLineStyleOptions(cleaned.style)
    }
    
    return cleaned
  }, [])

  // Function to get container dimensions
  const getContainerDimensions = (container: HTMLElement) => {
    const rect = container.getBoundingClientRect()
    return {
      width: rect.width,
      height: rect.height
    }
  }

  // Function to apply auto-sizing constraints
  const applySizeConstraints = (size: number, min?: number, max?: number) => {
    let constrainedSize = size
    if (min !== undefined && constrainedSize < min) {
      constrainedSize = min
    }
    if (max !== undefined && constrainedSize > max) {
      constrainedSize = max
    }
    return constrainedSize
  }

  // Function to resize chart based on container
  const resizeChart = useCallback((chart: IChartApi, container: HTMLElement, chartConfig: any) => {
    const { width: containerWidth, height: containerHeight } = getContainerDimensions(container)
    
    let newWidth = chartConfig.width || containerWidth
    let newHeight = chartConfig.height || containerHeight

    // Apply auto-sizing logic
    if (chartConfig.autoSize || chartConfig.autoWidth) {
      newWidth = applySizeConstraints(
        containerWidth, 
        chartConfig.minWidth, 
        chartConfig.maxWidth
      )
    }

    if (chartConfig.autoSize || chartConfig.autoHeight) {
      newHeight = applySizeConstraints(
        containerHeight, 
        chartConfig.minHeight, 
        chartConfig.maxHeight
      )
    }

    // Resize the chart
    chart.resize(newWidth, newHeight)
  }, [])

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
          console.warn('Auto-sizing resize failed:', error)
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
                console.warn('Time range synchronization failed:', error)
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
      const handleDataLoaded = () => {
        try {
          // Check if chart has series with data
          const series = Object.values(seriesRefs.current).flat()
          if (series.length === 0) {
            // No series yet, try again after a delay
            setTimeout(handleDataLoaded, 100)
            return
          }

          // Check if any series has data
          let hasData = false
          for (const s of series) {
            try {
              const data = s.dataByIndex(0, 1)
              if (data && data.length > 0) {
                hasData = true
                break
              }
            } catch (error) {
              // Series might not have data method or be disposed
            }
          }

          if (!hasData) {
            // No data yet, try again after a delay
            setTimeout(handleDataLoaded, 100)
            return
          }

          // Check if chart has a visible range
          const visibleRange = timeScale.getVisibleRange()
          if (visibleRange && visibleRange.from && visibleRange.to) {
            timeScale.fitContent()
          } else {
            // If no visible range, try again after a short delay
            setTimeout(() => {
              try {
                timeScale.fitContent()
              } catch (error) {
                console.warn('❌ fitContent after delay failed:', error)
              }
            }, 100)
          }
        } catch (error) {
          console.warn('❌ fitContent failed:', error)
        }
      }

      // Clear any existing timeout
      if (fitContentTimeoutRef.current) {
        clearTimeout(fitContentTimeoutRef.current)
      }

      // Call fitContent after a longer delay to ensure data is loaded
      fitContentTimeoutRef.current = setTimeout(handleDataLoaded, 500)
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
            console.warn('❌ fitContent on double-click failed:', error)
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
    // Clear any pending timeouts
    if (fitContentTimeoutRef.current) {
      clearTimeout(fitContentTimeoutRef.current)
      fitContentTimeoutRef.current = null
    }

    // Disconnect resize observer
    if (resizeObserverRef.current) {
      resizeObserverRef.current.disconnect()
      resizeObserverRef.current = null
    }

    // Remove all charts
    Object.values(chartRefs.current).forEach(chart => {
      try {
        chart.remove()
      } catch (error) {
        // Chart already removed or disposed
      }
    })

    // Clear references
    chartRefs.current = {}
    seriesRefs.current = {}
    rectanglePluginRefs.current = {}
  }, [])

  // Create series function
  const createSeries = useCallback((chart: IChartApi, seriesConfig: SeriesConfig, chartId?: string, seriesIndex?: number): ISeriesApi<any> | null => {
    const { 
      type, 
      data, 
      options = {}, 
      priceScale, 
      paneId, 
      lastValueVisible: topLevelLastValueVisible, 
      lastPriceAnimation,
      priceLineVisible: topLevelPriceLineVisible,
      priceLineSource: topLevelPriceLineSource,
      priceLineWidth: topLevelPriceLineWidth,
      priceLineColor: topLevelPriceLineColor,
      priceLineStyle: topLevelPriceLineStyle
    } = seriesConfig
    
    // Check both top-level and options for lastValueVisible
    const lastValueVisible = topLevelLastValueVisible !== undefined ? topLevelLastValueVisible : options.lastValueVisible
    
    // Check both top-level and options for price line properties
    const priceLineVisible = topLevelPriceLineVisible !== undefined ? topLevelPriceLineVisible : options.priceLineVisible
    const priceLineSource = topLevelPriceLineSource !== undefined ? topLevelPriceLineSource : options.priceLineSource
    const priceLineWidth = topLevelPriceLineWidth !== undefined ? topLevelPriceLineWidth : options.priceLineWidth
    const priceLineColor = topLevelPriceLineColor !== undefined ? topLevelPriceLineColor : options.priceLineColor
    const priceLineStyle = topLevelPriceLineStyle !== undefined ? topLevelPriceLineStyle : options.priceLineStyle
    


    let series: ISeriesApi<any>
    
    // Normalize series type to handle case variations
    const normalizedType = type?.toLowerCase()

    // Extract priceFormat from options and clean line styles
    const { priceFormat, ...otherOptions } = options
    const cleanedOptions = cleanLineStyleOptions(otherOptions)

    switch (normalizedType) {
      case 'area':
        const areaOptions = {
          ...cleanedOptions,
          lineColor: cleanedOptions.lineColor || '#2196F3',
          topColor: cleanedOptions.topColor || 'rgba(33, 150, 243, 0.4)',
          bottomColor: cleanedOptions.bottomColor || 'rgba(33, 150, 243, 0.0)',
          lineWidth: cleanedOptions.lineWidth || 2,
          relativeGradient: cleanedOptions.relativeGradient || false,
          invertFilledArea: cleanedOptions.invertFilledArea || false,
          lastValueVisible: lastValueVisible !== undefined ? lastValueVisible : true,
          lastPriceAnimation: lastPriceAnimation !== undefined ? lastPriceAnimation : 0,
          priceLineVisible: priceLineVisible !== undefined ? priceLineVisible : true,
          priceLineSource: priceLineSource !== undefined ? priceLineSource : 'lastBar',
          priceLineWidth: priceLineWidth !== undefined ? priceLineWidth : 1,
          priceLineColor: priceLineColor !== undefined ? priceLineColor : '',
          priceLineStyle: priceLineStyle !== undefined ? priceLineStyle : 2
        }
        if (priceFormat) {
          areaOptions.priceFormat = priceFormat
        }

        series = chart.addSeries(AreaSeries, areaOptions, paneId)
        
        // Try to apply lastValueVisible after series creation as a fallback
        try {
          if (lastValueVisible === false) {
            series.applyOptions({ lastValueVisible: false })
          }
        } catch (error) {
          console.warn(`❌ Failed to apply lastValueVisible after area series creation:`, error)
        }
        break
      case 'band':
        try {
          // Create band series using the custom plugin
          const bandSeries = createBandSeries(chart, {
            upperLineColor: cleanedOptions.upperLineColor || '#4CAF50',
            middleLineColor: cleanedOptions.middleLineColor || '#2196F3',
            lowerLineColor: cleanedOptions.lowerLineColor || '#F44336',
            upperLineWidth: cleanedOptions.upperLineWidth || 2,
            middleLineWidth: cleanedOptions.middleLineWidth || 2,
            lowerLineWidth: cleanedOptions.lowerLineWidth || 2,
            upperFillColor: cleanedOptions.upperFillColor || 'rgba(76, 175, 80, 0.1)',
            lowerFillColor: cleanedOptions.lowerFillColor || 'rgba(244, 67, 54, 0.1)',
            priceScaleId: cleanedOptions.priceScaleId || 'right',
            visible: cleanedOptions.visible !== false,
            lastValueVisible: lastValueVisible !== undefined ? lastValueVisible : true,
            priceLineVisible: priceLineVisible !== undefined ? priceLineVisible : true,
            priceLineSource: priceLineSource !== undefined ? priceLineSource : 'lastBar',
            priceLineWidth: priceLineWidth !== undefined ? priceLineWidth : 1,
            priceLineColor: priceLineColor !== undefined ? priceLineColor : '',
            priceLineStyle: priceLineStyle !== undefined ? priceLineStyle : 2
          })
          
          // Set data for band series
          if (data && data.length > 0) {
            bandSeries.setData(data as BandData[])
          }
          
          // Return a proxy object that mimics ISeriesApi interface
          return {
            setData: (newData: any[]) => {
              try {
                bandSeries.setData(newData as BandData[])
              } catch (error) {
                // Series is disposed or invalid - ignore error
              }
            },
            update: (newData: any) => {
              try {
                bandSeries.update(newData as BandData)
              } catch (error) {
                // Series is disposed or invalid - ignore error
              }
            },
            applyOptions: (options: any) => {
              try {
                bandSeries.setOptions(cleanLineStyleOptions(options))
              } catch (error) {
                // Series is disposed or invalid - ignore error
              }
            },
            priceScale: () => {
              try {
                return chart.priceScale(cleanedOptions.priceScaleId || 'right')
              } catch (error) {
                return null
              }
            },
            remove: () => {
              try {
                bandSeries.remove()
              } catch (error) {
                // Series is already removed - ignore error
              }
            },
          } as unknown as ISeriesApi<any>
        } catch (error) {
          // Failed to create band series - return null
          return null
        }
      case 'signal':
        try {
          // Create signal series using the custom plugin
          const signalSeries = createSignalSeriesPlugin(chart, {
            type: 'signal',
            data: data || [],
                              options: {
                    color0: cleanedOptions.color0 || '#ffffff',
                    color1: cleanedOptions.color1 || '#ff0000',
                    color2: cleanedOptions.color2,
                    visible: cleanedOptions.visible !== false,
                  }
          })
          
          // Store reference for cleanup
          signalPluginRefs.current[`${chartId}-${seriesIndex}`] = signalSeries
          
          // Return a proxy object that mimics ISeriesApi interface
          return {
            setData: (newData: any[]) => {
              try {
                signalSeries.updateData(newData)
              } catch (error) {
                // Series is disposed or invalid - ignore error
              }
            },
            update: (newData: any) => {
              try {
                // For signal series, we need to update the entire dataset
                signalSeries.updateData([newData])
              } catch (error) {
                // Series is disposed or invalid - ignore error
              }
            },
            applyOptions: (options: any) => {
              try {
                signalSeries.updateOptions({
                  color0: options.color0 || '#ffffff',
                  color1: options.color1 || '#ff0000',
                  color2: options.color2,
                  visible: options.visible !== false,
                })
              } catch (error) {
                // Series is disposed or invalid - ignore error
              }
            },
            priceScale: () => {
              try {
                return chart.priceScale(cleanedOptions.priceScaleId || 'right')
              } catch (error) {
                return null
              }
            },
            remove: () => {
              try {
                signalSeries.destroy()
                delete signalPluginRefs.current[`${chartId}-${seriesIndex}`]
              } catch (error) {
                // Series is already removed - ignore error
              }
            },
          } as unknown as ISeriesApi<any>
        } catch (error) {
          // Failed to create signal series - return null
          return null
        }
      case 'baseline':
        const baselineOptions = {
          ...cleanedOptions,
          baseValue: cleanedOptions.baseValue || { price: 0 },
          topLineColor: cleanedOptions.topLineColor || 'rgba(76, 175, 80, 0.4)',
          topFillColor1: cleanedOptions.topFillColor1 || 'rgba(76, 175, 80, 0.0)',
          topFillColor2: cleanedOptions.topFillColor2 || 'rgba(76, 175, 80, 0.4)',
          bottomLineColor: cleanedOptions.bottomLineColor || 'rgba(255, 82, 82, 0.4)',
          bottomFillColor1: cleanedOptions.bottomFillColor1 || 'rgba(255, 82, 82, 0.4)',
          bottomFillColor2: cleanedOptions.bottomFillColor2 || 'rgba(255, 82, 82, 0.0)',
          lineWidth: cleanedOptions.lineWidth || 2,
          lastValueVisible: lastValueVisible !== undefined ? lastValueVisible : true,
          priceLineVisible: priceLineVisible !== undefined ? priceLineVisible : true,
          priceLineSource: priceLineSource !== undefined ? priceLineSource : 'lastBar',
          priceLineWidth: priceLineWidth !== undefined ? priceLineWidth : 1,
          priceLineColor: priceLineColor !== undefined ? priceLineColor : '',
          priceLineStyle: priceLineStyle !== undefined ? priceLineStyle : 2
        }
        if (priceFormat) {
          baselineOptions.priceFormat = priceFormat
        }

        series = chart.addSeries(BaselineSeries, baselineOptions, paneId)
        break
      case 'histogram':
        const histogramOptions = {
          ...cleanedOptions,
          priceFormat: priceFormat || {
            type: 'volume',
          },
          priceScaleId: cleanedOptions.priceScaleId || '',
          scaleMargins: cleanedOptions.scaleMargins || {
            top: 0.75,
            bottom: 0,
          },
          lastValueVisible: lastValueVisible !== undefined ? lastValueVisible : true,
          color: cleanedOptions.color || '#2196F3',
          priceLineVisible: priceLineVisible !== undefined ? priceLineVisible : true,
          priceLineSource: priceLineSource !== undefined ? priceLineSource : 'lastBar',
          priceLineWidth: priceLineWidth !== undefined ? priceLineWidth : 1,
          priceLineColor: priceLineColor !== undefined ? priceLineColor : '',
          priceLineStyle: priceLineStyle !== undefined ? priceLineStyle : 2
        }

        series = chart.addSeries(HistogramSeries, histogramOptions, paneId)
        break
      case 'line':
        // Handle LineOptions if provided, otherwise use individual properties
        const lineOptionsConfig = seriesConfig.lineOptions || {}
        const lineOptions = {
          ...cleanedOptions,
          color: lineOptionsConfig.color || cleanedOptions.color || '#2196F3',
          lineWidth: lineOptionsConfig.lineWidth || cleanedOptions.lineWidth || 2,
          lineStyle: lineOptionsConfig.lineStyle || cleanedOptions.lineStyle || 0, // LineStyle.Solid
          lineType: lineOptionsConfig.lineType || cleanedOptions.lineType || 0, // LineType.Simple
          lineVisible: lineOptionsConfig.lineVisible !== false && cleanedOptions.lineVisible !== false, // Default true
          pointMarkersVisible: lineOptionsConfig.pointMarkersVisible || cleanedOptions.pointMarkersVisible || false,
          pointMarkersRadius: lineOptionsConfig.pointMarkersRadius || cleanedOptions.pointMarkersRadius,
          crosshairMarkerVisible: lineOptionsConfig.crosshairMarkerVisible !== false && cleanedOptions.crosshairMarkerVisible !== false, // Default true
          crosshairMarkerRadius: lineOptionsConfig.crosshairMarkerRadius || cleanedOptions.crosshairMarkerRadius || 4,
          crosshairMarkerBorderColor: lineOptionsConfig.crosshairMarkerBorderColor || cleanedOptions.crosshairMarkerBorderColor || '',
          crosshairMarkerBackgroundColor: lineOptionsConfig.crosshairMarkerBackgroundColor || cleanedOptions.crosshairMarkerBackgroundColor || '',
          crosshairMarkerBorderWidth: lineOptionsConfig.crosshairMarkerBorderWidth || cleanedOptions.crosshairMarkerBorderWidth || 2,
          lastValueVisible: lastValueVisible !== undefined ? lastValueVisible : true,
          lastPriceAnimation: lastPriceAnimation !== undefined ? lastPriceAnimation : 0,
          priceLineVisible: priceLineVisible !== undefined ? priceLineVisible : true,
          priceLineSource: priceLineSource !== undefined ? priceLineSource : 'lastBar',
          priceLineWidth: priceLineWidth !== undefined ? priceLineWidth : 1,
          priceLineColor: priceLineColor !== undefined ? priceLineColor : '',
          priceLineStyle: priceLineStyle !== undefined ? priceLineStyle : 2
        }
        if (priceFormat) {
          lineOptions.priceFormat = priceFormat
        }

        series = chart.addSeries(LineSeries, lineOptions, paneId)
        
        // Try to apply lastValueVisible after series creation as a fallback
        try {
          if (lastValueVisible === false) {
            series.applyOptions({ lastValueVisible: false })
          }
        } catch (error) {
          console.warn(`❌ Failed to apply lastValueVisible after series creation:`, error)
        }
        break
      case 'bar':
        const barOptions = {
          ...cleanedOptions,
          upColor: cleanedOptions.upColor || '#4CAF50',
          downColor: cleanedOptions.downColor || '#F44336',
          borderVisible: cleanedOptions.borderVisible !== false,
          wickUpColor: cleanedOptions.wickUpColor || '#4CAF50',
          wickDownColor: cleanedOptions.wickDownColor || '#F44336',
          lastValueVisible: lastValueVisible !== undefined ? lastValueVisible : true,
          priceLineVisible: priceLineVisible !== undefined ? priceLineVisible : true,
          priceLineSource: priceLineSource !== undefined ? priceLineSource : 'lastBar',
          priceLineWidth: priceLineWidth !== undefined ? priceLineWidth : 1,
          priceLineColor: priceLineColor !== undefined ? priceLineColor : '',
          priceLineStyle: priceLineStyle !== undefined ? priceLineStyle : 2
        }
        if (priceFormat) {
          barOptions.priceFormat = priceFormat
        }

        series = chart.addSeries(BarSeries, barOptions, paneId)
        break
      case 'candlestick':
        const candlestickOptions = {
          ...cleanedOptions,
          upColor: cleanedOptions.upColor || '#4CAF50',
          downColor: cleanedOptions.downColor || '#F44336',
          borderVisible: cleanedOptions.borderVisible !== false,
          wickUpColor: cleanedOptions.wickUpColor || '#4CAF50',
          wickDownColor: cleanedOptions.wickDownColor || '#F44336',
          lastValueVisible: lastValueVisible !== undefined ? lastValueVisible : true,
          priceLineVisible: priceLineVisible !== undefined ? priceLineVisible : true,
          priceLineSource: priceLineSource !== undefined ? priceLineSource : 'lastBar',
          priceLineWidth: priceLineWidth !== undefined ? priceLineWidth : 1,
          priceLineColor: priceLineColor !== undefined ? priceLineColor : '',
          priceLineStyle: priceLineStyle !== undefined ? priceLineStyle : 2
        }
        if (priceFormat) {
          candlestickOptions.priceFormat = priceFormat
        }

        series = chart.addSeries(CandlestickSeries, candlestickOptions, paneId)
        break
      default:
        // Unknown series type - handled silently in production
        return null
    }

    // Set price scale if specified
    if (priceScale) {
      series.priceScale().applyOptions(cleanLineStyleOptions(priceScale))
    }

    // Set data
    if (data && data.length > 0) {
      series.setData(data)
    }

    // Add price lines attached to this series
    if (seriesConfig.priceLines && Array.isArray(seriesConfig.priceLines)) {
      seriesConfig.priceLines.forEach((priceLine: any, index: number) => {
        try {
          series.createPriceLine(priceLine)
        } catch (error) {
          console.warn(`❌ Failed to create price line ${index + 1} for series:`, error)
        }
      })
    }

    // Add markers attached to this series
    if (seriesConfig.markers && Array.isArray(seriesConfig.markers)) {
      try {
        // Use createSeriesMarkers as per TradingView documentation
        createSeriesMarkers(series, seriesConfig.markers)
      } catch (error) {
        console.warn('❌ Failed to create markers for series:', error)
      }
    }

    return series
  }, [cleanLineStyleOptions])

  const addTradeVisualization = useCallback((chart: IChartApi, series: ISeriesApi<any>, trades: TradeConfig[], options: TradeVisualizationOptions, chartData?: any[]) => {
    if (!trades || trades.length === 0) return;

    try {
      // Create visual elements for trade visualization
      const visualElements = createTradeVisualElements(trades, options, chartData, 'right');
      
      // Add markers to the series
      if (visualElements.markers.length > 0) {
        try {
          createSeriesMarkers(series, visualElements.markers);
        } catch (error) {
          // Silent error handling
        }
      }

      // Add rectangles using the robust plugin
      const chartId = chart.chartElement().id || 'default';
      
      if (!rectanglePluginRefs.current[chartId]) {
        const rectanglePlugin = new TradeRectanglePlugin(chart, series);
        rectanglePluginRefs.current[chartId] = rectanglePlugin;
      }
      
      const rectanglePlugin = rectanglePluginRefs.current[chartId];
      rectanglePlugin.clearRectangles();
      
      visualElements.rectangles.forEach(rect => {
        rectanglePlugin.addRectangle(rect);
      });

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
          console.warn('Error processing visualElements.annotations:', error)
        }
      }
    } catch (error) {
      // Silent error handling
    }
  }, [cleanLineStyleOptions])

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
            layersArray = layersValues
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
          addAnnotations(chart, layer.annotations)
        }
      } catch (error) {
        console.warn(`Error processing layer at index ${index}:`, error, layer)
      }
    })
  }, [addAnnotations])

  const addModularTooltip = useCallback((chart: IChartApi, container: HTMLElement, seriesList: ISeriesApi<any>[], chartConfig: ChartConfig) => {
    // Tooltip implementation will be added here
    // For now, this is a placeholder
  }, [])

  const addRangeSwitcher = useCallback((chart: IChartApi, rangeConfig: any) => {
    // Range switcher implementation will be added here
    // For now, this is a placeholder
  }, [])

  const addLegend = useCallback((chart: IChartApi, legendConfig: LegendConfig, seriesList: ISeriesApi<any>[]) => {
    // Legend implementation will be added here
    // For now, this is a placeholder
  }, [])

  // Initialize charts
  const initializeCharts = useCallback(() => {
    // Clean up existing charts first
    cleanupCharts()

    if (!config || !config.charts || config.charts.length === 0) {
      return
    }

    config.charts.forEach((chartConfig: ChartConfig, chartIndex: number) => {
      const chartId = chartConfig.chartId || `chart-${chartIndex}`
      const containerId = `chart-container-${chartId}`
      
      // Find or create container
      let container = document.getElementById(containerId)
      if (!container) {
        container = document.createElement('div')
        container.id = containerId
        container.style.width = '100%'
        container.style.height = '100%'
        
        // Find the main chart container
        const mainContainer = document.querySelector('[data-testid="stHorizontalBlock"]') || 
                             document.querySelector('.stHorizontalBlock') ||
                             document.body
        mainContainer.appendChild(container)
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

        let chart: IChartApi
        try {
          chart = createChart(container, chartOptions)
        } catch (chartError) {
          console.error(`Failed to create chart for ${chartId}:`, chartError)
          return
        }

        // Check if chart was created successfully
        if (!chart) {
          console.error(`Chart creation returned null for ${chartId}`)
          return
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

              const series = createSeries(chart, seriesConfig, chartId, seriesIndex)
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
                  addTradeVisualization(chart, series, seriesConfig.trades, seriesConfig.tradeVisualizationOptions, seriesConfig.data)
                }
                
                // Add series-level annotations
                if (seriesConfig.annotations) {
                  addAnnotations(chart, seriesConfig.annotations)
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
        addModularTooltip(chart, container, seriesList, chartConfig)

        // Add chart-level trades
        if (chartConfig.trades && chartConfig.series.length > 0) {
          const firstSeries = seriesRefs.current[chartId][0]
          if (firstSeries) {
            // Use trade visualization options from chart config or default
            const tradeOptions = chartConfig.tradeVisualizationOptions || {
              style: 'markers',
              entryMarkerColorLong: '#2196F3',
              entryMarkerColorShort: '#FF9800',
              exitMarkerColorProfit: '#4CAF50',
              exitMarkerColorLoss: '#F44336'
            }
            addTradeVisualization(chart, firstSeries, chartConfig.trades, tradeOptions, chartConfig.series[0]?.data)
          }
        }

        // Add chart-level annotations
        if (chartConfig.annotations) {
          addAnnotations(chart, chartConfig.annotations)
        }

        // Add annotation layers
        if (chartConfig.annotationLayers) {
          addAnnotationLayers(chart, chartConfig.annotationLayers)
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
            addRangeSwitcher(chart, chartConfig.chart.rangeSwitcher)
          }, 100)
        }

        // Add legend if configured
        if (chartConfig.chart?.legend && chartConfig.chart.legend.visible) {
          // Add legend after a short delay to ensure chart is fully initialized
          setTimeout(() => {
            addLegend(chart, chartConfig.chart.legend, seriesList)
          }, 100)
        }

        // Setup auto-sizing for the chart
        setupAutoSizing(chart, container, chartConfig)
        
        // Setup chart synchronization if enabled
        if (config.syncConfig && config.syncConfig.enabled) {
          setupChartSynchronization(chart, chartId, config.syncConfig)
        }
        
        // Setup fitContent functionality
        setupFitContent(chart, chartConfig)

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
  }, [config, cleanupCharts, createSeries, addTradeVisualization, addAnnotations, addModularTooltip, addAnnotationLayers, addRangeSwitcher, addLegend, setupAutoSizing, setupChartSynchronization, setupFitContent, width, height])

  useEffect(() => {
    // Initialize charts when component mounts
    initializeCharts()
    
    // Cleanup on unmount
    return cleanupCharts
  }, [initializeCharts, cleanupCharts])

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