"""
Advanced Multi-Pane Synchronized Charts Example

This example demonstrates:
- Multiple synchronized chart panes
- Full crosshair and time range synchronization
- Dynamic data updates
- Event callbacks
- Custom indicators
- Price lines and markers
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from streamlit_lightweight_charts import (
    Chart, ChartGroup, SeriesType, PriceScaleMode,
    CrosshairMode, LineStyle, create_candlestick_chart,
    create_volume_chart, create_line_indicator
)

# Generate sample data
@st.cache_data
def generate_sample_data(days=100):
    """Generate sample OHLCV data"""
    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
    
    # Generate price data
    close_prices = 100 + np.cumsum(np.random.randn(days) * 2)
    high_prices = close_prices + np.abs(np.random.randn(days))
    low_prices = close_prices - np.abs(np.random.randn(days))
    open_prices = np.roll(close_prices, 1)
    open_prices[0] = close_prices[0]
    
    # Generate volume
    volume = np.abs(np.random.randn(days) * 1000000 + 5000000).astype(int)
    
    # Create OHLCV dataframe
    df = pd.DataFrame({
        'time': dates,
        'open': open_prices,
        'high': high_prices,
        'low': low_prices,
        'close': close_prices,
        'volume': volume
    })
    
    # Calculate indicators
    df['sma_20'] = df['close'].rolling(window=20).mean()
    df['sma_50'] = df['close'].rolling(window=50).mean()
    df['rsi'] = calculate_rsi(df['close'])
    df['macd'], df['signal'], df['histogram'] = calculate_macd(df['close'])
    
    return df

def calculate_rsi(prices, period=14):
    """Calculate RSI indicator"""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_macd(prices, fast=12, slow=26, signal=9):
    """Calculate MACD indicator"""
    exp1 = prices.ewm(span=fast, adjust=False).mean()
    exp2 = prices.ewm(span=slow, adjust=False).mean()
    macd = exp1 - exp2
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    histogram = macd - signal_line
    return macd, signal_line, histogram

def format_data_for_chart(df, columns):
    """Format dataframe for chart consumption"""
    data = []
    for _, row in df.iterrows():
        item = {'time': row['time'].strftime('%Y-%m-%d')}
        for col in columns:
            if col in row and pd.notna(row[col]):
                if col == 'volume':
                    item['value'] = row[col]
                elif col in ['open', 'high', 'low', 'close']:
                    item[col] = row[col]
                else:
                    item['value'] = row[col]
        data.append(item)
    return data

st.set_page_config(page_title="Advanced Multi-Pane Charts", layout="wide")

st.title("Advanced Multi-Pane Synchronized Charts")
st.markdown("""
This example demonstrates the full capabilities of the enhanced streamlit-lightweight-charts library:
- **Synchronized charts**: Time range and crosshair sync across all panes
- **Multiple indicators**: SMA, RSI, MACD in separate panes
- **Interactive features**: Click events, callbacks, and dynamic updates
- **Custom styling**: Different themes and configurations per chart
""")

# Sidebar controls
with st.sidebar:
    st.header("Chart Controls")
    
    # Data settings
    days = st.slider("Days of data", 30, 365, 100)
    
    # Sync settings
    st.subheader("Synchronization")
    sync_enabled = st.checkbox("Enable synchronization", True)
    sync_crosshair = st.checkbox("Sync crosshair", True)
    sync_time_range = st.checkbox("Sync time range", True)
    
    # Theme settings
    st.subheader("Theme")
    theme = st.selectbox("Color theme", ["Light", "Dark", "Trading View"])
    
    # Indicator settings
    st.subheader("Indicators")
    show_sma = st.checkbox("Show SMA", True)
    show_volume = st.checkbox("Show Volume", True)
    show_rsi = st.checkbox("Show RSI", True)
    show_macd = st.checkbox("Show MACD", True)
    
    # Update data
    if st.button("Refresh Data"):
        st.cache_data.clear()

# Generate data
df = generate_sample_data(days)

# Theme configurations
themes = {
    "Light": {
        "layout": {
            "background": {"type": "solid", "color": "white"},
            "textColor": "black"
        },
        "grid": {
            "vertLines": {"color": "rgba(197, 203, 206, 0.5)"},
            "horzLines": {"color": "rgba(197, 203, 206, 0.5)"}
        }
    },
    "Dark": {
        "layout": {
            "background": {"type": "solid", "color": "#131722"},
            "textColor": "#d1d4dc"
        },
        "grid": {
            "vertLines": {"color": "rgba(42, 46, 57, 0.6)"},
            "horzLines": {"color": "rgba(42, 46, 57, 0.6)"}
        }
    },
    "Trading View": {
        "layout": {
            "background": {"type": "solid", "color": "#1e222d"},
            "textColor": "#9598a1"
        },
        "grid": {
            "vertLines": {"color": "rgba(42, 46, 57, 0)"},
            "horzLines": {"color": "rgba(42, 46, 57, 0.6)"}
        }
    }
}

selected_theme = themes[theme]

# Create chart group
chart_group = ChartGroup(
    sync_enabled=sync_enabled,
    sync_crosshair=sync_crosshair,
    sync_time_range=sync_time_range
)

# Main price chart
main_chart = Chart(
    height=400,
    **selected_theme,
    crosshair={"mode": CrosshairMode.NORMAL},
    right_price_scale={
        "borderColor": "rgba(197, 203, 206, 0.8)",
        "mode": PriceScaleMode.NORMAL
    },
    time_scale={
        "borderColor": "rgba(197, 203, 206, 0.8)",
        "timeVisible": True,
        "secondsVisible": False
    },
    watermark={
        "visible": True,
        "fontSize": 24,
        "horzAlign": 'center',
        "vertAlign": 'center',
        "color": 'rgba(171, 71, 188, 0.1)',
        "text": f'{df["close"].iloc[-1]:.2f}',
    }
)

# Add candlestick series
candlestick_data = format_data_for_chart(df, ['open', 'high', 'low', 'close'])
main_chart.add_series(
    SeriesType.CANDLESTICK,
    candlestick_data,
    name="Price",
    options={
        "upColor": '#26a69a',
        "downColor": '#ef5350',
        "borderVisible": False,
        "wickUpColor": '#26a69a',
        "wickDownColor": '#ef5350'
    }
)

# Add SMA indicators
if show_sma:
    sma_20_data = format_data_for_chart(df[df['sma_20'].notna()], ['sma_20'])
    main_chart.add_series(
        SeriesType.LINE,
        sma_20_data,
        name="SMA 20",
        options={
            "color": '#2962FF',
            "lineWidth": 2,
            "priceScaleId": "right"
        }
    )
    
    sma_50_data = format_data_for_chart(df[df['sma_50'].notna()], ['sma_50'])
    main_chart.add_series(
        SeriesType.LINE,
        sma_50_data,
        name="SMA 50",
        options={
            "color": '#FF6D00',
            "lineWidth": 2,
            "priceScaleId": "right"
        }
    )

# Add price line for current price
current_price = df['close'].iloc[-1]
main_chart.add_price_line(
    price=current_price,
    color='#4CAF50',
    line_width=2,
    line_style=LineStyle.DASHED,
    axis_label_visible=True,
    title='Current'
)

chart_group.add_chart(main_chart)

# Volume chart
if show_volume:
    volume_chart = Chart(
        height=100,
        **selected_theme,
        time_scale={"visible": False},
        right_price_scale={
            "scaleMargins": {"top": 0.1, "bottom": 0}
        }
    )
    
    volume_data = format_data_for_chart(df, ['volume'])
    volume_chart.add_series(
        SeriesType.HISTOGRAM,
        volume_data,
        name="Volume",
        options={
            "color": '#26a69a',
            "priceFormat": {"type": 'volume'},
            "priceScaleId": "right"
        }
    )
    
    chart_group.add_chart(volume_chart)

# RSI chart
if show_rsi:
    rsi_chart = Chart(
        height=150,
        **selected_theme,
        time_scale={"visible": False},
        right_price_scale={
            "scaleMargins": {"top": 0.1, "bottom": 0.1}
        }
    )
    
    rsi_data = format_data_for_chart(df[df['rsi'].notna()], ['rsi'])
    rsi_chart.add_series(
        SeriesType.LINE,
        rsi_data,
        name="RSI",
        options={
            "color": '#9C27B0',
            "lineWidth": 2,
            "priceScaleId": "right"
        }
    )
    
    # Add overbought/oversold lines
    rsi_chart.add_price_line(
        price=70,
        color='#FF5252',
        line_width=1,
        line_style=LineStyle.DOTTED,
        title='Overbought'
    )
    rsi_chart.add_price_line(
        price=30,
        color='#4CAF50',
        line_width=1,
        line_style=LineStyle.DOTTED,
        title='Oversold'
    )
    
    chart_group.add_chart(rsi_chart)

# MACD chart
if show_macd:
    macd_chart = Chart(
        height=200,
        **selected_theme,
        time_scale={"visible": True},
        right_price_scale={
            "scaleMargins": {"top": 0.1, "bottom": 0.1}
        }
    )
    
    # MACD line
    macd_data = format_data_for_chart(df[df['macd'].notna()], ['macd'])
    macd_chart.add_series(
        SeriesType.LINE,
        macd_data,
        name="MACD",
        options={
            "color": '#2196F3',
            "lineWidth": 2,
            "priceScaleId": "right"
        }
    )
    
    # Signal line
    signal_data = format_data_for_chart(df[df['signal'].notna()], ['signal'])
    macd_chart.add_series(
        SeriesType.LINE,
        signal_data,
        name="Signal",
        options={
            "color": '#FF9800',
            "lineWidth": 2,
            "priceScaleId": "right"
        }
    )
    
    # Histogram
    histogram_data = format_data_for_chart(df[df['histogram'].notna()], ['histogram'])
    macd_chart.add_series(
        SeriesType.HISTOGRAM,
        histogram_data,
        name="Histogram",
        options={
            "color": '#26a69a',
            "priceScaleId": "right"
        }
    )
    
    chart_group.add_chart(macd_chart)

# Event callbacks
def on_click(event_data):
    st.session_state.last_click = event_data
    st.info(f"Clicked at time: {event_data.get('time', 'N/A')}")

def on_crosshair_move(event_data):
    if 'crosshair_data' not in st.session_state:
        st.session_state.crosshair_data = {}
    st.session_state.crosshair_data = event_data

# Register callbacks
chart_group.on_click(on_click)
chart_group.on_crosshair_move(on_crosshair_move)

# Render the chart group
chart_group.render(key="advanced_charts")

# Display event information
col1, col2 = st.columns(2)

with col1:
    st.subheader("Last Click Event")
    if 'last_click' in st.session_state:
        st.json(st.session_state.last_click)
    else:
        st.info("Click on any chart to see event data")

with col2:
    st.subheader("Current Crosshair Position")
    if 'crosshair_data' in st.session_state:
        st.json(st.session_state.crosshair_data)
    else:
        st.info("Move crosshair to see position data")

# Dynamic update example
st.subheader("Dynamic Updates")
if st.button("Add Random Price Alert"):
    random_price = np.random.uniform(df['low'].min(), df['high'].max())
    st.success(f"Price alert added at {random_price:.2f}")
    # In a real application, you would update the chart with this price line

# Performance metrics
st.subheader("Performance Metrics")
metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)

with metrics_col1:
    change = df['close'].iloc[-1] - df['close'].iloc[-2]
    change_pct = (change / df['close'].iloc[-2]) * 100
    st.metric("Last Price", f"${df['close'].iloc[-1]:.2f}", f"{change_pct:.2f}%")

with metrics_col2:
    st.metric("Volume", f"{df['volume'].iloc[-1]:,.0f}", 
              f"{((df['volume'].iloc[-1] / df['volume'].iloc[-2] - 1) * 100):.1f}%")

with metrics_col3:
    st.metric("RSI", f"{df['rsi'].iloc[-1]:.1f}" if pd.notna(df['rsi'].iloc[-1]) else "N/A")

with metrics_col4:
    st.metric("MACD", f"{df['macd'].iloc[-1]:.3f}" if pd.notna(df['macd'].iloc[-1]) else "N/A")