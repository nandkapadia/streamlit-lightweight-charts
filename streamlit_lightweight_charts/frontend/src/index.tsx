import React from 'react'
import ReactDOM from 'react-dom'
import { Streamlit } from 'streamlit-component-lib'
import { StreamlitProvider, useRenderData } from 'streamlit-component-lib-react-hooks'
import LightweightCharts from './LightweightCharts'
import { ComponentConfig } from './types'

const App: React.FC = () => {
  const renderData = useRenderData()
  const config = renderData.args["config"] as ComponentConfig
  const height = renderData.args["height"] as number || 400
  const width = renderData.args["width"] as number || 800

  if (!config) {
    return <div>No configuration provided</div>
  }

  return (
    <LightweightCharts 
      config={config}
      height={height}
      width={width}
    />
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

Streamlit.setComponentReady()
