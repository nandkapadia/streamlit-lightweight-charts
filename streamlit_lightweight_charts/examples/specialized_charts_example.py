"""Example demonstrating specialized charts with type safety and validation."""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from streamlit_lightweight_charts import (
    # Specialized charts
    CandlestickChart, LineChart, AreaChart,
    BarChart, HistogramChart, BaselineChart,
    # Options
    ChartOptions, LayoutOptions,
    CandlestickSeriesOptions, LineSeriesOptions,
    # Data types
    OhlcData, SingleValueData, HistogramData,
    # Utilities
    candlestick_chart_from_df, line_chart_from_df
)


def main():
    st.title("Specialized Charts Example")
    st.markdown("This example demonstrates the specialized chart classes with built-in data validation.")
    
    # Generate sample data
    dates = pd.date_range(start='2024-01-01', periods=50, freq='D')
    df = pd.DataFrame(index=dates)
    
    # Generate OHLC data
    df['close'] = 100 + np.cumsum(np.random.randn(50) * 2)
    df['open'] = df['close'].shift(1).fillna(100)
    df['high'] = df[['open', 'close']].max(axis=1) + np.abs(np.random.randn(50))
    df['low'] = df[['open', 'close']].min(axis=1) - np.abs(np.random.randn(50))
    df['volume'] = np.random.randint(1000, 10000, 50)
    
    # Create chart options
    chart_options = ChartOptions(
        height=400,
        layout=LayoutOptions(
            text_color='#333'
        )
    )
    
    # Example 1: CandlestickChart with type validation
    st.subheader("1. CandlestickChart with Type Validation")
    
    # Create OHLC data objects
    ohlc_data = []
    for timestamp, row in df.iterrows():
        ohlc_data.append(OhlcData(
            time=timestamp,
            open=row['open'],
            high=row['high'],
            low=row['low'],
            close=row['close']
        ))
    
    # Create candlestick chart - will validate that all data is OhlcData
    candlestick_chart = CandlestickChart(
        data=ohlc_data,
        options=chart_options,
        series_options=CandlestickSeriesOptions(
            up_color='#26a69a',
            down_color='#ef5350',
            border_visible=False
        )
    )
    candlestick_chart.render(key='candlestick')
    
    st.code("""
# The CandlestickChart validates that all data is OhlcData
# This will raise TypeError:
# candlestick_chart = CandlestickChart(
#     data=[SingleValueData(time='2024-01-01', value=100)]  # Wrong data type!
# )
    """)
    
    # Example 2: LineChart with multiple lines
    st.subheader("2. LineChart with Multiple Lines")
    
    # Create line data
    close_data = []
    for timestamp, value in df['close'].items():
        close_data.append(SingleValueData(time=timestamp, value=value))
    
    # Create MA data
    df['ma10'] = df['close'].rolling(window=10).mean()
    ma_data = []
    for timestamp, value in df['ma10'].dropna().items():
        ma_data.append(SingleValueData(time=timestamp, value=value))
    
    # Create line chart with first line
    line_chart = LineChart(
        data=close_data,
        options=chart_options,
        series_options=LineSeriesOptions(
            color='#2196F3',
            line_width=2
        )
    )
    
    # Add second line (with validation)
    line_chart.add_line(
        data=ma_data,
        options=LineSeriesOptions(
            color='#FF9800',
            line_width=2
        )
    )
    
    line_chart.render(key='multi_line')
    
    # Example 3: Direct from DataFrame
    st.subheader("3. Creating Charts Directly from DataFrames")
    st.markdown("Use utility functions to create charts directly from pandas DataFrames:")
    
    # Create candlestick chart from DataFrame
    candlestick_from_df = candlestick_chart_from_df(
        df,
        chart_options=chart_options,
        series_options=CandlestickSeriesOptions(
            up_color='#4CAF50',
            down_color='#F44336'
        )
    )
    candlestick_from_df.render(key='candlestick_from_df')
    
    st.code("""
# Create chart directly from DataFrame
chart = candlestick_chart_from_df(
    df,
    chart_options=chart_options,
    series_options=CandlestickSeriesOptions(
        up_color='#4CAF50',
        down_color='#F44336'
    )
)
chart.render()
    """)
    
    # Example 4: Data validation demonstration
    st.subheader("4. Data Validation Examples")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("✅ **Valid data types**")
        st.code("""
# CandlestickChart requires OhlcData
ohlc = OhlcData(
    time='2024-01-01',
    open=100, high=105,
    low=98, close=102
)

# LineChart requires SingleValueData
line = SingleValueData(
    time='2024-01-01',
    value=100
)
        """)
    
    with col2:
        st.markdown("❌ **Invalid data types**")
        st.code("""
# This will raise TypeError:
# CandlestickChart expects OhlcData
try:
    chart = CandlestickChart(
        data=[SingleValueData(
            time='2024-01-01',
            value=100
        )]
    )
except TypeError as e:
    print(e)
# Output: All data items must
# be OhlcData instances
        """)
    
    # Example 5: Update data with validation
    st.subheader("5. Updating Chart Data")
    
    # Create initial chart
    initial_data = ohlc_data[:20]
    update_chart = CandlestickChart(
        data=initial_data,
        options=ChartOptions(height=300)
    )
    
    # Add button to update data
    if st.button("Update with more data"):
        # This will validate the new data
        update_chart.update_data(ohlc_data[:30])
    
    update_chart.render(key='update_chart')
    
    st.code("""
# Update chart data (with validation)
chart.update_data(new_ohlc_data)

# This will raise TypeError if wrong data type:
# chart.update_data([SingleValueData(...)])  # Wrong type!
    """)
    
    # Example 6: Benefits summary
    st.subheader("6. Benefits of Specialized Charts")
    
    st.markdown("""
    ### Type Safety
    - IDE auto-completion for chart-specific options
    - Type checking prevents runtime errors
    - Clear API for each chart type
    
    ### Data Validation
    - Ensures correct data format at construction time
    - Helpful error messages for incorrect data
    - Prevents common mistakes
    
    ### Simplified API
    - No need to manually create series
    - Chart type is explicit in the class name
    - Specialized methods like `add_line()` for LineChart
    
    ### Example: IDE Auto-completion
    ```python
    # When you type:
    chart = CandlestickChart(
        data=ohlc_data,
        series_options=CandlestickSeriesOptions(
            # IDE shows candlestick-specific options:
            up_color='#26a69a',
            down_color='#ef5350',
            wick_visible=True,
            border_visible=False,
            # ... etc
        )
    )
    ```
    """)


if __name__ == "__main__":
    main()