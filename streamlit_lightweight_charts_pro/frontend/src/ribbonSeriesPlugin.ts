import {
  IChartApi,
  ISeriesApi,
  LineData,
  Time,
  LineSeries,
  ISeriesPrimitive,
  SeriesAttachedParameter,
  IPrimitivePaneView,
  IPrimitivePaneRenderer,
  Coordinate,
} from 'lightweight-charts'

// Ribbon data interface
export interface RibbonData extends LineData {
  upper: number
  lower: number
  fill?: string
}

// Line style options interface
export interface LineStyleOptions {
  color?: string
  lineStyle?: number
  lineWidth?: number
  lineVisible?: boolean
  lineType?: number
  crosshairMarkerVisible?: boolean
  crosshairMarkerRadius?: number
  crosshairMarkerBorderColor?: string
  crosshairMarkerBackgroundColor?: string
  crosshairMarkerBorderWidth?: number
  lastPriceAnimation?: number
}

// Ribbon series options
export interface RibbonSeriesOptions {
  // Line style options
  upperLine?: LineStyleOptions
  lowerLine?: LineStyleOptions
  
  // Fill color
  fill: string
  
  // Fill visibility
  fillVisible: boolean
  
  // Base options
  visible: boolean
  priceScaleId: string
  lastValueVisible: boolean
  priceLineVisible: boolean
  priceLineSource: string
  priceLineWidth: number
  priceLineColor: string
  priceLineStyle: number
  baseLineVisible: boolean
  baseLineWidth: number
  baseLineColor: string
  baseLineStyle: string
  priceFormat: any
}

// Default options
const defaultOptions: RibbonSeriesOptions = {
  // Line style options
  upperLine: {
    color: '#4CAF50',
    lineStyle: 0, // SOLID
    lineWidth: 2,
    lineVisible: true,
    lineType: 0, // SIMPLE
    crosshairMarkerVisible: true,
    crosshairMarkerRadius: 4,
    crosshairMarkerBorderColor: '',
    crosshairMarkerBackgroundColor: '',
    crosshairMarkerBorderWidth: 2,
    lastPriceAnimation: 0, // DISABLED
  },
  lowerLine: {
    color: '#F44336',
    lineStyle: 0, // SOLID
    lineWidth: 2,
    lineVisible: true,
    lineType: 0, // SIMPLE
    crosshairMarkerVisible: true,
    crosshairMarkerRadius: 4,
    crosshairMarkerBorderColor: '',
    crosshairMarkerBackgroundColor: '',
    crosshairMarkerBorderWidth: 2,
    lastPriceAnimation: 0, // DISABLED
  },
  
  // Fill color
  fill: 'rgba(76, 175, 80, 0.1)',
  
  // Fill visibility
  fillVisible: true,
  
  // Base options
  visible: true,
  priceScaleId: 'right',
  lastValueVisible: false,
  priceLineVisible: true,
  priceLineSource: 'lastBar',
  priceLineWidth: 1,
  priceLineColor: '#2196F3',
  priceLineStyle: 2, // DASHED
  baseLineVisible: false,
  baseLineWidth: 1,
  baseLineColor: '#FF9800',
  baseLineStyle: 'solid',
  priceFormat: { type: 'price', precision: 2 },
}

// Ribbon renderer data interface
interface RibbonRendererData {
  x: Coordinate | number
  upper: Coordinate | number
  lower: Coordinate | number
  fill?: string
}

// Ribbon view data interface
interface RibbonViewData {
  data: RibbonRendererData[]
  options: RibbonSeriesOptions
}

// Ribbon primitive pane renderer
class RibbonPrimitivePaneRenderer implements IPrimitivePaneRenderer {
  _viewData: RibbonViewData

  constructor(data: RibbonViewData) {
    this._viewData = data
  }

  draw() {}

  drawBackground(target: any) {
    const points: RibbonRendererData[] = this._viewData.data
    if (points.length === 0) return

    target.useBitmapCoordinateSpace((scope: any) => {
      const ctx = scope.context
      ctx.scale(scope.horizontalPixelRatio, scope.verticalPixelRatio)

      // Draw fill area between upper and lower bands only if enabled
      if (this._viewData.options.fillVisible) {
        ctx.fillStyle = this._viewData.options.fill
        ctx.beginPath()
        
        // Find first valid point
        let firstValidIndex = 0
        while (firstValidIndex < points.length && 
               (points[firstValidIndex].upper === null || points[firstValidIndex].lower === null)) {
          firstValidIndex++
        }
        
        if (firstValidIndex < points.length) {
          ctx.moveTo(points[firstValidIndex].x, points[firstValidIndex].upper)
          
          // Draw upper line (handle gaps)
          for (let i = firstValidIndex; i < points.length; i++) {
            const point = points[i]
            if (point.upper !== null && point.lower !== null) {
              ctx.lineTo(point.x, point.upper)
            } else {
              // Break the path when we hit a gap
              ctx.stroke()
              ctx.beginPath()
              // Find next valid point
              let nextValidIndex = i + 1
              while (nextValidIndex < points.length && 
                     (points[nextValidIndex].upper === null || points[nextValidIndex].lower === null)) {
                nextValidIndex++
              }
              if (nextValidIndex < points.length) {
                ctx.moveTo(points[nextValidIndex].x, points[nextValidIndex].upper)
                i = nextValidIndex - 1  // Adjust loop index
              }
            }
          }
          
          // Draw lower line (handle gaps)
          for (let i = points.length - 1; i >= firstValidIndex; i--) {
            const point = points[i]
            if (point.upper !== null && point.lower !== null) {
              ctx.lineTo(point.x, point.lower)
            } else {
              // Break the path when we hit a gap
              ctx.stroke()
              ctx.beginPath()
              // Find previous valid point
              let prevValidIndex = i - 1
              while (prevValidIndex >= firstValidIndex && 
                     (points[prevValidIndex].upper === null || points[prevValidIndex].lower === null)) {
                prevValidIndex--
              }
              if (prevValidIndex >= firstValidIndex) {
                ctx.moveTo(points[prevValidIndex].x, points[prevValidIndex].lower)
                i = prevValidIndex + 1  // Adjust loop index
              }
            }
          }
          
          ctx.closePath()
          ctx.fill()
        }
      }
    })
  }
}

// Ribbon primitive pane view
class RibbonPrimitivePaneView implements IPrimitivePaneView {
  _renderer: RibbonPrimitivePaneRenderer

  constructor(data: RibbonViewData) {
    this._renderer = new RibbonPrimitivePaneRenderer(data)
  }

  renderer(): IPrimitivePaneRenderer {
    return this._renderer
  }
}

// Ribbon primitive
class RibbonPrimitive implements ISeriesPrimitive<Time> {
  _view: RibbonPrimitivePaneView
  _data: RibbonRendererData[]
  _options: RibbonSeriesOptions

  constructor(data: RibbonRendererData[], options: RibbonSeriesOptions) {
    this._data = data
    this._options = options
    this._view = new RibbonPrimitivePaneView({ data, options })
  }

  attached(param: SeriesAttachedParameter<Time>): void {
    // Handle attachment to series
  }

  detached(): void {
    // Handle detachment from series
  }

  update(data: RibbonRendererData[], options: RibbonSeriesOptions): void {
    this._data = data
    this._options = options
    this._view = new RibbonPrimitivePaneView({ data, options })
  }

  data(): RibbonRendererData[] {
    return this._data
  }

  options(): RibbonSeriesOptions {
    return this._options
  }

  paneViews(): IPrimitivePaneView[] {
    return [this._view]
  }
}

// Ribbon series API
export class RibbonSeriesApi {
  private _chart: IChartApi
  private _upperSeries: ISeriesApi<'Line'>
  private _lowerSeries: ISeriesApi<'Line'>
  private _primitive: RibbonPrimitive | null = null
  private _options: RibbonSeriesOptions

  constructor(chart: IChartApi, options: RibbonSeriesOptions = defaultOptions) {
    this._chart = chart
    this._options = { ...defaultOptions, ...options }

    // Create upper and lower line series
    this._upperSeries = chart.addSeries(LineSeries, {
      color: this._options.upperLine?.color || '#4CAF50',
      lineStyle: this._options.upperLine?.lineStyle || 0,
      lineWidth: (this._options.upperLine?.lineWidth || 2) as any,
      lineVisible: this._options.upperLine?.lineVisible ?? true,
      lineType: this._options.upperLine?.lineType || 0,
      crosshairMarkerVisible: this._options.upperLine?.crosshairMarkerVisible ?? true,
      crosshairMarkerRadius: this._options.upperLine?.crosshairMarkerRadius || 4,
      crosshairMarkerBorderColor: this._options.upperLine?.crosshairMarkerBorderColor || '',
      crosshairMarkerBackgroundColor: this._options.upperLine?.crosshairMarkerBackgroundColor || '',
      crosshairMarkerBorderWidth: this._options.upperLine?.crosshairMarkerBorderWidth || 2,
      lastPriceAnimation: this._options.upperLine?.lastPriceAnimation || 0,
      priceScaleId: this._options.priceScaleId,
      lastValueVisible: this._options.lastValueVisible,
      priceLineVisible: this._options.priceLineVisible,
      priceLineSource: this._options.priceLineSource as any,
      priceLineWidth: this._options.priceLineWidth as any,
      priceLineColor: this._options.priceLineColor,
      priceLineStyle: this._options.priceLineStyle as any,
      baseLineVisible: this._options.baseLineVisible,
      baseLineWidth: this._options.baseLineWidth as any,
      baseLineColor: this._options.baseLineColor,
      baseLineStyle: this._options.baseLineStyle as any,
      priceFormat: this._options.priceFormat,
    })

    this._lowerSeries = chart.addSeries(LineSeries, {
      color: this._options.lowerLine?.color || '#F44336',
      lineStyle: this._options.lowerLine?.lineStyle || 0,
      lineWidth: (this._options.lowerLine?.lineWidth || 2) as any,
      lineVisible: this._options.lowerLine?.lineVisible ?? true,
      lineType: this._options.lowerLine?.lineType || 0,
      crosshairMarkerVisible: this._options.lowerLine?.crosshairMarkerVisible ?? true,
      crosshairMarkerRadius: this._options.lowerLine?.crosshairMarkerRadius || 4,
      crosshairMarkerBorderColor: this._options.lowerLine?.crosshairMarkerBorderColor || '',
      crosshairMarkerBackgroundColor: this._options.lowerLine?.crosshairMarkerBackgroundColor || '',
      crosshairMarkerBorderWidth: this._options.lowerLine?.crosshairMarkerBorderWidth || 2,
      lastPriceAnimation: this._options.lowerLine?.lastPriceAnimation || 0,
      priceScaleId: this._options.priceScaleId,
      lastValueVisible: this._options.lastValueVisible,
      priceLineVisible: this._options.priceLineVisible,
      priceLineSource: this._options.priceLineSource as any,
      priceLineWidth: this._options.priceLineWidth as any,
      priceLineColor: this._options.priceLineColor,
      priceLineStyle: this._options.priceLineStyle as any,
      baseLineVisible: this._options.baseLineVisible,
      baseLineWidth: this._options.baseLineWidth as any,
      baseLineColor: this._options.baseLineColor,
      baseLineStyle: this._options.baseLineStyle as any,
      priceFormat: this._options.priceFormat,
    })

    // Set visibility
    this._upperSeries.applyOptions({ visible: this._options.visible })
    this._lowerSeries.applyOptions({ visible: this._options.visible })
  }

  setData(data: RibbonData[]): void {
    // Extract upper and lower data, filtering out None values
    const upperData = data
      .filter(item => item.upper !== null && item.upper !== undefined)
      .map(item => ({
        time: item.time,
        value: item.upper,
      }))

    const lowerData = data
      .filter(item => item.lower !== null && item.lower !== undefined)
      .map(item => ({
        time: item.time,
        value: item.lower,
      }))

    // Set data for both series
    this._upperSeries.setData(upperData)
    this._lowerSeries.setData(lowerData)

    // Create primitive for fill area
    if (this._options.fillVisible) {
              const rendererData: RibbonRendererData[] = data.map(item => ({
          x: item.time as number,
          upper: item.upper,
          lower: item.lower,
          
          fill: item.fill,
        }))

      // Remove existing primitive if any
      if (this._primitive) {
        this._upperSeries.detachPrimitive(this._primitive)
        this._primitive = null
      }

      // Create new primitive
      this._primitive = new RibbonPrimitive(rendererData, this._options)
      this._upperSeries.attachPrimitive(this._primitive)
    }
  }

  updateOptions(options: Partial<RibbonSeriesOptions>): void {
    this._options = { ...this._options, ...options }

    // Update series options
    if (options.upperLine) {
      this._upperSeries.applyOptions({
        color: options.upperLine.color || '#4CAF50',
        lineStyle: options.upperLine.lineStyle,
        lineWidth: options.upperLine.lineWidth as any,
        lineVisible: options.upperLine.lineVisible,
        lineType: options.upperLine.lineType,
        crosshairMarkerVisible: options.upperLine.crosshairMarkerVisible,
        crosshairMarkerRadius: options.upperLine.crosshairMarkerRadius,
        crosshairMarkerBorderColor: options.upperLine.crosshairMarkerBorderColor,
        crosshairMarkerBackgroundColor: options.upperLine.crosshairMarkerBackgroundColor,
        crosshairMarkerBorderWidth: options.upperLine.crosshairMarkerBorderWidth,
        lastPriceAnimation: options.upperLine.lastPriceAnimation,
      })
    }

    if (options.lowerLine) {
      this._lowerSeries.applyOptions({
        color: options.lowerLine.color || '#F44336',
        lineStyle: options.lowerLine.lineStyle,
        lineWidth: options.lowerLine.lineWidth as any,
        lineVisible: options.lowerLine.lineVisible,
        lineType: options.lowerLine.lineType,
        crosshairMarkerVisible: options.lowerLine.crosshairMarkerVisible,
        crosshairMarkerRadius: options.lowerLine.crosshairMarkerRadius,
        crosshairMarkerBorderColor: options.lowerLine.crosshairMarkerBorderColor,
        crosshairMarkerBackgroundColor: options.lowerLine.crosshairMarkerBackgroundColor,
        crosshairMarkerBorderWidth: options.lowerLine.crosshairMarkerBorderWidth,
        lastPriceAnimation: options.lowerLine.lastPriceAnimation,
      })
    }

    // Update primitive if it exists
    if (this._primitive) {
      this._primitive.update(this._primitive.data(), this._options)
    }
  }

  setVisible(visible: boolean): void {
    this._options.visible = visible
    this._upperSeries.applyOptions({ visible })
    this._lowerSeries.applyOptions({ visible })
  }

  getUpperSeries(): ISeriesApi<'Line'> {
    return this._upperSeries
  }

  getLowerSeries(): ISeriesApi<'Line'> {
    return this._lowerSeries
  }

  remove(): void {
    if (this._primitive) {
      this._upperSeries.detachPrimitive(this._primitive)
    }
    this._chart.removeSeries(this._upperSeries)
    this._chart.removeSeries(this._lowerSeries)
  }
}

// Plugin function
export function ribbonSeriesPlugin(): (chart: IChartApi) => void {
  return (chart: IChartApi) => {
    // Plugin initialization if needed
  }
}
