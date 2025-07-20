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

from unittest.mock import MagicMock, patch

from streamlit_lightweight_charts_pro import LineSeries, SinglePaneChart, SingleValueData


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
    # Create test data and series
    series = LineSeries([SingleValueData("2023-01-01", 1.0)], color="#ff0000")
    chart = SinglePaneChart(series)

    # Test the configuration generation first (this doesn't require mocking)
    config = chart.to_frontend_config()

    # Verify the configuration structure
    assert "charts" in config
    assert len(config["charts"]) == 1

    chart_config = config["charts"][0]
    assert "series" in chart_config
    assert isinstance(chart_config["series"], list)
    # The actual implementation uses lowercase "line", not "Line"
    assert chart_config["series"][0]["type"] == "line"

    # Test the render method with proper mocking
    mock_component = MagicMock()
    mock_component.return_value = {"config": "test_config", "key": "test_key"}

    # Mock the component function at the module level
    with patch("streamlit_lightweight_charts_pro.component._component_func", mock_component):
        # Render the chart (this should use our mocked component)
        result = chart.render(key="test_chart")

        # Verify the component function was called with the correct arguments
        mock_component.assert_called_once()
        call_args = mock_component.call_args
        assert call_args is not None

        # Check that the component was called with config and key
        kwargs = call_args.kwargs
        assert "config" in kwargs
        assert "key" in kwargs
        assert kwargs["key"] == "test_chart"

        # Verify the result contains the expected structure
        assert result is not None
        assert result["config"] == "test_config"
        assert result["key"] == "test_key"

        # Verify the actual config structure passed to the component
        actual_config = kwargs["config"]
        assert "charts" in actual_config
        assert len(actual_config["charts"]) == 1

        actual_chart_config = actual_config["charts"][0]
        assert "series" in actual_chart_config
        assert isinstance(actual_chart_config["series"], list)
        assert actual_chart_config["series"][0]["type"] == "line"
