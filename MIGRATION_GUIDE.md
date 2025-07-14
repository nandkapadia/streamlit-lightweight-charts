# Migration Guide

This guide helps you migrate from the original streamlit-lightweight-charts to the enhanced version 2.0.

## Key Changes

### 1. New Import Structure

The library now exports new classes and utilities while maintaining backward compatibility:

```python
# Old way (still works)
from streamlit_lightweight_charts import renderLightweightCharts

# New way (recommended)
from streamlit_lightweight_charts import (
    Chart, ChartGroup, SeriesType, 
    PriceScaleMode, CrosshairMode, LineStyle,
    Themes, create_candlestick_chart, create_volume_chart
)
```

### 2. Chart Creation

#### Old API:
```python
chart_options = {
    "width": 600,
    "height": 400,
    "layout": {
        "textColor": 'black',
        "background": {"type": 'solid', "color": 'white'}
    }
}

series = [{
    "type": 'Candlestick',
    "data": candlestick_data,
    "options": {
        "upColor": '#26a69a',
        "downColor": '#ef5350'
    }
}]

renderLightweightCharts([{
    "chart": chart_options,
    "series": series
}], 'chart1')
```

#### New API:
```python
# Create a chart instance
chart = Chart(
    width=600,
    height=400,
    layout={
        'textColor': 'black',
        'background': {'type': 'solid', 'color': 'white'}
    }
)

# Add series
chart.add_series(
    SeriesType.CANDLESTICK,
    candlestick_data,
    options={
        'upColor': '#26a69a',
        'downColor': '#ef5350'
    }
)

# Create a chart group and render
chart_group = ChartGroup()
chart_group.add_chart(chart)
chart_group.render(key='chart1')
```

### 3. Multi-Pane Charts with Synchronization

#### Old API (Limited Sync):
```python
charts = [
    {"chart": chart1_options, "series": series1},
    {"chart": chart2_options, "series": series2}
]
renderLightweightCharts(charts, 'multipane')
```

#### New API (Full Sync):
```python
# Create synchronized chart group
chart_group = ChartGroup(
    sync_enabled=True,
    sync_crosshair=True,  # New: crosshair sync
    sync_time_range=True
)

# Add multiple charts
chart_group.add_chart(price_chart)
chart_group.add_chart(volume_chart)
chart_group.add_chart(rsi_chart)

chart_group.render(key='multipane')
```

### 4. Event Handling

#### Old API:
No event handling support.

#### New API:
```python
# Add event callbacks
def on_click(event_data):
    st.write(f"Clicked at {event_data['time']}")

def on_crosshair_move(event_data):
    st.session_state.crosshair_data = event_data

chart_group.on_click(on_click)
chart_group.on_crosshair_move(on_crosshair_move)
```

### 5. Using Enums for Better Type Safety

#### Old API:
```python
series = [{
    "type": 'Line',  # String literal
    "data": data
}]
```

#### New API:
```python
chart.add_series(
    SeriesType.LINE,  # Type-safe enum
    data
)
```

### 6. Price Lines and Advanced Features

#### Old API:
Not supported.

#### New API:
```python
# Add price lines
chart.add_price_line(
    price=100,
    color='#4CAF50',
    line_style=LineStyle.DASHED,
    title='Support'
)

# Use predefined themes
chart = Chart(**Themes.TRADING_VIEW)

# Multiple price scales
chart.add_series(
    SeriesType.LINE,
    data,
    price_scale_id="left",
    price_scale={'scaleMargins': {'top': 0.1, 'bottom': 0.1}}
)
```

## Quick Migration Checklist

1. **Update imports**: Add new classes to your imports
2. **Replace dictionary configs with Chart objects**: Use the Chart class for configuration
3. **Use ChartGroup for multiple charts**: Wrap charts in a ChartGroup for synchronization
4. **Replace string types with enums**: Use SeriesType enum for type safety
5. **Add event handlers**: Leverage new callback capabilities
6. **Update series configuration**: Use the add_series method with named parameters

## Backward Compatibility

The original `renderLightweightCharts()` function is still available and works exactly as before. You can migrate gradually:

```python
# This still works
renderLightweightCharts(old_chart_config, 'my_chart')

# But you can mix old and new in the same app
new_chart = Chart()
new_chart.add_series(SeriesType.LINE, data)
ChartGroup().add_chart(new_chart).render('new_chart')
```

## Common Migration Patterns

### Pattern 1: Simple Chart
```python
# Old
renderLightweightCharts([{
    "chart": {"width": 600, "height": 400},
    "series": [{"type": "Line", "data": data}]
}], 'chart')

# New
chart = Chart(width=600, height=400)
chart.add_series(SeriesType.LINE, data)
ChartGroup().add_chart(chart).render('chart')
```

### Pattern 2: Multi-Series Chart
```python
# Old
series = [
    {"type": "Candlestick", "data": ohlc_data},
    {"type": "Line", "data": sma_data, "options": {"color": "blue"}}
]
renderLightweightCharts([{"chart": {}, "series": series}], 'chart')

# New
chart = Chart()
chart.add_series(SeriesType.CANDLESTICK, ohlc_data)
chart.add_series(SeriesType.LINE, sma_data, options={'color': 'blue'})
ChartGroup().add_chart(chart).render('chart')
```

### Pattern 3: Indicators with Price Scales
```python
# Old (not well supported)
# Complex price scale configuration was difficult

# New
chart.add_series(
    SeriesType.HISTOGRAM,
    volume_data,
    price_scale_id='',  # Overlay
    price_scale={'scaleMargins': {'top': 0.7, 'bottom': 0}}
)
```

## Performance Considerations

The new API is designed to be more efficient:

1. **Better synchronization**: Charts sync without redundant updates
2. **Optimized rendering**: ChartGroup manages rendering efficiently
3. **Event debouncing**: Callbacks are automatically debounced

## Getting Help

- Check the [examples](examples/) directory for complete working examples
- Review the [enhanced README](README_ENHANCED.md) for detailed API documentation
- Report issues on the [GitHub repository](https://github.com/yourusername/streamlit-lightweight-charts)

## Summary

The enhanced version provides:
- ✅ Full backward compatibility
- ✅ Type-safe API with enums
- ✅ Better chart synchronization
- ✅ Event handling and callbacks
- ✅ More chart customization options
- ✅ Cleaner, more Pythonic API

Start with backward-compatible mode and gradually adopt new features as needed!