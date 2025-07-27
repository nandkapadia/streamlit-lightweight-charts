"""
Unit tests for BackgroundSeries class.

This module contains comprehensive unit tests for the BackgroundSeries class,
testing series construction, data handling, serialization, and integration.
"""

import pandas as pd
import pytest
from datetime import datetime

from streamlit_lightweight_charts_pro.charts.series.background import BackgroundSeries
from streamlit_lightweight_charts_pro.data.background_data import BackgroundData
from streamlit_lightweight_charts_pro.type_definitions import ChartType


def create_sample_background_data(n=5):
    """Create sample background data for testing."""
    return [
        BackgroundData(
            time=f"2024-01-{i+1:02d}",
            value=i / (n - 1) if n > 1 else 0.5,
            minColor="#FF0000",
            maxColor="#00FF00"
        )
        for i in range(n)
    ]


class TestBackgroundSeriesConstruction:
    """Test BackgroundSeries construction and initialization."""
    
    def test_basic_construction(self):
        """Test basic BackgroundSeries construction."""
        data = create_sample_background_data()
        series = BackgroundSeries(data=data)
        
        assert isinstance(series, BackgroundSeries)
        assert len(series.data) == 5
        assert series.visible is True
        assert series.price_scale_id == "right"
        assert series.pane_id == 0
        assert series.overlay is True
    
    def test_construction_with_custom_options(self):
        """Test BackgroundSeries construction with custom options."""
        data = create_sample_background_data()
        series = BackgroundSeries(
            data=data,
            visible=False,
            price_scale_id="left",
            pane_id=1,
            overlay=False
        )
        
        assert series.visible is False
        assert series.price_scale_id == "left"
        assert series.pane_id == 1
        assert series.overlay is False
    
    def test_construction_with_empty_data(self):
        """Test BackgroundSeries construction with empty data."""
        series = BackgroundSeries(data=[])
        
        assert len(series.data) == 0
        assert isinstance(series.data, list)
    
    def test_chart_type_property(self):
        """Test chart_type property returns correct type."""
        series = BackgroundSeries(data=create_sample_background_data())
        
        assert series.chart_type == ChartType.BACKGROUND
        assert series.chart_type == "background"


class TestBackgroundSeriesDataHandling:
    """Test BackgroundSeries data handling."""
    
    def test_data_access(self):
        """Test accessing data from series."""
        data = create_sample_background_data()
        series = BackgroundSeries(data=data)
        
        assert len(series.data) == 5
        assert all(isinstance(d, BackgroundData) for d in series.data)
        assert series.data[0].value == 0.0
        assert series.data[-1].value == 1.0
    
    def test_data_dict_property(self):
        """Test data_dict property returns correct format."""
        data = create_sample_background_data(3)
        series = BackgroundSeries(data=data)
        
        data_dict = series.data_dict
        
        assert isinstance(data_dict, list)
        assert len(data_dict) == 3
        assert all("time" in d for d in data_dict)
        assert all("value" in d for d in data_dict)
        assert all("minColor" in d for d in data_dict)
        assert all("maxColor" in d for d in data_dict)


class TestBackgroundSeriesDataFrame:
    """Test BackgroundSeries DataFrame integration."""
    
    def test_construction_from_dataframe(self):
        """Test BackgroundSeries construction from DataFrame."""
        df = pd.DataFrame({
            "time": pd.date_range("2024-01-01", periods=5, freq="D"),
            "value": [0.2, 0.4, 0.6, 0.8, 1.0],
            "minColor": ["#FF0000"] * 5,
            "maxColor": ["#00FF00"] * 5
        })
        
        series = BackgroundSeries(
            data=df,
            column_mapping={
                "time": "time",
                "value": "value",
                "minColor": "minColor",
                "maxColor": "maxColor"
            }
        )
        
        assert len(series.data) == 5
        assert all(isinstance(d, BackgroundData) for d in series.data)
        assert series.data[0].value == 0.2
        assert series.data[-1].value == 1.0
    
    def test_from_dataframe_class_method(self):
        """Test from_dataframe class method."""
        df = pd.DataFrame({
            "timestamp": pd.date_range("2024-01-01", periods=3, freq="H"),
            "indicator": [0.3, 0.5, 0.7],
            "min_col": ["#FF0000"] * 3,
            "max_col": ["#00FF00"] * 3
        })
        
        series = BackgroundSeries.from_dataframe(
            df=df,
            column_mapping={
                "time": "timestamp",
                "value": "indicator",
                "minColor": "min_col",
                "maxColor": "max_col"
            }
        )
        
        assert len(series.data) == 3
        assert series.data[0].value == 0.3
        assert series.data[1].value == 0.5
        assert series.data[2].value == 0.7


class TestBackgroundSeriesSerialization:
    """Test BackgroundSeries serialization."""
    
    def test_to_dict_basic(self):
        """Test basic to_dict conversion."""
        data = create_sample_background_data(2)
        series = BackgroundSeries(data=data)
        
        result = series.to_dict()
        
        assert result["type"] == "Background"
        assert "data" in result
        assert "options" in result
        assert len(result["data"]) == 2
    
    def test_to_dict_options(self):
        """Test to_dict includes correct options."""
        series = BackgroundSeries(
            data=create_sample_background_data(),
            visible=False,
            price_scale_id="left",
            pane_id=2,
            overlay=False
        )
        
        result = series.to_dict()
        options = result["options"]
        
        assert options["visible"] is False
        assert options["priceScaleId"] == "left"
        assert options["paneId"] == 2
        assert options["overlay"] is False
    
    def test_to_dict_with_price_format(self):
        """Test to_dict with price format."""
        from streamlit_lightweight_charts_pro.charts.options.price_format_options import (
            PriceFormatOptions
        )
        
        series = BackgroundSeries(data=create_sample_background_data())
        series.set_price_format(PriceFormatOptions(precision=4))
        
        result = series.to_dict()
        
        assert "priceFormat" in result["options"]
        assert result["options"]["priceFormat"]["precision"] == 4


class TestBackgroundSeriesIntegration:
    """Test BackgroundSeries integration scenarios."""
    
    def test_integration_with_chart(self):
        """Test BackgroundSeries integration with Chart."""
        from streamlit_lightweight_charts_pro.charts import Chart
        
        # Create background series
        background_data = create_sample_background_data()
        background_series = BackgroundSeries(data=background_data)
        
        # Create chart with background series
        chart = Chart(series=[background_series])
        
        assert len(chart.series) == 1
        assert chart.series[0] == background_series
    
    def test_multiple_background_series(self):
        """Test multiple background series in different panes."""
        # Create two background series for different indicators
        rsi_series = BackgroundSeries(
            data=[
                BackgroundData("2024-01-01", 0.3, "#FFE5E5", "#E5FFE5"),
                BackgroundData("2024-01-02", 0.7, "#FFE5E5", "#E5FFE5"),
            ],
            pane_id=0
        )
        
        macd_series = BackgroundSeries(
            data=[
                BackgroundData("2024-01-01", 0.4, "#E5E5FF", "#FFE5E5"),
                BackgroundData("2024-01-02", 0.6, "#E5E5FF", "#FFE5E5"),
            ],
            pane_id=1
        )
        
        assert rsi_series.pane_id == 0
        assert macd_series.pane_id == 1
        assert rsi_series.data[0].minColor != macd_series.data[0].minColor


class TestBackgroundSeriesEdgeCases:
    """Test BackgroundSeries edge cases."""
    
    def test_series_with_single_data_point(self):
        """Test BackgroundSeries with single data point."""
        data = [BackgroundData("2024-01-01", 0.5)]
        series = BackgroundSeries(data=data)
        
        assert len(series.data) == 1
        assert series.data[0].value == 0.5
    
    def test_series_with_nan_values(self):
        """Test BackgroundSeries with NaN values."""
        import numpy as np
        
        data = [
            BackgroundData("2024-01-01", np.nan),
            BackgroundData("2024-01-02", 0.5),
        ]
        series = BackgroundSeries(data=data)
        
        # NaN should be converted to 0.0
        assert series.data[0].value == 0.0
        assert series.data[1].value == 0.5
    
    def test_series_with_extreme_values(self):
        """Test BackgroundSeries with extreme values."""
        data = [
            BackgroundData("2024-01-01", -1000),
            BackgroundData("2024-01-02", 1000),
            BackgroundData("2024-01-03", float('inf')),
        ]
        series = BackgroundSeries(data=data)
        
        assert series.data[0].value == -1000
        assert series.data[1].value == 1000
        assert series.data[2].value == float('inf')
    
    def test_series_visibility_toggle(self):
        """Test toggling series visibility."""
        series = BackgroundSeries(data=create_sample_background_data())
        
        # Initially visible
        assert series.visible is True
        
        # Hide series
        series.set_visible(False)
        assert series.visible is False
        
        # Show series
        series.set_visible(True)
        assert series.visible is True