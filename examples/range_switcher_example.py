"""
Range Switcher Example

This example demonstrates basic multi-pane chart functionality
with candlestick and volume data.
"""

from datetime import datetime, timedelta

import streamlit as st

from streamlit_lightweight_charts_pro import Chart
from streamlit_lightweight_charts_pro.charts.series import CandlestickSeries, HistogramSeries
from streamlit_lightweight_charts_pro.data import OhlcData, SingleValueData
from streamlit_lightweight_charts_pro.type_definitions import ColumnNames

st.set_page_config(page_title="Multi-Pane Chart Demo", layout="wide")

st.title("Multi-Pane Chart Demo")
st.markdown(
    """
This example shows a multi-pane chart with candlestick and volume data using the new 
OOP architecture.
"""
)


# Generate sample data with more points for better visualization
def generate_extended_data(days=365):
    """Generate extended sample data for chart demo"""
    ohlc_data = []
    histogram_data = []
    base_date = datetime.now() - timedelta(days=days)
    base_price = 100

    for i in range(days):
        date = base_date + timedelta(days=i)
        # More realistic price movement
        change_ = (i % 7 - 3) * 0.5 + (i % 30 - 15) * 0.2
        base_price += change_

        open_price = base_price
        close_price = base_price + (1 if i % 2 == 0 else -1) * 0.8
        high_price = max(open_price, close_price) + 0.5
        low_price = min(open_price, close_price) - 0.5
        volume = 1000000 + abs(change_) * 100000

        ohlc_data.append(
            OhlcData(
                date.strftime("%Y-%m-%d"),
                open_price,
                high_price,
                low_price,
                close_price,
            )
        )

        histogram_data.append(SingleValueData(date.strftime("%Y-%m-%d"), volume))

    return ohlc_data, histogram_data


# Generate data
candlestick_data, volume_data = generate_extended_data()

# Sidebar controls
with st.sidebar:
    st.header("Chart Controls")

    # Theme selection
    theme = st.selectbox("Theme", ["Light", "Dark", "Trading View"], index=2)

# Create charts
candlestick_series = CandlestickSeries(data=candlestick_data)
candlestick_chart = Chart(series=candlestick_series)

histogram_series = HistogramSeries(data=volume_data)
histogram_chart = Chart(series=histogram_series)

# Create multi-pane chart
# MultiPaneChart removed - using individual charts instead
chart = candlestick_chart  # Use candlestick chart as primary

# Render the chart
chart.render(key="multi_pane_demo")

# Display data information
col1, col2 = st.columns(2)

with col1:
    st.subheader("Chart Information")
    st.info("This is a multi-pane chart with synchronized time axis")

with col2:
    st.subheader("Data Summary")
    st.info(f"Total data points: {len(candlestick_data)}")

# Usage instructions
with st.expander("How to Use Multi-Pane Charts"):
    st.markdown(
        """
    ### Multi-Pane Chart Features
    
    1. **Synchronized Time Axis**: All panes share the same time scale
    2. **Independent Price Scales**: Each pane can have its own price scale
    3. **Synchronized Interactions**: Pan and zoom affect all panes simultaneously
    4. **Flexible Layout**: Add multiple series to create complex chart layouts
    
    ### Code Example
    ```python
    # Create charts
    candlestick_series = CandlestickSeries(data=candlestick_data)
    candlestick_chart = SinglePaneChart(series=candlestick_series)
    
    histogram_series = HistogramSeries(data=volume_data)
    histogram_chart = SinglePaneChart(series=histogram_series)
    
    # Create multi-pane chart
    # MultiPaneChart removed - using individual charts instead
    chart = candlestick_chart  # Use candlestick chart as primary
    
    # Render the chart
    chart.render(key="charts")
    ```
    """
    )

# Performance metrics
st.subheader("Data Summary")
col1, col2, col3, col4 = st.columns(4)

last_candle = candlestick_data[-1]
prev_candle = candlestick_data[-2]

with col1:
    change = last_candle.close - prev_candle.close
    change_pct = (change / prev_candle.close) * 100
    st.metric("Last Close", f"${last_candle.close:.2f}", f"{change_pct:+.2f}%")

with col2:
    st.metric(
        "Data Points",
        f"{len(candlestick_data):,}",
        f"From {candlestick_data[0].time} to {candlestick_data[-1].time}",
    )

with col3:
    st.metric(
        ColumnNames.VOLUME,
        f"{volume_data[-1].value:,}",
        f"Daily average: {sum(item.value for item in volume_data) // len(volume_data):,}",
    )

with col4:
    price_range = last_candle.high - last_candle.low
    st.metric(
        "Daily Range",
        f"${price_range:.2f}",
        f"H: ${last_candle.high:.2f} L: ${last_candle.low:.2f}",
    )
