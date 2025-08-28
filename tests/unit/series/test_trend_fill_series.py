"""
Unit tests for TrendFillSeries with dual mode support.

This module provides comprehensive testing for the upgraded TrendFillSeries
that supports both single and dual trend line modes.
"""

import pandas as pd
import pytest

from streamlit_lightweight_charts_pro.charts.series.trend_fill import TrendFillSeries
from streamlit_lightweight_charts_pro.data.trend_fill import TrendFillData


class TestTrendFillData:
    """Test cases for TrendFillData class."""

    def test_single_mode_creation(self):
        """Test creating TrendFillData in single mode."""
        data = TrendFillData("2024-01-01", trend_line=110.0, body_middle=105.0, trend_direction=1)

        assert data.trend_line == 110.0
        assert data.body_middle == 105.0
        assert data.trend_direction == 1
        assert data.up_trend is None
        assert data.down_trend is None
        assert data.is_uptrend
        assert not data.is_downtrend
        assert not data.is_neutral

        """Test asdict output in single mode."""
        data = [
            TrendFillData("2024-01-01", trend_line=110.0, body_middle=105.0, trend_direction=1),
            TrendFillData("2024-01-02", trend_line=108.0, body_middle=113.0, trend_direction=-1),
        ]

        series = TrendFillSeries(
            data=data,
        )
        data_dict = series.asdict()

        assert len(data_dict["data"]) == 2

        # Check trend types
        assert data_dict["data"][0]["trend_type"] == "uptrend"
        assert data_dict["data"][1]["trend_type"] == "downtrend"

        # Check fill colors
        assert data_dict["data"][0]["fill_color"] is not None
        assert data_dict["data"][1]["fill_color"] is not None

        """Test trend period analysis."""
        data = [
            TrendFillData("2024-01-01", up_trend=110.0, body_middle=105.0, trend_direction=1),
            TrendFillData("2024-01-02", up_trend=112.0, body_middle=107.0, trend_direction=1),
            TrendFillData("2024-01-03", down_trend=108.0, body_middle=113.0, trend_direction=-1),
            TrendFillData("2024-01-04", down_trend=105.0, body_middle=110.0, trend_direction=-1),
        ]

        series = TrendFillSeries(
            data=data,
        )
        periods = series.get_trend_periods()

        assert len(periods) == 2
        assert periods[0]["trend_type"] == "uptrend"
        assert periods[0]["start_index"] == 0
        assert periods[0]["end_index"] == 1
        assert periods[1]["trend_type"] == "downtrend"
        assert periods[1]["start_index"] == 2
        assert periods[1]["end_index"] == 3

    def test_trend_statistics(self):
        """Test trend statistics calculation."""
        data = [
            TrendFillData("2024-01-01", up_trend=110.0, body_middle=105.0, trend_direction=1),
            TrendFillData("2024-01-02", up_trend=112.0, body_middle=107.0, trend_direction=1),
            TrendFillData("2024-01-03", down_trend=108.0, body_middle=113.0, trend_direction=-1),
            TrendFillData("2024-01-04", body_middle=110.0, trend_direction=0),
        ]

        series = TrendFillSeries(
            data=data,
        )
        stats = series.get_trend_statistics()

        assert stats["total_periods"] == 2
        assert stats["uptrend_periods"] == 1
        assert stats["downtrend_periods"] == 1
        assert stats["neutral_periods"] == 1
        assert stats["longest_uptrend"] == 2
        assert stats["longest_downtrend"] == 1

    def test_pandas_integration(self):
        """Test integration with pandas DataFrames."""
        df = pd.DataFrame(
            {
                "time": ["2024-01-01", "2024-01-02"],
                "up_trend": [110.0, 112.0],
                "body_middle": [105.0, 107.0],
                "trend_direction": [1, 1],
            }
        )

        series = TrendFillSeries(
            data=df,
            column_mapping={
                "time": "time",
                "up_trend": "up_trend",
                "body_middle": "body_middle",
                "trend_direction": "trend_direction",
            },
        )

        assert len(series.data) == 2
        assert series.data[0].up_trend == 110.0
        assert series.data[1].up_trend == 112.0

    def test_opacity_handling(self):
        """Test fill opacity handling."""
        series = TrendFillSeries(
            data=[], uptrend_fill_color="#00FF00", downtrend_fill_color="#FF0000", fill_opacity=0.5
        )

        # Check that colors are converted to rgba
        assert "rgba" in series._uptrend_fill_color
        assert "rgba" in series._downtrend_fill_color
        assert series._fill_opacity == 0.5

    def test_opacity_update(self):
        """Test updating fill opacity."""
        series = TrendFillSeries(data=[], fill_opacity=0.3)

        series.update_fill_opacity(0.7)
        assert series._fill_opacity == 0.7

    def test_invalid_opacity(self):
        """Test invalid opacity values."""
        series = TrendFillSeries(data=[], fill_opacity=0.5)

        with pytest.raises(ValueError, match="Opacity must be between 0.0 and 1.0"):
            series.update_fill_opacity(1.5)

    def test_empty_data(self):
        """Test handling of empty data."""
        series = TrendFillSeries(data=[])

        periods = series.get_trend_periods()
        stats = series.get_trend_statistics()

        assert periods == []
        assert stats["total_periods"] == 0
