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
  time: string | number;
  value: number;
  color?: string;
}

export interface SignalOptions {
  neutralColor?: string;
  signalColor?: string;
  alertColor?: string;
  visible: boolean;
}

export interface SignalSeriesConfig {
  type: 'signal';
  data: SignalData[];
  options: SignalOptions;
  paneId?: number;
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

  draw(target: any) {
    this.drawBackground(target);
  }

  drawBackground(target: any) {
    const points: SignalRendererData[] = this._viewData.data;
    
    if (points.length === 0) {
      return;
    }

    target.useBitmapCoordinateSpace((scope: any) => {
      const ctx = scope.context;
      ctx.scale(scope.horizontalPixelRatio, scope.verticalPixelRatio);
      
      // Draw background bands - following TradingView's approach
      for (let i = 0; i < points.length; i += 2) {
        if (i + 1 < points.length) {
          const startPoint = points[i];
          const endPoint = points[i + 1];

          // Use the color exactly as provided by the backend
          const fillStyle = startPoint.color;
          
          ctx.fillStyle = fillStyle;
          
          // Draw the background rectangle
          const width = Math.max(1, endPoint.x - startPoint.x); // Ensure minimum width
          const height = startPoint.y2 - startPoint.y1;
          
          ctx.fillRect(
            startPoint.x,
            startPoint.y1,
            width,
            height
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
    
    if (!timeScale || !priceScale) {
      return;
    }

    // Debug time scale information
    const visibleRange = timeScale.getVisibleRange();
    
    const bands = this._source.getBackgroundBands();
    
    const renderData: SignalRendererData[] = [];

    // Get bar spacing to properly align with bars
    const barSpacing = timeScale.options().barSpacing || 6;
    const halfBarSpacing = barSpacing / 2;
    
    bands.forEach((band, index) => {
      const startX = timeScale.timeToCoordinate(band.startTime);
      const endX = timeScale.timeToCoordinate(band.endTime);
      
      // Handle cases where coordinates are null (outside visible range)
      if (startX !== null && endX !== null) {
        // Both coordinates are valid - adjust for bar alignment
        const chartHeight = this._source.getChart().chartElement()?.clientHeight || 400;
        
        // Adjust start and end coordinates to align with bar boundaries
        const adjustedStartX = startX - halfBarSpacing;
        const adjustedEndX = endX + halfBarSpacing;
        
        renderData.push({
          x: adjustedStartX,
          y1: 0,
          y2: chartHeight,
          color: band.color,
        });
        
        renderData.push({
          x: adjustedEndX,
          y1: 0,
          y2: chartHeight,
          color: band.color,
        });
        

      } else if (startX !== null && endX === null) {
        // Start is visible but end is outside - extend to chart edge
        const chartHeight = this._source.getChart().chartElement()?.clientHeight || 400;
        const chartWidth = this._source.getChart().chartElement()?.clientWidth || 800;
        
        const adjustedStartX = startX - halfBarSpacing;
        
        renderData.push({
          x: adjustedStartX,
          y1: 0,
          y2: chartHeight,
          color: band.color,
        });
        
        renderData.push({
          x: chartWidth,
          y1: 0,
          y2: chartHeight,
          color: band.color,
        });
        
      } else if (startX === null && endX !== null) {
        // End is visible but start is outside - extend from chart edge
        const chartHeight = this._source.getChart().chartElement()?.clientHeight || 400;
        
        const adjustedEndX = endX + halfBarSpacing;
        
        renderData.push({
          x: 0,
          y1: 0,
          y2: chartHeight,
          color: band.color,
        });
        
        renderData.push({
          x: adjustedEndX,
          y1: 0,
          y2: chartHeight,
          color: band.color,
        });
      } else {
        // Both coordinates are null - band is completely outside visible range
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
  value: number | boolean;
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
  private paneId: number;

  constructor(chart: IChartApi, config: SignalSeriesConfig) {
    this.chart = chart;
    this.options = config.options;
    this.signalData = config.data;
    this.paneId = config.paneId || 0;
    this._paneViews = [new SignalPrimitivePaneView(this)];
    
    // Create a dummy line series to attach the primitive to
    this.dummySeries = chart.addSeries(LineSeries, {
      color: 'transparent',
      lineWidth: 0 as any,
      visible: false,
      priceScaleId: 'left',
    }, this.paneId);

    // Add some dummy data to ensure the time scale is properly initialized
    if (this.signalData.length > 0) {
      const dummyData = this.signalData.map(signal => ({
        time: this.parseTime(signal.time),
        value: 0
      }));
      this.dummySeries.setData(dummyData);
    }

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
    
    if (this.signalData.length === 0) {
      return;
    }

    // Sort signals by time to ensure proper ordering
    const sortedSignals = [...this.signalData].sort((a, b) => {
      const timeA = this.parseTime(a.time);
      const timeB = this.parseTime(b.time);
      return timeA - timeB;
    });
    
    let currentBandStart: UTCTimestamp | null = null;
    let currentBandValue: number | null = null;
    let currentBandColor: string | undefined = undefined;
    
    for (let i = 0; i < sortedSignals.length; i++) {
      const signal = sortedSignals[i];
      const signalTime = this.parseTime(signal.time);
      
      // Only calculate color if we need to start a new band
      if (currentBandStart === null || signal.value !== currentBandValue) {
        // End the previous band if it exists
        if (currentBandStart !== null && currentBandValue !== null) {
          const band = {
            value: currentBandValue,
            startTime: currentBandStart,
            endTime: signalTime,
            individualColor: currentBandColor,
          };
          this.addBackgroundBand(band);
        }
        
        // Start a new band
        currentBandStart = signalTime;
        currentBandValue = signal.value;
        currentBandColor = signal.color || this.getColorForValue(signal.value) || undefined;
      }
    }
    
    // End the last band - extend it to a reasonable future time
    if (currentBandStart !== null && currentBandValue !== null) {
      // Extend the last band by adding a reasonable time offset (e.g., 1 day)
      const lastSignalTime = sortedSignals[sortedSignals.length - 1];
      const lastTime = this.parseTime(lastSignalTime.time);
      const extendedEndTime = lastTime + (24 * 60 * 60); // Add 24 hours
      
      const band = {
        value: currentBandValue,
        startTime: currentBandStart,
        endTime: extendedEndTime as UTCTimestamp,
        individualColor: currentBandColor,
      };
      this.addBackgroundBand(band);
    }
    

  }

  /**
   * Add a background band
   */
  private addBackgroundBand(band: { value: number | boolean; startTime: UTCTimestamp; endTime: UTCTimestamp; individualColor?: string }): void {
    // Use individual color if available, otherwise fall back to series-level colors
    let color = band.individualColor;
    if (!color) {
      const seriesColor = this.getColorForValue(band.value);
      if (seriesColor) {
        color = seriesColor;
      }
    }
    
    if (!color) {
      return;
    }

    const backgroundBand = {
      startTime: band.startTime,
      endTime: band.endTime,
      value: typeof band.value === 'boolean' ? (band.value ? 1 : 0) : band.value,
      color: color,
    };
    
    this.backgroundBands.push(backgroundBand);
  }

  /**
   * Get color for a signal value
   */
  private getColorForValue(value: number | boolean): string | null {
    // Handle boolean values
    if (typeof value === 'boolean') {
      if (value === true) {
        return this.options.signalColor || null;
      } else {
        return this.options.neutralColor || null;
      }
    }
    
    // Handle numeric values
    switch (value) {
      case 0:
        return this.options.neutralColor || null;
      case 1:
        return this.options.signalColor || null;
      case 2:
        // For value 2, try alertColor first, then fall back to signalColor if alertColor is not set
        return this.options.alertColor || this.options.signalColor || null;
      default:
        return null;
    }
  }

  /**
   * Parse time value to timestamp
   * Handles both string dates and numeric timestamps
   */
  private parseTime(time: string | number): UTCTimestamp {
    try {
      // If it's already a number (Unix timestamp), convert to seconds if needed
      if (typeof time === 'number') {
        // If timestamp is in milliseconds, convert to seconds
        if (time > 1000000000000) {
          return Math.floor(time / 1000) as UTCTimestamp;
        }
        return Math.floor(time) as UTCTimestamp;
      }
      
      // If it's a string, try to parse as date
      if (typeof time === 'string') {
        // First try to parse as Unix timestamp string
        const timestamp = parseInt(time, 10);
        if (!isNaN(timestamp)) {
          // It's a numeric string (Unix timestamp)
          if (timestamp > 1000000000000) {
            return Math.floor(timestamp / 1000) as UTCTimestamp;
          }
          return Math.floor(timestamp) as UTCTimestamp;
        }
        
        // Try to parse as date string
        const date = new Date(time);
        if (isNaN(date.getTime())) {
          console.warn(`Failed to parse time: ${time}`);
          return 0 as UTCTimestamp;
        }
        return Math.floor(date.getTime() / 1000) as UTCTimestamp;
      }
      
      return 0 as UTCTimestamp;
    } catch (error) {
      console.error(`Error parsing time ${time}:`, error);
      return 0 as UTCTimestamp;
    }
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