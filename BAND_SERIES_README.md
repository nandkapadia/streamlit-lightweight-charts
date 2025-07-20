# BandSeries - Custom Band Charts for TradingView Lightweight Charts

## Overview

The **BandSeries** is a custom chart series type for TradingView's Lightweight Charts that visualizes three data lines simultaneously with configurable fill areas. It's perfect for technical analysis indicators like Bollinger Bands, Keltner Channels, and other envelope indicators.

## Features

- **Three-Line Visualization**: Upper, middle, and lower bands with independent styling
- **Configurable Fill Areas**: Customizable colors and opacity for areas between bands
- **Flexible Data Input**: Support for pandas DataFrames and custom data objects
- **Rich Styling Options**: Line colors, widths, styles, and visibility controls
- **Marker Support**: Add markers for signal points and annotations
- **Overlay Capability**: Can be used as an overlay on other chart types
- **Dynamic Updates**: Support for real-time data updates
- **Responsive Design**: Automatically resizes with the chart

## Installation

The BandSeries is part of the `streamlit-lightweight-charts-pro` package. No additional installation is required.

## Quick Start

### Basic Usage

```python
import pandas as pd
from streamlit_lightweight_charts_pro.charts.series.band import BandSeries
from streamlit_lightweight_charts_pro.data import BandData

# Create band data
data = [
    BandData("2024-01-01", 105.0, 100.0, 95.0),
    BandData("2024-01-02", 107.0, 102.0, 97.0),
    BandData("2024-01-03", 103.0, 98.0, 93.0),
]

# Create band series
band_series = BandSeries(data=data)

# Use in a chart
from streamlit_lightweight_charts_pro.charts.single_pane_chart import SinglePaneChart
chart = SinglePaneChart(series=[band_series])
```

### Using with Pandas DataFrame

```python
import pandas as pd

# Create DataFrame with band data
df = pd.DataFrame({
    "datetime": ["2024-01-01", "2024-01-02", "2024-01-03"],
    "upper": [105.0, 107.0, 103.0],
    "middle": [100.0, 102.0, 98.0],
    "lower": [95.0, 97.0, 93.0],
})

# Create band series from DataFrame
band_series = BandSeries(data=df)
```

## Data Structure

### BandData Object

```python
from streamlit_lightweight_charts_pro.data import BandData

# Create a single band data point
band_point = BandData(
    time="2024-01-01",    # Time in various formats
    upper=105.0,          # Upper band value
    middle=100.0,         # Middle band value
    lower=95.0            # Lower band value
)
```

### DataFrame Format

The DataFrame should contain these columns:
- `datetime` (or custom time column): Time values
- `upper`: Upper band values
- `middle`: Middle band values  
- `lower`: Lower band values

### Custom Column Mapping

```python
# DataFrame with custom column names
df = pd.DataFrame({
    "date": ["2024-01-01", "2024-01-02"],
    "u": [105.0, 107.0],
    "m": [100.0, 102.0],
    "l": [95.0, 97.0],
})

# Map custom columns
column_mapping = {
    "time": "date",
    "upper": "u",
    "middle": "m",
    "lower": "l",
}

band_series = BandSeries(data=df, column_mapping=column_mapping)
```

## Styling Options

### Line Colors and Widths

```python
band_series = BandSeries(
    data=data,
    # Upper band styling
    upper_line_color="#4CAF50",
    upper_line_width=2,
    upper_line_style=LineStyle.SOLID,
    
    # Middle band styling
    middle_line_color="#2196F3",
    middle_line_width=2,
    middle_line_style=LineStyle.SOLID,
    
    # Lower band styling
    lower_line_color="#F44336",
    lower_line_width=2,
    lower_line_style=LineStyle.SOLID,
)
```

### Fill Colors

```python
band_series = BandSeries(
    data=data,
    upper_fill_color="rgba(76, 175, 80, 0.1)",  # Light green
    lower_fill_color="rgba(244, 67, 54, 0.1)",  # Light red
)
```

### Line Visibility

```python
band_series = BandSeries(
    data=data,
    upper_line_visible=True,
    middle_line_visible=True,
    lower_line_visible=False,  # Hide lower line
)
```

### Line Types

```python
from streamlit_lightweight_charts_pro.type_definitions import LineType

band_series = BandSeries(
    data=data,
    line_type=LineType.CURVED,  # or LineType.SIMPLE
)
```

## Advanced Features

### Adding Markers

```python
from streamlit_lightweight_charts_pro.data import Marker, MarkerPosition, MarkerShape

band_series = BandSeries(data=data)

# Add a marker
band_series.add_marker(
    time="2024-01-02",
    position=MarkerPosition.ABOVE_BAR,
    color="#FF0000",
    shape=MarkerShape.CIRCLE,
    text="Signal Point",
    size=12,
)
```

### Method Chaining

```python
band_series = (
    BandSeries(data=data)
    .set_price_scale("left")
    .set_price_line(visible=True, color="#FF0000")
    .set_base_line(visible=True, color="#00FF00")
    .set_price_format(format_type="price", precision=4)
)
```

### Price Scale Configuration

```python
band_series = BandSeries(
    data=data,
    price_scale_id="left",
    price_scale_config={
        "visible": True,
        "ticksVisible": True,
        "borderVisible": True,
        "textColor": "#131722",
        "fontSize": 12,
    },
)
```

## Use Cases

### Bollinger Bands

```python
import pandas as pd
import numpy as np

def calculate_bollinger_bands(df, period=20, std_dev=2):
    """Calculate Bollinger Bands from OHLC data."""
    close_prices = df["close"]
    sma = close_prices.rolling(window=period, min_periods=1).mean()
    std = close_prices.rolling(window=period, min_periods=1).std()
    
    return pd.DataFrame({
        "datetime": df["datetime"],
        "upper": sma + (std_dev * std),
        "middle": sma,
        "lower": sma - (std_dev * std),
    })

# Calculate Bollinger Bands
bollinger_df = calculate_bollinger_bands(ohlc_df)

# Create band series
bollinger_series = BandSeries(
    data=bollinger_df,
    upper_line_color="#4CAF50",
    middle_line_color="#2196F3",
    lower_line_color="#F44336",
    upper_fill_color="rgba(76, 175, 80, 0.1)",
    lower_fill_color="rgba(244, 67, 54, 0.1)",
)
```

### Keltner Channels

```python
def calculate_keltner_channels(df, period=20, multiplier=2):
    """Calculate Keltner Channels from OHLC data."""
    typical_price = (df["high"] + df["low"] + df["close"]) / 3
    ema = typical_price.ewm(span=period).mean()
    
    high_low = df["high"] - df["low"]
    high_close = np.abs(df["high"] - df["close"].shift())
    low_close = np.abs(df["low"] - df["close"].shift())
    
    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = true_range.rolling(window=period, min_periods=1).mean()
    
    return pd.DataFrame({
        "datetime": df["datetime"],
        "upper": ema + (multiplier * atr),
        "middle": ema,
        "lower": ema - (multiplier * atr),
    })

# Calculate Keltner Channels
keltner_df = calculate_keltner_channels(ohlc_df)

# Create band series
keltner_series = BandSeries(
    data=keltner_df,
    upper_line_color="#9C27B0",
    middle_line_color="#FF9800",
    lower_line_color="#607D8B",
    upper_line_style=LineStyle.DASHED,
    lower_line_style=LineStyle.DASHED,
    line_type=LineType.CURVED,
)
```

### Overlay on Candlestick Chart

```python
from streamlit_lightweight_charts_pro.charts.series.candlestick import CandlestickSeries

# Create candlestick series
candlestick_series = CandlestickSeries(data=ohlc_df)

# Create band series as overlay
band_series = BandSeries(
    data=bollinger_df,
    price_scale_id="right",  # Same price scale as candlestick
    upper_line_width=1,
    middle_line_width=1,
    lower_line_width=1,
    upper_fill_color="rgba(76, 175, 80, 0.05)",  # Very light fill
    lower_fill_color="rgba(244, 67, 54, 0.05)",
)

# Create chart with both series
chart = SinglePaneChart(series=[candlestick_series, band_series])
```

## Frontend Integration

The BandSeries integrates seamlessly with the frontend React component through a custom TypeScript plugin that handles:

- Three separate line series (upper, middle, lower)
- Fill areas between bands
- Dynamic updates and resizing
- Crosshair markers and interactions
- Custom styling and animations

## Testing

Comprehensive test suites are included:

- **Unit Tests**: `tests/unit/charts/series/test_band_series.py` (21 tests)
- **Integration Tests**: `tests/integration/test_band_series_integration.py` (12 tests)

Run tests with:
```bash
python -m pytest tests/unit/charts/series/test_band_series.py -v
python -m pytest tests/integration/test_band_series_integration.py -v
```

## Example Application

See `examples/band_series_example.py` for a complete Streamlit application demonstrating:

- Bollinger Bands calculation and visualization
- Keltner Channels with custom styling
- Custom band indicators
- Overlay examples with candlestick charts
- Interactive configuration options

## API Reference

### BandSeries Constructor

```python
BandSeries(
    data: Union[Sequence[BandData], pd.DataFrame],
    visible: bool = True,
    price_scale_id: str = "right",
    column_mapping: Optional[Dict[str, str]] = None,
    
    # Upper band styling
    upper_line_color: str = "#4CAF50",
    upper_line_style: LineStyle = LineStyle.SOLID,
    upper_line_width: int = 2,
    upper_line_visible: bool = True,
    
    # Middle band styling
    middle_line_color: str = "#2196F3",
    middle_line_style: LineStyle = LineStyle.SOLID,
    middle_line_width: int = 2,
    middle_line_visible: bool = True,
    
    # Lower band styling
    lower_line_color: str = "#F44336",
    lower_line_style: LineStyle = LineStyle.SOLID,
    lower_line_width: int = 2,
    lower_line_visible: bool = True,
    
    # Fill colors
    upper_fill_color: str = "rgba(76, 175, 80, 0.1)",
    lower_fill_color: str = "rgba(244, 67, 54, 0.1)",
    
    # Line type
    line_type: LineType = LineType.SIMPLE,
    
    # Crosshair markers
    crosshair_marker_visible: bool = True,
    crosshair_marker_radius: int = 4,
    crosshair_marker_border_color: str = "",
    crosshair_marker_background_color: str = "",
    crosshair_marker_border_width: int = 2,
    
    # Animation
    last_price_animation: LastPriceAnimationMode = LastPriceAnimationMode.DISABLED,
    
    # Base options
    price_line_visible: bool = False,
    base_line_visible: bool = False,
    price_format: Optional[Dict[str, Any]] = None,
    markers: Optional[List[Marker]] = None,
    price_scale_config: Optional[Dict[str, Any]] = None,
)
```

### Key Methods

- `to_frontend_config()`: Convert to frontend-compatible configuration
- `get_data_range()`: Get min/max values and times
- `add_marker()`: Add a marker to the series
- `set_price_scale()`: Set price scale ID
- `set_price_line()`: Configure price line
- `set_base_line()`: Configure base line
- `set_price_format()`: Set price formatting

## Contributing

The BandSeries follows the same patterns as other series types in the library:

1. Extends the base `Series` class
2. Implements required abstract methods
3. Provides comprehensive test coverage
4. Follows PEP 8 style guidelines
5. Includes proper documentation

## License

This feature is part of the `streamlit-lightweight-charts-pro` package and follows the same license terms. 