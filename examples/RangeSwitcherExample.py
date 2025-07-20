"""
Range Switcher Example - Enhanced TradingView-style Range Switcher

This example demonstrates the enhanced range switcher functionality that allows users
to switch between different timeframes (1D, 1W, 1M, 1Y) with proper data switching
and visual feedback, similar to the TradingView range switcher demo.

Features:
- Multiple timeframe data sets (daily, weekly, monthly, yearly)
- Smooth transitions between timeframes
- Professional styling matching TradingView
- Active state management
- Proper time range calculations
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from streamlit_lightweight_charts_pro import render_chart

# Page configuration
st.set_page_config(
    page_title="Range Switcher Example",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Enhanced Range Switcher Example")
st.markdown("""
This example demonstrates the enhanced range switcher functionality that allows users to switch 
between different timeframes with proper data switching and visual feedback, similar to the 
TradingView range switcher demo.
""")

# Generate sample data for different timeframes
def generate_sample_data(start_date, end_date, freq='D', base_price=100):
    """Generate sample OHLCV data for different timeframes."""
    date_range = pd.date_range(start=start_date, end=end_date, freq=freq)
    
    data = []
    current_price = base_price
    
    for date in date_range:
        # Generate realistic price movements
        change = np.random.normal(0, 0.02)  # 2% daily volatility
        current_price *= (1 + change)
        
        # Generate OHLC from current price
        high = current_price * (1 + abs(np.random.normal(0, 0.01)))
        low = current_price * (1 - abs(np.random.normal(0, 0.01)))
        open_price = current_price * (1 + np.random.normal(0, 0.005))
        close_price = current_price
        
        # Ensure OHLC relationships
        high = max(high, open_price, close_price)
        low = min(low, open_price, close_price)
        
        # Generate volume
        volume = np.random.randint(1000000, 10000000)
        
        data.append({
            'time': date.strftime('%Y-%m-%d'),
            'open': round(open_price, 2),
            'high': round(high, 2),
            'low': round(low, 2),
            'close': round(close_price, 2),
            'volume': volume
        })
        
        current_price = close_price
    
    return data

# Generate data for different timeframes
end_date = datetime.now()
start_date_daily = end_date - timedelta(days=365)
start_date_weekly = end_date - timedelta(days=365*2)
start_date_monthly = end_date - timedelta(days=365*5)
start_date_yearly = end_date - timedelta(days=365*20)

# Create data sets for different timeframes
daily_data = generate_sample_data(start_date_daily, end_date, 'D', 100)
weekly_data = generate_sample_data(start_date_weekly, end_date, 'W', 100)
monthly_data = generate_sample_data(start_date_monthly, end_date, 'M', 100)
yearly_data = generate_sample_data(start_date_yearly, end_date, 'Y', 100)

# Create volume data for each timeframe
def create_volume_data(ohlc_data):
    """Create volume data from OHLC data."""
    return [{'time': item['time'], 'value': item['volume']} for item in ohlc_data]

daily_volume = create_volume_data(daily_data)
weekly_volume = create_volume_data(weekly_data)
monthly_volume = create_volume_data(monthly_data)
yearly_volume = create_volume_data(yearly_data)

# Store data in session state for switching
if 'current_timeframe' not in st.session_state:
    st.session_state.current_timeframe = '1D'

# Timeframe selection
st.subheader("🎯 Timeframe Selection")
timeframe = st.selectbox(
    "Select Timeframe:",
    ['1D', '1W', '1M', '1Y'],
    index=['1D', '1W', '1M', '1Y'].index(st.session_state.current_timeframe),
    help="Choose the timeframe for the chart data"
)

# Update session state
st.session_state.current_timeframe = timeframe

# Get current data based on selected timeframe
timeframe_data = {
    '1D': daily_data,
    '1W': weekly_data,
    '1M': monthly_data,
    '1Y': yearly_data
}

timeframe_volume = {
    '1D': daily_volume,
    '1W': weekly_volume,
    '1M': monthly_volume,
    '1Y': yearly_volume
}

current_data = timeframe_data[timeframe]
current_volume = timeframe_volume[timeframe]

# Display data info
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Timeframe", timeframe)
with col2:
    st.metric("Data Points", len(current_data))
with col3:
    st.metric("Date Range", f"{current_data[0]['time']} to {current_data[-1]['time']}")
with col4:
    latest_price = current_data[-1]['close']
    prev_price = current_data[-2]['close'] if len(current_data) > 1 else latest_price
    change = latest_price - prev_price
    change_pct = (change / prev_price) * 100 if prev_price > 0 else 0
    st.metric(
        "Latest Price", 
        f"${latest_price:.2f}", 
        f"{change:+.2f} ({change_pct:+.2f}%)"
    )

# Create the chart configuration
chart_options = {
    "width": 800,
    "height": 500,
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
    "leftPriceScale": {
        "visible": False,
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
        "defaultRange": timeframe
    }
}

# Create series configurations
candlestick_series = [
    {
        "type": "Candlestick",
        "data": current_data,
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
        "data": current_volume,
        "options": {
            "color": "#26a69a",
            "priceFormat": {
                "type": "volume",
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
st.subheader(f"📈 {timeframe} Chart with Range Switcher")

# Main chart with candlesticks and volume
main_chart = [
    {
        "chart": chart_options,
        "series": candlestick_series + volume_series,
    }
]

    render_chart(main_chart, key=f"range_switcher_{timeframe}")

# Display data table
st.subheader("📋 Data Table")
df = pd.DataFrame(current_data)
st.dataframe(
    df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "time": st.column_config.TextColumn("Date", width="medium"),
        "open": st.column_config.NumberColumn("Open", format="$%.2f"),
        "high": st.column_config.NumberColumn("High", format="$%.2f"),
        "low": st.column_config.NumberColumn("Low", format="$%.2f"),
        "close": st.column_config.NumberColumn("Close", format="$%.2f"),
        "volume": st.column_config.NumberColumn("Volume", format="%d"),
    }
)

# Show statistics
st.subheader("📊 Statistics")
col1, col2, col3 = st.columns(3)

with col1:
    st.write("**Price Statistics**")
    prices = [d['close'] for d in current_data]
    st.write(f"Min: ${min(prices):.2f}")
    st.write(f"Max: ${max(prices):.2f}")
    st.write(f"Mean: ${np.mean(prices):.2f}")
    st.write(f"Std: ${np.std(prices):.2f}")

with col2:
    st.write("**Volume Statistics**")
    volumes = [d['volume'] for d in current_data]
    st.write(f"Min: {min(volumes):,}")
    st.write(f"Max: {max(volumes):,}")
    st.write(f"Mean: {np.mean(volumes):,.0f}")
    st.write(f"Total: {sum(volumes):,}")

with col3:
    st.write("**Returns**")
    returns = []
    for i in range(1, len(current_data)):
        ret = (current_data[i]['close'] - current_data[i-1]['close']) / current_data[i-1]['close']
        returns.append(ret)
    
    if returns:
        st.write(f"Avg Daily Return: {np.mean(returns)*100:.2f}%")
        st.write(f"Volatility: {np.std(returns)*100:.2f}%")
        st.write(f"Total Return: {((current_data[-1]['close'] / current_data[0]['close']) - 1)*100:.2f}%")

# Usage instructions
st.subheader("💡 How to Use")
st.markdown("""
1. **Range Switcher**: Use the buttons in the top-right corner of the chart to switch between different time ranges
2. **Timeframe Selection**: Use the dropdown above to switch between different data timeframes (1D, 1W, 1M, 1Y)
3. **Interactive Features**: 
   - Hover over the chart to see crosshair
   - Click and drag to zoom
   - Use mouse wheel to zoom in/out
   - Double-click to reset view

The range switcher provides quick access to common time ranges while the timeframe selector changes the underlying data resolution.
""")

# Technical details
with st.expander("🔧 Technical Details"):
    st.markdown("""
    **Enhanced Range Switcher Features:**
    
    - **Professional Styling**: Matches TradingView's design with proper fonts, colors, and spacing
    - **Active State Management**: Visual feedback for the currently selected range
    - **Hover Effects**: Smooth transitions and hover states for better UX
    - **Flexible Positioning**: Can be positioned in any corner of the chart
    - **Customizable Ranges**: Easy to add or modify time ranges
    - **Callback Support**: Ready for event handling and integration
    
    **Time Range Calculations:**
    
    - 1D: Last 24 hours
    - 1W: Last 7 days  
    - 1M: Last 30 days
    - 3M: Last 90 days
    - 6M: Last 180 days
    - 1Y: Last 365 days
    - ALL: Fit all available data
    
    **Data Synchronization:**
    
    The range switcher works with the chart's time scale to provide smooth transitions
    and proper data visualization across different time ranges.
    """) 