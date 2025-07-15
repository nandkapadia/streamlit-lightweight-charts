"""
Multi-Pane Charts from CSV Example

This example demonstrates how to create multi-pane charts using data from a CSV file.
"""

import numpy as np
import pandas as pd
import streamlit as st

from streamlit_lightweight_charts import MultiPaneChart, render_chart
from streamlit_lightweight_charts.charts import CandlestickChart, HistogramChart, LineChart
from streamlit_lightweight_charts.data import HistogramData, OhlcData, SingleValueData

COLOR_BULL = "rgba(38,166,154,0.9)"  # #26a69a
COLOR_BEAR = "rgba(239,83,80,0.9)"  # #ef5350

CSVFILE = (
    "https://github.com/freyastreamlit/streamlit-lightweight-charts/blob/main/"
    "examples/MultiPaneChartsFromCSV.csv?raw=true"
)

df = pd.read_csv(CSVFILE, skiprows=0, parse_dates=["datetime"], skip_blank_lines=True)

df["time"] = df["datetime"].view("int64") // 10**9  # We will use time in UNIX timestamp
df["color"] = np.where(df["open"] > df["close"], COLOR_BEAR, COLOR_BULL)  # bull or bear

# Convert DataFrame to list of dictionaries
df_dict = df.to_dict("records")

# Convert to data objects
candlestick_data = [
    OhlcData(row["time"], row["open"], row["high"], row["low"], row["close"]) for row in df_dict
]

volume_data = [HistogramData(row["time"], row["volume"]) for row in df_dict]

macd_fast_data = [
    SingleValueData(row["time"], row["macd_fast"])
    for row in df_dict
    if not pd.isna(row["macd_fast"])
]

macd_slow_data = [
    SingleValueData(row["time"], row["macd_slow"])
    for row in df_dict
    if not pd.isna(row["macd_slow"])
]

macd_hist_data = [
    HistogramData(row["time"], row["macd_hist"]) for row in df_dict if not pd.isna(row["macd_hist"])
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

st.subheader("Multipane Chart (intraday) from CSV")

# Render the chart
render_chart(chart, key="multipane")
