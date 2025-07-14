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
interface RangeConfig {
  label: string
  seconds: number | null
}

interface RangeSwitcherConfig {
  ranges: RangeConfig[]
  position: string
  visible: boolean
  defaultRange?: string
}

interface SeriesConfig {
  type: 'Area' | 'Baseline' | 'Histogram' | 'Line' | 'Bar' | 'Candlestick'
  data: any[]
  options?: any
  name?: string
  priceScale?: any
  markers?: SeriesMarker<Time>[]
}

interface TradeConfig {
  type: string
  entryTime: string
  entryPrice: number
  exitTime?: string
  exitPrice?: number
  quantity?: number
  symbol?: string
  showMarkers: boolean
  showRectangle: boolean
  markerColor: string
  rectangleColor: string
}

interface ChartConfig {
  chart: any
  series: SeriesConfig[]
  priceLines?: any[]
  trades?: TradeConfig[]
  chartId?: string
  rangeSwitcher?: RangeSwitcherConfig
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
  private rangeSwitcherElement: HTMLDivElement | null = null

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

  addRangeSwitcher(config: RangeSwitcherConfig, onRangeChange?: (range: RangeConfig) => void) {
    if (!config.visible) return
    
    // Create range switcher container
    this.rangeSwitcherElement = document.createElement('div')
    this.rangeSwitcherElement.className = 'range-switcher'
    this.rangeSwitcherElement.style.cssText = `
      position: absolute;
      ${config.position.includes('top') ? 'top: 10px;' : 'bottom: 10px;'}
      ${config.position.includes('right') ? 'right: 10px;' : 'left: 10px;'}
      display: flex;
      gap: 4px;
      z-index: 1000;
      background: rgba(255, 255, 255, 0.9);
      border-radius: 4px;
      padding: 4px;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    `
    
    // Add range buttons
    config.ranges.forEach((range, index) => {
      const button = document.createElement('button')
      button.textContent = range.label
      button.style.cssText = `
        border: none;
        background: ${range.label === config.defaultRange ? '#2962FF' : 'transparent'};
        color: ${range.label === config.defaultRange ? 'white' : '#333'};
        padding: 4px 8px;
        border-radius: 3px;
        cursor: pointer;
        font-size: 12px;
        font-weight: 500;
        transition: all 0.2s;
      `
      
      button.addEventListener('click', () => {
        // Update button styles
        this.rangeSwitcherElement?.querySelectorAll('button').forEach(btn => {
          btn.style.background = 'transparent'
          btn.style.color = '#333'
        })
        button.style.background = '#2962FF'
        button.style.color = 'white'
        
        // Apply time range
        if (range.seconds !== null) {
          const now = Math.floor(Date.now() / 1000)
          const from = now - range.seconds
          this.chart.timeScale().setVisibleRange({
            from: from as UTCTimestamp,
            to: now as UTCTimestamp
          })
        } else {
          // "ALL" range - fit content
          this.chart.timeScale().fitContent()
        }
        
        // Call callback
        if (onRangeChange) {
          onRangeChange(range)
        }
      })
      
      this.rangeSwitcherElement.appendChild(button)
    })
    
    // Add to chart container
    const chartContainer = this.chart.chartElement()
    if (chartContainer) {
      chartContainer.style.position = 'relative'
      chartContainer.appendChild(this.rangeSwitcherElement)
    }
  }

  addTrades(trades: TradeConfig[], onTradeClick?: (trade: TradeConfig) => void) {
    trades.forEach((trade, index) => {
      // Add entry marker
      if (trade.showMarkers) {
        const entryMarker = {
          time: trade.entryTime as Time,
          position: trade.type === 'buy' || trade.type === 'long' ? 'belowBar' : 'aboveBar',
          color: trade.markerColor,
          shape: trade.type === 'buy' || trade.type === 'long' ? 'arrowUp' : 'arrowDown',
          text: `${trade.type.toUpperCase()} ${trade.quantity || ''}`,
          size: 2
        }
        
        // Add to first series
        const firstSeries = Array.from(this.series.values())[0]
        if (firstSeries) {
          const currentMarkers = firstSeries.markers() || []
          firstSeries.setMarkers([...currentMarkers, entryMarker])
        }
        
        // Add exit marker if trade is closed
        if (trade.exitTime && trade.exitPrice) {
          const exitMarker = {
            time: trade.exitTime as Time,
            position: trade.type === 'buy' || trade.type === 'long' ? 'aboveBar' : 'belowBar',
            color: trade.markerColor,
            shape: trade.type === 'buy' || trade.type === 'long' ? 'arrowDown' : 'arrowUp',
            text: `EXIT ${trade.quantity || ''}`,
            size: 2
          }
          
          if (firstSeries) {
            const currentMarkers = firstSeries.markers() || []
            firstSeries.setMarkers([...currentMarkers, exitMarker])
          }
        }
      }
      
      // Add rectangle overlay for trade duration
      if (trade.showRectangle && trade.exitTime) {
        // Create rectangle using price lines and time range
        const startTime = trade.entryTime as Time
        const endTime = trade.exitTime as Time
        
        // Add horizontal lines at entry and exit prices
        const entryLine = firstSeries?.createPriceLine({
          price: trade.entryPrice,
          color: trade.rectangleColor,
          lineWidth: 1,
          lineStyle: 2, // Dashed
          axisLabelVisible: true,
          title: `Entry: ${trade.entryPrice}`
        })
        
        if (trade.exitPrice) {
          const exitLine = firstSeries?.createPriceLine({
            price: trade.exitPrice,
            color: trade.rectangleColor,
            lineWidth: 1,
            lineStyle: 2, // Dashed
            axisLabelVisible: true,
            title: `Exit: ${trade.exitPrice}`
          })
        }
      }
    })
  }

  destroy() {
    if (this.rangeSwitcherElement) {
      this.rangeSwitcherElement.remove()
    }
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
       
       // Add trades if specified
       if (chartConfig.trades) {
         manager.addTrades(chartConfig.trades, (trade) => {
           // Send callback to Python if registered
           if (config.callbacks?.includes('onTradeClick')) {
             renderData.setComponentValue({
               onTradeClick: {
                 chartId: manager.getChartId(),
                 trade: trade
               }
             })
           }
         })
       }
       
       // Add range switcher if specified
       if (chartConfig.rangeSwitcher) {
         manager.addRangeSwitcher(chartConfig.rangeSwitcher, (range) => {
           // Send callback to Python if registered
           if (config.callbacks?.includes('onRangeSwitcherChange')) {
             renderData.setComponentValue({
               onRangeSwitcherChange: {
                 chartId: manager.getChartId(),
                 range: range
               }
             })
           }
         })
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
