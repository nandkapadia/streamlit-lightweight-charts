"""
Bar Chart Example

This example demonstrates how to create a simple bar chart using the new OOP architecture.
"""

import streamlit as st

from streamlit_lightweight_charts import BarChart, render_chart
from streamlit_lightweight_charts.data import OhlcData

# Create sample OHLC data
data = [
    OhlcData("2018-12-22", 10.0, 10.63, 9.49, 9.55),
    OhlcData("2018-12-23", 9.55, 10.30, 9.42, 9.94),
    OhlcData("2018-12-24", 9.94, 10.17, 9.92, 9.78),
    OhlcData("2018-12-25", 9.78, 10.59, 9.18, 9.51),
    OhlcData("2018-12-26", 9.51, 10.46, 9.10, 10.17),
    OhlcData("2018-12-27", 10.17, 10.96, 10.16, 10.47),
    OhlcData("2018-12-28", 10.47, 11.39, 10.40, 10.81),
    OhlcData("2018-12-29", 10.81, 11.60, 10.30, 10.75),
    OhlcData("2018-12-30", 10.75, 11.60, 10.49, 10.93),
    OhlcData("2018-12-31", 10.93, 11.53, 10.76, 10.96),
]

# Create bar chart
chart = BarChart(data)

st.subheader("Bar Chart sample")

# Render the chart
render_chart(chart, key="bar")
