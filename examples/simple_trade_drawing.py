"""
Simple Trade Drawing Example

This example demonstrates how to draw trades on a chart using the new OOP architecture.
"""

import streamlit as st

from streamlit_lightweight_charts_pro import CandlestickChart, render_chart
from streamlit_lightweight_charts_pro.data import OhlcData, Trade

# Create sample OHLC data
data = [
    OhlcData("2022-01-01", 100, 102, 99, 101),
    OhlcData("2022-01-02", 101, 104, 100, 102),
    OhlcData("2022-01-03", 102, 103, 100, 101),
    OhlcData("2022-01-04", 101, 106, 100, 105),
    OhlcData("2022-01-05", 105, 105, 102, 103),
    OhlcData("2022-01-06", 103, 109, 102, 108),
    OhlcData("2022-01-07", 108, 111, 107, 110),
]

# Create sample trades
trades = [
    Trade("2022-01-02", 102, "2022-01-04", 105, 1),
    Trade("2022-01-05", 103, "2022-01-07", 110, 1),
]

# Create candlestick chart
chart = CandlestickChart(data, trades=trades)

st.subheader("Simple Trade Drawing Example")

# Render the chart
render_chart(chart, key="simple_trade")
