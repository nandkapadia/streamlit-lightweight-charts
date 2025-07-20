#!/usr/bin/env python3
"""
Test script to verify rectangle plugin fixes
"""

import streamlit as st
from datetime import datetime, timedelta
from streamlit_lightweight_charts_pro import SinglePaneChart
from streamlit_lightweight_charts_pro.charts.series import CandlestickSeries
from streamlit_lightweight_charts_pro.data import (
    OhlcData,
    Trade,
    TradeVisualizationOptions,
    TradeVisualization,
)

st.set_page_config(page_title="Rectangle Plugin Test", layout="wide")

st.title("Rectangle Plugin Test")
st.markdown("Testing the fixed rectangle plugin for trade visualization")

# Generate simple test data
def generate_test_data():
    data = []
    base_date = datetime.now() - timedelta(days=30)
    base_price = 100
    
    for i in range(30):
        date = base_date + timedelta(days=i)
        open_price = base_price + (i % 3) * 0.5
        close_price = open_price + (1 if i % 2 == 0 else -1) * 1.2
        high_price = max(open_price, close_price) + 0.8
        low_price = min(open_price, close_price) - 0.8
        
        data.append(OhlcData(
            date.strftime("%Y-%m-%d"), 
            open_price, 
            high_price, 
            low_price, 
            close_price
        ))
        base_price = close_price
    
    return data

# Generate test trades
def generate_test_trades():
    base_date = datetime.now() - timedelta(days=30)
    
    trades = [
        Trade(
            entry_time=(base_date + timedelta(days=5)).strftime("%Y-%m-%d"),
            entry_price=102.50,
            exit_time=(base_date + timedelta(days=15)).strftime("%Y-%m-%d"),
            exit_price=108.30,
            quantity=100,
            trade_type="long",
        ),
        Trade(
            entry_time=(base_date + timedelta(days=18)).strftime("%Y-%m-%d"),
            entry_price=106.20,
            exit_time=(base_date + timedelta(days=25)).strftime("%Y-%m-%d"),
            exit_price=98.80,
            quantity=50,
            trade_type="short",
        ),
    ]
    return trades

# Generate data
ohlcv_data = generate_test_data()
test_trades = generate_test_trades()

# Display options
col1, col2 = st.columns(2)

with col1:
    st.subheader("Test Configuration")
    show_markers = st.checkbox("Show Trade Markers", True)
    show_rectangles = st.checkbox("Show Trade Rectangles", True)
    
    if st.button("Test Rectangle Plugin"):
        st.success("Rectangle plugin test initiated!")

with col2:
    st.subheader("Trade Data")
    for i, trade in enumerate(test_trades, 1):
        st.write(f"**Trade {i}**: {trade.trade_type.upper()}")
        st.write(f"Entry: {trade.entry_time} @ ${trade.entry_price}")
        st.write(f"Exit: {trade.exit_time} @ ${trade.exit_price}")
        st.write(f"P&L: ${trade.pnl:.2f} ({trade.pnl_percentage:.1f}%)")
        st.write("---")

# Determine trade visualization style
if show_markers and show_rectangles:
    trade_style = TradeVisualization.BOTH
elif show_markers:
    trade_style = TradeVisualization.MARKERS
elif show_rectangles:
    trade_style = TradeVisualization.RECTANGLES
else:
    trade_style = None

# Create candlestick series with trades
candlestick_series = CandlestickSeries(
    data=ohlcv_data,
    up_color="#4CAF50",
    down_color="#F44336",
    trades=test_trades if (show_markers or show_rectangles) else None,
    trade_visualization_options=TradeVisualizationOptions(
        style=trade_style,
        entry_marker_color_long="#4CAF50",
        entry_marker_color_short="#FF5722",
        exit_marker_color_profit="#4CAF50",
        exit_marker_color_loss="#F44336",
        rectangle_fill_opacity=0.3,
        rectangle_border_width=2
    ) if trade_style else None
)

# Create and render chart
chart = SinglePaneChart(series=candlestick_series)
chart.render(key="rectangle_test")

# Status information
st.subheader("Test Status")
st.info("""
**Expected Behavior:**
- ✅ No console errors about "right should be >= left"
- ✅ No "Object is disposed" errors
- ✅ Trade rectangles should display correctly
- ✅ Trade markers should display correctly
- ✅ Chart should be interactive and responsive

**If you see errors in the browser console, please report them.**
""")

# Debug information
with st.expander("Debug Information"):
    st.write("**Trade Data:**")
    for trade in test_trades:
        st.json({
            "entry_time": trade.entry_time,
            "entry_price": trade.entry_price,
            "exit_time": trade.exit_time,
            "exit_price": trade.exit_price,
            "trade_type": trade.trade_type,
            "pnl": trade.pnl,
            "pnl_percentage": trade.pnl_percentage
        })
    
    st.write("**Chart Configuration:**")
    st.json({
        "show_markers": show_markers,
        "show_rectangles": show_rectangles,
        "trade_style": trade_style,
        "data_points": len(ohlcv_data)
    }) 