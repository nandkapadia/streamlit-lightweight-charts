import {IChartApi} from 'lightweight-charts'

/**
 * Utility class for detecting when charts are ready with multiple fallback methods
 */
export class ChartReadyDetector {
  /**
   * Wait for chart to be fully ready with proper dimensions
   */
  static async waitForChartReady(
    chart: IChartApi,
    container: HTMLElement,
    options: {
      minWidth?: number
      minHeight?: number
      maxAttempts?: number
      baseDelay?: number
    } = {}
  ): Promise<boolean> {
    const {minWidth = 100, minHeight = 100, maxAttempts = 15, baseDelay = 200} = options

    return new Promise(resolve => {
      const checkReady = (attempts = 0) => {
        try {
          if (chart && container) {
            // Method 1: Try chart API first
            try {
              const chartElement = chart.chartElement()
              if (chartElement) {
                const chartRect = chartElement.getBoundingClientRect()
                if (chartRect.width >= minWidth && chartRect.height >= minHeight) {
                  resolve(true)
                  return
                }
              }
            } catch (apiError) {
              // Chart API method failed, trying DOM fallback
            }

            // Method 2: DOM fallback
            try {
              const containerRect = container.getBoundingClientRect()
              if (containerRect.width >= minWidth && containerRect.height >= minHeight) {
                resolve(true)
                return
              }
            } catch (domError) {
              // DOM method failed
            }
          }

          if (attempts < maxAttempts) {
            const delay = baseDelay * Math.pow(1.5, attempts)
            setTimeout(() => checkReady(attempts + 1), delay)
          } else {
            resolve(false)
          }
        } catch (error) {
          if (attempts < maxAttempts) {
            const delay = baseDelay * Math.pow(1.5, attempts)
            setTimeout(() => checkReady(attempts + 1), delay)
          } else {
            resolve(false)
          }
        }
      }

      checkReady()
    })
  }

  /**
   * Check if chart is ready synchronously (for immediate checks)
   */
  static isChartReadySync(
    chart: IChartApi | null,
    container: HTMLElement | null,
    minWidth: number = 100,
    minHeight: number = 100
  ): boolean {
    try {
      if (!chart || !container) return false

      // Try chart API first
      try {
        const chartElement = chart.chartElement()
        if (chartElement) {
          const chartRect = chartElement.getBoundingClientRect()
          if (chartRect.width >= minWidth && chartRect.height >= minHeight) {
            return true
          }
        }
      } catch (error) {
        // API method failed, continue to DOM
      }

      // Try DOM fallback
      try {
        const containerRect = container.getBoundingClientRect()
        return containerRect.width >= minWidth && containerRect.height >= minHeight
      } catch (error) {
        return false
      }
    } catch (error) {
      return false
    }
  }

  /**
   * Wait for specific chart element to be ready
   */
  static async waitForElementReady(
    selector: string,
    container: HTMLElement,
    options: {
      maxAttempts?: number
      baseDelay?: number
    } = {}
  ): Promise<Element | null> {
    const {maxAttempts = 10, baseDelay = 100} = options

    return new Promise(resolve => {
      const checkElement = (attempts = 0) => {
        try {
          const element = container.querySelector(selector)
          if (element) {
            resolve(element)
            return
          }

          if (attempts < maxAttempts) {
            const delay = baseDelay * Math.pow(1.5, attempts)
            setTimeout(() => checkElement(attempts + 1), delay)
          } else {
            resolve(null)
          }
        } catch (error) {
          if (attempts < maxAttempts) {
            const delay = baseDelay * Math.pow(1.5, attempts)
            setTimeout(() => checkElement(attempts + 1), delay)
          } else {
            resolve(null)
          }
        }
      }

      checkElement()
    })
  }
}
