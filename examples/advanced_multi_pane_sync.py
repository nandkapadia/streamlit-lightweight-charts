"""
Advanced Multi-Pane Synchronized Charts Example

This example demonstrates:
- Multiple synchronized chart panes
- Full crosshair and time range synchronization
- Dynamic data updates
- Custom indicators
"""

from datetime import datetime

import numpy as np
import pandas as pd
import streamlit as st

from streamlit_lightweight_charts_pro import MultiPaneChart
from streamlit_lightweight_charts_pro.charts import (
    CandlestickSeries,
    HistogramSeries,
    LineSeries,
    SinglePaneChart,
)
from streamlit_lightweight_charts_pro.data import HistogramData, OhlcData, SingleValueData


# Generate sample data
@st.cache_data
def generate_sample_data(days_=100):
    """Generate sample OHLCV data"""
    dates = pd.date_range(end=datetime.now(), periods=days_, freq="D")

    # Generate price data
    close_prices = 100 + np.cumsum(np.random.randn(days_) * 2)
    high_prices = close_prices + np.abs(np.random.randn(days_))
    low_prices = close_prices - np.abs(np.random.randn(days_))
    open_prices = np.roll(close_prices, 1)
    open_prices[0] = close_prices[0]

    # Generate volume
    volume = np.abs(np.random.randn(days_) * 1000000 + 5000000).astype(int)

    # Create OHLCV dataframe
    df_ = pd.DataFrame(
        {
            "time": dates,
            "open": open_prices,
            "high": high_prices,
            "low": low_prices,
            "close": close_prices,
            "volume": volume,
        }
    )

    # Calculate indicators
    df_["sma_20"] = df_["close"].rolling(window=20).mean()
    df_["sma_50"] = df_["close"].rolling(window=50).mean()
    df_["rsi"] = calculate_rsi(df_["close"])
    df_["macd"], df_["signal"], df_["histogram"] = calculate_macd(df_["close"])

    return df_


def calculate_rsi(prices, period=14):
    """Calculate RSI indicator"""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))


def calculate_macd(prices, fast=12, slow=26, signal=9):
    """Calculate MACD indicator"""
    exp1 = prices.ewm(span=fast, adjust=False).mean()
    exp2 = prices.ewm(span=slow, adjust=False).mean()
    macd = exp1 - exp2
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    histogram = macd - signal_line
    return macd, signal_line, histogram


st.set_page_config(page_title="Advanced Multi-Pane Charts", layout="wide")

st.title("Advanced Multi-Pane Synchronized Charts")
st.markdown(
    """
This example demonstrates the full capabilities of the enhanced streamlit-lightweight-charts 
library:
- **Synchronized charts**: Time range and crosshair sync across all panes
- **Multiple indicators**: SMA, RSI, MACD in separate panes
- **Interactive features**: Dynamic updates and custom styling
"""
)

# Sidebar controls
with st.sidebar:
    st.header("Chart Controls")

    # Data settings
    days = st.slider("Days of data", 30, 365, 100)

    # Theme settings
    st.subheader("Theme")
    theme = st.selectbox("Color theme", ["Light", "Dark", "Trading View"])

    # Indicator settings
    st.subheader("Indicators")
    show_sma = st.checkbox("Show SMA", True)
    show_volume = st.checkbox("Show Volume", True)
    show_rsi = st.checkbox("Show RSI", True)
    show_macd = st.checkbox("Show MACD", True)

    # Update data
    if st.button("Refresh Data"):
        st.cache_data.clear()

# Generate data
df = generate_sample_data(days)

# Convert data to objects
df["time"] = pd.to_datetime(df["time"]).dt.strftime("%Y-%m-%d")
df_dict = df.to_dict("records")

candlestick_data = [
    OhlcData(row["time"], row["open"], row["high"], row["low"], row["close"]) for row in df_dict
]

volume_data = [HistogramData(row["time"], row["volume"]) for row in df_dict]

# Create charts
candlestick_series = CandlestickSeries(data=candlestick_data)
candlestick_chart = SinglePaneChart(series=candlestick_series)
chart = MultiPaneChart()
chart.add_pane(candlestick_chart)

if show_volume:
    volume_series = HistogramSeries(data=volume_data)
    volume_chart = SinglePaneChart(series=volume_series)
    chart.add_pane(volume_chart)

if show_sma:
    sma_20_data = [
        SingleValueData(row["time"], row["sma_20"]) for row in df_dict if pd.notna(row["sma_20"])
    ]
    sma_20_series = LineSeries(data=sma_20_data)
    sma_20_chart = SinglePaneChart(series=sma_20_series)
    chart.add_pane(sma_20_chart)

    sma_50_data = [
        SingleValueData(row["time"], row["sma_50"]) for row in df_dict if pd.notna(row["sma_50"])
    ]
    sma_50_series = LineSeries(data=sma_50_data)
    sma_50_chart = SinglePaneChart(series=sma_50_series)
    chart.add_pane(sma_50_chart)

if show_rsi:
    rsi_data = [SingleValueData(row["time"], row["rsi"]) for row in df_dict if pd.notna(row["rsi"])]
    rsi_series = LineSeries(data=rsi_data)
    rsi_chart = SinglePaneChart(series=rsi_series)
    chart.add_pane(rsi_chart)

if show_macd:
    macd_data = [
        SingleValueData(row["time"], row["macd"]) for row in df_dict if pd.notna(row["macd"])
    ]
    macd_series = LineSeries(data=macd_data)
    macd_chart = SinglePaneChart(series=macd_series)
    chart.add_pane(macd_chart)

    signal_data = [
        SingleValueData(row["time"], row["signal"]) for row in df_dict if pd.notna(row["signal"])
    ]
    signal_series = LineSeries(data=signal_data)
    signal_chart = SinglePaneChart(series=signal_series)
    chart.add_pane(signal_chart)

    hist_data = [
        SingleValueData(row["time"], row["histogram"])
        for row in df_dict
        if pd.notna(row["histogram"])
    ]
    hist_series = LineSeries(data=hist_data)
    hist_chart = SinglePaneChart(series=hist_series)
    chart.add_pane(hist_chart)

# Render the chart
chart.render(key="advanced_multipane")
