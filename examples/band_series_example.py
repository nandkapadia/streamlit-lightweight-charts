"""
Band Series Example - Bollinger Bands and Other Band Charts

This example demonstrates how to use the BandSeries to create various types
of band charts, including Bollinger Bands, Keltner Channels, and custom bands.

The BandSeries visualizes three data lines simultaneously:
- Upper band (e.g., upper Bollinger Band)
- Middle band (e.g., moving average)
- Lower band (e.g., lower Bollinger Band)

Features demonstrated:
- Custom styling for each band line
- Fill colors between bands
- Markers for signal points
- Different line styles and types
- Integration with other chart types
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from streamlit_lightweight_charts_pro.charts.series.band import BandSeries
from streamlit_lightweight_charts_pro.charts.series.candlestick import CandlestickSeries
from streamlit_lightweight_charts_pro.charts.single_pane_chart import SinglePaneChart
from streamlit_lightweight_charts_pro.data import BandData, Marker, MarkerPosition, MarkerShape
from streamlit_lightweight_charts_pro.type_definitions import LineStyle, LineType


def generate_sample_data(periods=100):
    """Generate sample OHLC data with realistic price movements."""
    np.random.seed(42)
    
    # Generate base price series with random walk
    base_price = 100.0
    prices = [base_price]
    
    for _ in range(periods - 1):
        # Random walk with mean reversion
        change = np.random.normal(0, 1) * 0.02
        new_price = prices[-1] * (1 + change)
        prices.append(new_price)
    
    # Create OHLC data
    dates = pd.date_range("2024-01-01", periods=periods, freq="D")
    
    ohlc_data = []
    for i, (date, close) in enumerate(zip(dates, prices)):
        # Generate realistic OHLC from close price
        volatility = 0.02
        high = close * (1 + abs(np.random.normal(0, volatility)))
        low = close * (1 - abs(np.random.normal(0, volatility)))
        
        if i == 0:
            open_price = close
        else:
            open_price = ohlc_data[-1]["close"]
        
        ohlc_data.append({
            "datetime": date,
            "open": open_price,
            "high": high,
            "low": low,
            "close": close,
        })
    
    return pd.DataFrame(ohlc_data)


def calculate_bollinger_bands(df, period=20, std_dev=2):
    """Calculate Bollinger Bands from OHLC data."""
    # Use close prices for calculation
    close_prices = df["close"]
    
    # Calculate moving average
    sma = close_prices.rolling(window=period, min_periods=1).mean()
    
    # Calculate standard deviation
    std = close_prices.rolling(window=period, min_periods=1).std()
    
    # Fill any NaN values that might occur
    sma = sma.bfill().ffill()
    std = std.bfill().ffill()
    
    # Calculate bands
    upper_band = sma + (std_dev * std)
    lower_band = sma - (std_dev * std)
    
    return pd.DataFrame({
        "datetime": df["datetime"],
        "upper": upper_band,
        "middle": sma,
        "lower": lower_band,
    })


def calculate_keltner_channels(df, period=20, multiplier=2):
    """Calculate Keltner Channels from OHLC data."""
    # Calculate typical price
    typical_price = (df["high"] + df["low"] + df["close"]) / 3
    
    # Calculate EMA of typical price
    ema = typical_price.ewm(span=period).mean()
    
    # Calculate Average True Range (ATR)
    high_low = df["high"] - df["low"]
    high_close = np.abs(df["high"] - df["close"].shift())
    low_close = np.abs(df["low"] - df["close"].shift())
    
    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = true_range.rolling(window=period, min_periods=1).mean()
    
    # Fill any NaN values that might occur
    ema = ema.bfill().ffill()
    atr = atr.bfill().ffill()
    
    # Calculate channels
    upper_channel = ema + (multiplier * atr)
    lower_channel = ema - (multiplier * atr)
    
    return pd.DataFrame({
        "datetime": df["datetime"],
        "upper": upper_channel,
        "middle": ema,
        "lower": lower_channel,
    })


def main():
    """Main function to demonstrate BandSeries usage."""
    st.set_page_config(
        page_title="Band Series Examples",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 Band Series Examples")
    st.markdown("""
    This example demonstrates the **BandSeries** functionality for creating various types of band charts,
    including Bollinger Bands, Keltner Channels, and custom bands.
    
    The BandSeries visualizes three data lines simultaneously with customizable styling and fill areas.
    """)
    
    # Generate sample data
    ohlc_df = generate_sample_data(200)
    
    # Calculate different types of bands
    bollinger_df = calculate_bollinger_bands(ohlc_df, period=20, std_dev=2)
    keltner_df = calculate_keltner_channels(ohlc_df, period=20, multiplier=2)
    
    # Create tabs for different examples
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Bollinger Bands", 
        "📊 Keltner Channels", 
        "🎨 Custom Bands", 
        "🔗 Overlay Example"
    ])
    
    with tab1:
        st.header("Bollinger Bands")
        st.markdown("""
        **Bollinger Bands** are a technical analysis tool consisting of:
        - **Upper Band**: 20-period SMA + (2 × Standard Deviation)
        - **Middle Band**: 20-period Simple Moving Average
        - **Lower Band**: 20-period SMA - (2 × Standard Deviation)
        
        They help identify overbought/oversold conditions and volatility expansion/contraction.
        """)
        
        # Create Bollinger Bands series
        bollinger_series = BandSeries(
            data=bollinger_df,
            upper_line_color="#4CAF50",  # Green for upper band
            middle_line_color="#2196F3",  # Blue for middle band
            lower_line_color="#F44336",  # Red for lower band
            upper_line_width=2,
            middle_line_width=2,
            lower_line_width=2,
            upper_fill_color="rgba(76, 175, 80, 0.1)",  # Light green fill
            lower_fill_color="rgba(244, 67, 54, 0.1)",  # Light red fill
            line_type=LineType.SIMPLE,
        )
        
        # Add markers for signal points (when price touches bands)
        for i, row in ohlc_df.iterrows():
            if i < 20:  # Skip first 20 periods for calculation
                continue
                
            close_price = row["close"]
            upper_band = bollinger_df.iloc[i]["upper"]
            lower_band = bollinger_df.iloc[i]["lower"]
            
            # Add marker if price touches upper band (overbought)
            if abs(close_price - upper_band) < 0.5:
                bollinger_series.add_marker(
                    time=str(row["datetime"]),
                    position=MarkerPosition.ABOVE_BAR,
                    color="#FF9800",
                    shape=MarkerShape.ARROW_DOWN,
                    text="Overbought",
                    size=12,
                )
            
            # Add marker if price touches lower band (oversold)
            elif abs(close_price - lower_band) < 0.5:
                bollinger_series.add_marker(
                    time=str(row["datetime"]),
                    position=MarkerPosition.BELOW_BAR,
                    color="#4CAF50",
                    shape=MarkerShape.ARROW_UP,
                    text="Oversold",
                    size=12,
                )
        
        # Create chart
        chart = SinglePaneChart(
            series=[bollinger_series],
            options={
                "height": 400,
                "layout": {
                    "background": {"color": "#ffffff"},
                    "textColor": "#131722",
                },
                "grid": {
                    "vertLines": {"visible": True},
                    "horzLines": {"visible": True},
                },
            }
        )
        
        chart.render(key="bollinger_bands_chart")
        
        # Display statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Data Points", len(bollinger_df))
        with col2:
            st.metric("Upper Band Range", f"{bollinger_df['upper'].min():.2f} - {bollinger_df['upper'].max():.2f}")
        with col3:
            st.metric("Lower Band Range", f"{bollinger_df['lower'].min():.2f} - {bollinger_df['lower'].max():.2f}")
    
    with tab2:
        st.header("Keltner Channels")
        st.markdown("""
        **Keltner Channels** are volatility-based bands consisting of:
        - **Upper Channel**: EMA + (2 × ATR)
        - **Middle Channel**: Exponential Moving Average
        - **Lower Channel**: EMA - (2 × ATR)
        
        They are useful for identifying trend direction and volatility breakouts.
        """)
        
        # Create Keltner Channels series with different styling
        keltner_series = BandSeries(
            data=keltner_df,
            upper_line_color="#9C27B0",  # Purple for upper channel
            middle_line_color="#FF9800",  # Orange for middle channel
            lower_line_color="#607D8B",  # Blue-grey for lower channel
            upper_line_width=2,
            middle_line_width=3,  # Thicker middle line
            lower_line_width=2,
            upper_line_style=LineStyle.DASHED,  # Dashed upper line
            middle_line_style=LineStyle.SOLID,  # Solid middle line
            lower_line_style=LineStyle.DASHED,  # Dashed lower line
            upper_fill_color="rgba(156, 39, 176, 0.1)",  # Light purple fill
            lower_fill_color="rgba(96, 125, 139, 0.1)",  # Light blue-grey fill
            line_type=LineType.CURVED,  # Curved lines
        )
        
        # Create chart
        chart = SinglePaneChart(
            series=[keltner_series],
            options={
                "height": 400,
                "layout": {
                    "background": {"color": "#ffffff"},
                    "textColor": "#131722",
                },
                "grid": {
                    "vertLines": {"visible": True},
                    "horzLines": {"visible": True},
                },
            }
        )
        
        chart.render(key="keltner_channels_chart")
        
        # Display statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Data Points", len(keltner_df))
        with col2:
            st.metric("Upper Channel Range", f"{keltner_df['upper'].min():.2f} - {keltner_df['upper'].max():.2f}")
        with col3:
            st.metric("Lower Channel Range", f"{keltner_df['lower'].min():.2f} - {keltner_df['lower'].max():.2f}")
    
    with tab3:
        st.header("Custom Bands")
        st.markdown("""
        **Custom Bands** demonstrate the flexibility of BandSeries for creating
        any type of three-line visualization with custom styling and behavior.
        """)
        
        # Create custom bands with different periods
        custom_df = pd.DataFrame({
            "datetime": ohlc_df["datetime"],
            "upper": ohlc_df["close"] * 1.1,  # 10% above close
            "middle": ohlc_df["close"],  # Close price
            "lower": ohlc_df["close"] * 0.9,  # 10% below close
        })
        
        # Create custom band series with unique styling
        custom_series = BandSeries(
            data=custom_df,
            upper_line_color="#E91E63",  # Pink
            middle_line_color="#3F51B5",  # Indigo
            lower_line_color="#009688",  # Teal
            upper_line_width=1,
            middle_line_width=2,
            lower_line_width=1,
            upper_line_style=LineStyle.DOTTED,  # Dotted upper line
            middle_line_style=LineStyle.SOLID,  # Solid middle line
            lower_line_style=LineStyle.DOTTED,  # Dotted lower line
            upper_fill_color="rgba(233, 30, 99, 0.15)",  # Light pink fill
            lower_fill_color="rgba(0, 150, 136, 0.15)",  # Light teal fill
            line_type=LineType.SIMPLE,
        )
        
        # Create chart
        chart = SinglePaneChart(
            series=[custom_series],
            options={
                "height": 400,
                "layout": {
                    "background": {"color": "#ffffff"},
                    "textColor": "#131722",
                },
                "grid": {
                    "vertLines": {"visible": True},
                    "horzLines": {"visible": True},
                },
            }
        )
        
        chart.render(key="custom_bands_chart")
        
        # Display statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Data Points", len(custom_df))
        with col2:
            st.metric("Upper Band Range", f"{custom_df['upper'].min():.2f} - {custom_df['upper'].max():.2f}")
        with col3:
            st.metric("Lower Band Range", f"{custom_df['lower'].min():.2f} - {custom_df['lower'].max():.2f}")
    
    with tab4:
        st.header("Band Series as Overlay")
        st.markdown("""
        **Overlay Example** shows how BandSeries can be used as an overlay
        on other chart types, such as candlestick charts.
        """)
        
        # Create candlestick series
        candlestick_series = CandlestickSeries(
            data=ohlc_df.iloc[-50:],  # Last 50 points
            up_color="#4CAF50",
            down_color="#F44336",
            border_visible=True,
        )
        
        # Create band series as overlay
        overlay_series = BandSeries(
            data=bollinger_df.iloc[-50:],  # Last 50 points
            upper_line_color="#4CAF50",
            middle_line_color="#2196F3",
            lower_line_color="#F44336",
            upper_line_width=1,
            middle_line_width=1,
            lower_line_width=1,
            upper_fill_color="rgba(76, 175, 80, 0.05)",  # Very light fill
            lower_fill_color="rgba(244, 67, 54, 0.05)",  # Very light fill
            line_type=LineType.SIMPLE,
        )
        
        # Create chart with both series
        chart = SinglePaneChart(
            series=[candlestick_series, overlay_series],
            options={
                "height": 400,
                "layout": {
                    "background": {"color": "#ffffff"},
                    "textColor": "#131722",
                },
                "grid": {
                    "vertLines": {"visible": True},
                    "horzLines": {"visible": True},
                },
            }
        )
        
        chart.render(key="overlay_bands_chart")
        
        st.info("""
        💡 **Tip**: The BandSeries can be used as an overlay on any other chart type.
        The bands help identify support/resistance levels and volatility patterns.
        """)
    
    # Configuration sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        st.subheader("Band Settings")
        period = st.slider("Period", 5, 50, 20, help="Period for moving average calculation")
        std_dev = st.slider("Standard Deviation", 1.0, 3.0, 2.0, step=0.1, help="Multiplier for standard deviation")
        
        st.subheader("Styling Options")
        line_width = st.slider("Line Width", 1, 5, 2, help="Width of band lines")
        fill_opacity = st.slider("Fill Opacity", 0.0, 1.0, 0.1, step=0.05, help="Opacity of fill areas")
        
        line_type = st.selectbox(
            "Line Type",
            ["Simple", "Curved"],
            help="Type of line interpolation"
        )
        
        st.subheader("Data Info")
        st.metric("Total Data Points", len(ohlc_df))
        st.metric("Date Range", f"{ohlc_df['datetime'].min().strftime('%Y-%m-%d')} to {ohlc_df['datetime'].max().strftime('%Y-%m-%d')}")
        
        st.subheader("About")
        st.markdown("""
        **BandSeries** provides a powerful way to visualize three-line indicators
        with customizable styling, fill areas, and integration capabilities.
        
        Perfect for technical analysis indicators like:
        - Bollinger Bands
        - Keltner Channels
        - Donchian Channels
        - Custom envelope indicators
        """)


if __name__ == "__main__":
    main() 