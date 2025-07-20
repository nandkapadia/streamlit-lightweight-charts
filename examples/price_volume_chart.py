#!/usr/bin/env python3
"""
Price Volume Chart example with candlestick and volume.
"""

import streamlit as st
import pandas as pd

st.title("📊 Price Volume Chart Example")

# Create sample OHLCV data
df = pd.DataFrame(
    {
        "datetime": ["2022-01-17", "2022-01-18", "2022-01-19", "2022-01-20", "2022-01-21"],
        "open": [10.0, 9.8, 9.6, 9.9, 9.7],
        "high": [10.2, 10.1, 9.8, 10.0, 9.9],
        "low": [9.7, 9.5, 9.4, 9.6, 9.5],
        "close": [9.8, 9.6, 9.9, 9.7, 9.8],
        "volume": [1000, 1200, 800, 1500, 1100],
    }
)

st.write("### OHLCV Data:")
st.dataframe(df)

# Test PriceVolumeChart
st.write("### Test: PriceVolumeChart")
from streamlit_lightweight_charts_pro import PriceVolumeChart, render_chart

# Create PriceVolumeChart with default settings
price_volume_chart = PriceVolumeChart(
    data=df,
    # Candlestick options
    up_color="#4CAF50",
    down_color="#F44336",
    border_visible=False,
    wick_up_color="#4CAF50",
    wick_down_color="#F44336",
    # Volume options
    volume_color="#26a69a",
    volume_alpha=0.8,
    # Chart options
    height=400,
)

# Render the chart
render_chart(price_volume_chart, key="price_volume_chart_example")

st.write("### Features:")
st.write("- ✅ Candlestick chart in main area (75% of height)")
st.write("- ✅ Volume histogram in bottom area (25% of height)")
st.write("- ✅ Volume with 0.8 alpha transparency")
st.write("- ✅ Proper price scale configuration")
st.write("- ✅ Volume uses overlay price scale")

# Test without volume
st.write("### Test: PriceVolumeChart without Volume")
df_no_volume = df.drop(columns=["volume"])

price_volume_chart_no_vol = PriceVolumeChart(
    data=df_no_volume, up_color="#4CAF50", down_color="#F44336", border_visible=False, height=400
)

render_chart(price_volume_chart_no_vol, key="price_volume_chart_no_volume")

st.write("### Features (No Volume):")
st.write("- ✅ Candlestick chart only")
st.write("- ✅ No volume histogram")
st.write("- ✅ Chart adapts automatically")

# Test custom styling
st.write("### Test: Custom Styling")
price_volume_chart_custom = PriceVolumeChart(
    data=df,
    # Custom candlestick colors
    up_color="#00C851",
    down_color="#FF4444",
    border_visible=True,
    wick_up_color="#00C851",
    wick_down_color="#FF4444",
    # Custom volume styling
    volume_color="#2196F3",
    volume_alpha=0.6,
    # Custom chart options
    height=500,
)

render_chart(price_volume_chart_custom, key="price_volume_chart_custom")

st.write("### Custom Features:")
st.write("- ✅ Custom candlestick colors")
st.write("- ✅ Visible candle borders")
st.write("- ✅ Custom volume color and transparency")
st.write("- ✅ Larger chart height")

st.write("### Usage:")
st.code(
    """
from streamlit_lightweight_charts_pro import PriceVolumeChart, render_chart

# Create PriceVolumeChart
chart = PriceVolumeChart(
    data=df,  # DataFrame with OHLCV data
    volume_alpha=0.8,  # Volume transparency
    height=400
)

# Render the chart
render_chart(chart, key="my_chart")
"""
)
