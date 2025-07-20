"""
Data Toggling Example

This example demonstrates how to toggle between different datasets in an area chart using the ultra-simplified API.
"""

import streamlit as st

import streamlit_lightweight_charts_pro.dataSamples as data
from streamlit_lightweight_charts_pro import SinglePaneChart, render_chart
from streamlit_lightweight_charts_pro.charts.series import AreaSeries

st.subheader("Data Toggling for an Area Chart with Ultra-Simplified API")

data_select = st.sidebar.radio("Select data source:", ("Area 01", "Area 02"))

if data_select == "Area 01":
    # Create area series with first dataset
    area_series = AreaSeries(
        data=data.series_multiple_chart_area_01,
        top_color="rgba(46, 220, 135, 0.4)",
        bottom_color="rgba(40, 221, 100, 0)",
        line_color="#33D778",
    )
else:
    # Create area series with second dataset
    area_series = AreaSeries(
        data=data.series_multiple_chart_area_02,
        top_color="rgba(255, 87, 34, 0.4)",
        bottom_color="rgba(255, 87, 34, 0)",
        line_color="#FF5722",
    )

# Create chart
chart = SinglePaneChart([area_series])

# Render the chart
render_chart(chart, key="area")
