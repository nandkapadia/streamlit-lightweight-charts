# Component Module Tests

This directory contains unit tests for the `component.py` module of Streamlit Lightweight Charts Pro.

## Purpose

Component tests focus on:
- Streamlit component integration
- Chart rendering functionality
- Component configuration
- User interaction handling

## Test Categories

### Component Initialization
- Component creation and setup
- Default configuration handling
- Parameter validation
- Error handling during initialization

### Chart Rendering
- Chart HTML generation
- JavaScript integration
- CSS styling
- Responsive design

### User Interaction
- Event handling
- Callback functions
- State management
- User input validation

### Configuration Management
- Options processing
- Default value handling
- Configuration validation
- Dynamic configuration updates

## Running Component Tests

```bash
# All component tests
python -m pytest tests/component/ -v

# Specific component test
python -m pytest tests/component/test_component.py -v

# With coverage
python -m pytest tests/component/ --cov=streamlit_lightweight_charts_pro.component
```

## Test Patterns

### Component Initialization Testing
```python
def test_component_initialization():
    """Test component initialization and setup."""
    # Test default initialization
    component = StreamlitLightweightCharts()
    assert component is not None
    assert hasattr(component, 'render')
    
    # Test with custom configuration
    config = {'width': 800, 'height': 400}
    component = StreamlitLightweightCharts(**config)
    assert component.width == 800
    assert component.height == 400
```

### Chart Rendering Testing
```python
def test_chart_html_generation(sample_chart_config):
    """Test chart HTML generation."""
    component = StreamlitLightweightCharts()
    
    # Generate HTML
    html = component.generate_html(sample_chart_config)
    
    # Verify HTML structure
    assert '<html>' in html
    assert '<head>' in html
    assert '<body>' in html
    assert 'lightweight-charts' in html
    assert 'chart-container' in html
```

### User Interaction Testing
```python
def test_user_interaction_handling():
    """Test user interaction handling."""
    component = StreamlitLightweightCharts()
    
    # Mock user interaction
    interaction_data = {
        'type': 'click',
        'x': 100,
        'y': 200,
        'series': 'line_series_1'
    }
    
    # Handle interaction
    response = component.handle_interaction(interaction_data)
    
    # Verify response
    assert response is not None
    assert 'status' in response
    assert response['status'] == 'success'
```

### Configuration Management Testing
```python
def test_configuration_validation():
    """Test configuration validation."""
    component = StreamlitLightweightCharts()
    
    # Test valid configuration
    valid_config = {
        'width': 800,
        'height': 400,
        'layout': {'background': {'color': '#ffffff'}}
    }
    assert component.validate_config(valid_config) is True
    
    # Test invalid configuration
    invalid_config = {
        'width': -100,  # Invalid width
        'height': 400
    }
    assert component.validate_config(invalid_config) is False
```

## Mock Testing

### Streamlit Mock
```python
@pytest.fixture
def mock_streamlit():
    """Mock Streamlit for component testing."""
    class MockStreamlit:
        def __init__(self):
            self.components = []
            self.calls = []
        
        def components_v1_html(self, html, **kwargs):
            self.components.append(html)
            self.calls.append(('components_v1_html', kwargs))
            return None
        
        def write(self, data):
            self.calls.append(('write', data))
            return None
    
    return MockStreamlit()

def test_component_rendering_with_mock(mock_streamlit, sample_chart_config):
    """Test component rendering with mocked Streamlit."""
    component = StreamlitLightweightCharts()
    
    # Render chart
    component.render(sample_chart_config, streamlit=mock_streamlit)
    
    # Verify Streamlit was called
    assert len(mock_streamlit.calls) > 0
    assert any(call[0] == 'components_v1_html' for call in mock_streamlit.calls)
```

## Future Enhancements

- **Visual regression testing**: Screenshot comparison for rendered charts
- **Performance testing**: Component rendering performance
- **Accessibility testing**: WCAG compliance verification
- **Cross-browser testing**: Browser compatibility validation 