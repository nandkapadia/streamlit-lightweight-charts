import { Time, SeriesMarker } from "lightweight-charts"

// Enhanced Trade Configuration
export interface TradeConfig {
  entryTime: string | number
  entryPrice: number
  exitTime: string | number
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
  showAnnotations?: boolean
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
  visible: boolean
  opacity: number
  annotations: Annotation[]
}

export interface AnnotationManager {
  layers: { [key: string]: AnnotationLayer }
}

// Pane Height Configuration
export interface PaneHeightOptions {
  factor: number
}

// Signal Series Configuration
export interface SignalData {
  time: string
  value: number
}

export interface SignalOptions {
  color0: string
  color1: string
  color2?: string
  visible: boolean
}

// Enhanced Series Configuration
export interface SeriesConfig {
  type: 'Area' | 'Band' | 'Baseline' | 'Histogram' | 'Line' | 'Bar' | 'Candlestick'
  data: any[]
  options?: any
  name?: string
  priceScale?: any
  markers?: SeriesMarker<Time>[]
  priceLines?: any[]  // Add price lines to series
  trades?: TradeConfig[]  // Add trades to series
  tradeVisualizationOptions?: TradeVisualizationOptions
  annotations?: Annotation[]  // Add annotations to series
  shapes?: any[]  // Add shapes support
  tooltip?: TooltipConfig  // Add tooltip configuration
  paneId?: number // Add support for multi-pane charts
  // Signal series support
  signalData?: SignalData[]
  signalOptions?: SignalOptions
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
  legend?: LegendConfig
  tooltip?: TooltipConfig  // Add chart-level tooltip configuration
  tradeVisualizationOptions?: TradeVisualizationOptions  // Add chart-level trade visualization options
  autoSize?: boolean
  autoWidth?: boolean
  autoHeight?: boolean
  minWidth?: number
  minHeight?: number
  maxWidth?: number
  maxHeight?: number
  paneHeights?: { [key: string]: PaneHeightOptions }  // Add pane heights configuration
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

// Legend Configuration
export interface LegendConfig {
  visible: boolean
  type: 'simple' | '3line'
  position: 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right'
  symbolName?: string
  fontSize?: number
  fontFamily?: string
  fontWeight?: string
  color?: string
  backgroundColor?: string
  borderColor?: string
  borderWidth?: number
  borderRadius?: number
  padding?: number
  margin?: number
  zIndex?: number
  showLastValue?: boolean
  showTime?: boolean
  showSymbol?: boolean
  priceFormat?: string
  customTemplate?: string
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

// Modular Tooltip System
export interface TooltipField {
  label: string
  valueKey: string
  formatter?: (value: any) => string
  color?: string
  fontSize?: number
  fontWeight?: string
}

export interface TooltipConfig {
  enabled: boolean
  type: 'ohlc' | 'single' | 'multi' | 'custom'
  fields: TooltipField[]
  position?: 'cursor' | 'fixed' | 'auto'
  offset?: { x: number; y: number }
  style?: {
    backgroundColor?: string
    borderColor?: string
    borderWidth?: number
    borderRadius?: number
    padding?: number
    fontSize?: number
    fontFamily?: string
    color?: string
    boxShadow?: string
    zIndex?: number
  }
  showDate?: boolean
  dateFormat?: string
  showTime?: boolean
  timeFormat?: string
} 