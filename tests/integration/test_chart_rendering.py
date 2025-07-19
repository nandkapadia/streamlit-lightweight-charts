"""
Integration tests for chart rendering functionality.

This module contains integration tests that verify the chart rendering
system works correctly with the Streamlit component. These tests ensure
that charts can be properly serialized and rendered in a Streamlit
application environment.

The tests focus on:
    - Chart configuration serialization
    - Series data conversion
    - Frontend configuration generation
    - Component integration
"""

from unittest.mock import patch

from streamlit_lightweight_charts_pro import SinglePaneChart, LineSeries, SingleValueData


def test_render_chart_serialization():
    """
    Test chart rendering with BaseChart.render() method.
    
    This test verifies that the chart rendering system correctly:
        1. Creates a chart with series data
        2. Serializes the chart configuration
        3. Passes the configuration to the Streamlit component
        4. Returns the expected result structure
        
    The test mocks the component function to avoid actual Streamlit
    rendering while still testing the complete configuration flow.
    
    Test Coverage:
        - Chart initialization with series
        - Configuration serialization
        - Component function integration
        - Result structure validation
        
    Example:
        ```python
        # This test ensures the chart rendering pipeline works correctly
        series = LineSeries([SingleValueData("2023-01-01", 1.0)], color="#ff0000")
        chart = SinglePaneChart(series)
        result = chart.render()
        assert result is not None
        ```
    """
    # Mock the component function to return a dict with the config
    def mock_component_func(config=None, key=None):
        """
        Mock component function for testing.
        
        This function simulates the behavior of the actual Streamlit
        component function, returning a dictionary that contains the
        configuration and key passed to it.
        
        Args:
            config: Chart configuration dictionary
            key: Optional component key
            
        Returns:
            dict: Dictionary containing the config and key for verification
        """
        return {"config": config, "key": key}
    
    # Test the chart rendering with mocked component
    with patch(
        "streamlit_lightweight_charts_pro.component.get_component_func"
    ) as mock_get_component:
        # Configure the mock to return our test function
        mock_get_component.return_value = mock_component_func
        
        # Create test data and series
        series = LineSeries([SingleValueData("2023-01-01", 1.0)], color="#ff0000")
        chart = SinglePaneChart(series)
        
        # Render the chart (this should use our mocked component)
        result = chart.render()
        
        # Verify the result contains the expected structure
        assert result is not None
        assert "config" in result
        assert "series" in result["config"]
        assert isinstance(result["config"]["series"], list)
        assert result["config"]["series"][0]["type"] == "Line"
