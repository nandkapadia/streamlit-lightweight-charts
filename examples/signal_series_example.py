#!/usr/bin/env python3
"""
Signal Series Example - Background Coloring in Charts

This example demonstrates the new SignalSeries functionality that creates
vertical background bands colored based on signal values. This is commonly
used in financial charts to highlight specific market conditions, trading
signals, or events.

The SignalSeries takes signal data with binary or ternary values and maps
them to background colors for specific time periods. The background bands
appear across all chart panes and provide visual context for the data.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from streamlit_lightweight_charts_pro import (
    Chart, ChartOptions, LayoutOptions, PaneHeightOptions,
    LineSeries, CandlestickSeries, HistogramSeries,
    SignalSeries, SignalData, SignalOptions,
    LineData, CandlestickData, HistogramData
)

# Page configuration
st.set_page_config(
    page_title="Signal Series - Background Coloring",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🎨 Signal Series - Background Coloring")
st.markdown("""
This example demonstrates the new **SignalSeries** functionality that creates vertical background bands 
colored based on signal values. Perfect for highlighting market conditions, trading signals, or events!
""")

# Sidebar configuration
st.sidebar.header("🎛️ Signal Configuration")

# Signal type selection
signal_type = st.sidebar.selectbox(
    "Signal Type",
    ["Binary (0/1)", "Ternary (0/1/2)", "Custom Pattern"],
    help="Choose the type of signal pattern to display"
)

# Color configuration
st.sidebar.subheader("🎨 Color Settings")

color_0 = st.sidebar.color_picker(
    "Color for Value 0",
    value="#ffffff80",
    help="Background color for signal value = 0 (use alpha for opacity)"
)

color_1 = st.sidebar.color_picker(
    "Color for Value 1", 
    value="#ff000080",
    help="Background color for signal value = 1 (use alpha for opacity)"
)

color_2 = st.sidebar.color_picker(
    "Color for Value 2",
    value="#00ff0080", 
    help="Background color for signal value = 2 (ternary only, use alpha for opacity)"
) if signal_type == "Ternary (0/1/2)" else None

# Generate sample data
def generate_sample_data():
    """Generate sample financial data for demonstration."""
    # Generate dates
    start_date = datetime(2024, 1, 1)
    dates = [start_date + timedelta(days=i) for i in range(100)]
    
    # Generate price data (random walk)
    np.random.seed(42)
    price_changes = np.random.normal(0, 0.02, 100)
    prices = [100]
    for change in price_changes[1:]:
        prices.append(prices[-1] * (1 + change))
    
    # Generate OHLC data
    ohlc_data = []
    for i, (date, price) in enumerate(zip(dates, prices)):
        # Create realistic OHLC from price
        high = price * (1 + abs(np.random.normal(0, 0.01)))
        low = price * (1 - abs(np.random.normal(0, 0.01)))
        open_price = prices[i-1] if i > 0 else price
        close_price = price
        
        ohlc_data.append(CandlestickData(
            time=date.strftime("%Y-%m-%d"),
            open=open_price,
            high=high,
            low=low,
            close=close_price
        ))
    
    # Generate volume data
    volume_data = []
    for i, date in enumerate(dates):
        base_volume = 1000000
        volume = base_volume * (1 + abs(np.random.normal(0, 0.5)))
        volume_data.append(HistogramData(
            time=date.strftime("%Y-%m-%d"),
            value=volume,
            color="#2196F3"
        ))
    
    # Generate line data (SMA)
    sma_data = []
    window = 20
    for i, date in enumerate(dates):
        if i >= window - 1:
            sma = sum(prices[i-window+1:i+1]) / window
            sma_data.append(LineData(
                time=date.strftime("%Y-%m-%d"),
                value=sma
            ))
    
    return dates, ohlc_data, volume_data, sma_data

# Generate signal data based on type
def generate_signal_data(dates, signal_type):
    """Generate signal data based on the selected type."""
    signal_data = []
    
    if signal_type == "Binary (0/1)":
        # Alternating pattern
        for i, date in enumerate(dates):
            value = 1 if i % 10 < 5 else 0  # 5 days on, 5 days off
            signal_data.append(SignalData(
                time=date.strftime("%Y-%m-%d"),
                value=value
            ))
    
    elif signal_type == "Ternary (0/1/2)":
        # Three-state pattern
        for i, date in enumerate(dates):
            value = i % 3  # Cycles through 0, 1, 2
            signal_data.append(SignalData(
                time=date.strftime("%Y-%m-%d"),
                value=value
            ))
    
    elif signal_type == "Custom Pattern":
        # Custom pattern based on price movement
        prices = [100]
        for i in range(1, len(dates)):
            # Simulate price movement
            change = np.random.normal(0, 0.02)
            prices.append(prices[-1] * (1 + change))
        
        for i, (date, price) in enumerate(zip(dates, prices)):
            if i == 0:
                value = 0
            else:
                # Signal based on price movement
                price_change = (price - prices[i-1]) / prices[i-1]
                if price_change > 0.01:  # Strong positive
                    value = 1
                elif price_change < -0.01:  # Strong negative
                    value = 2 if color_2 else 0
                else:  # Neutral
                    value = 0
            
            signal_data.append(SignalData(
                time=date.strftime("%Y-%m-%d"),
                value=value
            ))
    
    return signal_data

# Generate data
dates, ohlc_data, volume_data, sma_data = generate_sample_data()
signal_data = generate_signal_data(dates, signal_type)

# Display data summary
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Days", len(dates))
with col2:
    st.metric("Signal Changes", len([s for s in signal_data if s.value != 0]))
with col3:
    unique_values = set(s.value for s in signal_data)
    st.metric("Signal Values", f"{', '.join(map(str, sorted(unique_values)))}")

# Create tabs for different chart configurations
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Basic Signal Chart", 
    "🕯️ Candlestick with Signals",
    "📈 Multi-Pane with Signals",
    "🎨 Advanced Configuration"
])

with tab1:
    st.subheader("📊 Basic Signal Chart")
    st.markdown("""
    A simple line chart with signal-based background coloring. The background bands
    highlight specific time periods based on signal values.
    """)
    
    # Create basic chart with signal series
    chart = Chart(
        options=ChartOptions(
            width=800,
            height=400,
            layout=LayoutOptions(
                background_options={"color": "#ffffff"},
                text_color="#000000"
            )
        )
    )
    
    # Add line series (price data)
    line_data = [LineData(time=d.strftime("%Y-%m-%d"), value=p) 
                 for d, p in zip(dates, [100 + i * 0.5 for i in range(len(dates))])]
    
    chart.add_series(LineSeries(
        data=line_data,
        options=LineSeries.line_options.set_color("#2196F3").set_line_width(2)
    ))
    
    # Add signal series
    signal_series = SignalSeries(
        data=signal_data,
        color_0=color_0,
        color_1=color_1,
        color_2=color_2
    )
    chart.add_series(signal_series)
    
    # Render chart
    chart.render(key="basic_signal_chart")

with tab2:
    st.subheader("🕯️ Candlestick with Signals")
    st.markdown("""
    A candlestick chart with signal-based background coloring. Perfect for
    highlighting market conditions or trading signals.
    """)
    
    # Create candlestick chart with signal series
    chart = Chart(
        options=ChartOptions(
            width=800,
            height=400,
            layout=LayoutOptions(
                background_options={"color": "#ffffff"},
                text_color="#000000"
            )
        )
    )
    
    # Add candlestick series
    chart.add_series(CandlestickSeries(data=ohlc_data))
    
    # Add signal series
    signal_series = SignalSeries(
        data=signal_data,
        color_0=color_0,
        color_1=color_1,
        color_2=color_2
    )
    chart.add_series(signal_series)
    
    # Render chart
    chart.render(key="candlestick_signal_chart")

with tab3:
    st.subheader("📈 Multi-Pane with Signals")
    st.markdown("""
    A multi-pane chart with candlestick, volume, and SMA, all with signal-based
    background coloring that spans across all panes.
    """)
    
    # Create multi-pane chart
    chart = Chart(
        options=ChartOptions(
            width=800,
            height=600,
            layout=LayoutOptions(
                background_options={"color": "#ffffff"},
                text_color="#000000",
                pane_heights={
                    0: PaneHeightOptions(factor=3),  # Main chart
                    1: PaneHeightOptions(factor=1),  # Volume
                    2: PaneHeightOptions(factor=1)   # SMA
                }
            )
        )
    )
    
    # Add candlestick series (pane 0)
    candlestick_series = CandlestickSeries(data=ohlc_data)
    candlestick_series.pane_id = 0
    chart.add_series(candlestick_series)
    
    # Add volume series (pane 1)
    volume_series = HistogramSeries(data=volume_data)
    volume_series.pane_id = 1
    chart.add_series(volume_series)
    
    # Add SMA line series (pane 2)
    sma_series = LineSeries(
        data=sma_data,
        options=LineSeries.line_options.set_color("#FF9800").set_line_width(2)
    )
    sma_series.pane_id = 2
    chart.add_series(sma_series)
    
    # Add signal series (spans all panes)
    signal_series = SignalSeries(
        data=signal_data,
        color_0=color_0,
        color_1=color_1,
        color_2=color_2
    )
    chart.add_series(signal_series)
    
    # Render chart
    chart.render(key="multi_pane_signal_chart")

with tab4:
    st.subheader("🎨 Advanced Configuration")
    st.markdown("""
    Advanced signal series configuration with custom options and interactive controls.
    """)
    
    # Advanced configuration options
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Signal Data Preview")
        # Show signal data table
        signal_df = pd.DataFrame([
            {"Date": s.time, "Value": s.value, "Color": f"Value {s.value}"}
            for s in signal_data[:20]  # Show first 20 entries
        ])
        st.dataframe(signal_df, use_container_width=True)
    
    with col2:
        st.subheader("Configuration Summary")
        st.json({
            "Signal Type": signal_type,
            "Color 0": color_0,
            "Color 1": color_1,
            "Color 2": color_2 if color_2 else "Not used",
            "Total Signals": len(signal_data),
            "Unique Values": list(set(s.value for s in signal_data))
        })
    
    # Create advanced chart with custom styling
    chart = Chart(
        options=ChartOptions(
            width=800,
            height=500,
            layout=LayoutOptions(
                background_options={"color": "#f8f9fa"},
                text_color="#2c3e50"
            )
        )
    )
    
    # Add candlestick series with custom styling
    candlestick_series = CandlestickSeries(
        data=ohlc_data,
        options=CandlestickSeries.candlestick_options
            .set_up_color("#26a69a")
            .set_down_color("#ef5350")
            .set_border_up_color("#26a69a")
            .set_border_down_color("#ef5350")
            .set_wick_up_color("#26a69a")
            .set_wick_down_color("#ef5350")
    )
    chart.add_series(candlestick_series)
    
    # Add signal series with advanced options
    signal_options = SignalOptions(
        color_0=color_0,
        color_1=color_1,
        color_2=color_2
    )
    
    signal_series = SignalSeries(
        data=signal_data,
        options=signal_options
    )
    chart.add_series(signal_series)
    
    # Render chart
    chart.render(key="advanced_signal_chart")

# Footer
st.markdown("---")
st.markdown("""
### 🎯 Signal Series Features

- **Background Coloring**: Vertical bands that span the entire chart height
- **Multi-Pane Support**: Signals appear across all chart panes
- **Custom Colors**: Configurable colors for different signal values
- **Alpha Support**: Use hex colors with alpha values for transparency
- **Real-time Updates**: Support for dynamic signal changes
- **Performance Optimized**: Efficient rendering for large datasets

### 📚 Use Cases

- **Trading Signals**: Highlight buy/sell signals or market conditions
- **Event Markers**: Mark important dates or announcements
- **Market Regimes**: Distinguish between different market states
- **Risk Management**: Highlight high-risk or low-risk periods
- **Performance Analysis**: Mark periods of good/bad performance
""") 