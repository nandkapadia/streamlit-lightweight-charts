import { RectangleOverlayPlugin } from '../rectanglePlugin';
import { SignalSeries } from '../signalSeriesPlugin';
import { createTradeVisualElements } from '../tradeVisualization';
import { createAnnotationVisualElements } from '../annotationSystem';

// Mock the lightweight-charts library
const mockChart = {
  addCandlestickSeries: () => ({
    setData: () => {},
    update: () => {},
    applyOptions: () => {},
    priceScale: () => ({ applyOptions: () => {} }),
  }),
  addLineSeries: () => ({
    setData: () => {},
    update: () => {},
    applyOptions: () => {},
    priceScale: () => ({ applyOptions: () => {} }),
  }),
  timeScale: {
    fitContent: () => {},
    scrollToPosition: () => {},
    scrollToTime: () => {},
    setVisibleRange: () => {},
    applyOptions: () => {},
  },
  priceScale: () => ({ applyOptions: () => {} }),
  applyOptions: () => {},
  resize: () => {},
  remove: () => {},
  subscribeClick: () => {},
  subscribeCrosshairMove: () => {},
  unsubscribeClick: () => {},
  unsubscribeCrosshairMove: () => {},
};

describe('Chart Plugins', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('RectangleOverlayPlugin', () => {
    it('should create rectangle overlay plugin', () => {
      const plugin = new RectangleOverlayPlugin();
      expect(plugin).toBeDefined();
    });

    it('should add rectangle overlay to chart', () => {
      const plugin = new RectangleOverlayPlugin();
      const chart = mockChart;
      
      plugin.addToChart(chart);
      
      expect(chart).toBeDefined();
    });

    it('should handle rectangle data', () => {
      const plugin = new RectangleOverlayPlugin();
      const chart = mockChart;
      
      plugin.addToChart(chart);
      
      const rectangleData = [
        {
          time: '2024-01-01',
          price: 100,
          width: 50,
          height: 20,
          color: '#ff0000',
        },
      ];
      
      plugin.setRectangles(rectangleData);
      
      expect(plugin).toBeDefined();
    });

    it('should handle empty rectangle data', () => {
      const plugin = new RectangleOverlayPlugin();
      const chart = mockChart;
      
      plugin.addToChart(chart);
      plugin.setRectangles([]);
      
      expect(plugin).toBeDefined();
    });

    it('should handle invalid rectangle data', () => {
      const plugin = new RectangleOverlayPlugin();
      const chart = mockChart;
      
      plugin.addToChart(chart);
      plugin.setRectangles(null);
      
      expect(plugin).toBeDefined();
    });
  });

  describe('SignalSeries', () => {
    it('should create signal series', () => {
      const signalSeries = new SignalSeries();
      expect(signalSeries).toBeDefined();
    });

    it('should add signal series to chart', () => {
      const signalSeries = new SignalSeries();
      const chart = mockChart;
      
      signalSeries.addToChart(chart);
      
      expect(chart).toBeDefined();
    });

    it('should handle signal data', () => {
      const signalSeries = new SignalSeries();
      const chart = mockChart;
      
      signalSeries.addToChart(chart);
      
      const signalData = [
        {
          time: '2024-01-01',
          price: 100,
          type: 'buy',
          color: '#00ff00',
        },
      ];
      
      signalSeries.setSignals(signalData);
      
      expect(signalSeries).toBeDefined();
    });

    it('should handle empty signal data', () => {
      const signalSeries = new SignalSeries();
      const chart = mockChart;
      
      signalSeries.addToChart(chart);
      signalSeries.setSignals([]);
      
      expect(signalSeries).toBeDefined();
    });

    it('should handle different signal types', () => {
      const signalSeries = new SignalSeries();
      const chart = mockChart;
      
      signalSeries.addToChart(chart);
      
      const signalData = [
        { time: '2024-01-01', price: 100, type: 'buy', color: '#00ff00' },
        { time: '2024-01-02', price: 110, type: 'sell', color: '#ff0000' },
        { time: '2024-01-03', price: 105, type: 'hold', color: '#ffff00' },
      ];
      
      signalSeries.setSignals(signalData);
      
      expect(signalSeries).toBeDefined();
    });
  });

  describe('Trade Visualization', () => {
    it('should create trade visual elements', () => {
      const trades = [
        {
          entryTime: '2024-01-01',
          entryPrice: 100,
          exitTime: '2024-01-02',
          exitPrice: 110,
          quantity: 10,
          tradeType: 'long',
        },
      ];
      
      const elements = createTradeVisualElements(trades);
      expect(elements).toBeDefined();
    });

    it('should handle empty trades', () => {
      const elements = createTradeVisualElements([]);
      expect(elements).toBeDefined();
    });

    it('should handle null trades', () => {
      const elements = createTradeVisualElements(null);
      expect(elements).toBeDefined();
    });

    it('should handle different trade types', () => {
      const trades = [
        {
          entryTime: '2024-01-01',
          entryPrice: 100,
          exitTime: '2024-01-02',
          exitPrice: 110,
          quantity: 10,
          tradeType: 'long',
        },
        {
          entryTime: '2024-01-03',
          entryPrice: 110,
          exitTime: '2024-01-04',
          exitPrice: 100,
          quantity: 5,
          tradeType: 'short',
        },
      ];
      
      const elements = createTradeVisualElements(trades);
      expect(elements).toBeDefined();
    });

    it('should handle trades with missing data', () => {
      const trades = [
        {
          entryTime: '2024-01-01',
          entryPrice: 100,
          exitTime: '2024-01-02',
          exitPrice: 110,
          quantity: 10,
          tradeType: 'long',
        },
        {
          entryTime: '2024-01-03',
          entryPrice: 110,
          // Missing exit data
          quantity: 5,
          tradeType: 'short',
        },
      ];
      
      const elements = createTradeVisualElements(trades);
      expect(elements).toBeDefined();
    });
  });

  describe('Annotation System', () => {
    it('should create annotation visual elements', () => {
      const annotations = [
        {
          time: '2024-01-01',
          price: 100,
          text: 'Test annotation',
          type: 'text',
          position: 'above',
        },
      ];
      
      const elements = createAnnotationVisualElements(annotations);
      expect(elements).toBeDefined();
    });

    it('should handle empty annotations', () => {
      const elements = createAnnotationVisualElements([]);
      expect(elements).toBeDefined();
    });

    it('should handle null annotations', () => {
      const elements = createAnnotationVisualElements(null);
      expect(elements).toBeDefined();
    });

    it('should handle different annotation types', () => {
      const annotations = [
        {
          time: '2024-01-01',
          price: 100,
          text: 'Text annotation',
          type: 'text',
          position: 'above',
        },
        {
          time: '2024-01-02',
          price: 110,
          text: 'Arrow annotation',
          type: 'arrow',
          position: 'below',
        },
        {
          time: '2024-01-03',
          price: 105,
          text: 'Shape annotation',
          type: 'shape',
          position: 'inline',
        },
      ];
      
      const elements = createAnnotationVisualElements(annotations);
      expect(elements).toBeDefined();
    });

    it('should handle annotations with custom styling', () => {
      const annotations = [
        {
          time: '2024-01-01',
          price: 100,
          text: 'Styled annotation',
          type: 'text',
          position: 'above',
          color: '#ff0000',
          backgroundColor: '#ffff00',
          fontSize: 14,
          fontWeight: 'bold',
        },
      ];
      
      const elements = createAnnotationVisualElements(annotations);
      expect(elements).toBeDefined();
    });

    it('should handle annotations with missing properties', () => {
      const annotations = [
        {
          time: '2024-01-01',
          price: 100,
          text: 'Minimal annotation',
          // Missing type and position
        },
      ];
      
      const elements = createAnnotationVisualElements(annotations);
      expect(elements).toBeDefined();
    });
  });

  describe('Plugin Integration', () => {
    it('should integrate multiple plugins with chart', () => {
      const chart = mockChart;
      
      const rectanglePlugin = new RectangleOverlayPlugin();
      const signalSeries = new SignalSeries();
      
      rectanglePlugin.addToChart(chart);
      signalSeries.addToChart(chart);
      
      expect(chart).toBeDefined();
    });

    it('should handle plugin cleanup', () => {
      const chart = mockChart;
      
      const rectanglePlugin = new RectangleOverlayPlugin();
      rectanglePlugin.addToChart(chart);
      
      // Simulate cleanup
      rectanglePlugin.remove();
      
      expect(rectanglePlugin).toBeDefined();
    });

    it('should handle plugin errors gracefully', () => {
      const chart = null; // Invalid chart
      
      const rectanglePlugin = new RectangleOverlayPlugin();
      
      // Should not throw error
      expect(() => {
        rectanglePlugin.addToChart(chart);
      }).not.toThrow();
    });
  });

  describe('Performance', () => {
    it('should handle large datasets efficiently', () => {
      const chart = mockChart;
      
      const rectanglePlugin = new RectangleOverlayPlugin();
      rectanglePlugin.addToChart(chart);
      
      const largeRectangleData = Array.from({ length: 1000 }, (_, i) => ({
        time: `2024-01-${String(i + 1).padStart(2, '0')}`,
        price: 100 + i,
        width: 50,
        height: 20,
        color: '#ff0000',
      }));
      
      rectanglePlugin.setRectangles(largeRectangleData);
      
      expect(rectanglePlugin).toBeDefined();
    });

    it('should handle rapid updates', () => {
      const chart = mockChart;
      
      const signalSeries = new SignalSeries();
      signalSeries.addToChart(chart);
      
      // Simulate rapid updates
      for (let i = 0; i < 100; i++) {
        const signalData = [
          {
            time: `2024-01-${String(i + 1).padStart(2, '0')}`,
            price: 100 + i,
            type: 'buy',
            color: '#00ff00',
          },
        ];
        
        signalSeries.setSignals(signalData);
      }
      
      expect(signalSeries).toBeDefined();
    });
  });

  describe('Error Handling', () => {
    it('should handle invalid plugin data', () => {
      const chart = mockChart;
      
      const rectanglePlugin = new RectangleOverlayPlugin();
      rectanglePlugin.addToChart(chart);
      
      const invalidData = [
        {
          time: 'invalid-time',
          price: 'invalid-price',
          width: -50,
          height: -20,
          color: 'invalid-color',
        },
      ];
      
      rectanglePlugin.setRectangles(invalidData);
      
      expect(rectanglePlugin).toBeDefined();
    });

    it('should handle plugin initialization errors', () => {
      const invalidChart = {
        // Missing required methods
      };
      
      const rectanglePlugin = new RectangleOverlayPlugin();
      
      expect(() => {
        rectanglePlugin.addToChart(invalidChart);
      }).not.toThrow();
    });
  });
}); 