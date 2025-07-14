"""
Range Switcher Example

This example demonstrates the new range switcher functionality
that allows users to quickly switch between predefined time ranges.
"""

import streamlit as st
from datetime import datetime, timedelta
from streamlit_lightweight_charts import (
    Chart, ChartGroup, SeriesType, Themes
)

st.set_page_config(page_title="Range Switcher Demo", layout="wide")

st.title("Range Switcher Demo")
st.markdown("""
This example shows the new range switcher functionality that allows users to quickly 
switch between predefined time ranges (1D, 1W, 1M, 3M, 6M, 1Y, ALL).
""")

# Generate sample data with more points for better range switching
def generate_extended_data(days=365):
    """Generate extended sample data for range switching demo"""
    data = []
    base_date = datetime.now() - timedelta(days=days)
    base_price = 100
    
    for i in range(days):
        date = base_date + timedelta(days=i)
        # More realistic price movement
        change = (i % 7 - 3) * 0.5 + (i % 30 - 15) * 0.2
        base_price += change
        
        open_price = base_price
        close_price = base_price + (1 if i % 2 == 0 else -1) * 0.8
        high_price = max(open_price, close_price) + 0.5
        low_price = min(open_price, close_price) - 0.5
        volume = 1000000 + abs(change) * 100000
        
        data.append({
            'time': date.strftime('%Y-%m-%d'),
            'open': open_price,
            'high': high_price,
            'low': low_price,
            'close': close_price,
            'volume': volume
        })
    
    return data

# Generate data
ohlcv_data = generate_extended_data()

# Separate candlestick and volume data
candlestick_data = [
    {k: v for k, v in item.items() if k != 'volume'} 
    for item in ohlcv_data
]
volume_data = [
    {'time': item['time'], 'value': item['volume']} 
    for item in ohlcv_data
]

# Sidebar controls
with st.sidebar:
    st.header("Range Switcher Controls")
    
    # Range switcher position
    position = st.selectbox(
        "Position",
        ["top-right", "top-left", "bottom-right", "bottom-left"],
        index=0
    )
    
    # Default range
    default_range = st.selectbox(
        "Default Range",
        ["1D", "1W", "1M", "3M", "6M", "1Y", "ALL"],
        index=2
    )
    
    # Custom ranges
    st.subheader("Custom Ranges")
    use_custom_ranges = st.checkbox("Use custom ranges", False)
    
    if use_custom_ranges:
        custom_ranges = []
        for i in range(3):
            col1, col2 = st.columns(2)
            with col1:
                label = st.text_input(f"Label {i+1}", f"Custom{i+1}")
            with col2:
                days = st.number_input(f"Days {i+1}", min_value=1, value=7*(i+1))
            custom_ranges.append({
                "label": label,
                "seconds": days * 86400
            })
    else:
        custom_ranges = None

# Create chart group
chart_group = ChartGroup(
    sync_enabled=True,
    sync_crosshair=True,
    sync_time_range=True
)

# Main price chart with range switcher
price_chart = Chart(
    height=400,
    **Themes.TRADING_VIEW,
    watermark={
        'visible': True,
        'text': 'RANGE SWITCHER DEMO',
        'fontSize': 16,
        'color': 'rgba(255, 255, 255, 0.1)'
    }
)

# Add candlestick series
price_chart.add_series(
    SeriesType.CANDLESTICK,
    candlestick_data,
    name="Price",
    options={
        'upColor': '#26a69a',
        'downColor': '#ef5350',
        'borderVisible': False,
        'wickUpColor': '#26a69a',
        'wickDownColor': '#ef5350'
    }
)

# Add range switcher
if use_custom_ranges:
    price_chart.add_range_switcher(
        ranges=custom_ranges,
        position=position,
        default_range=default_range
    )
else:
    price_chart.add_range_switcher(
        position=position,
        default_range=default_range
    )

# Volume chart
volume_chart = Chart(
    height=150,
    **Themes.TRADING_VIEW,
    time_scale={'visible': True}
)

volume_chart.add_series(
    SeriesType.HISTOGRAM,
    volume_data,
    name="Volume",
    options={
        'color': '#26a69a',
        'priceFormat': {'type': 'volume'}
    }
)

# Add charts to group
chart_group.add_chart(price_chart)
chart_group.add_chart(volume_chart)

# Event callbacks
def on_range_change(event_data):
    st.session_state['last_range_change'] = event_data
    st.info(f"Range changed to: {event_data['range']['label']}")

def on_crosshair_move(event_data):
    if 'crosshair_data' not in st.session_state:
        st.session_state.crosshair_data = {}
    st.session_state.crosshair_data = event_data

# Register callbacks
chart_group.on_range_switcher_change(on_range_change)
chart_group.on_crosshair_move(on_crosshair_move)

# Render the chart group
chart_group.render(key="range_switcher_demo")

# Display event information
col1, col2 = st.columns(2)

with col1:
    st.subheader("Last Range Change")
    if 'last_range_change' in st.session_state:
        st.json(st.session_state['last_range_change'])
    else:
        st.info("Click on range switcher buttons to see events")

with col2:
    st.subheader("Current Crosshair Position")
    if 'crosshair_data' in st.session_state:
        st.json(st.session_state['crosshair_data'])
    else:
        st.info("Move crosshair to see position data")

# Usage instructions
with st.expander("How to Use Range Switcher"):
    st.markdown("""
    ### Range Switcher Features
    
    1. **Quick Time Range Selection**: Click any button to instantly change the visible time range
    2. **Predefined Ranges**: 
       - 1D: Last 24 hours
       - 1W: Last 7 days  
       - 1M: Last 30 days
       - 3M: Last 90 days
       - 6M: Last 180 days
       - 1Y: Last 365 days
       - ALL: Show all available data
    
    3. **Visual Feedback**: Selected range is highlighted in blue
    4. **Event Callbacks**: Range changes trigger callbacks for programmatic handling
    5. **Customizable**: Position, ranges, and styling can be customized
    
    ### Code Example
    ```python
    chart = Chart()
    chart.add_series(SeriesType.CANDLESTICK, data)
    chart.add_range_switcher(
        position="top-right",
        default_range="1M"
    )
    ```
    """)

# Performance metrics
st.subheader("Data Summary")
col1, col2, col3, col4 = st.columns(4)

last_candle = ohlcv_data[-1]
prev_candle = ohlcv_data[-2]

with col1:
    change = last_candle['close'] - prev_candle['close']
    change_pct = (change / prev_candle['close']) * 100
    st.metric(
        "Last Close", 
        f"${last_candle['close']:.2f}", 
        f"{change_pct:+.2f}%"
    )

with col2:
    st.metric(
        "Data Points", 
        f"{len(ohlcv_data):,}",
        f"From {ohlcv_data[0]['time']} to {ohlcv_data[-1]['time']}"
    )

with col3:
    st.metric(
        "Volume", 
        f"{last_candle['volume']:,}", 
        f"Daily average: {sum(item['volume'] for item in ohlcv_data) // len(ohlcv_data):,}"
    )

with col4:
    price_range = last_candle['high'] - last_candle['low']
    st.metric(
        "Daily Range", 
        f"${price_range:.2f}",
        f"H: ${last_candle['high']:.2f} L: ${last_candle['low']:.2f}"
    ) 