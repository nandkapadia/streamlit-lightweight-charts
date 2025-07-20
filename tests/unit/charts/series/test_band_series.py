"""Unit tests for BandSeries."""

import pytest
import pandas as pd
from datetime import datetime

from streamlit_lightweight_charts_pro.charts.series.band import BandSeries
from streamlit_lightweight_charts_pro.data import BandData
from streamlit_lightweight_charts_pro.type_definitions import LineStyle, LineType, LastPriceAnimationMode


class TestBandSeries:
    """Test cases for BandSeries."""

    def setup_method(self):
        """Set up test data."""
        # Create sample band data
        self.band_data = [
            BandData("2024-01-01", 105.0, 100.0, 95.0),
            BandData("2024-01-02", 107.0, 102.0, 97.0),
            BandData("2024-01-03", 103.0, 98.0, 93.0),
        ]

        # Create sample DataFrame
        self.df_data = pd.DataFrame({
            "datetime": ["2024-01-01", "2024-01-02", "2024-01-03"],
            "upper": [105.0, 107.0, 103.0],
            "middle": [100.0, 102.0, 98.0],
            "lower": [95.0, 97.0, 93.0],
        })

    def test_band_series_creation_with_data_objects(self):
        """Test creating BandSeries with BandData objects."""
        series = BandSeries(data=self.band_data)
        
        assert len(series.data) == 3
        assert series.data[0].upper == 105.0
        assert series.data[0].middle == 100.0
        assert series.data[0].lower == 95.0
        assert series.chart_type.value == "Band"

    def test_band_series_creation_with_dataframe(self):
        """Test creating BandSeries with pandas DataFrame."""
        series = BandSeries(data=self.df_data)
        
        assert len(series.data) == 3
        assert series.data[0].upper == 105.0
        assert series.data[0].middle == 100.0
        assert series.data[0].lower == 95.0

    def test_band_series_creation_with_custom_column_mapping(self):
        """Test creating BandSeries with custom column mapping."""
        custom_df = pd.DataFrame({
            "date": ["2024-01-01", "2024-01-02", "2024-01-03"],
            "u": [105.0, 107.0, 103.0],
            "m": [100.0, 102.0, 98.0],
            "l": [95.0, 97.0, 93.0],
        })
        
        column_mapping = {
            "time": "date",
            "upper": "u",
            "middle": "m",
            "lower": "l",
        }
        
        series = BandSeries(data=custom_df, column_mapping=column_mapping)
        
        assert len(series.data) == 3
        assert series.data[0].upper == 105.0
        assert series.data[0].middle == 100.0
        assert series.data[0].lower == 95.0

    def test_band_series_default_options(self):
        """Test BandSeries default options."""
        series = BandSeries(data=self.band_data)
        
        # Test default line colors
        assert series.upper_line_color == "#4CAF50"
        assert series.middle_line_color == "#2196F3"
        assert series.lower_line_color == "#F44336"
        
        # Test default line widths
        assert series.upper_line_width == 2
        assert series.middle_line_width == 2
        assert series.lower_line_width == 2
        
        # Test default line styles
        assert series.upper_line_style == LineStyle.SOLID
        assert series.middle_line_style == LineStyle.SOLID
        assert series.lower_line_style == LineStyle.SOLID
        
        # Test default fill colors
        assert series.upper_fill_color == "rgba(76, 175, 80, 0.1)"
        assert series.lower_fill_color == "rgba(244, 67, 54, 0.1)"
        
        # Test default line type
        assert series.line_type == LineType.SIMPLE

    def test_band_series_custom_options(self):
        """Test BandSeries with custom options."""
        series = BandSeries(
            data=self.band_data,
            upper_line_color="#FF0000",
            middle_line_color="#00FF00",
            lower_line_color="#0000FF",
            upper_line_width=3,
            middle_line_width=4,
            lower_line_width=5,
            upper_line_style=LineStyle.DASHED,
            middle_line_style=LineStyle.DOTTED,
            lower_line_style=LineStyle.LARGE_DASHED,
            upper_fill_color="rgba(255, 0, 0, 0.2)",
            lower_fill_color="rgba(0, 0, 255, 0.2)",
            line_type=LineType.CURVED,
        )
        
        # Test custom line colors
        assert series.upper_line_color == "#FF0000"
        assert series.middle_line_color == "#00FF00"
        assert series.lower_line_color == "#0000FF"
        
        # Test custom line widths
        assert series.upper_line_width == 3
        assert series.middle_line_width == 4
        assert series.lower_line_width == 5
        
        # Test custom line styles
        assert series.upper_line_style == LineStyle.DASHED
        assert series.middle_line_style == LineStyle.DOTTED
        assert series.lower_line_style == LineStyle.LARGE_DASHED
        
        # Test custom fill colors
        assert series.upper_fill_color == "rgba(255, 0, 0, 0.2)"
        assert series.lower_fill_color == "rgba(0, 0, 255, 0.2)"
        
        # Test custom line type
        assert series.line_type == LineType.CURVED

    def test_band_series_line_visibility(self):
        """Test BandSeries line visibility options."""
        series = BandSeries(
            data=self.band_data,
            upper_line_visible=False,
            middle_line_visible=True,
            lower_line_visible=False,
        )
        
        assert series.upper_line_visible is False
        assert series.middle_line_visible is True
        assert series.lower_line_visible is False

    def test_band_series_crosshair_markers(self):
        """Test BandSeries crosshair marker options."""
        series = BandSeries(
            data=self.band_data,
            crosshair_marker_visible=False,
            crosshair_marker_radius=6,
            crosshair_marker_border_color="#FF0000",
            crosshair_marker_background_color="#00FF00",
            crosshair_marker_border_width=3,
        )
        
        assert series.crosshair_marker_visible is False
        assert series.crosshair_marker_radius == 6
        assert series.crosshair_marker_border_color == "#FF0000"
        assert series.crosshair_marker_background_color == "#00FF00"
        assert series.crosshair_marker_border_width == 3

    def test_band_series_animation(self):
        """Test BandSeries animation options."""
        series = BandSeries(
            data=self.band_data,
            last_price_animation=LastPriceAnimationMode.CONTINUOUS,
        )
        
        assert series.last_price_animation == LastPriceAnimationMode.CONTINUOUS

    def test_band_series_to_frontend_config(self):
        """Test BandSeries frontend configuration generation."""
        series = BandSeries(data=self.band_data)
        config = series.to_frontend_config()
        
        assert config["type"] == "band"
        assert len(config["data"]) == 3
        assert "options" in config
        
        # Test data structure
        assert config["data"][0]["time"] == 1704067200  # Unix timestamp
        assert config["data"][0]["upper"] == 105.0
        assert config["data"][0]["middle"] == 100.0
        assert config["data"][0]["lower"] == 95.0

    def test_band_series_options_dict(self):
        """Test BandSeries options dictionary generation."""
        series = BandSeries(data=self.band_data)
        options = series._get_options_dict()
        
        # Test basic options
        assert options["visible"] is True
        assert options["priceScaleId"] == "right"
        
        # Test line colors
        assert options["upperLineColor"] == "#4CAF50"
        assert options["middleLineColor"] == "#2196F3"
        assert options["lowerLineColor"] == "#F44336"
        
        # Test line widths
        assert options["upperLineWidth"] == 2
        assert options["middleLineWidth"] == 2
        assert options["lowerLineWidth"] == 2
        
        # Test line styles
        assert options["upperLineStyle"] == 0  # SOLID
        assert options["middleLineStyle"] == 0  # SOLID
        assert options["lowerLineStyle"] == 0  # SOLID
        
        # Test fill colors
        assert options["upperFillColor"] == "rgba(76, 175, 80, 0.1)"
        assert options["lowerFillColor"] == "rgba(244, 67, 54, 0.1)"
        
        # Test line type
        assert options["lineType"] == 0  # SIMPLE

    def test_band_series_with_markers(self):
        """Test BandSeries with markers."""
        from streamlit_lightweight_charts_pro.data import Marker, MarkerPosition, MarkerShape
        
        markers = [
            Marker(
                time="2024-01-02",
                position=MarkerPosition.ABOVE_BAR,
                color="#FF0000",
                shape=MarkerShape.CIRCLE,
                text="Signal",
            )
        ]
        
        series = BandSeries(data=self.band_data, markers=markers)
        config = series.to_frontend_config()
        
        assert "markers" in config
        assert len(config["markers"]) == 1
        assert config["markers"][0]["text"] == "Signal"

    def test_band_series_dataframe_missing_columns(self):
        """Test BandSeries with DataFrame missing required columns."""
        invalid_df = pd.DataFrame({
            "datetime": ["2024-01-01", "2024-01-02"],
            "upper": [105.0, 107.0],
            # Missing middle and lower columns
        })
        
        with pytest.raises(ValueError, match="DataFrame must contain columns"):
            BandSeries(data=invalid_df)

    def test_band_series_dataframe_invalid_data_types(self):
        """Test BandSeries with DataFrame containing invalid data types."""
        invalid_df = pd.DataFrame({
            "datetime": ["2024-01-01", "2024-01-02"],
            "upper": ["invalid", "invalid"],  # Should be numeric
            "middle": [100.0, 102.0],
            "lower": [95.0, 97.0],
        })
        
        # Should raise ValueError for invalid data types
        with pytest.raises(ValueError, match="could not convert string to float"):
            BandSeries(data=invalid_df)

    def test_band_series_method_chaining(self):
        """Test BandSeries method chaining."""
        series = BandSeries(data=self.band_data)
        
        # Test setting price scale
        result = series.set_price_scale("left")
        assert result is series
        assert series.price_scale_id == "left"
        
        # Test setting price line
        result = series.set_price_line(visible=True, color="#FF0000")
        assert result is series
        assert series.price_line_visible is True
        assert series.price_line_color == "#FF0000"
        
        # Test setting base line
        result = series.set_base_line(visible=True, color="#00FF00")
        assert result is series
        assert series.base_line_visible is True
        assert series.base_line_color == "#00FF00"

    def test_band_series_price_format(self):
        """Test BandSeries price format configuration."""
        series = BandSeries(
            data=self.band_data,
            price_format={"type": "price", "precision": 4, "minMove": 0.0001},
        )
        
        assert series.price_format["type"] == "price"
        assert series.price_format["precision"] == 4
        assert series.price_format["minMove"] == 0.0001

    def test_band_series_price_scale_config(self):
        """Test BandSeries price scale configuration."""
        price_scale_config = {
            "visible": True,
            "ticksVisible": True,
            "borderVisible": True,
        }
        
        series = BandSeries(
            data=self.band_data,
            price_scale_config=price_scale_config,
        )
        
        assert series.price_scale_config == price_scale_config

    def test_band_series_add_marker(self):
        """Test BandSeries add_marker method."""
        series = BandSeries(data=self.band_data)
        
        result = series.add_marker(
            time="2024-01-02",
            position="aboveBar",
            color="#FF0000",
            shape="circle",
            text="Test Marker",
            size=12,
        )
        
        assert result is series
        assert len(series.markers) == 1
        assert series.markers[0].text == "Test Marker"
        assert series.markers[0].size == 12

    def test_band_series_add_markers(self):
        """Test BandSeries add_markers method."""
        from streamlit_lightweight_charts_pro.data import Marker, MarkerPosition, MarkerShape
        
        series = BandSeries(data=self.band_data)
        
        markers = [
            Marker(
                time="2024-01-01",
                position=MarkerPosition.ABOVE_BAR,
                color="#FF0000",
                shape=MarkerShape.CIRCLE,
                text="Marker 1",
            ),
            Marker(
                time="2024-01-03",
                position=MarkerPosition.BELOW_BAR,
                color="#00FF00",
                shape=MarkerShape.SQUARE,
                text="Marker 2",
            ),
        ]
        
        result = series.add_markers(markers)
        assert result is series
        assert len(series.markers) == 2

    def test_band_series_clear_markers(self):
        """Test BandSeries clear_markers method."""
        series = BandSeries(data=self.band_data)
        
        # Add a marker first
        series.add_marker(
            time="2024-01-02",
            position="aboveBar",
            color="#FF0000",
            shape="circle",
        )
        
        assert len(series.markers) == 1
        
        # Clear markers
        result = series.clear_markers()
        assert result is series
        assert len(series.markers) == 0

    def test_band_series_set_price_scale_config(self):
        """Test BandSeries set_price_scale_config method."""
        series = BandSeries(data=self.band_data)
        
        result = series.set_price_scale_config(
            visible=True,
            ticksVisible=True,
            borderVisible=True,
        )
        
        assert result is series
        assert series.price_scale_config["visible"] is True
        assert series.price_scale_config["ticksVisible"] is True
        assert series.price_scale_config["borderVisible"] is True

    def test_band_series_get_data_range(self):
        """Test BandSeries get_data_range method."""
        series = BandSeries(data=self.band_data)
        
        data_range = series.get_data_range()
        
        assert data_range is not None
        assert "min_value" in data_range
        assert "max_value" in data_range
        assert "min_time" in data_range
        assert "max_time" in data_range
        assert data_range["min_value"] == 93.0  # Lowest value (lower band)
        assert data_range["max_value"] == 107.0  # Highest value (upper band) 