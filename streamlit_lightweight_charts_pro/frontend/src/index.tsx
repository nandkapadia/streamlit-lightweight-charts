import React, { useEffect, useRef, useCallback } from 'react'
import ReactDOM from 'react-dom'
import { Streamlit } from 'streamlit-component-lib'
import { StreamlitProvider, useRenderData } from 'streamlit-component-lib-react-hooks'
import LightweightCharts from './LightweightCharts'
import { ComponentConfig } from './types'

const App: React.FC = () => {
  const renderData = useRenderData()
  const config = renderData.args["config"] as ComponentConfig
  const height = renderData.args["height"] as number | null || 400
  const width = renderData.args["width"] as number | null || null  // Default to null for 100% width
  const containerRef = useRef<HTMLDivElement>(null)
  const isReadyRef = useRef(false)
  const isMountedRef = useRef(true)
  
  // Generate unique component ID for debugging
  const componentId = useRef(`component_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`)
  
      // Component initialized

  // Report component ready state
  useEffect(() => {
    if (!isReadyRef.current) {
      // Add a small delay to ensure proper registration
      setTimeout(() => {
        if (isMountedRef.current) {
          try {
            if (typeof Streamlit !== 'undefined' && Streamlit.setComponentReady) {
              isReadyRef.current = true
              Streamlit.setComponentReady()
              // Component ready state set
            } else {
              console.warn('[StreamlitComponent] Streamlit object not available for component ready')
            }
          } catch (error) {
            console.warn('[StreamlitComponent] Failed to set component ready:', error)
          }
        }
      }, 100)
    }
  }, [])

  // Handle charts ready callback
  const handleChartsReady = useCallback(() => {
    // Trigger height recalculation when charts are ready
    setTimeout(() => {
      if (containerRef.current && isReadyRef.current && isMountedRef.current) {
        const containerHeight = containerRef.current.scrollHeight
        const chartHeight = height || 400
        const totalHeight = Math.max(containerHeight, chartHeight)
        const finalHeight = totalHeight + 20
        
        try {
          if (typeof Streamlit !== 'undefined' && Streamlit.setFrameHeight) {
            Streamlit.setFrameHeight(finalHeight)
            // Component set frame height
          } else {
            console.warn('[StreamlitComponent] Streamlit object not available')
          }
        } catch (error) {
          console.warn('[StreamlitComponent] Failed to set frame height:', error)
        }
      }
    }, 50)
  }, [height])

  // Report frame height changes
  useEffect(() => {
    let heightReportTimeout: NodeJS.Timeout | null = null
    
    const reportHeight = () => {
      if (containerRef.current && isReadyRef.current && isMountedRef.current) {
        const containerHeight = containerRef.current.scrollHeight
        const chartHeight = height || 400
        const totalHeight = Math.max(containerHeight, chartHeight)
        
        // Add some padding for better appearance
        const finalHeight = totalHeight + 20
        
        try {
          if (typeof Streamlit !== 'undefined' && Streamlit.setFrameHeight) {
            Streamlit.setFrameHeight(finalHeight)
            // Component report height
          } else {
            console.warn('[StreamlitComponent] Streamlit object not available for height report')
          }
        } catch (error) {
          console.warn('[StreamlitComponent] Failed to report height:', error)
        }
      }
    }

    let lastReportTime = 0
    const debouncedReportHeight = () => {
      const now = Date.now()
      if (now - lastReportTime < 100) {
        // Throttle to max once every 100ms
        return
      }
      
      if (heightReportTimeout) {
        clearTimeout(heightReportTimeout)
      }
      heightReportTimeout = setTimeout(() => {
        lastReportTime = Date.now()
        reportHeight()
      }, 200)
    }

    // Report height immediately
    reportHeight()

    // Set up a ResizeObserver to report height changes
    if (containerRef.current) {
      const resizeObserver = new ResizeObserver(() => {
        debouncedReportHeight()
      })
      
      resizeObserver.observe(containerRef.current)
      
      return () => {
        if (heightReportTimeout) {
          clearTimeout(heightReportTimeout)
        }
        resizeObserver.disconnect()
      }
    }
  }, [height]) // Remove config dependency to prevent unnecessary re-runs

  // Cleanup effect to prevent messages after unmount
  useEffect(() => {
    return () => {
      isMountedRef.current = false
      // Component unmounted
    }
  }, [])

  if (!config) {
    return <div>No configuration provided</div>
  }

  return (
    <div ref={containerRef} style={{ width: '100%', minHeight: '200px' }}>
      <LightweightCharts 
        config={config}
        height={height}
        width={width}
        onChartsReady={handleChartsReady}
      />
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
