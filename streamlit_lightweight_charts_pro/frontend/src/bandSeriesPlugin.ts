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

// Band data interface
export interface BandData extends LineData {
  upper: number
  middle: number
  lower: number
}

// Band series options
export interface BandSeriesOptions {
  // Line colors
  upperLineColor: string
  middleLineColor: string
  lowerLineColor: string
  
  // Line styles
  upperLineStyle: number
  middleLineStyle: number
  lowerLineStyle: number
  
  // Line widths
  upperLineWidth: number
  middleLineWidth: number
  lowerLineWidth: number
  
  // Line visibility
  upperLineVisible: boolean
  middleLineVisible: boolean
  lowerLineVisible: boolean
  
  // Fill colors
  upperFillColor: string
  lowerFillColor: string
  
  // Line type
  lineType: number
  
  // Crosshair markers
  crosshairMarkerVisible: boolean
  crosshairMarkerRadius: number
  crosshairMarkerBorderColor: string
  crosshairMarkerBackgroundColor: string
  crosshairMarkerBorderWidth: number
  
  // Animation
  lastPriceAnimation: number
  
  // Base options
  visible: boolean
  priceScaleId: string
  lastValueVisible: boolean
  priceLineWidth: number
  priceLineColor: string
  priceLineStyle: string
  baseLineVisible: boolean
  baseLineWidth: number
  baseLineColor: string
  baseLineStyle: string
  priceFormat: any
}

// Default options
const defaultOptions: BandSeriesOptions = {
  // Line colors
  upperLineColor: '#4CAF50',
  middleLineColor: '#2196F3',
  lowerLineColor: '#F44336',
  
  // Line styles
  upperLineStyle: 0, // SOLID
  middleLineStyle: 0, // SOLID
  lowerLineStyle: 0, // SOLID
  
  // Line widths
  upperLineWidth: 2,
  middleLineWidth: 2,
  lowerLineWidth: 2,
  
  // Line visibility
  upperLineVisible: true,
  middleLineVisible: true,
  lowerLineVisible: true,
  
  // Fill colors
  upperFillColor: 'rgba(76, 175, 80, 0.1)',
  lowerFillColor: 'rgba(244, 67, 54, 0.1)',
  
  // Line type
  lineType: 0, // SIMPLE
  
  // Crosshair markers
  crosshairMarkerVisible: true,
  crosshairMarkerRadius: 4,
  crosshairMarkerBorderColor: '',
  crosshairMarkerBackgroundColor: '',
  crosshairMarkerBorderWidth: 2,
  
  // Animation
  lastPriceAnimation: 0, // DISABLED
  
  // Base options
  visible: true,
  priceScaleId: 'right',
        lastValueVisible: false,
  priceLineWidth: 1,
  priceLineColor: '#2196F3',
  priceLineStyle: 'solid',
  baseLineVisible: false,
  baseLineWidth: 1,
  baseLineColor: '#FF9800',
  baseLineStyle: 'solid',
  priceFormat: { type: 'price', precision: 2 },
}

// Band renderer data interface
interface BandRendererData {
  x: Coordinate | number
  upper: Coordinate | number
  middle: Coordinate | number
  lower: Coordinate | number
}

// Band view data interface
interface BandViewData {
  data: BandRendererData[]
  options: BandSeriesOptions
}

// Band primitive pane renderer
class BandPrimitivePaneRenderer implements IPrimitivePaneRenderer {
  _viewData: BandViewData

  constructor(data: BandViewData) {
    this._viewData = data
  }

  draw() {}

  drawBackground(target: any) {
    const points: BandRendererData[] = this._viewData.data
    if (points.length === 0) return

    target.useBitmapCoordinateSpace((scope: any) => {
      const ctx = scope.context
      ctx.scale(scope.horizontalPixelRatio, scope.verticalPixelRatio)

      // Draw upper fill area (between upper and middle)
      if (this._viewData.options.upperFillColor !== 'rgba(0, 0, 0, 0)') {
        ctx.fillStyle = this._viewData.options.upperFillColor
        ctx.beginPath()
        ctx.moveTo(points[0].x, points[0].upper)
        for (const point of points) {
          ctx.lineTo(point.x, point.upper)
        }
        for (let i = points.length - 1; i >= 0; i--) {
          ctx.lineTo(points[i].x, points[i].middle)
        }
        ctx.closePath()
        ctx.fill()
      }

      // Draw lower fill area (between middle and lower)
      if (this._viewData.options.lowerFillColor !== 'rgba(0, 0, 0, 0)') {
        ctx.fillStyle = this._viewData.options.lowerFillColor
        ctx.beginPath()
        ctx.moveTo(points[0].x, points[0].middle)
        for (const point of points) {
          ctx.lineTo(point.x, point.middle)
        }
        for (let i = points.length - 1; i >= 0; i--) {
          ctx.lineTo(points[i].x, points[i].lower)
        }
        ctx.closePath()
        ctx.fill()
      }
    })
  }
}

// Band primitive pane view
class BandPrimitivePaneView implements IPrimitivePaneView {
  _source: BandSeries
  _data: BandViewData

  constructor(source: BandSeries) {
    this._source = source
    this._data = {
      data: [],
      options: this._source.getOptions(),
    }
  }

  update() {
    const timeScale = this._source.getChart().timeScale()
    this._data.data = this._source.getData().map(d => {
      return {
        x: timeScale.timeToCoordinate(d.time) ?? -100,
        upper: this._source.getUpperSeries().priceToCoordinate(d.upper) ?? -100,
        middle: this._source.getMiddleSeries().priceToCoordinate(d.middle) ?? -100,
        lower: this._source.getLowerSeries().priceToCoordinate(d.lower) ?? -100,
      }
    })
  }

  renderer() {
    return new BandPrimitivePaneRenderer(this._data)
  }
}

// Band series class
export class BandSeries implements ISeriesPrimitive<Time> {
  private chart: IChartApi
  private upperSeries: ISeriesApi<'Line'>
  private middleSeries: ISeriesApi<'Line'>
  private lowerSeries: ISeriesApi<'Line'>
  private options: BandSeriesOptions
  private data: BandData[] = []
  private _paneViews: BandPrimitivePaneView[]

  constructor(chart: IChartApi, options: Partial<BandSeriesOptions> = {}) {
    this.chart = chart
    this.options = { ...defaultOptions, ...options }
    this._paneViews = [new BandPrimitivePaneView(this)]
    
    // Create the three line series
    this.upperSeries = chart.addSeries(LineSeries, {
      color: this.options.upperLineColor,
      lineStyle: this.options.upperLineStyle,
      lineWidth: this.options.upperLineWidth as any,
      visible: this.options.upperLineVisible,
      priceScaleId: this.options.priceScaleId,
      lastValueVisible: this.options.lastValueVisible,
      priceLineWidth: this.options.priceLineWidth as any,
      priceLineColor: this.options.priceLineColor,
      priceLineStyle: this.options.priceLineStyle as any,
      baseLineVisible: this.options.baseLineVisible,
      baseLineWidth: this.options.baseLineWidth as any,
      baseLineColor: this.options.baseLineColor,
      baseLineStyle: this.options.baseLineStyle as any,
      priceFormat: this.options.priceFormat,
      crosshairMarkerVisible: this.options.crosshairMarkerVisible,
      crosshairMarkerRadius: this.options.crosshairMarkerRadius,
      crosshairMarkerBorderColor: this.options.crosshairMarkerBorderColor,
      crosshairMarkerBackgroundColor: this.options.crosshairMarkerBackgroundColor,
      crosshairMarkerBorderWidth: this.options.crosshairMarkerBorderWidth,
      lastPriceAnimation: this.options.lastPriceAnimation,
      lineType: this.options.lineType,
    })

    this.middleSeries = chart.addSeries(LineSeries, {
      color: this.options.middleLineColor,
      lineStyle: this.options.middleLineStyle,
      lineWidth: this.options.middleLineWidth as any,
      visible: this.options.middleLineVisible,
      priceScaleId: this.options.priceScaleId,
      lastValueVisible: this.options.lastValueVisible,
      priceLineWidth: this.options.priceLineWidth as any,
      priceLineColor: this.options.priceLineColor,
      priceLineStyle: this.options.priceLineStyle as any,
      baseLineVisible: this.options.baseLineVisible,
      baseLineWidth: this.options.baseLineWidth as any,
      baseLineColor: this.options.baseLineColor,
      baseLineStyle: this.options.baseLineStyle as any,
      priceFormat: this.options.priceFormat,
      crosshairMarkerVisible: this.options.crosshairMarkerVisible,
      crosshairMarkerRadius: this.options.crosshairMarkerRadius,
      crosshairMarkerBorderColor: this.options.crosshairMarkerBorderColor,
      crosshairMarkerBackgroundColor: this.options.crosshairMarkerBackgroundColor,
      crosshairMarkerBorderWidth: this.options.crosshairMarkerBorderWidth,
      lastPriceAnimation: this.options.lastPriceAnimation,
      lineType: this.options.lineType,
    })

    this.lowerSeries = chart.addSeries(LineSeries, {
      color: this.options.lowerLineColor,
      lineStyle: this.options.lowerLineStyle,
      lineWidth: this.options.lowerLineWidth as any,
      visible: this.options.lowerLineVisible,
      priceScaleId: this.options.priceScaleId,
      lastValueVisible: this.options.lastValueVisible,
      priceLineWidth: this.options.priceLineWidth as any,
      priceLineColor: this.options.priceLineColor,
      priceLineStyle: this.options.priceLineStyle as any,
      baseLineVisible: this.options.baseLineVisible,
      baseLineWidth: this.options.baseLineWidth as any,
      baseLineColor: this.options.baseLineColor,
      baseLineStyle: this.options.baseLineStyle as any,
      priceFormat: this.options.priceFormat,
      crosshairMarkerVisible: this.options.crosshairMarkerVisible,
      crosshairMarkerRadius: this.options.crosshairMarkerRadius,
      crosshairMarkerBorderColor: this.options.crosshairMarkerBorderColor,
      crosshairMarkerBackgroundColor: this.options.crosshairMarkerBackgroundColor,
      crosshairMarkerBorderWidth: this.options.crosshairMarkerBorderWidth,
      lastPriceAnimation: this.options.lastPriceAnimation,
      lineType: this.options.lineType,
    })

    // Attach the primitive to the middle series for rendering
    this.middleSeries.attachPrimitive(this)
  }

  // Getter for options
  getOptions(): BandSeriesOptions {
    return this.options
  }

  // Getter for data
  getData(): BandData[] {
    return this.data
  }

  // Getter for chart
  getChart(): IChartApi {
    return this.chart
  }

  // Getter for series
  getUpperSeries(): ISeriesApi<'Line'> {
    return this.upperSeries
  }

  getMiddleSeries(): ISeriesApi<'Line'> {
    return this.middleSeries
  }

  getLowerSeries(): ISeriesApi<'Line'> {
    return this.lowerSeries
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

  setData(data: BandData[]): void {
    this.data = data
    
    // Extract individual series data
    const upperData: LineData[] = data.map(item => ({
      time: item.time,
      value: item.upper,
    }))
    
    const middleData: LineData[] = data.map(item => ({
      time: item.time,
      value: item.middle,
    }))
    
    const lowerData: LineData[] = data.map(item => ({
      time: item.time,
      value: item.lower,
    }))

    // Set data for each series
    this.upperSeries.setData(upperData)
    this.middleSeries.setData(middleData)
    this.lowerSeries.setData(lowerData)

    // Update the primitive view
    this.updateAllViews()
  }

  update(data: BandData): void {
    // Update individual series
    this.upperSeries.update({ time: data.time, value: data.upper })
    this.middleSeries.update({ time: data.time, value: data.middle })
    this.lowerSeries.update({ time: data.time, value: data.lower })

    // Update the primitive view
    this.updateAllViews()
  }

  setVisible(visible: boolean): void {
    this.upperSeries.applyOptions({ visible })
    this.middleSeries.applyOptions({ visible })
    this.lowerSeries.applyOptions({ visible })
  }

  setOptions(options: Partial<BandSeriesOptions>): void {
    this.options = { ...this.options, ...options }
    
    // Update line series options
    if (options.upperLineColor !== undefined) {
      this.upperSeries.applyOptions({ color: options.upperLineColor })
    }
    if (options.middleLineColor !== undefined) {
      this.middleSeries.applyOptions({ color: options.middleLineColor })
    }
    if (options.lowerLineColor !== undefined) {
      this.lowerSeries.applyOptions({ color: options.lowerLineColor })
    }
    
    if (options.upperLineWidth !== undefined) {
      this.upperSeries.applyOptions({ lineWidth: options.upperLineWidth as any })
    }
    if (options.middleLineWidth !== undefined) {
      this.middleSeries.applyOptions({ lineWidth: options.middleLineWidth as any })
    }
    if (options.lowerLineWidth !== undefined) {
      this.lowerSeries.applyOptions({ lineWidth: options.lowerLineWidth as any })
    }
    
    if (options.upperLineVisible !== undefined) {
      this.upperSeries.applyOptions({ visible: options.upperLineVisible })
    }
    if (options.middleLineVisible !== undefined) {
      this.middleSeries.applyOptions({ visible: options.middleLineVisible })
    }
    if (options.lowerLineVisible !== undefined) {
      this.lowerSeries.applyOptions({ visible: options.lowerLineVisible })
    }

    // Update the primitive view
    this.updateAllViews()
  }

  remove(): void {
    this.chart.removeSeries(this.upperSeries)
    this.chart.removeSeries(this.middleSeries)
    this.chart.removeSeries(this.lowerSeries)
  }

  to_frontend_config(): any {
    return {
      type: 'band',
      data: this.data,
      options: this.options,
    }
  }
}

// Plugin factory function
export function createBandSeries(
  chart: IChartApi,
  options: Partial<BandSeriesOptions> = {}
): BandSeries {
  return new BandSeries(chart, options)
} 