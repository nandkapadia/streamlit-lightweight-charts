# Time Handling Guide for Streamlit Lightweight Charts

## Overview

The refactored OOP version of streamlit-lightweight-charts now includes sophisticated time handling that seamlessly works with pandas, datetime, and other time formats.

## Key Features

### 1. Flexible Time Input

All data models now accept time in multiple formats:
- **pandas.Timestamp** - Direct from DataFrame indexes
- **datetime.datetime** - Python datetime objects
- **Unix timestamps** - Integer or float seconds since epoch
- **Date strings** - ISO format strings like '2024-01-01'

### 2. Automatic Conversion

The time property automatically converts between formats:
```python
from datetime import datetime
import pandas as pd
from streamlit_lightweight_charts import SingleValueData

# All these create the same data point
data1 = SingleValueData(time='2024-01-01', value=100)
data2 = SingleValueData(time=datetime(2024, 1, 1), value=100)
data3 = SingleValueData(time=pd.Timestamp('2024-01-01'), value=100)
data4 = SingleValueData(time=1704067200, value=100)  # Unix timestamp
```

### 3. Pandas Integration

Get time back as pandas Timestamp:
```python
data_point = SingleValueData(time='2024-01-01', value=100)
timestamp = data_point.time  # Returns pd.Timestamp
print(timestamp.day_name())  # 'Monday'
print(timestamp.month_name())  # 'January'
```

## DataFrame Utilities

Convert DataFrames to chart data easily:

```python
import pandas as pd
from streamlit_lightweight_charts.utils import df_to_line_data, df_to_ohlc_data

# Create DataFrame with datetime index
df = pd.DataFrame({
    'close': [100, 102, 98, 105],
    'volume': [1000, 1500, 800, 2000]
}, index=pd.date_range('2024-01-01', periods=4))

# Convert to chart data
line_data = df_to_line_data(df, value_column='close')
```

## Usage Examples

### Example 1: From DataFrame to Chart

```python
import pandas as pd
from streamlit_lightweight_charts import Chart, LineSeries
from streamlit_lightweight_charts.utils import df_to_line_data

# Your DataFrame with datetime index
df = pd.read_csv('stock_data.csv', index_col='date', parse_dates=True)

# Convert to chart data
data = df_to_line_data(df, value_column='close')

# Create and render chart
series = LineSeries(data=data)
chart = Chart(series=series)
chart.render()
```

### Example 2: Manual Data Creation

```python
from datetime import datetime, timedelta
from streamlit_lightweight_charts import SingleValueData, LineSeries

# Create data points with different time formats
data = []
base_date = datetime.now()

for i in range(10):
    # Using datetime objects
    data.append(SingleValueData(
        time=base_date - timedelta(days=i),
        value=100 + i * 2
    ))

series = LineSeries(data=data)
```

### Example 3: Working with Markers

```python
from streamlit_lightweight_charts import Marker, MarkerShape, MarkerPosition

# Markers also accept any time format
marker = Marker(
    time=pd.Timestamp('2024-01-15'),
    position=MarkerPosition.ABOVE_BAR,
    color='#FF0000',
    shape=MarkerShape.ARROW_DOWN,
    text='Important Event'
)

# Get time back as pandas Timestamp
event_time = marker.time
print(f"Event on: {event_time.strftime('%B %d, %Y')}")
```

## Internal Storage

- Time is internally stored as UTC timestamp (for numeric times) or date string (for date strings)
- This ensures compatibility with TradingView Lightweight Charts
- The conversion is transparent to the user

## Benefits

1. **No Manual Conversion**: Work with your preferred time format
2. **DataFrame Friendly**: Direct integration with pandas DataFrames
3. **Type Safety**: Clear property types with proper documentation
4. **Backward Compatible**: Still accepts the formats used by Lightweight Charts

## Migration from Dict-based API

Old approach:
```python
data = [
    {"time": '2024-01-01', "value": 100},
    {"time": '2024-01-02', "value": 102}
]
```

New OOP approach:
```python
data = [
    SingleValueData(time='2024-01-01', value=100),
    SingleValueData(time='2024-01-02', value=102)
]
```

Or directly from DataFrame:
```python
data = df_to_line_data(df, value_column='close')
```