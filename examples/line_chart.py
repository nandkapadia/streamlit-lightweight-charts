"""
Line Chart Example

This example demonstrates how to create a simple line chart using the new OOP architecture.
"""

import streamlit as st

from streamlit_lightweight_charts import LineChart, render_chart
from streamlit_lightweight_charts.data import SingleValueData

# Create sample data
data = [
    SingleValueData("2018-12-22", 32.51),
    SingleValueData("2018-12-23", 31.11),
    SingleValueData("2018-12-24", 27.02),
    SingleValueData("2018-12-25", 27.32),
    SingleValueData("2018-12-26", 25.17),
    SingleValueData("2018-12-27", 28.89),
    SingleValueData("2018-12-28", 25.46),
    SingleValueData("2018-12-29", 23.92),
    SingleValueData("2018-12-30", 22.68),
    SingleValueData("2018-12-31", 22.67),
]

# Create line chart
chart = LineChart(data)

st.subheader("Line Chart sample")

# Render the chart
render_chart(chart, key="line")
