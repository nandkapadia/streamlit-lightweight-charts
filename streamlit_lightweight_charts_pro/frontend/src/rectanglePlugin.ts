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
    if (!this.chart) return;
    
    try {
      this.container = this.chart.chartElement();
      if (!this.container) return;

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
      if (!this.ctx) return;

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
        this.chart.timeScale().subscribeVisibleTimeRangeChange(() => {
          if (!this.isDisposed && this.isChartValid()) {
            this.scheduleRedraw();
          }
        });

        this.chart.subscribeCrosshairMove(() => {
          if (!this.isDisposed && this.isChartValid()) {
            this.scheduleRedraw();
          }
        });
      } catch (e) {
        // Silent error handling
      }

      // Initial draw
      this.scheduleRedraw();
    } catch (error) {
      // Silent error handling
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
    this.animationFrameId = requestAnimationFrame(() => {
      this.drawRectangles();
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

  private drawRectangles() {
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
          const height = Math.abs(price2Pixel - price1Pixel);

          // FIX: Invert Y coordinates to match chart coordinate system
          // In financial charts, higher prices should be at the top (lower Y coordinates)
          const invertedY = this.canvas.height - Math.max(price1Pixel, price2Pixel);
          const invertedHeight = height; // Height remains the same

          // Validate rectangle dimensions - be more lenient with bounds checking
          if (width <= 0 || invertedHeight <= 0) {
            continue;
          }

          // Check if rectangle is completely outside canvas bounds
          if (x + width < 0 || invertedY + invertedHeight < 0 || x > this.canvas.width || invertedY > this.canvas.height) {
            continue;
          }

          // Clamp coordinates to canvas bounds
          const clampedX = Math.max(0, Math.min(x, this.canvas.width - width));
          const clampedY = Math.max(0, Math.min(invertedY, this.canvas.height - invertedHeight));
          const clampedWidth = Math.min(width, this.canvas.width - clampedX);
          const clampedHeight = Math.min(invertedHeight, this.canvas.height - clampedY);

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