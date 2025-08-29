import React, {useEffect, useRef, useCallback} from 'react'
import ReactDOM from 'react-dom'
import {Streamlit} from 'streamlit-component-lib'
import {StreamlitProvider, useRenderData} from 'streamlit-component-lib-react-hooks'
import LightweightCharts from './LightweightCharts'
import {ComponentConfig} from './types'
// import { ChartReadyDetector } from './utils/chartReadyDetection'
import {ResizeObserverManager} from './utils/resizeObserverManager'

const App: React.FC = () => {
  const renderData = useRenderData()
  const containerRef = useRef<HTMLDivElement>(null)
  const isReadyRef = useRef(false)
  const isMountedRef = useRef(false)
  const resizeObserverManager = useRef<ResizeObserverManager>(new ResizeObserverManager())
  const heightReportTimeout = useRef<NodeJS.Timeout | null>(null)
  const lastReportTime = useRef(0)
  const isReportingHeight = useRef(false) // Prevent recursive height reporting
  const lastReportedHeight = useRef(0) // Track last reported height to prevent unnecessary reports

  const handleChartsReady = () => {
    isReadyRef.current = true
  }

  // Enhanced height reporting with multiple detection methods
  const reportHeightWithFallback = useCallback(async () => {
    if (!containerRef.current || !isReadyRef.current || !isMountedRef.current) {
      return
    }

    try {
      // Method 1: Try container dimensions first
      let containerHeight = 0
      const chartHeight = renderData?.args?.height || 400

      try {
        containerHeight = containerRef.current.scrollHeight
      } catch (error) {
        console.warn('[StreamlitComponent] scrollHeight failed, trying alternative methods')
      }

      // Method 2: Try computed styles
      if (!containerHeight) {
        try {
          const computedStyle = window.getComputedStyle(containerRef.current)
          containerHeight = parseInt(computedStyle.height) || 0
        } catch (error) {
          console.warn('[StreamlitComponent] computed style method failed')
        }
      }

      // Method 3: Try offset dimensions
      if (!containerHeight) {
        try {
          containerHeight = containerRef.current.offsetHeight
        } catch (error) {
          console.warn('[StreamlitComponent] offsetHeight method failed')
        }
      }

      // Method 4: Try client dimensions
      if (!containerHeight) {
        try {
          containerHeight = containerRef.current.clientHeight
        } catch (error) {
          console.warn('[StreamlitComponent] clientHeight method failed')
        }
      }

      // Calculate total height
      const totalHeight = Math.max(containerHeight, chartHeight)
      const finalHeight = totalHeight + 20 // Add padding

      // Report height to Streamlit only if component is still mounted
      if (isMountedRef.current && typeof Streamlit !== 'undefined' && Streamlit.setFrameHeight) {
        try {
          Streamlit.setFrameHeight(finalHeight)
        } catch (error) {
          console.warn('[StreamlitComponent] Failed to set frame height:', error)
        }
      } else {
        console.warn(
          '[StreamlitComponent] Skipping height report - component not mounted or Streamlit not available'
        )
      }
    } catch (error) {
      console.error('[StreamlitComponent] Failed to report height:', error)
    }
  }, [renderData?.args?.height])

  // Debounced height reporting
  const debouncedReportHeight = useCallback(() => {
    // Don't schedule height reporting if component is not mounted
    if (!isMountedRef.current) {
      return
    }

    const now = Date.now()
    if (now - lastReportTime.current < 500) {
      // Increased from 100ms to 500ms
      // Throttle to max once every 500ms
      return
    }

    if (heightReportTimeout.current) {
      clearTimeout(heightReportTimeout.current)
    }

    heightReportTimeout.current = setTimeout(() => {
      // Check again if component is still mounted before reporting
      if (isMountedRef.current && !isReportingHeight.current) {
        lastReportTime.current = Date.now()
        reportHeightWithFallback()
      }
    }, 500) // Increased from 200ms to 500ms
  }, [reportHeightWithFallback])

  // Enhanced height reporting with ResizeObserver
  useEffect(() => {
    if (!containerRef.current) return

    // Report height immediately
    reportHeightWithFallback()

    // Set up ResizeObserver for height changes
    resizeObserverManager.current.addObserver(
      'streamlit-container',
      containerRef.current,
      entry => {
        // Don't process resize events if component is not mounted or if we're currently reporting height
        if (!isMountedRef.current || isReportingHeight.current) {
          return
        }

        // Handle both single entry and array of entries
        const entries = Array.isArray(entry) ? entry : [entry]

        entries.forEach(singleEntry => {
          if (singleEntry.target === containerRef.current) {
            const {width, height} = singleEntry.contentRect

            // Check if dimensions are valid and have actually changed significantly
            if (width > 0 && height > 0) {
              const currentHeight = lastReportedHeight.current
              const heightDiff = Math.abs(height - currentHeight)

              // Only report if height has changed significantly (more than 10px difference)
              if (heightDiff > 10) {
                debouncedReportHeight()
              } else {
                console.warn(
                  `[StreamlitComponent] Container resize ignored - change too small: ${heightDiff}px`
                )
              }
            }
          }
        })
      },
      {throttleMs: 200, debounceMs: 100} // Increased throttling to reduce frequency
    )

    return () => {
      if (heightReportTimeout.current) {
        clearTimeout(heightReportTimeout.current)
      }
    }
  }, [reportHeightWithFallback, debouncedReportHeight])

  // Enhanced height reporting with window resize
  useEffect(() => {
    const handleWindowResize = () => {
      debouncedReportHeight()
    }

    window.addEventListener('resize', handleWindowResize)

    return () => {
      window.removeEventListener('resize', handleWindowResize)
    }
  }, [debouncedReportHeight])

  // Cleanup on unmount
  useEffect(() => {
    isMountedRef.current = true

    // Capture the current ref value to avoid stale closure issues
    const currentResizeObserverManager = resizeObserverManager.current

    return () => {
      isMountedRef.current = false
      isReadyRef.current = false

      // Cleanup resize observers using captured reference
      if (currentResizeObserverManager) {
        currentResizeObserverManager.cleanup()
      }

      // Clear timeout
      if (heightReportTimeout.current) {
        clearTimeout(heightReportTimeout.current)
        heightReportTimeout.current = null
      }
    }
  }, [])

  // Report height when height prop changes
  useEffect(() => {
    if (isReadyRef.current && isMountedRef.current) {
      debouncedReportHeight()
    }
  }, [renderData?.args?.height, debouncedReportHeight])

  // Report height when config changes
  useEffect(() => {
    if (isReadyRef.current && isMountedRef.current) {
      // Small delay to ensure charts have rendered
      setTimeout(() => {
        debouncedReportHeight()
      }, 100)
    }
  }, [renderData, debouncedReportHeight])

  if (!renderData) {
    return <div>Loading...</div>
  }

  const config = renderData.args?.config as ComponentConfig
  const height = (renderData.args?.height as number) || 400

  return (
    <div ref={containerRef} style={{width: '100%', minHeight: height}}>
      <LightweightCharts config={config} height={height} onChartsReady={handleChartsReady} />
    </div>
  )
}

ReactDOM.render(
  <React.StrictMode>
    <StreamlitProvider>
      <App />
    </StreamlitProvider>
  </React.StrictMode>,
  document.getElementById('root')
)
