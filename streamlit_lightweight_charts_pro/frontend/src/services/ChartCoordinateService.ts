/**
 * Centralized service for managing chart coordinate calculations
 * Provides consistent positioning across all chart features
 */

import { IChartApi, ISeriesApi } from 'lightweight-charts';
import {
  ChartCoordinates,
  PaneCoordinates,
  LegendCoordinates,
  ElementPosition,
  CoordinateOptions,
  CoordinateCacheEntry,
  BoundingBox,
  ScaleDimensions,
  ContainerDimensions
} from '../types/coordinates';
import {
  validateChartCoordinates,
  sanitizeCoordinates,
  createBoundingBox,
  areCoordinatesStale,
  logValidationResult
} from '../utils/coordinateValidation';
import {
  DIMENSIONS,
  FALLBACKS,
  MARGINS,
  TIMING,
  Z_INDEX,
  getFallback,
  getMargins
} from '../config/positioningConfig';

/**
 * Singleton service for chart coordinate management
 */
export class ChartCoordinateService {
  private static instance: ChartCoordinateService;
  private coordinateCache = new Map<string, CoordinateCacheEntry>();
  private chartRegistry = new Map<string, IChartApi>();
  private updateCallbacks = new Map<string, Set<() => void>>();
  
  /**
   * Get singleton instance
   */
  static getInstance(): ChartCoordinateService {
    if (!this.instance) {
      this.instance = new ChartCoordinateService();
    }
    return this.instance;
  }
  
  private constructor() {
    // Private constructor for singleton
    this.startCacheCleanup();
  }
  
  /**
   * Register a chart for coordinate tracking
   */
  registerChart(chartId: string, chart: IChartApi): void {
    this.chartRegistry.set(chartId, chart);
    this.invalidateCache(chartId);
  }
  
  /**
   * Unregister a chart
   */
  unregisterChart(chartId: string): void {
    this.chartRegistry.delete(chartId);
    this.coordinateCache.delete(chartId);
    this.updateCallbacks.delete(chartId);
  }
  
  /**
   * Get coordinates for a chart with caching and validation
   */
  async getCoordinates(
    chart: IChartApi,
    container: HTMLElement,
    options: CoordinateOptions = {}
  ): Promise<ChartCoordinates> {
    const {
      includeMargins = true,
      useCache = true,
      validateResult = true,
      fallbackOnError = true
    } = options;
    
    // Generate cache key
    const cacheKey = this.generateCacheKey(chart, container);
    
    // Check cache if enabled
    if (useCache) {
      const cached = this.coordinateCache.get(cacheKey);
      if (cached && !areCoordinatesStale(cached, TIMING.cacheExpiration)) {
        return cached;
      }
    }
    
    try {
      // Calculate coordinates
      const coordinates = await this.calculateCoordinates(chart, container, includeMargins);
      
      // Validate if requested
      if (validateResult) {
        const validation = validateChartCoordinates(coordinates);
        logValidationResult(validation, 'ChartCoordinateService');
        
        if (!validation.isValid && fallbackOnError) {
          return sanitizeCoordinates(coordinates);
        }
      }
      
      // Cache the result
      const cacheEntry: CoordinateCacheEntry = {
        ...coordinates,
        cacheKey,
        expiresAt: Date.now() + TIMING.cacheExpiration
      };
      this.coordinateCache.set(cacheKey, cacheEntry);
      
      // Notify listeners
      this.notifyUpdateCallbacks(cacheKey);
      
      return coordinates;
      
    } catch (error) {
      console.error('Error calculating coordinates:', error);
      
      if (fallbackOnError) {
        return sanitizeCoordinates({});
      }
      
      throw error;
    }
  }
  
  /**
   * Get coordinates for a specific pane
   */
  getPaneCoordinates(chart: IChartApi, paneId: number): PaneCoordinates | null {
    try {
      // Get pane size from chart
      const paneSize = chart.paneSize(paneId);
      if (!paneSize) return null;
      
      // Calculate cumulative offset for this pane
      let offsetY = 0;
      for (let i = 0; i < paneId; i++) {
        const size = chart.paneSize(i);
        if (size) {
          offsetY += size.height;
        }
      }
      
      // Get chart element for price scale width
      const chartElement = chart.chartElement();
      const priceScaleWidth = this.getPriceScaleWidth(chart);
      const timeScaleHeight = this.getTimeScaleHeight(chart);
      
      // Calculate bounds
      const bounds = createBoundingBox(
        0,
        offsetY,
        paneSize.width || getFallback('paneWidth'),
        paneSize.height
      );
      
      // Calculate content area (excluding scales)
      const contentArea = createBoundingBox(
        priceScaleWidth,
        offsetY,
        bounds.width - priceScaleWidth,
        paneSize.height - (paneId === 0 ? 0 : timeScaleHeight)
      );
      
      // Get margins
      const margins = getMargins('pane');
      
      return {
        id: paneId,
        index: paneId,
        isMainPane: paneId === 0,
        bounds,
        contentArea,
        margins
      };
      
    } catch (error) {
      console.error(`Error getting pane coordinates for pane ${paneId}:`, error);
      return null;
    }
  }
  
  /**
   * Calculate legend position within a pane
   */
  getLegendPosition(
    chart: IChartApi,
    paneId: number,
    position: ElementPosition
  ): LegendCoordinates | null {
    const paneCoords = this.getPaneCoordinates(chart, paneId);
    if (!paneCoords) return null;
    
    const margins = getMargins('legend');
    const legendDimensions = DIMENSIONS.legend;
    
    let top = 0;
    let left = 0;
    let right: number | undefined;
    let bottom: number | undefined;
    
    // Calculate position based on alignment
    switch (position) {
      case 'top-left':
        top = paneCoords.contentArea.top + margins.top;
        left = paneCoords.contentArea.left + margins.left;
        break;
        
      case 'top-right':
        top = paneCoords.contentArea.top + margins.top;
        right = margins.right;
        break;
        
      case 'bottom-left':
        bottom = paneCoords.contentArea.bottom - legendDimensions.defaultHeight - margins.bottom;
        left = paneCoords.contentArea.left + margins.left;
        break;
        
      case 'bottom-right':
        bottom = paneCoords.contentArea.bottom - legendDimensions.defaultHeight - margins.bottom;
        right = margins.right;
        break;
        
      case 'center':
        top = paneCoords.contentArea.top + 
              (paneCoords.contentArea.height - legendDimensions.defaultHeight) / 2;
        left = paneCoords.contentArea.left + 
               (paneCoords.contentArea.width - legendDimensions.defaultWidth) / 2;
        break;
    }
    
    // Convert bottom to top if needed
    if (bottom !== undefined && top === 0) {
      top = bottom;
      bottom = undefined;
    }
    
    return {
      top,
      left,
      right,
      bottom,
      width: legendDimensions.defaultWidth,
      height: legendDimensions.defaultHeight,
      zIndex: Z_INDEX.legend
    };
  }
  
  /**
   * Subscribe to coordinate updates
   */
  onCoordinateUpdate(chartId: string, callback: () => void): () => void {
    if (!this.updateCallbacks.has(chartId)) {
      this.updateCallbacks.set(chartId, new Set());
    }
    
    this.updateCallbacks.get(chartId)!.add(callback);
    
    // Return unsubscribe function
    return () => {
      const callbacks = this.updateCallbacks.get(chartId);
      if (callbacks) {
        callbacks.delete(callback);
      }
    };
  }
  
  /**
   * Invalidate cache for a specific chart
   */
  invalidateCache(chartId?: string): void {
    if (chartId) {
      // Remove specific chart entries
      const keysToDelete: string[] = [];
      this.coordinateCache.forEach((entry, key) => {
        if (key.includes(chartId)) {
          keysToDelete.push(key);
        }
      });
      keysToDelete.forEach(key => this.coordinateCache.delete(key));
    } else {
      // Clear all cache
      this.coordinateCache.clear();
    }
  }
  
  /**
   * Calculate coordinates for a chart
   */
  private async calculateCoordinates(
    chart: IChartApi,
    container: HTMLElement,
    includeMargins: boolean
  ): Promise<ChartCoordinates> {
    return new Promise((resolve) => {
      // Use requestAnimationFrame for better performance
      requestAnimationFrame(() => {
        try {
          // Get container dimensions
          const containerDimensions = this.getContainerDimensions(container);
          
          // Get scale dimensions
          const timeScale = this.getTimeScaleDimensions(chart, containerDimensions);
          const priceScaleLeft = this.getPriceScaleDimensions(chart, 'left', containerDimensions);
          const priceScaleRight = this.getPriceScaleDimensions(chart, 'right', containerDimensions);
          
          // Get all panes
          const panes = this.getAllPaneCoordinates(chart);
          
          // Calculate content area
          const contentArea = this.calculateContentArea(
            containerDimensions,
            timeScale,
            priceScaleLeft,
            includeMargins
          );
          
          const coordinates: ChartCoordinates = {
            container: containerDimensions,
            timeScale,
            priceScaleLeft,
            priceScaleRight,
            panes,
            contentArea,
            timestamp: Date.now(),
            isValid: true
          };
          
          resolve(coordinates);
          
        } catch (error) {
          console.error('Error in calculateCoordinates:', error);
          resolve(sanitizeCoordinates({}));
        }
      });
    });
  }
  
  /**
   * Get container dimensions
   */
  private getContainerDimensions(container: HTMLElement): ContainerDimensions {
    const rect = container.getBoundingClientRect();
    return {
      width: rect.width || container.offsetWidth || getFallback('containerWidth'),
      height: rect.height || container.offsetHeight || getFallback('containerHeight'),
      offsetTop: container.offsetTop || 0,
      offsetLeft: container.offsetLeft || 0
    };
  }
  
  /**
   * Get time scale dimensions
   */
  private getTimeScaleDimensions(chart: IChartApi, container: ContainerDimensions): ScaleDimensions {
    try {
      const timeScale = chart.timeScale();
      const height = timeScale.height() || getFallback('timeScaleHeight');
      const width = timeScale.width() || container.width;
      
      return {
        x: 0,
        y: container.height - height,
        width,
        height
      };
    } catch {
      return {
        x: 0,
        y: container.height - getFallback('timeScaleHeight'),
        width: container.width,
        height: getFallback('timeScaleHeight')
      };
    }
  }
  
  /**
   * Get price scale dimensions
   */
  private getPriceScaleDimensions(
    chart: IChartApi,
    side: 'left' | 'right',
    container: ContainerDimensions
  ): ScaleDimensions {
    try {
      const priceScale = chart.priceScale(side);
      const width = priceScale.width() || 
                   (side === 'left' ? getFallback('priceScaleWidth') : 0);
      
      return {
        x: side === 'left' ? 0 : container.width - width,
        y: 0,
        width,
        height: container.height - getFallback('timeScaleHeight')
      };
    } catch {
      const defaultWidth = side === 'left' ? getFallback('priceScaleWidth') : 0;
      return {
        x: side === 'left' ? 0 : container.width - defaultWidth,
        y: 0,
        width: defaultWidth,
        height: container.height - getFallback('timeScaleHeight')
      };
    }
  }
  
  /**
   * Get all pane coordinates
   */
  private getAllPaneCoordinates(chart: IChartApi): PaneCoordinates[] {
    const panes: PaneCoordinates[] = [];
    let paneIndex = 0;
    let currentY = 0;
    
    // Try to get panes until we hit an invalid one
    while (paneIndex < 10) { // Safety limit
      try {
        const paneSize = chart.paneSize(paneIndex);
        if (!paneSize) break;
        
        const paneCoords = this.getPaneCoordinates(chart, paneIndex);
        if (paneCoords) {
          panes.push(paneCoords);
        }
        
        currentY += paneSize.height;
        paneIndex++;
      } catch {
        break;
      }
    }
    
    // Ensure we have at least one pane
    if (panes.length === 0) {
      panes.push({
        id: 0,
        index: 0,
        isMainPane: true,
        bounds: createBoundingBox(0, 0, getFallback('paneWidth'), getFallback('paneHeight')),
        contentArea: createBoundingBox(
          getFallback('priceScaleWidth'),
          0,
          getFallback('paneWidth') - getFallback('priceScaleWidth'),
          getFallback('paneHeight') - getFallback('timeScaleHeight')
        ),
        margins: getMargins('pane')
      });
    }
    
    return panes;
  }
  
  /**
   * Calculate content area
   */
  private calculateContentArea(
    container: ContainerDimensions,
    timeScale: ScaleDimensions,
    priceScaleLeft: ScaleDimensions,
    includeMargins: boolean
  ): BoundingBox {
    const margins = includeMargins ? getMargins('content') : { top: 0, right: 0, bottom: 0, left: 0 };
    
    const x = priceScaleLeft.width + margins.left;
    const y = margins.top;
    const width = container.width - priceScaleLeft.width - margins.left - margins.right;
    const height = container.height - timeScale.height - margins.top - margins.bottom;
    
    return createBoundingBox(x, y, width, height);
  }
  
  /**
   * Get price scale width helper
   */
  private getPriceScaleWidth(chart: IChartApi, side: 'left' | 'right' = 'left'): number {
    try {
      const priceScale = chart.priceScale(side);
      return priceScale.width() || (side === 'left' ? getFallback('priceScaleWidth') : 0);
    } catch {
      return side === 'left' ? getFallback('priceScaleWidth') : 0;
    }
  }
  
  /**
   * Get time scale height helper
   */
  private getTimeScaleHeight(chart: IChartApi): number {
    try {
      const timeScale = chart.timeScale();
      return timeScale.height() || getFallback('timeScaleHeight');
    } catch {
      return getFallback('timeScaleHeight');
    }
  }
  
  /**
   * Generate cache key
   */
  private generateCacheKey(chart: IChartApi, container: HTMLElement): string {
    const chartId = chart?.chartElement?.()?.id || 'unknown';
    const containerId = container?.id || 'unknown';
    return `${chartId}-${containerId}`;
  }
  
  /**
   * Notify update callbacks
   */
  private notifyUpdateCallbacks(cacheKey: string): void {
    const chartId = cacheKey.split('-')[0];
    const callbacks = this.updateCallbacks.get(chartId);
    
    if (callbacks) {
      callbacks.forEach(callback => {
        try {
          callback();
        } catch (error) {
          console.error('Error in coordinate update callback:', error);
        }
      });
    }
  }
  
  /**
   * Start cache cleanup timer
   */
  private startCacheCleanup(): void {
    setInterval(() => {
      const now = Date.now();
      const keysToDelete: string[] = [];
      this.coordinateCache.forEach((entry, key) => {
        if (entry.expiresAt < now) {
          keysToDelete.push(key);
        }
      });
      keysToDelete.forEach(key => this.coordinateCache.delete(key));
    }, TIMING.cacheExpiration);
  }
}
