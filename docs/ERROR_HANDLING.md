# Error Handling Guide

This guide explains the comprehensive error handling improvements in the streamlit-lightweight-charts-pro library and how to handle common issues.

## Overview

The library now includes comprehensive error handling to prevent crashes and provide informative error messages when issues occur. All annotation-related errors have been addressed with multiple layers of validation and defensive programming.

## Common Issues and Solutions

### 1. Annotation Errors - RESOLVED ✅

**Problem**: `TypeError: t.forEach is not a function` in annotation system

**Root Cause**: Multiple issues were identified and fixed:
- Annotations passed as `undefined`, `null`, or non-array values
- Annotation structure mismatch between Python AnnotationManager and frontend expectations
- Missing validation in multiple forEach calls throughout the codebase

**Comprehensive Solution**: Multiple layers of validation and structure handling:

```python
# ❌ These will now be handled gracefully (no crash)
series = CandlestickSeries(
    data=data,
    annotations=None  # Invalid but handled
)

series = CandlestickSeries(
    data=data,
    annotations="not an array"  # Invalid but handled
)

# ✅ These are the correct ways
series = CandlestickSeries(
    data=data,
    annotations=[]  # Valid empty array
)

# ✅ Using AnnotationManager (recommended)
from streamlit_lightweight_charts_pro.data.annotation import create_text_annotation

annotation = create_text_annotation("2024-01-15", 100, "Test")
chart.add_annotation(annotation)  # Creates proper structure
```

### 2. Annotation Structure Handling - RESOLVED ✅

**Problem**: Annotations from Python's AnnotationManager create a different structure than expected

**Root Cause**: Python's AnnotationManager creates a `{layers: {...}}` structure, but frontend expected direct arrays

**Solution**: The frontend now handles both structures automatically:

```python
# Python side creates this structure:
{
    "layers": {
        "default": {
            "name": "default",
            "visible": True,
            "annotations": [...]
        }
    }
}

# Frontend now extracts annotations from all visible layers
# and processes them correctly
```

### 3. Multiple forEach Validation - RESOLVED ✅

**Problem**: Multiple forEach calls throughout the codebase lacked proper validation

**Solution**: Added comprehensive validation to all forEach calls:

- `createAnnotationVisualElements` function
- `addAnnotations` function  
- `addAnnotationLayers` function
- `visualElements.annotations.forEach` calls
- `Object.values(annotations.layers).forEach` calls
- `Object.values(layers.layers)` calls

### 4. Chart Creation Failures - RESOLVED ✅

**Problem**: Charts fail to create due to invalid options or container issues

**Solution**: Enhanced error handling with informative messages:

```python
# The library now provides detailed error messages
chart = Chart(
    ChartOptions(
        width=800,
        height=400
    )
)

# If chart creation fails, you'll see specific error messages
# instead of silent failures
```

### 5. Series Creation Failures - RESOLVED ✅

**Problem**: Individual series fail to create, causing chart to be incomplete

**Solution**: Series creation is now isolated - if one series fails, others continue:

```python
# If one series fails, others will still be created
chart.add_series(series1)  # This might fail
chart.add_series(series2)  # This will still work
chart.add_series(series3)  # This will still work
```

### 6. Invalid Configuration - RESOLVED ✅

**Problem**: Invalid configuration objects cause crashes

**Solution**: Configuration validation with warnings:

```python
# ❌ Invalid config - will show warning but won't crash
chart = Chart(
    ChartOptions(
        width="invalid",  # Should be number
        height=None       # Should be number
    )
)

# ✅ Valid config
chart = Chart(
    ChartOptions(
        width=800,
        height=400
    )
)
```

## Error Handling Features

### 1. Graceful Degradation - ENHANCED ✅

The library now handles errors gracefully:
- Invalid annotations are skipped with warnings
- Failed series creation doesn't prevent other series
- Chart creation failures are logged but don't crash the app
- Multiple validation layers prevent forEach errors

### 2. Informative Logging - ENHANCED ✅

Enhanced console logging provides useful debugging information:
- Warning messages for invalid configurations
- Error messages with context for failures
- Success confirmations for operations
- Debug logging for annotation processing

### 3. Comprehensive Validation - ENHANCED ✅

Multiple layers of validation ensure data integrity:
- Array validation for annotations and layers
- Object validation for configuration
- Type checking for critical parameters
- forEach function validation
- Structure compatibility checks

### 4. Structure Compatibility - ENHANCED ✅

The frontend now handles multiple annotation structures:
- Direct arrays of annotations
- AnnotationManager structures with layers
- Mixed structures with both formats
- Null and undefined values
- Invalid data types

### 5. Defensive Programming - NEW ✅

Added defensive programming throughout the codebase:
- Try-catch blocks around all critical operations
- Multiple validation layers
- Graceful fallbacks for invalid data
- Comprehensive error recovery

## Best Practices

### 1. Always Validate Data

```python
# Validate your data before creating charts
if not data or len(data) == 0:
    st.error("No data available")
    return

# Validate annotations
if annotations and not isinstance(annotations, list):
    st.warning("Annotations must be a list")
    annotations = []
```

### 2. Use Try-Catch Blocks

```python
try:
    chart = Chart(ChartOptions(width=800, height=400))
    chart.add_series(series)
    st.components.v1.html(chart.to_html(), height=450)
except Exception as e:
    st.error(f"Failed to create chart: {e}")
```

### 3. Check Console Logs

Monitor browser console for warnings and errors:
- Open browser developer tools (F12)
- Check Console tab for messages
- Look for warnings about invalid configurations
- Monitor for annotation processing logs

### 4. Use Proper Annotation Structure

```python
# ✅ Recommended: Use AnnotationManager
from streamlit_lightweight_charts_pro.data.annotation import create_text_annotation

annotation = create_text_annotation("2024-01-15", 100, "Event")
chart.add_annotation(annotation)

# ✅ Also valid: Direct array
annotations = [
    {
        "time": "2024-01-15",
        "price": 100,
        "text": "Event",
        "type": "text"
    }
]

# ✅ Also valid: Mixed valid/invalid (will skip invalid)
annotations = [
    {"time": "2024-01-15", "price": 100, "text": "Valid", "type": "text"},
    None,  # Will be skipped
    "invalid",  # Will be skipped
    {"time": "2024-01-16", "price": 110, "text": "Valid", "type": "text"}
]
```

## Debugging Tips

### 1. Enable Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 2. Check Data Types

```python
# Verify data structure
print(f"Data type: {type(data)}")
print(f"Data length: {len(data) if data else 0}")
print(f"First item: {data[0] if data else None}")
```

### 3. Validate Configuration

```python
# Check chart options
print(f"Chart options: {chart_options}")
print(f"Series config: {series_config}")
```

### 4. Check Annotation Structure

```python
# Verify annotation structure
config = chart.to_frontend_config()
annotations = config["charts"][0]["annotations"]
print(f"Annotation structure: {annotations}")
```

### 5. Monitor Console Logs

The library now provides extensive console logging:
- `createAnnotationVisualElements called with:` - Shows what's being processed
- `Type of annotations:` - Shows the data type
- `Is array:` - Shows if it's an array
- `Has forEach:` - Shows if forEach is available

## Common Error Messages

| Error | Cause | Solution | Status |
|-------|-------|----------|--------|
| `t.forEach is not a function` | Invalid annotations array or structure | Ensure annotations is a list or use AnnotationManager | ✅ RESOLVED |
| `Failed to create chart` | Invalid chart options | Check ChartOptions parameters | ✅ RESOLVED |
| `Invalid series config` | Malformed series data | Validate series configuration | ✅ RESOLVED |
| `Container not connected` | DOM issues | Check container element | ✅ RESOLVED |
| `layers.forEach is not a function` | Annotation structure mismatch | Use proper annotation structure | ✅ RESOLVED |
| `visualElements.annotations.forEach is not a function` | Invalid visual elements | Library now validates automatically | ✅ RESOLVED |

## Testing Error Handling

Use the provided test examples to verify error handling:

```bash
# Test comprehensive error handling
python examples/comprehensive_error_test.py

# Test annotation structure handling
python examples/annotation_structure_test.py

# Test general error handling
python examples/error_handling_test.py
```

These examples create charts with various error scenarios to ensure they're handled properly.

## What's Fixed

### ✅ Annotation System
- `TypeError: t.forEach is not a function` - COMPLETELY RESOLVED
- Invalid annotation structures - HANDLED GRACEFULLY
- Null/undefined annotations - HANDLED GRACEFULLY
- Mixed valid/invalid annotations - INVALID ONES SKIPPED
- AnnotationManager structure mismatch - AUTOMATICALLY HANDLED

### ✅ Error Prevention
- Multiple validation layers added
- Defensive programming throughout
- Comprehensive try-catch blocks
- Graceful degradation for all error scenarios

### ✅ Debugging Support
- Extensive console logging
- Informative error messages
- Debug information for annotation processing
- Clear warnings for invalid configurations

## Reporting Issues

When reporting issues, include:
1. Error messages from browser console
2. Python code that reproduces the issue
3. Data structure and types
4. Browser and version information
5. Annotation structure being used
6. Console logs showing the debug information

This helps us provide better error handling and fixes.

## Summary

The annotation system has been completely overhauled with comprehensive error handling. The `TypeError: t.forEach is not a function` error and all related issues have been resolved through:

1. **Multiple validation layers** in all annotation processing functions
2. **Structure compatibility** for both direct arrays and AnnotationManager structures
3. **Defensive programming** with try-catch blocks throughout
4. **Comprehensive logging** for debugging and monitoring
5. **Graceful degradation** for all error scenarios

The library now handles any annotation-related errors gracefully without crashing, providing a robust and reliable charting experience. 