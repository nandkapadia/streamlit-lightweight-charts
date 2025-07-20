"""
Multi-Pane Chart Example

This example demonstrates how to create a multi-pane chart with candlestick, histogram, and baseline series using the ultra-simplified API.
"""

import streamlit as st

import streamlit_lightweight_charts_pro.dataSamples as data
from streamlit_lightweight_charts_pro import MultiPaneChart, SinglePaneChart, render_chart
from streamlit_lightweight_charts_pro.charts.series import (
    CandlestickSeries,
    HistogramSeries,
    BaselineSeries,
)
from streamlit_lightweight_charts_pro.data import BaselineData, HistogramData, OhlcData

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

# Create series with ultra-simplified API
candlestick_series = CandlestickSeries(
    data=candlestick_data, up_color="#26a69a", down_color="#ef5350"
)

histogram_series = HistogramSeries(data=histogram_data, color="#2196F3", base=0)

baseline_series = BaselineSeries(
    data=baseline_data,
    top_line_color="rgba(38, 166, 154, 1)",
    bottom_line_color="rgba(239, 83, 80, 1)",
)

# Create single pane charts
candlestick_chart = SinglePaneChart([candlestick_series])
histogram_chart = SinglePaneChart([histogram_series])
baseline_chart = SinglePaneChart([baseline_series])

# Create multi-pane chart
chart = MultiPaneChart([candlestick_chart, histogram_chart, baseline_chart])

st.subheader("Multipane Chart with Ultra-Simplified API")

# Render the chart
render_chart(chart, key="multipane")
