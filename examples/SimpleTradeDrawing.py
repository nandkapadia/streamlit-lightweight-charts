"""
Simple Trade Drawing Example

This example demonstrates the basic trade drawing functionality:
1. Buy and sell markers on candlestick charts
2. Trade rectangles showing trade duration
3. Individual trade markers
"""

import streamlit as st
from streamlit_lightweight_charts import (
    Chart, SeriesType, TradeType, MarkerShape, create_trade_chart
)

st.title("Simple Trade Drawing Example")

# Sample OHLCV data
ohlcv_data = [
    {'time': '2024-01-01', 'open': 100, 'high': 105, 'low': 98, 'close': 103, 'volume': 1000000},
    {'time': '2024-01-02', 'open': 103, 'high': 108, 'low': 102, 'close': 106, 'volume': 1200000},
    {'time': '2024-01-03', 'open': 106, 'high': 110, 'low': 104, 'close': 108, 'volume': 1100000},
    {'time': '2024-01-04', 'open': 108, 'high': 112, 'low': 106, 'close': 110, 'volume': 1300000},
    {'time': '2024-01-05', 'open': 110, 'high': 115, 'low': 108, 'close': 113, 'volume': 1400000},
    {'time': '2024-01-08', 'open': 113, 'high': 116, 'low': 110, 'close': 114, 'volume': 1200000},
    {'time': '2024-01-09', 'open': 114, 'high': 117, 'low': 111, 'close': 115, 'volume': 1100000},
    {'time': '2024-01-10', 'open': 115, 'high': 118, 'low': 112, 'close': 116, 'volume': 1300000},
    {'time': '2024-01-11', 'open': 116, 'high': 119, 'low': 113, 'close': 117, 'volume': 1400000},
    {'time': '2024-01-12', 'open': 117, 'high': 120, 'low': 114, 'close': 118, 'volume': 1500000},
    {'time': '2024-01-15', 'open': 118, 'high': 121, 'low': 115, 'close': 119, 'volume': 1600000},
    {'time': '2024-01-16', 'open': 119, 'high': 122, 'low': 116, 'close': 120, 'volume': 1700000},
    {'time': '2024-01-17', 'open': 120, 'high': 123, 'low': 117, 'close': 121, 'volume': 1800000},
    {'time': '2024-01-18', 'open': 121, 'high': 124, 'low': 118, 'close': 122, 'volume': 1900000},
    {'time': '2024-01-19', 'open': 122, 'high': 125, 'low': 119, 'close': 123, 'volume': 2000000},
]

# Sample trades
trades = [
    {
        "type": TradeType.BUY,
        "entry_time": "2024-01-02",
        "entry_price": 103,
        "exit_time": "2024-01-10",
        "exit_price": 116,
        "quantity": 100,
        "symbol": "AAPL"
    },
    {
        "type": TradeType.SELL,
        "entry_time": "2024-01-12",
        "entry_price": 118,
        "exit_time": "2024-01-19",
        "exit_price": 123,
        "quantity": 50,
        "symbol": "AAPL"
    }
]

# Create chart with trades
chart = create_trade_chart(
    chart_data=ohlcv_data,
    trades=trades,
    height=400,
    show_trade_markers=True,
    show_trade_rectangles=True
)

# Add individual markers
chart.add_trade_marker(
    time="2024-01-01",
    price=100,
    trade_type=TradeType.BUY,
    shape=MarkerShape.CIRCLE,
    text="BUY SIGNAL",
    color="#4CAF50"
)

chart.add_trade_marker(
    time="2024-01-15",
    price=119,
    trade_type=TradeType.SELL,
    shape=MarkerShape.TRIANGLE_DOWN,
    text="SELL SIGNAL",
    color="#FF5722"
)

# Render the chart
chart.render(key="simple_trade_demo")

# Display trade information
st.subheader("Trade Summary")
for i, trade in enumerate(trades, 1):
    pnl = (trade['exit_price'] - trade['entry_price']) * trade['quantity']
    return_pct = ((trade['exit_price'] / trade['entry_price']) - 1) * 100
    
    st.write(f"**Trade {i}**: {trade['type'].upper()} {trade['quantity']} shares")
    st.write(f"Entry: {trade['entry_time']} @ ${trade['entry_price']}")
    st.write(f"Exit: {trade['exit_time']} @ ${trade['exit_price']}")
    st.write(f"P&L: ${pnl:.2f} ({return_pct:.1f}%)")
    st.write("---")

# Code example
with st.expander("Code Example"):
    st.code("""
# Create chart with trades
chart = create_trade_chart(
    chart_data=ohlcv_data,
    trades=trades,
    height=400,
    show_trade_markers=True,
    show_trade_rectangles=True
)

# Add individual markers
chart.add_trade_marker(
    time="2024-01-01",
    price=100,
    trade_type=TradeType.BUY,
    shape=MarkerShape.CIRCLE,
    text="BUY SIGNAL"
)

# Render the chart
chart.render(key="simple_trade_demo")
    """) 