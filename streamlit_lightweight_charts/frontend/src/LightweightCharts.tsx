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
import { ComponentConfig, ChartConfig, SeriesConfig, TradeConfig, TradeVisualizationOptions, Annotation, AnnotationLayer } from './types'
import { createTradeVisualElements } from './tradeVisualization'
import { createAnnotationVisualElements } from './annotationSystem'

interface LightweightChartsProps {
  config: ComponentConfig
  height?: number
  width?: number
}

const LightweightCharts: React.FC<LightweightChartsProps> = ({ config, height = 400, width = 800 }) => {
  const chartRefs = useRef<{ [key: string]: IChartApi }>({})
  const seriesRefs = useRef<{ [key: string]: ISeriesApi<any>[] }>({})
  const [isInitialized, setIsInitialized] = useState(false)

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
        // Create chart
        const chart = createChart(container, {
          width: width,
          height: height,
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
        })

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
        if (chartConfig.rangeSwitcher && chartConfig.rangeSwitcher.visible) {
          addRangeSwitcher(chart, chartConfig.rangeSwitcher)
        }
      } catch (error) {
        // Error creating chart in container
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
        console.warn(`Unknown series type: ${type}`)
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

  const addRangeSwitcher = (chart: IChartApi, rangeConfig: any) => {
    // Create range switcher UI
    const container = chart.chartElement()
    const switcher = document.createElement('div')
    switcher.style.cssText = `
      position: absolute;
      top: 10px;
      right: 10px;
      z-index: 1000;
      background: white;
      border: 1px solid #ccc;
      border-radius: 4px;
      padding: 5px;
    `

    rangeConfig.ranges.forEach((range: any) => {
      const button = document.createElement('button')
      button.textContent = range.label
      button.style.cssText = `
        margin: 0 2px;
        padding: 4px 8px;
        border: 1px solid #ddd;
        border-radius: 3px;
        background: white;
        cursor: pointer;
      `
      button.onclick = () => {
        if (range.seconds) {
          chart.timeScale().setVisibleRange({
            from: (Date.now() / 1000 - range.seconds) as UTCTimestamp,
            to: (Date.now() / 1000) as UTCTimestamp
          })
        }
      }
      switcher.appendChild(button)
    })

    container.appendChild(switcher)
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
        
        return (
          <div key={chartId} style={{ border: '1px solid #ddd', borderRadius: '4px', padding: '10px' }}>
            <div id={containerId} style={{ width: width, height: height }} />
          </div>
        )
      })}
    </div>
  )
}

export default LightweightCharts
