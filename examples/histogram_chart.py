"""
Histogram Chart Example

This example demonstrates how to create a simple histogram chart using the new OOP architecture.
"""

import streamlit as st

from streamlit_lightweight_charts import HistogramChart, render_chart
from streamlit_lightweight_charts.data import HistogramData

# Create sample histogram data
data = [
    HistogramData("2018-12-22", 32.51),
    HistogramData("2018-12-23", 31.11),
    HistogramData("2018-12-24", 27.02),
    HistogramData("2018-12-25", 27.32),
    HistogramData("2018-12-26", 25.17),
    HistogramData("2018-12-27", 28.89),
    HistogramData("2018-12-28", 25.46),
    HistogramData("2018-12-29", 23.92),
    HistogramData("2018-12-30", 22.68),
    HistogramData("2018-12-31", 22.67),
]

# Create histogram chart
chart = HistogramChart(data)

st.subheader("Histogram Chart sample")

# Render the chart
render_chart(chart, key="histogram")
