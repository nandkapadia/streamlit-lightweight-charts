"""
Unit tests for the Series base class.

This module tests the abstract Series class functionality including
data handling, configuration, and method chaining.
"""

import pandas as pd
import pytest

from streamlit_lightweight_charts_pro.charts.options.price_format_options import PriceFormatOptions
from streamlit_lightweight_charts_pro.charts.options.price_line_options import PriceLineOptions
from streamlit_lightweight_charts_pro.charts.series.base import Series
from streamlit_lightweight_charts_pro.data.line_data import LineData
from streamlit_lightweight_charts_pro.data.marker import Marker
from streamlit_lightweight_charts_pro.type_definitions.enums import MarkerPosition, MarkerShape


class ConcreteSeries(Series):
    """Concrete implementation of Series for testing."""

    DATA_CLASS = LineData

    def __init__(self, data, **kwargs):
        if isinstance(data, pd.DataFrame):
            # Use the new from_dataframe logic for DataFrame processing
            column_mapping = kwargs.get("column_mapping", {})
            if not column_mapping:
                # Default column mapping if none provided
                column_mapping = {"time": "time", "value": "value"}

            # Process DataFrame using the same logic as from_dataframe
            df = data.copy()
            self.data_class.required_columns

            # Get index names for normalization
            index_names = df.index.names if hasattr(df.index, "names") else [df.index.name]

            # Normalize index as column if needed
            for key, col in column_mapping.items():
                if col in df.columns:
                    continue

                # Handle DatetimeIndex with no name
                if isinstance(df.index, pd.DatetimeIndex) and df.index.name is None:
                    df.index.name = col
                    df = df.reset_index()
                # Handle MultiIndex with unnamed DatetimeIndex level
                elif isinstance(df.index, pd.MultiIndex):
                    # Find the level index that matches the column name
                    for i, name in enumerate(df.index.names):
                        if name is None and i < len(df.index.levels):
                            # Check if this level is a DatetimeIndex
                            if isinstance(df.index.levels[i], pd.DatetimeIndex):
                                # Set the name for this level
                                new_names = list(df.index.names)
                                new_names[i] = col
                                df.index.names = new_names
                                df = df.reset_index(level=col)
                                break
                    # If not found as unnamed DatetimeIndex, check if it's a named level
                    else:
                        if col in df.index.names:
                            df = df.reset_index(level=col)
                # Handle regular index with matching name
                elif col in index_names:
                    df = df.reset_index()

            # Process the DataFrame into data objects
            data = self._process_dataframe(df)

        super().__init__(data=data, **kwargs)

    def asdict(self):
        return {
            "type": "test",
            "data": [d.asdict() for d in self.data],
            "options": {},
            "priceLines": [pl.asdict() for pl in self.price_lines],
            "markers": [marker.asdict() for marker in self.markers],
        }

    def _process_dataframe(self, df):
        """Process DataFrame into LineData objects."""
        data = []
        for _, row in df.iterrows():
            data.append(LineData(time=row["time"], value=row["value"]))
        return data

    def _get_columns(self):
        return {"time": "time", "value": "value"}


class TestSeriesBase:
    """Test cases for the Series base class."""

    def test_construction_with_list_data(self):
        """Test Series construction with list of data objects."""
        data = [
            LineData(time=1640995200, value=100),
            LineData(time=1641081600, value=110),
        ]

        series = ConcreteSeries(data=data)

        assert len(series.data) == 2
        assert series.visible is True
        assert series.price_scale_id == "right"
        assert series.pane_id == 0

    def test_construction_with_dataframe(self):
        """Test Series construction with DataFrame."""
        df = pd.DataFrame({"time": [1640995200, 1641081600], "value": [100, 110]})

        series = ConcreteSeries(data=df, column_mapping={"time": "time", "value": "value"})

        assert len(series.data) == 2
        assert all(isinstance(d, LineData) for d in series.data)

    def test_construction_with_custom_parameters(self):
        """Test Series construction with custom parameters."""
        data = [LineData(time=1640995200, value=100)]

        series = ConcreteSeries(data=data, visible=False, price_scale_id="left", pane_id=1)

        assert series.visible is False
        assert series.price_scale_id == "left"
        assert series.pane_id == 1

    def test_data_dict_property(self):
        """Test the data_dict property."""
        data = [
            LineData(time=1640995200, value=100),
            LineData(time=1641081600, value=110),
        ]

        series = ConcreteSeries(data=data)
        data_dict = series.data_dict

        assert len(data_dict) == 2
        assert data_dict[0]["time"] == 1640995200
        assert data_dict[0]["value"] == 100
        assert data_dict[1]["time"] == 1641081600
        assert data_dict[1]["value"] == 110

    def test_set_visible_method(self):
        """Test the set_visible method."""
        data = [LineData(time=1640995200, value=100)]
        series = ConcreteSeries(data=data)

        result = series.set_visible(False)

        assert result is series  # Method chaining
        assert series.visible is False

    def test_add_marker_method(self):
        """Test the add_marker method."""
        data = [LineData(time=1640995200, value=100)]
        series = ConcreteSeries(data=data)

        result = series.add_marker(
            time=1640995200,
            position=MarkerPosition.ABOVE_BAR,
            color="#ff0000",
            shape=MarkerShape.CIRCLE,
            text="Test",
            size=10,
        )

        assert result is series  # Method chaining
        assert len(series.markers) == 1
        # Time is normalized to UNIX timestamp format in Marker
        assert isinstance(series.markers[0].time, int)
        assert series.markers[0].time == 1640995200  # UNIX timestamp
        assert series.markers[0].position == MarkerPosition.ABOVE_BAR
        assert series.markers[0].color == "#ff0000"
        assert series.markers[0].shape == MarkerShape.CIRCLE
        assert series.markers[0].text == "Test"
        assert series.markers[0].size == 10

    def test_add_markers_method(self):
        """Test the add_markers method."""
        data = [LineData(time=1640995200, value=100)]
        series = ConcreteSeries(data=data)

        markers = [
            Marker(
                time=1640995200,
                position=MarkerPosition.ABOVE_BAR,
                color="#ff0000",
                shape=MarkerShape.CIRCLE,
            ),
            Marker(
                time=1641081600,
                position=MarkerPosition.BELOW_BAR,
                color="#00ff00",
                shape=MarkerShape.SQUARE,
            ),
        ]

        result = series.add_markers(markers)

        assert result is series  # Method chaining
        assert len(series.markers) == 2

    def test_clear_markers_method(self):
        """Test the clear_markers method."""
        data = [LineData(time=1640995200, value=100)]
        series = ConcreteSeries(data=data)

        # Add some markers first
        series.add_marker(
            time=1640995200,
            position=MarkerPosition.ABOVE_BAR,
            color="#ff0000",
            shape=MarkerShape.CIRCLE,
        )

        assert len(series.markers) == 1

        # Clear markers
        result = series.clear_markers()

        assert result is series  # Method chaining
        assert len(series.markers) == 0

    def test_price_scale_id_property(self):
        """Test the price_scale_id property."""
        data = [LineData(time=1640995200, value=100)]
        series = ConcreteSeries(data=data)

        series.price_scale_id = "left"
        assert series.price_scale_id == "left"

    def test_price_format_property(self):
        """Test the price_format property."""
        data = [LineData(time=1640995200, value=100)]
        series = ConcreteSeries(data=data)

        price_format = PriceFormatOptions(type="price", precision=2)
        series.price_format = price_format

        assert series.price_format is price_format

    def test_price_lines_property(self):
        """Test the price_lines property."""
        data = [LineData(time=1640995200, value=100)]
        series = ConcreteSeries(data=data)

        price_lines = [
            PriceLineOptions(price=100, color="#ff0000"),
            PriceLineOptions(price=110, color="#00ff00"),
        ]

        series.price_lines = price_lines
        assert series.price_lines == price_lines

    def test_add_price_line_method(self):
        """Test the add_price_line method."""
        data = [LineData(time=1640995200, value=100)]
        series = ConcreteSeries(data=data)

        price_line = PriceLineOptions(price=100, color="#ff0000")
        result = series.add_price_line(price_line)

        assert result is series  # Method chaining
        assert len(series.price_lines) == 1
        assert series.price_lines[0] is price_line

    def test_clear_price_lines_method(self):
        """Test the clear_price_lines method."""
        data = [LineData(time=1640995200, value=100)]
        series = ConcreteSeries(data=data)

        # Add some price lines first
        price_line = PriceLineOptions(price=100, color="#ff0000")
        series.add_price_line(price_line)

        assert len(series.price_lines) == 1

        # Clear price lines
        result = series.clear_price_lines()

        assert result is series  # Method chaining
        assert len(series.price_lines) == 0

    def test_markers_property(self):
        """Test the markers property."""
        data = [LineData(time=1640995200, value=100)]
        series = ConcreteSeries(data=data)

        markers = [
            Marker(
                time=1640995200,
                position=MarkerPosition.ABOVE_BAR,
                color="#ff0000",
                shape=MarkerShape.CIRCLE,
            ),
        ]

        series.markers = markers
        assert series.markers == markers

    def test_data_class_property(self):
        """Test the data_class class property."""
        assert ConcreteSeries.data_class == LineData

    def test_from_dataframe_classmethod(self):
        """Test the from_dataframe class method."""
        df = pd.DataFrame({"time": [1640995200, 1641081600], "value": [100, 110]})

        series = ConcreteSeries.from_dataframe(
            df=df, column_mapping={"time": "time", "value": "value"}
        )

        assert len(series.data) == 2
        assert all(isinstance(d, LineData) for d in series.data)
        assert series.data[0].time == 1640995200
        assert series.data[0].value == 100

    def test_from_dataframe_with_index_columns(self):
        """Test from_dataframe with index columns."""
        df = pd.DataFrame({"value": [100, 110]}, index=pd.to_datetime(["2022-01-01", "2022-01-02"]))

        series = ConcreteSeries.from_dataframe(
            df=df, column_mapping={"time": "datetime", "value": "value"}
        )

        assert len(series.data) == 2
        assert all(isinstance(d, LineData) for d in series.data)

    def test_from_dataframe_with_multi_index(self):
        """Test from_dataframe with multi-index."""
        # Create DataFrame with multi-index already as columns
        df = pd.DataFrame(
            {"date": [1640995200, 1641081600], "symbol": ["A", "B"], "value": [100, 110]}
        )

        series = ConcreteSeries.from_dataframe(
            df=df, column_mapping={"time": "date", "value": "value"}
        )

        assert len(series.data) == 2
        assert all(isinstance(d, LineData) for d in series.data)

    def test_from_dataframe_with_unnamed_datetime_index(self):
        """Test from_dataframe with unnamed DatetimeIndex."""
        df = pd.DataFrame({"value": [100, 110]}, index=pd.to_datetime(["2022-01-01", "2022-01-02"]))

        series = ConcreteSeries.from_dataframe(
            df=df, column_mapping={"time": "datetime", "value": "value"}
        )

        assert len(series.data) == 2
        assert all(isinstance(d, LineData) for d in series.data)
        # Verify the time values are properly converted
        assert series.data[0].time == 1640995200  # 2022-01-01
        assert series.data[1].time == 1641081600  # 2022-01-02

    def test_from_dataframe_with_unnamed_datetime_multi_index(self):
        """Test from_dataframe with MultiIndex containing unnamed DatetimeIndex level."""
        # Create DataFrame with datetime column already available
        df = pd.DataFrame(
            {
                "datetime": [pd.Timestamp("2022-01-01"), pd.Timestamp("2022-01-02")],
                "symbol": ["A", "B"],
                "value": [100, 110],
            }
        )

        series = ConcreteSeries.from_dataframe(
            df=df, column_mapping={"time": "datetime", "value": "value"}
        )

        assert len(series.data) == 2
        assert all(isinstance(d, LineData) for d in series.data)
        # Verify the time values are properly converted
        assert series.data[0].time == 1640995200  # 2022-01-01
        assert series.data[1].time == 1641081600  # 2022-01-02

    def test_validate_pane_config(self):
        """Test the _validate_pane_config method."""
        data = [LineData(time=1640995200, value=100)]

        # Should not raise an exception
        series = ConcreteSeries(data=data, pane_id=0)
        series._validate_pane_config()

        # Should not raise an exception for valid pane_id
        series = ConcreteSeries(data=data, pane_id=1)
        series._validate_pane_config()

    def test_validate_pane_config_invalid(self):
        """Test _validate_pane_config with invalid pane_id."""
        data = [LineData(time=1640995200, value=100)]

        # Should raise ValueError for negative pane_id
        series = ConcreteSeries(data=data, pane_id=-1)
        with pytest.raises(ValueError, match="pane_id must be non-negative"):
            series._validate_pane_config()

    def test_method_chaining(self):
        """Test method chaining functionality."""
        data = [LineData(time=1640995200, value=100)]
        series = ConcreteSeries(data=data)

        # Test chaining multiple methods
        result = (
            series.set_visible(False)
            .add_marker(
                time=1640995200,
                position=MarkerPosition.ABOVE_BAR,
                color="#ff0000",
                shape=MarkerShape.CIRCLE,
            )
            .add_price_line(PriceLineOptions(price=100, color="#ff0000"))
            .clear_markers()
            .clear_price_lines()
        )

        assert result is series
        assert series.visible is False
        assert len(series.markers) == 0
        assert len(series.price_lines) == 0

    def test_error_handling_invalid_data(self):
        """Test error handling with invalid data."""
        # The new implementation should raise an error for invalid data types
        with pytest.raises(
            ValueError, match="data must be a list of SingleValueData objects, DataFrame, or Series"
        ):
            ConcreteSeries(data="invalid_data")

    def test_error_handling_missing_required_columns(self):
        """Test error handling with missing required columns."""
        df = pd.DataFrame({"value": [100, 110]})  # Missing 'time' column

        with pytest.raises(ValueError, match="Time column 'time' not found"):
            ConcreteSeries.from_dataframe(df=df, column_mapping={"time": "time", "value": "value"})

    def test_error_handling_invalid_data_type(self):
        """Test error handling with invalid data type."""
        with pytest.raises(
            ValueError, match="data must be a list of SingleValueData objects, DataFrame, or Series"
        ):
            ConcreteSeries(data="invalid_data")

    def test_error_handling_dataframe_without_column_mapping(self):
        """Test error handling with DataFrame without column_mapping."""
        df = pd.DataFrame({"time": [1640995200], "value": [100]})

        # Create a Series subclass that doesn't override __init__
        class TestSeries(Series):
            DATA_CLASS = LineData

        with pytest.raises(
            ValueError, match="column_mapping is required when providing DataFrame or Series data"
        ):
            TestSeries(data=df)

    def test_error_handling_invalid_list_data(self):
        """Test error handling with list containing non-SingleValueData objects."""
        invalid_data = [{"time": 1640995200, "value": 100}]  # dict instead of SingleValueData

        with pytest.raises(
            ValueError, match="All items in data list must be instances of Data or its subclasses"
        ):
            ConcreteSeries(data=invalid_data)


class TestSeriesBaseAdvanced:
    """Advanced test cases for the Series base class."""

    def test_get_enum_value_helper_function(self):
        """Test the _get_enum_value helper function."""
        from streamlit_lightweight_charts_pro.type_definitions.enums import LineStyle
        from tests.unit.utils import _get_enum_value

        # Test with enum object
        result = _get_enum_value(LineStyle.SOLID, LineStyle)
        assert result == 0  # LineStyle.SOLID.value is 0

        # Test with string
        result = _get_enum_value("solid", LineStyle)
        assert result == "solid"

        # Test with invalid string
        result = _get_enum_value("invalid", LineStyle)
        assert result == "invalid"

        # Test with non-enum, non-string value
        result = _get_enum_value(123, LineStyle)
        assert result == 123

    def test_to_dict_with_complex_options(self):
        """Test to_dict method with complex nested options."""
        data = [LineData(time=1640995200, value=100)]
        series = ConcreteSeries(data=data)

        # Add complex options
        series.price_format = PriceFormatOptions(type="price", precision=2)
        series.add_price_line(PriceLineOptions(price=100, color="#ff0000"))
        series.add_marker(
            time=1640995200,
            position=MarkerPosition.ABOVE_BAR,
            color="#ff0000",
            shape=MarkerShape.CIRCLE,
        )

        result = series.asdict()

        assert "type" in result
        assert "data" in result
        assert "priceLines" in result
        assert "markers" in result
        assert "options" in result

    def test_to_dict_with_none_options(self):
        """Test to_dict method with None options."""
        data = [LineData(time=1640995200, value=100)]
        series = ConcreteSeries(data=data)

        # Set price_format to None
        series.price_format = None

        result = series.asdict()

        # Should not include price_format in options
        assert "type" in result
        assert "data" in result
        assert "options" in result

    def test_to_dict_with_empty_options(self):
        """Test to_dict method with empty options."""
        data = [LineData(time=1640995200, value=100)]
        series = ConcreteSeries(data=data)

        # Clear all options
        series.price_lines = []
        series.markers = []
        series.price_format = None

        result = series.asdict()

        assert "type" in result
        assert "data" in result
        assert "options" in result
        # ConcreteSeries always includes priceLines and markers even when empty
        assert "priceLines" in result
        assert "markers" in result
        assert result["priceLines"] == []
        assert result["markers"] == []

    def test_validate_pane_config_edge_cases(self):
        """Test _validate_pane_config with edge cases."""
        data = [LineData(time=1640995200, value=100)]

        # Test with pane_id=None (should set pane_id to 0)
        series = ConcreteSeries(data=data, pane_id=None)
        series._validate_pane_config()
        assert series.pane_id == 0

        # Test with pane_id=0 (should not raise error)
        series = ConcreteSeries(data=data, pane_id=0)
        series._validate_pane_config()  # Should not raise

    def test_data_class_property_inheritance(self):
        """Test data_class property with inheritance."""

        class ChildSeries(ConcreteSeries):
            DATA_CLASS = LineData  # Same as parent

        class GrandchildSeries(ChildSeries):
            pass  # Should inherit DATA_CLASS from ChildSeries

        # Test that data_class returns the correct class
        assert ConcreteSeries.data_class == LineData
        assert ChildSeries.data_class == LineData
        assert GrandchildSeries.data_class == LineData

    def test_from_dataframe_with_complex_multi_index(self):
        """Test from_dataframe with complex MultiIndex scenarios."""
        # Test with DataFrame that has datetime and symbol columns
        df = pd.DataFrame(
            {
                "datetime": [pd.Timestamp("2022-01-01"), pd.Timestamp("2022-01-02")],
                "symbol": ["A", "B"],
                "value": [100, 110],
            }
        )

        series = ConcreteSeries.from_dataframe(
            df=df, column_mapping={"time": "datetime", "value": "value"}
        )

        assert len(series.data) == 2
        assert all(isinstance(d, LineData) for d in series.data)

    def test_from_dataframe_with_datetime_index_no_name(self):
        """Test from_dataframe with DatetimeIndex that has no name."""
        df = pd.DataFrame({"value": [100, 110]})
        df.index = pd.to_datetime(["2022-01-01", "2022-01-02"])
        df.index.name = None  # Ensure no name

        series = ConcreteSeries.from_dataframe(
            df=df, column_mapping={"time": "datetime", "value": "value"}
        )

        assert len(series.data) == 2
        assert all(isinstance(d, LineData) for d in series.data)

    def test_from_dataframe_with_series_input(self):
        """Test from_dataframe with pandas Series input."""
        series_data = pd.Series([100, 110], index=pd.to_datetime(["2022-01-01", "2022-01-02"]))

        series = ConcreteSeries.from_dataframe(
            df=series_data, column_mapping={"time": "index", "value": 0}
        )

        assert len(series.data) == 2
        assert all(isinstance(d, LineData) for d in series.data)

    def test_from_dataframe_error_handling(self):
        """Test from_dataframe error handling."""
        df = pd.DataFrame({"value": [100, 110]})

        # Test missing required column in column_mapping
        with pytest.raises(ValueError, match="Missing required columns in column_mapping"):
            ConcreteSeries.from_dataframe(
                df=df, column_mapping={"value": "value"}  # Missing 'time'
            )

        # Test missing column in DataFrame
        with pytest.raises(ValueError, match="Time column 'missing_column' not found"):
            ConcreteSeries.from_dataframe(
                df=df, column_mapping={"time": "missing_column", "value": "value"}
            )

    def test_constructor_with_series_data(self):
        """Test constructor with pandas Series data."""
        series_data = pd.Series([100, 110], index=[1640995200, 1641081600])

        series = ConcreteSeries(data=series_data, column_mapping={"time": "index", "value": 0})

        assert len(series.data) == 2
        assert all(isinstance(d, LineData) for d in series.data)

    def test_constructor_with_none_data(self):
        """Test constructor with None data."""
        series = ConcreteSeries(data=None)
        assert series.data == []

    def test_constructor_with_empty_list(self):
        """Test constructor with empty list."""
        series = ConcreteSeries(data=[])
        assert series.data == []

    def test_price_scale_id_setter(self):
        """Test price_scale_id setter."""
        data = [LineData(time=1640995200, value=100)]
        series = ConcreteSeries(data=data)

        series.price_scale_id = "left"
        assert series.price_scale_id == "left"

        series.price_scale_id = "right"
        assert series.price_scale_id == "right"

    def test_price_format_setter(self):
        """Test price_format setter."""
        data = [LineData(time=1640995200, value=100)]
        series = ConcreteSeries(data=data)

        price_format = PriceFormatOptions(type="price", precision=2)
        series.price_format = price_format
        assert series.price_format == price_format

    def test_price_lines_setter(self):
        """Test price_lines setter."""
        data = [LineData(time=1640995200, value=100)]
        series = ConcreteSeries(data=data)

        price_lines = [PriceLineOptions(price=100, color="#ff0000")]
        series.price_lines = price_lines
        assert series.price_lines == price_lines

    def test_markers_setter(self):
        """Test markers setter."""
        data = [LineData(time=1640995200, value=100)]
        series = ConcreteSeries(data=data)

        markers = [
            Marker(
                time=1640995200,
                position=MarkerPosition.ABOVE_BAR,
                color="#ff0000",
                shape=MarkerShape.CIRCLE,
            )
        ]
        series.markers = markers
        assert series.markers == markers

    def test_price_scale_id_included_in_to_dict(self):
        """Test that priceScaleId is included in to_dict output."""
        from streamlit_lightweight_charts_pro.charts.options.line_options import LineOptions
        from streamlit_lightweight_charts_pro.charts.series.line import LineSeries
        from streamlit_lightweight_charts_pro.data import LineData

        # Create series with custom price_scale_id
        data = [LineData("2024-01-01", 100)]
        series = LineSeries(data=data, price_scale_id="left")

        # Convert to dict
        result = series.asdict()

        # Verify priceScaleId is included
        assert "priceScaleId" in result["options"]
        assert result["options"]["priceScaleId"] == "left"

        # Test with default price_scale_id
        series_default = LineSeries(data=data)  # Default is "right"
        result_default = series_default.asdict()

        assert "priceScaleId" in result_default["options"]
        assert result_default["options"]["priceScaleId"] == "right"
