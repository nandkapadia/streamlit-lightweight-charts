# Baseline Charts Examples

This folder contains comprehensive examples demonstrating the usage of `BaselineSeries` in the streamlit-lightweight-charts-pro library.

## Overview

Baseline charts are specialized area charts that display data relative to a baseline value, typically used for showing performance metrics, relative changes, or data that needs to be compared against a reference point. They provide clear visual distinction between values above and below the baseline.

## Examples

### 1. Basic Baseline Chart (`basic_baseline_chart.py`)
- **Purpose**: Learn the fundamentals of creating baseline charts
- **Features**:
  - Basic baseline data visualization
  - DataFrame integration
  - Series properties exploration
  - Baseline analysis and statistics
- **Data Source**: Sample baseline data from `data_samples.py`

### 2. Customized Baseline Chart (`customized_baseline_chart.py`)
- **Purpose**: Explore advanced styling and customization options
- **Features**:
  - Color customization (top/bottom area colors)
  - Baseline value settings
  - Relative gradient options
  - Interactive settings via sidebar
- **Data Source**: Sample baseline data from `data_samples.py`

## Key Features

### BaselineSeries Properties
- **Baseline Value**: Set the reference baseline value
- **Colors**: Customize top and bottom area colors separately
- **Relative Gradient**: Enable relative gradient coloring
- **Data Handling**: Support for both LineData objects and pandas DataFrames
- **Interactive**: Real-time customization through Streamlit widgets

### Data Requirements
Baseline charts require single-value data with the following structure:
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
streamlit run examples/baseline_charts/basic_baseline_chart.py

# Run customized example
streamlit run examples/baseline_charts/customized_baseline_chart.py

# Run launcher
streamlit run examples/baseline_charts/launcher.py
```

### Basic Implementation
```python
from streamlit_lightweight_charts_pro.charts import Chart
from streamlit_lightweight_charts_pro.charts.series.baseline import BaselineSeries
from examples.data_samples import get_baseline_data

# Get sample data
baseline_data = get_baseline_data()

# Create baseline series
baseline_series = BaselineSeries(data=baseline_data)

# Create and render chart
chart = Chart()
chart.add_series(baseline_series)
chart.render()
```

## Customization Options

### Baseline Configuration
- `base_value`: Set the baseline reference value (default: 0)
- `relative_gradient`: Enable relative gradient coloring

### Colors
- `top_fill_color1`: Primary fill color for values above baseline
- `top_fill_color2`: Secondary fill color for values above baseline
- `top_line_color`: Line color for values above baseline
- `bottom_fill_color1`: Primary fill color for values below baseline
- `bottom_fill_color2`: Secondary fill color for values below baseline
- `bottom_line_color`: Line color for values below baseline

### Data Mapping
When using DataFrames, specify column mapping:
```python
baseline_series = BaselineSeries(
    data=df,
    column_mapping={
        "time": "datetime",
        "value": "value"
    }
)
```

## Baseline Analysis

### Value Classification
- **Above Baseline**: Values greater than the baseline reference
- **Below Baseline**: Values less than the baseline reference
- **At Baseline**: Values equal to the baseline reference

### Distance Metrics
- **Average Distance**: Mean distance from baseline
- **Maximum Distance**: Greatest deviation from baseline
- **Distribution**: Percentage of values above/below baseline

## Data Analysis Features

Each example includes comprehensive data analysis:
- **Value Statistics**: Minimum, maximum, average values
- **Baseline Analysis**: Count of values above/below baseline
- **Distance Metrics**: Average and maximum distance from baseline
- **Series Properties**: Chart type, visibility, scale settings
- **Raw Data Display**: Interactive DataFrame viewer

## Use Cases

### Performance Metrics
- **Relative Performance**: Compare performance against benchmarks
- **Target Achievement**: Track progress toward goals
- **Deviation Analysis**: Identify outliers from expected values

### Financial Applications
- **Index Performance**: Compare against market indices
- **Risk Metrics**: Show risk-adjusted returns
- **Portfolio Analysis**: Compare portfolio performance to benchmarks

### Business Intelligence
- **KPI Tracking**: Monitor key performance indicators
- **Budget Analysis**: Compare actual vs. budgeted values
- **Quality Metrics**: Track quality scores against targets

## Integration with Other Series

Baseline charts can be combined with other series types:
- **Line Series**: Add trend lines or moving averages
- **Area Series**: Overlay additional performance metrics
- **Bar Series**: Show discrete performance periods

## Best Practices

1. **Baseline Selection**: Choose meaningful baseline values
2. **Color Choice**: Use contrasting colors for above/below baseline
3. **Context**: Provide clear context for baseline interpretation
4. **Scale**: Choose appropriate scales for your data range
5. **Interactivity**: Allow users to adjust baseline values

## Advanced Features

### Baseline Configuration
- **Dynamic Baselines**: Adjust baseline values interactively
- **Multiple Baselines**: Compare against multiple reference points
- **Relative Gradients**: Use gradient coloring for visual appeal

### Analysis Tools
- **Statistical Analysis**: Calculate deviation statistics
- **Trend Analysis**: Identify trends relative to baseline
- **Outlier Detection**: Identify significant deviations

## Related Documentation

- [BaselineSeries API Reference](../../streamlit_lightweight_charts_pro/charts/series/baseline.py)
- [LineData Model](../../streamlit_lightweight_charts_pro/data/line_data.py)
- [Chart Configuration](../../streamlit_lightweight_charts_pro/charts/chart.py)
- [Data Samples](../data_samples.py) 