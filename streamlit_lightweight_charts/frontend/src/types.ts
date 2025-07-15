import { Time, SeriesMarker } from "lightweight-charts"

// Enhanced Trade Configuration
export interface TradeConfig {
  entryTime: string
  entryPrice: number
  exitTime: string
  exitPrice: number
  quantity: number
  tradeType: 'long' | 'short'
  id?: string
  notes?: string
  text?: string  // Custom tooltip text
  pnl?: number
  pnlPercentage?: number
  isProfitable?: boolean
}

// Trade Visualization Options
export interface TradeVisualizationOptions {
  style: 'markers' | 'rectangles' | 'both' | 'lines' | 'arrows' | 'zones'
  
  // Marker options
  entryMarkerColorLong?: string
  entryMarkerColorShort?: string
  exitMarkerColorProfit?: string
  exitMarkerColorLoss?: string
  markerSize?: number
  showPnlInMarkers?: boolean
  
  // Rectangle options
  rectangleFillOpacity?: number
  rectangleBorderWidth?: number
  rectangleColorProfit?: string
  rectangleColorLoss?: string
  
  // Line options
  lineWidth?: number
  lineStyle?: string
  lineColorProfit?: string
  lineColorLoss?: string
  
  // Arrow options
  arrowSize?: number
  arrowColorProfit?: string
  arrowColorLoss?: string
  
  // Zone options
  zoneOpacity?: number
  zoneColorLong?: string
  zoneColorShort?: string
  zoneExtendBars?: number
  
  // Annotation options
  showTradeId?: boolean
  showQuantity?: boolean
  showTradeType?: boolean
  annotationFontSize?: number
  annotationBackground?: string
}

// Annotation System
export interface Annotation {
  time: string
  price: number
  text: string
  type: 'text' | 'arrow' | 'shape' | 'line' | 'rectangle' | 'circle'
  position: 'above' | 'below' | 'inline'
  color?: string
  backgroundColor?: string
  fontSize?: number
  fontWeight?: string
  textColor?: string
  borderColor?: string
  borderWidth?: number
  opacity?: number
  showTime?: boolean
  tooltip?: string
  lineStyle?: string // <-- added for build fix
}

export interface AnnotationLayer {
  name: string
  annotations: Annotation[]
  visible: boolean
  opacity: number
}

// Enhanced Series Configuration
export interface SeriesConfig {
  type: 'Area' | 'Baseline' | 'Histogram' | 'Line' | 'Bar' | 'Candlestick'
  data: any[]
  options?: any
  name?: string
  priceScale?: any
  markers?: SeriesMarker<Time>[]
  trades?: TradeConfig[]  // Add trades to series
  tradeVisualizationOptions?: TradeVisualizationOptions
  annotations?: Annotation[]  // Add annotations to series
  shapes?: any[]  // Add shapes support
}

// Enhanced Chart Configuration
export interface ChartConfig {
  chart: any
  series: SeriesConfig[]
  priceLines?: any[]
  trades?: TradeConfig[]
  annotations?: Annotation[]  // Add chart-level annotations
  annotationLayers?: AnnotationLayer[]  // Add layer management
  chartId?: string
  rangeSwitcher?: RangeSwitcherConfig
}

// Range Switcher Configuration
export interface RangeConfig {
  label: string
  seconds: number | null
}

export interface RangeSwitcherConfig {
  ranges: RangeConfig[]
  position: string
  visible: boolean
  defaultRange?: string
}

// Sync Configuration
export interface SyncConfig {
  enabled: boolean
  crosshair: boolean
  timeRange: boolean
}

// Component Configuration
export interface ComponentConfig {
  charts: ChartConfig[]
  syncConfig: SyncConfig
  callbacks?: string[]
} 