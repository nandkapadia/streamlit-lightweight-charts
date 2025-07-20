"""
Multi-Pane Charts with Pandas Example

This example demonstrates how to create multi-pane charts using pandas data with yfinance.
"""

import numpy as np
import streamlit as st
import yfinance as yf

from streamlit_lightweight_charts_pro import MultiPaneChart
from streamlit_lightweight_charts_pro.charts import (
    CandlestickSeries,
    HistogramSeries,
    LineSeries,
    SinglePaneChart,
)
from streamlit_lightweight_charts_pro.data import HistogramData, OhlcData, SingleValueData

COLOR_BULL = "rgba(38,166,154,0.9)"  # #26a69a
COLOR_BEAR = "rgba(239,83,80,0.9)"  # #ef5350

# Request historic pricing data via finance.yahoo.com API
df = yf.Ticker("AAPL").history(period="4mo")[["Open", "High", "Low", "Close", "Volume"]]

# Some data wrangling to match required format
df = df.reset_index()
df.columns = ["time", "open", "high", "low", "close", "volume"]  # rename columns
df["time"] = df["time"].dt.strftime("%Y-%m-%d")  # Date to string
df["color"] = np.where(df["open"] > df["close"], COLOR_BEAR, COLOR_BULL)  # bull or bear

# Calculate simple moving averages instead of MACD
df["sma_20"] = df["close"].rolling(window=20).mean()
df["sma_50"] = df["close"].rolling(window=50).mean()

# Convert DataFrame to list of dictionaries
df_dict = df.to_dict("records")

# Convert to data objects
candlestick_data = [
    OhlcData(row["time"], row["open"], row["high"], row["low"], row["close"]) for row in df_dict
]

volume_data = [HistogramData(row["time"], row["volume"]) for row in df_dict]

sma_20_data = [
    SingleValueData(row["time"], row["sma_20"])
    for row in df_dict
    if not np.isnan(row["sma_20"])
]

sma_50_data = [
    SingleValueData(row["time"], row["sma_50"])
    for row in df_dict
    if not np.isnan(row["sma_50"])
]

# Create charts
candlestick_series = CandlestickSeries(data=candlestick_data)
candlestick_chart = SinglePaneChart(series=candlestick_series)

volume_series = HistogramSeries(data=volume_data)
volume_chart = SinglePaneChart(series=volume_series)

sma_20_series = LineSeries(data=sma_20_data, color="#FF6B6B")
sma_20_chart = SinglePaneChart(series=sma_20_series)

sma_50_series = LineSeries(data=sma_50_data, color="#4ECDC4")
sma_50_chart = SinglePaneChart(series=sma_50_series)

# Create multi-pane chart
chart = MultiPaneChart([candlestick_chart, volume_chart, sma_20_chart, sma_50_chart])

st.subheader("Multipane Chart with Pandas")

# Render the chart
chart.render(key="multipane")
