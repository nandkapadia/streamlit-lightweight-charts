"""
Price Volume Line Chart Example

This example demonstrates how to create a price-volume chart using line charts for price data.
"""

import pandas as pd
import streamlit as st

import streamlit_lightweight_charts_pro.dataSamples as data
from streamlit_lightweight_charts_pro import PriceVolumeChart, render_chart

# Create a DataFrame with price and volume data
price_data = pd.DataFrame(data.price_volume_series_area)
volume_data = pd.DataFrame(data.price_volume_series_histogram)

# Create a combined DataFrame with price and volume
df = pd.DataFrame(
    {
        "time": price_data["time"],
        "price": price_data["value"],
        "volume": volume_data["value"][: len(price_data)],  # Match the length
    }
)

# Create price-volume chart with line price type
chart = PriceVolumeChart(
    df=df,
    price_type="line",
    price_column="price",
    volume_column="volume",
    price_height=400,
    volume_height=100,
)

st.subheader("Price with Volume Series Chart (Line)")

# Render the chart
render_chart(chart, key="priceAndVolumeLine")
