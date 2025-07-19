"""
End-to-end tests for PriceVolumeChart class.
"""

import pytest
import pandas as pd
import numpy as np
import streamlit as st
from unittest.mock import patch, MagicMock
import time

from streamlit_lightweight_charts_pro.charts.price_volume_chart import PriceVolumeChart


class TestPriceVolumeChartE2E:
    """End-to-end test cases for PriceVolumeChart class."""

    def setup_method(self):
        """Set up test data."""
        # Create realistic market data
        dates = pd.date_range("2022-01-01", periods=50, freq="D")
        np.random.seed(42)

        # Generate realistic price data with trends
        base_price = 100.0
        trend = 0.001  # Slight upward trend
        volatility = 0.02

        prices = [base_price]
        for i in range(1, 50):
            # Add trend and random walk
            change = trend + np.random.normal(0, volatility)
            new_price = prices[-1] * (1 + change)
            prices.append(max(new_price, 1.0))  # Ensure positive prices

        # Create OHLCV data with realistic patterns
        self.ohlcv_df = pd.DataFrame(
            {
                "datetime": dates,
                "open": prices,
                "high": [p * (1 + abs(np.random.normal(0, 0.015))) for p in prices],
                "low": [p * (1 - abs(np.random.normal(0, 0.015))) for p in prices],
                "close": [p * (1 + np.random.normal(0, 0.01)) for p in prices],
                "volume": np.random.randint(1000, 50000, 50),
            }
        )

        # Ensure OHLC consistency
        self.ohlcv_df["high"] = self.ohlcv_df[["open", "close", "high"]].max(axis=1)
        self.ohlcv_df["low"] = self.ohlcv_df[["open", "close", "low"]].min(axis=1)

    def test_complete_workflow_e2e(self):
        """Test complete workflow from data to rendered chart."""
        # Step 1: Create chart
        chart = PriceVolumeChart(
            data=self.ohlcv_df,
            up_color="#4CAF50",
            down_color="#F44336",
            volume_color="#26a69a",
            volume_alpha=0.8,
            height=400,
        )

        # Step 2: Verify chart structure
        assert chart.has_volume() is True
        assert len(chart.series) == 2

        # Step 3: Generate frontend configuration
        config = chart.to_frontend_config()
        assert "series" in config
        assert "options" in config
        assert len(config["series"]) == 2

        # Step 4: Verify configuration structure
        candlestick_config = config["series"][0]
        volume_config = config["series"][1]

        assert candlestick_config["type"] == "Candlestick"
        assert volume_config["type"] == "Histogram"
        assert candlestick_config["priceScaleId"] == "right"
        assert volume_config["priceScaleId"] == "volume"

        # Step 5: Mock rendering
        with patch("streamlit_lightweight_charts_pro._component_func") as mock_component:
            mock_component.return_value = MagicMock()

            # Render the chart
            result = chart.render(key="e2e_test")

            # Verify rendering was called
            mock_component.assert_called_once()
            call_args = mock_component.call_args
            assert "config" in call_args[1]
            assert call_args[1]["key"] == "e2e_test"

    def test_real_world_scenario_e2e(self):
        """Test real-world scenario with typical usage patterns."""
        # Simulate real-world data loading
        # Step 1: Load and prepare data
        df = self.ohlcv_df.copy()

        # Step 2: Data validation
        assert not df.isnull().any().any()
        assert len(df) > 0
        assert all(
            col in df.columns for col in ["datetime", "open", "high", "low", "close", "volume"]
        )

        # Step 3: Create chart with real-world settings
        chart = PriceVolumeChart(
            data=df,
            up_color="#00C851",  # Green for up candles
            down_color="#FF4444",  # Red for down candles
            border_visible=True,
            volume_color="#2196F3",  # Blue for volume
            volume_alpha=0.7,
            height=500,
        )

        # Step 4: Verify chart properties
        assert chart.has_volume() is True
        candlestick_series = chart.get_candlestick_series()
        volume_series = chart.get_volume_series()

        assert candlestick_series.up_color == "#00C851"
        assert candlestick_series.down_color == "#FF4444"
        assert candlestick_series.border_visible is True
        assert volume_series.color == "#2196F3b3"  # with 0.7 alpha

        # Step 5: Test dynamic updates
        chart.update_volume_alpha(0.5)
        chart.update_volume_color("#FF9800", 0.6)

        # Step 6: Generate final configuration
        config = chart.to_frontend_config()

        # Step 7: Verify final state
        assert config["options"]["height"] == 500
        assert len(config["series"]) == 2
        assert config["series"][0]["type"] == "Candlestick"
        assert config["series"][1]["type"] == "Histogram"

    def test_data_transformation_e2e(self):
        """Test end-to-end data transformation workflow."""
        # Step 1: Start with raw data
        raw_data = [
            {"date": "2022-01-01", "o": 100.0, "h": 105.0, "l": 98.0, "c": 102.0, "v": 1000},
            {"date": "2022-01-02", "o": 102.0, "h": 108.0, "l": 101.0, "c": 106.0, "v": 1500},
            {"date": "2022-01-03", "o": 106.0, "h": 110.0, "l": 104.0, "c": 108.0, "v": 1200},
        ]

        # Step 2: Transform to DataFrame
        df = pd.DataFrame(raw_data)

        # Step 3: Create chart with custom column mapping
        chart = PriceVolumeChart(
            data=df,
            column_mapping={
                "time": "date",
                "open": "o",
                "high": "h",
                "low": "l",
                "close": "c",
                "volume": "v",
            },
            volume_alpha=0.8,
        )

        # Step 4: Verify transformation worked
        assert chart.has_volume() is True
        assert len(chart.get_candlestick_series().data) == 3
        assert len(chart.get_volume_series().data) == 3

        # Step 5: Verify data integrity
        candlestick_data = chart.get_candlestick_series().data
        volume_data = chart.get_volume_series().data

        assert candlestick_data[0].time == "2022-01-01"
        assert candlestick_data[0].open == 100.0
        assert candlestick_data[0].high == 105.0
        assert candlestick_data[0].low == 98.0
        assert candlestick_data[0].close == 102.0

        assert volume_data[0].time == "2022-01-01"
        assert volume_data[0].value == 1000

    def test_performance_e2e(self):
        """Test end-to-end performance characteristics."""
        # Step 1: Create large dataset
        large_dates = pd.date_range("2020-01-01", periods=1000, freq="D")
        np.random.seed(42)

        large_prices = [100.0]
        for _ in range(999):
            large_prices.append(large_prices[-1] * (1 + np.random.normal(0, 0.02)))

        large_df = pd.DataFrame(
            {
                "datetime": large_dates,
                "open": large_prices,
                "high": [p * (1 + abs(np.random.normal(0, 0.01))) for p in large_prices],
                "low": [p * (1 - abs(np.random.normal(0, 0.01))) for p in large_prices],
                "close": [p * (1 + np.random.normal(0, 0.005)) for p in large_prices],
                "volume": np.random.randint(1000, 10000, 1000),
            }
        )

        # Ensure data integrity
        large_df["high"] = large_df[["open", "close", "high"]].max(axis=1)
        large_df["low"] = large_df[["open", "close", "low"]].min(axis=1)

        # Step 2: Measure chart creation time
        start_time = time.time()
        chart = PriceVolumeChart(data=large_df)
        creation_time = time.time() - start_time

        # Step 3: Measure configuration generation time
        start_time = time.time()
        config = chart.to_frontend_config()
        config_time = time.time() - start_time

        # Step 4: Verify performance requirements
        assert creation_time < 2.0  # Should create chart in under 2 seconds
        assert config_time < 1.0  # Should generate config in under 1 second

        # Step 5: Verify chart handles large dataset correctly
        assert chart.has_volume() is True
        assert len(chart.series) == 2
        assert len(chart.get_candlestick_series().data) == 1000
        assert len(chart.get_volume_series().data) == 1000

    def test_error_handling_e2e(self):
        """Test end-to-end error handling."""
        # Step 1: Test with invalid data
        with pytest.raises(ValueError):
            PriceVolumeChart(data=None)

        # Step 2: Test with empty DataFrame
        empty_df = pd.DataFrame(columns=["datetime", "open", "high", "low", "close", "volume"])
        chart = PriceVolumeChart(data=empty_df)
        assert chart.has_volume() is True
        assert len(chart.series) == 2

        # Step 3: Test with missing columns
        invalid_df = pd.DataFrame(
            {
                "datetime": ["2022-01-01"],
                "open": [100.0],
                # Missing required columns
            }
        )

        with pytest.raises(KeyError):
            PriceVolumeChart(data=invalid_df)

        # Step 4: Test with invalid column mapping
        valid_df = self.ohlcv_df.copy()
        with pytest.raises(KeyError):
            PriceVolumeChart(data=valid_df, column_mapping={"invalid": "column"})

    def test_memory_management_e2e(self):
        """Test end-to-end memory management."""
        import psutil
        import os

        # Step 1: Get initial memory usage
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss

        # Step 2: Create multiple charts
        charts = []
        for i in range(10):
            chart = PriceVolumeChart(data=self.ohlcv_df)
            charts.append(chart)

            # Generate configuration for each chart
            config = chart.to_frontend_config()
            assert len(config["series"]) == 2

        # Step 3: Measure memory usage
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory

        # Step 4: Verify memory usage is reasonable
        assert memory_increase < 100 * 1024 * 1024  # Less than 100MB

        # Step 5: Clean up
        del charts

        # Step 6: Verify memory can be freed
        import gc

        gc.collect()

        cleanup_memory = process.memory_info().rss
        assert cleanup_memory <= final_memory

    def test_concurrent_usage_e2e(self):
        """Test end-to-end concurrent usage scenarios."""
        import threading
        import time

        results = []
        errors = []

        def create_and_test_chart(thread_id):
            try:
                # Create chart
                chart = PriceVolumeChart(data=self.ohlcv_df)

                # Test basic functionality
                assert chart.has_volume() is True
                assert len(chart.series) == 2

                # Generate configuration
                config = chart.to_frontend_config()
                assert len(config["series"]) == 2

                # Test dynamic updates
                chart.update_volume_alpha(0.5)
                chart.update_volume_color("#FF0000", 0.7)

                results.append((thread_id, True))
            except Exception as e:
                errors.append((thread_id, str(e)))

        # Step 1: Create multiple threads
        threads = []
        for i in range(5):
            thread = threading.Thread(target=create_and_test_chart, args=(i,))
            threads.append(thread)

        # Step 2: Start all threads
        for thread in threads:
            thread.start()

        # Step 3: Wait for completion
        for thread in threads:
            thread.join()

        # Step 4: Verify results
        assert len(errors) == 0, f"Errors occurred: {errors}"
        assert len(results) == 5

        for thread_id, success in results:
            assert success is True

    def test_streamlit_integration_e2e(self):
        """Test end-to-end Streamlit integration."""
        # Step 1: Create chart
        chart = PriceVolumeChart(data=self.ohlcv_df, volume_alpha=0.8, height=400)

        # Step 2: Mock Streamlit components
        with patch("streamlit.components.v1.html") as mock_html:
            mock_html.return_value = MagicMock()

            # Step 3: Mock the component function
            with patch("streamlit_lightweight_charts_pro._component_func") as mock_component:
                mock_component.return_value = MagicMock()

                # Step 4: Render chart
                result = chart.render(key="streamlit_test")

                # Step 5: Verify rendering
                mock_component.assert_called_once()

                # Step 6: Verify chart properties
                call_args = mock_component.call_args
                assert "config" in call_args[1]
                assert call_args[1]["key"] == "streamlit_test"

    def test_data_consistency_e2e(self):
        """Test end-to-end data consistency across the entire workflow."""
        # Step 1: Create original data
        original_data = self.ohlcv_df.copy()

        # Step 2: Create chart
        chart = PriceVolumeChart(data=original_data)

        # Step 3: Extract data from chart
        candlestick_data = chart.get_candlestick_series().data
        volume_data = chart.get_volume_series().data

        # Step 4: Verify data consistency
        assert len(candlestick_data) == len(original_data)
        assert len(volume_data) == len(original_data)

        # Step 5: Verify each data point
        for i in range(len(original_data)):
            original_row = original_data.iloc[i]
            candlestick_point = candlestick_data[i]
            volume_point = volume_data[i]

            # Verify time consistency
            assert str(original_row["datetime"]) == candlestick_point.time
            assert candlestick_point.time == volume_point.time

            # Verify OHLC data
            assert abs(original_row["open"] - candlestick_point.open) < 1e-10
            assert abs(original_row["high"] - candlestick_point.high) < 1e-10
            assert abs(original_row["low"] - candlestick_point.low) < 1e-10
            assert abs(original_row["close"] - candlestick_point.close) < 1e-10

            # Verify volume data
            assert abs(original_row["volume"] - volume_point.value) < 1e-10

        # Step 6: Generate configuration and verify
        config = chart.to_frontend_config()
        candlestick_config = config["series"][0]
        volume_config = config["series"][1]

        assert len(candlestick_config["data"]) == len(original_data)
        assert len(volume_config["data"]) == len(original_data)

    def test_user_experience_e2e(self):
        """Test end-to-end user experience workflow."""
        # Step 1: Simulate user creating a chart
        chart = PriceVolumeChart(
            data=self.ohlcv_df,
            up_color="#4CAF50",
            down_color="#F44336",
            volume_color="#26a69a",
            volume_alpha=0.8,
        )

        # Step 2: Simulate user checking chart properties
        assert chart.has_volume() is True
        candlestick_series = chart.get_candlestick_series()
        volume_series = chart.get_volume_series()

        # Step 3: Simulate user customizing the chart
        chart.update_volume_alpha(0.6)
        chart.update_volume_color("#FF9800", 0.7)
        chart.update_options(height=500)

        # Step 4: Simulate user generating the chart
        config = chart.to_frontend_config()

        # Step 5: Verify user experience is smooth
        assert config["options"]["height"] == 500
        assert len(config["series"]) == 2
        assert config["series"][0]["type"] == "Candlestick"
        assert config["series"][1]["type"] == "Histogram"

        # Step 6: Simulate user rendering the chart
        with patch("streamlit_lightweight_charts_pro._component_func") as mock_component:
            mock_component.return_value = MagicMock()
            result = chart.render(key="user_experience_test")

            # Verify rendering works
            mock_component.assert_called_once()
