# Multi-Pane Charts and Multiple Charts Guide

This guide explains how to properly implement multi-pane charts and multiple charts using the streamlit-lightweight-charts-pro library, following the official lightweight-charts API documentation.

## Overview

The library supports two main scenarios:
1. **Multi-Pane Charts**: Single chart with multiple panes (e.g., price chart + volume + indicators)
2. **Multiple Charts**: Multiple independent charts with synchronization capabilities

## Multi-Pane Charts

### Basic Multi-Pane Setup

```python
from streamlit_lightweight_charts_pro import Chart, CandlestickSeries, HistogramSeries, LineSeries
from streamlit_lightweight_charts_pro.data import OhlcvData, SingleValueData

# Create data
ohlcv_data = [
    OhlcvData("2024-01-01", 100, 105, 98, 102, 1000),
    OhlcvData("2024-01-02", 102, 108, 101, 106, 1200),
]

rsi_data = [
    SingleValueData("2024-01-01", 65),
    SingleValueData("2024-01-02", 70),
]

# Create series with different pane IDs
price_series = CandlestickSeries(
    data=ohlcv_data,
    pane_id=0,  # Main price pane
    price_scale_id="right"
)

volume_series = HistogramSeries(
    data=ohlcv_data,
    pane_id=0,  # Same pane as price (overlay)
    price_scale_id="volume"  # Custom overlay price scale
)

rsi_series = LineSeries(
    data=rsi_data,
    pane_id=1,  # Separate pane for RSI
    price_scale_id="right"
)

# Create chart with multiple panes
chart = Chart(series=[price_series, volume_series, rsi_series])

# Add overlay price scale for volume
from streamlit_lightweight_charts_pro.charts.options.price_scale_options import PriceScaleOptions, PriceScaleMargins

volume_scale = PriceScaleOptions(
    visible=False,
    auto_scale=True,
    scale_margins=PriceScaleMargins(top=0.8, bottom=0.0),
    price_scale_id="volume"
)

chart.add_overlay_price_scale("volume", volume_scale)
chart.render(key="multi_pane_chart")
```

### Advanced Multi-Pane Configuration

```python
from streamlit_lightweight_charts_pro.charts.options import ChartOptions, LayoutOptions

# Configure chart with custom pane heights
chart_options = ChartOptions(
    height=600,
    layout=LayoutOptions(
        background_color="#ffffff",
        text_color="#131722"
    )
)

# Create chart with custom options
chart = Chart(
    series=[price_series, volume_series, rsi_series],
    options=chart_options
)

# Add multiple overlay price scales
volume_scale = PriceScaleOptions(
    visible=False,
    auto_scale=True,
    scale_margins=PriceScaleMargins(top=0.8, bottom=0.0),
    price_scale_id="volume"
)

rsi_scale = PriceScaleOptions(
    visible=True,
    auto_scale=True,
    scale_margins=PriceScaleMargins(top=0.1, bottom=0.1),
    price_scale_id="rsi"
)

chart.add_overlay_price_scale("volume", volume_scale)
chart.add_overlay_price_scale("rsi", rsi_scale)
```

## Multiple Charts

### Basic Multiple Charts Setup

```python
# Create multiple independent charts
chart1 = Chart(series=CandlestickSeries(data=ohlcv_data))
chart2 = Chart(series=LineSeries(data=rsi_data))

# Render charts separately
chart1.render(key="price_chart")
chart2.render(key="indicator_chart")
```

### Synchronized Multiple Charts

```python
from streamlit_lightweight_charts_pro import create_chart

# Create synchronized charts
chart1 = (create_chart()
          .add_candlestick_series(ohlcv_data)
          .set_height(400)
          .build())

chart2 = (create_chart()
          .add_line_series(rsi_data)
          .set_height(200)
          .build())

# Configure synchronization
sync_config = {
    "enabled": True,
    "crosshair": True,
    "timeRange": True
}

# Render with synchronization
chart1.render(key="price_chart", sync_config=sync_config)
chart2.render(key="indicator_chart", sync_config=sync_config)
```

## Price Scale Management

### Overlay Price Scales

```python
# Create volume overlay price scale
volume_scale = PriceScaleOptions(
    visible=False,
    auto_scale=True,
    border_visible=False,
    scale_margins=PriceScaleMargins(top=0.8, bottom=0.0),
    price_scale_id="volume"
)

# Create indicator overlay price scale
indicator_scale = PriceScaleOptions(
    visible=True,
    auto_scale=True,
    scale_margins=PriceScaleMargins(top=0.1, bottom=0.1),
    price_scale_id="indicator"
)

chart.add_overlay_price_scale("volume", volume_scale)
chart.add_overlay_price_scale("indicator", indicator_scale)
```

### Series with Custom Price Scales

```python
# Series using custom price scale
volume_series = HistogramSeries(
    data=volume_data,
    price_scale_id="volume",  # Uses the overlay price scale
    pane_id=0
)

indicator_series = LineSeries(
    data=indicator_data,
    price_scale_id="indicator",  # Uses the indicator price scale
    pane_id=1
)
```

## Pane Management

### Automatic Pane Creation

The library automatically creates panes when series specify `pane_id` values:

```python
# These series will automatically create panes 0 and 1
price_series = CandlestickSeries(data=price_data, pane_id=0)
volume_series = HistogramSeries(data=volume_data, pane_id=0)  # Same pane
rsi_series = LineSeries(data=rsi_data, pane_id=1)  # New pane
macd_series = LineSeries(data=macd_data, pane_id=2)  # Another new pane
```

### Manual Pane Configuration

```python
from streamlit_lightweight_charts_pro.charts.options.layout_options import LayoutOptions

# Configure pane heights manually
layout_options = LayoutOptions(
    background_color="#ffffff",
    text_color="#131722"
)

chart_options = ChartOptions(
    height=600,
    layout=layout_options
)

# The library will automatically distribute height among panes
chart = Chart(series=[price_series, volume_series, rsi_series], options=chart_options)
```

## Best Practices

### 1. Pane ID Management

- Use `pane_id=0` for the main price chart
- Use sequential pane IDs (1, 2, 3...) for additional panes
- Keep related indicators in the same pane when possible

### 2. Price Scale Configuration

- Use `price_scale_id="right"` for main price data
- Use `price_scale_id="left"` for secondary price data
- Use custom IDs for overlay scales (e.g., "volume", "rsi", "macd")

### 3. Performance Optimization

- Limit the number of panes to 3-4 for optimal performance
- Use overlay price scales instead of separate panes when possible
- Consider data density and update frequency

### 4. Synchronization

- Enable crosshair synchronization for better user experience
- Use time range synchronization for coordinated zooming
- Consider performance impact of synchronization on large datasets

## Common Patterns

### Price + Volume + RSI

```python
# Standard trading chart setup
price_series = CandlestickSeries(data=price_data, pane_id=0)
volume_series = HistogramSeries(data=volume_data, pane_id=0, price_scale_id="volume")
rsi_series = LineSeries(data=rsi_data, pane_id=1)

chart = Chart(series=[price_series, volume_series, rsi_series])

# Add volume overlay scale
volume_scale = PriceScaleOptions(
    visible=False,
    auto_scale=True,
    scale_margins=PriceScaleMargins(top=0.8, bottom=0.0),
    price_scale_id="volume"
)
chart.add_overlay_price_scale("volume", volume_scale)
```

### Multiple Timeframes

```python
# Create charts for different timeframes
daily_chart = Chart(series=CandlestickSeries(data=daily_data))
hourly_chart = Chart(series=CandlestickSeries(data=hourly_data))

# Synchronize for coordinated analysis
sync_config = {"enabled": True, "crosshair": True, "timeRange": True}
daily_chart.render(key="daily", sync_config=sync_config)
hourly_chart.render(key="hourly", sync_config=sync_config)
```

## Troubleshooting

### Common Issues

1. **Panes not appearing**: Ensure `pane_id` is properly set on series
2. **Price scales not working**: Verify `price_scale_id` matches overlay scale configuration
3. **Synchronization not working**: Check that `sync_config` is properly enabled
4. **Performance issues**: Reduce number of panes or use overlay scales instead

### Debug Tips

- Check browser console for error messages
- Verify data format and time alignment
- Test with minimal configuration first
- Use the browser's developer tools to inspect chart elements

## API Reference

### Chart Methods

- `add_overlay_price_scale(scale_id, options)`: Add custom price scale
- `add_series(series)`: Add series to chart
- `update_options(options)`: Update chart configuration

### Series Properties

- `pane_id`: Specify which pane the series belongs to
- `price_scale_id`: Specify which price scale to use
- `options`: Series-specific styling and behavior options

### Configuration Options

- `ChartOptions`: Main chart configuration
- `PriceScaleOptions`: Price scale configuration
- `LayoutOptions`: Layout and appearance configuration 