"""Simple example using pandas DataFrames with utility functions."""

import streamlit as st
import pandas as pd
import numpy as np
from streamlit_lightweight_charts import (
    Chart, ChartOptions, LayoutOptions,
    LineSeries, CandlestickSeries, HistogramSeries,
    LineSeriesOptions, CandlestickSeriesOptions, HistogramSeriesOptions,
    Background
)
from streamlit_lightweight_charts.utils import (
    df_to_line_data, df_to_ohlc_data, df_to_histogram_data
)


@st.cache_data
def generate_stock_data():
    """Generate sample stock data."""
    # Generate 100 days of data
    dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
    
    # Generate price data with trend and noise
    base_price = 100
    trend = np.linspace(0, 20, 100)
    noise = np.random.randn(100) * 3
    close_prices = base_price + trend + noise
    
    # Generate OHLC data
    df = pd.DataFrame(index=dates)
    df['close'] = close_prices
    df['open'] = df['close'].shift(1).fillna(base_price)
    df['high'] = df[['open', 'close']].max(axis=1) + np.abs(np.random.randn(100) * 2)
    df['low'] = df[['open', 'close']].min(axis=1) - np.abs(np.random.randn(100) * 2)
    df['volume'] = np.random.randint(100000, 1000000, 100)
    
    return df


def main():
    st.title("DataFrame Integration Example")
    st.markdown("This example shows how easy it is to use pandas DataFrames with the OOP API.")
    
    # Generate sample data
    df = generate_stock_data()
    
    # Show the DataFrame
    st.subheader("Sample Stock Data")
    st.dataframe(df.head(10))
    
    # Create chart options
    chart_options = ChartOptions(
        height=400,
        layout=LayoutOptions(
            background=Background.solid('#f0f0f0'),
            text_color='#333'
        )
    )
    
    # Example 1: Simple line chart from DataFrame
    st.subheader("1. Line Chart - Closing Prices")
    
    # Convert DataFrame to line data using utility function
    line_data = df_to_line_data(df, value_column='close')
    
    # Create line series
    line_series = LineSeries(
        data=line_data,
        options=LineSeriesOptions(
            color='#2196F3',
            line_width=2
        )
    )
    
    # Create and render chart
    Chart(series=line_series, options=chart_options).render(key='line_chart')
    
    # Example 2: Candlestick chart
    st.subheader("2. Candlestick Chart")
    
    # Convert DataFrame to OHLC data
    ohlc_data = df_to_ohlc_data(df)
    
    # Create candlestick series
    candlestick_series = CandlestickSeries(
        data=ohlc_data,
        options=CandlestickSeriesOptions(
            up_color='#4CAF50',
            down_color='#F44336'
        )
    )
    
    # Create and render chart
    Chart(series=candlestick_series, options=chart_options).render(key='candlestick_chart')
    
    # Example 3: Volume histogram
    st.subheader("3. Volume Histogram")
    
    # Convert DataFrame to histogram data
    histogram_data = df_to_histogram_data(
        df, 
        value_column='volume',
        positive_color='#4CAF50',
        negative_color='#F44336'
    )
    
    # Create histogram series
    histogram_series = HistogramSeries(
        data=histogram_data,
        options=HistogramSeriesOptions(color='#607D8B')
    )
    
    # Create chart with smaller height for volume
    volume_options = ChartOptions(height=150)
    Chart(series=histogram_series, options=volume_options).render(key='volume_chart')
    
    # Example 4: Multiple series on one chart
    st.subheader("4. Combined Chart - Price and Moving Average")
    
    # Calculate moving average
    df['ma20'] = df['close'].rolling(window=20).mean()
    
    # Create data for both series
    price_data = df_to_line_data(df, value_column='close')
    ma_data = df_to_line_data(df.dropna(), value_column='ma20')  # Drop NaN values
    
    # Create series
    price_series = LineSeries(
        data=price_data,
        options=LineSeriesOptions(
            color='#2196F3',
            line_width=2
        )
    )
    
    ma_series = LineSeries(
        data=ma_data,
        options=LineSeriesOptions(
            color='#FF9800',
            line_width=2
        )
    )
    
    # Create and render chart with both series
    Chart(
        series=[price_series, ma_series],
        options=chart_options
    ).render(key='combined_chart')
    
    # Show time extraction
    st.subheader("5. Working with Time Data")
    st.write("You can easily access time data as pandas Timestamps:")
    
    # Get first few data points
    first_point = line_data[0]
    st.code(f"First data point time: {first_point.time}")
    st.code(f"Type: {type(first_point.time)}")
    st.code(f"Day of week: {first_point.time.day_name()}")
    st.code(f"Month: {first_point.time.month_name()}")


if __name__ == "__main__":
    main()