"""
Simple Multi-Pane Chart Example

This example demonstrates basic usage of the enhanced streamlit-lightweight-charts library
with minimal dependencies and simple data.
"""

from datetime import datetime, timedelta

import streamlit as st

from streamlit_lightweight_charts_pro import MultiPaneChart, render_chart
from streamlit_lightweight_charts_pro.charts import CandlestickChart, HistogramChart
from streamlit_lightweight_charts_pro.data import HistogramData, OhlcData

st.set_page_config(page_title="Simple Multi-Pane Charts", layout="wide")

st.title("Simple Multi-Pane Chart Example")
st.markdown("This example shows synchronized candlestick and volume charts using the enhanced API.")


# Generate simple sample data
def generate_simple_data():
    """Generate simple OHLCV data without pandas/numpy dependencies"""
    ohlc_data = []
    histogram_data = []
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

        ohlc_data.append(
            OhlcData(date.strftime("%Y-%m-%d"), open_price, high_price, low_price, close_price)
        )

        histogram_data.append(HistogramData(date.strftime("%Y-%m-%d"), volume))

        base_price = close_price

    return ohlc_data, histogram_data


# Generate data
candlestick_data, volume_data = generate_simple_data()

# Create a synchronized chart group
st.subheader("Synchronized Charts")

# Allow theme selection
theme_name = st.selectbox("Select Theme", ["Light", "Dark", "Trading View"])

# Create charts
candlestick_chart = CandlestickChart(data=candlestick_data)
histogram_chart = HistogramChart(data=volume_data)

# Create multi-pane chart
chart = MultiPaneChart()
chart.add_pane(candlestick_chart)
chart.add_pane(histogram_chart)

# Render the charts
render_chart(chart, key="simple_charts")

# Show some basic stats
st.subheader("Data Summary")
col1, col2, col3 = st.columns(3)

last_candle = candlestick_data[-1]
prev_candle = candlestick_data[-2]

with col1:
    price_change = last_candle.close - prev_candle.close
    price_change_pct = (price_change / prev_candle.close) * 100
    st.metric("Last Close", f"${last_candle.close:.2f}", f"{price_change_pct:+.2f}%")

with col2:
    volume_change = volume_data[-1].value - volume_data[-2].value
    volume_change_pct = (volume_change / volume_data[-2].value) * 100
    st.metric("Volume", f"{volume_data[-1].value:,}", f"{volume_change_pct:+.1f}%")

with col3:
    price_range = last_candle.high - last_candle.low
    st.metric(
        "Daily Range",
        f"${price_range:.2f}",
        f"H: ${last_candle.high:.2f} L: ${last_candle.low:.2f}",
    )

# Usage tips
with st.expander("Usage Tips"):
    st.markdown(
        """
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
    """
    )

# Code example
with st.expander("Show Code"):
    st.code(
        """
# Create candlestick and histogram charts
candlestick_chart = CandlestickChart(data=candlestick_data)
histogram_chart = HistogramChart(data=volume_data)

# Create multi-pane chart
chart = MultiPaneChart()
chart.add_pane(candlestick_chart)
chart.add_pane(histogram_chart)

# Render the chart
render_chart(chart, key="charts")
""",
        language="python",
    )
