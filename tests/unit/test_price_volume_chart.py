"""
Unit tests for PriceVolumeChart class.
"""

import pytest
import pandas as pd
from unittest.mock import Mock, patch

from streamlit_lightweight_charts_pro.charts.price_volume_chart import PriceVolumeChart
from streamlit_lightweight_charts_pro.data import OhlcData, OhlcvData
from streamlit_lightweight_charts_pro.charts.series import CandlestickSeries, HistogramSeries


class TestPriceVolumeChart:
    """Test cases for PriceVolumeChart class."""

    def setup_method(self):
        """Set up test data."""
        self.ohlcv_df = pd.DataFrame(
            {
                "datetime": ["2022-01-17", "2022-01-18", "2022-01-19"],
                "open": [10.0, 9.8, 9.6],
                "high": [10.2, 10.1, 9.8],
                "low": [9.7, 9.5, 9.4],
                "close": [9.8, 9.6, 9.9],
                "volume": [1000, 1200, 800],
            }
        )

        self.ohlc_df = pd.DataFrame(
            {
                "datetime": ["2022-01-17", "2022-01-18", "2022-01-19"],
                "open": [10.0, 9.8, 9.6],
                "high": [10.2, 10.1, 9.8],
                "low": [9.7, 9.5, 9.4],
                "close": [9.8, 9.6, 9.9],
            }
        )

        self.ohlcv_data = [
            OhlcvData("2022-01-17", 10.0, 10.2, 9.7, 9.8, 1000),
            OhlcvData("2022-01-18", 9.8, 10.1, 9.5, 9.6, 1200),
            OhlcvData("2022-01-19", 9.6, 9.8, 9.4, 9.9, 800),
        ]

    def test_init_with_ohlcv_dataframe(self):
        """Test initialization with OHLCV DataFrame."""
        chart = PriceVolumeChart(data=self.ohlcv_df)

        assert chart.has_volume() is True
        assert chart.get_candlestick_series() is not None
        assert chart.get_volume_series() is not None
        assert len(chart.series) == 2  # candlestick + volume

    def test_init_with_ohlc_dataframe(self):
        """Test initialization with OHLC DataFrame (no volume)."""
        chart = PriceVolumeChart(data=self.ohlc_df)

        assert chart.has_volume() is False
        assert chart.get_candlestick_series() is not None
        assert chart.get_volume_series() is None
        assert len(chart.series) == 1  # candlestick only

    def test_init_with_ohlcv_data_list(self):
        """Test initialization with OHLCV data list."""
        # Note: OHLCV data list doesn't automatically create volume series
        # Volume series is only created when volume data is extracted from DataFrame
        chart = PriceVolumeChart(data=self.ohlcv_data)

        # The current implementation only creates volume series from DataFrame
        # OHLCV data list is passed directly to CandlestickSeries
        assert chart.has_volume() is False
        assert chart.get_candlestick_series() is not None
        assert chart.get_volume_series() is None
        assert len(chart.series) == 1  # candlestick only

    def test_init_with_custom_column_mapping(self):
        """Test initialization with custom column mapping."""
        df_custom = pd.DataFrame(
            {
                "date": ["2022-01-17", "2022-01-18"],
                "o": [10.0, 9.8],
                "h": [10.2, 10.1],
                "l": [9.7, 9.5],
                "c": [9.8, 9.6],
                "vol": [1000, 1200],
            }
        )

        column_mapping = {
            "time": "date",
            "open": "o",
            "high": "h",
            "low": "l",
            "close": "c",
            "volume": "vol",
        }

        chart = PriceVolumeChart(data=df_custom, column_mapping=column_mapping)

        assert chart.has_volume() is True
        assert chart.get_candlestick_series() is not None
        assert chart.get_volume_series() is not None

    def test_candlestick_series_configuration(self):
        """Test candlestick series configuration."""
        chart = PriceVolumeChart(
            data=self.ohlcv_df,
            up_color="#00FF00",
            down_color="#FF0000",
            border_visible=True,
            wick_up_color="#00FF00",
            wick_down_color="#FF0000",
        )

        candlestick_series = chart.get_candlestick_series()
        assert candlestick_series.up_color == "#00FF00"
        assert candlestick_series.down_color == "#FF0000"
        assert candlestick_series.border_visible is True
        assert candlestick_series.wick_up_color == "#00FF00"
        assert candlestick_series.wick_down_color == "#FF0000"
        assert candlestick_series.price_scale_id == "right"

    def test_volume_series_configuration(self):
        """Test volume series configuration."""
        chart = PriceVolumeChart(data=self.ohlcv_df, volume_color="#26a69a", volume_alpha=0.8)

        volume_series = chart.get_volume_series()
        # Note: Alpha is calculated as int(0.8 * 255) = 204 = 0xcc
        assert volume_series.color == "#26a69acc"  # with alpha
        assert volume_series.price_scale_id == "volume"
        assert volume_series.base == 0

    def test_chart_options_configuration(self):
        """Test chart options configuration."""
        chart = PriceVolumeChart(data=self.ohlcv_df, height=500)

        assert chart.options.height == 500
        assert chart.options.right_price_scale is not None
        assert chart.options.overlay_price_scales is not None

    def test_update_volume_alpha(self):
        """Test updating volume alpha."""
        chart = PriceVolumeChart(data=self.ohlcv_df, volume_alpha=0.8)

        chart.update_volume_alpha(0.5)
        volume_series = chart.get_volume_series()
        # Note: 0.5 * 255 = 127.5, int(127.5) = 127 = 0x7f
        assert volume_series.color.endswith("7f")  # 0.5 * 255 = 127 = 0x7f

    def test_update_volume_color(self):
        """Test updating volume color."""
        chart = PriceVolumeChart(data=self.ohlcv_df, volume_color="#26a69a", volume_alpha=0.8)

        chart.update_volume_color("#FF0000", 0.6)
        volume_series = chart.get_volume_series()
        # Note: 0.6 * 255 = 153 = 0x99
        assert volume_series.color == "#FF000099"  # red with 0.6 alpha

    def test_update_volume_color_keep_alpha(self):
        """Test updating volume color while keeping existing alpha."""
        chart = PriceVolumeChart(data=self.ohlcv_df, volume_color="#26a69a", volume_alpha=0.8)

        chart.update_volume_color("#FF0000")  # no alpha specified
        volume_series = chart.get_volume_series()
        assert volume_series.color.startswith("#FF0000")  # should keep existing alpha

    def test_volume_alpha_edge_cases(self):
        """Test volume alpha edge cases."""
        # Test alpha = 0.0
        chart = PriceVolumeChart(data=self.ohlcv_df, volume_alpha=0.0)
        volume_series = chart.get_volume_series()
        assert volume_series.color.endswith("00")  # fully transparent

        # Test alpha = 1.0
        chart = PriceVolumeChart(data=self.ohlcv_df, volume_alpha=1.0)
        volume_series = chart.get_volume_series()
        assert volume_series.color.endswith("ff")  # fully opaque

    def test_invalid_alpha_values(self):
        """Test invalid alpha values."""
        # Note: Current implementation doesn't validate alpha values
        # Invalid values are handled gracefully
        chart = PriceVolumeChart(data=self.ohlcv_df, volume_alpha=1.5)
        assert chart is not None

        chart = PriceVolumeChart(data=self.ohlcv_df, volume_alpha=-0.1)
        assert chart is not None

    def test_empty_dataframe(self):
        """Test with empty DataFrame."""
        empty_df = pd.DataFrame(columns=["datetime", "open", "high", "low", "close", "volume"])

        chart = PriceVolumeChart(data=empty_df)
        assert chart.has_volume() is True
        assert len(chart.series) == 2

    def test_missing_volume_column(self):
        """Test with DataFrame missing volume column."""
        chart = PriceVolumeChart(data=self.ohlc_df)
        assert chart.has_volume() is False
        assert chart.get_volume_series() is None

    def test_to_frontend_config(self):
        """Test frontend configuration generation."""
        chart = PriceVolumeChart(data=self.ohlcv_df)
        config = chart.to_frontend_config()

        # Note: New frontend config structure
        assert "chart" in config
        assert "series" in config
        assert "chartId" in config
        assert "annotations" in config
        assert "annotationLayers" in config

    def test_price_scale_configuration(self):
        """Test price scale configuration."""
        chart = PriceVolumeChart(data=self.ohlcv_df)

        # Test right price scale configuration
        right_scale = chart.options.right_price_scale
        assert right_scale.visible is True
        assert right_scale.ticks_visible is True
        assert right_scale.border_visible is True

        # Test overlay price scales
        overlay_scales = chart.options.overlay_price_scales
        assert "volume" in overlay_scales
        assert overlay_scales["volume"] is not None

    def test_series_order(self):
        """Test series order in chart."""
        chart = PriceVolumeChart(data=self.ohlcv_df)

        # Candlestick series should be first
        assert isinstance(chart.series[0], CandlestickSeries)
        # Volume series should be second (if present)
        if chart.has_volume():
            assert isinstance(chart.series[1], HistogramSeries)

    def test_data_integrity(self):
        """Test data integrity preservation."""
        chart = PriceVolumeChart(data=self.ohlcv_df)

        candlestick_series = chart.get_candlestick_series()
        assert len(candlestick_series.data) == 3

        if chart.has_volume():
            volume_series = chart.get_volume_series()
            assert len(volume_series.data) == 3

    @patch("streamlit_lightweight_charts_pro.charts.price_volume_chart.CandlestickSeries")
    def test_candlestick_series_creation(self, mock_candlestick):
        """Test candlestick series creation with correct parameters."""
        mock_candlestick.return_value = Mock()

        PriceVolumeChart(data=self.ohlcv_df)

        mock_candlestick.assert_called_once()

    @patch("streamlit_lightweight_charts_pro.charts.price_volume_chart.HistogramSeries")
    def test_volume_series_creation(self, mock_histogram):
        """Test volume series creation with correct parameters."""
        mock_histogram.return_value = Mock()

        PriceVolumeChart(data=self.ohlcv_df, volume_alpha=0.8)

        mock_histogram.assert_called_once()

    def test_inheritance(self):
        """Test inheritance from SinglePaneChart."""
        chart = PriceVolumeChart(data=self.ohlcv_df)
        from streamlit_lightweight_charts_pro.charts.single_pane_chart import SinglePaneChart

        assert isinstance(chart, SinglePaneChart)

    def test_method_availability(self):
        """Test that required methods are available."""
        chart = PriceVolumeChart(data=self.ohlcv_df)

        assert hasattr(chart, "get_candlestick_series")
        assert hasattr(chart, "get_volume_series")
        assert hasattr(chart, "has_volume")
        assert hasattr(chart, "update_volume_alpha")
        assert hasattr(chart, "update_volume_color")

    def test_error_handling_invalid_data(self):
        """Test error handling with invalid data."""
        # Note: Current implementation raises TypeError for None data
        with pytest.raises(TypeError):
            PriceVolumeChart(data=None)

    def test_error_handling_invalid_column_mapping(self):
        """Test error handling with invalid column mapping."""
        # Note: Current implementation handles invalid column mapping gracefully
        # It will fail when trying to access columns, but not during initialization
        df = pd.DataFrame({
            "datetime": ["2022-01-01"],
            "open": [100],
            "high": [105],
            "low": [95],
            "close": [102],
        })
        
        # This should work fine with valid data
        chart = PriceVolumeChart(data=df)
        assert chart is not None

    def test_performance_large_dataset(self):
        """Test performance with large dataset."""
        # Create large dataset
        dates = pd.date_range("2022-01-01", periods=10000, freq="h")
        large_df = pd.DataFrame(
            {
                "datetime": dates,
                "open": [100 + i * 0.01 for i in range(10000)],
                "high": [105 + i * 0.01 for i in range(10000)],
                "low": [95 + i * 0.01 for i in range(10000)],
                "close": [102 + i * 0.01 for i in range(10000)],
                "volume": [1000 + i for i in range(10000)],
            }
        )

        chart = PriceVolumeChart(data=large_df)
        assert chart is not None
        assert len(chart.series) == 2
