"""
Multi-Pane Chart Example

This example demonstrates how to create a multi-pane chart with candlestick, histogram, and baseline series.
"""

import streamlit as st

import streamlit_lightweight_charts.dataSamples as data
from streamlit_lightweight_charts import MultiPaneChart, render_chart
from streamlit_lightweight_charts.charts import BaselineChart, CandlestickChart, HistogramChart
from streamlit_lightweight_charts.data import BaselineData, HistogramData, OhlcData

# Convert dictionary data to proper data objects
candlestick_data = [
    OhlcData(item["time"], item["open"], item["high"], item["low"], item["close"])
    for item in data.price_candlestick_multipane
]

baseline_data = [
    BaselineData(item["time"], item["value"]) for item in data.price_baseline_multipane
]

histogram_data = [
    HistogramData(item["time"], item["value"]) for item in data.price_volume_multipane
]

# Create charts
candlestick_chart = CandlestickChart(data=candlestick_data)
histogram_chart = HistogramChart(data=histogram_data)
baseline_chart = BaselineChart(data=baseline_data)

# Create multi-pane chart
chart = MultiPaneChart()
chart.add_pane(candlestick_chart)
chart.add_pane(histogram_chart)
chart.add_pane(baseline_chart)

st.subheader("Multipane Chart with Watermark")

# Render the chart
render_chart(chart, key="multipane")
