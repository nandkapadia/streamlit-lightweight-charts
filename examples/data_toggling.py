"""
Data Toggling Example

This example demonstrates how to toggle between different datasets in an area chart using the ultra-simplified API.
"""

import streamlit as st

from dataSamples import get_multi_area_data_1, get_multi_area_data_2
from streamlit_lightweight_charts_pro import SinglePaneChart
from streamlit_lightweight_charts_pro.charts.series import AreaSeries

st.subheader("Data Toggling for an Area Chart with Ultra-Simplified API")

data_select = st.sidebar.radio("Select data source:", ("Area 01", "Area 02"))

if data_select == "Area 01":
    # Create area series with first dataset
    area_series = AreaSeries(
        data=get_multi_area_data_1(),
        top_color="rgba(46, 220, 135, 0.4)",
        bottom_color="rgba(40, 221, 100, 0)",
        line_color="#33D778",
    )
else:
    # Create area series with second dataset
    area_series = AreaSeries(
        data=get_multi_area_data_2(),
        top_color="rgba(255, 87, 34, 0.4)",
        bottom_color="rgba(255, 87, 34, 0)",
        line_color="#FF5722",
    )

# Create chart
chart = SinglePaneChart([area_series])

# Render the chart
chart.render(key="area")
