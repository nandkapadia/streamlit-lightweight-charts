# Integration Tests

This directory contains integration tests that verify how different components work together.

## Purpose

Integration tests focus on:
- Component interactions and data flow
- End-to-end workflows
- Cross-module dependencies
- Real-world usage scenarios

## Test Categories

### Data Flow Tests
- Data validation across multiple components
- Series and data integration
- Options and series integration
- Backend to frontend data flow

### Component Integration Tests
- Chart builder with multiple series
- Options integration with different chart types
- Data conversion and serialization chains
- Error handling across components

### Frontend Integration Tests
- JSON serialization compatibility
- Component rendering integration
- Streamlit integration workflows
- Browser compatibility validation

## Running Integration Tests

```bash
# All integration tests
python -m pytest tests/integration/ -v

# Specific integration test
python -m pytest tests/integration/test_data_flow.py -v

# With coverage
python -m pytest tests/integration/ --cov=streamlit_lightweight_charts_pro
```

## Test Patterns

### Data Flow Testing
```python
def test_data_flow_line_series_to_chart():
    """Test complete data flow from LineData to rendered chart."""
    # Create data
    data = LineData(time=timestamps, value=values)
    
    # Create series
    series = LineSeries(data=data)
    
    # Create chart options
    options = ChartOptions(width=800, height=400)
    
    # Verify integration
    chart_config = series.to_dict()
    assert 'data' in chart_config
    assert 'options' in chart_config
```

### Component Integration Testing
```python
def test_multiple_series_integration():
    """Test multiple series working together."""
    # Create multiple series
    line_series = LineSeries(data=line_data)
    area_series = AreaSeries(data=area_data)
    
    # Verify they can be combined
    combined_config = {
        'series': [line_series.to_dict(), area_series.to_dict()]
    }
    assert len(combined_config['series']) == 2
```

## Future Enhancements

- **Performance integration tests**: Large dataset handling
- **Error propagation tests**: Error handling across components
- **Memory leak tests**: Long-running integration scenarios
- **Concurrent access tests**: Multi-threaded usage patterns 