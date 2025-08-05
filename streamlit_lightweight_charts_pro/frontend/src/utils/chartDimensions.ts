import { IChartApi, ISeriesApi } from 'lightweight-charts';

/**
 * Get chart dimensions using requestAnimationFrame approach
 * 
 * This function runs inside a RequestAnimationFrame so that the chart has a chance to 
 * render once before querying the dimensions.
 * 
 * @param chart - The IChartAPI reference returned by LightweightCharts.createChart
 * @param container - The container element that holds the chart
 * @param mainSeries - Optional ISeriesAPI reference returned when adding data (e.g., chart.addLineSeries(...))
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
  return new Promise((resolve) => {
    // Run inside a RequestAnimationFrame so that the chart has a chance to 
    // render once before querying the dimensions.
    requestAnimationFrame(() => {
      try {
        // Check if chart is disposed
        if (!chart || !chart.chartElement) {
          console.warn('Chart is disposed or invalid');
          resolve({
            timeScalePositionAndSize: { x: 0, y: 0, height: 35, width: 0 },
            priceScalePositionAndSize: { x: 0, y: 0, height: 0, width: 70 },
            containerDimensions: { width: 0, height: 0 }
          });
          return;
        }
        
        // Additional check for chart validity
        try {
          chart.chartElement()
        } catch (error) {
          console.warn('Chart is disposed, cannot get dimensions');
          resolve({
            timeScalePositionAndSize: { x: 0, y: 0, height: 35, width: 0 },
            priceScalePositionAndSize: { x: 0, y: 0, height: 0, width: 70 },
            containerDimensions: { width: 0, height: 0 }
          });
          return;
        }

        const containerElement = container;
        const containerDimensions = containerElement.getBoundingClientRect();

        // chart is the IChartAPI reference returned by LightweightCharts.createChart
        const timeScale = chart.timeScale();
        if (!timeScale) {
          console.warn('Time scale is not available');
          resolve({
            timeScalePositionAndSize: { x: 0, y: 0, height: 35, width: 0 },
            priceScalePositionAndSize: { x: 0, y: 0, height: 0, width: 70 },
            containerDimensions: { width: containerDimensions.width || 0, height: containerDimensions.height || 0 }
          });
          return;
        }

        const timeScaleWidth = timeScale.width();
        const timeScaleHeight = timeScale.height();

              // mainSeries is the ISeriesAPI reference returned when adding data
        // for example with: chart.addLineSeries(...)
        let priceScaleWidth = 70; // Default fallback
        if (mainSeries) {
          try {
            const priceScale = mainSeries.priceScale();
            if (priceScale && typeof priceScale.width === 'function') {
              priceScaleWidth = priceScale.width();
            }
          } catch (error) {
            console.debug('Could not get price scale width from main series, using default:', error);
            // Fallback to default price scale
            try {
              const priceScale = chart.priceScale('right');
              if (priceScale && typeof priceScale.width === 'function') {
                priceScaleWidth = priceScale.width();
              }
            } catch (fallbackError) {
              console.debug('Could not get price scale width from default scale, using fallback:', fallbackError);
            }
          }
        } else {
          // Fallback to default price scale if no main series provided
          try {
            const priceScale = chart.priceScale('right');
            if (priceScale && typeof priceScale.width === 'function') {
              priceScaleWidth = priceScale.width();
            }
          } catch (error) {
            console.debug('Could not get price scale width, using fallback:', error);
          }
        }

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

              // Only log in development mode to reduce noise
        if (process.env.NODE_ENV === 'development') {
          console.log({ timeScalePositionAndSize, priceScalePositionAndSize });
        }
        resolve({ timeScalePositionAndSize, priceScalePositionAndSize, containerDimensions });
      } catch (error) {
        console.warn('Error getting chart dimensions:', error);
        resolve({
          timeScalePositionAndSize: { x: 0, y: 0, height: 35, width: 0 },
          priceScalePositionAndSize: { x: 0, y: 0, height: 0, width: 70 },
          containerDimensions: { width: 0, height: 0 }
        });
      }
    });
  });
}; 