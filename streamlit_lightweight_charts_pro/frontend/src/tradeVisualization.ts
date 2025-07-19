import { TradeConfig, TradeVisualizationOptions } from './types'
import { SeriesMarker, Time, UTCTimestamp } from 'lightweight-charts'

export interface TradeVisualElements {
  markers: SeriesMarker<Time>[]
  shapes: any[]
  annotations: any[]
}

export function createTradeVisualElements(
  trades: TradeConfig[],
  options: TradeVisualizationOptions,
  chartData?: any[]
): TradeVisualElements {
  const result: TradeVisualElements = {
    markers: [],
    shapes: [],
    annotations: []
  }

  for (const trade of trades) {
    if (options.style === 'markers' || options.style === 'both') {
      const markers = createTradeMarkers(trade, options)
      result.markers.push(...markers)
    }

    if (options.style === 'rectangles' || options.style === 'both') {
      const rectangle = createTradeRectangle(trade, options)
      result.shapes.push(rectangle)
    }

    if (options.style === 'lines') {
      const line = createTradeLine(trade, options)
      result.shapes.push(line)
    }

    if (options.style === 'arrows') {
      const arrow = createTradeArrow(trade, options)
      result.shapes.push(arrow)
    }

    if (options.style === 'zones') {
      const zone = createTradeZone(trade, options, chartData)
      result.shapes.push(zone)
    }

    // Add trade annotation if enabled
    if (options.showTradeId || options.showQuantity || options.showTradeType) {
      const annotation = createTradeAnnotation(trade, options)
      result.annotations.push(annotation)
    }
  }

  return result
}

function createTradeMarkers(trade: TradeConfig, options: TradeVisualizationOptions): SeriesMarker<Time>[] {
  const markers: SeriesMarker<Time>[] = []

  // Entry marker
  const entryColor = trade.tradeType === 'long' 
    ? (options.entryMarkerColorLong || '#2196F3')
    : (options.entryMarkerColorShort || '#FF9800')

  const entryMarker: SeriesMarker<Time> = {
    time: parseTime(trade.entryTime),
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
    time: parseTime(trade.exitTime),
    position: trade.tradeType === 'long' ? 'aboveBar' : 'belowBar',
    color: exitColor,
    shape: trade.tradeType === 'long' ? 'arrowDown' : 'arrowUp',
    text: options.showPnlInMarkers && trade.text ? trade.text : `Exit: $${trade.exitPrice.toFixed(2)}`
  }
  markers.push(exitMarker)

  return markers
}

function createTradeRectangle(trade: TradeConfig, options: TradeVisualizationOptions): any {
  const color = trade.isProfitable 
    ? (options.rectangleColorProfit || '#4CAF50')
    : (options.rectangleColorLoss || '#F44336')

  const opacity = options.rectangleFillOpacity || 0.2
  const fillColor = `${color}${Math.floor(opacity * 255).toString(16).padStart(2, '0')}`

  return {
    type: 'rectangle',
    time1: parseTime(trade.entryTime),
    price1: trade.entryPrice,
    time2: parseTime(trade.exitTime),
    price2: trade.exitPrice,
    fillColor: fillColor,
    borderColor: color,
    borderWidth: options.rectangleBorderWidth || 1,
    borderStyle: 'solid'
  }
}

function createTradeLine(trade: TradeConfig, options: TradeVisualizationOptions): any {
  const color = trade.isProfitable 
    ? (options.lineColorProfit || '#4CAF50')
    : (options.lineColorLoss || '#F44336')

  return {
    type: 'trendLine',
    time1: parseTime(trade.entryTime),
    price1: trade.entryPrice,
    time2: parseTime(trade.exitTime),
    price2: trade.exitPrice,
    lineColor: color,
    lineWidth: options.lineWidth || 2,
    lineStyle: getLineStyleValue(options.lineStyle || 'dashed')
  }
}

function createTradeArrow(trade: TradeConfig, options: TradeVisualizationOptions): any {
  const color = trade.isProfitable 
    ? (options.arrowColorProfit || '#4CAF50')
    : (options.arrowColorLoss || '#F44336')

  return {
    type: 'arrow',
    time1: parseTime(trade.entryTime),
    price1: trade.entryPrice,
    time2: parseTime(trade.exitTime),
    price2: trade.exitPrice,
    lineColor: color,
    lineWidth: options.lineWidth || 2,
    arrowSize: options.arrowSize || 10,
    text: trade.pnlPercentage ? `${trade.pnlPercentage.toFixed(1)}%` : ''
  }
}

function createTradeZone(trade: TradeConfig, options: TradeVisualizationOptions, chartData?: any[]): any {
  const color = trade.tradeType === 'long' 
    ? (options.zoneColorLong || '#2196F3')
    : (options.zoneColorShort || '#FF9800')

  const opacity = options.zoneOpacity || 0.1
  const fillColor = `${color}${Math.floor(opacity * 255).toString(16).padStart(2, '0')}`

  let time1 = parseTime(trade.entryTime)
  let time2 = parseTime(trade.exitTime)

  // Extend zone if chart data is available
  if (chartData && options.zoneExtendBars && options.zoneExtendBars > 0) {
    const entryIndex = chartData.findIndex(bar => bar.time >= trade.entryTime)
    const exitIndex = chartData.findIndex(bar => bar.time >= trade.exitTime)

    if (entryIndex >= options.zoneExtendBars) {
      time1 = chartData[entryIndex - options.zoneExtendBars].time
    }
    if (exitIndex + options.zoneExtendBars < chartData.length) {
      time2 = chartData[exitIndex + options.zoneExtendBars].time
    }
  }

  // Calculate zone height
  const topPrice = Math.max(trade.entryPrice, trade.exitPrice) * 1.01
  const bottomPrice = Math.min(trade.entryPrice, trade.exitPrice) * 0.99

  return {
    type: 'rectangle',
    time1: time1,
    price1: bottomPrice,
    time2: time2,
    price2: topPrice,
    fillColor: fillColor,
    borderColor: 'transparent',
    borderWidth: 0
  }
}

function createTradeAnnotation(trade: TradeConfig, options: TradeVisualizationOptions): any {
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
  const midTime = (parseTime(trade.entryTime) + parseTime(trade.exitTime)) / 2
  const midPrice = (trade.entryPrice + trade.exitPrice) / 2

  return {
    type: 'text',
    time: midTime,
    price: midPrice,
    text: textParts.join(' | '),
    fontSize: options.annotationFontSize || 12,
    backgroundColor: options.annotationBackground || 'rgba(255, 255, 255, 0.8)',
    color: '#000000',
    padding: 4
  }
}

function parseTime(timeStr: string): UTCTimestamp {
  // Convert string time to UTC timestamp
  const date = new Date(timeStr)
  return Math.floor(date.getTime() / 1000) as UTCTimestamp
}

function getLineStyleValue(style: string): number {
  const styleMap: { [key: string]: number } = {
    'solid': 0,
    'dotted': 1,
    'dashed': 2,
    'large_dashed': 3,
    'sparse_dotted': 4
  }
  return styleMap[style] || 2 // Default to dashed
} 