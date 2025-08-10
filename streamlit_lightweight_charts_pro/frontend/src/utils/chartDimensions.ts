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
 * Get chart dimensions using the new unified coordinate service
 * 
 * This function is now a wrapper around ChartCoordinateService for backward compatibility.
 * It provides the same interface but uses the centralized positioning system.
 * 
 * @param chart - The IChartAPI reference returned by LightweightCharts.createChart
 * @param container - The container element that holds the chart
 * @param mainSeries - Optional ISeriesAPI reference returned when adding data
 * @returns Promise with chart dimensions including time scale and price scale positions and sizes
 * @deprecated Use ChartCoordinateService.getInstance().getCoordinates() directly
 */
export const getChartDimensions = async (
  chart: IChartApi, 
  container: HTMLElement, 
  mainSeries?: ISeriesApi<any>
): Promise<{
  timeScalePositionAndSize: { x: number; y: number; height: number; width: number };
  priceScalePositionAndSize: { x: number; y: number; height: number; width: number };
  containerDimensions: { width: number; height: number };
}> => {
  // Import the new coordinate service
  const { ChartCoordinateService } = await import('../services/ChartCoordinateService');
  const coordinateService = ChartCoordinateService.getInstance();
  
  try {
    // Get coordinates using the new unified service
    const coordinates = await coordinateService.getCoordinates(chart, container, {
      useCache: true,
      validateResult: true,
      fallbackOnError: true
    });
    
    // Transform to legacy format for backward compatibility
    return {
      timeScalePositionAndSize: coordinates.timeScale,
      priceScalePositionAndSize: coordinates.priceScaleLeft, // Use left price scale for backward compat
      containerDimensions: {
        width: coordinates.container.width,
        height: coordinates.container.height
      }
    };
  } catch (error) {
    console.error('Error getting chart dimensions:', error);
    
    // Return fallback values
    return {
      timeScalePositionAndSize: { x: 0, y: 0, height: 35, width: 0 },
      priceScalePositionAndSize: { x: 0, y: 0, height: 0, width: 70 },
      containerDimensions: { width: 0, height: 0 }
    };
  }
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
 * Synchronous version using the new unified coordinate service
 * 
 * This function provides immediate results without async operations.
 * It's a wrapper around the coordinate service for backward compatibility.
 * 
 * @param chart - The IChartAPI reference returned by LightweightCharts.createChart
 * @param container - The container element that holds the chart
 * @param mainSeries - Optional ISeriesAPI reference returned when adding data
 * @returns Chart dimensions including time scale and price scale positions and sizes
 * @deprecated Use ChartCoordinateService directly for better error handling
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
  try {
    // Get container dimensions
    const rect = container.getBoundingClientRect();
    const containerDimensions = {
      width: rect.width || container.offsetWidth || 800,
      height: rect.height || container.offsetHeight || 600
    };
    
    // Get time scale dimensions
    let timeScaleHeight = 35;
    let timeScaleWidth = containerDimensions.width;
    try {
      const timeScale = chart.timeScale();
      timeScaleHeight = timeScale.height() || 35;
      timeScaleWidth = timeScale.width() || containerDimensions.width;
    } catch (e) {
      // Use defaults
    }
    
    // Get price scale width
    let priceScaleWidth = 70;
    try {
      const priceScale = chart.priceScale('left');
      priceScaleWidth = priceScale.width() || 70;
    } catch (e) {
      // Use default
    }
    
    // Return dimensions in legacy format
    return {
      timeScalePositionAndSize: {
        x: 0,
        y: containerDimensions.height - timeScaleHeight,
        height: timeScaleHeight,
        width: timeScaleWidth,
      },
      priceScalePositionAndSize: {
        x: 0,
        y: 0,
        height: containerDimensions.height - timeScaleHeight,
        width: priceScaleWidth,
      },
      containerDimensions
    };
    
  } catch (error) {
    console.warn('Error getting chart dimensions synchronously:', error);
    
    // Return fallback values
    return {
      timeScalePositionAndSize: { x: 0, y: 0, height: 35, width: 0 },
      priceScalePositionAndSize: { x: 0, y: 0, height: 0, width: 70 },
      containerDimensions: { width: 800, height: 600 }
    };
  }
}; 