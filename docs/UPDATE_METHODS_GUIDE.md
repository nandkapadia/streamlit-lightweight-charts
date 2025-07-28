# Update Methods Guide

This guide explains the dictionary-based update functionality for both Options and Series base classes in the streamlit-lightweight-charts library.

## Overview

The `update()` method provides a flexible, pythonic way to update object properties using dictionaries. It supports:

- **Simple property updates**: Direct assignment of values
- **Nested object updates**: Automatic creation and updating of nested Options objects
- **CamelCase key support**: Automatic conversion from camelCase to snake_case
- **Method chaining**: Fluent API for multiple updates
- **Error handling**: Validation of field names and types
- **None value handling**: Graceful handling of None values for method chaining

## Options Base Class Update Method

### Basic Usage

```python
from streamlit_lightweight_charts_pro.charts.options.line_options import LineOptions
from streamlit_lightweight_charts_pro.type_definitions.enums import LineStyle

# Create options
options = LineOptions()

# Update simple properties
options.update({
    "color": "#ff0000",
    "line_width": 3,
    "line_style": LineStyle.DASHED
})

print(f"Color: {options.color}")
print(f"Line Width: {options.line_width}")
print(f"Line Style: {options.line_style}")
```

### CamelCase Key Support

```python
# Keys can be in camelCase (automatically converted to snake_case)
options.update({
    "lineWidth": 5,
    "lineStyle": LineStyle.DOTTED
})

# Both formats work
assert options.line_width == 5
assert options.line_style == LineStyle.DOTTED
```

### Method Chaining

```python
# Chain multiple updates
result = (options
         .update({"color": "#ff0000"})
         .update({"line_width": 3})
         .update({"line_style": LineStyle.DASHED}))

assert result is options  # Returns self for chaining
```

### Nested Options Updates

```python
# For nested Options objects, the update method handles them automatically
# If the field is None, it creates a new instance
# If the field exists, it updates the existing instance

class ChartOptions(Options):
    line_options: Optional[LineOptions] = None

chart_options = ChartOptions()

# This will create a new LineOptions instance and update it
chart_options.update({
    "line_options": {
        "color": "#ff0000",
        "line_width": 3
    }
})

assert chart_options.line_options.color == "#ff0000"
assert chart_options.line_options.line_width == 3
```

## Series Base Class Update Method

### Basic Usage

```python
from streamlit_lightweight_charts_pro.charts.series.line import LineSeries
from streamlit_lightweight_charts_pro.charts.options.line_options import LineOptions
from streamlit_lightweight_charts_pro.data.line_data import LineData

# Create series
data = [LineData(time=1640995200, value=100)]
line_options = LineOptions()
series = LineSeries(data=data, line_options=line_options)

# Update simple properties
series.update({
    "visible": False,
    "price_scale_id": "left",
    "pane_id": 1
})

print(f"Visible: {series.visible}")
print(f"Price Scale ID: {series.price_scale_id}")
print(f"Pane ID: {series.pane_id}")
```

### Nested Options Updates

```python
# Update nested Options objects
series.update({
    "line_options": {
        "color": "#0000ff",
        "line_width": 4,
        "line_style": LineStyle.SOLID
    }
})

print(f"Line Color: {series.line_options.color}")
print(f"Line Width: {series.line_options.line_width}")
```

### Complex Nested Updates

```python
# Update both simple properties and nested objects in one call
series.update({
    "visible": True,
    "price_scale_id": "right",
    "line_options": {
        "color": "#ff6600",
        "line_width": 2,
        "line_style": LineStyle.DASHED
    }
})
```

## Error Handling

### Invalid Fields

```python
options = LineOptions()

# This raises ValueError
try:
    options.update({"invalid_field": "value"})
except ValueError as e:
    print(f"Error: {e}")
    # Output: Error: Invalid option field: invalid_field
```

### Mixed Valid and Invalid Fields

```python
# The first valid field is updated, then error is raised
try:
    options.update({
        "color": "#ff0000",  # This works
        "invalid_field": "value"  # This raises error
    })
except ValueError as e:
    print(f"Error: {e}")
    # The color was still updated before the error
```

## Advanced Usage Patterns

### Configuration from Dictionary

```python
# Load configuration from external source
config = {
    "color": "#ff0000",
    "line_width": 2,
    "line_style": LineStyle.DASHED
}

options = LineOptions()
options.update(config)
```

### Conditional Updates

```python
options = LineOptions()

# Update based on condition
if some_condition:
    options.update({"color": "#00ff00"})
else:
    options.update({"color": "#ff0000"})
```

### Progressive Updates

```python
options = LineOptions()

# Update in stages
options.update({"color": "#ff0000"})
options.update({"line_width": 3})
options.update({"line_style": LineStyle.DOTTED})
```

### Preserving Existing Values

```python
options = LineOptions(color="#ff0000", line_width=2, line_style=LineStyle.SOLID)

# Only update line_width, preserve others
options.update({"line_width": 5})

assert options.color == "#ff0000"  # Preserved
assert options.line_width == 5     # Updated
assert options.line_style == LineStyle.SOLID  # Preserved
```

## Integration with Serialization

The update methods work seamlessly with the existing serialization system:

```python
options = LineOptions()
options.update({
    "color": "#ff0000",
    "line_width": 3,
    "line_style": LineStyle.DASHED
})

# Serialize to dictionary (camelCase keys for frontend)
result = options.asdict()

print(result)
# Output: {
#     "color": "#ff0000",
#     "lineWidth": 3,
#     "lineStyle": 1  # Enum value
# }
```

## Best Practices

### 1. Use Method Chaining for Multiple Updates

```python
# Good: Method chaining
options.update({"color": "#ff0000"}).update({"line_width": 3})

# Less efficient: Multiple separate calls
options.update({"color": "#ff0000"})
options.update({"line_width": 3})
```

### 2. Handle None Values Gracefully

```python
# Good: None values are ignored for method chaining
options.update({
    "color": None,  # Ignored
    "line_width": 3  # Applied
})

# This allows for conditional updates without errors
```

### 3. Validate Configuration Dictionaries

```python
# Good: Validate before updating
config = load_config_from_file()
if is_valid_config(config):
    options.update(config)
else:
    raise ValueError("Invalid configuration")
```

### 4. Use Type Hints for Better IDE Support

```python
from typing import Dict, Any

def update_chart_options(options: LineOptions, config: Dict[str, Any]) -> LineOptions:
    return options.update(config)
```

## Performance Considerations

- **Single update call**: More efficient than multiple separate calls
- **Field validation**: Minimal overhead for field existence checks
- **Nested object creation**: Only creates new objects when needed
- **Memory usage**: No additional memory overhead beyond normal object creation

## Migration from Existing Code

### Before (Manual Property Setting)

```python
# Old way
options = LineOptions()
options.color = "#ff0000"
options.line_width = 3
options.line_style = LineStyle.DASHED
```

### After (Dictionary Updates)

```python
# New way
options = LineOptions()
options.update({
    "color": "#ff0000",
    "line_width": 3,
    "line_style": LineStyle.DASHED
})
```

### Benefits of Migration

1. **More concise**: Single call instead of multiple assignments
2. **More flexible**: Easy to update from external configuration
3. **Better error handling**: Validation of field names
4. **Method chaining**: Fluent API for complex updates
5. **CamelCase support**: Automatic key conversion

## Testing

The update methods are thoroughly tested with comprehensive test cases covering:

- Simple property updates
- Nested object updates
- CamelCase key conversion
- Method chaining
- Error handling
- Edge cases
- Integration with serialization

Run the tests with:

```bash
python -m pytest tests/unit/test_update_methods.py -v
```

## Conclusion

The `update()` method provides a powerful, pythonic way to update Options and Series objects. It maintains backward compatibility while adding significant flexibility and convenience for configuration management.

The implementation follows Python best practices and integrates seamlessly with the existing codebase, making it easy to adopt in both new and existing code. 