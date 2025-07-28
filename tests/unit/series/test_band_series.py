"""
Tests for BandSeries class.

This module contains comprehensive tests for the BandSeries class,
covering construction, styling options, serialization, and edge cases.
"""

import pandas as pd
import pytest

from streamlit_lightweight_charts_pro.charts.options.line_options import LineOptions
from streamlit_lightweight_charts_pro.charts.options.price_line_options import PriceLineOptions
from streamlit_lightweight_charts_pro.charts.series.band import BandSeries
from streamlit_lightweight_charts_pro.charts.series.base import Series
from streamlit_lightweight_charts_pro.data.band import BandData
from streamlit_lightweight_charts_pro.type_definitions.enums import (
    LineStyle,
    LineType,
    MarkerPosition,
    MarkerShape,
)


class TestBandSeriesConstruction:
    """Test cases for BandSeries construction."""

    def test_standard_construction(self):
        """Test standard BandSeries construction."""
        data = [BandData(time=1640995200, upper=110.0, middle=105.0, lower=100.0)]
        series = BandSeries(data=data)

        assert series.data == data
        assert series.chart_type == "band"
        assert series.visible is True
        assert series.price_scale_id == "right"
        assert series.pane_id == 0
        assert series.upper_fill_color == "rgba(76, 175, 80, 0.1)"
        assert series.lower_fill_color == "rgba(244, 67, 54, 0.1)"
        assert isinstance(series.upper_line_options, LineOptions)
        assert isinstance(series.middle_line_options, LineOptions)
        assert isinstance(series.lower_line_options, LineOptions)

    def test_construction_with_custom_parameters(self):
        """Test BandSeries construction with custom parameters."""
        data = [BandData(time=1640995200, upper=110.0, middle=105.0, lower=100.0)]
        series = BandSeries(
            data=data,
            visible=False,
            price_scale_id="left",
            pane_id=1,
        )

        assert series.data == data
        assert series.visible is False
        assert series.price_scale_id == "left"
        assert series.pane_id == 1

    def test_construction_with_dataframe(self):
        """Test BandSeries construction with DataFrame."""
        df = pd.DataFrame(
            {
                "datetime": [1640995200, 1641081600],
                "upper": [110.0, 112.0],
                "middle": [105.0, 107.0],
                "lower": [100.0, 102.0],
            }
        )

        series = BandSeries(
            data=df,
            column_mapping={
                "time": "datetime",
                "upper": "upper",
                "middle": "middle",
                "lower": "lower",
            },
        )

        assert len(series.data) == 2
        assert series.data[0].time == 1640995200
        assert series.data[0].upper == 110.0
        assert series.data[0].middle == 105.0
        assert series.data[0].lower == 100.0
        assert series.data[1].time == 1641081600
        assert series.data[1].upper == 112.0
        assert series.data[1].middle == 107.0
        assert series.data[1].lower == 102.0

    def test_default_line_options(self):
        """Test default line options values."""
        data = [BandData(time=1640995200, upper=110.0, middle=105.0, lower=100.0)]
        series = BandSeries(data=data)

        # Check default colors
        assert series.upper_line_options.color == "#4CAF50"
        assert series.middle_line_options.color == "#2196F3"
        assert series.lower_line_options.color == "#F44336"

        # Check default line widths
        assert series.upper_line_options.line_width == 2
        assert series.middle_line_options.line_width == 2
        assert series.lower_line_options.line_width == 2

        # Check default line styles
        assert series.upper_line_options.line_style == "solid"
        assert series.middle_line_options.line_style == "solid"
        assert series.lower_line_options.line_style == "solid"


class TestBandSeriesProperties:
    """Test cases for BandSeries properties."""

    def test_chart_type_property(self):
        """Test chart_type property."""
        data = [BandData(time=1640995200, upper=110.0, middle=105.0, lower=100.0)]
        series = BandSeries(data=data)
        assert series.chart_type == "band"

    def test_upper_line_options_property(self):
        """Test upper_line_options property."""
        data = [BandData(time=1640995200, upper=110.0, middle=105.0, lower=100.0)]
        series = BandSeries(data=data)

        # Test getter
        assert isinstance(series.upper_line_options, LineOptions)
        assert series.upper_line_options.color == "#4CAF50"

        # Test setter
        new_options = LineOptions(color="#FF0000", line_width=3)
        series.upper_line_options = new_options
        assert series.upper_line_options == new_options
        assert series.upper_line_options.color == "#FF0000"

    def test_middle_line_options_property(self):
        """Test middle_line_options property."""
        data = [BandData(time=1640995200, upper=110.0, middle=105.0, lower=100.0)]
        series = BandSeries(data=data)

        # Test getter
        assert isinstance(series.middle_line_options, LineOptions)
        assert series.middle_line_options.color == "#2196F3"

        # Test setter
        new_options = LineOptions(color="#00FF00", line_width=4)
        series.middle_line_options = new_options
        assert series.middle_line_options == new_options
        assert series.middle_line_options.color == "#00FF00"

    def test_lower_line_options_property(self):
        """Test lower_line_options property."""
        data = [BandData(time=1640995200, upper=110.0, middle=105.0, lower=100.0)]
        series = BandSeries(data=data)

        # Test getter
        assert isinstance(series.lower_line_options, LineOptions)
        assert series.lower_line_options.color == "#F44336"

        # Test setter
        new_options = LineOptions(color="#0000FF", line_width=5)
        series.lower_line_options = new_options
        assert series.lower_line_options == new_options
        assert series.lower_line_options.color == "#0000FF"

    def test_fill_color_properties(self):
        """Test fill color properties."""
        data = [BandData(time=1640995200, upper=110.0, middle=105.0, lower=100.0)]
        series = BandSeries(data=data)

        # Test default values
        assert series.upper_fill_color == "rgba(76, 175, 80, 0.1)"
        assert series.lower_fill_color == "rgba(244, 67, 54, 0.1)"

        # Test setters
        series.upper_fill_color = "rgba(255, 0, 0, 0.5)"
        series.lower_fill_color = "rgba(0, 255, 0, 0.5)"

        assert series.upper_fill_color == "rgba(255, 0, 0, 0.5)"
        assert series.lower_fill_color == "rgba(0, 255, 0, 0.5)"

    def test_property_validation(self):
        """Test property validation."""
        data = [BandData(time=1640995200, upper=110.0, middle=105.0, lower=100.0)]
        series = BandSeries(data=data)

        # Test invalid line options type
        with pytest.raises(
            TypeError, match="upper_line_options must be an instance of LineOptions or None"
        ):
            series.upper_line_options = "invalid"

        # Test invalid middle line options type
        with pytest.raises(
            TypeError, match="middle_line_options must be an instance of LineOptions or None"
        ):
            series.middle_line_options = "invalid"

        with pytest.raises(
            TypeError, match="lower_line_options must be an instance of LineOptions or None"
        ):
            series.lower_line_options = "invalid"

        # Test invalid fill color type
        with pytest.raises(TypeError, match="upper_fill_color must be a string"):
            series.upper_fill_color = 123

        with pytest.raises(TypeError, match="lower_fill_color must be a string"):
            series.lower_fill_color = 123


class TestBandSeriesSerialization:
    """Test cases for BandSeries serialization."""

    def test_to_dict_basic(self):
        """Test basic to_dict functionality."""
        data = [BandData(time=1640995200, upper=110.0, middle=105.0, lower=100.0)]
        series = BandSeries(data=data)
        result = series.asdict()

        assert result["type"] == "band"
        assert len(result["data"]) == 1
        assert result["data"][0]["time"] == 1640995200
        assert result["data"][0]["upper"] == 110.0
        assert result["data"][0]["middle"] == 105.0
        assert result["data"][0]["lower"] == 100.0

    def test_to_dict_with_line_options(self):
        """Test to_dict with custom line options."""
        data = [BandData(time=1640995200, upper=110.0, middle=105.0, lower=100.0)]
        series = BandSeries(data=data)

        # Customize line options
        series.upper_line_options.color = "#FF0000"
        series.upper_line_options.line_width = 3
        series.middle_line_options.color = "#00FF00"
        series.middle_line_options.line_style = LineStyle.DOTTED
        series.lower_line_options.color = "#0000FF"
        series.upper_line_options.line_type = LineType.CURVED

        result = series.asdict()
        options = result["options"]
        # The base class to_dict flattens options, so check for flat keys
        assert options["color"] == "#FF0000"
        assert options["lineWidth"] == 3
        assert options["lineStyle"] == "solid"  # Only upper_line_options is used for flat keys
        assert options["lineType"] == LineType.CURVED.value

    def test_to_dict_with_fill_colors(self):
        """Test to_dict with custom fill colors."""
        data = [BandData(time=1640995200, upper=110.0, middle=105.0, lower=100.0)]
        series = BandSeries(data=data)

        series.upper_fill_color = "rgba(255, 0, 0, 0.5)"
        series.lower_fill_color = "rgba(0, 255, 0, 0.5)"

        result = series.asdict()
        options = result["options"]
        # The base class to_dict uses camelCase keys
        assert options["upperFillColor"] == "rgba(255, 0, 0, 0.5)"
        assert options["lowerFillColor"] == "rgba(0, 255, 0, 0.5)"

    def test_to_dict_with_markers(self):
        """Test to_dict with markers."""
        data = [BandData(time=1640995200, upper=110.0, middle=105.0, lower=100.0)]
        series = BandSeries(data=data)

        series.add_marker(
            time=1640995200,
            position=MarkerPosition.ABOVE_BAR,
            color="#FF0000",
            shape=MarkerShape.CIRCLE,
            text="Test Marker",
        )

        result = series.asdict()
        assert "markers" in result
        assert len(result["markers"]) == 1
        assert result["markers"][0]["time"] == 1640995200
        assert result["markers"][0]["position"] == MarkerPosition.ABOVE_BAR.value
        assert result["markers"][0]["color"] == "#FF0000"
        assert result["markers"][0]["shape"] == MarkerShape.CIRCLE.value
        assert result["markers"][0]["text"] == "Test Marker"

    def test_to_dict_with_price_lines(self):
        """Test to_dict with price lines."""
        data = [BandData(time=1640995200, upper=110.0, middle=105.0, lower=100.0)]
        series = BandSeries(data=data)

        price_line = PriceLineOptions(price=105.0, color="#FF0000")
        series.add_price_line(price_line)

        result = series.asdict()
        assert "priceLines" in result
        assert len(result["priceLines"]) == 1
        assert result["priceLines"][0]["price"] == 105.0
        assert result["priceLines"][0]["color"] == "#FF0000"

    def test_to_dict_complete_structure(self):
        """Test complete to_dict structure."""
        data = [BandData(time=1640995200, upper=110.0, middle=105.0, lower=100.0)]
        series = BandSeries(data=data)

        # Customize all options
        series.upper_line_options.color = "#FF0000"
        series.middle_line_options.color = "#00FF00"
        series.lower_line_options.color = "#0000FF"
        series.upper_fill_color = "rgba(255, 0, 0, 0.5)"
        series.lower_fill_color = "rgba(0, 255, 0, 0.5)"

        result = series.asdict()
        # Check basic structure
        assert "type" in result
        assert "data" in result
        assert "options" in result
        options = result["options"]
        # Check for camelCase keys
        assert options["color"] == "#FF0000"
        assert options["upperFillColor"] == "rgba(255, 0, 0, 0.5)"
        assert options["lowerFillColor"] == "rgba(0, 255, 0, 0.5)"

    def test_method_chaining(self):
        """Test method chaining."""
        data = [BandData(time=1640995200, upper=110.0, middle=105.0, lower=100.0)]
        series = BandSeries(data=data)

        # Test chaining add_marker and add_price_line
        result = series.add_marker(
            1640995200, MarkerPosition.ABOVE_BAR, "#FF0000", MarkerShape.CIRCLE
        ).add_price_line(PriceLineOptions(price=105.0, color="#FF0000"))

        assert result is series
        assert len(series.markers) == 1
        assert len(series.price_lines) == 1


class TestBandSeriesDataHandling:
    """Test cases for BandSeries data handling."""

    def test_from_dataframe_classmethod(self):
        """Test from_dataframe classmethod."""
        df = pd.DataFrame(
            {
                "datetime": [1640995200, 1641081600],
                "upper": [110.0, 112.0],
                "middle": [105.0, 107.0],
                "lower": [100.0, 102.0],
            }
        )

        series = BandSeries.from_dataframe(
            df=df,
            column_mapping={
                "time": "datetime",
                "upper": "upper",
                "middle": "middle",
                "lower": "lower",
            },
        )

        assert len(series.data) == 2
        assert series.data[0].time == 1640995200
        assert series.data[0].upper == 110.0
        assert series.data[1].time == 1641081600
        assert series.data[1].upper == 112.0

    def test_dataframe_with_nan_values(self):
        """Test DataFrame handling with NaN values."""
        df = pd.DataFrame(
            {
                "datetime": [1640995200, 1641081600, 1641168000],
                "upper": [110.0, float("nan"), 108.0],
                "middle": [105.0, 107.0, float("nan")],
                "lower": [100.0, 102.0, 98.0],
            }
        )

        series = BandSeries(
            data=df,
            column_mapping={
                "time": "datetime",
                "upper": "upper",
                "middle": "middle",
                "lower": "lower",
            },
        )

        # NaN values are converted to 0.0, not filtered out
        assert len(series.data) == 3
        assert series.data[0].time == 1640995200
        assert series.data[0].upper == 110.0
        assert series.data[1].upper == 0.0  # NaN converted to 0.0
        assert series.data[2].middle == 0.0  # NaN converted to 0.0


class TestBandSeriesValidation:
    """Test cases for BandSeries validation."""

    def test_validate_pane_config(self):
        """Test validate_pane_config method."""
        data = [BandData(time=1640995200, upper=110.0, middle=105.0, lower=100.0)]
        series = BandSeries(data=data, pane_id=0)
        # Should not raise any exception
        series._validate_pane_config()

    def test_validate_pane_config_invalid(self):
        """Test validate_pane_config with invalid configuration."""
        data = [BandData(time=1640995200, upper=110.0, middle=105.0, lower=100.0)]
        series = BandSeries(data=data, pane_id=-1)

        with pytest.raises(ValueError, match="pane_id must be non-negative"):
            series._validate_pane_config()

    def test_error_handling_invalid_data(self):
        """Test error handling with invalid data."""
        with pytest.raises(ValueError):
            BandSeries(data="invalid_data")

    def test_error_handling_missing_required_columns(self):
        """Test error handling with missing required columns."""
        df = pd.DataFrame(
            {
                "datetime": [1640995200],
                "upper": [110.0],
                # Missing middle and lower columns
            }
        )

        with pytest.raises(ValueError, match="DataFrame is missing required column"):
            BandSeries(
                data=df,
                column_mapping={
                    "time": "datetime",
                    "upper": "upper",
                    "middle": "middle",
                    "lower": "lower",
                },
            )

    def test_error_handling_invalid_data_type(self):
        """Test error handling with invalid data type."""
        with pytest.raises(ValueError, match="data must be a list of SingleValueData objects"):
            BandSeries(data=123)


class TestBandSeriesEdgeCases:
    """Test cases for BandSeries edge cases."""

    def test_empty_data_handling(self):
        """Test handling of empty data."""
        series = BandSeries(data=[])
        assert len(series.data) == 0
        result = series.asdict()
        assert result["data"] == []

    def test_single_data_point(self):
        """Test handling of single data point."""
        data = [BandData(time=1640995200, upper=110.0, middle=105.0, lower=100.0)]
        series = BandSeries(data=data)
        assert len(series.data) == 1
        result = series.asdict()
        assert len(result["data"]) == 1

    def test_large_dataset(self):
        """Test handling of large dataset."""
        data = [
            BandData(
                time=1640995200 + i * 86400, upper=110.0 + i, middle=105.0 + i, lower=100.0 + i
            )
            for i in range(100)
        ]
        series = BandSeries(data=data)
        assert len(series.data) == 100
        result = series.asdict()
        assert len(result["data"]) == 100

    def test_empty_string_colors(self):
        """Test handling of empty string colors."""
        data = [BandData(time=1640995200, upper=110.0, middle=105.0, lower=100.0)]
        series = BandSeries(data=data)

        # Should handle empty strings gracefully
        series.upper_fill_color = ""
        series.lower_fill_color = ""

        result = series.asdict()
        options = result["options"]
        # Empty strings are omitted by base class to_dict
        assert "upperFillColor" not in options
        assert "lowerFillColor" not in options


class TestBandSeriesInheritance:
    """Test cases for BandSeries inheritance."""

    def test_inherits_from_series(self):
        """Test that BandSeries inherits from Series."""
        data = [BandData(time=1640995200, upper=110.0, middle=105.0, lower=100.0)]
        series = BandSeries(data=data)
        assert isinstance(series, Series)

    def test_has_required_methods(self):
        """Test that BandSeries has required methods."""
        data = [BandData(time=1640995200, upper=110.0, middle=105.0, lower=100.0)]
        series = BandSeries(data=data)

        required_methods = [
            "asdict",
            "add_marker",
            "add_price_line",
            "clear_markers",
            "clear_price_lines",
            "set_visible",
        ]

        for method in required_methods:
            assert hasattr(series, method)
            assert callable(getattr(series, method))

    def test_has_required_properties(self):
        """Test that BandSeries has required properties."""
        data = [BandData(time=1640995200, upper=110.0, middle=105.0, lower=100.0)]
        series = BandSeries(data=data)

        required_properties = [
            "chart_type",
            "data",
            "visible",
            "price_scale_id",
            "pane_id",
            "markers",
            "price_lines",
            "price_format",
            "upper_line_options",
            "middle_line_options",
            "lower_line_options",
            "upper_fill_color",
            "lower_fill_color",
        ]

        for prop in required_properties:
            assert hasattr(series, prop)


class TestBandSeriesJsonStructure:
    """Test cases for BandSeries JSON structure."""

    def test_basic_json_structure(self):
        """Test basic JSON structure."""
        data = [BandData(time=1640995200, upper=110.0, middle=105.0, lower=100.0)]
        series = BandSeries(data=data)
        result = series.asdict()

        # Check basic structure
        assert "type" in result
        assert "data" in result
        assert "options" in result

        # Check type
        assert result["type"] == "band"

        # Check data structure
        assert isinstance(result["data"], list)
        assert len(result["data"]) == 1
        data_point = result["data"][0]
        assert "time" in data_point
        assert "upper" in data_point
        assert "middle" in data_point
        assert "lower" in data_point

    def test_band_series_options_structure(self):
        """Test band series options structure."""
        data = [BandData(time=1640995200, upper=110.0, middle=105.0, lower=100.0)]
        series = BandSeries(data=data)
        result = series.asdict()
        options = result["options"]
        # Check for camelCase keys
        for key in ["color", "lineWidth", "lineStyle", "upperFillColor", "lowerFillColor"]:
            assert key in options

    def test_markers_json_structure(self):
        """Test markers JSON structure."""
        data = [BandData(time=1640995200, upper=110.0, middle=105.0, lower=100.0)]
        series = BandSeries(data=data)

        series.add_marker(
            time=1640995200,
            position=MarkerPosition.ABOVE_BAR,
            color="#FF0000",
            shape=MarkerShape.CIRCLE,
            text="Test Marker",
            size=10,
        )

        result = series.asdict()
        assert "markers" in result
        markers = result["markers"]
        assert isinstance(markers, list)
        assert len(markers) == 1

        marker = markers[0]
        expected_keys = {"time", "position", "color", "shape", "text", "size"}
        assert set(marker.keys()) == expected_keys

    def test_price_lines_json_structure(self):
        """Test price lines JSON structure."""
        data = [BandData(time=1640995200, upper=110.0, middle=105.0, lower=100.0)]
        series = BandSeries(data=data)

        series.add_price_line(PriceLineOptions(price=105.0, color="#FF0000", line_width=2))

        result = series.asdict()
        assert "priceLines" in result
        price_lines = result["priceLines"]
        assert isinstance(price_lines, list)
        assert len(price_lines) == 1

        price_line = price_lines[0]
        # PriceLineOptions has many more keys than expected
        expected_keys = {"price", "color", "lineWidth", "lineStyle", "axisLabelVisible"}
        for key in expected_keys:
            assert key in price_line, f"Expected key {key} not found in price line"

    def test_complete_json_structure(self):
        """Test complete JSON structure with all options."""
        data = [BandData(time=1640995200, upper=110.0, middle=105.0, lower=100.0)]
        series = BandSeries(data=data)
        # Add markers and price lines
        series.add_marker(1640995200, MarkerPosition.ABOVE_BAR, "#FF0000", MarkerShape.CIRCLE)
        series.add_price_line(PriceLineOptions(price=105.0, color="#FF0000"))
        # Customize all options
        series.upper_line_options.color = "#FF0000"
        series.middle_line_options.color = "#00FF00"
        series.lower_line_options.color = "#0000FF"
        series.upper_fill_color = "rgba(255, 0, 0, 0.5)"
        series.lower_fill_color = "rgba(0, 255, 0, 0.5)"
        result = series.asdict()
        # Check all expected keys
        assert "type" in result
        assert "data" in result
        assert "options" in result
        assert "markers" in result
        assert "priceLines" in result
        options = result["options"]
        assert options["color"] == "#FF0000"
        assert options["upperFillColor"] == "rgba(255, 0, 0, 0.5)"
        assert options["lowerFillColor"] == "rgba(0, 255, 0, 0.5)"

    def test_json_serialization_consistency(self):
        """Test JSON serialization consistency."""
        data = [BandData(time=1640995200, upper=110.0, middle=105.0, lower=100.0)]
        series = BandSeries(data=data)
        # Serialize multiple times
        result1 = series.asdict()
        result2 = series.asdict()
        assert result1 == result2
        # Modify options and serialize again
        series.upper_line_options.color = "#FF0000"
        result3 = series.asdict()
        assert result1 != result3
        assert result3["options"]["color"] == "#FF0000"

    def test_frontend_compatibility(self):
        """Test frontend compatibility of JSON structure."""
        data = [BandData(time=1640995200, upper=110.0, middle=105.0, lower=100.0)]
        series = BandSeries(data=data)
        result = series.asdict()
        # Check that all option keys are camelCase
        for key in result["options"].keys():
            assert key[0].islower() and not "_" in key, f"Key {key} is not camelCase"

    def test_empty_options_handling(self):
        """Test handling of empty options."""
        data = [BandData(time=1640995200, upper=110.0, middle=105.0, lower=100.0)]
        series = BandSeries(data=data)
        # Set empty strings for colors
        series.upper_fill_color = ""
        series.lower_fill_color = ""
        result = series.asdict()
        options = result["options"]
        # Empty strings are omitted by base class to_dict
        assert "upperFillColor" not in options
        assert "lowerFillColor" not in options

    def test_missing_optional_fields(self):
        """Test handling of missing optional fields."""
        data = [BandData(time=1640995200, upper=110.0, middle=105.0, lower=100.0)]
        series = BandSeries(data=data)
        result = series.asdict()
        # Should not include markers or price lines if not present
        assert "markers" not in result
        assert "priceLines" not in result
        # Should include all required options
        for option in ["color", "lineWidth", "lineStyle", "upperFillColor", "lowerFillColor"]:
            assert option in result["options"]
