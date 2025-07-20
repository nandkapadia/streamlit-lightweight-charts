"""
Price Volume Line Chart Example

This example demonstrates how to create a price-volume chart using line charts for price data.
"""

import pandas as pd
import streamlit as st

from dataSamples import get_candlestick_data, get_volume_data
from streamlit_lightweight_charts_pro import PriceVolumeChart

# Create a DataFrame with price and volume data
price_data = get_candlestick_data()
volume_data = get_volume_data()

# Create a combined DataFrame with price and volume
# Convert to DataFrame format
df = pd.DataFrame(
    {
        "datetime": [item.time for item in price_data],
        "open": [item.open for item in price_data],
        "high": [item.high for item in price_data],
        "low": [item.low for item in price_data],
        "close": [item.close for item in price_data],
        "volume": [item.value for item in volume_data[:len(price_data)]],  # Match the length
    }
)

# Create price-volume chart with line price type
chart = PriceVolumeChart(
    data=df,
    height=500,
)

st.subheader("Price with Volume Series Chart (Line)")

# Render the chart
chart.render(key="priceAndVolumeLine")
