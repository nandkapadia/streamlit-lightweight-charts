"""
Price Volume Chart Example

This example demonstrates how to create a price-volume chart using the new OOP architecture.
The volume is now displayed as an overlay histogram on the same chart.
"""

import pandas as pd
import streamlit as st

import streamlit_lightweight_charts.dataSamples as data
from streamlit_lightweight_charts import PriceVolumeChart, render_chart

# Create a DataFrame with OHLC and volume data
# Combine candlestick data with volume data
candlestick_data = pd.DataFrame(data.series_candlestick_chart)
volume_data = pd.DataFrame(data.price_volume_series_histogram)

# Create a combined DataFrame with OHLC and volume
df = pd.DataFrame(
    {
        "time": candlestick_data["time"],
        "open": candlestick_data["open"],
        "high": candlestick_data["high"],
        "low": candlestick_data["low"],
        "close": candlestick_data["close"],
        "volume": volume_data["value"][: len(candlestick_data)],  # Match the length
    }
)

# Create price-volume chart with candlestick price type and overlay volume
chart = PriceVolumeChart(df=df, price_type="candlestick", height=500, volume_column="volume")

st.subheader("Price with Volume Overlay Chart sample")

# Render the chart
render_chart(chart, key="priceAndVolume")
