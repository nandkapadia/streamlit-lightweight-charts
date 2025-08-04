# Line Chart Examples

This directory contains comprehensive examples demonstrating all features of the Line Chart component in the `streamlit-lightweight-charts-pro` library.

## 📁 Example Files

### 1. `line_chart_basic.py` - Basic Line Chart
**Purpose**: Demonstrates a simple line chart with default styling.

**Features**:
- Basic line chart creation
- Default styling and colors
- Time series data handling
- Data validation and normalization

**Key Code**:
```python
from streamlit_lightweight_charts_pro import Chart
from streamlit_lightweight_charts_pro.charts.series.line import LineSeries
from examples.data_samples import get_line_data

# Get sample data
line_data = get_line_data()

# Create line series
line_series = LineSeries(data=line_data)

# Create chart
chart = Chart(series=line_series)
chart.render(key="basic_line_chart")
```

### 2. `line_chart_with_price_lines.py` - Price Lines
**Purpose**: Shows how to add horizontal price lines to highlight key levels.

**Features**:
- Support and resistance levels
- Average price line
- Custom styling for price lines
- Method chaining for adding price lines

**Key Code**:
```python
from streamlit_lightweight_charts_pro.charts.options.price_line_options import PriceLineOptions
from streamlit_lightweight_charts_pro.type_definitions.enums import LineStyle

# Create price lines
support_line = PriceLineOptions(
    price=min_price,
    color="#26a69a",
    line_width=2,
    line_style=LineStyle.DASHED,
    title="Support Level"
)

# Add to series
line_series = (LineSeries(data=line_data)
               .add_price_line(support_line)
               .add_price_line(resistance_line))
```

### 3. `line_chart_with_markers.py` - Markers
**Purpose**: Demonstrates how to add markers to highlight specific data points.

**Features**:
- Different marker shapes (arrows, circles, squares)
- Different marker positions (above, below, in bar)
- Custom marker colors and text labels
- Event-based marker placement

**Key Code**:
```python
from streamlit_lightweight_charts_pro.data.marker import BarMarker
from streamlit_lightweight_charts_pro.type_definitions.enums import MarkerPosition, MarkerShape

# Create markers
support_marker = Marker(
    time=min_point.time,
    position=MarkerPosition.BELOW_BAR,
    color="#26a69a",
    shape=MarkerShape.ARROW_UP,
    text="Support Level",
    size=12
)

# Add to series
line_series = (LineSeries(data=line_data)
               .add_marker(support_marker)
               .add_marker(resistance_marker))
```

### 4. `line_chart_advanced.py` - Advanced Features
**Purpose**: Comprehensive example showing all features together.

**Features**:
- Custom line styling with LineOptions
- Price lines with labels
- Multiple marker types
- Method chaining
- Advanced options and customization

**Key Code**:
```python
# Custom line options
line_options = LineOptions(
    color="#2196F3",
    line_width=3,
    line_style=LineStyle.SOLID,
    crosshair_marker_visible=True,
    point_markers_visible=True
)

# Advanced series with all features
line_series = (LineSeries(data=line_data, line_options=line_options)
               .add_price_line(support_line)
               .add_price_line(resistance_line)
               .add_marker(support_marker)
               .add_marker(resistance_marker))
```

### 5. `line_chart_dataframe.py` - DataFrame Input
**Purpose**: Shows how to create line charts from pandas DataFrames.

**Features**:
- DataFrame to LineSeries conversion
- Column mapping
- Color mapping from DataFrame columns
- Data validation and error handling

**Key Code**:
```python
# Define column mapping
column_mapping = {
    "time": "datetime",
    "value": "value",
    "color": "color"  # Optional
}

# Create from DataFrame
line_series = LineSeries.from_dataframe(
    df=df,
    column_mapping=column_mapping
)
```

## 🎯 Key Features Demonstrated

### Core Features
- ✅ **Basic Line Chart**: Simple time series visualization
- ✅ **Custom Styling**: Colors, line width, line styles
- ✅ **Price Lines**: Horizontal lines for key levels
- ✅ **Markers**: Point markers for events and signals
- ✅ **Method Chaining**: Fluent API for building charts

### Advanced Features
- ✅ **DataFrame Integration**: Direct pandas DataFrame support
- ✅ **Column Mapping**: Flexible data column mapping
- ✅ **Color Mapping**: Dynamic colors based on data
- ✅ **Crosshair Markers**: Interactive crosshair display
- ✅ **Point Markers**: Visible data point indicators

### Data Handling
- ✅ **Time Normalization**: Automatic time format conversion
- ✅ **NaN Handling**: Proper handling of missing data
- ✅ **Data Validation**: Required column and type checking
- ✅ **Error Handling**: Clear error messages

## 🚀 Running the Examples

### Prerequisites
```bash
pip install streamlit-lightweight-charts-pro pandas streamlit
```

### Running Individual Examples
```bash
# Basic line chart
streamlit run examples/line_chart_basic.py

# Line chart with price lines
streamlit run examples/line_chart_with_price_lines.py

# Line chart with markers
streamlit run examples/line_chart_with_markers.py

# Advanced line chart
streamlit run examples/line_chart_advanced.py

# DataFrame line chart
streamlit run examples/line_chart_dataframe.py
```

### Running All Examples
```bash
# Create a simple launcher
streamlit run examples/line_chart_launcher.py
```

## 📊 Data Sources

All examples use sample data from `examples/data_samples.py`:

- **`get_line_data()`**: Returns `List[LineData]` for basic charts
- **`get_dataframe_line_data()`**: Returns `pd.DataFrame` for DataFrame examples

## 🎨 Customization Options

### Line Options (`LineOptions`)
```python
LineOptions(
    color="#2196F3",                    # Line color
    line_width=3,                       # Line thickness
    line_style=LineStyle.SOLID,         # Line style (SOLID, DASHED, DOTTED)
    crosshair_marker_visible=True,      # Show crosshair marker
    point_markers_visible=True,         # Show point markers
    crosshair_marker_radius=6,          # Crosshair marker size
    point_markers_radius=4              # Point marker size
)
```

### Price Line Options (`PriceLineOptions`)
```python
PriceLineOptions(
    price=100.0,                        # Price level
    color="#26a69a",                    # Line color
    line_width=2,                       # Line thickness
    line_style=LineStyle.DASHED,        # Line style
    title="Support Level",              # Label text
    axis_label_color="#26a69a",         # Label color
    axis_label_text_color="#ffffff"     # Label text color
)
```

### Marker Options (`Marker`)
```python
Marker(
    time="2024-01-01",                  # Time position
    position=MarkerPosition.BELOW_BAR,  # Position relative to data
    color="#26a69a",                    # Marker color
    shape=MarkerShape.ARROW_UP,         # Marker shape
    text="Support Level",               # Label text
    size=12                             # Marker size
)
```

## 🔗 Related Documentation

- [TradingView Lightweight Charts API](https://tradingview.github.io/lightweight-charts/docs/api)
- [Line Series Documentation](https://tradingview.github.io/lightweight-charts/docs/api/interfaces/LineStyleOptions)
- [Price Line Documentation](https://tradingview.github.io/lightweight-charts/tutorials/how_to/price-line)
- [Series Markers Documentation](https://tradingview.github.io/lightweight-charts/tutorials/how_to/series-markers)

## 🤝 Contributing

To add new line chart examples:

1. Create a new Python file in the `examples/` directory
2. Follow the naming convention: `line_chart_<feature>.py`
3. Include comprehensive documentation and comments
4. Add the example to this README
5. Test the example thoroughly

## 📝 Notes

- All examples use the same sample data for consistency
- Examples demonstrate both basic and advanced usage patterns
- Method chaining is used throughout for cleaner code
- Error handling and validation are demonstrated
- Performance considerations are addressed in DataFrame examples 