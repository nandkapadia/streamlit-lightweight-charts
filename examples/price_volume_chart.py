#!/usr/bin/env python3
"""
Price Volume Chart example with candlestick and volume.
"""

import pandas as pd
import streamlit as st
from datetime import datetime
from streamlit_lightweight_charts_pro import PriceVolumeChart
from examples.dataSamples import series_candlestick_chart, series_volume_chart

st.title("📊 Price Volume Chart Example")

def create_ohlcv_data():
    """Create OHLCV data by combining candlestick and volume data from dataSamples.py"""
    # Convert Unix timestamps to datetime strings for both datasets
    def timestamp_to_datetime(timestamp):
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
    
    # Create a dictionary to map datetime to volume data
    volume_dict = {}
    for item in series_volume_chart:
        dt_str = timestamp_to_datetime(item["datetime"])
        volume_dict[dt_str] = item["value"]
    
    # Combine candlestick data with volume data
    ohlcv_data = []
    for candle in series_candlestick_chart:
        dt_str = timestamp_to_datetime(candle["datetime"])
        volume = volume_dict.get(dt_str, 0)  # Default to 0 if no volume data
        
        ohlcv_data.append({
            "datetime": dt_str,
            "open": candle["open"],
            "high": candle["high"],
            "low": candle["low"],
            "close": candle["close"],
            "volume": volume
        })
    
    return pd.DataFrame(ohlcv_data)

# Create OHLCV data from dataSamples.py
df = create_ohlcv_data()

st.write("### OHLCV Data from dataSamples.py:")
st.dataframe(df)

# Test PriceVolumeChart
st.write("### Test: PriceVolumeChart")

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
price_volume_chart.render(key="price_volume_chart_example")

st.write("### Features:")
st.write("- ✅ Candlestick chart in main area (75% of height)")
st.write("- ✅ Volume histogram in bottom area (25% of height)")
st.write("- ✅ Volume with 0.8 alpha transparency")
st.write("- ✅ Proper price scale configuration")
st.write("- ✅ Volume uses overlay price scale")
st.write("- ✅ Data sourced from dataSamples.py")

# Test without volume
st.write("### Test: PriceVolumeChart without Volume")
df_no_volume = df.drop(columns=["volume"])

price_volume_chart_no_vol = PriceVolumeChart(
    data=df_no_volume, up_color="#4CAF50", down_color="#F44336", border_visible=False, height=400
)

price_volume_chart_no_vol.render(key="price_volume_chart_no_volume")

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

price_volume_chart_custom.render(key="price_volume_chart_custom")

st.write("### Custom Features:")
st.write("- ✅ Custom candlestick colors")
st.write("- ✅ Visible candle borders")
st.write("- ✅ Custom volume color and transparency")
st.write("- ✅ Larger chart height")

st.write("### Usage:")
st.code(
    """
from streamlit_lightweight_charts_pro import PriceVolumeChart
from examples.dataSamples import create_ohlcv_data

# Create OHLCV data from dataSamples.py
df = create_ohlcv_data()

# Create PriceVolumeChart
chart = PriceVolumeChart(
    data=df,  # DataFrame with OHLCV data
    volume_alpha=0.8,  # Volume transparency
    height=400
)

# Render the chart
chart.render(key="my_chart")
"""
)
