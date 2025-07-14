import React, { useRef, useEffect, useCallback, useState } from "react"
import { useRenderData } from "streamlit-component-lib-react-hooks"
import {
  createChart,
  IChartApi,
  ISeriesApi,
  SeriesType,
  MouseEventParams,
  TimeRange,
  LogicalRange,
  BusinessDay,
  Time,
  LineData,
  HistogramData,
  AreaData,
  BarData,
  CandlestickData,
  BaselineData,
  SeriesMarker,
  CrosshairMode,
  PriceScaleMode,
  LineStyle,
  ColorType,
  UTCTimestamp
} from "lightweight-charts"

// Type definitions for our component props
interface SeriesConfig {
  type: 'Area' | 'Baseline' | 'Histogram' | 'Line' | 'Bar' | 'Candlestick'
  data: any[]
  options?: any
  name?: string
  priceScale?: any
  markers?: SeriesMarker<Time>[]
}

interface ChartConfig {
  chart: any
  series: SeriesConfig[]
  priceLines?: any[]
  chartId?: string
}

interface SyncConfig {
  enabled: boolean
  crosshair: boolean
  timeRange: boolean
}

interface ComponentConfig {
  charts: ChartConfig[]
  syncConfig: SyncConfig
  callbacks?: string[]
}

// Chart instance manager
class ChartManager {
  private chart: IChartApi
  private series: Map<string, ISeriesApi<SeriesType>> = new Map()
  private chartId: string
  private isUpdating: boolean = false

  constructor(chart: IChartApi, chartId: string) {
    this.chart = chart
    this.chartId = chartId
  }

  getChart(): IChartApi {
    return this.chart
  }

  getChartId(): string {
    return this.chartId
  }

  addSeries(config: SeriesConfig): ISeriesApi<SeriesType> | null {
    let series: ISeriesApi<SeriesType> | null = null
    
    switch(config.type) {
      case 'Area':
        series = this.chart.addAreaSeries(config.options || {})
        break
      case 'Bar':
        series = this.chart.addBarSeries(config.options || {})
        break
      case 'Baseline':
        series = this.chart.addBaselineSeries(config.options || {})
        break
      case 'Candlestick':
        series = this.chart.addCandlestickSeries(config.options || {})
        break
      case 'Histogram':
        series = this.chart.addHistogramSeries(config.options || {})
        break
      case 'Line':
        series = this.chart.addLineSeries(config.options || {})
        break
      default:
        console.warn(`Unknown series type: ${config.type}`)
        return null
    }

    if (series && config.name) {
      this.series.set(config.name, series)
    }

    // Apply price scale options if specified
    if (series && config.priceScale && config.options?.priceScaleId !== undefined) {
      this.chart.priceScale(config.options.priceScaleId).applyOptions(config.priceScale)
    }

    // Set data
    if (series && config.data) {
      series.setData(config.data)
    }

    // Add markers if specified
    if (series && config.markers) {
      series.setMarkers(config.markers)
    }

    return series
  }

  setUpdating(updating: boolean) {
    this.isUpdating = updating
  }

  isCurrentlyUpdating(): boolean {
    return this.isUpdating
  }

  updateSeries(name: string, data: any[]) {
    const series = this.series.get(name)
    if (series) {
      series.setData(data)
    }
  }

  addPriceLines(priceLines: any[]) {
    priceLines.forEach(priceLine => {
      // Get the first series to add price line to
      const firstSeries = Array.from(this.series.values())[0]
      if (firstSeries && 'createPriceLine' in firstSeries) {
        firstSeries.createPriceLine(priceLine)
      }
    })
  }

  fitContent() {
    this.chart.timeScale().fitContent()
  }

  destroy() {
    this.chart.remove()
  }
}

const LightweightChartsEnhanced: React.FC = () => {
  const renderData = useRenderData()
  const config = renderData.args["config"] as ComponentConfig
  
  const containerRef = useRef<HTMLDivElement>(null)
  const chartManagersRef = useRef<ChartManager[]>([])
  const [isInitialized, setIsInitialized] = useState(false)
  
  // Synchronization state
  const syncStateRef = useRef({
    isInternalUpdate: false,
    lastCrosshairTime: null as Time | null,
    lastVisibleRange: null as TimeRange | null
  })

  // Handle chart synchronization
  const setupSynchronization = useCallback((managers: ChartManager[]) => {
    if (!config.syncConfig.enabled || managers.length <= 1) return

    managers.forEach((manager, index) => {
      const chart = manager.getChart()
      
      // Sync time range
      if (config.syncConfig.timeRange) {
        chart.timeScale().subscribeVisibleTimeRangeChange((timeRange: TimeRange | null) => {
          if (syncStateRef.current.isInternalUpdate || !timeRange) return
          
          syncStateRef.current.isInternalUpdate = true
          syncStateRef.current.lastVisibleRange = timeRange
          
          managers.forEach((otherManager, otherIndex) => {
            if (index !== otherIndex && !otherManager.isCurrentlyUpdating()) {
              otherManager.setUpdating(true)
              const otherChart = otherManager.getChart()
              otherChart.timeScale().setVisibleRange(timeRange)
              otherManager.setUpdating(false)
            }
          })
          
          syncStateRef.current.isInternalUpdate = false

          // Send callback to Python if registered
          if (config.callbacks?.includes('onVisibleTimeRangeChange')) {
            renderData.setComponentValue({
              onVisibleTimeRangeChange: {
                chartId: manager.getChartId(),
                timeRange
              }
            })
          }
        })

        chart.timeScale().subscribeVisibleLogicalRangeChange((range: LogicalRange | null) => {
          if (syncStateRef.current.isInternalUpdate || !range) return
          
          syncStateRef.current.isInternalUpdate = true
          
          managers.forEach((otherManager, otherIndex) => {
            if (index !== otherIndex && !otherManager.isCurrentlyUpdating()) {
              otherManager.setUpdating(true)
              const otherChart = otherManager.getChart()
              otherChart.timeScale().setVisibleLogicalRange(range)
              otherManager.setUpdating(false)
            }
          })
          
          syncStateRef.current.isInternalUpdate = false
        })
      }

      // Sync crosshair
      if (config.syncConfig.crosshair) {
        chart.subscribeCrosshairMove((param: MouseEventParams) => {
          if (syncStateRef.current.isInternalUpdate) return
          
          syncStateRef.current.isInternalUpdate = true
          
          managers.forEach((otherManager, otherIndex) => {
            if (index !== otherIndex) {
              const otherChart = otherManager.getChart()
              
              if (param.time) {
                // Use setCrossHairXY to sync crosshair position
                const coordinate = otherChart.timeScale().timeToCoordinate(param.time)
                if (coordinate !== null) {
                  // We need to get the y-coordinate from the first series
                  const point = param.point || { x: coordinate, y: 0 }
                  otherChart.setCrossHairXY(coordinate, point.y, false)
                }
              } else {
                // Clear crosshair
                otherChart.clearCrossHair()
              }
            }
          })
          
          syncStateRef.current.isInternalUpdate = false

          // Send callback to Python if registered
          if (config.callbacks?.includes('onCrosshairMove')) {
            renderData.setComponentValue({
              onCrosshairMove: {
                chartId: manager.getChartId(),
                time: param.time,
                point: param.point,
                seriesPrices: param.seriesPrices
              }
            })
          }
        })
      }

      // Handle click events
      if (config.callbacks?.includes('onClick')) {
        chart.subscribeClick((param: MouseEventParams) => {
          renderData.setComponentValue({
            onClick: {
              chartId: manager.getChartId(),
              time: param.time,
              point: param.point,
              seriesPrices: param.seriesPrices
            }
          })
        })
      }
    })
  }, [config, renderData])

  // Initialize charts
  useEffect(() => {
    if (!containerRef.current || isInitialized) return

    // Clear existing charts
    chartManagersRef.current.forEach(manager => manager.destroy())
    chartManagersRef.current = []

    // Create container divs for each chart
    containerRef.current.innerHTML = ''
    
    const managers: ChartManager[] = []
    
    config.charts.forEach((chartConfig, index) => {
      const chartDiv = document.createElement('div')
      chartDiv.id = `chart-${index}`
      chartDiv.style.position = 'relative'
      containerRef.current!.appendChild(chartDiv)
      
      // Create chart with options
      const chartOptions = {
        width: chartDiv.clientWidth,
        height: 400,
        ...chartConfig.chart,
        layout: {
          textColor: 'black',
          background: { type: ColorType.Solid, color: 'white' },
          ...chartConfig.chart?.layout
        }
      }
      
      const chart = createChart(chartDiv, chartOptions)
      const manager = new ChartManager(chart, chartConfig.chartId || `chart_${index}`)
      
      // Add all series
      chartConfig.series.forEach(seriesConfig => {
        manager.addSeries(seriesConfig)
      })
      
      // Add price lines if specified
      if (chartConfig.priceLines) {
        manager.addPriceLines(chartConfig.priceLines)
      }
      
      // Fit content
      manager.fitContent()
      
      managers.push(manager)
    })
    
    chartManagersRef.current = managers
    
    // Setup synchronization
    setupSynchronization(managers)
    
    setIsInitialized(true)

    // Handle resize
    const handleResize = () => {
      managers.forEach((manager, index) => {
        const chartDiv = document.getElementById(`chart-${index}`)
        if (chartDiv) {
          manager.getChart().applyOptions({ 
            width: chartDiv.clientWidth 
          })
        }
      })
    }
    
    window.addEventListener('resize', handleResize)
    
    return () => {
      window.removeEventListener('resize', handleResize)
      managers.forEach(manager => manager.destroy())
    }
  }, [config, setupSynchronization, isInitialized])

  // Handle dynamic updates
  useEffect(() => {
    if (!isInitialized) return
    
    // Check for updates in session state or other mechanisms
    // This is where we would handle dynamic data updates
    // For now, we'll rely on key changes to trigger re-renders
    
  }, [renderData.args, isInitialized])

  return (
    <div 
      ref={containerRef} 
      style={{ 
        width: '100%',
        display: 'flex',
        flexDirection: 'column',
        gap: '4px'
      }}
    />
  )
}

export default LightweightChartsEnhanced
