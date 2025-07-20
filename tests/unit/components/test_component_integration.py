"""Tests for Streamlit component integration."""

import pytest
import pandas as pd
from unittest.mock import Mock, patch, MagicMock
import streamlit as st

from streamlit_lightweight_charts_pro.component import get_component_func
from streamlit_lightweight_charts_pro.charts.single_pane_chart import SinglePaneChart
from streamlit_lightweight_charts_pro.charts.series import LineSeries, CandlestickSeries
from streamlit_lightweight_charts_pro.data import (
    SingleValueData, OhlcData, create_text_annotation
)


class TestComponentIntegration:
    """Test Streamlit component integration functionality."""

    def setup_method(self):
        """Set up test data."""
        self.sample_data = [
            SingleValueData("2024-01-01", 100),
            SingleValueData("2024-01-02", 105),
            SingleValueData("2024-01-03", 110),
        ]
        
        self.ohlc_data = [
            OhlcData("2024-01-01", 100, 105, 98, 103),
            OhlcData("2024-01-02", 103, 108, 102, 106),
            OhlcData("2024-01-03", 106, 112, 104, 110),
        ]
        
        self.line_series = LineSeries(self.sample_data, color="#ff0000")
        self.candlestick_series = CandlestickSeries(self.ohlc_data)

    def test_get_component_func_returns_function(self):
        """Test that get_component_func returns a callable function."""
        component_func = get_component_func()
        
        # The function should either be None (if not available) or a callable
        assert component_func is None or callable(component_func)

    def test_component_rendering_basic(self):
        """Test basic chart rendering configuration."""
        chart = SinglePaneChart(series=self.line_series)
        config = chart.to_frontend_config()
        
        # Test that configuration is properly structured
        assert "charts" in config
        assert "syncConfig" in config
        assert len(config["charts"]) == 1
        
        chart_config = config["charts"][0]
        assert "chartId" in chart_config
        assert "chart" in chart_config
        assert "series" in chart_config
        assert "annotations" in chart_config

    def test_component_rendering_with_height_width(self):
        """Test chart rendering with custom height and width."""
        chart = SinglePaneChart(series=self.line_series)
        chart.update_options(height=600, width=800)
        config = chart.to_frontend_config()
        
        # Test that options are properly set
        chart_options = config["charts"][0]["chart"]
        assert chart_options["height"] == 600
        assert chart_options["width"] == 800

    def test_component_rendering_with_annotations(self):
        """Test chart rendering with annotations."""
        chart = SinglePaneChart(series=self.line_series)
        annotation = create_text_annotation("2024-01-01", 100, "Test")
        chart.add_annotation(annotation)
        config = chart.to_frontend_config()
        
        # Test that annotations are properly included
        annotations = config["charts"][0]["annotations"]
        assert len(annotations) == 1
        assert annotations[0]["name"] == "default"

    def test_component_rendering_multiple_series(self):
        """Test chart rendering with multiple series."""
        chart = SinglePaneChart(series=[self.line_series, self.candlestick_series])
        config = chart.to_frontend_config()
        
        # Test that multiple series are properly included
        series = config["charts"][0]["series"]
        assert len(series) == 2
        assert series[0]["type"] == "line"
        assert series[1]["type"] == "candlestick"

    def test_component_rendering_with_custom_options(self):
        """Test chart rendering with custom chart options."""
        chart = SinglePaneChart(series=self.line_series)
        chart.update_options(height=500, width=700, auto_size=True)
        config = chart.to_frontend_config()
        
        # Test that custom options are properly set
        chart_options = config["charts"][0]["chart"]
        assert chart_options["height"] == 500
        assert chart_options["width"] == 700
        assert chart_options["autoSize"] is True

    def test_component_rendering_with_dataframe_series(self):
        """Test chart rendering with DataFrame series."""
        df = pd.DataFrame({
            'datetime': ['2024-01-01', '2024-01-02', '2024-01-03'],
            'close': [100, 105, 110]
        })
        
        series = LineSeries(df, color="#ff0000")
        chart = SinglePaneChart(series=series)
        config = chart.to_frontend_config()
        
        # Test that DataFrame series is properly processed
        assert "charts" in config
        assert len(config["charts"]) == 1
        assert len(config["charts"][0]["series"]) == 1

    def test_component_rendering_error_handling(self):
        """Test chart rendering error handling."""
        # Test with empty series
        chart = SinglePaneChart(series=[])
        config = chart.to_frontend_config()
        
        # Should handle empty series gracefully
        assert "charts" in config
        assert len(config["charts"]) == 1
        assert len(config["charts"][0]["series"]) == 0

    def test_component_rendering_large_dataset(self):
        """Test chart rendering with large dataset."""
        large_data = [SingleValueData(f"2024-01-{i:02d}", 100 + i) for i in range(1, 1001)]
        large_series = LineSeries(large_data, color="#ff0000")
        chart = SinglePaneChart(series=large_series)
        config = chart.to_frontend_config()
        
        # Test that large dataset is properly processed
        assert "charts" in config
        assert len(config["charts"]) == 1
        series_data = config["charts"][0]["series"][0]["data"]
        assert len(series_data) == 1000

    def test_component_rendering_complex_configuration(self):
        """Test chart rendering with complex configuration."""
        chart = (SinglePaneChart(series=self.line_series)
                .add_series(self.candlestick_series)
                .update_options(height=600, width=800, auto_size=True)
                .add_annotation(create_text_annotation("2024-01-01", 100, "Start")))
        
        config = chart.to_frontend_config()
        
        # Test complex configuration
        assert "charts" in config
        assert len(config["charts"]) == 1
        
        chart_config = config["charts"][0]
        assert len(chart_config["series"]) == 2
        assert len(chart_config["annotations"]) == 1
        
        chart_options = chart_config["chart"]
        assert chart_options["height"] == 600
        assert chart_options["width"] == 800
        assert chart_options["autoSize"] is True

    def test_component_rendering_with_empty_series(self):
        """Test chart rendering with empty series."""
        chart = SinglePaneChart(series=[])
        config = chart.to_frontend_config()
        
        # Should handle empty series gracefully
        assert "charts" in config
        assert len(config["charts"]) == 1
        assert len(config["charts"][0]["series"]) == 0

    def test_component_rendering_performance(self):
        """Test chart rendering performance."""
        import time
        
        chart = SinglePaneChart(series=self.line_series)
        
        start_time = time.time()
        config = chart.to_frontend_config()
        end_time = time.time()
        
        # Should complete within reasonable time
        assert end_time - start_time < 1.0
        assert "charts" in config

    def test_component_rendering_memory_usage(self):
        """Test chart rendering memory usage."""
        import gc
        import psutil
        
        process = psutil.Process()
        initial_memory = process.memory_info().rss
        
        chart = SinglePaneChart(series=self.line_series)
        config = chart.to_frontend_config()
        
        # Force garbage collection
        gc.collect()
        final_memory = process.memory_info().rss
        
        # Memory usage should be reasonable
        memory_increase = final_memory - initial_memory
        assert memory_increase < 50 * 1024 * 1024  # Less than 50MB increase

    def test_component_rendering_with_special_characters(self):
        """Test chart rendering with special characters in data."""
        special_data = [
            SingleValueData("2024-01-01", 100),
            SingleValueData("2024-01-02", 105),
        ]
        
        chart = SinglePaneChart(series=LineSeries(special_data))
        annotation = create_text_annotation("2024-01-01", 100, "Test & Special < > \" ' Characters")
        chart.add_annotation(annotation)
        config = chart.to_frontend_config()
        
        # Test that special characters are handled properly
        assert "charts" in config
        assert len(config["charts"]) == 1
        assert len(config["charts"][0]["annotations"]) == 1

    def test_component_rendering_workflow_integration(self):
        """Test complete integration workflow."""
        # Create complex chart
        chart = (SinglePaneChart(series=self.line_series)
                .add_series(self.candlestick_series)
                .update_options(height=600, width=800, auto_size=True)
                .add_annotation(create_text_annotation("2024-01-01", 100, "Start"))
                .add_annotation(create_text_annotation("2024-01-03", 110, "End")))
        
        # Generate configuration
        config = chart.to_frontend_config()
        
        # Verify configuration structure
        assert "charts" in config
        assert "syncConfig" in config
        assert len(config["charts"]) == 1
        
        chart_config = config["charts"][0]
        assert "chartId" in chart_config
        assert "chart" in chart_config
        assert "series" in chart_config
        assert "annotations" in chart_config
        
        # Verify series
        assert len(chart_config["series"]) == 2
        assert chart_config["series"][0]["type"] == "line"
        assert chart_config["series"][1]["type"] == "candlestick"
        
        # Verify annotations
        assert len(chart_config["annotations"]) == 1
        
        # Verify chart options
        chart_options = chart_config["chart"]
        assert chart_options["height"] == 600
        assert chart_options["width"] == 800
        assert chart_options["autoSize"] is True
        
        # Verify sync config
        sync_config = config["syncConfig"]
        assert sync_config["enabled"] is False 