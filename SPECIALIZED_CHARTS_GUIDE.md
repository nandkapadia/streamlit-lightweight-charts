# Specialized Charts Guide

## Overview

The refactored OOP version of streamlit-lightweight-charts includes specialized chart classes that provide type safety, data validation, and a cleaner API for each chart type.

## Chart Types

### 1. CandlestickChart
For financial OHLC (Open, High, Low, Close) data.

```python
from streamlit_lightweight_charts import CandlestickChart, OhlcData

# Create OHLC data
data = [
    OhlcData(time='2024-01-01', open=100, high=105, low=98, close=102),
    OhlcData(time='2024-01-02', open=102, high=108, low=101, close=106),
    # ... more data
]

# Create chart with validation
chart = CandlestickChart(
    data=data,  # Must be List[OhlcData]
    series_options=CandlestickSeriesOptions(
        up_color='#26a69a',
        down_color='#ef5350'
    )
)
chart.render()
```

### 2. LineChart
For simple time-value data with support for multiple lines.

```python
from streamlit_lightweight_charts import LineChart, SingleValueData

# Create line data
data = [
    SingleValueData(time='2024-01-01', value=100),
    SingleValueData(time='2024-01-02', value=102),
    # ... more data
]

# Create chart
chart = LineChart(data=data)

# Add another line
ma_data = [
    SingleValueData(time='2024-01-01', value=99),
    SingleValueData(time='2024-01-02', value=101),
]
chart.add_line(data=ma_data, options=LineSeriesOptions(color='#FF9800'))

chart.render()
```

### 3. AreaChart
Similar to LineChart but with filled area.

```python
from streamlit_lightweight_charts import AreaChart

chart = AreaChart(
    data=data,
    series_options=AreaSeriesOptions(
        top_color='rgba(33, 150, 243, 0.56)',
        bottom_color='rgba(33, 150, 243, 0.04)',
        line_color='#2196F3'
    )
)
```

### 4. BarChart
For OHLC data displayed as bars.

```python
from streamlit_lightweight_charts import BarChart

chart = BarChart(
    data=ohlc_data,  # Same as CandlestickChart
    series_options=BarSeriesOptions(
        up_color='#26a69a',
        down_color='#ef5350',
        thin_bars=True
    )
)
```

### 5. HistogramChart
For volume or other histogram data.

```python
from streamlit_lightweight_charts import HistogramChart, HistogramData

data = [
    HistogramData(time='2024-01-01', value=10000, color='#26a69a'),
    HistogramData(time='2024-01-02', value=15000, color='#ef5350'),
]

chart = HistogramChart(data=data)
```

### 6. BaselineChart
For data with a baseline reference.

```python
from streamlit_lightweight_charts import BaselineChart, BaselineData

data = [
    BaselineData(time='2024-01-01', value=100),
    BaselineData(time='2024-01-02', value=95),
]

chart = BaselineChart(
    data=data,
    base_value=100  # Reference baseline
)
```

## Data Validation

Each specialized chart validates its data:

```python
# ✅ Correct - CandlestickChart with OhlcData
candlestick = CandlestickChart(data=[
    OhlcData(time='2024-01-01', open=100, high=105, low=98, close=102)
])

# ❌ Wrong - CandlestickChart with SingleValueData
try:
    candlestick = CandlestickChart(data=[
        SingleValueData(time='2024-01-01', value=100)  # Wrong type!
    ])
except TypeError as e:
    print(e)  # "All data items must be OhlcData instances"
```

## Creating from DataFrames

Use utility functions to create charts directly from pandas DataFrames:

```python
import pandas as pd
from streamlit_lightweight_charts import candlestick_chart_from_df

# Your DataFrame with OHLC columns
df = pd.DataFrame({
    'open': [100, 102, 101],
    'high': [105, 108, 103],
    'low': [98, 101, 99],
    'close': [102, 106, 101]
}, index=pd.date_range('2024-01-01', periods=3))

# Create chart directly
chart = candlestick_chart_from_df(
    df,
    series_options=CandlestickSeriesOptions(
        up_color='#4CAF50',
        down_color='#F44336'
    )
)
chart.render()
```

Available DataFrame builders:
- `candlestick_chart_from_df()`
- `line_chart_from_df()`
- `area_chart_from_df()`
- `bar_chart_from_df()`
- `histogram_chart_from_df()`
- `baseline_chart_from_df()`

## Benefits

### 1. Type Safety
```python
# IDE knows exactly what options are available
chart = CandlestickChart(
    data=data,
    series_options=CandlestickSeriesOptions(
        # IDE auto-completes these options
        up_color='#26a69a',
        down_color='#ef5350',
        wick_visible=True,
        border_visible=False
    )
)
```

### 2. Clear API
```python
# Chart type is explicit
candlestick = CandlestickChart(data=ohlc_data)
line = LineChart(data=line_data)
histogram = HistogramChart(data=volume_data)
```

### 3. Data Validation
```python
# Catches errors at construction time
chart = CandlestickChart(data=wrong_data_type)  # TypeError immediately
```

### 4. Specialized Methods
```python
# LineChart has add_line() method
line_chart = LineChart(data=price_data)
line_chart.add_line(data=ma_data)  # Add moving average

# CandlestickChart has update_data() with validation
candlestick.update_data(new_ohlc_data)
```

## Migration from Generic Chart

Old approach:
```python
# Generic Chart with manual series creation
from streamlit_lightweight_charts import Chart, CandlestickSeries

series = CandlestickSeries(data=ohlc_data)
chart = Chart(series=series)
```

New approach:
```python
# Specialized CandlestickChart
from streamlit_lightweight_charts import CandlestickChart

chart = CandlestickChart(data=ohlc_data)
```

## Complete Example

```python
import streamlit as st
import pandas as pd
from streamlit_lightweight_charts import (
    CandlestickChart, 
    candlestick_chart_from_df,
    ChartOptions, LayoutOptions, Background
)

# Load your data
df = pd.read_csv('stock_data.csv', index_col='date', parse_dates=True)

# Create chart options
options = ChartOptions(
    height=400,
    layout=LayoutOptions(
        background=Background.solid('#1e1e1e'),
        text_color='#d1d4dc'
    )
)

# Create chart from DataFrame
chart = candlestick_chart_from_df(
    df,
    chart_options=options,
    series_options=CandlestickSeriesOptions(
        up_color='#26a69a',
        down_color='#ef5350'
    )
)

# Render in Streamlit
chart.render(key='my_candlestick_chart')
```