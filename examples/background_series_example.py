"""
Background Series Example for Streamlit Lightweight Charts.

This example demonstrates how to use the BackgroundSeries to create
indicator-based background shading on charts. The background color
is interpolated between minColor and maxColor based on the indicator value.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from streamlit_lightweight_charts_pro.charts import Chart
from streamlit_lightweight_charts_pro.charts.series import BackgroundSeries, LineSeries
from streamlit_lightweight_charts_pro.charts.options.line_options import LineOptions
from streamlit_lightweight_charts_pro.data import BackgroundData, LineData


def generate_price_data(days=30):
    """Generate sample price data."""
    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
    prices = 100 + np.cumsum(np.random.randn(days) * 2)
    
    return [
        LineData(time=date.strftime("%Y-%m-%d"), value=float(price))
        for date, price in zip(dates, prices)
    ]


def generate_rsi_background_data(days=30):
    """Generate RSI-based background data."""
    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
    
    # Simulate RSI values (0-100 range, normalized to 0-1)
    rsi_raw = 50 + 30 * np.sin(np.linspace(0, 4 * np.pi, days)) + np.random.randn(days) * 5
    rsi_normalized = np.clip(rsi_raw, 0, 100) / 100
    
    return [
        BackgroundData(
            time=date.strftime("%Y-%m-%d"),
            value=float(value),
            minColor="#FFE5E5",  # Light red for oversold
            maxColor="#E5FFE5"   # Light green for overbought
        )
        for date, value in zip(dates, rsi_normalized)
    ]


def generate_sentiment_background_data(days=30):
    """Generate sentiment-based background data."""
    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
    
    # Simulate sentiment scores (0-1 range)
    sentiment = np.random.beta(2, 2, days)  # Beta distribution for realistic sentiment
    
    return [
        BackgroundData(
            time=date.strftime("%Y-%m-%d"),
            value=float(value),
            minColor="#FF6B6B",  # Red for bearish
            maxColor="#4ECDC4"   # Teal for bullish
        )
        for date, value in zip(dates, sentiment)
    ]


def main():
    """Main function to run the Streamlit app."""
    st.set_page_config(page_title="Background Series Example", layout="wide")
    
    st.title("Background Series Example")
    st.markdown("""
    This example demonstrates the **BackgroundSeries** feature that creates
    indicator-based background shading. The background color changes based on
    indicator values, perfect for visualizing market conditions, sentiment,
    or technical indicators.
    """)
    
    # Sidebar configuration
    st.sidebar.header("Configuration")
    
    indicator_type = st.sidebar.selectbox(
        "Select Indicator Type",
        ["RSI (Relative Strength Index)", "Market Sentiment", "Custom"]
    )
    
    days = st.sidebar.slider("Number of Days", 10, 90, 30)
    
    show_price = st.sidebar.checkbox("Show Price Line", value=True)
    
    opacity = st.sidebar.slider("Background Opacity", 0.1, 0.5, 0.2, 0.05)
    
    # Generate data based on selection
    if indicator_type == "RSI (Relative Strength Index)":
        background_data = generate_rsi_background_data(days)
        st.info("📊 RSI Background: Red indicates oversold, Green indicates overbought")
    elif indicator_type == "Market Sentiment":
        background_data = generate_sentiment_background_data(days)
        st.info("📈 Sentiment Background: Red for bearish, Teal for bullish sentiment")
    else:  # Custom
        col1, col2 = st.columns(2)
        with col1:
            min_color = st.color_picker("Min Color", "#FFE5E5")
        with col2:
            max_color = st.color_picker("Max Color", "#E5FFE5")
        
        # Generate custom data
        dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
        values = np.random.uniform(0, 1, days)
        
        background_data = [
            BackgroundData(
                time=date.strftime("%Y-%m-%d"),
                value=float(value),
                minColor=min_color,
                maxColor=max_color
            )
            for date, value in zip(dates, values)
        ]
        st.info("🎨 Custom Background: Colors interpolate based on indicator values")
    
    # Create chart
    series = []
    
    # Add background series
    background_series = BackgroundSeries(data=background_data)
    # Note: In frontend, you would set opacity through options
    series.append(background_series)
    
    # Add price line if enabled
    if show_price:
        price_data = generate_price_data(days)
        line_series = LineSeries(
            data=price_data,
            line_options=LineOptions(
                color="#2196F3",
                line_width=2
            )
        )
        series.append(line_series)
    
    # Create and render chart
    chart = Chart(series=series)
    
    # Display chart (in real implementation)
    st.subheader("Chart Visualization")
    st.markdown("""
    ```python
    # Create background series
    background_series = BackgroundSeries(data=background_data)
    
    # Create chart with background
    chart = Chart(series=[background_series, line_series])
    
    # Render chart
    chart.render(key="background_chart")
    ```
    """)
    
    # Show data sample
    with st.expander("View Background Data Sample"):
        sample_data = pd.DataFrame([
            {
                "time": d.time,
                "value": f"{d.value:.3f}",
                "minColor": d.minColor,
                "maxColor": d.maxColor
            }
            for d in background_data[:10]
        ])
        st.dataframe(sample_data)
    
    # Show code example
    with st.expander("View Complete Code"):
        st.code("""
# Create RSI background data
background_data = [
    BackgroundData(
        time="2024-01-01",
        value=0.3,  # RSI normalized to 0-1
        minColor="#FFE5E5",  # Oversold color
        maxColor="#E5FFE5"   # Overbought color
    ),
    # ... more data points
]

# Create background series
background_series = BackgroundSeries(data=background_data)

# Create price series
price_series = LineSeries(
    data=price_data,
    line_options=LineOptions(color="#2196F3")
)

# Create chart with both series
chart = Chart(series=[background_series, price_series])

# Render the chart
chart.render(key="rsi_background_chart")
        """, language="python")
    
    # Additional information
    st.markdown("---")
    st.subheader("Use Cases")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **📊 Technical Indicators**
        - RSI overbought/oversold zones
        - MACD signal strength
        - Bollinger Band positions
        """)
    
    with col2:
        st.markdown("""
        **📈 Market Conditions**
        - Bull/bear market phases
        - Volatility regimes
        - Trend strength
        """)
    
    with col3:
        st.markdown("""
        **🎯 Custom Indicators**
        - Sentiment analysis
        - Risk levels
        - Custom scoring systems
        """)


if __name__ == "__main__":
    main()