import { useRef, useCallback, useMemo, useEffect, useLayoutEffect } from 'react';
import { IChartApi, ISeriesApi } from 'lightweight-charts';
import { debounce, throttle, shallowEqual, PerformanceMonitor } from '../utils/performance';

// Performance monitor instance
const perfMonitor = PerformanceMonitor.getInstance();

interface ChartRefs {
  chart: IChartApi | null;
  series: ISeriesApi<any>[];
  container: HTMLElement | null;
  isInitialized: boolean;
  isDisposed: boolean;
}

interface UseOptimizedChartOptions {
  chartId: string;
  autoResize?: boolean;
  debounceMs?: number;
  throttleMs?: number;
  enablePerformanceMonitoring?: boolean;
}

/**
 * Optimized React hook for chart management
 * Provides better performance through memoization, debouncing, and efficient cleanup
 */
export function useOptimizedChart(options: UseOptimizedChartOptions) {
  const {
    chartId,
    autoResize = true,
    debounceMs = 100,
    throttleMs = 16,
    enablePerformanceMonitoring = process.env.NODE_ENV === 'development'
  } = options;

  // Chart references
  const chartRefs = useRef<ChartRefs>({
    chart: null,
    series: [],
    container: null,
    isInitialized: false,
    isDisposed: false
  });

  // Performance monitoring
  const performanceTimer = useRef<(() => void) | null>(null);

  // Memoized chart creation function
  const createChart = useCallback((
    container: HTMLElement,
    chartOptions: any
  ): IChartApi | null => {
    if (enablePerformanceMonitoring) {
      performanceTimer.current = perfMonitor.startTimer(`createChart-${chartId}`);
    }

    try {
      const { createChart: createChartFn } = require('lightweight-charts');
      const chart = createChartFn(container, chartOptions);
      
      // Set chart element ID for easier identification
      const chartElement = chart.chartElement();
      if (chartElement) {
        chartElement.id = chartId;
      }

      chartRefs.current.chart = chart;
      chartRefs.current.container = container;
      chartRefs.current.isInitialized = true;
      chartRefs.current.isDisposed = false;

      if (enablePerformanceMonitoring && performanceTimer.current) {
        performanceTimer.current();
      }

      return chart;
    } catch (error) {
      console.error(`Failed to create chart ${chartId}:`, error);
      if (enablePerformanceMonitoring && performanceTimer.current) {
        performanceTimer.current();
      }
      return null;
    }
  }, [chartId, enablePerformanceMonitoring]);

  // Optimized resize handler with debouncing
  const handleResize = useMemo(() => {
    if (!autoResize) return null;

    return debounce((width: number, height: number) => {
      if (chartRefs.current.chart && !chartRefs.current.isDisposed) {
        try {
          chartRefs.current.chart.resize(width, height);
        } catch (error) {
          console.warn(`Resize failed for chart ${chartId}:`, error);
        }
      }
    }, debounceMs);
  }, [autoResize, debounceMs, chartId]);

  // Throttled resize observer callback
  const resizeObserverCallback = useMemo(() => {
    if (!autoResize) return null;

    return throttle((entries: ResizeObserverEntry[]) => {
      entries.forEach(entry => {
        if (entry.target === chartRefs.current.container) {
          const { width, height } = entry.contentRect;
          if (handleResize) {
            handleResize(width, height);
          }
        }
      });
    }, throttleMs);
  }, [autoResize, throttleMs, handleResize]);

  // Resize observer ref
  const resizeObserverRef = useRef<ResizeObserver | null>(null);

  // Setup resize observer
  const setupResizeObserver = useCallback(() => {
    if (!autoResize || !chartRefs.current.container || !resizeObserverCallback) {
      return;
    }

    try {
      if (resizeObserverRef.current) {
        resizeObserverRef.current.disconnect();
      }

      resizeObserverRef.current = new ResizeObserver(resizeObserverCallback);
      resizeObserverRef.current.observe(chartRefs.current.container);
    } catch (error) {
      console.warn(`Failed to setup resize observer for chart ${chartId}:`, error);
    }
  }, [autoResize, resizeObserverCallback, chartId]);

  // Cleanup function
  const cleanup = useCallback(() => {
    const stopTimer = enablePerformanceMonitoring 
      ? perfMonitor.startTimer(`cleanup-${chartId}`)
      : null;

    try {
      // Mark as disposed
      chartRefs.current.isDisposed = true;

      // Disconnect resize observer
      if (resizeObserverRef.current) {
        resizeObserverRef.current.disconnect();
        resizeObserverRef.current = null;
      }

      // Remove chart
      if (chartRefs.current.chart) {
        try {
          chartRefs.current.chart.remove();
        } catch (error) {
          console.warn(`Error removing chart ${chartId}:`, error);
        }
        chartRefs.current.chart = null;
      }

      // Clear series references
      chartRefs.current.series = [];
      chartRefs.current.container = null;
      chartRefs.current.isInitialized = false;

      if (stopTimer) {
        stopTimer();
      }
    } catch (error) {
      console.error(`Error during cleanup for chart ${chartId}:`, error);
      if (stopTimer) {
        stopTimer();
      }
    }
  }, [chartId, enablePerformanceMonitoring]);

  // Add series with optimization
  const addSeries = useCallback((
    seriesType: any,
    options: any = {},
    paneId?: number
  ): ISeriesApi<any> | null => {
    if (!chartRefs.current.chart || chartRefs.current.isDisposed) {
      return null;
    }

    const stopTimer = enablePerformanceMonitoring 
      ? perfMonitor.startTimer(`addSeries-${chartId}`)
      : null;

    try {
      const series = chartRefs.current.chart.addSeries(seriesType, options, paneId);
      chartRefs.current.series.push(series);

      if (stopTimer) {
        stopTimer();
      }

      return series;
    } catch (error) {
      console.error(`Failed to add series to chart ${chartId}:`, error);
      if (stopTimer) {
        stopTimer();
      }
      return null;
    }
  }, [chartId, enablePerformanceMonitoring]);

  // Get series by index
  const getSeries = useCallback((index: number): ISeriesApi<any> | null => {
    return chartRefs.current.series[index] || null;
  }, []);

  // Get all series
  const getAllSeries = useCallback((): ISeriesApi<any>[] => {
    return [...chartRefs.current.series];
  }, []);

  // Check if chart is ready
  const isReady = useCallback((): boolean => {
    return chartRefs.current.isInitialized && !chartRefs.current.isDisposed;
  }, []);

  // Get chart instance
  const getChart = useCallback((): IChartApi | null => {
    return chartRefs.current.chart;
  }, []);

  // Get container
  const getContainer = useCallback((): HTMLElement | null => {
    return chartRefs.current.container;
  }, []);

  // Manual resize
  const resize = useCallback((width: number, height: number) => {
    if (chartRefs.current.chart && !chartRefs.current.isDisposed) {
      try {
        chartRefs.current.chart.resize(width, height);
      } catch (error) {
        console.warn(`Manual resize failed for chart ${chartId}:`, error);
      }
    }
  }, [chartId]);

  // Setup resize observer when chart is created
  useEffect(() => {
    if (chartRefs.current.isInitialized && !chartRefs.current.isDisposed) {
      setupResizeObserver();
    }
  }, [setupResizeObserver]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      cleanup();
    };
  }, [cleanup]);

  // Use layout effect for immediate cleanup when dependencies change
  useLayoutEffect(() => {
    return () => {
      // Immediate cleanup for layout changes
      if (resizeObserverRef.current) {
        resizeObserverRef.current.disconnect();
      }
    };
  }, []);

  return {
    createChart,
    addSeries,
    getSeries,
    getAllSeries,
    getChart,
    getContainer,
    isReady,
    resize,
    cleanup,
    chartId
  };
}

/**
 * Hook for comparing chart configurations efficiently
 */
export function useChartConfigComparison<T>(config: T): T {
  return useMemo(() => config, [JSON.stringify(config)]);
}

/**
 * Hook for optimized chart data updates
 */
export function useOptimizedDataUpdate<T>(
  data: T[],
  series: ISeriesApi<any> | null,
  options: {
    enableBatching?: boolean;
    batchSize?: number;
    throttleMs?: number;
  } = {}
) {
  const {
    enableBatching = true,
    batchSize = 1000,
    throttleMs = 16
  } = options;

  const updateData = useCallback((
    newData: T[],
    targetSeries?: ISeriesApi<any>
  ) => {
    const seriesToUpdate = targetSeries || series;
    if (!seriesToUpdate) return;

    const stopTimer = perfMonitor.startTimer('updateData');

    try {
      if (enableBatching && newData.length > batchSize) {
        // Batch update for large datasets
        for (let i = 0; i < newData.length; i += batchSize) {
          const batch = newData.slice(i, i + batchSize);
          seriesToUpdate.setData(batch);
        }
      } else {
        // Single update for smaller datasets
        seriesToUpdate.setData(newData);
      }

      stopTimer();
    } catch (error) {
      console.error('Error updating chart data:', error);
      stopTimer();
    }
  }, [series, enableBatching, batchSize]);

  const throttledUpdateData = useMemo(() => {
    return throttle(updateData, throttleMs);
  }, [updateData, throttleMs]);

  return {
    updateData,
    throttledUpdateData
  };
} 