# Examples

This directory contains example applications demonstrating various chart types and features of the `streamlit-lightweight-charts-pro` library.

## Running Examples

### Simple Approach (Recommended)

Since the `examples` directory has an `__init__.py` file, you can run examples directly using PYTHONPATH:

```bash
PYTHONPATH=. streamlit run examples/line_charts/line_chart_basic.py
PYTHONPATH=. streamlit run examples/area_charts/basic_area_chart.py
PYTHONPATH=. streamlit run examples/candlestick_charts/basic_candlestick_chart.py
```

### Alternative Approaches

1. **From examples directory:**
   ```bash
   cd examples
   streamlit run line_charts/line_chart_basic.py
   ```

2. **Install examples as development package:**
   ```bash
   pip install -e examples/
   streamlit run examples/line_charts/line_chart_basic.py
   ```

## Available Examples

### Line Charts
- `line_charts/line_chart_basic.py` - Basic line chart
- `line_charts/line_chart_advanced.py` - Advanced line chart features
- `line_charts/line_chart_with_markers.py` - Line chart with markers
- `line_charts/line_chart_with_price_lines.py` - Line chart with price lines
- `line_charts/line_chart_dataframe.py` - Line chart from DataFrame
- `line_charts/line_chart_launcher.py` - Launcher for all line chart examples

### Area Charts
- `area_charts/basic_area_chart.py` - Basic area chart
- `area_charts/customized_area_chart.py` - Customized area chart
- `area_charts/interactive_area_chart.py` - Interactive area chart
- `area_charts/multi_area_chart.py` - Multiple area charts

### Candlestick Charts
- `candlestick_charts/basic_candlestick_chart.py` - Basic candlestick chart
- `candlestick_charts/customized_candlestick_chart.py` - Customized candlestick chart

### Bar Charts
- `bar_charts/basic_bar_chart.py` - Basic bar chart
- `bar_charts/customized_bar_chart.py` - Customized bar chart

### Baseline Charts
- `baseline_charts/basic_baseline_chart.py` - Basic baseline chart
- `baseline_charts/customized_baseline_chart.py` - Customized baseline chart

### Histogram Charts
- `histogram_charts/basic_histogram_chart.py` - Basic histogram chart
- `histogram_charts/customized_histogram_chart.py` - Customized histogram chart

### Base Series Examples
- `base_series/basic_series_usage.py` - Basic series usage
- `base_series/advanced_features.py` - Advanced series features
- `base_series/data_handling.py` - Data handling examples
- `base_series/markers_and_price_lines.py` - Markers and price lines

## Data Samples

The `data_samples.py` module provides sample datasets for all chart types:

- `get_line_data()` - Sample line chart data
- `get_bar_data()` - Sample bar chart data
- `get_candlestick_data()` - Sample candlestick data
- `get_volume_data()` - Sample volume data
- `get_baseline_data()` - Sample baseline data
- `get_multi_area_data_1()` - Sample multi-area data 1
- `get_multi_area_data_2()` - Sample multi-area data 2
- `get_dataframe_line_data()` - Sample DataFrame for line charts
- `get_dataframe_candlestick_data()` - Sample DataFrame for candlestick charts

## Features Demonstrated

- Basic chart creation and rendering
- Custom styling and colors
- Interactive features
- Data handling and validation
- Multiple chart types
- Price lines and markers
- Trade visualization
- Annotations and overlays 