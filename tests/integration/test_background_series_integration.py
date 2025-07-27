"""
Integration tests for BackgroundSeries.

This module contains integration tests for the BackgroundSeries class,
testing its interaction with other components like Chart, DataFrame pipelines,
and frontend configuration.
"""

import json
import pandas as pd
import numpy as np
import pytest

from streamlit_lightweight_charts_pro.charts import Chart
from streamlit_lightweight_charts_pro.charts.series import BackgroundSeries, LineSeries
from streamlit_lightweight_charts_pro.charts.options.line_options import LineOptions
from streamlit_lightweight_charts_pro.data import BackgroundData, LineData


def create_rsi_background_data(n=10):
    """Create RSI-based background data for testing."""
    # Simulate RSI values
    rsi_values = np.sin(np.linspace(0, 2 * np.pi, n)) * 0.3 + 0.5
    
    return [
        BackgroundData(
            time=f"2024-01-{i+1:02d}",
            value=float(rsi_values[i]),
            minColor="#FFE5E5",  # Light red for oversold
            maxColor="#E5FFE5"   # Light green for overbought
        )
        for i in range(n)
    ]


def create_price_data(n=10):
    """Create price data for testing."""
    base_price = 100
    prices = base_price + np.cumsum(np.random.randn(n) * 2)
    
    return [
        LineData(
            time=f"2024-01-{i+1:02d}",
            value=float(prices[i])
        )
        for i in range(n)
    ]


class TestBackgroundSeriesChartIntegration:
    """Test BackgroundSeries integration with Chart."""
    
    def test_chart_with_background_and_line_series(self):
        """Test chart with background series and line series."""
        # Create background series for RSI
        background_data = create_rsi_background_data()
        background_series = BackgroundSeries(data=background_data)
        
        # Create line series for price
        price_data = create_price_data()
        line_series = LineSeries(
            data=price_data,
            line_options=LineOptions(color="#2196F3")
        )
        
        # Create chart with both series
        chart = Chart(series=[background_series, line_series])
        
        assert len(chart.series) == 2
        assert isinstance(chart.series[0], BackgroundSeries)
        assert isinstance(chart.series[1], LineSeries)
        
        # Check frontend config
        config = chart.to_frontend_config()
        assert len(config["charts"][0]["series"]) == 2
        
        # Verify background series is first (rendered behind)
        assert config["charts"][0]["series"][0]["type"] == "Background"
        assert config["charts"][0]["series"][1]["type"] == "Line"
    
    def test_multiple_pane_background_series(self):
        """Test background series in multiple panes."""
        # Main price pane with background
        price_background = BackgroundSeries(
            data=create_rsi_background_data(),
            pane_id=0
        )
        
        price_line = LineSeries(
            data=create_price_data(),
            line_options=LineOptions(),
            pane_id=0
        )
        
        # Indicator pane with background
        indicator_background = BackgroundSeries(
            data=[
                BackgroundData("2024-01-01", 0.2, "#E5E5FF", "#FFE5E5"),
                BackgroundData("2024-01-02", 0.8, "#E5E5FF", "#FFE5E5"),
            ],
            pane_id=1
        )
        
        indicator_line = LineSeries(
            data=[
                LineData("2024-01-01", 50),
                LineData("2024-01-02", 60),
            ],
            line_options=LineOptions(color="#FF5722"),
            pane_id=1
        )
        
        # Create chart
        chart = Chart(series=[
            price_background,
            price_line,
            indicator_background,
            indicator_line
        ])
        
        assert len(chart.series) == 4
        
        # Check frontend config
        config = chart.to_frontend_config()
        series_configs = config["charts"][0]["series"]
        
        # Verify pane assignments
        assert series_configs[0]["options"]["paneId"] == 0
        assert series_configs[1]["options"]["paneId"] == 0
        assert series_configs[2]["options"]["paneId"] == 1
        assert series_configs[3]["options"]["paneId"] == 1


class TestBackgroundSeriesDataFrameIntegration:
    """Test BackgroundSeries DataFrame integration."""
    
    def test_dataframe_to_background_series_pipeline(self):
        """Test complete DataFrame to BackgroundSeries pipeline."""
        # Create DataFrame with indicator data
        df = pd.DataFrame({
            "date": pd.date_range("2024-01-01", periods=20, freq="D"),
            "rsi": np.sin(np.linspace(0, 4 * np.pi, 20)) * 30 + 50,
        })
        
        # Normalize RSI to 0-1 range
        df["rsi_normalized"] = (df["rsi"] - 30) / 40  # 30-70 range to 0-1
        
        # Add color columns
        df["min_color"] = "#FFE5E5"
        df["max_color"] = "#E5FFE5"
        
        # Create series from DataFrame
        series = BackgroundSeries.from_dataframe(
            df=df,
            column_mapping={
                "time": "date",
                "value": "rsi_normalized",
                "minColor": "min_color",
                "maxColor": "max_color"
            }
        )
        
        assert len(series.data) == 20
        assert all(isinstance(d, BackgroundData) for d in series.data)
        
        # Verify data integrity
        assert series.data[0].minColor == "#FFE5E5"
        assert series.data[0].maxColor == "#E5FFE5"
        
        # Create chart
        chart = Chart(series=[series])
        config = chart.to_frontend_config()
        
        # Verify JSON serialization
        json_str = json.dumps(config)
        assert len(json_str) > 0
    
    def test_mixed_dataframe_sources(self):
        """Test creating chart from mixed DataFrame sources."""
        # Price data DataFrame
        price_df = pd.DataFrame({
            "timestamp": pd.date_range("2024-01-01", periods=10, freq="H"),
            "price": 100 + np.cumsum(np.random.randn(10) * 2)
        })
        
        # Background data DataFrame
        background_df = pd.DataFrame({
            "timestamp": pd.date_range("2024-01-01", periods=10, freq="H"),
            "sentiment": np.random.uniform(0, 1, 10),
            "bearish_color": ["#FFE5E5"] * 10,
            "bullish_color": ["#E5FFE5"] * 10
        })
        
        # Create series
        line_series = LineSeries.from_dataframe(
            df=price_df,
            column_mapping={"time": "timestamp", "value": "price"},
            line_options=LineOptions()
        )
        
        background_series = BackgroundSeries.from_dataframe(
            df=background_df,
            column_mapping={
                "time": "timestamp",
                "value": "sentiment",
                "minColor": "bearish_color",
                "maxColor": "bullish_color"
            }
        )
        
        # Create chart
        chart = Chart(series=[background_series, line_series])
        
        assert len(chart.series) == 2
        assert chart.series[0].data[0].value == background_df["sentiment"].iloc[0]
        assert chart.series[1].data[0].value == price_df["price"].iloc[0]


class TestBackgroundSeriesFrontendConfig:
    """Test BackgroundSeries frontend configuration."""
    
    def test_frontend_config_structure(self):
        """Test that frontend config has correct structure."""
        series = BackgroundSeries(
            data=create_rsi_background_data(5),
            visible=True,
            price_scale_id="right",
            pane_id=0,
            overlay=True
        )
        
        config = series.to_dict()
        
        # Check top-level structure
        assert config["type"] == "Background"
        assert "data" in config
        assert "options" in config
        
        # Check data structure
        assert len(config["data"]) == 5
        for data_point in config["data"]:
            assert "time" in data_point
            assert "value" in data_point
            assert "minColor" in data_point
            assert "maxColor" in data_point
        
        # Check options structure
        options = config["options"]
        assert options["visible"] is True
        assert options["priceScaleId"] == "right"
        assert options["paneId"] == 0
        assert options["overlay"] is True
    
    def test_chart_config_with_background_series(self):
        """Test complete chart config with background series."""
        # Create complex chart
        background = BackgroundSeries(data=create_rsi_background_data())
        line = LineSeries(
            data=create_price_data(),
            line_options=LineOptions()
        )
        
        chart = Chart(series=[background, line])
        config = chart.to_frontend_config()
        
        # Verify chart structure
        assert "charts" in config
        assert len(config["charts"]) == 1
        
        chart_config = config["charts"][0]
        assert "series" in chart_config
        assert len(chart_config["series"]) == 2
        
        # Verify series order (background should be first)
        assert chart_config["series"][0]["type"] == "Background"
        assert chart_config["series"][1]["type"] == "Line"
        
        # Test JSON serialization
        json_str = json.dumps(config)
        parsed = json.loads(json_str)
        assert parsed == config


class TestBackgroundSeriesPerformance:
    """Test BackgroundSeries performance with large datasets."""
    
    def test_large_dataset_performance(self):
        """Test BackgroundSeries with large dataset."""
        # Create large dataset (10k points)
        n = 10000
        data = []
        
        for i in range(n):
            data.append(
                BackgroundData(
                    time=1640995200 + i * 60,  # 1 minute intervals
                    value=np.sin(i / 100) * 0.5 + 0.5,
                    minColor="#FF0000",
                    maxColor="#00FF00"
                )
            )
        
        # Create series
        import time
        start_time = time.time()
        
        series = BackgroundSeries(data=data)
        
        creation_time = time.time() - start_time
        
        # Test serialization performance
        start_time = time.time()
        
        config = series.to_dict()
        
        serialization_time = time.time() - start_time
        
        # Assertions
        assert len(series.data) == n
        assert creation_time < 1.0  # Should create in less than 1 second
        assert serialization_time < 1.0  # Should serialize in less than 1 second
        assert len(config["data"]) == n
    
    def test_memory_efficiency(self):
        """Test memory efficiency of BackgroundSeries."""
        import psutil
        import gc
        
        # Force garbage collection
        gc.collect()
        
        # Get initial memory
        process = psutil.Process()
        initial_memory = process.memory_info().rss
        
        # Create large dataset
        n = 50000
        data = [
            BackgroundData(
                time=1640995200 + i * 60,
                value=i / n,
                minColor="#FF0000",
                maxColor="#00FF00"
            )
            for i in range(n)
        ]
        
        series = BackgroundSeries(data=data)
        
        # Get memory after creation
        memory_after = process.memory_info().rss
        memory_increase = (memory_after - initial_memory) / 1024 / 1024  # MB
        
        # Clean up
        del series
        del data
        gc.collect()
        
        # Memory increase should be reasonable
        assert memory_increase < 500  # Less than 500MB for 50k points