"""
Simple Multi-Pane Chart Example

This example demonstrates basic usage of the enhanced streamlit-lightweight-charts library
with minimal dependencies and simple data.
"""

import streamlit as st
from datetime import datetime, timedelta
from streamlit_lightweight_charts import (
    Chart, ChartGroup, SeriesType, Themes,
    create_candlestick_chart, create_volume_chart
)

st.set_page_config(page_title="Simple Multi-Pane Charts", layout="wide")

st.title("Simple Multi-Pane Chart Example")
st.markdown("This example shows synchronized candlestick and volume charts using the enhanced API.")

# Generate simple sample data
def generate_simple_data():
    """Generate simple OHLCV data without pandas/numpy dependencies"""
    data = []
    base_price = 100
    base_date = datetime.now() - timedelta(days=30)
    
    for i in range(30):
        date = base_date + timedelta(days=i)
        # Simple price movement simulation
        open_price = base_price + (i % 3) * 0.5
        close_price = open_price + (1 if i % 2 == 0 else -1) * 0.8
        high_price = max(open_price, close_price) + 0.3
        low_price = min(open_price, close_price) - 0.3
        volume = 1000000 + i * 50000
        
        data.append({
            'time': date.strftime('%Y-%m-%d'),
            'open': open_price,
            'high': high_price,
            'low': low_price,
            'close': close_price,
            'volume': volume
        })
        
        base_price = close_price
    
    return data

# Generate data
ohlcv_data = generate_simple_data()

# Separate candlestick and volume data
candlestick_data = [
    {k: v for k, v in item.items() if k != 'volume'} 
    for item in ohlcv_data
]
volume_data = [
    {'time': item['time'], 'value': item['volume']} 
    for item in ohlcv_data
]

# Create a synchronized chart group
st.subheader("Synchronized Charts")

# Allow theme selection
theme_name = st.selectbox("Select Theme", ["Light", "Dark", "Trading View"])
theme = getattr(Themes, theme_name.upper().replace(" ", "_"))

# Create chart group
chart_group = ChartGroup(
    sync_enabled=True,
    sync_crosshair=True,
    sync_time_range=True
)

# Create price chart
price_chart = Chart(
    height=400,
    **theme,
    watermark={
        'visible': True,
        'text': 'DEMO',
        'fontSize': 24,
        'color': 'rgba(0, 0, 0, 0.1)'
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

# Create volume chart
volume_chart = Chart(
    height=150,
    **theme,
    time_scale={'visible': True}
)

# Add volume series
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

# Render the charts
chart_group.render(key="simple_charts")

# Show some basic stats
st.subheader("Data Summary")
col1, col2, col3 = st.columns(3)

last_candle = ohlcv_data[-1]
prev_candle = ohlcv_data[-2]

with col1:
    price_change = last_candle['close'] - prev_candle['close']
    price_change_pct = (price_change / prev_candle['close']) * 100
    st.metric(
        "Last Close", 
        f"${last_candle['close']:.2f}", 
        f"{price_change_pct:+.2f}%"
    )

with col2:
    volume_change = last_candle['volume'] - prev_candle['volume']
    volume_change_pct = (volume_change / prev_candle['volume']) * 100
    st.metric(
        "Volume", 
        f"{last_candle['volume']:,}", 
        f"{volume_change_pct:+.1f}%"
    )

with col3:
    price_range = last_candle['high'] - last_candle['low']
    st.metric(
        "Daily Range", 
        f"${price_range:.2f}",
        f"H: ${last_candle['high']:.2f} L: ${last_candle['low']:.2f}"
    )

# Usage tips
with st.expander("Usage Tips"):
    st.markdown("""
    ### Chart Interactions
    - **Pan**: Click and drag to move the chart
    - **Zoom**: Use mouse wheel or pinch gesture
    - **Crosshair**: Move mouse over chart to see crosshair (synchronized across charts)
    - **Reset**: Double-click to reset zoom
    
    ### Features Demonstrated
    - Multi-pane charts with shared time axis
    - Synchronized scrolling and zooming
    - Synchronized crosshair movement
    - Theme switching
    - Watermark overlay
    """)

# Code example
with st.expander("Show Code"):
    st.code('''
# Create a synchronized chart group
chart_group = ChartGroup(
    sync_enabled=True,
    sync_crosshair=True,
    sync_time_range=True
)

# Create and configure charts
price_chart = Chart(height=400, **theme)
price_chart.add_series(SeriesType.CANDLESTICK, candlestick_data)

volume_chart = Chart(height=150, **theme)
volume_chart.add_series(SeriesType.HISTOGRAM, volume_data)

# Add to group and render
chart_group.add_chart(price_chart)
chart_group.add_chart(volume_chart)
chart_group.render(key="charts")
''', language='python')