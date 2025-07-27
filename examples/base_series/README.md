# Base Series Examples

This directory contains examples demonstrating the fundamental Series functionality that all series types share in the `streamlit-lightweight-charts-pro` library.

## Overview

The `Series` class is the abstract base class for all series types. While you cannot create direct instances of `Series` (it's abstract), these examples demonstrate the common functionality that all concrete series implementations inherit.

## Examples

### 1. Basic Series Usage (`basic_series_usage.py`)
Demonstrates fundamental Series functionality:
- Series creation and configuration
- Visibility control
- Price scale configuration
- Property access and modification
- Method chaining
- Data access methods

### 2. Markers and Price Lines (`markers_and_price_lines.py`)
Shows how to add visual enhancements to any series:
- Adding markers with different positions and shapes
- Creating price lines for support/resistance levels
- Marker and price line management
- Combining markers and price lines

### 3. Data Handling (`data_handling.py`)
Demonstrates data input capabilities:
- Working with Data objects
- DataFrame input with column mapping
- Series input with column mapping
- Data validation and error handling
- Data access patterns
- Data processing examples

### 4. Advanced Features (`advanced_features.py`)
Shows advanced Series functionality:
- Method chaining for fluent API
- Price format configuration
- Series configuration management
- Serialization to dictionary/JSON
- Series validation
- Factory methods
- Data access patterns

## Running the Examples

### Using the Launcher
```bash
streamlit run examples/base_series/launcher.py
```

### Running Individual Examples
```bash
# Basic usage
streamlit run examples/base_series/basic_series_usage.py

# Markers and price lines
streamlit run examples/base_series/markers_and_price_lines.py

# Data handling
streamlit run examples/base_series/data_handling.py

# Advanced features
streamlit run examples/base_series/advanced_features.py
```

## Key Concepts

### Series Properties
All series share these common properties:
- `visible`: Whether the series is displayed
- `price_scale_id`: Which price scale to use ("left" or "right")
- `pane_id`: Which pane the series belongs to
- `overlay`: Whether the series overlays others
- `data`: The series data points
- `markers`: List of markers on the series
- `price_lines`: List of price lines on the series

### Method Chaining
Series support method chaining for fluent configuration:
```python
series = (
    LineSeries(data=data)
    .set_visible(True)
    .add_marker(time, position, color, shape, text)
    .add_price_line(price_line_options)
)
```

### Data Input Formats
Series accept multiple data formats:
```python
# Data objects
series = LineSeries(data=line_data_objects)

# DataFrame with column mapping
series = LineSeries(
    data=df,
    column_mapping={'time': 'datetime', 'value': 'close'}
)

# Series with column mapping
series = LineSeries(
    data=series_data,
    column_mapping={'time': 'index', 'value': 0}
)
```

### Markers
Add visual markers to highlight specific points:
```python
series.add_marker(
    time="2024-01-01",
    position=MarkerPosition.ABOVE_BAR,
    color="#FF0000",
    shape=MarkerShape.CIRCLE,
    text="Peak",
    size=12
)
```

### Price Lines
Add horizontal lines for support/resistance levels:
```python
price_line = PriceLineOptions(
    price=30.0,
    color="#FF0000",
    line_width=2,
    line_style="dashed",
    title="Resistance"
)
series.add_price_line(price_line)
```

## Data Sources

All examples use data from `examples/data_samples.py`, which provides:
- `get_line_data()`: LineData objects for line charts
- `get_dataframe_line_data()`: DataFrame format for line data
- `get_dataframe_candlestick_data()`: DataFrame format for OHLC data

## Notes

- These examples use `LineSeries` as a concrete implementation since `Series` is abstract
- All functionality demonstrated applies to other series types (AreaSeries, BarSeries, etc.)
- The examples focus on common Series functionality rather than series-specific features
- Error handling and validation are demonstrated throughout the examples

## Related Documentation

- [Series Base Class](../streamlit_lightweight_charts_pro/charts/series/base.py)
- [Data Models](../streamlit_lightweight_charts_pro/data/)
- [Options Classes](../streamlit_lightweight_charts_pro/charts/options/)
- [Type Definitions](../streamlit_lightweight_charts_pro/type_definitions/) 