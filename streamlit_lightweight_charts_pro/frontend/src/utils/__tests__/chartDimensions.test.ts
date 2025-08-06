import { getChartDimensions } from '../chartDimensions';

// Mock DOM methods
Object.defineProperty(window, 'getComputedStyle', {
  value: () => ({
    getPropertyValue: () => '',
  }),
});

Element.prototype.getBoundingClientRect = jest.fn(() => ({
  width: 800,
  height: 600,
  top: 0,
  left: 0,
  right: 800,
  bottom: 600,
}));

describe('chartDimensions', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('getChartDimensions', () => {
    it('should return default dimensions when container is null', () => {
      const result = getChartDimensions(null, 400, 800);
      expect(result).toEqual({
        width: 800,
        height: 400,
      });
    });

    it('should return default dimensions when container is undefined', () => {
      const result = getChartDimensions(undefined, 400, 800);
      expect(result).toEqual({
        width: 800,
        height: 400,
      });
    });

    it('should return container dimensions when available', () => {
      const mockContainer = document.createElement('div');
      (mockContainer.getBoundingClientRect as jest.Mock).mockReturnValue({
        width: 1000,
        height: 500,
        top: 0,
        left: 0,
        right: 1000,
        bottom: 500,
      });

      const result = getChartDimensions(mockContainer, 400, 800);
      expect(result).toEqual({
        width: 1000,
        height: 500,
      });
    });

    it('should use default width when container width is 0', () => {
      const mockContainer = document.createElement('div');
      (mockContainer.getBoundingClientRect as jest.Mock).mockReturnValue({
        width: 0,
        height: 500,
        top: 0,
        left: 0,
        right: 0,
        bottom: 500,
      });

      const result = getChartDimensions(mockContainer, 400, 800);
      expect(result).toEqual({
        width: 800,
        height: 500,
      });
    });

    it('should use default height when container height is 0', () => {
      const mockContainer = document.createElement('div');
      (mockContainer.getBoundingClientRect as jest.Mock).mockReturnValue({
        width: 1000,
        height: 0,
        top: 0,
        left: 0,
        right: 1000,
        bottom: 0,
      });

      const result = getChartDimensions(mockContainer, 400, 800);
      expect(result).toEqual({
        width: 1000,
        height: 400,
      });
    });

    it('should handle negative dimensions', () => {
      const mockContainer = document.createElement('div');
      (mockContainer.getBoundingClientRect as jest.Mock).mockReturnValue({
        width: -100,
        height: -50,
        top: 0,
        left: 0,
        right: -100,
        bottom: -50,
      });

      const result = getChartDimensions(mockContainer, 400, 800);
      expect(result).toEqual({
        width: 800,
        height: 400,
      });
    });

    it('should handle very large dimensions', () => {
      const mockContainer = document.createElement('div');
      (mockContainer.getBoundingClientRect as jest.Mock).mockReturnValue({
        width: 10000,
        height: 5000,
        top: 0,
        left: 0,
        right: 10000,
        bottom: 5000,
      });

      const result = getChartDimensions(mockContainer, 400, 800);
      expect(result).toEqual({
        width: 10000,
        height: 5000,
      });
    });

    it('should handle decimal dimensions', () => {
      const mockContainer = document.createElement('div');
      (mockContainer.getBoundingClientRect as jest.Mock).mockReturnValue({
        width: 800.5,
        height: 400.25,
        top: 0,
        left: 0,
        right: 800.5,
        bottom: 400.25,
      });

      const result = getChartDimensions(mockContainer, 400, 800);
      expect(result).toEqual({
        width: 800.5,
        height: 400.25,
      });
    });

    it('should handle null default dimensions', () => {
      const mockContainer = document.createElement('div');
      (mockContainer.getBoundingClientRect as jest.Mock).mockReturnValue({
        width: 1000,
        height: 500,
        top: 0,
        left: 0,
        right: 1000,
        bottom: 500,
      });

      const result = getChartDimensions(mockContainer, null, null);
      expect(result).toEqual({
        width: 1000,
        height: 500,
      });
    });

    it('should handle undefined default dimensions', () => {
      const mockContainer = document.createElement('div');
      (mockContainer.getBoundingClientRect as jest.Mock).mockReturnValue({
        width: 1000,
        height: 500,
        top: 0,
        left: 0,
        right: 1000,
        bottom: 500,
      });

      const result = getChartDimensions(mockContainer, undefined, undefined);
      expect(result).toEqual({
        width: 1000,
        height: 500,
      });
    });

    it('should handle mixed null/undefined default dimensions', () => {
      const mockContainer = document.createElement('div');
      (mockContainer.getBoundingClientRect as jest.Mock).mockReturnValue({
        width: 1000,
        height: 500,
        top: 0,
        left: 0,
        right: 1000,
        bottom: 500,
      });

      const result = getChartDimensions(mockContainer, null, 800);
      expect(result).toEqual({
        width: 1000,
        height: 500,
      });
    });
  });
}); 