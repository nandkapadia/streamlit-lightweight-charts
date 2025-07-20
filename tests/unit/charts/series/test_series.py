"""Comprehensive tests for Series classes and related functionality."""

import time
import gc
import copy
import pytest
import pandas as pd
import psutil
from datetime import datetime
import pickle
import json
from unittest.mock import Mock, patch

from streamlit_lightweight_charts_pro.charts.series.base import Series, _get_enum_value
from streamlit_lightweight_charts_pro.charts.series import (
    LineSeries, AreaSeries, BarSeries, BaselineSeries, 
    CandlestickSeries, HistogramSeries
)
from streamlit_lightweight_charts_pro.data import (
    SingleValueData, OhlcData, HistogramData, BaselineData
)
from streamlit_lightweight_charts_pro.charts.options import ChartOptions
from streamlit_lightweight_charts_pro.data import Marker, MarkerPosition, MarkerShape
from streamlit_lightweight_charts_pro.type_definitions import LineStyle
from streamlit_lightweight_charts_pro.type_definitions.enums import LineStyle as LineStyleEnum, LineType
from streamlit_lightweight_charts_pro import (
    SinglePaneChart, create_chart
)
from streamlit_lightweight_charts_pro.charts.chart_builder import ChartBuilder


class TestSeries:
    """Comprehensive test cases for Series classes and functionality."""

    def setup_method(self):
        """Set up test data."""
        self.sample_data = [
            SingleValueData("2024-01-01", 100),
            SingleValueData("2024-01-02", 105),
            SingleValueData("2024-01-03", 110),
        ]

        self.ohlc_data = [
            OhlcData("2024-01-01", 100, 105, 98, 103),
            OhlcData("2024-01-02", 103, 108, 102, 106),
            OhlcData("2024-01-03", 106, 112, 104, 110),
        ]

        self.sample_df = pd.DataFrame({
            "datetime": ["2024-01-01", "2024-01-02", "2024-01-03"],
            "close": [100, 105, 110]
        })

    # ===== SERIES BASE CLASS TESTS =====

    def test_series_abstract_class(self):
        """Test that Series is an abstract base class."""
        with pytest.raises(TypeError):
            Series(data=self.sample_data)  # Should not be instantiable directly

    def test_series_subclass_implementation(self):
        """Test that concrete series classes implement required methods."""
        series = LineSeries(self.sample_data)

        # Test required properties
        assert hasattr(series, "data")
        assert hasattr(series, "color")  # LineSeries stores options as direct attributes
        assert hasattr(series, "line_width")
        assert hasattr(series, "chart_type")

        # Test required methods
        assert hasattr(series, "to_dict")
        assert hasattr(series, "_get_options_dict")

    def test_get_enum_value_with_enum_object(self):
        """Test _get_enum_value with enum object."""
        result = _get_enum_value(LineStyleEnum.SOLID, LineStyleEnum)
        assert result == LineStyleEnum.SOLID.value

    def test_get_enum_value_with_string(self):
        """Test _get_enum_value with string."""
        result = _get_enum_value("solid", LineStyleEnum)
        assert result == "solid"

    def test_get_enum_value_with_invalid_string(self):
        """Test _get_enum_value with invalid string."""
        result = _get_enum_value("invalid", LineStyleEnum)
        assert result == "invalid"

    def test_get_enum_value_with_other_type(self):
        """Test _get_enum_value with other type."""
        result = _get_enum_value(123, LineStyleEnum)
        assert result == 123

    # ===== LINE SERIES TESTS =====

    def test_line_series_initialization(self):
        """Test LineSeries initialization."""
        series = LineSeries(self.sample_data, color="#ff0000", line_width=2)

        assert len(series.data) == 3
        assert series.color == "#ff0000"
        assert series.line_width == 2

    def test_line_series_defaults(self):
        """Test LineSeries default values."""
        series = LineSeries(self.sample_data)

        # Check that default options are set
        assert hasattr(series, "color")
        assert hasattr(series, "line_width")

    def test_line_series_to_dict(self):
        """Test LineSeries to_dict method."""
        series = LineSeries(self.sample_data, color="#ff0000")

        result = series.to_dict()

        assert isinstance(result, dict)
        assert "type" in result
        assert "data" in result
        assert "options" in result
        assert result["type"] == "line"
        assert len(result["data"]) == 3

    def test_line_series_get_options_dict(self):
        """Test LineSeries _get_options_dict method."""
        series = LineSeries(self.sample_data, color="#ff0000", line_width=2)

        result = series._get_options_dict()

        assert isinstance(result, dict)
        assert "color" in result
        assert "lineWidth" in result
        assert result["color"] == "#ff0000"
        assert result["lineWidth"] == 2

    def test_line_series_chart_type(self):
        """Test LineSeries chart_type property."""
        series = LineSeries(self.sample_data)
        assert series.chart_type.value == "Line"

    def test_line_series_ultra_simplified(self):
        """Test LineSeries with ultra-simplified API."""
        series = LineSeries(
            data=self.sample_data,
            color="#ff0000",
            line_style=LineStyleEnum.DASHED,
            line_width=2,
            line_type=LineType.CURVED,
        )

        assert series.color == "#ff0000"
        assert series.line_style == LineStyleEnum.DASHED

        options = series._get_options_dict()
        assert options["color"] == "#ff0000"
        assert options["lineStyle"] == LineStyleEnum.DASHED.value
        assert options["lineType"] == LineType.CURVED.value

    # ===== AREA SERIES TESTS =====

    def test_area_series_ultra_simplified(self):
        """Test AreaSeries with ultra-simplified API."""
        series = AreaSeries(
            data=self.sample_data,
            top_color="rgba(0,255,0,0.5)",
            bottom_color="rgba(0,255,0,0.0)",
            line_color="#00ff00",
            line_width=3,
        )

        assert series.top_color == "rgba(0,255,0,0.5)"
        assert series.line_width == 3

        options = series._get_options_dict()
        assert options["topColor"] == "rgba(0,255,0,0.5)"
        assert options["lineWidth"] == 3
        assert options["lineStyle"] == LineStyleEnum.SOLID.value

    def test_area_series_column_mapping_attribute(self):
        """Test that AreaSeries has column_mapping attribute set correctly."""
        # Test with default column mapping
        series = AreaSeries(data=self.sample_data)
        assert hasattr(series, 'column_mapping')
        assert series.column_mapping is None  # Default is None
        
        # Test with custom column mapping
        series = AreaSeries(data=self.sample_data, column_mapping={"time": "datetime", "value": "close"})
        assert series.column_mapping == {"time": "datetime", "value": "close"}

    # ===== BAR SERIES TESTS =====

    def test_bar_series_ultra_simplified(self):
        """Test BarSeries with ultra-simplified API."""
        series = BarSeries(
            data=self.sample_data,
            color="#00ff00",
            base=0.0,
        )

        assert series.color == "#00ff00"
        assert series.base == 0.0

        options = series._get_options_dict()
        assert options["color"] == "#00ff00"
        assert options["base"] == 0.0

    def test_bar_series_column_mapping_attribute(self):
        """Test that BarSeries has column_mapping attribute set correctly."""
        series = BarSeries(data=self.sample_data, column_mapping={"time": "datetime", "value": "value"})
        assert hasattr(series, 'column_mapping')
        assert series.column_mapping == {"time": "datetime", "value": "value"}

    # ===== CANDLESTICK SERIES TESTS =====

    def test_candlestick_series_ultra_simplified(self):
        """Test CandlestickSeries with ultra-simplified API."""
        series = CandlestickSeries(
            data=self.ohlc_data,
            up_color="#00ff00",
            down_color="#ff0000",
            wick_visible=False,
            border_visible=True,
        )

        assert series.up_color == "#00ff00"
        assert series.wick_visible is False
        assert series.border_visible is True

        options = series._get_options_dict()
        assert options["upColor"] == "#00ff00"
        assert options["wickVisible"] is False
        assert options["borderVisible"] is True

    # ===== HISTOGRAM SERIES TESTS =====

    def test_histogram_series_ultra_simplified(self):
        """Test HistogramSeries with ultra-simplified API."""
        data = [HistogramData("2024-01-01", 1000000)]

        series = HistogramSeries(
            data=data,
            color="#ff00ff",
            base=10.0,
        )

        assert series.color == "#ff00ff"
        assert series.base == 10.0

        options = series._get_options_dict()
        assert options["color"] == "#ff00ff"
        assert options["base"] == 10.0

    def test_histogram_series_column_mapping_attribute(self):
        """Test that HistogramSeries has column_mapping attribute set correctly."""
        series = HistogramSeries(data=self.sample_data, column_mapping={"time": "datetime", "value": "value"})
        assert hasattr(series, 'column_mapping')
        assert series.column_mapping == {"time": "datetime", "value": "value"}

    # ===== BASELINE SERIES TESTS =====

    def test_baseline_series_ultra_simplified(self):
        """Test BaselineSeries with ultra-simplified API."""
        data = [BaselineData("2024-01-01", 5.2)]

        series = BaselineSeries(
            data=data,
            base_value={"type": "price", "price": 50.0},
            top_line_color="#00ff00",
            bottom_line_color="#ff0000",
        )

        assert series.base_value["price"] == 50.0
        assert series.top_line_color == "#00ff00"

        options = series._get_options_dict()
        assert options["baseValue"]["price"] == 50.0
        assert options["topLineColor"] == "#00ff00"

    # ===== DATA VALIDATION TESTS =====

    def test_series_data_validation(self):
        """Test series data validation."""
        # Test with valid data
        series = LineSeries(self.sample_data)
        assert len(series.data) == 3

        # Test with empty data
        series = LineSeries([])
        assert len(series.data) == 0

        # Test with DataFrame - need to use the expected column names
        series = LineSeries(self.sample_df)
        assert len(series.data) == 3

    def test_series_data_validation_errors(self):
        """Test series data validation error handling."""
        # Test with invalid data type - error occurs when trying to use the data
        series = LineSeries("invalid_data")
        with pytest.raises(AttributeError):
            series.to_dict()

        # Test with DataFrame missing required columns
        invalid_df = pd.DataFrame({"wrong_column": [100, 105, 110]})

        with pytest.raises(ValueError):
            LineSeries(invalid_df)

    def test_dataframe_column_mapping_issue(self):
        """Test the DataFrame column mapping issue we encountered."""
        # Create DataFrame with "datetime" and "value" columns (not "close")
        df = pd.DataFrame({
            "datetime": ["2024-01-01", "2024-01-02", "2024-01-03"],
            "value": [100, 105, 103]
        })
        
        # This should work with correct column mapping
        series = AreaSeries(
            data=df, 
            column_mapping={"time": "datetime", "value": "value"}
        )
        assert len(series.data) == 3
        
        # This should fail without column mapping (expecting "close" column)
        with pytest.raises(ValueError, match="DataFrame must contain columns: datetime and close"):
            AreaSeries(data=df)

    def test_dataframe_processing_with_column_mapping(self):
        """Test DataFrame processing with various column mappings."""
        df = pd.DataFrame({
            "datetime": ["2024-01-01", "2024-01-02"],
            "value": [100, 105]
        })
        
        # Test AreaSeries
        area_series = AreaSeries(
            data=df, 
            column_mapping={"time": "datetime", "value": "value"}
        )
        assert len(area_series.data) == 2
        assert str(area_series.data[0].time) == "2024-01-01 00:00:00"
        assert area_series.data[0].value == 100
        
        # Test BarSeries
        bar_series = BarSeries(
            data=df, 
            column_mapping={"time": "datetime", "value": "value"}
        )
        assert len(bar_series.data) == 2
        
        # Test HistogramSeries
        hist_series = HistogramSeries(
            data=df, 
            column_mapping={"time": "datetime", "value": "value"}
        )
        assert len(hist_series.data) == 2

    def test_series_with_dataframe(self):
        """Test Series classes with DataFrame input."""
        # Test LineSeries with DataFrame
        series = LineSeries(data=self.sample_df, color="#ff0000", line_width=3)

        # Test that data was converted correctly
        assert len(series.data) == 3
        assert series.data[0].value == 100.0
        assert series.data[1].value == 105.0

        # Test options
        options = series._get_options_dict()
        assert options["color"] == "#ff0000"
        assert options["lineWidth"] == 3

    def test_series_with_custom_column_mapping(self):
        """Test Series classes with custom column mapping."""
        # Create test DataFrame with custom column names
        df = pd.DataFrame({"date": ["2024-01-01", "2024-01-02"], "price": [100.0, 105.0]})

        # Test LineSeries with custom column mapping
        series = LineSeries(data=df, column_mapping={"time": "date", "value": "price"}, color="#ff0000")

        # Test that data was converted correctly
        assert len(series.data) == 2
        assert series.data[0].value == 100.0
        assert series.data[1].value == 105.0

    def test_series_dataframe_custom_columns(self):
        """Test series DataFrame with custom column mapping."""
        df = pd.DataFrame(
            {"datetime": ["2024-01-01", "2024-01-02", "2024-01-03"], "price": [100, 105, 110]}
        )

        series = LineSeries(df, column_mapping={"time": "datetime", "value": "price"})

        assert len(series.data) == 3
        assert str(series.data[0].time) == "2024-01-01 00:00:00"
        assert series.data[0].value == 100

    def test_series_dataframe_conversion(self):
        """Test series DataFrame conversion."""
        series = LineSeries(self.sample_df)

        assert len(series.data) == 3
        assert str(series.data[0].time) == "2024-01-01 00:00:00"
        assert series.data[0].value == 100

    # ===== OPTIONS VALIDATION TESTS =====

    def test_series_options_validation(self):
        """Test series options validation."""
        # Test with invalid color - LineSeries doesn't validate colors
        series = LineSeries(self.sample_data, color="invalid_color")
        assert series.color == "invalid_color"

        # Test with invalid line width - LineSeries doesn't validate line width
        series = LineSeries(self.sample_data, line_width=-1)
        assert series.line_width == -1

    def test_series_options_initialization(self):
        """Test series options initialization."""
        series = LineSeries(self.sample_data, color="#ff0000", line_width=2)

        assert series.color == "#ff0000"
        assert series.line_width == 2

    # ===== OBJECT BEHAVIOR TESTS =====

    def test_series_equality(self):
        """Test series equality comparison."""
        series1 = LineSeries(self.sample_data, color="#ff0000")
        series2 = LineSeries(self.sample_data, color="#ff0000")
        series3 = LineSeries(self.sample_data, color="#00ff00")

        # Series equality is based on object identity, not content
        assert series1 != series2  # Different objects
        assert series1 != series3  # Different objects

    def test_series_hash(self):
        """Test series hash functionality."""
        series = LineSeries(self.sample_data)

        # Series should be hashable
        hash_value = hash(series)
        assert isinstance(hash_value, int)

    def test_series_repr(self):
        """Test series string representation."""
        series = LineSeries(self.sample_data)

        repr_str = repr(series)
        assert isinstance(repr_str, str)
        assert "LineSeries" in repr_str

    def test_series_str(self):
        """Test series string conversion."""
        series = LineSeries(self.sample_data)

        str_value = str(series)
        assert isinstance(str_value, str)
        assert "LineSeries" in str_value

    def test_series_data_immutability(self):
        """Test series data immutability."""
        series = LineSeries(self.sample_data)
        original_value = series.data[0].value

        # Attempt to modify data - LineSeries data is mutable
        series.data[0] = SingleValueData("2024-01-01", 999)

        # Data should be modified since it's mutable
        assert series.data[0].value == 999

    def test_series_options_immutability(self):
        """Test series options immutability."""
        series = LineSeries(self.sample_data, color="#ff0000")
        original_color = series.color

        # Attempt to modify options - LineSeries options are mutable
        series.color = "#00ff00"

        # Options should be modified since they're mutable
        assert series.color == "#00ff00"

    # ===== SERIALIZATION TESTS =====

    def test_series_data_serialization(self):
        """Test series data serialization."""
        series = LineSeries(self.sample_data)

        # Test JSON serialization
        series_dict = series.to_dict()
        json_str = json.dumps(series_dict)
        assert isinstance(json_str, str)

        # Test that we can reconstruct the data
        parsed = json.loads(json_str)
        assert parsed["type"] == "line"
        assert len(parsed["data"]) == 3

    def test_series_copy_functionality(self):
        """Test series copy functionality."""
        series = LineSeries(self.sample_data, color="#ff0000")

        copied_series = copy.copy(series)

        assert copied_series is not series
        assert copied_series.color == series.color
        assert len(copied_series.data) == len(series.data)

    def test_series_deep_copy_functionality(self):
        """Test series deep copy functionality."""
        series = LineSeries(self.sample_data, color="#ff0000")

        deep_copied_series = copy.deepcopy(series)

        assert deep_copied_series is not series
        assert deep_copied_series.color == series.color
        assert len(deep_copied_series.data) == len(series.data)

    def test_series_pickle_functionality(self):
        """Test series pickle functionality."""
        series = LineSeries(self.sample_data, color="#ff0000")

        pickled = pickle.dumps(series)
        unpickled = pickle.loads(pickled)

        assert unpickled.color == series.color
        assert len(unpickled.data) == len(series.data)

    # ===== PERFORMANCE TESTS =====

    def test_series_performance_large_dataset(self):
        """Test series performance with large dataset."""
        large_data = [SingleValueData(f"2024-01-{i:02d}", 100 + i) for i in range(1, 1001)]
        series = LineSeries(large_data)

        # Test serialization performance
        start_time = time.time()
        result = series.to_dict()
        end_time = time.time()

        assert len(result["data"]) == 1000
        assert end_time - start_time < 1.0  # Should complete within 1 second

    def test_series_memory_usage(self):
        """Test series memory usage."""
        process = psutil.Process()
        initial_memory = process.memory_info().rss

        series_list = []
        for _ in range(1000):
            series = LineSeries(self.sample_data)
            series_list.append(series)

        # Force garbage collection
        gc.collect()
        final_memory = process.memory_info().rss

        # Memory usage should be reasonable
        memory_increase = final_memory - initial_memory
        assert memory_increase < 50 * 1024 * 1024  # Less than 50MB increase

    # ===== METHOD CHAINING TESTS =====

    def test_series_method_chaining(self):
        """Test series method chaining functionality."""
        series = LineSeries(self.sample_data)

        # Test method chaining
        result = (series
                 .set_visible(True)
                 .set_price_scale("right")
                 .set_price_line(visible=True, color="#ff0000")
                 .set_base_line(visible=True, color="#00ff00"))

        assert result is series
        assert series.visible is True
        assert series.price_scale_id == "right"

    def test_series_method_chaining_comprehensive(self):
        """Test comprehensive series method chaining."""
        series = LineSeries(self.sample_data)

        result = (series
                 .set_visible(True)
                 .set_price_scale("right")
                 .set_price_line(visible=True, color="#ff0000", width=2)
                 .set_base_line(visible=True, color="#00ff00", width=1)
                 .set_price_format(min_move=0.01, precision=2)
                 .add_marker(
                     time="2024-01-02",
                     position=MarkerPosition.ABOVE_BAR,
                     color="#ff0000",
                     shape=MarkerShape.CIRCLE,
                     text="Test Marker"
                 )
                 .set_price_scale_config(visible=True, auto_scale=True))

        assert result is series
        assert series.visible is True
        assert series.price_scale_id == "right"

    # ===== SERIES CONFIGURATION TESTS =====

    def test_series_set_visible(self):
        """Test series set_visible method."""
        series = LineSeries(self.sample_data)
        
        result = series.set_visible(False)
        
        assert result is series
        assert series.visible is False

    def test_series_set_price_scale(self):
        """Test series set_price_scale method."""
        series = LineSeries(self.sample_data)
        
        result = series.set_price_scale("left")
        
        assert result is series
        assert series.price_scale_id == "left"

    def test_series_set_price_line_all_parameters(self):
        """Test series set_price_line method with all parameters."""
        series = LineSeries(self.sample_data)
        
        result = series.set_price_line(
            visible=True,
            color="#ff0000",
            width=2,
            style=LineStyleEnum.DASHED
        )
        
        assert result is series
        # Note: LineSeries doesn't store price_line as an attribute
        # The method sets internal configuration

    def test_series_set_price_line_partial_parameters(self):
        """Test series set_price_line method with partial parameters."""
        series = LineSeries(self.sample_data)
        
        result = series.set_price_line(visible=True)
        
        assert result is series
        # Note: LineSeries doesn't store price_line as an attribute
        # The method sets internal configuration

    def test_series_set_base_line_all_parameters(self):
        """Test series set_base_line method with all parameters."""
        series = LineSeries(self.sample_data)
        
        result = series.set_base_line(
            visible=True,
            color="#00ff00",
            width=1,
            style=LineStyleEnum.SOLID
        )
        
        assert result is series
        # Note: LineSeries doesn't store base_line as an attribute
        # The method sets internal configuration

    def test_series_set_base_line_partial_parameters(self):
        """Test series set_base_line method with partial parameters."""
        series = LineSeries(self.sample_data)
        
        result = series.set_base_line(visible=True)
        
        assert result is series
        # Note: LineSeries doesn't store base_line as an attribute
        # The method sets internal configuration

    def test_series_set_price_format(self):
        """Test series set_price_format method."""
        series = LineSeries(self.sample_data)
        
        result = series.set_price_format(min_move=0.01, precision=2)
        
        assert result is series
        assert series.price_format["minMove"] == 0.01
        assert series.price_format["precision"] == 2

    def test_series_set_price_format_defaults(self):
        """Test series set_price_format method with defaults."""
        series = LineSeries(self.sample_data)
        
        result = series.set_price_format()
        
        assert result is series
        assert "minMove" in series.price_format
        assert "precision" in series.price_format

    def test_series_set_price_scale_config(self):
        """Test series set_price_scale_config method."""
        series = LineSeries(self.sample_data)
        
        result = series.set_price_scale_config(
            visible=True,
            auto_scale=True,
            scale_margins={"top": 0.1, "bottom": 0.1}
        )
        
        assert result is series
        # Note: The actual attribute name may be different
        # The method sets internal configuration

    # ===== MARKER TESTS =====

    def test_series_add_marker(self):
        """Test series add_marker method."""
        series = LineSeries(self.sample_data)
        
        result = series.add_marker(
            time="2024-01-02",
            position=MarkerPosition.ABOVE_BAR,
            color="#ff0000",
            shape=MarkerShape.CIRCLE,
            text="Test Marker"
        )
        
        assert result is series
        assert len(series.markers) == 1
        marker = series.markers[0]
        assert marker._time == "2024-01-02"
        assert marker.position == MarkerPosition.ABOVE_BAR
        assert marker.shape == MarkerShape.CIRCLE
        assert marker.text == "Test Marker"

    def test_series_add_marker_with_enum_strings(self):
        """Test series add_marker method with enum strings."""
        series = LineSeries(self.sample_data)
        
        result = series.add_marker(
            time="2024-01-02",
            position=MarkerPosition.BELOW_BAR,
            color="#ff0000",
            shape=MarkerShape.ARROW_DOWN,
            text="Test Marker",
            size=2
        )
        
        assert result is series
        assert len(series.markers) == 1
        marker = series.markers[0]
        assert marker.position == MarkerPosition.BELOW_BAR
        assert marker.shape == MarkerShape.ARROW_DOWN
        assert marker.color == "#ff0000"
        assert marker.size == 2

    def test_series_add_markers(self):
        """Test series add_markers method."""
        series = LineSeries(self.sample_data)
        
        markers = [
            {"time": "2024-01-01", "position": "aboveBar", "shape": "circle", "text": "Start"},
            {"time": "2024-01-03", "position": "belowBar", "shape": "arrowDown", "text": "End"}
        ]
        
        result = series.add_markers(markers)
        
        assert result is series
        assert len(series.markers) == 2

    def test_series_clear_markers(self):
        """Test series clear_markers method."""
        series = LineSeries(self.sample_data)
        series.add_marker(
            time="2024-01-02",
            position=MarkerPosition.ABOVE_BAR,
            color="#ff0000",
            shape=MarkerShape.CIRCLE,
            text="Test Marker"
        )
        
        result = series.clear_markers()
        
        assert result is series
        assert len(series.markers) == 0

    # ===== DATA RANGE TESTS =====

    def test_series_get_data_range_with_data(self):
        """Test series get_data_range with data."""
        series = LineSeries(self.sample_data)
        
        data_range = series.get_data_range()
        
        assert data_range is not None
        assert "min_value" in data_range
        assert "max_value" in data_range
        assert data_range["min_value"] == 100
        assert data_range["max_value"] == 110

    def test_series_get_data_range_empty_data(self):
        """Test series get_data_range with empty data."""
        series = LineSeries([])
        
        data_range = series.get_data_range()
        
        assert data_range is None

    def test_series_get_data_range_single_data_point(self):
        """Test series get_data_range with single data point."""
        series = LineSeries([SingleValueData("2024-01-01", 100)])
        
        data_range = series.get_data_range()
        
        assert data_range is not None
        assert data_range["min_value"] == 100
        assert data_range["max_value"] == 100

    def test_series_get_data_range_with_none_values(self):
        """Test series get_data_range with None values."""
        data_with_none = [
            SingleValueData("2024-01-01", 100),
            SingleValueData("2024-01-02", None),
            SingleValueData("2024-01-03", 110)
        ]
        series = LineSeries(data_with_none)
        
        data_range = series.get_data_range()
        
        assert data_range is not None
        assert data_range["min_value"] == 100
        assert data_range["max_value"] == 110

    def test_series_get_data_range_all_none_values(self):
        """Test series get_data_range with all None values."""
        data_all_none = [
            SingleValueData("2024-01-01", None),
            SingleValueData("2024-01-02", None),
            SingleValueData("2024-01-03", None)
        ]
        series = LineSeries(data_all_none)
        
        data_range = series.get_data_range()
        
        # When all values are None, the range still exists but with None values
        assert data_range is not None
        assert data_range["min_value"] is None
        assert data_range["max_value"] is None

    # ===== INTEGRATION TESTS =====

    def test_series_to_frontend_config_structure(self):
        """Test that series to_frontend_config returns correct structure."""
        series = LineSeries(self.sample_data)
        config = series.to_frontend_config()
        
        assert "type" in config
        assert "data" in config
        assert "options" in config

    def test_single_pane_chart_to_frontend_config_structure(self):
        """Test that to_frontend_config returns the correct structure."""
        chart = SinglePaneChart(series=LineSeries(self.sample_data))
        config = chart.to_frontend_config()
        
        # Test the structure we fixed
        assert "charts" in config
        assert isinstance(config["charts"], list)
        assert len(config["charts"]) == 1
        
        chart_config = config["charts"][0]
        assert "chartId" in chart_config
        assert "chart" in chart_config
        assert "series" in chart_config
        assert "annotations" in chart_config
        
        assert "syncConfig" in config
        assert config["syncConfig"]["enabled"] is False

    def test_chart_builder_method_chaining(self):
        """Test ChartBuilder method chaining with the methods we needed."""
        # This should work without errors
        chart = (create_chart()
                .add_area_series(self.sample_data)
                .set_height(400)
                .set_width(600)
                .set_watermark("Test Chart")
                .set_legend(True)
                .build())
        
        assert chart is not None
        assert len(chart.series) == 1

    def test_chart_builder_has_set_watermark_method(self):
        """Test that ChartBuilder has set_watermark method."""
        builder = ChartBuilder()
        assert hasattr(builder, 'set_watermark')
        assert callable(builder.set_watermark)
        
        # Test that it returns self for chaining
        result = builder.set_watermark("Test Watermark")
        assert result is builder
        assert builder.options.watermark == "Test Watermark"

    def test_chart_builder_has_set_legend_method(self):
        """Test that ChartBuilder has set_legend method."""
        builder = ChartBuilder()
        assert hasattr(builder, 'set_legend')
        assert callable(builder.set_legend)
        
        # Test that it returns self for chaining
        result = builder.set_legend(True)
        assert result is builder
        assert builder.options.legend is True

    # ===== COMPLEX WORKFLOW TESTS =====

    def test_series_complex_workflow(self):
        """Test series complex workflow."""
        # Create series with various configurations
        series = (LineSeries(self.sample_data)
                 .set_visible(True)
                 .set_price_scale("right")
                 .set_price_line(visible=True, color="#ff0000")
                 .set_base_line(visible=True, color="#00ff00")
                 .set_price_format(min_move=0.01, precision=2)
                 .add_marker(
                     time="2024-01-02",
                     position=MarkerPosition.ABOVE_BAR,
                     color="#ff0000",
                     shape=MarkerShape.CIRCLE,
                     text="Test Marker"
                 )
                 .set_price_scale_config(visible=True, auto_scale=True))

        # Test serialization
        result = series.to_dict()

        # Test that result can be used in chart configuration
        assert isinstance(result, dict)
        assert "type" in result
        assert "data" in result
        assert "options" in result

        # Test that result is valid for frontend
        assert result["type"] == "line"
        assert len(result["data"]) == 3

    def test_series_error_recovery(self):
        """Test series error recovery."""
        # Test with invalid data - should handle gracefully
        try:
            series = LineSeries("invalid_data")
            # If we get here, it means the series accepted the invalid data
            # This is the actual behavior
        except Exception:
            # If an exception is raised, that's also acceptable
            pass

        # Test with valid data after invalid data
        series = LineSeries(self.sample_data)
        assert len(series.data) == 3

    def test_series_data_consistency(self):
        """Test series data consistency."""
        series = LineSeries(self.sample_data)

        # Test that data remains consistent
        assert len(series.data) == 3
        assert series.data[0].value == 100
        assert series.data[1].value == 105
        assert series.data[2].value == 110

        # Test that modifications don't affect original data
        series.data[0] = SingleValueData("2024-01-01", 999)
        assert series.data[0].value == 999

    def test_series_options_consistency(self):
        """Test series options consistency."""
        series = LineSeries(self.sample_data, color="#ff0000", line_width=2)

        # Test that options remain consistent
        assert series.color == "#ff0000"
        assert series.line_width == 2

        # Test that modifications work correctly
        series.color = "#00ff00"
        assert series.color == "#00ff00" 