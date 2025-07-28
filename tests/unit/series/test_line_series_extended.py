"""
Extended unit tests for the LineSeries class.

This module provides additional test coverage for LineSeries functionality
that may not be covered in the main test file.
"""

import pandas as pd
import pytest

from streamlit_lightweight_charts_pro.charts.options.line_options import LineOptions
from streamlit_lightweight_charts_pro.charts.options.price_line_options import PriceLineOptions
from streamlit_lightweight_charts_pro.charts.series.line import LineSeries
from streamlit_lightweight_charts_pro.data.line_data import LineData
from streamlit_lightweight_charts_pro.data.marker import Marker
from streamlit_lightweight_charts_pro.type_definitions.enums import (
    ChartType,
    MarkerPosition,
    MarkerShape,
)


class TestLineSeriesExtended:
    """Extended test cases for LineSeries."""

    def test_chart_type_property(self):
        """Test the chart_type property."""
        data = [LineData(time=1640995200, value=100)]
        line_options = LineOptions()
        series = LineSeries(data=data, line_options=line_options)
        assert series.chart_type == ChartType.LINE

    def test_to_dict_method_complete(self):
        """Test the complete to_dict method."""
        line_options = LineOptions(color="#ff0000")
        data = [LineData(time=1640995200, value=100)]

        series = LineSeries(data=data, line_options=line_options)

        # Add price lines and markers
        price_line = PriceLineOptions(price=100, color="#00ff00")
        marker = Marker(
            time=1640995200,
            position=MarkerPosition.ABOVE_BAR,
            color="#0000ff",
            shape=MarkerShape.CIRCLE,
        )

        series.add_price_line(price_line)
        series.add_marker(
            time=1640995200,
            position=MarkerPosition.ABOVE_BAR,
            color="#0000ff",
            shape=MarkerShape.CIRCLE,
        )

        result = series.asdict()

        assert result["type"] == "line"
        assert len(result["data"]) == 1
        assert result["data"][0]["time"] == 1640995200
        assert result["data"][0]["value"] == 100
        assert result["options"]["color"] == "#ff0000"
        assert len(result["priceLines"]) == 1
        assert len(result["markers"]) == 1

    def test_to_dict_method_empty_data(self):
        """Test to_dict method with empty data."""
        line_options = LineOptions()
        series = LineSeries(data=[], line_options=line_options)

        result = series.asdict()

        assert result["type"] == "line"
        assert result["data"] == []
        assert "options" in result
        # priceLines should only be present when price lines are added

    def test_from_dataframe_with_custom_column_mapping(self):
        """Test from_dataframe with custom column mapping."""
        df = pd.DataFrame(
            {
                "timestamp": [1640995200, 1641081600],
                "price": [100, 110],
                "line_color": ["#ff0000", "#00ff00"],
            }
        )

        line_options = LineOptions()
        series = LineSeries.from_dataframe(
            df=df,
            line_options=line_options,
            column_mapping={"time": "timestamp", "value": "price", "color": "line_color"},
        )

        assert len(series.data) == 2
        assert series.data[0].time == 1640995200
        assert series.data[0].value == 100
        assert series.data[0].color == "#ff0000"
        assert series.data[1].time == 1641081600
        assert series.data[1].value == 110
        assert series.data[1].color == "#00ff00"

    def test_from_dataframe_with_index_time(self):
        """Test from_dataframe with time in index."""
        df = pd.DataFrame({"value": [100, 110]}, index=pd.to_datetime(["2022-01-01", "2022-01-02"]))

        line_options = LineOptions()
        series = LineSeries.from_dataframe(
            df=df, line_options=line_options, column_mapping={"time": "index", "value": "value"}
        )

        assert len(series.data) == 2
        assert all(isinstance(d, LineData) for d in series.data)

    def test_from_dataframe_with_multi_index(self):
        """Test from_dataframe with multi-index."""
        df = pd.DataFrame({"value": [100, 110]})
        df.index = pd.MultiIndex.from_tuples(
            [("2022-01-01", "A"), ("2022-01-02", "B")], names=["date", "symbol"]
        )

        line_options = LineOptions()
        series = LineSeries.from_dataframe(
            df=df, line_options=line_options, column_mapping={"time": "date", "value": "value"}
        )

        assert len(series.data) == 2
        assert all(isinstance(d, LineData) for d in series.data)

    def test_error_handling_missing_line_options(self):
        """Test error handling when line_options is missing."""
        data = [LineData(time=1640995200, value=100)]

        with pytest.raises(TypeError):
            LineSeries(data=data)  # Missing line_options

    def test_error_handling_invalid_line_options(self):
        """Test error handling with invalid line_options."""
        data = [LineData(time=1640995200, value=100)]

        # This should raise TypeError as the constructor validates line_options type
        with pytest.raises(TypeError, match="line_options must be an instance of LineOptions"):
            series = LineSeries(data=data, line_options="invalid")

    def test_line_options_property(self):
        """Test the line_options property."""
        line_options = LineOptions(color="#ff0000")
        data = [LineData(time=1640995200, value=100)]

        series = LineSeries(data=data, line_options=line_options)

        assert series.line_options is line_options

    def test_complex_method_chaining(self):
        """Test complex method chaining with LineSeries."""
        line_options = LineOptions(color="#ff0000")
        data = [LineData(time=1640995200, value=100)]

        series = LineSeries(data=data, line_options=line_options)

        # Test complex chaining
        result = (
            series.set_visible(False)
            .add_price_line(PriceLineOptions(price=100, color="#00ff00"))
            .add_marker(
                time=1640995200,
                position=MarkerPosition.ABOVE_BAR,
                color="#0000ff",
                shape=MarkerShape.CIRCLE,
                text="Test",
                size=10,
            )
            .clear_price_lines()
            .clear_markers()
        )

        assert result is series
        assert series.visible is False
        assert len(series.price_lines) == 0
        assert len(series.markers) == 0

    def test_data_class_property(self):
        """Test the data_class property."""
        assert LineSeries.data_class == LineData

    def test_required_columns_property(self):
        """Test the required_columns property."""
        required = LineSeries.data_class.required_columns
        assert isinstance(required, set)
        assert "time" in required
        assert "value" in required

    def test_optional_columns_property(self):
        """Test the optional_columns property."""
        optional = LineSeries.data_class.optional_columns
        assert isinstance(optional, set)
        assert "color" in optional

    def test_serialization_consistency(self):
        """Test that serialization is consistent across multiple calls."""
        line_options = LineOptions(color="#ff0000")
        data = [LineData(time=1640995200, value=100)]

        series = LineSeries(data=data, line_options=line_options)

        # Add some elements
        series.add_price_line(PriceLineOptions(price=100, color="#00ff00"))
        series.add_marker(
            time=1640995200,
            position=MarkerPosition.ABOVE_BAR,
            color="#0000ff",
            shape=MarkerShape.CIRCLE,
        )

        # Get serialized form multiple times
        result1 = series.asdict()
        result2 = series.asdict()

        # Should be identical
        assert result1 == result2

        # Should have expected structure
        assert result1["type"] == "line"
        assert len(result1["data"]) == 1
        assert len(result1["priceLines"]) == 1
        assert len(result1["markers"]) == 1

    def test_edge_case_empty_dataframe(self):
        """Test handling of empty DataFrame."""
        df = pd.DataFrame(columns=["time", "value"])

        line_options = LineOptions()
        series = LineSeries.from_dataframe(
            df=df, line_options=line_options, column_mapping={"time": "time", "value": "value"}
        )

        assert len(series.data) == 0

    def test_edge_case_single_row_dataframe(self):
        """Test handling of single row DataFrame."""
        df = pd.DataFrame({"time": [1640995200], "value": [100]})

        line_options = LineOptions()
        series = LineSeries.from_dataframe(
            df=df, line_options=line_options, column_mapping={"time": "time", "value": "value"}
        )

        assert len(series.data) == 1
        assert series.data[0].time == 1640995200
        assert series.data[0].value == 100
