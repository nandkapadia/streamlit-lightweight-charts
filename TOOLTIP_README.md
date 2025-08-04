# Tooltip System for Lightweight Charts

This document describes the comprehensive tooltip functionality implemented for the Lightweight Charts project. The tooltip system provides dynamic content with placeholders, multiple tooltip types, and flexible configuration options.

## Features

- **Dynamic Content**: Use placeholders like `{price}`, `{volume}`, `{value}` that are automatically replaced with actual data
- **Multiple Tooltip Types**: OHLC, single value, multi-series, custom, trade, and marker tooltips
- **Flexible Positioning**: Cursor, fixed, or auto positioning
- **Custom Styling**: Full control over appearance including colors, fonts, borders, and shadows
- **Template Support**: Use custom templates with placeholders for dynamic content
- **Field Configuration**: Define custom fields with formatting, precision, prefixes, and suffixes
- **Date/Time Formatting**: Configurable date and time display
- **Trade Integration**: Special tooltips for trade visualization with P&L information
- **Marker Support**: Tooltips for custom markers and annotations

## Quick Start

### Basic OHLC Tooltip

```python
from streamlit_lightweight_charts_pro import Chart, CandlestickSeries
from streamlit_lightweight_charts_pro.data import create_ohlc_tooltip

# Create chart
chart = Chart(series=CandlestickSeries(data=ohlc_data))

# Add default OHLC tooltip
tooltip_config = create_ohlc_tooltip()
chart.add_tooltip_config("default", tooltip_config)

chart.render()
```

### Custom Template Tooltip

```python
from streamlit_lightweight_charts_pro.data import create_custom_tooltip, TooltipField

# Create custom tooltip with template
custom_tooltip = create_custom_tooltip(
    template="Price: {price}\nVolume: {volume}\nDate: {time}"
)

# Add field formatting
custom_tooltip.fields = [
    TooltipField("Price", "price", precision=2, prefix="$"),
    TooltipField("Volume", "volume", formatter=lambda x: f"{x:,.0f}"),
    TooltipField("Date", "time")
]

chart.add_tooltip_config("custom", custom_tooltip)
```

### Custom Styled Tooltip

```python
from streamlit_lightweight_charts_pro.data.tooltip import TooltipConfig, TooltipStyle

styled_tooltip = TooltipConfig(
    type=TooltipType.SINGLE,
    template="📈 Price: {price}",
    position=TooltipPosition.CURSOR,
    offset={"x": 10, "y": -10},
    style=TooltipStyle(
        background_color="rgba(0, 0, 0, 0.9)",
        border_color="#00ff00",
        border_width=2,
        border_radius=8,
        padding=12,
        font_size=14,
        font_family="monospace",
        color="#ffffff",
        box_shadow="0 4px 8px rgba(0, 0, 0, 0.3)"
    ),
    show_date=True,
    show_time=True
)

chart.add_tooltip_config("styled", styled_tooltip)
```

## Tooltip Types

### 1. OHLC Tooltip (`TooltipType.OHLC`)
Default tooltip for candlestick charts showing Open, High, Low, Close, and Volume.

```python
ohlc_tooltip = create_ohlc_tooltip()
```

### 2. Single Value Tooltip (`TooltipType.SINGLE`)
For line charts and single value series.

```python
single_tooltip = create_single_value_tooltip()
```

### 3. Multi-Series Tooltip (`TooltipType.MULTI`)
For charts with multiple series.

```python
multi_tooltip = create_multi_series_tooltip()
```

### 4. Custom Tooltip (`TooltipType.CUSTOM`)
Fully customizable tooltip with template and field configuration.

```python
custom_tooltip = create_custom_tooltip("Custom template: {price}")
```

### 5. Trade Tooltip (`TooltipType.TRADE`)
Specialized tooltip for trade visualization with P&L information.

```python
trade_tooltip = create_trade_tooltip()
```

### 6. Marker Tooltip (`TooltipType.MARKER`)
Tooltip for custom markers and annotations.

```python
marker_tooltip = TooltipConfig(type=TooltipType.MARKER)
```

## Tooltip Configuration

### TooltipConfig

The main configuration class for tooltips:

```python
TooltipConfig(
    enabled=True,                    # Enable/disable tooltip
    type=TooltipType.OHLC,          # Tooltip type
    template="Price: {price}",      # Custom template
    fields=[...],                   # Field configurations
    position=TooltipPosition.CURSOR, # Positioning
    offset={"x": 10, "y": -10},     # Offset from position
    style=TooltipStyle(...),        # Styling
    show_date=True,                 # Show date
    show_time=True,                 # Show time
    date_format="%Y-%m-%d",         # Date format
    time_format="%H:%M"             # Time format
)
```

### TooltipField

Configure individual fields in tooltips:

```python
TooltipField(
    label="Price",                  # Display label
    value_key="price",              # Data key
    formatter=lambda x: f"${x:.2f}", # Custom formatter
    color="#ff0000",                # Text color
    font_size=14,                   # Font size
    font_weight="bold",             # Font weight
    prefix="$",                     # Prefix
    suffix=" USD",                  # Suffix
    precision=2                     # Decimal precision
)
```

### TooltipStyle

Configure tooltip appearance:

```python
TooltipStyle(
    background_color="rgba(255, 255, 255, 0.95)",
    border_color="#e1e3e6",
    border_width=1,
    border_radius=4,
    padding=8,
    font_size=12,
    font_family="sans-serif",
    color="#131722",
    box_shadow="0 2px 4px rgba(0, 0, 0, 0.1)",
    z_index=1000
)
```

## Positioning Options

### TooltipPosition

- `CURSOR`: Follows the mouse cursor
- `FIXED`: Fixed position on the chart
- `AUTO`: Automatic positioning

```python
tooltip_config.position = TooltipPosition.CURSOR
tooltip_config.offset = {"x": 10, "y": -10}  # Offset from position
```

## Available Placeholders

The following placeholders can be used in templates:

- `{price}` - Current price value
- `{value}` - Series value
- `{time}` - Time/date
- `{open}` - Open price (OHLC)
- `{high}` - High price (OHLC)
- `{low}` - Low price (OHLC)
- `{close}` - Close price (OHLC)
- `{volume}` - Volume data
- `{index}` - Data point index
- Custom data fields from your series

## Trade Tooltips

Special tooltips for trade visualization:

```python
from streamlit_lightweight_charts_pro.data import TradeData, TradeType

# Create trade data
trade = TradeData(
    entry_time="2024-01-15 10:00:00",
    entry_price=100.0,
    exit_time="2024-01-20 15:00:00",
    exit_price=105.0,
    quantity=100,
    trade_type=TradeType.LONG,
    id="TRADE_001",
    notes="Breakout trade"
)

# Create trade tooltip
trade_tooltip = create_trade_tooltip()
trade_tooltip.template = """
Trade: {id}
Entry: ${entryPrice} | Exit: ${exitPrice}
Quantity: {quantity}
P&L: ${pnl} ({pnlPercentage}%)
Type: {tradeType}
Notes: {notes}
"""

chart.add_tooltip_config("trade", trade_tooltip)
chart.add_trades([trade])
```

## Tooltip Manager

For complex scenarios with multiple tooltip configurations:

```python
from streamlit_lightweight_charts_pro.data.tooltip import TooltipManager

# Create tooltip manager
tooltip_manager = TooltipManager()

# Add multiple configurations
tooltip_manager.create_ohlc_tooltip("price")
tooltip_manager.create_single_value_tooltip("volume")

# Create custom tooltip
ma_tooltip = tooltip_manager.create_custom_tooltip(
    "Moving Average: {value}",
    "ma"
)

# Set manager on chart
chart.set_tooltip_manager(tooltip_manager)
```

## Series-Level Tooltips

You can also set tooltips directly on series:

```python
from streamlit_lightweight_charts_pro import LineSeries
from streamlit_lightweight_charts_pro.data import create_single_value_tooltip

# Create series with tooltip
series = LineSeries(data=data)
series.tooltip = create_single_value_tooltip()

# Add to chart
chart = Chart(series=series)
```

## Examples

### Basic Line Chart with Tooltip

```python
import streamlit as st
from streamlit_lightweight_charts_pro import Chart, LineSeries
from streamlit_lightweight_charts_pro.data import SingleValueData, create_single_value_tooltip

# Create data
data = [
    SingleValueData(time="2024-01-01", value=100),
    SingleValueData(time="2024-01-02", value=105),
    SingleValueData(time="2024-01-03", value=102),
]

# Create chart
chart = Chart(series=LineSeries(data=data))

# Add tooltip
tooltip = create_single_value_tooltip()
chart.add_tooltip_config("default", tooltip)

# Render
chart.render()
```

### Candlestick Chart with OHLC Tooltip

```python
from streamlit_lightweight_charts_pro import CandlestickSeries
from streamlit_lightweight_charts_pro.data import CandlestickData, create_ohlc_tooltip

# Create OHLC data
ohlc_data = [
    CandlestickData(time="2024-01-01", open=100, high=105, low=98, close=103),
    CandlestickData(time="2024-01-02", open=103, high=108, low=101, close=106),
]

# Create chart
chart = Chart(series=CandlestickSeries(data=ohlc_data))

# Add OHLC tooltip
tooltip = create_ohlc_tooltip()
chart.add_tooltip_config("ohlc", tooltip)

chart.render()
```

### Custom Styled Tooltip

```python
from streamlit_lightweight_charts_pro.data.tooltip import TooltipConfig, TooltipStyle, TooltipType

# Create custom styled tooltip
styled_tooltip = TooltipConfig(
    type=TooltipType.SINGLE,
    template="🎯 Price: {price}\n📊 Value: {value}",
    position=TooltipPosition.CURSOR,
    style=TooltipStyle(
        background_color="rgba(0, 0, 0, 0.9)",
        border_color="#00ff00",
        border_width=2,
        border_radius=8,
        padding=12,
        font_size=14,
        font_family="monospace",
        color="#ffffff"
    ),
    show_date=True,
    show_time=True
)

chart.add_tooltip_config("styled", styled_tooltip)
```

## Integration with Existing Code

The tooltip system is designed to be non-intrusive and backward compatible. Existing charts will continue to work without any changes. To add tooltips to existing charts, simply add the tooltip configuration:

```python
# Existing chart code
chart = Chart(series=LineSeries(data=data))

# Add tooltip (new)
tooltip = create_single_value_tooltip()
chart.add_tooltip_config("default", tooltip)

# Render (unchanged)
chart.render()
```

## Best Practices

1. **Use Appropriate Tooltip Types**: Choose the tooltip type that matches your data (OHLC for candlesticks, single for lines, etc.)

2. **Keep Templates Simple**: Use clear, concise templates that are easy to read

3. **Use Field Formatting**: Leverage field configuration for consistent formatting across your application

4. **Consider Performance**: For large datasets, consider disabling tooltips or using simpler configurations

5. **Test Positioning**: Ensure tooltips are positioned correctly and don't interfere with chart interaction

6. **Use Custom Formatters**: Create custom formatters for complex data formatting needs

## Troubleshooting

### Tooltip Not Showing
- Check that tooltip is enabled (`enabled=True`)
- Verify that the tooltip configuration is properly added to the chart
- Ensure the chart has data and is interactive

### Placeholders Not Replaced
- Verify that the placeholder names match the data keys
- Check that the data contains the expected fields
- Use field configuration to ensure proper formatting

### Styling Issues
- Check that the style configuration is valid
- Verify CSS color formats (hex, rgba, etc.)
- Ensure z-index is appropriate for your layout

## API Reference

### Classes

- `TooltipConfig` - Main tooltip configuration
- `TooltipField` - Individual field configuration
- `TooltipStyle` - Styling configuration
- `TooltipManager` - Manager for multiple tooltip configurations

### Enums

- `TooltipType` - Available tooltip types
- `TooltipPosition` - Positioning options

### Functions

- `create_ohlc_tooltip()` - Create default OHLC tooltip
- `create_single_value_tooltip()` - Create single value tooltip
- `create_custom_tooltip(template)` - Create custom tooltip
- `create_trade_tooltip()` - Create trade tooltip
- `create_multi_series_tooltip()` - Create multi-series tooltip

For detailed API documentation, see the individual class and function docstrings. 