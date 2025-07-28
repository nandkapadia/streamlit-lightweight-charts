"""
Unit tests for LineSeries JSON format validation.

This module tests that the LineSeries.asdict() method produces JSON
in the exact format expected by the frontend React component.
"""

import json

from streamlit_lightweight_charts_pro.charts.options.line_options import LineOptions
from streamlit_lightweight_charts_pro.charts.options.price_line_options import PriceLineOptions
from streamlit_lightweight_charts_pro.charts.series.line import LineSeries
from streamlit_lightweight_charts_pro.data.line_data import LineData
from streamlit_lightweight_charts_pro.type_definitions.enums import (
    LastPriceAnimationMode,
    LineStyle,
    LineType,
    MarkerPosition,
    MarkerShape,
)


class TestLineSeriesJsonFormat:
    """Test cases for LineSeries JSON format and frontend compatibility."""

    def test_line_series_basic_json_structure(self):
        """Test basic JSON structure matches frontend SeriesConfig interface."""
        # Create test data
        data = [
            LineData(time=1704067200, value=100.0),
            LineData(time=1704153600, value=105.0),
            LineData(time=1704240000, value=102.0),
        ]

        line_options = LineOptions(color="#2196f3", line_width=2)
        series = LineSeries(data=data)

        result = series.asdict()

        # Check required fields from SeriesConfig interface
        assert "type" in result
        assert result["type"] == "line"
        assert "data" in result
        assert isinstance(result["data"], list)
        assert len(result["data"]) == 3

        # Check data structure
        assert result["data"][0]["time"] == 1704067200
        assert result["data"][0]["value"] == 100.0
        assert result["data"][1]["time"] == 1704153600
        assert result["data"][1]["value"] == 105.0
        assert result["data"][2]["time"] == 1704240000
        assert result["data"][2]["value"] == 102.0

        # Check options structure
        assert "options" in result
        options = result["options"]
        assert options["color"] == "#2196f3"
        assert options["lineWidth"] == 2

        # Check other required fields
        assert "pane_id" in result
        assert result["pane_id"] == 0

    def test_line_series_options_json_structure(self):
        """Test line series options match frontend expectations."""
        data = [LineData(time=1704067200, value=100.0)]

        # Create comprehensive line options
        line_options = LineOptions(
            color="#ff0000",
            line_style=LineStyle.DASHED,
            line_width=3,
            line_type=LineType.CURVED,
            line_visible=True,
            point_markers_visible=True,
            point_markers_radius=5,
            crosshair_marker_visible=True,
            crosshair_marker_radius=4,
            crosshair_marker_border_color="#000000",
            crosshair_marker_background_color="#ffffff",
            crosshair_marker_border_width=2,
            last_price_animation=LastPriceAnimationMode.CONTINUOUS,
        )

        series = LineSeries(data=data)
        result = series.asdict()

        # Check options structure
        options = result["options"]
        assert options["color"] == "#ff0000"
        assert options["lineStyle"] == 2  # LineStyle.DASHED.value
        assert options["lineWidth"] == 3
        assert options["lineType"] == 1  # LineType.CURVED.value
        assert options["lineVisible"] is True
        assert options["pointMarkersVisible"] is True
        assert options["pointMarkersRadius"] == 5
        assert options["crosshairMarkerVisible"] is True
        assert options["crosshairMarkerRadius"] == 4
        assert options["crosshairMarkerBorderColor"] == "#000000"
        assert options["crosshairMarkerBackgroundColor"] == "#ffffff"
        assert options["crosshairMarkerBorderWidth"] == 2
        assert options["lastPriceAnimation"] == 1  # LastPriceAnimationMode.CONTINUOUS.value

    def test_line_series_with_price_lines_json_structure(self):
        """Test line series with price lines JSON structure."""
        data = [LineData(time=1704067200, value=100.0)]
        line_options = LineOptions(color="#2196f3")
        series = LineSeries(data=data)

        # Add price lines
        resistance = PriceLineOptions(
            price=108.0,
            color="#F44336",
            line_width=2,
            line_style=LineStyle.DASHED,
            title="Resistance",
        )
        support = PriceLineOptions(
            price=95.0, color="#4CAF50", line_width=2, line_style=LineStyle.DASHED, title="Support"
        )
        series.add_price_line(resistance).add_price_line(support)

        result = series.asdict()

        # Check price lines structure
        assert "priceLines" in result
        assert len(result["priceLines"]) == 2

        # Check first price line
        price_line1 = result["priceLines"][0]
        assert price_line1["price"] == 108.0
        assert price_line1["color"] == "#F44336"
        assert price_line1["lineWidth"] == 2
        assert price_line1["lineStyle"] == 2  # LineStyle.DASHED.value
        assert price_line1["title"] == "Resistance"

        # Check second price line
        price_line2 = result["priceLines"][1]
        assert price_line2["price"] == 95.0
        assert price_line2["color"] == "#4CAF50"
        assert price_line2["lineWidth"] == 2
        assert price_line2["lineStyle"] == 2  # LineStyle.DASHED.value
        assert price_line2["title"] == "Support"

    def test_line_series_with_markers_json_structure(self):
        """Test line series with markers JSON structure."""
        data = [LineData(time=1704067200, value=100.0)]
        line_options = LineOptions(color="#2196f3")
        series = LineSeries(data=data)

        # Add markers
        series.add_marker(
            time=1704067200,
            position=MarkerPosition.ABOVE_BAR,
            color="#ff0000",
            shape=MarkerShape.CIRCLE,
            text="Peak",
            size=10,
        )

        series.add_marker(
            time=1704153600,
            position=MarkerPosition.BELOW_BAR,
            color="#00ff00",
            shape=MarkerShape.SQUARE,
            text="Valley",
            size=8,
        )

        result = series.asdict()

        # Check markers structure
        assert "markers" in result
        assert len(result["markers"]) == 2

        # Check first marker
        marker1 = result["markers"][0]
        assert marker1["time"] == 1704067200
        assert marker1["position"] == "aboveBar"
        assert marker1["color"] == "#ff0000"
        assert marker1["shape"] == "circle"
        assert marker1["text"] == "Peak"
        assert marker1["size"] == 10

        # Check second marker
        marker2 = result["markers"][1]
        assert marker2["time"] == 1704153600
        assert marker2["position"] == "belowBar"
        assert marker2["color"] == "#00ff00"
        assert marker2["shape"] == "square"
        assert marker2["text"] == "Valley"
        assert marker2["size"] == 8

    def test_line_series_json_serialization(self):
        """Test that JSON serialization works correctly."""
        data = [LineData(time=1704067200, value=100.0)]
        line_options = LineOptions(color="#2196f3")
        series = LineSeries(data=data)

        result = series.asdict()

        # Test JSON serialization
        json_str = json.dumps(result)
        assert isinstance(json_str, str)

        # Test JSON parsing
        parsed = json.loads(json_str)
        assert parsed["type"] == "line"
        assert len(parsed["data"]) == 1
        assert parsed["data"][0]["time"] == 1704067200
        assert parsed["data"][0]["value"] == 100.0

    def test_line_series_frontend_compatibility(self):
        """Test that the JSON structure is compatible with frontend SeriesConfig interface."""
        data = [LineData(time=1704067200, value=100.0)]
        line_options = LineOptions(color="#2196f3")
        series = LineSeries(data=data)

        result = series.asdict()

        # Frontend expects these fields in SeriesConfig
        assert "type" in result
        assert "data" in result
        assert "options" in result
        assert "pane_id" in result

        # Type should be lowercase to match frontend expectations
        assert result["type"] == "line"

        # Data should be an array
        assert isinstance(result["data"], list)

        # Options should be an object
        assert isinstance(result["options"], dict)

        # pane_id should be a number
        assert isinstance(result["pane_id"], int)

    def test_line_series_empty_data_handling(self):
        """Test that empty data is handled correctly."""
        line_options = LineOptions(color="#2196f3")
        series = LineSeries(data=[])

        result = series.asdict()

        assert result["type"] == "line"
        assert result["data"] == []
        assert isinstance(result["options"], dict)
        # priceLines should only be present when price lines are added

    def test_line_series_nan_handling(self):
        """Test that NaN values are handled correctly in JSON output."""
        data = [
            LineData(time=1704067200, value=100.0),
            LineData(time=1704153600, value=float("nan")),  # This should become 0.0
            LineData(time=1704240000, value=102.0),
        ]

        line_options = LineOptions()
        series = LineSeries(data=data)

        result = series.asdict()

        # NaN should be converted to 0.0 in SingleValueData.__post_init__
        assert result["data"][0]["value"] == 100.0
        assert result["data"][1]["value"] == 0.0  # NaN converted to 0.0
        assert result["data"][2]["value"] == 102.0

    def test_line_series_actual_json_output(self):
        """Test the actual JSON output format to verify frontend compatibility."""
        # Create test data with various scenarios
        data = [
            LineData(time=1704067200, value=100.0),  # No color
            LineData(time=1704153600, value=105.0, color="#ff0000"),  # With color
            LineData(time=1704240000, value=102.0),  # No color
        ]

        # Create line options with all properties
        line_options = LineOptions(
            color="#2196f3",
            line_style=LineStyle.DASHED,
            line_width=2,
            line_type=LineType.CURVED,
            line_visible=True,
            point_markers_visible=True,
            point_markers_radius=5,
            crosshair_marker_visible=True,
            crosshair_marker_radius=4,
            crosshair_marker_border_color="#000000",
            crosshair_marker_background_color="#ffffff",
            crosshair_marker_border_width=2,
            last_price_animation=LastPriceAnimationMode.CONTINUOUS,
        )

        # Create series
        series = LineSeries(data=data)

        # Add a price line
        price_line = PriceLineOptions(
            price=110.0,
            color="#4CAF50",
            line_width=2,
            line_style=LineStyle.SOLID,
            line_visible=True,
            axis_label_visible=True,
            title="Resistance Level",
        )
        series.add_price_line(price_line)

        # Get JSON representation
        result = series.asdict()

        # Print the actual JSON for inspection
        json_str = json.dumps(result, indent=2)
        print(f"\nActual JSON output:\n{json_str}")

        # Verify the structure matches frontend expectations
        expected_structure = {
            "type": "line",
            "data": [
                {"time": 1704067200, "value": 100.0},  # No color field
                {"time": 1704153600, "value": 105.0, "color": "#ff0000"},  # With color
                {"time": 1704240000, "value": 102.0},  # No color field
            ],
            "options": {
                "color": "#2196f3",
                "lineStyle": 2,  # LineStyle.DASHED.value
                "lineWidth": 2,
                "lineType": 1,  # LineType.CURVED.value
                "lineVisible": True,
                "pointMarkersVisible": True,
                "pointMarkersRadius": 5,
                "crosshairMarkerVisible": True,
                "crosshairMarkerRadius": 4,
                "crosshairMarkerBorderColor": "#000000",
                "crosshairMarkerBackgroundColor": "#ffffff",
                "crosshairMarkerBorderWidth": 2,
                "lastPriceAnimation": 1,  # LastPriceAnimationMode.CONTINUOUS.value
            },
            "priceLines": [
                {
                    "id": None,
                    "price": 110.0,
                    "color": "#4CAF50",
                    "lineWidth": 2,
                    "lineStyle": 1,  # LineStyle.SOLID.value
                    "lineVisible": True,
                    "axisLabelVisible": True,
                    "title": "Resistance Level",
                }
            ],
            "pane_id": 0,
        }

        # Verify key structure matches
        assert result["type"] == expected_structure["type"]
        assert result["data"] == expected_structure["data"]
        assert result["options"]["color"] == expected_structure["options"]["color"]
        assert result["options"]["lineStyle"] == expected_structure["options"]["lineStyle"]
        assert result["priceLines"][0]["price"] == expected_structure["priceLines"][0]["price"]
        assert result["pane_id"] == expected_structure["pane_id"]
