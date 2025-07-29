# Auto-Size and Fit Content Guide

This guide explains how to configure auto-sizing and fit content functionality in the streamlit-lightweight-charts library.

## Overview

The library provides two main features for automatic chart sizing:

1. **Auto-Size**: Automatically adjusts chart dimensions to fit the container
2. **Fit Content**: Automatically scales the time axis to show all data points

## Fit Content Configuration

### Chart Level Configuration

You can configure fit content behavior at the chart level using `ChartOptions`:

```python
from streamlit_lightweight_charts_pro import Chart, ChartOptions

chart = Chart(
    ChartOptions(
        width=800,
        height=400,
        fit_content_on_load=True,  # Enable fit content on load
        handle_double_click=True   # Enable double-click to fit content
    )
)
```

### Time Scale Level Configuration

You can also configure fit content at the time scale level for more granular control:

```python
from streamlit_lightweight_charts_pro import Chart, ChartOptions, TimeScaleOptions

chart = Chart(
    ChartOptions(
        width=800,
        height=400,
        time_scale=TimeScaleOptions(
            fit_content_on_load=True,  # Enable fit content on load
            handle_double_click=True   # Enable double-click to fit content
        )
    )
)
```

### Default Behavior

By default, both `fit_content_on_load` and `handle_double_click` are set to `True`:

```python
# These are the default values
ChartOptions(
    fit_content_on_load=True,  # Default: True
    handle_double_click=True   # Default: True
)

TimeScaleOptions(
    fit_content_on_load=True,  # Default: True
    handle_double_click=True   # Default: True
)
```

## How It Works

### Fit Content on Load

When `fit_content_on_load` is enabled, the chart will automatically call `timeScale.fitContent()` after:

1. All series are created
2. All data is loaded into the series
3. A short delay to ensure data processing is complete

The system uses multiple timing approaches to ensure reliability:

1. **Initial delay**: 500ms after chart creation
2. **Data verification**: Checks if series have data before calling fitContent
3. **Final call**: 300ms after all series are created

### Double-Click to Fit Content

When `handle_double_click` is enabled, users can double-click on the time axis to manually trigger `fitContent()`.

The double-click detection uses a 300ms threshold to distinguish between single and double clicks.

## Configuration Examples

### Enable Fit Content (Default)

```python
from streamlit_lightweight_charts_pro import Chart, ChartOptions, TimeScaleOptions

chart = Chart(
    ChartOptions(
        width=800,
        height=400,
        # fit_content_on_load=True,  # Default, can be omitted
        # handle_double_click=True,  # Default, can be omitted
        time_scale=TimeScaleOptions(
            # fit_content_on_load=True,  # Default, can be omitted
            # handle_double_click=True,  # Default, can be omitted
        )
    )
)
```

### Disable Fit Content

```python
chart = Chart(
    ChartOptions(
        width=800,
        height=400,
        fit_content_on_load=False,  # Disable automatic fit content
        handle_double_click=True,   # Keep double-click enabled
        time_scale=TimeScaleOptions(
            fit_content_on_load=False,  # Disable at time scale level
            handle_double_click=True,   # Keep double-click enabled
        )
    )
)
```

### Custom Configuration

```python
chart = Chart(
    ChartOptions(
        width=800,
        height=400,
        fit_content_on_load=True,   # Enable automatic fit content
        handle_double_click=False,  # Disable double-click
        time_scale=TimeScaleOptions(
            fit_content_on_load=True,   # Enable at time scale level
            handle_double_click=False,  # Disable double-click
        )
    )
)
```

## Troubleshooting

### Chart Not Fitting to Content

If your chart is not automatically fitting to show all data:

1. **Check configuration**: Ensure `fit_content_on_load` is not set to `False`
2. **Verify data**: Make sure your series have data before creating the chart
3. **Check console**: Look for fitContent-related log messages:
   - `✅ fitContent() called after data loaded`
   - `✅ fitContent() called after delay`
   - `✅ fitContent() called after all series loaded`

### Double-Click Not Working

If double-click to fit content is not working:

1. **Check configuration**: Ensure `handle_double_click` is not set to `False`
2. **Click location**: Make sure you're double-clicking on the time axis (x-axis)
3. **Timing**: Ensure clicks are within 300ms of each other

### Performance Considerations

- **Large datasets**: Fit content may take longer with very large datasets
- **Multiple series**: Charts with many series may need more time to process
- **Network delays**: Data loading from external sources may affect timing

## Testing

Use the provided test example to verify fit content functionality:

```bash
streamlit run examples/fit_content_test.py
```

This example demonstrates:
- Charts with fit content enabled vs disabled
- Multi-series charts with fit content
- Double-click functionality
- Expected behavior and troubleshooting

## Console Logging

The library provides detailed console logging for fit content operations:

- `✅ fitContent() called after data loaded` - Initial fit content call
- `✅ fitContent() called after delay` - Fallback fit content call
- `✅ fitContent() called after all series loaded` - Final fit content call
- `✅ fitContent() called on double-click` - Manual double-click trigger
- `❌ fitContent failed` - Error during fit content operation

These logs help diagnose timing and configuration issues. 