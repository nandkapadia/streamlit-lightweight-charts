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
        return LineStyle.Solid
      }
    }
    
    // Invalid line style, return undefined to use default
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
    
    // Clean nested line objects (for band series)
    if (cleaned.upperLine && typeof cleaned.upperLine === 'object') {
      cleaned.upperLine = cleanLineStyleOptions(cleaned.upperLine)
    }
    if (cleaned.middleLine && typeof cleaned.middleLine === 'object') {
      cleaned.middleLine = cleanLineStyleOptions(cleaned.middleLine)
    }
    if (cleaned.lowerLine && typeof cleaned.lowerLine === 'object') {
      cleaned.lowerLine = cleanLineStyleOptions(cleaned.lowerLine)
    }
    
    // Recursively clean any other nested objects
    for (const key in cleaned) {
      if (cleaned[key] && typeof cleaned[key] === 'object' && !Array.isArray(cleaned[key])) {
        cleaned[key] = cleanLineStyleOptions(cleaned[key])
      }
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
      priceLineStyle: topLevelPriceLineStyle,
      priceScaleId: topLevelPriceScaleId
    } = seriesConfig
    


    
    // Check both top-level and options for lastValueVisible
    const lastValueVisible = topLevelLastValueVisible !== undefined ? topLevelLastValueVisible : options.lastValueVisible
    
    // Check both top-level and options for price line properties
    const priceLineVisible = topLevelPriceLineVisible !== undefined ? topLevelPriceLineVisible : options.priceLineVisible
    const priceLineSource = topLevelPriceLineSource !== undefined ? topLevelPriceLineSource : options.priceLineSource
    const priceLineWidth = topLevelPriceLineWidth !== undefined ? topLevelPriceLineWidth : options.priceLineWidth
    const priceLineColor = topLevelPriceLineColor !== undefined ? topLevelPriceLineColor : options.priceLineColor
    const priceLineStyle = topLevelPriceLineStyle !== undefined ? topLevelPriceLineStyle : options.priceLineStyle
    
    // Check both top-level and options for priceScaleId
    const priceScaleId = topLevelPriceScaleId !== undefined ? topLevelPriceScaleId : options.priceScaleId
    

    


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
          priceScaleId: priceScaleId || '',
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
          // Failed to apply lastValueVisible after area series creation
        }
        break
      case 'band':
        console.log(`🔧 [createSeries] Creating band series`)
        try {
          // Create band series using the custom plugin
          const bandSeriesOptions = {
            upperLine: cleanedOptions.upperLine || {
              color: '#4CAF50',
              lineStyle: 0,
              lineWidth: 2,
              lineVisible: true,
            },
            middleLine: cleanedOptions.middleLine || {
              color: '#2196F3',
              lineStyle: 0,
              lineWidth: 2,
              lineVisible: true,
            },
            lowerLine: cleanedOptions.lowerLine || {
              color: '#F44336',
              lineStyle: 0,
              lineWidth: 2,
              lineVisible: true,
            },
            upperFillColor: cleanedOptions.upperFillColor || 'rgba(76, 175, 80, 0.1)',
            lowerFillColor: cleanedOptions.lowerFillColor || 'rgba(244, 67, 54, 0.1)',
            priceScaleId: priceScaleId || 'right',
            visible: cleanedOptions.visible !== false,
            lastValueVisible: lastValueVisible !== undefined ? lastValueVisible : true,
            priceLineVisible: priceLineVisible !== undefined ? priceLineVisible : true,
            priceLineSource: priceLineSource !== undefined ? priceLineSource : 'lastBar',
            priceLineWidth: priceLineWidth !== undefined ? priceLineWidth : 1,
            priceLineColor: priceLineColor !== undefined ? priceLineColor : '',
            priceLineStyle: priceLineStyle !== undefined ? priceLineStyle : 2
          }
          console.log(`🔧 [createSeries] Band series options:`, bandSeriesOptions)
          const bandSeries = createBandSeries(chart, bandSeriesOptions)
          
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
                return chart.priceScale(priceScaleId || 'right')
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
                return chart.priceScale(priceScaleId || 'right')
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
          priceScaleId: priceScaleId || '',
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
          priceScaleId: priceScaleId || '',
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
          priceScaleId: priceScaleId || '',
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
          priceScaleId: priceScaleId || '',
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
          priceScaleId: priceScaleId || '',
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
    console.log('🔍 [addTradeVisualization] Starting trade visualization:', {
      tradesCount: trades?.length,
      options,
      chartDataCount: chartData?.length
    });

    if (!trades || trades.length === 0) {
      console.log('❌ [addTradeVisualization] No trades provided');
      return;
    }

    // Check if time scale is properly initialized
    const timeScale = chart.timeScale();
    const visibleRange = timeScale.getVisibleRange();
    console.log('🔍 [addTradeVisualization] Time scale visible range:', visibleRange);
    
    // Check if chart has data and time scale is ready
    if (!visibleRange || !visibleRange.from || !visibleRange.to) {
      console.warn('⚠️ [addTradeVisualization] Time scale not properly initialized, waiting...');
      // Retry after a short delay
      setTimeout(() => {
        addTradeVisualization(chart, series, trades, options, chartData);
      }, 200);
      return;
    }
    
    // Additional check: ensure the time scale has a reasonable range
    const timeRange = Number(visibleRange.to ?? 0) - Number(visibleRange.from ?? 0);
    if (timeRange < 1000) { // Less than 1000 seconds (about 16 minutes)
      console.warn('⚠️ [addTradeVisualization] Time scale range too small, waiting for more data...');
      setTimeout(() => {
        addTradeVisualization(chart, series, trades, options, chartData);
      }, 200);
      return;
    }

    try {
      // Use default price scale ID for now
      const priceScaleId = 'right';
      console.log('🔍 [addTradeVisualization] Using price scale ID:', priceScaleId);
      
      // Create visual elements for trade visualization
      const visualElements = createTradeVisualElements(trades, options, chartData, priceScaleId);
      
      console.log('🔍 [addTradeVisualization] Visual elements created:', {
        markersCount: visualElements.markers.length,
        rectanglesCount: visualElements.rectangles.length,
        annotationsCount: visualElements.annotations.length
      });
      
      // Add markers to the series
      if (visualElements.markers.length > 0) {
        try {
          createSeriesMarkers(series, visualElements.markers);
          console.log('✅ [addTradeVisualization] Markers added successfully');
        } catch (error) {
          console.warn('❌ [addTradeVisualization] Error adding markers:', error);
        }
      }

      // Add rectangles using the robust plugin
      const chartId = chart.chartElement().id || 'default';
      
      if (!rectanglePluginRefs.current[chartId]) {
        const rectanglePlugin = new TradeRectanglePlugin(chart, series);
        rectanglePluginRefs.current[chartId] = rectanglePlugin;
        console.log('✅ [addTradeVisualization] Created new rectangle plugin for chart:', chartId);
      }
      
      const rectanglePlugin = rectanglePluginRefs.current[chartId];
      rectanglePlugin.clearRectangles();
      
      console.log('🔍 [addTradeVisualization] Adding rectangles:', visualElements.rectangles);
      visualElements.rectangles.forEach((rect, index) => {
        rectanglePlugin.addRectangle(rect);
        console.log(`✅ [addTradeVisualization] Added rectangle ${index}:`, rect);
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
          console.log('✅ [addTradeVisualization] Annotations added successfully');
        } catch (error) {
          console.warn('❌ [addTradeVisualization] Error processing annotations:', error)
        }
      }
    } catch (error) {
      console.error('❌ [addTradeVisualization] Error in trade visualization:', error);
    }
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
    console.log("🎯 [addLegend] Starting legend creation with config:", legendConfig)
    console.log("🎯 [addLegend] Series list length:", seriesList.length)
    if (!legendConfig.visible || seriesList.length === 0) {
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
            const paneMargin = 12 // Use TradingView's margin
            
            // Calculate pane boundaries using the chart's layout
            const chartElement = chart.chartElement()
            const chartRect = chartElement.getBoundingClientRect()
            const chartHeight = chartRect.height
            
            // Use the actual relative factors from Python: [3.0, 1.5, 1.0] / 5.5
            const paneHeights = [3.0/5.5, 1.5/5.5, 1.0/5.5] // Exact relative heights from Python config
            let paneTopOffset = 0
            
            // Calculate the top offset for this pane
            for (let i = 0; i < paneId; i++) {
              paneTopOffset += paneHeights[i] * chartHeight
            }
            
            const paneHeight = paneHeights[paneId] * chartHeight
            
            // Position legend within the calculated pane boundaries
            switch (position) {
              case 'top-left':
                legendContainer.style.top = `${paneTopOffset + paneMargin}px`
                legendContainer.style.left = `${paneMargin}px`
                break
              case 'top-right':
                legendContainer.style.top = `${paneTopOffset + paneMargin}px`
                legendContainer.style.right = `${paneMargin}px`
                break
              case 'bottom-left':
                legendContainer.style.top = `${paneTopOffset + paneHeight - 80}px` // Fixed height for legend
                legendContainer.style.left = `${paneMargin}px`
                break
              case 'bottom-right':
                legendContainer.style.top = `${paneTopOffset + paneHeight - 80}px` // Fixed height for legend
                legendContainer.style.right = `${paneMargin}px`
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
          console.log(`🔧 [createChart] Creating chart with options:`, chartOptions)
        console.log(`🔍 [createChart] Full chart config:`, JSON.stringify(chartConfig, null, 2))
          chart = createChart(container, chartOptions)
          console.log(`🔧 [createChart] Chart created successfully:`, chart)
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
          console.log(`🔧 [createChart] Creating ${chartConfig.series.length} series`)
          chartConfig.series.forEach((seriesConfig: SeriesConfig, seriesIndex: number) => {
            try {
              console.log(`🔧 [createChart] Creating series ${seriesIndex}:`, seriesConfig)
              if (!seriesConfig || typeof seriesConfig !== 'object') {
                console.warn(`Invalid series config at index ${seriesIndex}:`, seriesConfig)
                return
              }

              const series = createSeries(chart, seriesConfig, chartId, seriesIndex)
              console.log(`🔧 [createChart] Series ${seriesIndex} created:`, series)
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

        // Add chart-level trades with delay to ensure chart is fully initialized
        console.log('🔍 [createChart] Checking for chart-level trades:', {
          hasTrades: !!chartConfig.trades,
          tradesCount: chartConfig.trades?.length,
          hasSeries: chartConfig.series.length > 0,
          hasTradeOptions: !!chartConfig.tradeVisualizationOptions,
          trades: chartConfig.trades,
          tradeOptions: chartConfig.tradeVisualizationOptions
        });
        
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
            console.log('🔍 [createChart] Adding chart-level trade visualization with options:', tradeOptions);
            
            // Add trade visualization after a delay to ensure chart is fully initialized
            setTimeout(() => {
              console.log('🔍 [createChart] Adding trade visualization after delay');
              
              // Ensure chart is fitted to content first
              try {
                chart.timeScale().fitContent()
                console.log('✅ [createChart] Chart fitted to content')
              } catch (error) {
                console.warn('⚠️ [createChart] Could not fit content:', error)
              }
              
              // Add a small additional delay to ensure fitContent is applied
              setTimeout(() => {
                addTradeVisualization(chart, firstSeries, chartConfig.trades ?? [], tradeOptions, chartConfig.series[0]?.data)
              }, 100)
            }, 500) // 500ms delay to ensure chart data is loaded and time scale is ready
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
        console.log("🔍 [createChart] Legend check:", {
          hasChart: !!chartConfig.chart,
          hasLegend: !!chartConfig.chart?.legend,
          legendVisible: chartConfig.chart?.legend?.visible,
          legendConfig: chartConfig.chart?.legend
        })
        console.log("🔍 [createChart] Full legend config:", JSON.stringify(chartConfig.chart?.legend, null, 2))
        
        if (chartConfig.chart?.legend && chartConfig.chart.legend.visible) {
          console.log("✅ [createChart] Adding legend with config:", chartConfig.chart.legend)
          // Add legend after a short delay to ensure chart is fully initialized
          setTimeout(() => {
            addLegend(chart, chartConfig.chart.legend, seriesList)
          }, 100)
        } else {
          console.log("❌ [createChart] Legend not added - missing or not visible")
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
  }, [config, cleanupCharts, createSeries, addTradeVisualization, addAnnotations, addModularTooltip, addAnnotationLayers, addRangeSwitcher, addLegend, setupAutoSizing, setupChartSynchronization, setupFitContent, cleanLineStyleOptions, width, height])

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