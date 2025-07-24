"""
Simple Range Switcher Example

A simple example demonstrating the enhanced range switcher functionality
with a single dataset, similar to the TradingView range switcher demo.

This example shows how to add a range switcher to any chart with minimal configuration.
"""

from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import streamlit as st

from streamlit_lightweight_charts_pro.type_definitions import ColumnNames

st.title("📊 Simple Range Switcher Example")
st.markdown(
    """
This example demonstrates the enhanced range switcher functionality with a single dataset.
The range switcher allows users to quickly switch between different time ranges (1D, 1W, 1M, 1Y, ALL).
"""
)


# Generate sample data
@st.cache_data
def generate_data():
    """Generate sample OHLCV data."""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365 * 2)  # 2 years of data

    date_range = pd.date_range(start=start_date, end=end_date, freq="D")

    data = []
    current_price = 100

    for date in date_range:
        # Generate realistic price movements
        change = np.random.normal(0, 0.015)  # 1.5% daily volatility
        current_price *= 1 + change

        # Generate OHLC from current price
        high = current_price * (1 + abs(np.random.normal(0, 0.008)))
        low = current_price * (1 - abs(np.random.normal(0, 0.008)))
        open_price = current_price * (1 + np.random.normal(0, 0.004))
        close_price = current_price

        # Ensure OHLC relationships
        high = max(high, open_price, close_price)
        low = min(low, open_price, close_price)

        # Generate volume
        volume = np.random.randint(1000000, 10000000)

        data.append(
            {
                ColumnNames.TIME: date.strftime("%Y-%m-%d"),
                ColumnNames.OPEN: round(open_price, 2),
                ColumnNames.HIGH: round(high, 2),
                ColumnNames.LOW: round(low, 2),
                ColumnNames.CLOSE: round(close_price, 2),
                ColumnNames.VOLUME: volume,
            }
        )

        current_price = close_price

    return data


# Generate the data
data = generate_data()

# Create volume data
volume_data = [
    {ColumnNames.TIME: item[ColumnNames.TIME], ColumnNames.VALUE: item[ColumnNames.VOLUME]}
    for item in data
]

# Chart configuration with range switcher
chart_options = {
    "width": 800,
    "height": 400,
    "layout": {
        "background": {"type": "solid", "color": "white"},
        "textColor": "black",
    },
    "grid": {
        "vertLines": {"color": "rgba(197, 203, 206, 0.5)"},
        "horzLines": {"color": "rgba(197, 203, 206, 0.5)"},
    },
    "crosshair": {
        "mode": 1,
    },
    "rightPriceScale": {
        "borderColor": "rgba(197, 203, 206, 0.8)",
        "scaleMargins": {
            "top": 0.1,
            "bottom": 0.2,
        },
    },
    "timeScale": {
        "borderColor": "rgba(197, 203, 206, 0.8)",
        "timeVisible": True,
        "secondsVisible": False,
    },
    "overlayPriceScales": {
        "scaleMargins": {
            "top": 0.8,
            "bottom": 0,
        }
    },
    # Range switcher configuration
    "rangeSwitcher": {
        "ranges": [
            {"label": "1D", "seconds": 86400},
            {"label": "1W", "seconds": 604800},
            {"label": "1M", "seconds": 2592000},
            {"label": "3M", "seconds": 7776000},
            {"label": "6M", "seconds": 15552000},
            {"label": "1Y", "seconds": 31536000},
            {"label": "ALL", "seconds": None},
        ],
        "position": "top-right",
        "visible": True,
        "defaultRange": "1M",  # Start with 1M view
    },
}

# Series configurations
candlestick_series = [
    {
        "type": "Candlestick",
        "data": data,
        "options": {
            "upColor": "#26a69a",
            "downColor": "#ef5350",
            "borderVisible": False,
            "wickUpColor": "#26a69a",
            "wickDownColor": "#ef5350",
        },
    }
]

volume_series = [
    {
        "type": "Histogram",
        "data": volume_data,
        "options": {
            "color": "#26a69a",
            "priceFormat": {
                "type": ColumnNames.VOLUME,
            },
            "priceScaleId": "",
        },
        "priceScale": {
            "scaleMargins": {
                "top": 0.8,
                "bottom": 0,
            },
        },
    }
]

# Render the chart
st.subheader("📈 Chart with Range Switcher")
st.markdown("Use the buttons in the top-right corner to switch between different time ranges.")

chart_config = [
    {
        "chart": chart_options,
        "series": candlestick_series + volume_series,
    }
]

chart_config.render(key="simple_range_switcher")

# Display data info
st.subheader("📋 Data Information")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Data Points", len(data))
with col2:
    st.metric("Date Range", f"{data[0]['time']} to {data[-1]['time']}")
with col3:
    latest_price = data[-1][ColumnNames.CLOSE]
    prev_price = data[-2][ColumnNames.CLOSE]
    change = latest_price - prev_price
    change_pct = (change / prev_price) * 100
    st.metric("Latest Price", f"${latest_price:.2f}", f"{change:+.2f} ({change_pct:+.2f}%)")
with col4:
    total_volume = sum(d[ColumnNames.VOLUME] for d in data)
    st.metric("Total Volume", f"{total_volume:,}")

# Show sample data
st.subheader("📊 Sample Data")
df = pd.DataFrame(data[-10:])  # Show last 10 rows
st.dataframe(
    df,
    use_container_width=True,
    hide_index=True,
    column_config={
        ColumnNames.TIME: st.column_config.TextColumn("Date", width="medium"),
        ColumnNames.OPEN: st.column_config.NumberColumn(ColumnNames.OPEN, format="$%.2f"),
        ColumnNames.HIGH: st.column_config.NumberColumn(ColumnNames.HIGH, format="$%.2f"),
        ColumnNames.LOW: st.column_config.NumberColumn(ColumnNames.LOW, format="$%.2f"),
        ColumnNames.CLOSE: st.column_config.NumberColumn(ColumnNames.CLOSE, format="$%.2f"),
        ColumnNames.VOLUME: st.column_config.NumberColumn(ColumnNames.VOLUME, format="%d"),
    },
)

# Usage instructions
st.subheader("💡 How to Use the Range Switcher")
st.markdown(
    """
1. **Range Switcher Buttons**: Click the buttons in the top-right corner of the chart
2. **Available Ranges**:
   - **1D**: Last 24 hours
   - **1W**: Last 7 days
   - **1M**: Last 30 days
   - **3M**: Last 90 days
   - **6M**: Last 180 days
   - **1Y**: Last 365 days
   - **ALL**: Show all available data

3. **Interactive Features**:
   - Hover over the chart to see crosshair
   - Click and drag to zoom
   - Use mouse wheel to zoom in/out
   - Double-click to reset view

The range switcher provides quick access to common time ranges for financial analysis.
"""
)

# Code example
with st.expander("🔧 Code Example"):
    st.code(
        """
# Chart configuration with range switcher
chart_options = {
    "width": 800,
    "height": 400,
    "layout": {
        "background": {"type": "solid", "color": "white"},
        "textColor": "black",
    },
    # ... other chart options ...
    
    # Range switcher configuration
    "rangeSwitcher": {
        "ranges": [
            {"label": "1D", "seconds": 86400},
            {"label": "1W", "seconds": 604800},
            {"label": "1M", "seconds": 2592000},
            {"label": "3M", "seconds": 7776000},
            {"label": "6M", "seconds": 15552000},
            {"label": "1Y", "seconds": 31536000},
            {"label": "ALL", "seconds": None}
        ],
        "position": "top-right",
        "visible": True,
        "defaultRange": "1M"
    }
}

# Render the chart
chart_config = [
    {
        "chart": chart_options,
        "series": candlestick_series + volume_series,
    }
]

chart_config.render(key="my_chart")
""",
        language="python",
    )
