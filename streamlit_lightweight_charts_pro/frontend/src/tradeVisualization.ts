import { TradeConfig, TradeVisualizationOptions } from './types'
import { SeriesMarker, Time, UTCTimestamp } from 'lightweight-charts'
import { RectangleConfig } from './rectanglePlugin'

export interface TradeVisualElements {
  markers: SeriesMarker<Time>[]
  rectangles: RectangleConfig[]
  annotations: any[]
}

export const createTradeVisualElements = (
  trades: TradeConfig[],
  options: TradeVisualizationOptions = { style: 'both' },
  chartData?: any[],
  priceScaleId: string = 'right'
): TradeVisualElements => {
  const markers: SeriesMarker<Time>[] = []
  const rectangles: RectangleConfig[] = []
  const annotations: any[] = []

  trades.forEach((trade, index) => {
    try {
      const entryTimeParsed = parseTime(trade.entryTime);
      const exitTimeParsed = trade.exitTime ? parseTime(trade.exitTime) : null;
      if (!entryTimeParsed) return;

      // Create entry marker if style includes markers
      if (options.style === 'markers' || options.style === 'both') {
        const entryMarker: SeriesMarker<Time> = {
          time: entryTimeParsed,
          position: trade.tradeType === 'long' ? 'belowBar' : 'aboveBar',
          color: trade.tradeType === 'long' ? 
            (options.entryMarkerColorLong || '#4CAF50') : 
            (options.entryMarkerColorShort || '#FF9800'),
          shape: 'arrowUp',
          text: `Entry ${trade.tradeType.toUpperCase()}`,
          size: options.markerSize || 1
        }
        markers.push(entryMarker)
      }

      // Create exit marker if style includes markers and exit time exists
      if ((options.style === 'markers' || options.style === 'both') && exitTimeParsed) {
        const isProfit = trade.isProfitable || false;
        const exitMarker: SeriesMarker<Time> = {
          time: exitTimeParsed,
          position: trade.tradeType === 'long' ? 'aboveBar' : 'belowBar',
          color: isProfit ? 
            (options.exitMarkerColorProfit || '#4CAF50') : 
            (options.exitMarkerColorLoss || '#F44336'),
          shape: 'arrowDown',
          text: `Exit ${isProfit ? 'PROFIT' : 'LOSS'}`,
          size: options.markerSize || 1
        }
        markers.push(exitMarker)
      }

      // Create rectangle for trade period if style includes rectangles
      if ((options.style === 'rectangles' || options.style === 'both') && exitTimeParsed) {
        const rectangle: RectangleConfig = {
          time1: entryTimeParsed,
          time2: exitTimeParsed,
          price1: trade.entryPrice,
          price2: trade.exitPrice,
          fillColor: trade.isProfitable ? 
            (options.rectangleColorProfit || '#4CAF50') : 
            (options.rectangleColorLoss || '#F44336'),
          borderColor: trade.isProfitable ? 
            (options.rectangleColorProfit || '#4CAF50') : 
            (options.rectangleColorLoss || '#F44336'),
          borderWidth: options.rectangleBorderWidth || 1,
          borderStyle: 'solid',
          opacity: options.rectangleFillOpacity || 0.2,
          priceScaleId: priceScaleId
        }
        rectangles.push(rectangle)
      }

      // Create annotation for trade details
      const annotation = {
        time: entryTimeParsed,
        price: trade.entryPrice,
        text: `Trade ${index + 1}: ${trade.tradeType.toUpperCase()}\nEntry: ${trade.entryPrice}\nExit: ${trade.exitPrice || 'Open'}`,
        color: '#131722',
        backgroundColor: 'rgba(255, 255, 255, 0.9)',
        fontSize: options.annotationFontSize || 12,
        fontFamily: 'Arial'
      }
      annotations.push(annotation)
    } catch (error) {
      // Silent error handling
    }
  })

  return { markers, rectangles, annotations }
}

function createTradeMarkers(trade: TradeConfig, options: TradeVisualizationOptions): SeriesMarker<Time>[] {
  const markers: SeriesMarker<Time>[] = []

  // Validate trade data
  if (!trade.entryTime || !trade.exitTime || 
      typeof trade.entryPrice !== 'number' || typeof trade.exitPrice !== 'number') {
    return markers
  }

  // Parse times and validate
  const entryTime = parseTime(trade.entryTime)
  const exitTime = parseTime(trade.exitTime)
  
  if (entryTime === null || exitTime === null) {
    return markers
  }

  // Entry marker
  const entryColor = trade.tradeType === 'long' 
    ? (options.entryMarkerColorLong || '#2196F3')
    : (options.entryMarkerColorShort || '#FF9800')

  const entryMarker: SeriesMarker<Time> = {
    time: entryTime,
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
    time: exitTime,
    position: trade.tradeType === 'long' ? 'aboveBar' : 'belowBar',
    color: exitColor,
    shape: trade.tradeType === 'long' ? 'arrowDown' : 'arrowUp',
    text: options.showPnlInMarkers && trade.text ? trade.text : `Exit: $${trade.exitPrice.toFixed(2)}`
  }
  markers.push(exitMarker)

  return markers
}

function createTradeRectangle(trade: TradeConfig, options: TradeVisualizationOptions, priceScaleId?: string): RectangleConfig | null {
  // Validate trade data
  if (!trade.entryTime || !trade.exitTime || 
      typeof trade.entryPrice !== 'number' || typeof trade.exitPrice !== 'number') {
    return null
  }

  // Parse times and validate
  const time1 = parseTime(trade.entryTime)
  const time2 = parseTime(trade.exitTime)
  
  if (time1 === null || time2 === null || time1 === time2) {
    return null
  }

  // Validate prices
  if (trade.entryPrice <= 0 || trade.exitPrice <= 0) {
    return null
  }

  const color = trade.isProfitable 
    ? (options.rectangleColorProfit || '#4CAF50')
    : (options.rectangleColorLoss || '#F44336')

  const opacity = options.rectangleFillOpacity || 0.2

  return {
    time1: Math.min(time1, time2) as UTCTimestamp,
    price1: Math.min(trade.entryPrice, trade.exitPrice),
    time2: Math.max(time1, time2) as UTCTimestamp,
    price2: Math.max(trade.entryPrice, trade.exitPrice),
    fillColor: color,
    borderColor: color,
    borderWidth: options.rectangleBorderWidth || 1,
    borderStyle: 'solid',
    opacity: opacity,
    priceScaleId: priceScaleId
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
  const entryTime = parseTime(trade.entryTime)
  const exitTime = parseTime(trade.exitTime)
  
  if (entryTime === null || exitTime === null) {
    return null
  }
  
  const midTime = (entryTime + exitTime) / 2
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

function parseTime(timeStr: string): UTCTimestamp | null {
  try {
    // Convert string time to UTC timestamp
    const date = new Date(timeStr)
    if (isNaN(date.getTime())) {
      return null
    }
    return Math.floor(date.getTime() / 1000) as UTCTimestamp
  } catch (error) {
    return null
  }
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