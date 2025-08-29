// jest-dom adds custom jest matchers for asserting on DOM nodes.
import '@testing-library/jest-dom'

// Mock lightweight-charts library
const mockChart = {
  addCandlestickSeries: () => ({
    setData: () => {},
    update: () => {},
    applyOptions: () => {},
    priceScale: () => ({applyOptions: () => {}})
  }),
  addLineSeries: () => ({
    setData: () => {},
    update: () => {},
    applyOptions: () => {},
    priceScale: () => ({applyOptions: () => {}})
  }),
  addAreaSeries: () => ({
    setData: () => {},
    update: () => {},
    applyOptions: () => {},
    priceScale: () => ({applyOptions: () => {}})
  }),
  addHistogramSeries: () => ({
    setData: () => {},
    update: () => {},
    applyOptions: () => {},
    priceScale: () => ({applyOptions: () => {}})
  }),
  addBaselineSeries: () => ({
    setData: () => {},
    update: () => {},
    applyOptions: () => {},
    priceScale: () => ({applyOptions: () => {}})
  }),
  addBandSeries: () => ({
    setData: () => {},
    update: () => {},
    applyOptions: () => {},
    priceScale: () => ({applyOptions: () => {}})
  }),
  timeScale: {
    fitContent: () => {},
    scrollToPosition: () => {},
    scrollToTime: () => {},
    setVisibleRange: () => {},
    applyOptions: () => {}
  },
  priceScale: () => ({applyOptions: () => {}}),
  applyOptions: () => {},
  resize: () => {},
  remove: () => {},
  subscribeClick: () => {},
  subscribeCrosshairMove: () => {},
  unsubscribeClick: () => {},
  unsubscribeCrosshairMove: () => {},
  chartElement: () => ({
    width: 800,
    height: 600,
    getBoundingClientRect: () => ({
      width: 800,
      height: 600,
      top: 0,
      left: 0,
      right: 800,
      bottom: 600
    })
  })
}

// Mock modules
jest.mock('lightweight-charts', () => ({
  createChart: () => mockChart,
  createSeriesMarkers: () => []
}))

jest.mock('streamlit-component-lib', () => ({
  Streamlit: {
    setComponentValue: () => {},
    setFrameHeight: () => {},
    setComponentReady: () => {},
    RENDER_EVENT: 'streamlit:render',
    SET_FRAME_HEIGHT_EVENT: 'streamlit:setFrameHeight'
  }
}))

jest.mock('streamlit-component-lib-react-hooks', () => ({
  useStreamlit: () => ({
    theme: {
      base: 'light',
      primaryColor: '#ff4b4b',
      backgroundColor: '#ffffff',
      secondaryBackgroundColor: '#f0f2f6',
      textColor: '#262730'
    },
    args: {},
    disabled: false,
    height: 400,
    width: 800
  }),
  useRenderData: () => ({
    args: {
      config: {
        charts: [
          {
            chartId: 'test-chart',
            chart: {
              height: 400,
              autoSize: true,
              layout: {
                color: '#ffffff',
                textColor: '#000000'
              }
            },
            series: [],
            annotations: {
              layers: {}
            }
          }
        ],
        sync: {
          enabled: false,
          crosshair: false,
          timeRange: false
        }
      },
      height: 400,
      width: null
    },
    disabled: false,
    height: 400,
    width: 800,
    theme: {
      base: 'light',
      primaryColor: '#ff4b4b',
      backgroundColor: '#ffffff',
      secondaryBackgroundColor: '#f0f2f6',
      textColor: '#262730'
    }
  }),
  StreamlitProvider: ({children}) => {
    const React = require('react')
    return React.createElement('div', {}, children)
  }
}))

// Mock browser APIs
global.ResizeObserver = class ResizeObserver {
  observe() {}
  unobserve() {}
  disconnect() {}
}

global.IntersectionObserver = class IntersectionObserver {
  constructor() {}
  observe() {}
  unobserve() {}
  disconnect() {}
}

Object.defineProperty(window, 'performance', {
  value: {
    now: () => Date.now(),
    mark: () => {},
    measure: () => {},
    getEntriesByType: () => []
  },
  writable: true
})

global.requestAnimationFrame = callback => {
  setTimeout(callback, 0)
  return 1
}

global.cancelAnimationFrame = () => {}

// Mock DOM methods
Object.defineProperty(window, 'getComputedStyle', {
  value: () => ({
    getPropertyValue: () => ''
  })
})

Element.prototype.getBoundingClientRect = () => ({
  width: 800,
  height: 600,
  top: 0,
  left: 0,
  right: 800,
  bottom: 600
})

Object.defineProperty(HTMLElement.prototype, 'scrollHeight', {
  configurable: true,
  value: 600
})

Object.defineProperty(HTMLElement.prototype, 'offsetHeight', {
  configurable: true,
  value: 600
})

Object.defineProperty(HTMLElement.prototype, 'offsetWidth', {
  configurable: true,
  value: 800
})
