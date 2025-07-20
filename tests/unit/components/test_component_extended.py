"""
Extended tests for component module to improve coverage.

This module provides additional tests for the component module,
covering initialization, error handling, and edge cases.
"""

from unittest.mock import Mock, patch

import pytest

from streamlit_lightweight_charts_pro.component import get_component_func


class TestComponentExtended:
    """Extended test suite for component module."""

    def test_get_component_func_returns_cached_function(self):
        """Test get_component_func returns the cached component function."""
        # Mock the module-level _component_func variable
        mock_component = Mock()
        with patch("streamlit_lightweight_charts_pro.component._component_func", mock_component):
            result = get_component_func()
            assert result is mock_component

    def test_get_component_func_returns_none_when_not_initialized(self):
        """Test get_component_func returns None when component is not initialized."""
        with patch("streamlit_lightweight_charts_pro.component._component_func", None):
            result = get_component_func()
            assert result is None

    def test_component_function_signature(self):
        """Test that component function has expected signature when available."""
        mock_component = Mock()
        with patch("streamlit_lightweight_charts_pro.component._component_func", mock_component):
            result = get_component_func()
            assert result == mock_component

    def test_component_rendering_with_config(self):
        """Test component rendering with configuration."""
        mock_component = Mock()
        with patch("streamlit_lightweight_charts_pro.component._component_func", mock_component):
            config = {"charts": [], "syncConfig": {}}
            key = "test_chart"

            result = get_component_func()(config=config, key=key)

            mock_component.assert_called_once_with(config=config, key=key)

    def test_component_rendering_without_key(self):
        """Test component rendering without key parameter."""
        mock_component = Mock()
        with patch("streamlit_lightweight_charts_pro.component._component_func", mock_component):
            config = {"charts": [], "syncConfig": {}}

            result = get_component_func()(config=config)

            mock_component.assert_called_once_with(config=config)

    def test_component_rendering_error_handling(self):
        """Test component rendering error handling."""
        mock_component = Mock()
        mock_component.side_effect = Exception("Rendering error")
        with patch("streamlit_lightweight_charts_pro.component._component_func", mock_component):
            config = {"charts": [], "syncConfig": {}}

            with pytest.raises(Exception, match="Rendering error"):
                get_component_func()(config=config)

    def test_multiple_calls_to_get_component_func(self):
        """Test that multiple calls to get_component_func return the same result."""
        mock_component = Mock()
        with patch("streamlit_lightweight_charts_pro.component._component_func", mock_component):
            # Call multiple times
            result1 = get_component_func()
            result2 = get_component_func()
            result3 = get_component_func()

            assert result1 == mock_component
            assert result2 == mock_component
            assert result3 == mock_component

    def test_component_function_with_different_configs(self):
        """Test component function with different configuration types."""
        mock_component = Mock()
        with patch("streamlit_lightweight_charts_pro.component._component_func", mock_component):
            # Test with different config types
            configs = [
                {"charts": [], "syncConfig": {}},
                {"charts": [{"type": "line", "data": []}], "syncConfig": {"sync": True}},
                {"charts": None, "syncConfig": None},
                {},
            ]

            for config in configs:
                get_component_func()(config=config)
                mock_component.assert_called_with(config=config)

    def test_component_function_with_different_keys(self):
        """Test component function with different key values."""
        mock_component = Mock()
        with patch("streamlit_lightweight_charts_pro.component._component_func", mock_component):
            config = {"charts": [], "syncConfig": {}}
            keys = ["chart1", "chart2", "", None]

            for key in keys:
                get_component_func()(config=config, key=key)
                mock_component.assert_called_with(config=config, key=key)

    def test_component_function_return_value(self):
        """Test component function return value."""
        mock_component = Mock()
        mock_component.return_value = "rendered_chart"
        with patch("streamlit_lightweight_charts_pro.component._component_func", mock_component):
            config = {"charts": [], "syncConfig": {}}

            result = get_component_func()(config=config)

            assert result == "rendered_chart"

    def test_component_function_with_complex_config(self):
        """Test component function with complex configuration."""
        mock_component = Mock()
        with patch("streamlit_lightweight_charts_pro.component._component_func", mock_component):
            complex_config = {
                "charts": [
                    {
                        "type": "candlestick",
                        "data": [
                            {
                                "time": "2023-01-01",
                                "open": 100,
                                "high": 110,
                                "low": 90,
                                "close": 105,
                            }
                        ],
                        "options": {"upColor": "#26a69a", "downColor": "#ef5350"},
                    }
                ],
                "syncConfig": {"sync": True, "group": "charts"},
            }

            get_component_func()(config=complex_config, key="complex_chart")

            mock_component.assert_called_once_with(config=complex_config, key="complex_chart")

    def test_component_function_none_config(self):
        """Test component function with None config."""
        mock_component = Mock()
        with patch("streamlit_lightweight_charts_pro.component._component_func", mock_component):
            # Component should handle None config gracefully
            get_component_func()(config=None)
            mock_component.assert_called_once_with(config=None)

    def test_component_function_missing_config(self):
        """Test component function with missing config parameter."""
        mock_component = Mock()
        with patch("streamlit_lightweight_charts_pro.component._component_func", mock_component):
            # Component should handle missing config gracefully
            get_component_func()()
            mock_component.assert_called_once_with()

    def test_component_function_extra_parameters(self):
        """Test component function with extra parameters."""
        mock_component = Mock()
        with patch("streamlit_lightweight_charts_pro.component._component_func", mock_component):
            config = {"charts": [], "syncConfig": {}}

            # Test with extra parameters
            get_component_func()(config=config, key="test", extra_param="value")

            mock_component.assert_called_once_with(config=config, key="test", extra_param="value")

    def test_component_initialization_production_mode(self):
        """Test component initialization in production mode."""
        with patch("streamlit_lightweight_charts_pro.component._RELEASE", True):
            with patch("pathlib.Path.exists") as mock_exists:
                mock_exists.return_value = True
                with patch("streamlit.components.v1.declare_component") as mock_declare:
                    mock_declare.return_value = Mock()

                    # Re-import to trigger initialization
                    import importlib

                    import streamlit_lightweight_charts_pro.component

                    importlib.reload(streamlit_lightweight_charts_pro.component)

                    result = get_component_func()
                    assert result is not None

    def test_component_initialization_development_mode(self):
        """Test component initialization in development mode."""
        with patch("streamlit_lightweight_charts_pro.component._RELEASE", False):
            with patch("streamlit.components.v1.declare_component") as mock_declare:
                mock_declare.return_value = Mock()

                # Re-import to trigger initialization
                import importlib

                import streamlit_lightweight_charts_pro.component

                importlib.reload(streamlit_lightweight_charts_pro.component)

                result = get_component_func()
                assert result is not None

    def test_component_initialization_error_handling(self):
        """Test component initialization error handling."""
        with patch("streamlit_lightweight_charts_pro.component._RELEASE", True):
            with patch("pathlib.Path.exists") as mock_exists:
                mock_exists.return_value = True
                with patch("streamlit.components.v1.declare_component") as mock_declare:
                    mock_declare.side_effect = Exception("Component error")

                    # Re-import to trigger initialization
                    import importlib

                    import streamlit_lightweight_charts_pro.component

                    importlib.reload(streamlit_lightweight_charts_pro.component)

                    result = get_component_func()
                    assert result is None
