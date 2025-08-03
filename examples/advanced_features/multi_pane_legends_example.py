import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from streamlit_lightweight_charts_pro import (
    Chart,
    ChartOptions,
    CandlestickSeries,
    LineSeries,
    HistogramSeries,
)
from streamlit_lightweight_charts_pro.charts.options.layout_options import (
    LayoutOptions,
    PaneHeightOptions,
)
from streamlit_lightweight_charts_pro.charts.options.ui_options import LegendOptions
from streamlit_lightweight_charts_pro.data import CandlestickData, LineData, HistogramData

# Page configuration
st.set_page_config(page_title="Multi-Pane Legends Example", page_icon="📊", layout="wide")

st.title("📊 Multi-Pane Chart with Legends Example")
st.markdown(
    """
This example demonstrates a comprehensive multi-pane chart with legends for each pane:
- **Main Pane**: Candlestick chart with moving averages
- **RSI Pane**: Relative Strength Index indicator
- **Volume Pane**: Volume histogram with moving average
"""
)


# Generate realistic sample data
def generate_market_data(days=60):
    """Generate realistic market data with trends and volatility."""
    start_date = datetime(2024, 1, 1)
    end_date = start_date + timedelta(days=days)
    dates = pd.date_range(start=start_date, end=end_date, freq="D")

    # Base trend with some volatility
    np.random.seed(42)  # For reproducible results
    base_price = 100
    prices = []

    for i in range(len(dates)):
        # Add trend component
        trend = np.sin(i * 0.1) * 20

        # Add volatility
        volatility = np.random.normal(0, 3)

        # Add some momentum
        if i > 0:
            momentum = (prices[-1]["close"] - base_price) * 0.1
        else:
            momentum = 0

        # Calculate OHLC
        base_price += trend + volatility + momentum
        open_price = base_price
        high_price = base_price + abs(np.random.normal(0, 2))
        low_price = base_price - abs(np.random.normal(0, 2))
        close_price = base_price + np.random.normal(0, 1)

        # Ensure high >= max(open, close) and low <= min(open, close)
        high_price = max(high_price, open_price, close_price)
        low_price = min(low_price, open_price, close_price)

        prices.append(
            {
                "time": dates[i],
                "open": round(open_price, 2),
                "high": round(high_price, 2),
                "low": round(low_price, 2),
                "close": round(close_price, 2),
                "volume": int(np.random.uniform(1000, 10000)),
            }
        )

    return prices


# Calculate technical indicators
def calculate_indicators(prices):
    """Calculate RSI and moving averages."""
    df = pd.DataFrame(prices)

    # Calculate moving averages
    df["ma20"] = df["close"].rolling(window=20).mean()
    df["ma50"] = df["close"].rolling(window=50).mean()

    # Calculate RSI
    delta = df["close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df["rsi"] = 100 - (100 / (1 + rs))

    # Calculate volume moving average
    df["volume_ma"] = df["volume"].rolling(window=20).mean()

    return df


# Generate data
prices = generate_market_data(60)
df = calculate_indicators(prices)

# Convert to chart data
candlestick_data = [
    CandlestickData(
        time=row["time"], open=row["open"], high=row["high"], low=row["low"], close=row["close"]
    )
    for _, row in df.iterrows()
    if pd.notna(row["close"])
]

ma20_data = [
    LineData(time=row["time"], value=row["ma20"])
    for _, row in df.iterrows()
    if pd.notna(row["ma20"])
]

ma50_data = [
    LineData(time=row["time"], value=row["ma50"])
    for _, row in df.iterrows()
    if pd.notna(row["ma50"])
]

rsi_data = [
    LineData(time=row["time"], value=row["rsi"]) for _, row in df.iterrows() if pd.notna(row["rsi"])
]

volume_data = [
    HistogramData(time=row["time"], value=row["volume"])
    for _, row in df.iterrows()
    if pd.notna(row["volume"])
]

volume_ma_data = [
    LineData(time=row["time"], value=row["volume_ma"])
    for _, row in df.iterrows()
    if pd.notna(row["volume_ma"])
]

# Create the multi-pane chart
st.header("🎯 Multi-Pane Chart with Legends")

# Configuration options
col1, col2, col3 = st.columns(3)

with col1:
    legend_position = st.selectbox(
        "Legend Position", ["top-right", "top-left", "bottom-right", "bottom-left"], index=0
    )

    show_last_value = st.checkbox("Show Last Value", value=True)

with col2:
    legend_font_size = st.slider("Font Size", 8, 16, 12)

    legend_bg_color = st.color_picker(
        "Background Color",
        "#ffffff",
        help="Use rgba for transparency (e.g., rgba(255,255,255,0.9))",
    )

with col3:
    legend_border_color = st.color_picker("Border Color", "#e1e3e6")

    legend_padding = st.slider("Padding", 4, 16, 8)

# Create the chart
multi_pane_chart = Chart(
    options=ChartOptions(
        width=1200,
        height=800,
        layout=LayoutOptions(
            pane_heights={
                0: PaneHeightOptions(factor=3.0),  # Main chart (candlestick + MAs)
                1: PaneHeightOptions(factor=1.5),  # RSI
                2: PaneHeightOptions(factor=1.0),  # Volume
            }
        ),
        legend=LegendOptions(
            visible=True,
            position=legend_position,
            show_last_value=show_last_value,
            font_size=legend_font_size,
            background_color=legend_bg_color,
            border_color=legend_border_color,
            border_width=1,
            border_radius=4,
            padding=legend_padding,
            margin=4,
            z_index=1000,
        ),
    ),
    series=[
        # Main chart pane (pane_id=0)
        CandlestickSeries(data=candlestick_data, pane_id=0),
        LineSeries(data=ma20_data, pane_id=0),
        LineSeries(data=ma50_data, pane_id=0),
        # RSI pane (pane_id=1)
        LineSeries(data=rsi_data, pane_id=1),
        # Volume pane (pane_id=2)
        HistogramSeries(data=volume_data, pane_id=2),
        LineSeries(data=volume_ma_data, pane_id=2),
    ],
)

# Set titles and colors for the series
multi_pane_chart.series[0].title = "Price"
multi_pane_chart.series[1].title = "MA20"
multi_pane_chart.series[2].title = "MA50"
multi_pane_chart.series[3].title = "RSI (14)"
multi_pane_chart.series[4].title = "Volume"
multi_pane_chart.series[5].title = "Volume MA"

multi_pane_chart.series[1].line_options.color = "#2196f3"  # MA20
multi_pane_chart.series[2].line_options.color = "#ff9800"  # MA50
multi_pane_chart.series[3].line_options.color = "#9c27b0"  # RSI
multi_pane_chart.series[5].line_options.color = "#ff5722"  # Volume MA

# Debug: Check legend configuration
st.write(
    "Legend Configuration:",
    (
        multi_pane_chart.options.legend.asdict()
        if multi_pane_chart.options.legend
        else "No legend configured"
    ),
)

# Debug: Check chart configuration
chart_config = multi_pane_chart.to_frontend_config()
st.write("Chart Config Keys:", list(chart_config.keys()))
if "charts" in chart_config and len(chart_config["charts"]) > 0:
    st.write("First Chart Keys:", list(chart_config["charts"][0].keys()))
    if "chart" in chart_config["charts"][0]:
        st.write("Chart Options Keys:", list(chart_config["charts"][0]["chart"].keys()))
        if "legend" in chart_config["charts"][0]["chart"]:
            st.write("Legend in Chart Config:", chart_config["charts"][0]["chart"]["legend"])
        else:
            st.write("❌ Legend NOT found in chart config!")
            st.write("Available keys:", list(chart_config["charts"][0]["chart"].keys()))

# Render the chart
multi_pane_chart.render(key="multi_pane_legend")

# Code example
st.header("💻 Code Example")
st.markdown("Here's how to create this multi-pane chart with legends:")

code_example = """
# Create multi-pane chart with legends
chart = Chart(
    options=ChartOptions(
        width=1200,
        height=800,
        layout=LayoutOptions(
            pane_heights={
                0: PaneHeightOptions(factor=3.0),  # Main chart
                1: PaneHeightOptions(factor=1.5),  # RSI
                2: PaneHeightOptions(factor=1.0)   # Volume
            }
        ),
        legend=LegendOptions(
            visible=True,
            position="top-right",
            show_last_value=True,
            font_size=12,
            background_color="rgba(255, 255, 255, 0.9)",
            border_color="#e1e3e6",
            border_width=1,
            border_radius=4,
            padding=8,
            margin=4
        )
    ),
    series=[
        # Main chart pane
        CandlestickSeries(data=candlestick_data, pane_id=0, title="Price"),
        LineSeries(data=ma20_data, pane_id=0, title="MA20"),
        LineSeries(data=ma50_data, pane_id=0, title="MA50"),
        
        # RSI pane
        LineSeries(data=rsi_data, pane_id=1, title="RSI (14)"),
        
        # Volume pane
        HistogramSeries(data=volume_data, pane_id=2, title="Volume"),
        LineSeries(data=volume_ma_data, pane_id=2, title="Volume MA")
    ]
)

# Set colors for the series
chart.series[1].line_options.color = "#2196f3"  # MA20
chart.series[2].line_options.color = "#ff9800"  # MA50
chart.series[3].line_options.color = "#9c27b0"  # RSI
chart.series[5].line_options.color = "#ff5722"  # Volume MA
"""

st.code(code_example, language="python")

# Legend configuration details
st.header("🔧 Legend Configuration Options")
st.markdown(
    """
### Key Features Demonstrated:

1. **Multi-Pane Support**: Legends work across all panes, showing series from each pane
2. **Series Titles**: Each series has a descriptive title that appears in the legend
3. **Color Indicators**: Each series shows its color in the legend
4. **Last Value Display**: Shows the most recent value for each series
5. **Customizable Positioning**: Legend can be positioned in any corner
6. **Styling Options**: Full control over appearance and styling

### Legend Options Available:

- **visible**: Show/hide the legend (default: true)
- **position**: 'top-left', 'top-right', 'bottom-left', 'bottom-right'
- **show_last_value**: Display the last value for each series
- **font_size**: Font size in pixels
- **font_family**: Font family (default: 'Arial, sans-serif')
- **font_weight**: Font weight (default: 'normal')
- **color**: Text color (default: '#131722')
- **background_color**: Background color (supports rgba for transparency)
- **border_color**: Border color
- **border_width**: Border width in pixels
- **border_radius**: Border radius in pixels
- **padding**: Internal padding in pixels
- **margin**: External margin in pixels
- **z_index**: CSS z-index for layering

### Best Practices:

- Use descriptive series titles for better legend readability
- Choose appropriate legend positions that don't overlap with important chart data
- Use semi-transparent backgrounds for better chart visibility
- Consider font size and padding for different screen sizes
- Use consistent color schemes between series and legend indicators
"""
)

# Data summary
st.header("📈 Data Summary")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Data Points", len(candlestick_data))
    # Convert UNIX timestamps to datetime for display
    start_date = datetime.fromtimestamp(candlestick_data[0].time)
    end_date = datetime.fromtimestamp(candlestick_data[-1].time)
    st.metric("Date Range", f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")

with col2:
    latest_price = candlestick_data[-1]
    st.metric("Latest Close", f"${latest_price.close:.2f}")
    st.metric("Latest Volume", f"{volume_data[-1].value:,}")

with col3:
    latest_rsi = rsi_data[-1].value
    st.metric("Latest RSI", f"{latest_rsi:.1f}")
    rsi_status = "Overbought" if latest_rsi > 70 else "Oversold" if latest_rsi < 30 else "Neutral"
    st.metric("RSI Status", rsi_status)

st.markdown("---")
st.markdown(
    """
### Chart Components:
- **Main Pane**: Candlestick chart showing price action with 20-day and 50-day moving averages
- **RSI Pane**: 14-period Relative Strength Index showing momentum
- **Volume Pane**: Volume histogram with 20-period volume moving average

The legend displays all series across all panes, making it easy to identify and track each indicator.
"""
)
