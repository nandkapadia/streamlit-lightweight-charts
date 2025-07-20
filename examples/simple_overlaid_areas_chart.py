"""
Simple Overlaid Areas Chart Example

This example demonstrates how to create overlaid area charts with markers using a single chart with multiple series.
"""

import streamlit as st

import streamlit_lightweight_charts_pro.dataSamples as data
from streamlit_lightweight_charts_pro import render_chart
from streamlit_lightweight_charts_pro.charts import AreaSeries, Chart
from streamlit_lightweight_charts_pro.charts.options import (
    ChartOptions,
    GridLineOptions,
    GridOptions,
    LayoutOptions,
    PriceScaleMargins,
    PriceScaleOptions,
    TimeScaleOptions,
)
from streamlit_lightweight_charts_pro.data import Marker, MarkerPosition, MarkerShape
from streamlit_lightweight_charts_pro.type_definitions.colors import Background
from streamlit_lightweight_charts_pro.type_definitions.enums import LineStyle, PriceScaleMode

# Create chart options
chart_options = ChartOptions(
    layout=LayoutOptions(background=Background.solid("#100841"), text_color="#ffffff"),
    grid=GridOptions(
        vert_lines=GridLineOptions(color="rgba(197, 203, 206, 0.4)", style=LineStyle.SOLID),
        horz_lines=GridLineOptions(color="rgba(197, 203, 206, 0.4)", style=LineStyle.SOLID),
    ),
    right_price_scale=PriceScaleOptions(
        scale_margins=PriceScaleMargins(top=0.1, bottom=0.1),
        mode=PriceScaleMode.NORMAL,
        border_color="rgba(197, 203, 206, 0.4)",
    ),
    time_scale=TimeScaleOptions(border_color="rgba(197, 203, 206, 0.4)"),
)

# Create markers for first series
markers1 = [
    Marker(
        time="2019-04-08",
        position=MarkerPosition.ABOVE_BAR,
        color="rgba(255, 192, 0, 1)",
        shape=MarkerShape.ARROW_DOWN,
        text="H",
        size=3,
    ),
    Marker(
        time="2019-05-13",
        position=MarkerPosition.BELOW_BAR,
        color="rgba(255, 192, 0, 1)",
        shape=MarkerShape.ARROW_UP,
        text="L",
        size=3,
    ),
]

# Create markers for second series
markers2 = [
    Marker(
        time="2019-05-03",
        position=MarkerPosition.ABOVE_BAR,
        color="rgba(67, 83, 254, 1)",
        shape=MarkerShape.ARROW_DOWN,
        text="PEAK",
        size=3,
    )
]

# Create area series
series1 = AreaSeries(
    data=data.series_multiple_chart_area_01,
    options={
        "topColor": "rgba(255, 192, 0, 0.7)",
        "bottomColor": "rgba(255, 192, 0, 0.3)",
        "lineColor": "rgba(255, 192, 0, 1)",
        "lineWidth": 2,
    },
    markers=markers1,
)

series2 = AreaSeries(
    data=data.series_multiple_chart_area_02,
    options={
        "topColor": "rgba(67, 83, 254, 0.7)",
        "bottomColor": "rgba(67, 83, 254, 0.3)",
        "lineColor": "rgba(67, 83, 254, 1)",
        "lineWidth": 2,
    },
    markers=markers2,
)

# Create a single chart with both series
chart = Chart([series1, series2], options=chart_options)

st.subheader("Overlaid Series with Markers (Single Chart)")

# Render the chart
render_chart(chart, key="simple_overlaid")
