"""Example demonstrating time handling with pandas and datetime objects."""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from streamlit_lightweight_charts import (
    Chart, ChartOptions, LineSeries, CandlestickSeries,
    SingleValueData, OhlcData, Marker,
    LineSeriesOptions, CandlestickSeriesOptions,
    MarkerShape, MarkerPosition
)


def create_sample_dataframe():
    """Create a sample DataFrame with datetime index."""
    # Create date range
    dates = pd.date_range(start='2024-01-01', end='2024-01-31', freq='D')
    
    # Create sample price data
    df = pd.DataFrame({
        'close': 100 + pd.Series(range(len(dates))).cumsum() * 0.5 + pd.Series(range(len(dates))).apply(lambda x: pd.np.random.randn() * 2),
        'volume': pd.Series(range(len(dates))).apply(lambda x: pd.np.random.randint(1000, 10000))
    }, index=dates)
    
    # Add OHLC data
    df['open'] = df['close'].shift(1).fillna(df['close'].iloc[0])
    df['high'] = df[['open', 'close']].max(axis=1) + pd.Series(range(len(dates))).apply(lambda x: pd.np.random.rand() * 2)
    df['low'] = df[['open', 'close']].min(axis=1) - pd.Series(range(len(dates))).apply(lambda x: pd.np.random.rand() * 2)
    
    return df


def main():
    st.title("Time Handling Example")
    st.markdown("This example shows how to use pandas DataFrames and datetime objects with the charts.")
    
    # Create sample data
    df = create_sample_dataframe()
    
    # Example 1: Using pandas Timestamp directly
    st.subheader("Example 1: Line Chart with Pandas Timestamps")
    
    # Create data points from DataFrame
    line_data = []
    for timestamp, row in df.iterrows():
        # The time setter accepts pandas Timestamp directly
        data_point = SingleValueData(time=timestamp, value=row['close'])
        line_data.append(data_point)
    
    # Create line series
    line_series = LineSeries(
        data=line_data,
        options=LineSeriesOptions(
            color='#2196F3',
            line_width=2
        )
    )
    
    # Create and render chart
    chart1 = Chart(series=line_series, options=ChartOptions(height=300))
    chart1.render(key='pandas_timestamp_chart')
    
    # Show that we can get time back as pandas Timestamp
    st.code(f"First data point time: {line_data[0].time}")
    st.code(f"Type: {type(line_data[0].time)}")
    
    # Example 2: Using datetime objects
    st.subheader("Example 2: Candlestick Chart with datetime objects")
    
    candlestick_data = []
    for i, (timestamp, row) in enumerate(df.iterrows()):
        # Convert pandas Timestamp to datetime
        dt = timestamp.to_pydatetime()
        
        # The time setter accepts datetime objects
        data_point = OhlcData(
            time=dt,
            open=row['open'],
            high=row['high'],
            low=row['low'],
            close=row['close']
        )
        candlestick_data.append(data_point)
    
    # Create candlestick series
    candlestick_series = CandlestickSeries(
        data=candlestick_data,
        options=CandlestickSeriesOptions(
            up_color='#26a69a',
            down_color='#ef5350'
        )
    )
    
    # Create and render chart
    chart2 = Chart(series=candlestick_series, options=ChartOptions(height=400))
    chart2.render(key='datetime_chart')
    
    # Example 3: Using Unix timestamps
    st.subheader("Example 3: Using Unix Timestamps")
    
    unix_data = []
    for timestamp, row in df.iterrows():
        # Convert to Unix timestamp
        unix_ts = int(timestamp.timestamp())
        
        # The time setter accepts Unix timestamps
        data_point = SingleValueData(time=unix_ts, value=row['volume'])
        unix_data.append(data_point)
    
    volume_series = LineSeries(
        data=unix_data,
        options=LineSeriesOptions(
            color='#4CAF50',
            line_width=2
        )
    )
    
    chart3 = Chart(series=volume_series, options=ChartOptions(height=200))
    chart3.render(key='unix_timestamp_chart')
    
    # Example 4: Using date strings
    st.subheader("Example 4: Using Date Strings")
    
    string_data = []
    for timestamp, row in df.iterrows():
        # Convert to date string
        date_str = timestamp.strftime('%Y-%m-%d')
        
        # The time setter accepts date strings
        data_point = SingleValueData(time=date_str, value=row['close'])
        string_data.append(data_point)
    
    # Add markers with different time formats
    markers = [
        Marker(
            time=df.index[5],  # Pandas Timestamp
            position=MarkerPosition.ABOVE_BAR,
            color='#FF5722',
            shape=MarkerShape.ARROW_DOWN,
            text='Pandas TS'
        ),
        Marker(
            time=datetime.now() - timedelta(days=20),  # datetime object
            position=MarkerPosition.BELOW_BAR,
            color='#2196F3',
            shape=MarkerShape.ARROW_UP,
            text='datetime'
        ),
        Marker(
            time='2024-01-15',  # Date string
            position=MarkerPosition.ABOVE_BAR,
            color='#4CAF50',
            shape=MarkerShape.CIRCLE,
            text='String'
        )
    ]
    
    string_series = LineSeries(
        data=string_data,
        options=LineSeriesOptions(
            color='#9C27B0',
            line_width=3
        ),
        markers=markers
    )
    
    chart4 = Chart(series=string_series, options=ChartOptions(height=350))
    chart4.render(key='date_string_chart')
    
    # Example 5: Converting back to pandas
    st.subheader("Example 5: Converting Data Back to Pandas")
    
    # Show how to extract data back as pandas DataFrame
    times = []
    values = []
    
    for data_point in line_data[:10]:  # First 10 points
        times.append(data_point.time)  # This returns pd.Timestamp
        values.append(data_point.value)
    
    # Create DataFrame from the data
    extracted_df = pd.DataFrame({
        'time': times,
        'value': values
    })
    extracted_df.set_index('time', inplace=True)
    
    st.write("Extracted DataFrame (first 10 rows):")
    st.dataframe(extracted_df)
    
    # Show the internal storage format
    st.subheader("Internal Storage Format")
    st.write("Data is internally stored in the format expected by Lightweight Charts:")
    st.code(f"Internal time format: {line_data[0]._time}")
    st.code(f"Dictionary representation: {line_data[0].to_dict()}")


if __name__ == "__main__":
    main()