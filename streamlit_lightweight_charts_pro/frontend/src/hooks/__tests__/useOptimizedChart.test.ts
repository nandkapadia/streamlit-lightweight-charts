import {renderHook, act} from '@testing-library/react'
import {useOptimizedChart} from '../useOptimizedChart'

// Mock ResizeObserver
global.ResizeObserver = jest.fn().mockImplementation(() => ({
  observe: jest.fn(),
  unobserve: jest.fn(),
  disconnect: jest.fn()
}))

// Mock performance API
Object.defineProperty(window, 'performance', {
  value: {
    now: jest.fn(() => Date.now()),
    mark: jest.fn(),
    measure: jest.fn(),
    getEntriesByType: jest.fn(() => [])
  },
  writable: true
})

// Mock requestAnimationFrame
global.requestAnimationFrame = jest.fn(callback => {
  setTimeout(callback, 0)
  return 1
})

global.cancelAnimationFrame = jest.fn()

describe('useOptimizedChart Hook', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  describe('Initialization', () => {
    it('should initialize with default values', () => {
      const {result} = renderHook(() => useOptimizedChart())

      expect(result.current.isInitialized).toBe(false)
      expect(result.current.isDisposing).toBe(false)
      expect(result.current.chartRefs).toEqual({})
      expect(result.current.seriesRefs).toEqual({})
      expect(result.current.chartConfigs).toEqual({})
    })

    it('should initialize with custom options', () => {
      const options = {
        enablePerformanceLogging: true,
        debounceDelay: 200,
        maxRetries: 5
      }

      const {result} = renderHook(() => useOptimizedChart(options))

      expect(result.current.isInitialized).toBe(false)
      expect(result.current.isDisposing).toBe(false)
    })
  })

  describe('Chart Management', () => {
    it('should add chart successfully', () => {
      const {result} = renderHook(() => useOptimizedChart())

      act(() => {
        result.current.addChart('test-chart', {} as any, {} as any)
      })

      expect(result.current.chartRefs['test-chart']).toBeDefined()
      expect(result.current.chartConfigs['test-chart']).toBeDefined()
    })

    it('should add multiple charts', () => {
      const {result} = renderHook(() => useOptimizedChart())

      act(() => {
        result.current.addChart('chart1', {} as any, {} as any)
        result.current.addChart('chart2', {} as any, {} as any)
        result.current.addChart('chart3', {} as any, {} as any)
      })

      expect(Object.keys(result.current.chartRefs)).toHaveLength(3)
      expect(Object.keys(result.current.chartConfigs)).toHaveLength(3)
    })

    it('should remove chart successfully', () => {
      const {result} = renderHook(() => useOptimizedChart())

      act(() => {
        result.current.addChart('test-chart', {} as any, {} as any)
      })

      expect(result.current.chartRefs['test-chart']).toBeDefined()

      act(() => {
        result.current.removeChart('test-chart')
      })

      expect(result.current.chartRefs['test-chart']).toBeUndefined()
      expect(result.current.chartConfigs['test-chart']).toBeUndefined()
    })

    it('should handle removing non-existent chart', () => {
      const {result} = renderHook(() => useOptimizedChart())

      act(() => {
        result.current.removeChart('non-existent')
      })

      // Should not throw error
      expect(result.current.chartRefs).toEqual({})
    })

    it('should clear all charts', () => {
      const {result} = renderHook(() => useOptimizedChart())

      act(() => {
        result.current.addChart('chart1', {} as any, {} as any)
        result.current.addChart('chart2', {} as any, {} as any)
        result.current.addChart('chart3', {} as any, {} as any)
      })

      expect(Object.keys(result.current.chartRefs)).toHaveLength(3)

      act(() => {
        result.current.clearAllCharts()
      })

      expect(result.current.chartRefs).toEqual({})
      expect(result.current.chartConfigs).toEqual({})
      expect(result.current.seriesRefs).toEqual({})
    })
  })

  describe('Series Management', () => {
    it('should add series to chart', () => {
      const {result} = renderHook(() => useOptimizedChart())

      act(() => {
        result.current.addChart('test-chart', {} as any, {} as any)
        result.current.addSeries('test-chart', 'series1', {} as any)
      })

      expect(result.current.seriesRefs['test-chart']).toBeDefined()
      expect(result.current.seriesRefs['test-chart']['series1']).toBeDefined()
    })

    it('should add multiple series to chart', () => {
      const {result} = renderHook(() => useOptimizedChart())

      act(() => {
        result.current.addChart('test-chart', {} as any, {} as any)
        result.current.addSeries('test-chart', 'series1', {} as any)
        result.current.addSeries('test-chart', 'series2', {} as any)
        result.current.addSeries('test-chart', 'series3', {} as any)
      })

      expect(Object.keys(result.current.seriesRefs['test-chart'])).toHaveLength(3)
    })

    it('should remove series from chart', () => {
      const {result} = renderHook(() => useOptimizedChart())

      act(() => {
        result.current.addChart('test-chart', {} as any, {} as any)
        result.current.addSeries('test-chart', 'series1', {} as any)
      })

      expect(result.current.seriesRefs['test-chart']['series1']).toBeDefined()

      act(() => {
        result.current.removeSeries('test-chart', 'series1')
      })

      expect(result.current.seriesRefs['test-chart']['series1']).toBeUndefined()
    })

    it('should handle removing series from non-existent chart', () => {
      const {result} = renderHook(() => useOptimizedChart())

      act(() => {
        result.current.removeSeries('non-existent', 'series1')
      })

      // Should not throw error
      expect(result.current.seriesRefs).toEqual({})
    })

    it('should clear all series from chart', () => {
      const {result} = renderHook(() => useOptimizedChart())

      act(() => {
        result.current.addChart('test-chart', {} as any, {} as any)
        result.current.addSeries('test-chart', 'series1', {} as any)
        result.current.addSeries('test-chart', 'series2', {} as any)
        result.current.addSeries('test-chart', 'series3', {} as any)
      })

      expect(Object.keys(result.current.seriesRefs['test-chart'])).toHaveLength(3)

      act(() => {
        result.current.clearChartSeries('test-chart')
      })

      expect(result.current.seriesRefs['test-chart']).toEqual({})
    })
  })

  describe('Performance Optimization', () => {
    it('should debounce resize events', () => {
      jest.useFakeTimers()
      const {result} = renderHook(() => useOptimizedChart({debounceDelay: 100}))

      act(() => {
        result.current.addChart('test-chart', {} as any, {} as any)
      })

      const mockChart = result.current.chartRefs['test-chart']
      const mockResize = jest.fn()
      mockChart.resize = mockResize

      act(() => {
        result.current.handleResize('test-chart')
        result.current.handleResize('test-chart')
        result.current.handleResize('test-chart')
      })

      expect(mockResize).not.toHaveBeenCalled()

      act(() => {
        jest.advanceTimersByTime(100)
      })

      expect(mockResize).toHaveBeenCalledTimes(1)

      jest.useRealTimers()
    })

    it('should handle performance logging', () => {
      const consoleSpy = jest.spyOn(console, 'log').mockImplementation()
      const {result} = renderHook(() => useOptimizedChart({enablePerformanceLogging: true}))

      act(() => {
        result.current.addChart('test-chart', {} as any, {} as any)
      })

      expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('Chart added'))

      consoleSpy.mockRestore()
    })
  })

  describe('Error Handling', () => {
    it('should handle chart creation errors', () => {
      const {result} = renderHook(() => useOptimizedChart())

      act(() => {
        // Simulate error by passing invalid parameters
        result.current.addChart('test-chart', null as any, null as any)
      })

      expect(result.current.chartRefs['test-chart']).toBeDefined()
    })

    it('should handle series creation errors', () => {
      const {result} = renderHook(() => useOptimizedChart())

      act(() => {
        result.current.addChart('test-chart', {} as any, {} as any)
        result.current.addSeries('test-chart', 'series1', null as any)
      })

      expect(result.current.seriesRefs['test-chart']['series1']).toBeDefined()
    })

    it('should handle resize errors', () => {
      const {result} = renderHook(() => useOptimizedChart())

      act(() => {
        result.current.addChart('test-chart', {} as any, {} as any)
      })

      const mockChart = result.current.chartRefs['test-chart']
      mockChart.resize = jest.fn().mockImplementation(() => {
        throw new Error('Resize error')
      })

      act(() => {
        result.current.handleResize('test-chart')
      })

      // Should not throw error
      expect(mockChart.resize).toHaveBeenCalled()
    })
  })

  describe('State Management', () => {
    it('should update initialization state', () => {
      const {result} = renderHook(() => useOptimizedChart())

      expect(result.current.isInitialized).toBe(false)

      act(() => {
        result.current.setInitialized(true)
      })

      expect(result.current.isInitialized).toBe(true)
    })

    it('should update disposal state', () => {
      const {result} = renderHook(() => useOptimizedChart())

      expect(result.current.isDisposing).toBe(false)

      act(() => {
        result.current.setDisposing(true)
      })

      expect(result.current.isDisposing).toBe(true)
    })

    it('should get chart by ID', () => {
      const {result} = renderHook(() => useOptimizedChart())

      act(() => {
        result.current.addChart('test-chart', {} as any, {} as any)
      })

      const chart = result.current.getChart('test-chart')
      expect(chart).toBeDefined()
    })

    it('should return undefined for non-existent chart', () => {
      const {result} = renderHook(() => useOptimizedChart())

      const chart = result.current.getChart('non-existent')
      expect(chart).toBeUndefined()
    })

    it('should get series by ID', () => {
      const {result} = renderHook(() => useOptimizedChart())

      act(() => {
        result.current.addChart('test-chart', {} as any, {} as any)
        result.current.addSeries('test-chart', 'series1', {} as any)
      })

      const series = result.current.getSeries('test-chart', 'series1')
      expect(series).toBeDefined()
    })

    it('should return undefined for non-existent series', () => {
      const {result} = renderHook(() => useOptimizedChart())

      const series = result.current.getSeries('test-chart', 'series1')
      expect(series).toBeUndefined()
    })
  })

  describe('Cleanup', () => {
    it('should cleanup on unmount', () => {
      const {result, unmount} = renderHook(() => useOptimizedChart())

      act(() => {
        result.current.addChart('test-chart', {} as any, {} as any)
        result.current.addSeries('test-chart', 'series1', {} as any)
      })

      expect(result.current.chartRefs['test-chart']).toBeDefined()

      unmount()

      // Cleanup should be handled by the hook
      expect(result.current.chartRefs).toEqual({})
    })

    it('should handle cleanup with multiple charts', () => {
      const {result, unmount} = renderHook(() => useOptimizedChart())

      act(() => {
        result.current.addChart('chart1', {} as any, {} as any)
        result.current.addChart('chart2', {} as any, {} as any)
        result.current.addChart('chart3', {} as any, {} as any)
      })

      expect(Object.keys(result.current.chartRefs)).toHaveLength(3)

      unmount()

      expect(result.current.chartRefs).toEqual({})
    })
  })
})
