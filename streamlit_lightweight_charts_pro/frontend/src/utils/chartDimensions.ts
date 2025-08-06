import { IChartApi, ISeriesApi } from 'lightweight-charts';
import { memoize, getCachedDimensions, PerformanceMonitor } from './performance';

// Performance monitor instance
const perfMonitor = PerformanceMonitor.getInstance();

// Cache for chart dimensions to avoid repeated calculations
const dimensionCache = new Map<string, {
  timeScalePositionAndSize: { x: number; y: number; height: number; width: number };
  priceScalePositionAndSize: { x: number; y: number; height: number; width: number };
  containerDimensions: { width: number; height: number };
  timestamp: number;
}>();

// Cache invalidation time (5 seconds)
const CACHE_DURATION = 5000;

// Memoized chart element validation
const isValidChart = memoize(
  (chart: IChartApi): boolean => {
    try {
      if (!chart || typeof chart.chartElement !== 'function') {
        return false;
      }
      chart.chartElement();
      return true;
    } catch {
      return false;
    }
  },
  (chart: IChartApi) => chart?.chartElement?.()?.id || 'unknown'
);

// Memoized time scale validation
const isValidTimeScale = memoize(
  (chart: IChartApi): boolean => {
    try {
      if (!isValidChart(chart)) {
        return false;
      }
      const timeScale = chart.timeScale();
      return timeScale !== null && timeScale !== undefined;
    } catch {
      return false;
    }
  },
  (chart: IChartApi) => chart?.chartElement?.()?.id || 'unknown'
);

// Memoized price scale width calculation
const getPriceScaleWidth = memoize(
  (chart: IChartApi, mainSeries?: ISeriesApi<any>): number => {
    const stopTimer = perfMonitor.startTimer('getPriceScaleWidth');
    
    try {
      // Try to get width from main series first
      if (mainSeries) {
        try {
          const priceScale = mainSeries.priceScale();
          if (priceScale && typeof priceScale.width === 'function') {
            const width = priceScale.width();
            stopTimer();
            return width;
          }
        } catch (error) {
          // Fall through to default price scale
        }
      }
      
      // Fallback to default price scale
      try {
        const priceScale = chart.priceScale('right');
        if (priceScale && typeof priceScale.width === 'function') {
          const width = priceScale.width();
          stopTimer();
          return width;
        }
      } catch (error) {
        // Use default fallback
      }
      
      stopTimer();
      return 70; // Default fallback
    } catch (error) {
      stopTimer();
      return 70; // Default fallback
    }
  },
  (chart: IChartApi, mainSeries?: ISeriesApi<any>) => {
    const chartId = chart?.chartElement?.()?.id || 'unknown';
    const seriesId = mainSeries ? 'with-series' : 'no-series';
    return `${chartId}-${seriesId}`;
  }
);

/**
 * Get chart dimensions using optimized approach with caching
 * 
 * This function uses caching and memoization to avoid repeated expensive calculations.
 * It also includes performance monitoring to identify bottlenecks.
 * 
 * @param chart - The IChartAPI reference returned by LightweightCharts.createChart
 * @param container - The container element that holds the chart
 * @param mainSeries - Optional ISeriesAPI reference returned when adding data
 * @returns Promise with chart dimensions including time scale and price scale positions and sizes
 */
export const getChartDimensions = (
  chart: IChartApi, 
  container: HTMLElement, 
  mainSeries?: ISeriesApi<any>
): Promise<{
  timeScalePositionAndSize: { x: number; y: number; height: number; width: number };
  priceScalePositionAndSize: { x: number; y: number; height: number; width: number };
  containerDimensions: { width: number; height: number };
}> => {
  const stopTimer = perfMonitor.startTimer('getChartDimensions');
  
  return new Promise((resolve) => {
    // Generate cache key
    const chartId = chart?.chartElement?.()?.id || 'unknown';
    const containerId = container?.id || 'unknown';
    const cacheKey = `${chartId}-${containerId}-${mainSeries ? 'with-series' : 'no-series'}`;
    
    // Check cache first
    const cached = dimensionCache.get(cacheKey);
    if (cached && (Date.now() - cached.timestamp) < CACHE_DURATION) {
      stopTimer();
      resolve(cached);
      return;
    }
    
    // Use requestAnimationFrame for better performance
    requestAnimationFrame(() => {
      try {
        // Validate chart
        if (!isValidChart(chart)) {
          const fallback = {
            timeScalePositionAndSize: { x: 0, y: 0, height: 35, width: 0 },
            priceScalePositionAndSize: { x: 0, y: 0, height: 0, width: 70 },
            containerDimensions: { width: 0, height: 0 }
          };
          stopTimer();
          resolve(fallback);
          return;
        }
        
        // Get container dimensions using cached function
        const containerDimensions = getCachedDimensions(container);
        
        // Validate time scale
        if (!isValidTimeScale(chart)) {
          const fallback = {
            timeScalePositionAndSize: { x: 0, y: 0, height: 35, width: 0 },
            priceScalePositionAndSize: { x: 0, y: 0, height: 0, width: 70 },
            containerDimensions
          };
          stopTimer();
          resolve(fallback);
          return;
        }
        
        // Get time scale dimensions
        const timeScale = chart.timeScale();
        const timeScaleWidth = timeScale.width();
        const timeScaleHeight = timeScale.height();
        
        // Get price scale width using memoized function
        const priceScaleWidth = getPriceScaleWidth(chart, mainSeries);
        
        // Calculate positions and sizes
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
        
        // Create result object
        const result = {
          timeScalePositionAndSize,
          priceScalePositionAndSize,
          containerDimensions
        };
        
        // Cache the result
        dimensionCache.set(cacheKey, {
          ...result,
          timestamp: Date.now()
        });
        
        // Log in development mode only
        if (process.env.NODE_ENV === 'development') {
          // Chart dimensions calculated
        }
        
        stopTimer();
        resolve(result);
        
      } catch (error) {
        console.warn('Error getting chart dimensions:', error);
        
        const fallback = {
          timeScalePositionAndSize: { x: 0, y: 0, height: 35, width: 0 },
          priceScalePositionAndSize: { x: 0, y: 0, height: 0, width: 70 },
          containerDimensions: { width: 0, height: 0 }
        };
        
        stopTimer();
        resolve(fallback);
      }
    });
  });
};

/**
 * Clear the dimension cache
 * Useful when charts are resized or reconfigured
 */
export const clearDimensionCache = (): void => {
  dimensionCache.clear();
};

/**
 * Get performance metrics for dimension calculations
 */
export const getDimensionMetrics = () => {
  return perfMonitor.getMetrics();
};

/**
 * Optimized version that doesn't use requestAnimationFrame for immediate results
 * Use this when you need dimensions immediately without waiting for the next frame
 */
export const getChartDimensionsSync = (
  chart: IChartApi, 
  container: HTMLElement, 
  mainSeries?: ISeriesApi<any>
): {
  timeScalePositionAndSize: { x: number; y: number; height: number; width: number };
  priceScalePositionAndSize: { x: number; y: number; height: number; width: number };
  containerDimensions: { width: number; height: number };
} => {
  const stopTimer = perfMonitor.startTimer('getChartDimensionsSync');
  
  try {
    // Validate chart
    if (!isValidChart(chart)) {
      const fallback = {
        timeScalePositionAndSize: { x: 0, y: 0, height: 35, width: 0 },
        priceScalePositionAndSize: { x: 0, y: 0, height: 0, width: 70 },
        containerDimensions: { width: 0, height: 0 }
      };
      stopTimer();
      return fallback;
    }
    
    // Get container dimensions
    const containerDimensions = getCachedDimensions(container);
    
    // Validate time scale
    if (!isValidTimeScale(chart)) {
      const fallback = {
        timeScalePositionAndSize: { x: 0, y: 0, height: 35, width: 0 },
        priceScalePositionAndSize: { x: 0, y: 0, height: 0, width: 70 },
        containerDimensions
      };
      stopTimer();
      return fallback;
    }
    
    // Get dimensions
    const timeScale = chart.timeScale();
    const timeScaleWidth = timeScale.width();
    const timeScaleHeight = timeScale.height();
    const priceScaleWidth = getPriceScaleWidth(chart, mainSeries);
    
    const result = {
      timeScalePositionAndSize: {
        x: 0,
        y: containerDimensions.height - timeScaleHeight,
        height: timeScaleHeight,
        width: timeScaleWidth,
      },
      priceScalePositionAndSize: {
        x: timeScaleWidth,
        y: 0,
        height: containerDimensions.height - timeScaleHeight,
        width: priceScaleWidth,
      },
      containerDimensions
    };
    
    stopTimer();
    return result;
    
  } catch (error) {
    console.warn('Error getting chart dimensions synchronously:', error);
    
    const fallback = {
      timeScalePositionAndSize: { x: 0, y: 0, height: 35, width: 0 },
      priceScalePositionAndSize: { x: 0, y: 0, height: 0, width: 70 },
      containerDimensions: { width: 0, height: 0 }
    };
    
    stopTimer();
    return fallback;
  }
}; 