"""
Data Toggling Example

This example demonstrates how to toggle between different datasets in an area chart.
"""

import streamlit as st

import streamlit_lightweight_charts.dataSamples as data
from streamlit_lightweight_charts import AreaChart, render_chart

st.subheader("Data Toggling for an Area Chart")

data_select = st.sidebar.radio("Select data source:", ("Area 01", "Area 02"))

if data_select == "Area 01":
    # Create area chart with first dataset
    chart = AreaChart(data.series_multiple_chart_area_01)
else:
    # Create area chart with second dataset
    chart = AreaChart(data.series_multiple_chart_area_02)

# Render the chart
render_chart(chart, key="area")
