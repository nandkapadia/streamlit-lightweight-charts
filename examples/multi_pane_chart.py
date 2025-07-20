"""
Multi-Pane Chart Example

This example demonstrates how to create a multi-pane chart with candlestick, histogram, and baseline series using the ultra-simplified API.
"""

import streamlit as st

from dataSamples import (
    get_baseline_data,
    get_candlestick_data,
    get_volume_data,
)
from streamlit_lightweight_charts_pro import MultiPaneChart, SinglePaneChart
from streamlit_lightweight_charts_pro.charts.series import (
    BaselineSeries,
    CandlestickSeries,
    HistogramSeries,
)

# Get sample data
candlestick_data = get_candlestick_data()
baseline_data = get_baseline_data()
histogram_data = get_volume_data()

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
chart.render(key="multipane")
