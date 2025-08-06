import { IChartApi, UTCTimestamp } from 'lightweight-charts';

export interface RectangleConfig {
  time1: UTCTimestamp;
  price1: number;
  time2: UTCTimestamp;
  price2: number;
  fillColor: string;
  borderColor: string;
  borderWidth: number;
  borderStyle: 'solid' | 'dashed' | 'dotted';
  opacity: number;
  priceScaleId?: string;
}

export class RectangleOverlayPlugin {
  private rectangles: RectangleConfig[] = [];
  private chart: IChartApi | null = null;
  private series: any = null;
  private canvas: HTMLCanvasElement | null = null;
  private ctx: CanvasRenderingContext2D | null = null;
  private container: HTMLElement | null = null;
  private resizeObserver: ResizeObserver | null = null;
  private isDisposed: boolean = false;
  private animationFrameId: number | null = null;

  constructor(rectangles?: RectangleConfig[]) {
    if (rectangles) this.rectangles = rectangles;
  }

  setChart(chart: IChartApi, series?: any) {
    this.chart = chart;
    this.series = series;
    this.init();
  }

  private init() {
    if (!this.chart) {
      return;
    }
    
    try {
      this.container = this.chart.chartElement();
      if (!this.container) {
        return;
      }

      // Create canvas overlay
      this.canvas = document.createElement('canvas');
      this.canvas.style.position = 'absolute';
      this.canvas.style.top = '0';
      this.canvas.style.left = '0';
      this.canvas.style.pointerEvents = 'none';
      this.canvas.style.zIndex = '1';
      
      this.container.style.position = 'relative';
      this.container.appendChild(this.canvas);

      // Get canvas context
      this.ctx = this.canvas.getContext('2d');
      if (!this.ctx) {
        return;
      }

      // Set initial canvas size
      this.resizeCanvas();

      // Listen for chart resize events
      this.resizeObserver = new ResizeObserver(() => {
        if (!this.isDisposed && this.isChartValid()) {
          this.resizeCanvas();
          this.scheduleRedraw();
        }
      });
      this.resizeObserver.observe(this.container);

      // Listen for chart updates
      try {
        // Listen for time scale changes (panning, zooming)
        this.chart.timeScale().subscribeVisibleTimeRangeChange(() => {
          if (!this.isDisposed && this.isChartValid()) {
            this.scheduleRedraw();
          }
        });

        // Listen for price scale changes (using time scale as proxy since price scale doesn't have direct events)
        // The time scale changes will also trigger when price scale changes due to zooming

        // Listen for crosshair movement
        this.chart.subscribeCrosshairMove(() => {
          if (!this.isDisposed && this.isChartValid()) {
            this.scheduleRedraw();
          }
        });

        // Listen for chart resize
        this.chart.subscribeClick(() => {
          // Redraw on any chart interaction
          if (!this.isDisposed && this.isChartValid()) {
            this.scheduleRedraw();
          }
        });
      } catch (e) {
        // Error setting up chart event listeners
      }

      // Initial draw
      this.scheduleRedraw();
    } catch (error) {
      // Initialization error
    }
  }

  private isChartValid(): boolean {
    if (!this.chart) return false;
    
    try {
      // Check if chart element exists and is connected
      const chartElement = this.chart.chartElement();
      if (!chartElement || !chartElement.parentNode || !chartElement.isConnected) {
        return false;
      }

      // Try to access timeScale to check if chart is still valid
      this.chart.timeScale();
      return true;
    } catch (e) {
      return false;
    }
  }

  private scheduleRedraw() {
    if (this.animationFrameId) {
      cancelAnimationFrame(this.animationFrameId);
    }
    this.animationFrameId = requestAnimationFrame(async () => {
      await this.drawRectangles();
    });
  }

  // Function to get chart dimensions using requestAnimationFrame approach
  private getChartDimensions(): Promise<{
    timeScalePositionAndSize: { x: number; y: number; height: number; width: number };
    priceScalePositionAndSize: { x: number; y: number; height: number; width: number };
    containerDimensions: { width: number; height: number };
  }> {
    return new Promise((resolve) => {
      // Run inside a RequestAnimationFrame so that the chart has a chance to 
      // render once before querying the dimensions.
      requestAnimationFrame(() => {
        if (!this.container || !this.chart) {
          resolve({
            timeScalePositionAndSize: { x: 0, y: 0, height: 35, width: 0 },
            priceScalePositionAndSize: { x: 0, y: 0, height: 0, width: 70 },
            containerDimensions: { width: 0, height: 0 }
          });
          return;
        }
        
        // Check if chart is disposed
        try {
          this.chart.chartElement()
        } catch (error) {
          console.warn('Chart is disposed in rectangle plugin, cannot get dimensions');
          resolve({
            timeScalePositionAndSize: { x: 0, y: 0, height: 35, width: 0 },
            priceScalePositionAndSize: { x: 0, y: 0, height: 0, width: 70 },
            containerDimensions: { width: 0, height: 0 }
          });
          return;
        }

        const containerElement = this.container!;
        const containerDimensions = containerElement.getBoundingClientRect();

        // chart is the IChartAPI reference returned by LightweightCharts.createChart
        const timeScale = this.chart!.timeScale();
        const timeScaleWidth = timeScale.width();
        const timeScaleHeight = timeScale.height();

        // mainSeries is the ISeriesAPI reference returned when adding data
        // for example with: chart.addLineSeries(...)
        let priceScaleWidth = 70; // Default fallback
        if (this.series) {
          try {
            const priceScale = this.series.priceScale();
            priceScaleWidth = priceScale.width();
          } catch (error) {
            console.debug('Could not get price scale width from main series, using default:', error);
            // Fallback to default price scale
            try {
              const priceScale = this.chart!.priceScale('right');
              priceScaleWidth = priceScale ? priceScale.width() : 70;
            } catch (fallbackError) {
              console.debug('Could not get price scale width from default scale, using fallback:', fallbackError);
            }
          }
        } else {
          // Fallback to default price scale if no main series provided
          try {
            const priceScale = this.chart!.priceScale('right');
            priceScaleWidth = priceScale ? priceScale.width() : 70;
          } catch (error) {
            console.debug('Could not get price scale width, using fallback:', error);
          }
        }

        const priceScalePositionAndSize = {
          x: timeScaleWidth,
          y: 0,
          height: containerDimensions.height - timeScaleHeight,
          width: priceScaleWidth,
        };

        const timeScalePositionAndSize = {
          x: 0,
          y: containerDimensions.height - timeScaleHeight,
          height: timeScaleHeight,
          width: timeScaleWidth,
        };

        // Only log in development mode to reduce noise
        if (process.env.NODE_ENV === 'development') {
          console.log({ timeScalePositionAndSize, priceScalePositionAndSize });
        }
        resolve({ timeScalePositionAndSize, priceScalePositionAndSize, containerDimensions });
      });
    });
  }

  private resizeCanvas() {
    if (!this.canvas || !this.container) return;
    
    try {
      const rect = this.container.getBoundingClientRect();
      if (rect.width > 0 && rect.height > 0) {
        this.canvas.width = rect.width;
        this.canvas.height = rect.height;
        this.canvas.style.width = `${rect.width}px`;
        this.canvas.style.height = `${rect.height}px`;
      }
    } catch (error) {
      // Silent error handling
    }
  }

  private async getChartDrawingArea(): Promise<{ left: number; top: number; right: number; bottom: number } | null> {
    try {
      if (!this.chart || !this.canvas || !this.series) return null;

      // Get chart dimensions using the new requestAnimationFrame approach
      await this.getChartDimensions();
      
      // Get the chart's drawing area bounds
      const timeScale = this.chart.timeScale();
      
      // Get the price scale for the specific series
      let priceScale = null;
      try {
        // Try to get the price scale from the series first
        priceScale = this.series.priceScale();
      } catch (error) {
        // Fallback to default price scale
        priceScale = this.chart.priceScale('right');
      }
      
      if (!timeScale || !priceScale) return null;

      // Get the chart's logical bounds
      const logicalBounds = timeScale.getVisibleLogicalRange();
      if (!logicalBounds) return null;

      // Convert logical bounds to pixel coordinates
      const left = timeScale.logicalToCoordinate(logicalBounds.from);
      const right = timeScale.logicalToCoordinate(logicalBounds.to);
      
      if (left === null || right === null) return null;

      // Get price scale bounds for the specific series
      const priceRange = priceScale.getVisibleRange();
      if (!priceRange) return null;

      // Use the series priceToCoordinate method instead of priceScale
      const top = this.series.priceToCoordinate(priceRange.to); // Higher price = lower Y
      const bottom = this.series.priceToCoordinate(priceRange.from); // Lower price = higher Y
      
      if (top === null || bottom === null) return null;

      // Calculate the actual chart drawing area bounds
      // The chart drawing area excludes axes, labels, and other UI elements
      let paneTop = top;
      let paneBottom = bottom;
      
      try {
        // Get the chart's actual drawing area
        const chartElement = this.chart.chartElement();
        if (chartElement) {
          // Get the chart's internal drawing area
          const chartRect = chartElement.getBoundingClientRect();
          const canvasRect = this.canvas.getBoundingClientRect();
          
          // Calculate the relative position of the chart within the canvas
          const chartTop = chartRect.top - canvasRect.top;
          const chartBottom = chartRect.bottom - canvasRect.top;
          
          // Use the chart's actual bounds, but ensure we stay within the price scale bounds
          paneTop = Math.max(top, chartTop);
          paneBottom = Math.min(bottom, chartBottom);
          
        } else {
          // Fallback to price scale bounds
          paneTop = top;
          paneBottom = bottom;
        }
      } catch (error) {
        // If we can't get chart bounds, use the price scale bounds
        paneTop = top;
        paneBottom = bottom;
      }

      // Calculate the actual chart drawing area
      // The time scale width represents the actual chart area width
      const chartLeft = left;
      const chartRight = right;

      const chartArea = {
        left: chartLeft,
        top: Math.max(paneTop, top),
        right: chartRight,
        bottom: Math.min(paneBottom, bottom)
      };
      
      return chartArea;
    } catch (error) {
      return null;
    }
  }

  // Coordinate conversion methods following the lightweight-chart-plugin pattern
  private timeToCoordinate(time: UTCTimestamp): number | null {
    try {
      if (!this.chart) return null;
      const timeScale = this.chart.timeScale();
      const coordinate = timeScale.timeToCoordinate(time);
      return coordinate !== null ? coordinate : null;
    } catch (e) {
      // Silent error handling
      return null;
    }
  }

  private priceToCoordinate(price: number, priceScaleId?: string): number | null {
    try {
      if (!this.chart) return null;
      
      // If a specific price scale is requested, use it
      if (priceScaleId) {
        const priceScale = this.chart.priceScale(priceScaleId);
        if (priceScale && typeof (priceScale as any).priceToCoordinate === 'function') {
          const coordinate = (priceScale as any).priceToCoordinate(price);
          return coordinate !== null ? coordinate : null;
        }
      }
      
      // Fallback to series if available
      if (this.series && typeof this.series.priceToCoordinate === 'function') {
        const coordinate = this.series.priceToCoordinate(price);
        return coordinate !== null ? coordinate : null;
      }
      
      // Final fallback to default price scale
      const defaultPriceScale = this.chart.priceScale('right');
      if (defaultPriceScale && typeof (defaultPriceScale as any).priceToCoordinate === 'function') {
        const coordinate = (defaultPriceScale as any).priceToCoordinate(price);
        return coordinate !== null ? coordinate : null;
      }
      
      return null;
    } catch (e) {
      // Silent error handling
      return null;
    }
  }

  private async drawRectangles() {
    if (this.isDisposed || !this.ctx || !this.canvas || !this.chart) {
      return;
    }

    try {
      if (!this.isChartValid()) {
        this.isDisposed = true;
        return;
      }

      // Check if we have a series for price conversion
      if (!this.series) {
        return;
      }

      // Clear canvas
      this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

      // Get chart drawing area bounds (excluding axes and labels) - now async
      const chartArea = await this.getChartDrawingArea();
      if (!chartArea) {
        return;
      }

      // Draw each rectangle
      for (let index = 0; index < this.rectangles.length; index++) {
        const rect = this.rectangles[index];
        try {
          // Convert coordinates using the lightweight-chart-plugin pattern
          const time1Pixel = this.timeToCoordinate(rect.time1);
          const time2Pixel = this.timeToCoordinate(rect.time2);
          const price1Pixel = this.priceToCoordinate(rect.price1, rect.priceScaleId);
          const price2Pixel = this.priceToCoordinate(rect.price2, rect.priceScaleId);


          


          // Validate coordinates
          if (
            time1Pixel === null || time2Pixel === null || 
            price1Pixel === null || price2Pixel === null ||
            isNaN(time1Pixel) || isNaN(time2Pixel) || 
            isNaN(price1Pixel) || isNaN(price2Pixel)
          ) {
            continue;
          }

          // Calculate rectangle dimensions with proper bounds checking
          const x = Math.min(time1Pixel, time2Pixel);
          const width = Math.abs(time2Pixel - time1Pixel);
          const y = Math.min(price1Pixel, price2Pixel); // Lower price = higher Y coordinate
          const rectHeight = Math.abs(price2Pixel - price1Pixel);

          // Validate rectangle dimensions
          if (width <= 0 || rectHeight <= 0) {
            continue;
          }

          // Check if rectangle is completely outside chart drawing area
          if (x + width < chartArea.left || y + rectHeight < chartArea.top || 
              x > chartArea.right || y > chartArea.bottom) {
            continue;
          }

          // Clamp coordinates to chart drawing area bounds
          // Handle negative coordinates by clipping from the left edge
          let clampedX = x;
          let clampedWidth = width;
          
          // If rectangle starts before the left edge, clip it
          if (x < chartArea.left) {
            const clipAmount = chartArea.left - x;
            clampedX = chartArea.left;
            clampedWidth = Math.max(0, width - clipAmount);
          }
          
          // If rectangle extends beyond the right edge, clip it
          if (x + width > chartArea.right) {
            clampedWidth = Math.max(0, chartArea.right - clampedX);
          }
          
          // Clamp Y coordinates
          const clampedY = Math.max(chartArea.top, Math.min(y, chartArea.bottom));
          const maxHeight = chartArea.bottom - clampedY;
          const clampedHeight = Math.min(rectHeight, maxHeight);

          // Draw rectangle
          this.ctx.save();
          

          
          // Set fill style
          this.ctx.fillStyle = rect.fillColor;
          this.ctx.globalAlpha = rect.opacity || 0.2;
          this.ctx.fillRect(clampedX, clampedY, clampedWidth, clampedHeight);

          // Set border style
          if (rect.borderWidth > 0) {
            this.ctx.strokeStyle = rect.borderColor;
            this.ctx.lineWidth = rect.borderWidth;
            this.ctx.globalAlpha = 1.0;
            
            // Set line style
            if (rect.borderStyle === 'dashed') {
              this.ctx.setLineDash([5, 5]);
            } else if (rect.borderStyle === 'dotted') {
              this.ctx.setLineDash([2, 2]);
            } else {
              this.ctx.setLineDash([]);
            }
            
            this.ctx.strokeRect(clampedX, clampedY, clampedWidth, clampedHeight);
          }

          this.ctx.restore();
        } catch (rectError) {
          continue;
        }
      }
    } catch (error) {
      // Silent error handling
    }
  }

  setRectangles(rects: RectangleConfig[]) {
    this.rectangles = rects;
    this.scheduleRedraw();
  }

  addRectangle(rect: RectangleConfig) {
    this.rectangles.push(rect);
    this.scheduleRedraw();
  }

  clearRectangles() {
    this.rectangles = [];
    this.scheduleRedraw();
  }

  removeRectangle(index: number) {
    this.rectangles.splice(index, 1);
    this.scheduleRedraw();
  }

  destroy() {
    this.isDisposed = true;
    
    if (this.animationFrameId) {
      cancelAnimationFrame(this.animationFrameId);
      this.animationFrameId = null;
    }
    
    if (this.resizeObserver) {
      this.resizeObserver.disconnect();
      this.resizeObserver = null;
    }
    
    if (this.canvas && this.container) {
      try {
        this.container.removeChild(this.canvas);
      } catch (e) {
        // Canvas already removed
      }
    }
    
    this.rectangles = [];
    this.canvas = null;
    this.ctx = null;
    this.container = null;
    this.chart = null;
    this.series = null;
  }
}

export function registerRectanglePlugin(chart: IChartApi, series?: any, rectangles?: RectangleConfig[]): RectangleOverlayPlugin {
  const plugin = new RectangleOverlayPlugin(rectangles);
  plugin.setChart(chart, series);
  return plugin;
} 