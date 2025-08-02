import { 
  UTCTimestamp, 
  SeriesMarker, 
  Time, 
  ISeriesPrimitive,
  IPrimitivePaneView,
  IPrimitivePaneRenderer,
  SeriesAttachedParameter,
  IChartApi,
  ISeriesApi,
  Coordinate
} from 'lightweight-charts'
import { TradeConfig, TradeVisualizationOptions } from './types'

// Trade rectangle data interface
interface TradeRectangleData {
  time1: UTCTimestamp
  time2: UTCTimestamp
  price1: number
  price2: number
  fillColor: string
  borderColor: string
  borderWidth: number
  borderStyle: 'solid' | 'dashed' | 'dotted'
  opacity: number
  priceScaleId?: string
}

// Trade rectangle renderer data interface
interface TradeRectangleRendererData {
  x1: Coordinate | null
  y1: Coordinate | null
  x2: Coordinate | null
  y2: Coordinate | null
  fillColor: string
  borderColor: string
  borderWidth: number
  borderStyle: string
  opacity: number
}

// Trade rectangle view data interface
interface TradeRectangleViewData {
  data: TradeRectangleRendererData[]
}

// Trade rectangle primitive pane renderer
class TradeRectanglePaneRenderer implements IPrimitivePaneRenderer {
  _viewData: TradeRectangleViewData

  constructor(data: TradeRectangleViewData) {
    this._viewData = data
  }

  draw(target: any) {
    const rectangles = this._viewData.data
    if (rectangles.length === 0) return

    target.useBitmapCoordinateSpace((scope: any) => {
      const ctx = scope.context
      ctx.scale(scope.horizontalPixelRatio, scope.verticalPixelRatio)

      rectangles.forEach(rect => {
        if (
          rect.x1 === null || rect.y1 === null ||
          rect.x2 === null || rect.y2 === null
        ) {
          return
        }

        // Calculate rectangle dimensions
        const x = Math.min(rect.x1, rect.x2)
        const y = Math.min(rect.y1, rect.y2)
        const width = Math.abs(rect.x2 - rect.x1)
        const height = Math.abs(rect.y2 - rect.y1)

        // Validate dimensions
        if (width <= 0 || height <= 0) {
          return
        }

        // Draw fill
        ctx.save()
        ctx.fillStyle = rect.fillColor
        ctx.globalAlpha = rect.opacity
        ctx.fillRect(x, y, width, height)

        // Draw border
        if (rect.borderWidth > 0) {
          ctx.strokeStyle = rect.borderColor
          ctx.lineWidth = rect.borderWidth
          ctx.globalAlpha = 1.0
          
          // Set line style
          if (rect.borderStyle === 'dashed') {
            ctx.setLineDash([5, 5])
          } else if (rect.borderStyle === 'dotted') {
            ctx.setLineDash([2, 2])
          } else {
            ctx.setLineDash([])
          }
          
          ctx.strokeRect(x, y, width, height)
        }
        ctx.restore()
      })
    })
  }
}

// Trade rectangle primitive pane view
class TradeRectanglePaneView implements IPrimitivePaneView {
  _source: TradeRectanglePlugin
  _data: TradeRectangleViewData

  constructor(source: TradeRectanglePlugin) {
    this._source = source
    this._data = {
      data: []
    }
  }

  update() {
    const timeScale = this._source.getChart().timeScale()
    const series = this._source.getSeries()
    
    console.log(`🔍 [TradeRectanglePaneView] Updating ${this._source.getRectangles().length} rectangles`);
    console.log(`🔍 [TradeRectanglePaneView] Time scale:`, timeScale);
    console.log(`🔍 [TradeRectanglePaneView] Series:`, series);
    
    // Get visible range for debugging
    const visibleRange = timeScale.getVisibleRange()
    console.log(`🔍 [TradeRectanglePaneView] Visible range:`, visibleRange);
    
    this._data.data = this._source.getRectangles().map((rect, index) => {
      // Convert timestamps to coordinates
      const x1 = timeScale.timeToCoordinate(rect.time1) ?? null;
      const y1 = series.priceToCoordinate(rect.price1) ?? null;
      const x2 = timeScale.timeToCoordinate(rect.time2) ?? null;
      const y2 = series.priceToCoordinate(rect.price2) ?? null;
      
      // Validate coordinates
      const validCoordinates = x1 !== null && y1 !== null && x2 !== null && y2 !== null;
      const positiveCoordinates = validCoordinates && x1 >= 0 && x2 >= 0 && y1 >= 0 && y2 >= 0;
      
      console.log(`🔍 [TradeRectanglePaneView] Rectangle ${index} coordinates:`, {
        time1: rect.time1, time2: rect.time2,
        price1: rect.price1, price2: rect.price2,
        x1, y1, x2, y2,
        validCoordinates,
        positiveCoordinates,
        timeScaleVisibleRange: visibleRange,
        priceScaleVisibleRange: series.priceScale()?.getVisibleRange(),
        // Add more debugging info
        time1Date: new Date(rect.time1 * 1000).toISOString(),
        time2Date: new Date(rect.time2 * 1000).toISOString(),
        chartWidth: this._source.getChart().chartElement().clientWidth
      });
      
      // Only return valid coordinates
      if (!validCoordinates || !positiveCoordinates) {
        console.warn(`⚠️ [TradeRectanglePaneView] Invalid coordinates for rectangle ${index}, skipping`);
        return {
          x1: null, y1: null, x2: null, y2: null,
          fillColor: rect.fillColor,
          borderColor: rect.borderColor,
          borderWidth: rect.borderWidth,
          borderStyle: rect.borderStyle,
          opacity: rect.opacity
        }
      }
      
      return {
        x1, y1, x2, y2,
        fillColor: rect.fillColor,
        borderColor: rect.borderColor,
        borderWidth: rect.borderWidth,
        borderStyle: rect.borderStyle,
        opacity: rect.opacity
      }
    })
  }

  renderer() {
    return new TradeRectanglePaneRenderer(this._data)
  }
}

// Trade rectangle plugin class
export class TradeRectanglePlugin implements ISeriesPrimitive<Time> {
  private chart: IChartApi
  private series: ISeriesApi<any>
  private rectangles: TradeRectangleData[] = []
  private _paneViews: TradeRectanglePaneView[]

  constructor(chart: IChartApi, series: ISeriesApi<any>) {
    this.chart = chart
    this.series = series
    this._paneViews = [new TradeRectanglePaneView(this)]
    
    // Attach the primitive to the series for rendering
    this.series.attachPrimitive(this)
  }

  // Getter methods
  getChart(): IChartApi {
    return this.chart
  }

  getSeries(): ISeriesApi<any> {
    return this.series
  }

  getRectangles(): TradeRectangleData[] {
    return this.rectangles
  }

  // ISeriesPrimitive implementation
  attached(param: SeriesAttachedParameter<Time>): void {
    // Primitive is attached to the series
  }

  detached(): void {
    // Primitive is detached from the series
  }

  updateAllViews(): void {
    this._paneViews.forEach(pv => pv.update())
  }

  paneViews(): IPrimitivePaneView[] {
    return this._paneViews
  }

  // Trade rectangle management
  addRectangle(rect: TradeRectangleData): void {
    this.rectangles.push(rect)
    this.updateAllViews()
  }

  setRectangles(rects: TradeRectangleData[]): void {
    this.rectangles = rects
    this.updateAllViews()
  }

  clearRectangles(): void {
    this.rectangles = []
    this.updateAllViews()
  }

  removeRectangle(index: number): void {
    this.rectangles.splice(index, 1)
    this.updateAllViews()
  }

  destroy(): void {
    this.series.detachPrimitive(this)
  }
}

// Create trade rectangles from trade data
function createTradeRectangles(trades: TradeConfig[], options: TradeVisualizationOptions, chartData?: any[]): TradeRectangleData[] {
  const rectangles: TradeRectangleData[] = []

  console.log(`🔍 [createTradeRectangles] Creating rectangles for ${trades.length} trades`);
  console.log(`🔍 [createTradeRectangles] Options style:`, options.style);
  console.log(`🔍 [createTradeRectangles] Chart data length:`, chartData?.length);

  trades.forEach((trade, index) => {
    console.log(`🔍 [createTradeRectangles] Processing trade ${index}:`, trade);
    
    // Validate trade data
    if (!trade.entryTime || !trade.exitTime || 
        typeof trade.entryPrice !== 'number' || typeof trade.exitPrice !== 'number') {
      console.warn(`❌ [createTradeRectangles] Invalid trade data for trade ${index}:`, trade);
      return
    }

    // Parse times and validate
    const time1 = parseTime(trade.entryTime)
    const time2 = parseTime(trade.exitTime)
    
    console.log(`🔍 [createTradeRectangles] Parsed times for trade ${index}:`, { time1, time2 });
    
    if (time1 === null || time2 === null || time1 === time2) {
      console.warn(`❌ [createTradeRectangles] Invalid times for trade ${index}:`, { time1, time2 });
      return
    }

    // Find nearest available times in chart data if provided
    let adjustedTime1 = time1
    let adjustedTime2 = time2
    
    if (chartData && chartData.length > 0) {
      const nearestTime1 = findNearestTime(time1, chartData)
      const nearestTime2 = findNearestTime(time2, chartData)
      
      if (nearestTime1) adjustedTime1 = nearestTime1
      if (nearestTime2) adjustedTime2 = nearestTime2
    }

    // Validate prices
    if (trade.entryPrice <= 0 || trade.exitPrice <= 0) {
      return
    }

    const color = trade.isProfitable 
      ? (options.rectangleColorProfit || '#4CAF50')
      : (options.rectangleColorLoss || '#F44336')

    const opacity = options.rectangleFillOpacity || 0.2

    rectangles.push({
      time1: Math.min(adjustedTime1, adjustedTime2) as UTCTimestamp,
      price1: Math.min(trade.entryPrice, trade.exitPrice),
      time2: Math.max(adjustedTime1, adjustedTime2) as UTCTimestamp,
      price2: Math.max(trade.entryPrice, trade.exitPrice),
      fillColor: color,
      borderColor: color,
      borderWidth: options.rectangleBorderWidth || 1,
      borderStyle: 'solid',
      opacity: opacity
    })
  })

  return rectangles
}

// Create trade markers
function createTradeMarkers(trades: TradeConfig[], options: TradeVisualizationOptions, chartData?: any[]): SeriesMarker<Time>[] {
  const markers: SeriesMarker<Time>[] = []

  trades.forEach((trade, index) => {
    // Validate trade data
    if (!trade.entryTime || !trade.exitTime || 
        typeof trade.entryPrice !== 'number' || typeof trade.exitPrice !== 'number') {
      console.warn(`Invalid trade data for trade ${index}:`, trade)
      return
    }

    // Parse times and validate
    const entryTime = parseTime(trade.entryTime)
    const exitTime = parseTime(trade.exitTime)
    
    if (!entryTime || !exitTime) {
      console.warn(`Invalid trade data for trade ${index}:`, trade)
      return
    }

    // Find nearest available times in chart data if provided
    let adjustedEntryTime = entryTime
    let adjustedExitTime = exitTime
    
    if (chartData && chartData.length > 0) {
      const nearestEntryTime = findNearestTime(entryTime, chartData)
      const nearestExitTime = findNearestTime(exitTime, chartData)
      
      if (nearestEntryTime) adjustedEntryTime = nearestEntryTime
      if (nearestExitTime) adjustedExitTime = nearestExitTime
      
    }

    // Entry marker
    const entryColor = trade.tradeType === 'long' 
      ? (options.entryMarkerColorLong || '#2196F3')
      : (options.entryMarkerColorShort || '#FF9800')

    const entryMarker: SeriesMarker<Time> = {
      time: adjustedEntryTime,
      position: trade.tradeType === 'long' ? 'belowBar' : 'aboveBar',
      color: entryColor,
      shape: trade.tradeType === 'long' ? 'arrowUp' : 'arrowDown',
      text: options.showPnlInMarkers && trade.text ? trade.text : `Entry: $${trade.entryPrice.toFixed(2)}`
    }
    markers.push(entryMarker)

    // Exit marker
    const exitColor = trade.isProfitable 
      ? (options.exitMarkerColorProfit || '#4CAF50')
      : (options.exitMarkerColorLoss || '#F44336')

    const exitMarker: SeriesMarker<Time> = {
      time: adjustedExitTime,
      position: trade.tradeType === 'long' ? 'aboveBar' : 'belowBar',
      color: exitColor,
      shape: trade.tradeType === 'long' ? 'arrowDown' : 'arrowUp',
      text: options.showPnlInMarkers && trade.text ? trade.text : `Exit: $${trade.exitPrice.toFixed(2)}`
    }
    markers.push(exitMarker)
  })

  return markers
}

// Find nearest available time in chart data
function findNearestTime(targetTime: UTCTimestamp, chartData: any[]): UTCTimestamp | null {
  if (!chartData || chartData.length === 0) {
    return null
  }

  // Convert chart data times to timestamps for comparison
  const availableTimes = chartData.map(item => {
    if (typeof item.time === 'number') {
      return item.time
    } else if (typeof item.time === 'string') {
      return Math.floor(new Date(item.time).getTime() / 1000) as UTCTimestamp
    }
    return null
  }).filter(time => time !== null) as UTCTimestamp[]

  if (availableTimes.length === 0) {
    return null
  }

  // Find the nearest time
  let nearestTime = availableTimes[0]
  let minDiff = Math.abs(targetTime - nearestTime)

  for (const time of availableTimes) {
    const diff = Math.abs(targetTime - time)
    if (diff < minDiff) {
      minDiff = diff
      nearestTime = time
    }
  }

  return nearestTime
}

// Parse time string to UTC timestamp
function parseTime(timeStr: string | number): UTCTimestamp | null {
  try {
    // If it's already a number (Unix timestamp), convert to seconds if needed
    if (typeof timeStr === 'number') {
      // If timestamp is in milliseconds, convert to seconds
      if (timeStr > 1000000000000) {
        return Math.floor(timeStr / 1000) as UTCTimestamp
      }
      return Math.floor(timeStr) as UTCTimestamp
    }
    
    // If it's a string, try to parse as date
    if (typeof timeStr === 'string') {
      // First try to parse as Unix timestamp string
      const timestamp = parseInt(timeStr, 10)
      if (!isNaN(timestamp)) {
        // It's a numeric string (Unix timestamp)
        if (timestamp > 1000000000000) {
          return Math.floor(timestamp / 1000) as UTCTimestamp
        }
        return Math.floor(timestamp) as UTCTimestamp
      }
      
      // Try to parse as date string
      const date = new Date(timeStr)
      if (isNaN(date.getTime())) {
        console.warn(`Failed to parse time: ${timeStr}`)
        return null
      }
      return Math.floor(date.getTime() / 1000) as UTCTimestamp
    }
    
    return null
  } catch (error) {
    console.error(`Error parsing time ${timeStr}:`, error)
    return null
  }
}

// Main function to create trade visual elements
export function createTradeVisualElements(
  trades: TradeConfig[], 
  options: TradeVisualizationOptions, 
  chartData?: any[],
  priceScaleId?: string
): {
  markers: SeriesMarker<Time>[]
  rectangles: TradeRectangleData[]
  annotations: any[]
} {
  const markers: SeriesMarker<Time>[] = []
  const rectangles: TradeRectangleData[] = []
  const annotations: any[] = []

  if (!trades || trades.length === 0) {
    return { markers, rectangles, annotations }
  }

  // Create markers if enabled
  if (options.style === 'markers' || options.style === 'both') {
    markers.push(...createTradeMarkers(trades, options, chartData))
  }

  // Create rectangles if enabled
  console.log(`🔍 [createTradeVisualElements] Style check: options.style=${options.style}, should create rectangles: ${options.style === 'rectangles' || options.style === 'both'}`);
  if (options.style === 'rectangles' || options.style === 'both') {
    const newRectangles = createTradeRectangles(trades, options, chartData)
    console.log(`🔍 [createTradeVisualElements] Created ${newRectangles.length} rectangles`);
    rectangles.push(...newRectangles)
  }

  // Create annotations if enabled
  if (options.showAnnotations) {
    trades.forEach(trade => {
      const textParts: string[] = []

      if (options.showTradeId && trade.id) {
        textParts.push(`#${trade.id}`)
      }

      if (options.showTradeType) {
        textParts.push(trade.tradeType.toUpperCase())
      }

      if (options.showQuantity) {
        textParts.push(`Qty: ${trade.quantity}`)
      }

      if (trade.pnlPercentage !== undefined) {
        textParts.push(`P&L: ${trade.pnlPercentage.toFixed(1)}%`)
      }

      // Calculate midpoint for annotation position
      const entryTime = parseTime(trade.entryTime)
      const exitTime = parseTime(trade.exitTime)
      
      if (entryTime === null || exitTime === null) {
        return
      }
      
      const midTime = (entryTime + exitTime) / 2
      const midPrice = (trade.entryPrice + trade.exitPrice) / 2

      annotations.push({
        type: 'text',
        time: midTime,
        price: midPrice,
        text: textParts.join(' | '),
        fontSize: options.annotationFontSize || 12,
        backgroundColor: options.annotationBackground || 'rgba(255, 255, 255, 0.8)',
        color: '#000000',
        padding: 4
      })
    })
  }

  return { markers, rectangles, annotations }
} 