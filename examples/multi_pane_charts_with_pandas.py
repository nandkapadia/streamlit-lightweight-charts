"""
Multi-Pane Charts with Pandas Example

This example demonstrates how to create multi-pane charts using pandas data with yfinance.
"""

import numpy as np
import streamlit as st
import yfinance as yf

from streamlit_lightweight_charts import MultiPaneChart, render_chart
from streamlit_lightweight_charts.charts import CandlestickChart, HistogramChart, LineChart
from streamlit_lightweight_charts.data import HistogramData, OhlcData, SingleValueData

COLOR_BULL = "rgba(38,166,154,0.9)"  # #26a69a
COLOR_BEAR = "rgba(239,83,80,0.9)"  # #ef5350

# Request historic pricing data via finance.yahoo.com API
df = yf.Ticker("AAPL").history(period="4mo")[["Open", "High", "Low", "Close", "Volume"]]

# Some data wrangling to match required format
df = df.reset_index()
df.columns = ["time", "open", "high", "low", "close", "volume"]  # rename columns
df["time"] = df["time"].dt.strftime("%Y-%m-%d")  # Date to string
df["color"] = np.where(df["open"] > df["close"], COLOR_BEAR, COLOR_BULL)  # bull or bear
df.ta.macd(close="close", fast=6, slow=12, signal=5, append=True)  # calculate macd

# Convert DataFrame to list of dictionaries
df_dict = df.to_dict("records")

# Convert to data objects
candlestick_data = [
    OhlcData(row["time"], row["open"], row["high"], row["low"], row["close"]) for row in df_dict
]

volume_data = [HistogramData(row["time"], row["volume"]) for row in df_dict]

macd_fast_data = [
    SingleValueData(row["time"], row["MACDh_6_12_5"])
    for row in df_dict
    if not np.isnan(row["MACDh_6_12_5"])
]

macd_slow_data = [
    SingleValueData(row["time"], row["MACDs_6_12_5"])
    for row in df_dict
    if not np.isnan(row["MACDs_6_12_5"])
]

macd_hist_data = [
    HistogramData(row["time"], row["MACD_6_12_5"])
    for row in df_dict
    if not np.isnan(row["MACD_6_12_5"])
]

# Create charts
candlestick_chart = CandlestickChart(data=candlestick_data)
volume_chart = HistogramChart(data=volume_data)
macd_fast_chart = LineChart(data=macd_fast_data)
macd_slow_chart = LineChart(data=macd_slow_data)
macd_hist_chart = HistogramChart(data=macd_hist_data)

# Create multi-pane chart
chart = MultiPaneChart()
chart.add_pane(candlestick_chart)
chart.add_pane(volume_chart)
chart.add_pane(macd_fast_chart)
chart.add_pane(macd_slow_chart)
chart.add_pane(macd_hist_chart)

st.subheader("Multipane Chart with Pandas")

# Render the chart
render_chart(chart, key="multipane")
