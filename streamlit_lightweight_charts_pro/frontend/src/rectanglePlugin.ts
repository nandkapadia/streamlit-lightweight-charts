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

      // Listen for chart updates
      this.chart.timeScale().subscribeVisibleTimeRangeChange(() => {
        if (!this.isDisposed) {
          this.scheduleRedraw();
        }
      });

      // Initial draw
      this.scheduleRedraw();
    } catch (error) {
      console.warn('[RectanglePlugin] Initialization error:', error);
    }
  }

  private resizeCanvas() {
    if (!this.canvas || !this.container) return;
    
    const rect = this.container.getBoundingClientRect();
    if (rect.width > 0 && rect.height > 0) {
      this.canvas.width = rect.width;
      this.canvas.height = rect.height;
      this.canvas.style.width = `${rect.width}px`;
      this.canvas.style.height = `${rect.height}px`;
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

  private timeToCoordinate(time: UTCTimestamp): number | null {
    try {
      if (!this.chart) return null;
      const timeScale = this.chart.timeScale();
      return timeScale.timeToCoordinate(time);
    } catch (e) {
      return null;
    }
  }

  private priceToCoordinate(price: number): number | null {
    try {
      if (!this.series) return null;
      return this.series.priceToCoordinate(price);
    } catch (e) {
      return null;
    }
  }

  private drawRectangles() {
    if (this.isDisposed || !this.ctx || !this.canvas || !this.chart || !this.series) return;

    try {
      // Clear canvas
      this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

      // Get chart dimensions for proper clipping
      const leftPriceScale = this.chart.priceScale('left');
      const rightPriceScale = this.chart.priceScale('right');
      
      // Calculate clipping boundaries
      const leftClip = leftPriceScale ? leftPriceScale.width() : 0;
      const rightClip = rightPriceScale ? this.canvas.width - rightPriceScale.width() : this.canvas.width;

      // Draw each rectangle
      for (const rect of this.rectangles) {
        // Convert coordinates
        const time1Pixel = this.timeToCoordinate(rect.time1);
        const time2Pixel = this.timeToCoordinate(rect.time2);
        const price1Pixel = this.priceToCoordinate(rect.price1);
        const price2Pixel = this.priceToCoordinate(rect.price2);

        if (time1Pixel === null || time2Pixel === null || price1Pixel === null || price2Pixel === null) {
          continue;
        }

        // Calculate rectangle dimensions
        let x = Math.min(time1Pixel, time2Pixel);
        let width = Math.abs(time2Pixel - time1Pixel);
        const y = Math.min(price1Pixel, price2Pixel);
        const height = Math.abs(price2Pixel - price1Pixel);

        if (width <= 0 || height <= 0) continue;

        // Draw rectangle with canvas clipping
        this.ctx.save();
        
        // Set up clipping region
        this.ctx.beginPath();
        this.ctx.rect(leftClip, 0, rightClip - leftClip, this.canvas.height);
        this.ctx.clip();
        
        // Set fill style
        this.ctx.fillStyle = rect.fillColor;
        this.ctx.globalAlpha = rect.opacity || 0.2;
        this.ctx.fillRect(x, y, width, height);

        // Set border style
        if (rect.borderWidth > 0) {
          this.ctx.strokeStyle = rect.borderColor;
          this.ctx.lineWidth = rect.borderWidth;
          this.ctx.globalAlpha = 1.0;
          
          if (rect.borderStyle === 'dashed') {
            this.ctx.setLineDash([5, 5]);
          } else if (rect.borderStyle === 'dotted') {
            this.ctx.setLineDash([2, 2]);
          } else {
            this.ctx.setLineDash([]);
          }
          
          this.ctx.strokeRect(x, y, width, height);
        }

        this.ctx.restore();
      }
    } catch (error) {
      console.warn('[RectanglePlugin] Error drawing rectangles:', error);
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