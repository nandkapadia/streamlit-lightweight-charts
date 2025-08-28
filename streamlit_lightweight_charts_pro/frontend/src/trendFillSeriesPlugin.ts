/**
 * Trend Fill Series Plugin for Lightweight Charts
 * 
 * This plugin renders trend lines with fill areas between upper and lower bands,
 * creating a visual representation of trend direction and strength.
 * 
 * Features:
 * - Partial line drawing (segmented trend lines)
 * - Band filling between upper and lower trend lines
 * - Dynamic color changes based on trend direction
 * - Base line support for reference
 */

import {
  IChartApi,
  ISeriesApi,
  ISeriesPrimitive,
  SeriesAttachedParameter,
  IPrimitivePaneView,
  IPrimitivePaneRenderer,
  Time,
  UTCTimestamp,
  LineSeries,
} from 'lightweight-charts';

// Data structure for trend fill series
export interface TrendFillData {
  time: number | string;
  base_line?: number | null;
  upper_trend?: number | null;
  lower_trend?: number | null;
  trend_direction?: number | null;
  // Legacy field names for backward compatibility
  baseLine?: number | null;
  upperTrend?: number | null;
  lowerTrend?: number | null;
  trendDirection?: number | null;
}

// Options for trend fill series
export interface TrendFillOptions {
  uptrend_fill_color: string;
  downtrend_fill_color: string;
  fill_opacity: number;
  upper_trend_line: {
    color: string;
    lineWidth: 1 | 2 | 3 | 4;
    lineStyle: 0 | 1 | 2;
    visible: boolean;
  };
  lower_trend_line: {
    color: string;
    lineWidth: 1 | 2 | 3 | 4;
    lineStyle: 0 | 1 | 2;
    visible: boolean;
  };
  base_line: {
    color: string;
    lineWidth: 1 | 2 | 3 | 4;
    lineStyle: 0 | 1 | 2;
    visible: boolean;
  };
  visible: boolean;
  debug_mode?: boolean; // Control debug logging
  coordinate_tolerance?: number; // Coordinate bounds tolerance
}

// Internal data structures for rendering
interface TrendLineSegment {
  startTime: UTCTimestamp;
  endTime: UTCTimestamp;
  startPrice: number;
  endPrice: number;
  color: string;
  lineWidth: number;
  lineStyle: number;
}

interface BandFillData {
  startTime: UTCTimestamp;
  endTime: UTCTimestamp;
  upperPrice: number;
  lowerPrice: number;
  fillColor: string;
  opacity: number;
}

interface BaseLineData {
  time: UTCTimestamp;
  price: number;
  color: string;
  lineWidth: number;
  lineStyle: number;
}

// Renderer data interface
interface TrendFillRendererData {
  trendLines: TrendLineSegment[];
  bandFills: BandFillData[];
  baseLines: BaseLineData[];
  timeScale: any;
  priceScale: any;
  chartWidth: number;
}

// View data interface
interface TrendFillViewData {
  data: TrendFillRendererData;
  options: TrendFillOptions;
}

/**
 * Parse time value to timestamp
 * Handles both string dates and numeric timestamps
 */
function parseTime(time: string | number): UTCTimestamp {
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

// Trend fill primitive pane renderer
class TrendFillPrimitivePaneRenderer implements IPrimitivePaneRenderer {
  _viewData: TrendFillViewData;

  constructor(data: TrendFillViewData) {
    this._viewData = data;
  }

  draw(target: any) {
    this.drawTrendLines(target);
    this.drawBandFills(target);
    this.drawBaseLines(target);
  }

  private drawTrendLines(target: any) {
    const { trendLines } = this._viewData.data;
    
    if (trendLines.length === 0) return;

    target.useBitmapCoordinateSpace((scope: any) => {
      const ctx = scope.context;
      ctx.scale(scope.horizontalPixelRatio, scope.verticalPixelRatio);
      
      // Reset canvas state to prevent artifacts
      ctx.save();
      
      trendLines.forEach((segment, index) => {
        // Convert time and price to coordinates
        const timeScale = this._viewData.data.timeScale;
        const priceScale = this._viewData.data.priceScale;
        
        if (!timeScale || !priceScale) return;
        
        // Check if priceScale has the required methods
        if (typeof priceScale.priceToCoordinate !== 'function') {
          console.warn('[TrendFillSeries] priceScale.priceToCoordinate is not available');
          return;
        }
        
        // Safely convert coordinates with error handling
        let startX: number | null = null;
        let endX: number | null = null;
        let startY: number | null = null;
        let endY: number | null = null;
        
        try {
          startX = timeScale.timeToCoordinate(segment.startTime);
          endX = timeScale.timeToCoordinate(segment.endTime);
          startY = priceScale.priceToCoordinate(segment.startPrice);
          endY = priceScale.priceToCoordinate(segment.endPrice);
        } catch (error) {
          console.warn(`[TrendFillSeries] Error converting coordinates for trend line ${index}:`, error);
          return;
        }
        
        // Debug: Log only when debug mode is enabled and limit frequency
        if (this._viewData.options.debug_mode && index < 2) { // Only log first 2 when debug is enabled
          console.log(`[TrendFillSeries] Trend line ${index} coordinates:`, {
            startTime: segment.startTime,
            endTime: segment.endTime,
            startPrice: segment.startPrice,
            endPrice: segment.endPrice,
            startX, endX, startY, endY,
            chartWidth: this._viewData.data.chartWidth
          });
        }
        
        // Validate coordinates are within reasonable bounds
        if (startX === null || endX === null || startY === null || endY === null) {
          console.warn(`[TrendFillSeries] Invalid coordinates for trend line ${index}:`, { startX, endX, startY, endY });
          return;
        }
        
        // Check if coordinates are within reasonable bounds with configurable tolerance
        const chartWidth = this._viewData.data.chartWidth || 800;
        const tolerance = this._viewData.options.coordinate_tolerance || 100;
        if (startX < -tolerance || endX < -tolerance || startX > chartWidth + tolerance || endX > chartWidth + tolerance) {
          if (this._viewData.options.debug_mode) {
            console.warn(`[TrendFillSeries] Coordinates significantly out of bounds for trend line ${index}:`, { startX, endX, chartWidth, tolerance });
          }
          return;
        }
        
        // Clamp coordinates to chart bounds for better rendering
        const clampedStartX = Math.max(0, Math.min(startX, chartWidth));
        const clampedEndX = Math.max(0, Math.min(endX, chartWidth));
        
        // Set line style
        ctx.strokeStyle = segment.color;
        ctx.lineWidth = segment.lineWidth;
        ctx.setLineDash(this.getLineDash(segment.lineStyle));
        
        // Draw the line segment with clamped coordinates
        ctx.beginPath();
        ctx.moveTo(clampedStartX, startY);
        ctx.lineTo(clampedEndX, endY);
        ctx.stroke();
      });
      
      // Restore canvas state
      ctx.restore();
    });
  }

  private drawBandFills(target: any) {
    const { bandFills } = this._viewData.data;
    
    if (bandFills.length === 0) return;

    target.useBitmapCoordinateSpace((scope: any) => {
      const ctx = scope.context;
      ctx.scale(scope.horizontalPixelRatio, scope.verticalPixelRatio);
      
      // Reset canvas state to prevent artifacts
      ctx.save();
      
      bandFills.forEach((band, index) => {
        const timeScale = this._viewData.data.timeScale;
        const priceScale = this._viewData.data.priceScale;
        
        if (!timeScale || !priceScale) return;
        
        // Check if priceScale has the required methods
        if (typeof priceScale.priceToCoordinate !== 'function') {
          console.warn('[TrendFillSeries] priceScale.priceToCoordinate is not available');
          return;
        }
        
        // Safely convert coordinates with error handling
        let startX: number | null = null;
        let endX: number | null = null;
        let upperY: number | null = null;
        let lowerY: number | null = null;
        
        try {
          startX = timeScale.timeToCoordinate(band.startTime);
          endX = timeScale.timeToCoordinate(band.endTime);
          upperY = priceScale.priceToCoordinate(band.upperPrice);
          lowerY = priceScale.priceToCoordinate(band.lowerPrice);
        } catch (error) {
          console.warn(`[TrendFillSeries] Error converting coordinates for band fill ${index}:`, error);
          return;
        }
        
        // Validate coordinates are within reasonable bounds
        if (startX === null || endX === null || upperY === null || lowerY === null) {
          console.warn(`[TrendFillSeries] Invalid coordinates for band fill ${index}:`, { startX, endX, upperY, lowerY });
          return;
        }
        
        // Check if coordinates are within reasonable bounds with configurable tolerance
        const chartWidth = this._viewData.data.chartWidth || 800;
        const tolerance = this._viewData.options.coordinate_tolerance || 100;
        if (startX < -tolerance || endX < -tolerance || startX > chartWidth + tolerance || endX > chartWidth + tolerance) {
          if (this._viewData.options.debug_mode) {
            console.warn(`[TrendFillSeries] Coordinates significantly out of bounds for band fill ${index}:`, { startX, endX, chartWidth, tolerance });
          }
          return;
        }
        
        // Clamp coordinates to chart bounds for better rendering
        const clampedStartX = Math.max(0, Math.min(startX, chartWidth));
        const clampedEndX = Math.max(0, Math.min(endX, chartWidth));
        
        // Set fill style
        ctx.fillStyle = band.fillColor;
        ctx.globalAlpha = band.opacity;
        
        // Draw the filled area with clamped coordinates
        ctx.beginPath();
        ctx.moveTo(clampedStartX, upperY);
        ctx.lineTo(clampedEndX, upperY);
        ctx.lineTo(clampedEndX, lowerY);
        ctx.lineTo(clampedStartX, lowerY);
        ctx.closePath();
        ctx.fill();
        
        // Reset alpha
        ctx.globalAlpha = 1.0;
      });
      
      // Restore canvas state
      ctx.restore();
    });
  }

  private drawBaseLines(target: any) {
    const { baseLines } = this._viewData.data;
    
    if (baseLines.length === 0) return;

    target.useBitmapCoordinateSpace((scope: any) => {
      const ctx = scope.context;
      ctx.scale(scope.horizontalPixelRatio, scope.verticalPixelRatio);
      
      // Reset canvas state to prevent artifacts
      ctx.save();
      
      baseLines.forEach((baseLine, index) => {
        const timeScale = this._viewData.data.timeScale;
        const priceScale = this._viewData.data.priceScale;
        
        if (!timeScale || !priceScale) return;
        
        // Check if priceScale has the required methods
        if (typeof priceScale.priceToCoordinate !== 'function') {
          console.warn('[TrendFillSeries] priceScale.priceToCoordinate is not available');
          return;
        }
        
        // Safely convert coordinates with error handling
        let x: number | null = null;
        let y: number | null = null;
        
        try {
          x = timeScale.timeToCoordinate(baseLine.time);
          y = priceScale.priceToCoordinate(baseLine.price);
        } catch (error) {
          console.warn(`[TrendFillSeries] Error converting coordinates for base line ${index}:`, error);
          return;
        }
        
        // Debug: Log only when debug mode is enabled and limit frequency
        if (this._viewData.options.debug_mode && index < 2) { // Only log first 2 when debug is enabled
          console.log(`[TrendFillSeries] Base line ${index} coordinates:`, {
            time: baseLine.time,
            price: baseLine.price,
            x, y,
            chartWidth: this._viewData.data.chartWidth
          });
        }
        
        // Validate coordinates are within reasonable bounds
        if (x === null || y === null) {
          console.warn(`[TrendFillSeries] Invalid coordinates for base line ${index}:`, { x, y });
          return;
        }
        
        // Check if coordinates are within reasonable bounds with configurable tolerance
        const chartWidth = this._viewData.data.chartWidth || 800;
        const tolerance = this._viewData.options.coordinate_tolerance || 100;
        if (x < -tolerance || x > chartWidth + tolerance) {
          if (this._viewData.options.debug_mode) {
            console.warn(`[TrendFillSeries] X coordinate significantly out of bounds for base line ${index}:`, { x, chartWidth, tolerance });
          }
          return;
        }
        
        // Set line style
        ctx.strokeStyle = baseLine.color;
        ctx.lineWidth = baseLine.lineWidth;
        ctx.setLineDash(this.getLineDash(baseLine.lineStyle));
        
        // Draw horizontal line across the chart
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(chartWidth, y);
        ctx.stroke();
      });
      
      // Restore canvas state
      ctx.restore();
    });
  }

  private getLineDash(lineStyle: number): number[] {
    switch (lineStyle) {
      case 0: return []; // Solid
      case 1: return [5, 5]; // Dotted
      case 2: return [10, 5]; // Dashed
      default: return [];
    }
  }
}

// Trend fill primitive pane view
class TrendFillPrimitivePaneView implements IPrimitivePaneView {
  _source: TrendFillSeries;
  _data: TrendFillViewData;

  constructor(source: TrendFillSeries) {
    this._source = source;
    this._data = {
      data: {
        trendLines: [],
        bandFills: [],
        baseLines: [],
        timeScale: null,
        priceScale: null,
        chartWidth: 0,
      },
      options: this._source.getOptions(),
    };
  }

  update() {
    const chart = this._source.getChart();
    const timeScale = chart.timeScale();
    const chartElement = chart.chartElement();
    
    if (!timeScale || !chartElement) {
      return;
    }

    // Get the price scale from the dummy series (following the pattern from TradeRectanglePlugin)
    const dummySeries = this._source.getDummySeries();
    if (!dummySeries) {
      console.warn('[TrendFillSeries] No dummy series found');
      return;
    }

    // Verify the dummy series has the required methods
    if (typeof dummySeries.priceToCoordinate !== 'function') {
      console.warn('[TrendFillSeries] Dummy series does not have priceToCoordinate method');
      return;
    }

    console.log('[TrendFillSeries] Update successful - timeScale:', !!timeScale, 'priceScale:', !!dummySeries, 'chartWidth:', chartElement.clientWidth);

    // Update view data with better chart width handling
    this._data.data.timeScale = timeScale;
    this._data.data.priceScale = dummySeries;
    
    // Get chart width with fallback and validation
    const chartWidth = chartElement?.clientWidth || 800;
    if (chartWidth > 0) {
      this._data.data.chartWidth = chartWidth;
    } else {
      // Fallback to a reasonable default if clientWidth is not available
      this._data.data.chartWidth = 800;
      console.warn('[TrendFillSeries] Chart width not available, using fallback value');
    }

    // Get processed data from source
    const { trendLines, bandFills, baseLines } = this._source.getProcessedData();
    
    this._data.data.trendLines = trendLines;
    this._data.data.bandFills = bandFills;
    this._data.data.baseLines = baseLines;
  }

  renderer() {
    return new TrendFillPrimitivePaneRenderer(this._data);
  }
}

// Trend fill series class
export class TrendFillSeries implements ISeriesPrimitive<Time> {
  private chart: IChartApi;
  private dummySeries: ISeriesApi<'Line'>;
  private options: TrendFillOptions;
  private data: TrendFillData[] = [];
  private _paneViews: TrendFillPrimitivePaneView[];
  private paneId: number;

  // Processed data for rendering
  private trendLines: TrendLineSegment[] = [];
  private bandFills: BandFillData[] = [];
  private baseLines: BaseLineData[] = [];

  constructor(
    chart: IChartApi,
    options: TrendFillOptions = {
      uptrend_fill_color: '#4CAF50',
      downtrend_fill_color: '#F44336',
      fill_opacity: 0.3,
      upper_trend_line: {
        color: '#F44336',
        lineWidth: 2,
        lineStyle: 0,
        visible: true
      },
      lower_trend_line: {
        color: '#4CAF50',
        lineWidth: 2,
        lineStyle: 0,
        visible: true
      },
      base_line: {
        color: '#666666',
        lineWidth: 1,
        lineStyle: 1,
        visible: false
      },
      visible: true,
      debug_mode: false,
      coordinate_tolerance: 100
    },
    paneId: number = 0
  ) {
    this.chart = chart;
    this.options = { ...options };
    this.paneId = paneId;
    this._paneViews = [new TrendFillPrimitivePaneView(this)];
    
    // Create a dummy line series to attach the primitive to
    this.dummySeries = chart.addSeries(LineSeries, {
      color: 'transparent',
      lineWidth: 0 as any,
      visible: false,
      priceScaleId: 'right'
    }, this.paneId);

    // Add minimal dummy data to ensure the time scale is properly initialized
    const dummyData = [{
      time: Math.floor(Date.now() / 1000) as UTCTimestamp,
      value: 0
    }];
    this.dummySeries.setData(dummyData);

    // Attach the primitive to the dummy series for rendering
    this.dummySeries.attachPrimitive(this);
    
    // Wait for chart to be ready before initial update
    this.waitForChartReady();
  }
  
  private waitForChartReady(): void {
    const checkReady = () => {
      try {
        const timeScale = this.chart.timeScale();
        const dummySeries = this.dummySeries;
        
        if (timeScale && dummySeries && typeof dummySeries.priceToCoordinate === 'function') {
          console.log('[TrendFillSeries] Chart is ready, performing initial update');
          this.updateAllViews();
        } else {
          // Retry after a short delay
          setTimeout(checkReady, 50);
        }
      } catch (error) {
        // Chart not ready yet, retry
        setTimeout(checkReady, 50);
      }
    };
    
    // Start checking after a short delay
    setTimeout(checkReady, 100);
  }

  public setData(data: TrendFillData[]): void {
    this.data = data;
    this.processData();
    
    // Add a small delay to ensure chart is fully initialized
    setTimeout(() => {
      this.updateAllViews();
    }, 100);
  }

  public updateData(data: TrendFillData[]): void {
    this.setData(data);
  }

  private processData(): void {
    this.trendLines = [];
    this.bandFills = [];
    this.baseLines = [];

    if (!this.data || this.data.length === 0) return;

    console.log('[TrendFillSeries] Processing data:', this.data.length, 'points');
    console.log('[TrendFillSeries] Sample data point:', this.data[0]);

    // Sort data by time
    const sortedData = [...this.data].sort((a, b) => {
      const timeA = parseTime(a.time);
      const timeB = parseTime(b.time);
      return timeA - timeB;
    });

    let currentTrendStart: UTCTimestamp | null = null;
    let currentTrendDirection: number | null = null;
    let currentUpperTrend: number | null = null;
    let currentLowerTrend: number | null = null;

    // Process each data point
    for (let i = 0; i < sortedData.length; i++) {
      const item = sortedData[i];
      const time = parseTime(item.time);
      const baseLine = item.base_line !== undefined ? item.base_line : item.baseLine;
      const upperTrend = item.upper_trend !== undefined ? item.upper_trend : item.upperTrend;
      const lowerTrend = item.lower_trend !== undefined ? item.lower_trend : item.lowerTrend;
      const trendDirection = item.trend_direction !== undefined ? item.trend_direction : item.trendDirection;

      // Add base line if visible
      if (this.options.base_line.visible && baseLine !== null && baseLine !== undefined) {
        this.baseLines.push({
          time,
          price: baseLine,
          color: this.options.base_line.color,
          lineWidth: this.options.base_line.lineWidth,
          lineStyle: this.options.base_line.lineStyle
        });
      }

      // Process trend changes
      if (trendDirection !== null && trendDirection !== undefined) {
        const isUptrend = trendDirection > 0;
        
        // Check if trend direction changed
        if (currentTrendDirection !== null && currentTrendDirection !== trendDirection) {
          // End previous trend
          if (currentTrendStart !== null && currentUpperTrend !== null && currentLowerTrend !== null) {
            this.addTrendSegment(currentTrendStart, time, currentUpperTrend, currentLowerTrend, currentTrendDirection);
          }
          
          // Start new trend
          currentTrendStart = time;
          currentTrendDirection = trendDirection;
          currentUpperTrend = upperTrend;
          currentLowerTrend = lowerTrend;
        } else if (currentTrendStart === null) {
          // First trend
          currentTrendStart = time;
          currentTrendDirection = trendDirection;
          currentUpperTrend = upperTrend;
          currentLowerTrend = lowerTrend;
        } else {
          // Continue current trend
          currentUpperTrend = upperTrend;
          currentLowerTrend = lowerTrend;
        }
      }
    }

    // End final trend
    if (currentTrendStart !== null && currentUpperTrend !== null && currentLowerTrend !== null && currentTrendDirection !== null) {
      const finalTime = parseTime(sortedData[sortedData.length - 1].time);
      this.addTrendSegment(currentTrendStart, finalTime, currentUpperTrend, currentLowerTrend, currentTrendDirection);
    }

    console.log('[TrendFillSeries] Processed:', {
      trendLines: this.trendLines.length,
      bandFills: this.bandFills.length,
      baseLines: this.baseLines.length
    });
  }

  private addTrendSegment(startTime: UTCTimestamp, endTime: UTCTimestamp, upperTrend: number, lowerTrend: number, trendDirection: number): void {
    const isUptrend = trendDirection > 0;
    
    // Determine colors and styles based on trend direction
    const lineColor = isUptrend ? 
      this.options.lower_trend_line.color : 
      this.options.upper_trend_line.color;
    
    const lineWidth = isUptrend ? 
      this.options.lower_trend_line.lineWidth : 
      this.options.upper_trend_line.lineWidth;
    
    const lineStyle = isUptrend ? 
      this.options.lower_trend_line.lineStyle : 
      this.options.upper_trend_line.lineStyle;
    
    const fillColor = isUptrend ? 
      this.options.uptrend_fill_color : 
      this.options.downtrend_fill_color;

    // Add trend line segment
    if (this.options.upper_trend_line.visible || this.options.lower_trend_line.visible) {
      const trendLinePrice = isUptrend ? lowerTrend : upperTrend;
      
      this.trendLines.push({
        startTime,
        endTime,
        startPrice: trendLinePrice,
        endPrice: trendLinePrice,
        color: lineColor,
        lineWidth,
        lineStyle
      });
    }

    // Add band fill
    if (upperTrend !== null && lowerTrend !== null && upperTrend !== lowerTrend) {
      this.bandFills.push({
        startTime,
        endTime,
        upperPrice: upperTrend,
        lowerPrice: lowerTrend,
        fillColor,
        opacity: this.options.fill_opacity
      });
    }
  }

  public applyOptions(options: Partial<TrendFillOptions>): void {
    this.options = { ...this.options, ...options };
    this.processData();
    this.updateAllViews();
  }

  public setVisible(visible: boolean): void {
    this.options.visible = visible;
    this.processData();
    this.updateAllViews();
  }

  public destroy(): void {
    try {
      this.chart.removeSeries(this.dummySeries);
    } catch (error) {
      console.warn('Failed to remove trend fill series:', error);
    }
  }

  // Getter methods
  getOptions(): TrendFillOptions {
    return this.options;
  }

  getChart(): IChartApi {
    return this.chart;
  }

  getProcessedData() {
    return {
      trendLines: this.trendLines,
      bandFills: this.bandFills,
      baseLines: this.baseLines
    };
  }

  getDummySeries(): ISeriesApi<'Line'> {
    return this.dummySeries;
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
}

// Factory function to create trend fill series
export function createTrendFillSeriesPlugin(
  chart: IChartApi,
  config: {
    type: string;
    data: TrendFillData[];
    options?: TrendFillOptions;
    paneId?: number;
  }
): TrendFillSeries {
  return new TrendFillSeries(
    chart,
    config.options,
    config.paneId || 0
  );
}
