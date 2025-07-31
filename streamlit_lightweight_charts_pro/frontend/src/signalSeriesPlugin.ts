/**
 * Signal Series Plugin for Lightweight Charts
 * 
 * This plugin renders background bands based on signal data, creating
 * vertical colored bands that span the entire chart height for specific
 * time periods.
 */

import {
  IChartApi,
  ISeriesApi,
  ISeriesPrimitive,
  SeriesAttachedParameter,
  IPrimitivePaneView,
  IPrimitivePaneRenderer,
  Coordinate,
  Time,
  UTCTimestamp,
  LineSeries,
} from 'lightweight-charts';

export interface SignalData {
  time: string;
  value: number;
}

export interface SignalOptions {
  color0: string;
  color1: string;
  color2?: string;
  visible: boolean;
}

export interface SignalSeriesConfig {
  type: 'signal';
  data: SignalData[];
  options: SignalOptions;
}

// Signal renderer data interface
interface SignalRendererData {
  x: Coordinate | number;
  y1: Coordinate | number;
  y2: Coordinate | number;
  color: string;
}

// Signal view data interface
interface SignalViewData {
  data: SignalRendererData[];
  options: SignalOptions;
}

// Signal primitive pane renderer
class SignalPrimitivePaneRenderer implements IPrimitivePaneRenderer {
  _viewData: SignalViewData;

  constructor(data: SignalViewData) {
    this._viewData = data;
  }

  draw() {}

  drawBackground(target: any) {
    const points: SignalRendererData[] = this._viewData.data;
    if (points.length === 0) return;

    target.useBitmapCoordinateSpace((scope: any) => {
      const ctx = scope.context;
      ctx.scale(scope.horizontalPixelRatio, scope.verticalPixelRatio);

      // Draw background bands
      for (let i = 0; i < points.length; i += 2) {
        if (i + 1 < points.length) {
          const startPoint = points[i];
          const endPoint = points[i + 1];

          ctx.fillStyle = startPoint.color;
          
          ctx.fillRect(
            startPoint.x,
            startPoint.y1,
            endPoint.x - startPoint.x,
            startPoint.y2 - startPoint.y1
          );
        }
      }
    });
  }
}

// Signal primitive pane view
class SignalPrimitivePaneView implements IPrimitivePaneView {
  _source: SignalSeries;
  _data: SignalViewData;

  constructor(source: SignalSeries) {
    this._source = source;
    this._data = {
      data: [],
      options: this._source.getOptions(),
    };
  }

  update() {
    const timeScale = this._source.getChart().timeScale();
    const priceScale = this._source.getChart().priceScale('left');
    
    if (!timeScale || !priceScale) return;

    const bands = this._source.getBackgroundBands();
    const renderData: SignalRendererData[] = [];

    bands.forEach(band => {
      const startX = timeScale.timeToCoordinate(band.startTime);
      const endX = timeScale.timeToCoordinate(band.endTime);
      
      if (startX !== null && endX !== null) {
        // Get the full height of the chart
        const chartHeight = this._source.getChart().chartElement()?.clientHeight || 400;
        
        renderData.push({
          x: startX,
          y1: 0,
          y2: chartHeight,
          color: band.color,
        });
        
        renderData.push({
          x: endX,
          y1: 0,
          y2: chartHeight,
          color: band.color,
        });
      }
    });

    this._data.data = renderData;
  }

  renderer() {
    return new SignalPrimitivePaneRenderer(this._data);
  }
}

// Background band interface
interface BackgroundBand {
  startTime: UTCTimestamp;
  endTime: UTCTimestamp;
  value: number;
  color: string;
}

// Signal series class
export class SignalSeries implements ISeriesPrimitive<Time> {
  private chart: IChartApi;
  private dummySeries: ISeriesApi<'Line'>;
  private options: SignalOptions;
  private signalData: SignalData[] = [];
  private backgroundBands: BackgroundBand[] = [];
  private _paneViews: SignalPrimitivePaneView[];

  constructor(chart: IChartApi, config: SignalSeriesConfig) {
    this.chart = chart;
    this.options = config.options;
    this.signalData = config.data;
    this._paneViews = [new SignalPrimitivePaneView(this)];
    
    // Create a dummy line series to attach the primitive to
    this.dummySeries = chart.addSeries(LineSeries, {
      color: 'transparent',
      lineWidth: 0 as any,
      visible: false,
      priceScaleId: 'left',
    });

    // Process signal data to create background bands
    this.processSignalData();

    // Attach the primitive to the dummy series for rendering
    this.dummySeries.attachPrimitive(this);
  }

  /**
   * Process signal data to create background bands
   */
  private processSignalData(): void {
    this.backgroundBands = [];
    
    if (this.signalData.length === 0) return;

    // Group consecutive signals with the same value
    let currentBand = {
      value: this.signalData[0].value,
      startTime: this.timeToTimestamp(this.signalData[0].time),
      endTime: this.timeToTimestamp(this.signalData[0].time),
    };

    for (let i = 1; i < this.signalData.length; i++) {
      const signal = this.signalData[i];
      
      if (signal.value === currentBand.value) {
        // Extend current band
        currentBand.endTime = this.timeToTimestamp(signal.time);
      } else {
        // End current band and start new one
        this.addBackgroundBand(currentBand);
        currentBand = {
          value: signal.value,
          startTime: this.timeToTimestamp(signal.time),
          endTime: this.timeToTimestamp(signal.time),
        };
      }
    }

    // Add the last band
    this.addBackgroundBand(currentBand);
  }

  /**
   * Add a background band
   */
  private addBackgroundBand(band: { value: number; startTime: UTCTimestamp; endTime: UTCTimestamp }): void {
    const color = this.getColorForValue(band.value);
    if (!color) return;

    this.backgroundBands.push({
      startTime: band.startTime,
      endTime: band.endTime,
      value: band.value,
      color: color,
    });
  }

  /**
   * Get color for a signal value
   */
  private getColorForValue(value: number): string | null {
    switch (value) {
      case 0:
        return this.options.color0;
      case 1:
        return this.options.color1;
      case 2:
        return this.options.color2 || null;
      default:
        return null;
    }
  }

  /**
   * Convert time string to timestamp
   */
  private timeToTimestamp(timeStr: string): UTCTimestamp {
    const date = new Date(timeStr);
    return (date.getTime() / 1000) as UTCTimestamp;
  }

  // Getter methods
  getOptions(): SignalOptions {
    return this.options;
  }

  getChart(): IChartApi {
    return this.chart;
  }

  getBackgroundBands(): BackgroundBand[] {
    return this.backgroundBands;
  }

  // ISeriesPrimitive implementation
  attached(param: SeriesAttachedParameter<Time>): void {
    // Primitive is attached to the series
  }

  detached(): void {
    // Primitive is detached from the series
  }

  updateAllViews(): void {
    this._paneViews.forEach(pv => pv.update());
  }

  paneViews(): IPrimitivePaneView[] {
    return this._paneViews;
  }

  /**
   * Update signal data and re-render
   */
  updateData(newData: SignalData[]): void {
    this.signalData = newData;
    this.processSignalData();
    this.updateAllViews();
  }

  /**
   * Update options and re-render
   */
  updateOptions(newOptions: SignalOptions): void {
    this.options = newOptions;
    this.processSignalData();
    this.updateAllViews();
  }

  /**
   * Set data (for compatibility with ISeriesApi interface)
   */
  setData(data: SignalData[]): void {
    this.updateData(data);
  }

  /**
   * Update single data point (for compatibility with ISeriesApi interface)
   */
  update(data: SignalData): void {
    // For signal series, we need to update the entire dataset
    const newData = [...this.signalData];
    const existingIndex = newData.findIndex(item => item.time === data.time);
    
    if (existingIndex >= 0) {
      newData[existingIndex] = data;
    } else {
      newData.push(data);
    }
    
    this.updateData(newData);
  }

  /**
   * Apply options (for compatibility with ISeriesApi interface)
   */
  applyOptions(options: Partial<SignalOptions>): void {
    this.updateOptions({ ...this.options, ...options });
  }

  /**
   * Get price scale (for compatibility with ISeriesApi interface)
   */
  priceScale(): any {
    return this.chart.priceScale('left');
  }

  /**
   * Remove the series (for compatibility with ISeriesApi interface)
   */
  remove(): void {
    this.destroy();
  }

  /**
   * Destroy the plugin and clean up resources
   */
  destroy(): void {
    try {
      this.chart.removeSeries(this.dummySeries);
    } catch (error) {
      // Series already removed
    }
  }
}

/**
 * Factory function to create signal series plugin
 */
export function createSignalSeriesPlugin(chart: IChartApi, config: SignalSeriesConfig): SignalSeries {
  return new SignalSeries(chart, config);
} 