"""Tests for the ultra-simplified Series API."""

import pandas as pd

from streamlit_lightweight_charts_pro.charts.series import (
    AreaSeries,
    BarSeries,
    BaselineSeries,
    CandlestickSeries,
    HistogramSeries,
    LineSeries,
)
from streamlit_lightweight_charts_pro.data import OhlcData, SingleValueData
from streamlit_lightweight_charts_pro.type_definitions.enums import LineStyle, LineType


def test_area_series_ultra_simplified():
    """Test AreaSeries with ultra-simplified API."""
    # Create test data
    data = [SingleValueData("2024-01-01", 100.0), SingleValueData("2024-01-02", 105.0)]

    # Test with direct styling parameters
    series = AreaSeries(
        data=data,
        top_color="rgba(0,255,0,0.5)",
        bottom_color="rgba(0,255,0,0.0)",
        line_color="#00ff00",
        line_width=3,
    )

    # Test attributes are set correctly
    assert series.top_color == "rgba(0,255,0,0.5)"
    assert series.line_width == 3

    # Test options dictionary
    options = series._get_options_dict()
    assert options["topColor"] == "rgba(0,255,0,0.5)"
    assert options["lineWidth"] == 3
    assert options["lineStyle"] == LineStyle.SOLID.value


def test_line_series_ultra_simplified():
    """Test LineSeries with ultra-simplified API."""
    # Create test data
    data = [SingleValueData("2024-01-01", 100.0), SingleValueData("2024-01-02", 105.0)]

    # Test with direct styling parameters
    series = LineSeries(
        data=data,
        color="#ff0000",
        line_style=LineStyle.DASHED,
        line_width=2,
        line_type=LineType.CURVED,
    )

    # Test attributes are set correctly
    assert series.color == "#ff0000"
    assert series.line_style == LineStyle.DASHED

    # Test options dictionary
    options = series._get_options_dict()
    assert options["color"] == "#ff0000"
    assert options["lineStyle"] == LineStyle.DASHED.value
    assert options["lineType"] == LineType.CURVED.value


def test_bar_series_ultra_simplified():
    """Test BarSeries with ultra-simplified API."""
    # Create test data
    data = [SingleValueData("2024-01-01", 100.0)]

    # Test with direct styling parameters
    series = BarSeries(
        data=data,
        color="#00ff00",
        base=0.0,
    )

    # Test attributes are set correctly
    assert series.color == "#00ff00"
    assert series.base == 0.0

    # Test options dictionary
    options = series._get_options_dict()
    assert options["color"] == "#00ff00"
    assert options["base"] == 0.0


def test_candlestick_series_ultra_simplified():
    """Test CandlestickSeries with ultra-simplified API."""
    # Create test data
    data = [OhlcData("2024-01-01", 100.0, 105.0, 98.0, 102.0)]

    # Test with direct styling parameters
    series = CandlestickSeries(
        data=data,
        up_color="#00ff00",
        down_color="#ff0000",
        wick_visible=False,
        border_visible=True,
    )

    # Test attributes are set correctly
    assert series.up_color == "#00ff00"
    assert series.wick_visible is False
    assert series.border_visible is True

    # Test options dictionary
    options = series._get_options_dict()
    assert options["upColor"] == "#00ff00"
    assert options["wickVisible"] is False
    assert options["borderVisible"] is True


def test_histogram_series_ultra_simplified():
    """Test HistogramSeries with ultra-simplified API."""
    from streamlit_lightweight_charts_pro.data import HistogramData

    # Create test data
    data = [HistogramData("2024-01-01", 1000000)]

    # Test with direct styling parameters
    series = HistogramSeries(
        data=data,
        color="#ff00ff",
        base=10.0,
    )

    # Test attributes are set correctly
    assert series.color == "#ff00ff"
    assert series.base == 10.0

    # Test options dictionary
    options = series._get_options_dict()
    assert options["color"] == "#ff00ff"
    assert options["base"] == 10.0


def test_baseline_series_ultra_simplified():
    """Test BaselineSeries with ultra-simplified API."""
    from streamlit_lightweight_charts_pro.data import BaselineData

    # Create test data
    data = [BaselineData("2024-01-01", 5.2)]

    # Test with direct styling parameters
    series = BaselineSeries(
        data=data,
        base_value={"type": "price", "price": 50.0},
        top_line_color="#00ff00",
        bottom_line_color="#ff0000",
    )

    # Test attributes are set correctly
    assert series.base_value["price"] == 50.0
    assert series.top_line_color == "#00ff00"

    # Test options dictionary
    options = series._get_options_dict()
    assert options["baseValue"]["price"] == 50.0
    assert options["topLineColor"] == "#00ff00"


def test_series_with_dataframe():
    """Test Series classes with DataFrame input."""
    # Create test DataFrame
    df = pd.DataFrame({"datetime": ["2024-01-01", "2024-01-02"], "close": [100.0, 105.0]})

    # Test LineSeries with DataFrame
    series = LineSeries(data=df, color="#ff0000", line_width=3)

    # Test that data was converted correctly
    assert len(series.data) == 2
    assert series.data[0].value == 100.0
    assert series.data[1].value == 105.0

    # Test options
    options = series._get_options_dict()
    assert options["color"] == "#ff0000"
    assert options["lineWidth"] == 3


def test_series_with_custom_column_mapping():
    """Test Series classes with custom column mapping."""
    # Create test DataFrame with custom column names
    df = pd.DataFrame({"date": ["2024-01-01", "2024-01-02"], "price": [100.0, 105.0]})

    # Test LineSeries with custom column mapping
    series = LineSeries(data=df, column_mapping={"time": "date", "value": "price"}, color="#ff0000")

    # Test that data was converted correctly
    assert len(series.data) == 2
    assert series.data[0].value == 100.0
    assert series.data[1].value == 105.0


def test_series_to_dict():
    """Test Series to_dict method."""
    data = [SingleValueData("2024-01-01", 100.0)]

    series = LineSeries(data=data, color="#ff0000", line_width=3)

    result = series.to_dict()

    # Test structure
    assert "type" in result
    assert "data" in result
    assert "options" in result

    # Test data
    assert len(result["data"]) == 1
    assert result["data"][0]["value"] == 100.0

    # Test options
    assert result["options"]["color"] == "#ff0000"
    assert result["options"]["lineWidth"] == 3


def test_series_chart_type():
    """Test that each series has the correct chart type."""
    data = [SingleValueData("2024-01-01", 100.0)]

    # Test each series type
    assert LineSeries(data=data).chart_type.value == "Line"
    assert AreaSeries(data=data).chart_type.value == "Area"
    assert HistogramSeries(data=data).chart_type.value == "Histogram"
    assert BaselineSeries(data=data).chart_type.value == "Baseline"

    # Test OHLC series types
    ohlc_data = [OhlcData("2024-01-01", 100.0, 105.0, 98.0, 102.0)]
    assert CandlestickSeries(data=ohlc_data).chart_type.value == "Candlestick"

    # Test single value series types
    single_value_data = [SingleValueData("2024-01-01", 100.0)]
    assert BarSeries(data=single_value_data).chart_type.value == "Bar"
