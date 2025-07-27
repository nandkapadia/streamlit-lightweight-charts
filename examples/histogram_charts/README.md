# Histogram Charts Examples

This folder contains comprehensive examples demonstrating the usage of `HistogramSeries` in the streamlit-lightweight-charts-pro library.

## Overview

Histogram charts are perfect for visualizing volume data, frequency distributions, and other quantitative data that can be represented as bars. They display data as a series of vertical bars, with the height of each bar representing the value.

## Examples

### 1. Basic Histogram Chart (`basic_histogram_chart.py`)
- **Purpose**: Learn the fundamentals of creating histogram charts
- **Features**:
  - Basic volume data visualization
  - DataFrame integration
  - Series properties exploration
  - Volume analysis and statistics
- **Data Source**: Sample volume data from `data_samples.py`

### 2. Customized Histogram Chart (`customized_histogram_chart.py`)
- **Purpose**: Explore advanced styling and customization options
- **Features**:
  - Color customization
  - Base value settings
  - Volume trend analysis
  - Interactive settings via sidebar
- **Data Source**: Sample volume data from `data_samples.py`

## Key Features

### HistogramSeries Properties
- **Colors**: Customize bar colors
- **Base Value**: Set the base value for bars (default: 0)
- **Data Handling**: Support for both LineData objects and pandas DataFrames
- **Interactive**: Real-time customization through Streamlit widgets

### Data Requirements
Histogram charts require single-value data with the following structure:
```python
{
    "time": timestamp,
    "value": float
}
```

## Usage

### Running Examples
```bash
# Run basic example
streamlit run examples/histogram_charts/basic_histogram_chart.py

# Run customized example
streamlit run examples/histogram_charts/customized_histogram_chart.py

# Run launcher
streamlit run examples/histogram_charts/launcher.py
```

### Basic Implementation
```python
from streamlit_lightweight_charts_pro.charts import Chart
from streamlit_lightweight_charts_pro.charts.series.histogram import HistogramSeries
from examples.data_samples import get_volume_data

# Get sample data
histogram_data = get_volume_data()

# Create histogram series
histogram_series = HistogramSeries(data=histogram_data)

# Create and render chart
chart = Chart()
chart.add_series(histogram_series)
chart.render()
```

## Customization Options

### Colors
- `color`: Color for histogram bars
- `base`: Base value for bars (default: 0)

### Data Mapping
When using DataFrames, specify column mapping:
```python
histogram_series = HistogramSeries(
    data=df,
    column_mapping={
        "time": "datetime",
        "value": "value"
    }
)
```

## Data Analysis Features

Each example includes comprehensive data analysis:
- **Volume Statistics**: Minimum, maximum, average, and total volume
- **Volume Distribution**: Analysis of volume ranges and frequencies
- **Volume Trends**: Analysis of volume changes over time
- **Series Properties**: Chart type, visibility, scale settings
- **Raw Data Display**: Interactive DataFrame viewer

## Use Cases

### Volume Analysis
- **Trading Volume**: Visualize trading volume patterns
- **Frequency Distribution**: Show distribution of values
- **Time Series Data**: Display quantitative data over time

### Financial Applications
- **Volume Profile**: Analyze trading volume at different price levels
- **Volume Indicators**: Create volume-based technical indicators
- **Market Analysis**: Study volume patterns and trends

## Integration with Other Series

Histogram charts can be combined with other series types:
- **Price Charts**: Overlay volume on price charts
- **Line Series**: Add trend lines or moving averages
- **Area Series**: Create volume-weighted indicators

## Best Practices

1. **Data Quality**: Ensure volume data is properly validated
2. **Color Choice**: Use appropriate colors for your data context
3. **Base Value**: Set appropriate base values for your data range
4. **Scale**: Choose appropriate scales for volume visualization
5. **Interactivity**: Provide customization options for user experience

## Advanced Features

### Volume Analysis
- **Distribution Analysis**: Categorize volume into ranges
- **Trend Analysis**: Identify volume trends and patterns
- **Statistical Metrics**: Calculate variance, standard deviation

### Customization
- **Dynamic Colors**: Change colors based on data values
- **Base Value Adjustment**: Modify base values for different contexts
- **Interactive Controls**: Real-time parameter adjustment

## Related Documentation

- [HistogramSeries API Reference](../../streamlit_lightweight_charts_pro/charts/series/histogram.py)
- [LineData Model](../../streamlit_lightweight_charts_pro/data/line_data.py)
- [Chart Configuration](../../streamlit_lightweight_charts_pro/charts/chart.py)
- [Data Samples](../data_samples.py) 