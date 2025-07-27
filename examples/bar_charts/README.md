# Bar Charts Examples

This folder contains comprehensive examples demonstrating the usage of `BarSeries` in the streamlit-lightweight-charts-pro library.

## Overview

Bar charts are essential for financial data visualization, displaying OHLC (Open, High, Low, Close) data in a clear, easy-to-understand format. Each bar represents a time period with the open, high, low, and close prices.

## Examples

### 1. Basic Bar Chart (`basic_bar_chart.py`)
- **Purpose**: Learn the fundamentals of creating bar charts
- **Features**:
  - Basic OHLC data visualization
  - DataFrame integration
  - Series properties exploration
  - Data statistics and analysis
- **Data Source**: Sample OHLC data from `data_samples.py`

### 2. Customized Bar Chart (`customized_bar_chart.py`)
- **Purpose**: Explore advanced styling and customization options
- **Features**:
  - Color customization (up/down/base colors)
  - Visibility controls (open visibility, thin bars)
  - Price movement analysis
  - Interactive settings via sidebar
- **Data Source**: Sample OHLC data from `data_samples.py`

## Key Features

### BarSeries Properties
- **Colors**: Customize up, down, and base colors
- **Visibility**: Control open price visibility and bar thickness
- **Data Handling**: Support for both OhlcData objects and pandas DataFrames
- **Interactive**: Real-time customization through Streamlit widgets

### Data Requirements
Bar charts require OHLC data with the following structure:
```python
{
    "time": timestamp,
    "open": float,
    "high": float, 
    "low": float,
    "close": float
}
```

## Usage

### Running Examples
```bash
# Run basic example
streamlit run examples/bar_charts/basic_bar_chart.py

# Run customized example
streamlit run examples/bar_charts/customized_bar_chart.py

# Run launcher
streamlit run examples/bar_charts/launcher.py
```

### Basic Implementation
```python
from streamlit_lightweight_charts_pro.charts import Chart
from streamlit_lightweight_charts_pro.charts.series.bar_series import BarSeries
from examples.data_samples import get_bar_data

# Get sample data
bar_data = get_bar_data()

# Create bar series
bar_series = BarSeries(data=bar_data)

# Create and render chart
chart = Chart()
chart.add_series(bar_series)
chart.render()
```

## Customization Options

### Colors
- `up_color`: Color for bars where close > open
- `down_color`: Color for bars where close < open  
- `color`: Base color for all bars

### Visibility
- `open_visible`: Show/hide open price on bars
- `thin_bars`: Use thin bar style

### Data Mapping
When using DataFrames, specify column mapping:
```python
bar_series = BarSeries(
    data=df,
    column_mapping={
        "time": "datetime",
        "open": "open", 
        "high": "high",
        "low": "low",
        "close": "close"
    }
)
```

## Data Analysis Features

Each example includes comprehensive data analysis:
- **Price Statistics**: Average open, high, low, close values
- **Movement Analysis**: Count of up/down/flat price movements
- **Series Properties**: Chart type, visibility, scale settings
- **Raw Data Display**: Interactive DataFrame viewer

## Integration with Other Series

Bar charts can be combined with other series types:
- **Line Series**: Add trend lines or moving averages
- **Area Series**: Overlay volume or indicator data
- **Candlestick Series**: Compare with candlestick representation

## Best Practices

1. **Data Quality**: Ensure OHLC data is properly validated
2. **Color Choice**: Use contrasting colors for up/down movements
3. **Time Scale**: Choose appropriate time intervals for your data
4. **Interactivity**: Provide customization options for user experience
5. **Performance**: Use efficient data structures for large datasets

## Related Documentation

- [BarSeries API Reference](../../streamlit_lightweight_charts_pro/charts/series/bar_series.py)
- [OhlcData Model](../../streamlit_lightweight_charts_pro/data/ohlc_data.py)
- [Chart Configuration](../../streamlit_lightweight_charts_pro/charts/chart.py)
- [Data Samples](../data_samples.py) 