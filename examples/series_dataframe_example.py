"""Example demonstrating Series classes with DataFrame support."""

import pandas as pd
import streamlit as st

from streamlit_lightweight_charts_pro import (
    AreaSeries,
    BarSeries,
    CandlestickSeries,
    Chart,
    LineSeries,
)
from streamlit_lightweight_charts_pro.type_definitions import ColumnNames

# Sample data
dates = pd.date_range("2024-01-01", periods=30, freq="D")
df = pd.DataFrame(
    {
        ColumnNames.DATETIME: dates,
        ColumnNames.OPEN: [100 + i * 0.5 + (i % 3 - 1) * 2 for i in range(30)],
        ColumnNames.HIGH: [105 + i * 0.5 + (i % 3 - 1) * 2 for i in range(30)],
        ColumnNames.LOW: [95 + i * 0.5 + (i % 3 - 1) * 2 for i in range(30)],
        ColumnNames.CLOSE: [102 + i * 0.5 + (i % 3 - 1) * 2 for i in range(30)],
        ColumnNames.VOLUME: [1000 + i * 10 for i in range(30)],
        "price": [102 + i * 0.5 + (i % 3 - 1) * 2 for i in range(30)],
        ColumnNames.VALUE: [50 + i * 0.3 for i in range(30)],
    }
)

st.title("Series DataFrame Support Example")

st.header("1. Direct Series Creation from DataFrame")

# Line Series
st.subheader("Line Series")
line_series = LineSeries(
    data=df, column_mapping={ColumnNames.TIME: ColumnNames.DATETIME, ColumnNames.VALUE: "price"}
)
line_chart = Chart(series=[line_series])
st.components.v1.html(line_chart.render(), height=400)

# Area Series
st.subheader("Area Series")
area_series = AreaSeries(
    data=df,
    column_mapping={ColumnNames.TIME: ColumnNames.DATETIME, ColumnNames.VALUE: ColumnNames.CLOSE},
)
area_chart = Chart(series=[area_series])
st.components.v1.html(area_chart.render(), height=400)

# Candlestick Series
st.subheader("Candlestick Series")
candlestick_series = CandlestickSeries(
    data=df,
    column_mapping={
        ColumnNames.TIME: ColumnNames.DATETIME,
        ColumnNames.OPEN: ColumnNames.OPEN,
        ColumnNames.HIGH: ColumnNames.HIGH,
        ColumnNames.LOW: ColumnNames.LOW,
        ColumnNames.CLOSE: ColumnNames.CLOSE,
    },
)
candlestick_chart = Chart(series=[candlestick_series])
st.components.v1.html(candlestick_chart.render(), height=400)

# Bar Series
st.subheader("Bar Series")
bar_series = BarSeries(
    data=df,
    column_mapping={
        ColumnNames.TIME: ColumnNames.DATETIME,
        ColumnNames.OPEN: ColumnNames.OPEN,
        ColumnNames.HIGH: ColumnNames.HIGH,
        ColumnNames.LOW: ColumnNames.LOW,
        ColumnNames.CLOSE: ColumnNames.CLOSE,
    },
)
bar_chart = Chart(series=[bar_series])
st.components.v1.html(bar_chart.render(), height=400)

st.header("2. Multi-Pane Chart with Series")

# Create multiple series for multi-pane chart
candlestick_series_multi = CandlestickSeries(
    data=df,
    column_mapping={
        ColumnNames.TIME: ColumnNames.DATETIME,
        ColumnNames.OPEN: ColumnNames.OPEN,
        ColumnNames.HIGH: ColumnNames.HIGH,
        ColumnNames.LOW: ColumnNames.LOW,
        ColumnNames.CLOSE: ColumnNames.CLOSE,
    },
)

line_series_multi = LineSeries(
    data=df, column_mapping={ColumnNames.TIME: ColumnNames.DATETIME, ColumnNames.VALUE: "price"}
)

multi_chart = Chart(
    charts=[
        Chart(series=[candlestick_series_multi]),
        Chart(series=[line_series_multi]),
    ]
)

st.components.v1.html(multi_chart.render(), height=600)

st.header("3. Custom Column Mapping Example")

# Example with different column names
df_custom = pd.DataFrame(
    {
        "date": dates,
        "o": [100 + i * 0.5 for i in range(30)],
        "h": [105 + i * 0.5 for i in range(30)],
        "l": [95 + i * 0.5 for i in range(30)],
        "c": [102 + i * 0.5 for i in range(30)],
        "v": [1000 + i * 10 for i in range(30)],
    }
)

custom_candlestick = CandlestickSeries(
    data=df_custom,
    column_mapping={
        ColumnNames.TIME: "date",
        ColumnNames.OPEN: "o",
        ColumnNames.HIGH: "h",
        ColumnNames.LOW: "l",
        ColumnNames.CLOSE: "c",
    },
)

custom_chart = Chart(series=[custom_candlestick])
st.components.v1.html(custom_chart.render(), height=400)

st.success("✅ All Series classes now support DataFrame input with column mapping!")
