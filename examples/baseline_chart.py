"""
Baseline Chart Example

This example demonstrates how to create a simple baseline chart using the ultra-simplified API.
"""

import streamlit as st

from streamlit_lightweight_charts_pro import SinglePaneChart, render_chart
from streamlit_lightweight_charts_pro.charts.series import BaselineSeries
from streamlit_lightweight_charts_pro.data import BaselineData

# Create sample baseline data
data = [
    BaselineData("2018-12-22", 32.51),
    BaselineData("2018-12-23", 31.11),
    BaselineData("2018-12-24", 27.02),
    BaselineData("2018-12-25", 27.32),
    BaselineData("2018-12-26", 25.17),
    BaselineData("2018-12-27", 28.89),
    BaselineData("2018-12-28", 25.46),
    BaselineData("2018-12-29", 23.92),
    BaselineData("2018-12-30", 22.68),
    BaselineData("2018-12-31", 22.67),
]

# Create baseline series with ultra-simplified API
baseline_series = BaselineSeries(
    data=data,
    top_line_color="rgba(38, 166, 154, 1)",  # Direct styling parameter
    bottom_line_color="rgba(239, 83, 80, 1)",  # Direct styling parameter
    line_width=3,
)

# Create chart
chart = SinglePaneChart([baseline_series])

st.subheader("Baseline Chart with Ultra-Simplified API")

# Render the chart
render_chart(chart, key="baseline")
