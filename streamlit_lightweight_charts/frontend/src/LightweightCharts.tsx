import React, { useEffect, useRef, useState } from 'react'
import { 
  createChart, 
  IChartApi, 
  ISeriesApi, 
  ColorType, 
  UTCTimestamp,
  AreaSeries,
  LineSeries,
  BarSeries,
  CandlestickSeries,
  HistogramSeries,
  BaselineSeries,
  createSeriesMarkers
} from 'lightweight-charts'
import { ComponentConfig, ChartConfig, SeriesConfig, TradeConfig, TradeVisualizationOptions, Annotation, AnnotationLayer, LegendConfig, TooltipConfig } from './types'
import { createTradeVisualElements } from './tradeVisualization'
import { createAnnotationVisualElements } from './annotationSystem'

interface LightweightChartsProps {
  config: ComponentConfig
  height?: number | null
  width?: number | null
}

const LightweightCharts: React.FC<LightweightChartsProps> = ({ config, height = 400, width = null }) => {
  const chartRefs = useRef<{ [key: string]: IChartApi }>({})
  const seriesRefs = useRef<{ [key: string]: ISeriesApi<any>[] }>({})
  const [isInitialized, setIsInitialized] = useState(false)
  const resizeObserverRef = useRef<ResizeObserver | null>(null)

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
  const resizeChart = (chart: IChartApi, container: HTMLElement, chartConfig: any) => {
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
  }

  // Function to setup auto-sizing for a chart
  const setupAutoSizing = (chart: IChartApi, container: HTMLElement, chartConfig: any) => {
    if (!chartConfig.autoSize && !chartConfig.autoWidth && !chartConfig.autoHeight) {
      return
    }

    // Initial resize
    resizeChart(chart, container, chartConfig)

    // Setup resize observer for container size changes
    if (resizeObserverRef.current) {
      resizeObserverRef.current.disconnect()
    }

    resizeObserverRef.current = new ResizeObserver(() => {
      resizeChart(chart, container, chartConfig)
    })

    resizeObserverRef.current.observe(container)
  }

  useEffect(() => {
    if (!config.charts || config.charts.length === 0) return

    // Initialize charts with retry mechanism
    const initializeCharts = () => {
      config.charts.forEach((chartConfig, index) => {
        const chartId = chartConfig.chartId || `chart-${index}`
        const containerId = `chart-container-${chartId}`
        
        const container = document.getElementById(containerId)
        if (!container) {
          // Retry after a short delay
          setTimeout(() => {
            const retryContainer = document.getElementById(containerId)
            if (retryContainer) {
              createChartInContainer(retryContainer, chartConfig, chartId)
            }
          }, 100)
          return
        }

        createChartInContainer(container, chartConfig, chartId)
      })
    }

    // Function to create chart in a specific container
    const createChartInContainer = (container: HTMLElement, chartConfig: any, chartId: string) => {
      try {
        // Create chart with proper width/height handling for auto-sizing
        const chartOptions = {
          width: chartConfig.chart?.autoWidth ? undefined : (chartConfig.chart?.width || (width || undefined)),
          height: chartConfig.chart?.autoHeight ? undefined : (chartConfig.chart?.height || (height || undefined)),
          layout: {
            background: { type: ColorType.Solid, color: 'white' },
            textColor: 'black',
          },
          grid: {
            vertLines: { color: '#f0f0f0' },
            horzLines: { color: '#f0f0f0' },
          },
          crosshair: {
            mode: 1,
          },
          rightPriceScale: {
            borderColor: '#cccccc',
          },
          leftPriceScale: chartConfig.chart?.leftPriceScale || {
            visible: false,
            borderColor: '#cccccc',
          },
          timeScale: {
            borderColor: '#cccccc',
            timeVisible: true,
            secondsVisible: false,
          },
          ...chartConfig.chart
        }

        const chart = createChart(container, chartOptions)

        chartRefs.current[chartId] = chart

        // Initialize series
        const seriesList: ISeriesApi<any>[] = []
        
        chartConfig.series.forEach((seriesConfig: SeriesConfig, seriesIndex: number) => {
          const series = createSeries(chart, seriesConfig)
          if (series) {
            seriesList.push(series)
            
            // Add trade visualization if configured
            if (seriesConfig.trades && seriesConfig.tradeVisualizationOptions) {
              addTradeVisualization(series, seriesConfig.trades, seriesConfig.tradeVisualizationOptions, seriesConfig.data)
            }
            
            // Add series-level annotations
            if (seriesConfig.annotations) {
              addAnnotations(chart, seriesConfig.annotations)
            }
          }
        })

        seriesRefs.current[chartId] = seriesList

        // Add modular tooltip system
        addModularTooltip(chart, container, seriesList, chartConfig)

        // Add chart-level trades
        if (chartConfig.trades && chartConfig.series.length > 0) {
          const firstSeries = seriesRefs.current[chartId][0]
          if (firstSeries) {
            // Use default trade visualization options if not specified
            const defaultOptions: TradeVisualizationOptions = {
              style: 'markers',
              entryMarkerColorLong: '#2196F3',
              entryMarkerColorShort: '#FF9800',
              exitMarkerColorProfit: '#4CAF50',
              exitMarkerColorLoss: '#F44336'
            }
            addTradeVisualization(firstSeries, chartConfig.trades, defaultOptions, chartConfig.series[0]?.data)
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

              } catch (error) {
          // Error creating chart in container - handled silently in production
        }
    }

    // Start the initialization process
    initializeCharts()

    setIsInitialized(true)

    // Setup synchronization if enabled
    if (config.syncConfig.enabled) {
      setupChartSync()
    }

    // Cleanup function
    return () => {
      Object.values(chartRefs.current).forEach(chart => {
        chart.remove()
      })
      chartRefs.current = {}
      seriesRefs.current = {}
      if (resizeObserverRef.current) {
        resizeObserverRef.current.disconnect()
      }
    }
  }, [config, height, width])

  const createSeries = (chart: IChartApi, seriesConfig: SeriesConfig): ISeriesApi<any> | null => {
    const { type, data, options = {}, name, priceScale } = seriesConfig

    let series: ISeriesApi<any>
    
    // Normalize series type to handle case variations
    const normalizedType = type?.toLowerCase()

    switch (normalizedType) {
      case 'area':
        series = chart.addSeries(AreaSeries, {
          lineColor: '#2196F3',
          topColor: 'rgba(33, 150, 243, 0.4)',
          bottomColor: 'rgba(33, 150, 243, 0.0)',
          lineWidth: 2,
          ...options
        })
        break
      case 'baseline':
        series = chart.addSeries(BaselineSeries, {
          baseValue: { price: 0 },
          topLineColor: 'rgba(76, 175, 80, 0.4)',
          topFillColor1: 'rgba(76, 175, 80, 0.0)',
          topFillColor2: 'rgba(76, 175, 80, 0.4)',
          bottomLineColor: 'rgba(255, 82, 82, 0.4)',
          bottomFillColor1: 'rgba(255, 82, 82, 0.4)',
          bottomFillColor2: 'rgba(255, 82, 82, 0.0)',
          lineWidth: 2,
          ...options
        })
        break
      case 'histogram':
        series = chart.addSeries(HistogramSeries, {
          color: '#2196F3',
          priceFormat: {
            type: 'volume',
          },
          priceScaleId: options.priceScaleId || '',
          scaleMargins: {
            top: 0.8,
            bottom: 0,
          },
          ...options
        })
        break
      case 'line':
        series = chart.addSeries(LineSeries, {
          color: '#2196F3',
          lineWidth: 2,
          ...options
        })
        break
      case 'bar':
        series = chart.addSeries(BarSeries, {
          upColor: '#4CAF50',
          downColor: '#F44336',
          borderVisible: false,
          wickUpColor: '#4CAF50',
          wickDownColor: '#F44336',
          ...options
        })
        break
      case 'candlestick':
        series = chart.addSeries(CandlestickSeries, {
          upColor: '#4CAF50',
          downColor: '#F44336',
          borderVisible: false,
          wickUpColor: '#4CAF50',
          wickDownColor: '#F44336',
          ...options
        })
        break
              default:
          // Unknown series type - handled silently in production
          return null
    }

    // Set price scale if specified
    if (priceScale) {
      series.priceScale().applyOptions(priceScale)
    }

    // Set data
    if (data && data.length > 0) {
      series.setData(data)
    }

    return series
  }

  const addTradeVisualization = (
    series: ISeriesApi<any>,
    trades: TradeConfig[],
    options: TradeVisualizationOptions,
    chartData?: any[]
  ) => {
    const visualElements = createTradeVisualElements(trades, options, chartData)

    // Add markers using the markers plugin
    if (visualElements.markers.length > 0) {
      const seriesMarkers = createSeriesMarkers(series, visualElements.markers)
      // The markers are now set through the plugin
    }

    // Add shapes (rectangles, lines, arrows, zones)
    // REMOVED: if (visualElements.shapes.length > 0) {
    //   visualElements.shapes.forEach(shape => {
    //     series.setShapes([shape])
    //   })
    // }

    // Add annotations
    // REMOVED: if (visualElements.annotations.length > 0) {
    //   visualElements.annotations.forEach(annotation => {
    //     series.setShapes([annotation])
    //   })
    // }
  }

  const addAnnotations = (chart: IChartApi, annotations: Annotation[]) => {
    const visualElements = createAnnotationVisualElements(annotations)

    // Add markers using the markers plugin
    if (visualElements.markers.length > 0) {
      const seriesList = Object.values(seriesRefs.current).flat()
      if (seriesList.length > 0) {
        const seriesMarkers = createSeriesMarkers(seriesList[0], visualElements.markers)
        // The markers are now set through the plugin
      }
    }

    // Add shapes and texts
    // REMOVED: if (visualElements.shapes.length > 0 || visualElements.texts.length > 0) {
    //   const allElements = [...visualElements.shapes, ...visualElements.texts]
    //   const seriesList = Object.values(seriesRefs.current).flat()
    //   if (seriesList.length > 0) {
    //     seriesList[0].setShapes(allElements)
    //   }
    // }
  }

  const addAnnotationLayers = (chart: IChartApi, layers: AnnotationLayer[]) => {
    const allAnnotations = layers
      .filter(layer => layer.visible)
      .flatMap(layer => layer.annotations)

    if (allAnnotations.length > 0) {
      addAnnotations(chart, allAnnotations)
    }
  }

  const addModularTooltip = (chart: IChartApi, container: HTMLElement, seriesList: ISeriesApi<any>[], chartConfig: ChartConfig) => {
    // Check if tooltip is enabled at chart level
    const chartTooltip = chartConfig.tooltip
    if (!chartTooltip || !chartTooltip.enabled) {
      return
    }

    // Create tooltip element
    const tooltip = document.createElement('div')
    
    // Apply default styles
    const defaultStyle = `
      position: absolute;
      display: none;
      background: rgba(255, 255, 255, 0.95);
      border: 1px solid rgba(197, 203, 206, 0.8);
      border-radius: 6px;
      padding: 8px 12px;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      font-size: 12px;
      color: #131722;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
      z-index: 1000;
      pointer-events: none;
      white-space: nowrap;
      line-height: 1.4;
    `

    // Apply custom styles if provided
    const customStyle = chartTooltip.style ? Object.entries(chartTooltip.style)
      .map(([key, value]) => `${key.replace(/([A-Z])/g, '-$1').toLowerCase()}: ${value}`)
      .join('; ') : ''

    tooltip.style.cssText = defaultStyle + (customStyle ? '; ' + customStyle : '')
    container.appendChild(tooltip)

    // Subscribe to crosshair move events
    chart.subscribeCrosshairMove((param) => {
      if (
        param.point === undefined ||
        !param.time ||
        param.point.x < 0 ||
        param.point.x > container.clientWidth ||
        param.point.y < 0 ||
        param.point.y > container.clientHeight
      ) {
        tooltip.style.display = 'none'
        return
      }

      // Build tooltip content based on type
      let tooltipContent = ''
      
      switch (chartTooltip.type) {
        case 'ohlc':
          tooltipContent = buildOHLCTooltip(param, seriesList, chartConfig.series, chartTooltip)
          break
        case 'single':
          tooltipContent = buildSingleSeriesTooltip(param, seriesList[0], chartConfig.series[0], chartTooltip)
          break
        case 'multi':
          tooltipContent = buildMultiSeriesTooltip(param, seriesList, chartConfig.series, chartTooltip)
          break
        case 'custom':
          tooltipContent = buildCustomTooltip(param, seriesList, chartConfig.series, chartTooltip)
          break
        default:
          tooltipContent = buildDefaultTooltip(param, seriesList, chartConfig.series, chartTooltip)
      }

      if (!tooltipContent) {
        tooltip.style.display = 'none'
        return
      }

      tooltip.innerHTML = tooltipContent
      tooltip.style.display = 'block'

      // Position tooltip
      positionTooltip(tooltip, param, container, chartTooltip)
    })
  }



  const buildOHLCTooltip = (param: any, seriesList: ISeriesApi<any>[], seriesConfigs: SeriesConfig[], tooltipConfig: TooltipConfig): string => {
    const seriesData = param.seriesData.get(seriesList[0])
    if (!seriesData) return ''

    // Type guard for OHLC data
    const isOHLC = (d: any): d is { open: number, high: number, low: number, close: number } =>
      d && typeof d.open === 'number' && typeof d.high === 'number' && typeof d.low === 'number' && typeof d.close === 'number'

    if (!isOHLC(seriesData)) return ''

    let content = ''
    
    // Use custom fields if provided, otherwise use default OHLC fields
    const fields = tooltipConfig.fields.length > 0 ? tooltipConfig.fields : [
      { label: 'Open', valueKey: 'open' },
      { label: 'High', valueKey: 'high' },
      { label: 'Low', valueKey: 'low' },
      { label: 'Close', valueKey: 'close' }
    ]

    fields.forEach(field => {
      const value = seriesData[field.valueKey as keyof typeof seriesData]
      if (value !== undefined) {
        const formattedValue = field.formatter ? field.formatter(value) : typeof value === 'number' ? value.toFixed(2) : String(value)
        const style = `color: ${field.color || '#787b86'}; font-size: ${field.fontSize || 11}px; font-weight: ${field.fontWeight || 'normal'}`
        content += `<div style="${style}">${field.label}: ${formattedValue}</div>`
      }
    })

    // Add date/time if configured
    if (tooltipConfig.showDate || tooltipConfig.showTime) {
      const dateStr = formatDateTime(param.time, tooltipConfig)
      if (dateStr) {
        content += `<div style="color: #787b86; font-size: 11px; margin-top: 4px;">${dateStr}</div>`
      }
    }

    return content
  }

  const buildSingleSeriesTooltip = (param: any, series: ISeriesApi<any>, seriesConfig: SeriesConfig, tooltipConfig: TooltipConfig): string => {
    const seriesData = param.seriesData.get(series)
    if (!seriesData) return ''

    const seriesName = seriesConfig?.name || 'Price'
    let content = `<div style="font-weight: 500; margin-bottom: 4px;">${seriesName}</div>`

    // Use custom fields if provided
    if (tooltipConfig.fields.length > 0) {
      tooltipConfig.fields.forEach(field => {
        const value = seriesData[field.valueKey as keyof typeof seriesData]
        if (value !== undefined) {
          const formattedValue = field.formatter ? field.formatter(value) : typeof value === 'number' ? value.toFixed(2) : String(value)
          const style = `color: ${field.color || '#787b86'}; font-size: ${field.fontSize || 11}px; font-weight: ${field.fontWeight || 'normal'}`
          content += `<div style="${style}">${field.label}: ${formattedValue}</div>`
        }
      })
    } else {
      // Default behavior for single series
      if ('value' in seriesData && typeof seriesData.value === 'number') {
        content += `<div style="color: #787b86; font-size: 11px;">Value: ${seriesData.value.toFixed(2)}</div>`
      } else if ('volume' in seriesData && typeof seriesData.volume === 'number') {
        content += `<div style="color: #787b86; font-size: 11px;">Volume: ${seriesData.volume.toLocaleString()}</div>`
      }
    }

    // Add date/time if configured
    if (tooltipConfig.showDate || tooltipConfig.showTime) {
      const dateStr = formatDateTime(param.time, tooltipConfig)
      if (dateStr) {
        content += `<div style="color: #787b86; font-size: 11px; margin-top: 4px;">${dateStr}</div>`
      }
    }

    return content
  }

  const buildMultiSeriesTooltip = (param: any, seriesList: ISeriesApi<any>[], seriesConfigs: SeriesConfig[], tooltipConfig: TooltipConfig): string => {
    let content = ''

    // Use custom fields if provided, otherwise show all series values
    if (tooltipConfig.fields.length > 0) {
      tooltipConfig.fields.forEach(field => {
        const seriesIndex = parseInt(field.valueKey) || 0
        if (seriesIndex < seriesList.length) {
          const seriesData = param.seriesData.get(seriesList[seriesIndex])
          if (seriesData) {
            const value = getValueFromData(seriesData, field.valueKey)
            if (value !== null) {
              const formattedValue = field.formatter ? field.formatter(value) : typeof value === 'number' ? value.toFixed(2) : String(value)
              const style = `color: ${field.color || '#131722'}; font-weight: ${field.fontWeight || '500'}`
              content += `<div style="${style}">${field.label}: ${formattedValue}</div>`
            }
          }
        }
      })
    } else {
      // Default multi-series behavior
      seriesList.forEach((series, index) => {
        const seriesData = param.seriesData.get(series)
        const seriesName = seriesConfigs[index]?.name || `Series ${index + 1}`
        
        if (seriesData) {
          const value = getValueFromData(seriesData)
          if (value !== null) {
            content += `<div style="color: #131722; font-weight: 500;">${seriesName}: ${value.toFixed(2)}</div>`
          }
        }
      })
    }

    // Add date/time if configured
    if (tooltipConfig.showDate || tooltipConfig.showTime) {
      const dateStr = formatDateTime(param.time, tooltipConfig)
      if (dateStr) {
        content += `<div style="color: #787b86; font-size: 11px; margin-top: 4px;">${dateStr}</div>`
      }
    }

    return content
  }

  const buildCustomTooltip = (param: any, seriesList: ISeriesApi<any>[], seriesConfigs: SeriesConfig[], tooltipConfig: TooltipConfig): string => {
    let content = ''

    // Build content based on custom fields
    tooltipConfig.fields.forEach(field => {
      // Try to get value from any series that has this field
      let value: any = null
      
      for (let i = 0; i < seriesList.length; i++) {
        const seriesData = param.seriesData.get(seriesList[i])
        if (seriesData && field.valueKey in seriesData) {
          value = seriesData[field.valueKey as keyof typeof seriesData]
          break
        }
      }

      if (value !== null && value !== undefined) {
        const formattedValue = field.formatter ? field.formatter(value) : typeof value === 'number' ? value.toFixed(2) : String(value)
        const style = `color: ${field.color || '#131722'}; font-size: ${field.fontSize || 12}px; font-weight: ${field.fontWeight || 'normal'}`
        content += `<div style="${style}">${field.label}: ${formattedValue}</div>`
      }
    })

    // Add date/time if configured
    if (tooltipConfig.showDate || tooltipConfig.showTime) {
      const dateStr = formatDateTime(param.time, tooltipConfig)
      if (dateStr) {
        content += `<div style="color: #787b86; font-size: 11px; margin-top: 4px;">${dateStr}</div>`
      }
    }

    return content
  }

  const buildDefaultTooltip = (param: any, seriesList: ISeriesApi<any>[], seriesConfigs: SeriesConfig[], tooltipConfig: TooltipConfig): string => {
    // Default behavior based on number of series
    if (seriesList.length === 1) {
      return buildSingleSeriesTooltip(param, seriesList[0], seriesConfigs[0], tooltipConfig)
    } else if (seriesList.length >= 2) {
      return buildMultiSeriesTooltip(param, seriesList, seriesConfigs, tooltipConfig)
    }
    return ''
  }

  const getValueFromData = (data: any, valueKey?: string): number | null => {
    if (valueKey && valueKey in data) {
      return data[valueKey]
    }
    
    // Try common value keys
    if ('value' in data && typeof data.value === 'number') return data.value
    if ('close' in data && typeof data.close === 'number') return data.close
    if ('high' in data && typeof data.high === 'number') return data.high
    if ('low' in data && typeof data.low === 'number') return data.low
    if ('open' in data && typeof data.open === 'number') return data.open
    
    return null
  }

  const formatDateTime = (time: any, tooltipConfig: TooltipConfig): string => {
    if (!time) return ''
    
    let dateStr = ''
    
    if (tooltipConfig.showDate) {
      if (typeof time === 'string') {
        dateStr = time
      } else {
        const date = new Date((time as number) * 1000)
        // For now, use default formatting since custom format is not supported in toLocaleDateString
        dateStr = date.toLocaleDateString()
      }
    }
    
    if (tooltipConfig.showTime) {
      const date = typeof time === 'string' ? new Date(time) : new Date((time as number) * 1000)
      // For now, use default formatting since custom format is not supported in toLocaleTimeString
      const timeStr = date.toLocaleTimeString()
      
      if (dateStr) {
        dateStr += ` ${timeStr}`
      } else {
        dateStr = timeStr
      }
    }
    
    return dateStr
  }

  const positionTooltip = (tooltip: HTMLElement, param: any, container: HTMLElement, tooltipConfig: TooltipConfig) => {
    const tooltipWidth = tooltip.offsetWidth
    const tooltipHeight = tooltip.offsetHeight
    
    let left = param.point.x
    let top = param.point.y
    
    // Apply offset if configured
    if (tooltipConfig.offset) {
      left += tooltipConfig.offset.x
      top += tooltipConfig.offset.y
    } else {
      // Default offset
      left += 12
      top -= tooltipHeight + 12
    }
    
    // Adjust position to keep tooltip within container bounds
    if (left + tooltipWidth > container.clientWidth) {
      left = param.point.x - tooltipWidth - 12
    }
    
    if (top < 0) {
      top = param.point.y + 12
    }
    
    tooltip.style.left = `${left}px`
    tooltip.style.top = `${top}px`
  }

  const addRangeSwitcher = (chart: IChartApi, rangeConfig: any) => {
    // Create range switcher UI
    const container = chart.chartElement()
    
    // Ensure the chart container has relative positioning
    if (container) {
      container.style.position = 'relative'
    } else {
      // Chart container not found - handled silently in production
      return
    }
    
    // Remove any existing switcher
    const oldSwitcher = container.querySelector('.range-switcher')
    if (oldSwitcher) oldSwitcher.remove()

    const switcher = document.createElement('div')
    switcher.className = 'range-switcher'
    // ---
    // Position the switcher inside the plot area, never over the y-axis or x-axis
    // We use pointer-events: auto so it is clickable, and a transform to offset from the axis
    // The offset is set to 12px from the top and 12px from the right of the plot area
    // ---
    // Determine position based on rangeConfig
    const getPositionStyles = (position: string) => {
      switch (position) {
        case 'top-left':
          return 'top: 12px; left: 12px;'
        case 'top-right':
          return 'top: 12px; right: 12px;'
        case 'bottom-left':
          return 'bottom: 12px; left: 12px;'
        case 'bottom-right':
          return 'bottom: 12px; right: 12px;'
        default:
          return 'top: 12px; right: 12px;'
      }
    }
    // Ensure position is set correctly
    const position = rangeConfig.position || 'top-right'
    
    switcher.style.cssText = `
      position: absolute;
      ${getPositionStyles(position)}
      z-index: 10;
      display: flex;
      flex-direction: row;
      gap: 4px;
      background: rgba(255, 255, 255, 0.95);
      border-radius: 6px;
      padding: 2px;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
      border: 1px solid rgba(197, 203, 206, 0.3);
      pointer-events: auto;
      transition: box-shadow 0.2s;
    `

    // Track active button
    let activeButton: HTMLButtonElement | null = null

    // Default TradingView-style ranges if not provided
    const defaultRanges = [
      { label: "1D", seconds: 86400 },
      { label: "1W", seconds: 604800 },
      { label: "1M", seconds: 2592000 },
      { label: "1Y", seconds: 31536000 }
    ]
    
    const ranges = rangeConfig.ranges || defaultRanges
    const defaultRange = rangeConfig.defaultRange || "1D"



    ranges.forEach((range: any) => {
      const button = document.createElement('button')
      button.textContent = range.label
      button.style.cssText = `
        all: initial;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
        font-size: 13px;
        font-weight: 500;
        line-height: 1.2;
        padding: 6px 12px;
        color: #131722;
        background-color: transparent;
        border-radius: 4px;
        cursor: pointer;
        border: none;
        transition: all 0.15s ease;
        min-width: 32px;
        text-align: center;
        user-select: none;
      `

      // Set initial active state
      if (range.label === defaultRange) {
        button.style.backgroundColor = '#2962ff'
        button.style.color = 'white'
        activeButton = button
      }

      // Add hover effects
      button.addEventListener('mouseenter', () => {
        if (button !== activeButton) {
          button.style.backgroundColor = 'rgba(41, 98, 255, 0.1)'
          button.style.color = '#2962ff'
        }
      })

      button.addEventListener('mouseleave', () => {
        if (button !== activeButton) {
          button.style.backgroundColor = 'transparent'
          button.style.color = '#131722'
        }
      })

      button.addEventListener('click', () => {
        // Update button styles
        if (activeButton) {
          activeButton.style.backgroundColor = 'transparent'
          activeButton.style.color = '#131722'
        }
        button.style.backgroundColor = '#2962ff'
        button.style.color = 'white'
        activeButton = button

        // Apply time range
        if (range.seconds !== null) {
          const now = Math.floor(Date.now() / 1000)
          const from = now - range.seconds
          chart.timeScale().setVisibleRange({
            from: from as UTCTimestamp,
            to: now as UTCTimestamp
          })
        } else {
          // "ALL" range - fit content
          chart.timeScale().fitContent()
        }

        // Send callback if configured
        if (config.callbacks?.includes('onRangeSwitcherChange')) {
          // This would need to be implemented with proper callback handling
        }
      })

      switcher.appendChild(button)
    })

    container.appendChild(switcher)
  }

  const addLegend = (chart: IChartApi, legendConfig: LegendConfig, seriesList: ISeriesApi<any>[]) => {
    const container = chart.chartElement()
          if (!container) {
        // Chart container not found - handled silently in production
        return
      }

    // Ensure the chart container has relative positioning
    container.style.position = 'relative'

    // Remove any existing legend
    const oldLegend = container.querySelector('.legend')
    if (oldLegend) oldLegend.remove()

    // Determine position based on legendConfig
    const getPositionStyles = (position: string) => {
      switch (position) {
        case 'top-left':
          return 'top: 12px; left: 12px;'
        case 'top-right':
          return 'top: 12px; right: 12px;'
        case 'bottom-left':
          return 'bottom: 12px; left: 12px;'
        case 'bottom-right':
          return 'bottom: 12px; right: 12px;'
        default:
          return 'bottom: 12px; left: 12px;'
      }
    }

    const legend = document.createElement('div')
    legend.className = 'legend'
    legend.style.cssText = `
      position: absolute;
      ${getPositionStyles(legendConfig.position)}
      z-index: ${legendConfig.zIndex || 10};
      display: flex;
      flex-direction: column;
      gap: 4px;
      background: ${legendConfig.backgroundColor || 'rgba(255, 255, 255, 0.95)'};
      border-radius: ${legendConfig.borderRadius || 6}px;
      padding: ${legendConfig.padding || 8}px;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
      border: ${legendConfig.borderWidth || 1}px solid ${legendConfig.borderColor || 'rgba(197, 203, 206, 0.3)'};
      pointer-events: auto;
      transition: box-shadow 0.2s;
      font-family: ${legendConfig.fontFamily || 'sans-serif'};
      font-size: ${legendConfig.fontSize || 12}px;
      font-weight: ${legendConfig.fontWeight || '300'};
      color: ${legendConfig.color || '#131722'};
    `

    // Create legend content based on type
    if (legendConfig.type === 'simple') {
      const simpleLegend = document.createElement('div')
      simpleLegend.className = 'simple-legend'
      simpleLegend.style.cssText = `
        display: flex;
        flex-direction: row;
        gap: 8px;
        align-items: center;
      `
      
      // Add symbol name if provided
      if (legendConfig.showSymbol && legendConfig.symbolName) {
        const symbolSpan = document.createElement('span')
        symbolSpan.textContent = legendConfig.symbolName
        symbolSpan.style.fontWeight = 'bold'
        simpleLegend.appendChild(symbolSpan)
      }

      // Add price display
      if (legendConfig.showLastValue) {
        const priceLabel = document.createElement('span')
        priceLabel.textContent = 'Price:'
        simpleLegend.appendChild(priceLabel)

        const priceValue = document.createElement('span')
        priceValue.className = 'price-value'
        priceValue.textContent = '--'
        simpleLegend.appendChild(priceValue)
      }

      legend.appendChild(simpleLegend)
    } else if (legendConfig.type === '3line') {
      const threeLineLegend = document.createElement('div')
      threeLineLegend.className = 'three-line-legend'
      threeLineLegend.style.cssText = `
        display: flex;
        flex-direction: column;
        gap: 2px;
        align-items: flex-start;
      `

      // Line 1: Symbol name
      if (legendConfig.showSymbol && legendConfig.symbolName) {
        const symbolLine = document.createElement('div')
        symbolLine.style.fontWeight = 'bold'
        symbolLine.textContent = legendConfig.symbolName
        threeLineLegend.appendChild(symbolLine)
      }

      // Line 2: Price
      if (legendConfig.showLastValue) {
        const priceLine = document.createElement('div')
        priceLine.style.cssText = `
          display: flex;
          gap: 4px;
        `
        const priceLabel = document.createElement('span')
        priceLabel.textContent = 'Price:'
        priceLine.appendChild(priceLabel)

        const priceValue = document.createElement('span')
        priceValue.className = 'price-value'
        priceValue.textContent = '--'
        priceLine.appendChild(priceValue)
        threeLineLegend.appendChild(priceLine)
      }

      // Line 3: Time
      if (legendConfig.showTime) {
        const timeLine = document.createElement('div')
        timeLine.style.cssText = `
          display: flex;
          gap: 4px;
        `
        const timeLabel = document.createElement('span')
        timeLabel.textContent = 'Time:'
        timeLine.appendChild(timeLabel)

        const timeValue = document.createElement('span')
        timeValue.className = 'time-value'
        timeValue.textContent = '--'
        timeLine.appendChild(timeValue)
        threeLineLegend.appendChild(timeLine)
      }

      legend.appendChild(threeLineLegend)
    }

    // Add crosshair subscription for real-time updates
    chart.subscribeCrosshairMove((param) => {
      const priceElements = legend.querySelectorAll('.price-value')
      const timeElements = legend.querySelectorAll('.time-value')

      if (param.time !== undefined && param.seriesData && seriesList.length > 0) {
        // Get the first series data
        const firstSeries = seriesList[0]
        const data = param.seriesData.get(firstSeries)
        
        if (data) {
          // Extract price from data
          let price: number | undefined
          if ('value' in data) {
            price = data.value as number
          } else if ('close' in data) {
            price = data.close as number
          } else if ('high' in data) {
            price = data.high as number
          }

          // Update price values
          if (price !== undefined) {
            const priceString = price.toFixed(parseInt(legendConfig.priceFormat || '2'))
            priceElements.forEach((element) => {
              element.textContent = priceString
            })
          }

          // Update time values
          let timeString = '--'
          if (typeof param.time === 'number') {
            timeString = new Date(param.time * 1000).toLocaleTimeString()
          } else if (typeof param.time === 'string' || typeof param.time === 'object') {
            // Try to parse as date string or business day
            try {
              timeString = new Date(param.time as any).toLocaleTimeString()
            } catch {}
          }
          timeElements.forEach((element) => {
            element.textContent = timeString
          })
        }
      } else {
        // Reset values when crosshair is not over data
        priceElements.forEach((element) => {
          element.textContent = '--'
        })
        timeElements.forEach((element) => {
          element.textContent = '--'
        })
      }
    })

    container.appendChild(legend)
  }

  const setupChartSync = () => {
    const charts = Object.values(chartRefs.current)
    
    if (charts.length < 2) return

    charts.forEach((chart, index) => {
      // Sync crosshair
      if (config.syncConfig.crosshair) {
        chart.subscribeCrosshairMove((param) => {
          const seriesList = Object.values(seriesRefs.current)[index] || [];
          const firstSeries = seriesList[0];
          let price: number | undefined = undefined;
          if (firstSeries && param.seriesData) {
            const data = param.seriesData.get(firstSeries);
            if (data) {
              // Try to get price from value (line/area/histogram), or close (candlestick/bar)
              price = (data as any).value ?? (data as any).close;
            }
          }
          charts.forEach((otherChart, otherIndex) => {
            if (otherIndex !== index && price !== undefined && param.time !== undefined && firstSeries) {
              otherChart.setCrosshairPosition(price, param.time, firstSeries);
            }
          })
        })
      }

      // Sync time range
      if (config.syncConfig.timeRange) {
        chart.timeScale().subscribeVisibleTimeRangeChange((param) => {
          if (param !== null) {
            charts.forEach((otherChart, otherIndex) => {
              if (otherIndex !== index) {
                otherChart.timeScale().setVisibleRange(param)
              }
            })
          }
        })
      }
    })
  }

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
          width: shouldAutoSize || width === null ? '100%' : width || '100%', // Use 100% if auto-sizing or width is null
          height: shouldAutoSize ? '100%' : height || '100%', // Use height if available, otherwise 100%
          minWidth: chartOptions.minWidth || chartConfig.minWidth || (shouldAutoSize ? 200 : undefined),
          minHeight: chartOptions.minHeight || chartConfig.minHeight || (shouldAutoSize ? 200 : undefined),
          maxWidth: chartOptions.maxWidth || chartConfig.maxWidth,
          maxHeight: chartOptions.maxHeight || chartConfig.maxHeight,
        }
        
        const chartContainerStyle: React.CSSProperties = {
          width: shouldAutoSize || width === null ? '100%' : width || '100%', // Use 100% if auto-sizing or width is null
          height: shouldAutoSize ? '100%' : height || '100%', // Use height if available, otherwise 100%
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
