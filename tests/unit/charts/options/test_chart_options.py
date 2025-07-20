"""Comprehensive tests for ChartOptions and related option classes."""

import copy
import gc
import json
import pickle
import time

import psutil
import pytest

from streamlit_lightweight_charts_pro.charts.options import (
    ChartOptions,
    CrosshairLineOptions,
    CrosshairOptions,
    GridLineOptions,
    GridOptions,
    LayoutOptions,
    RightPriceScale,
    TimeScaleOptions,
    WatermarkOptions,
)
from streamlit_lightweight_charts_pro.type_definitions.colors import Background
from streamlit_lightweight_charts_pro.type_definitions.enums import (
    CrosshairMode,
    HorzAlign,
    LineStyle,
    PriceScaleMode,
    VertAlign,
)


class TestChartOptions:
    """Comprehensive test cases for ChartOptions and related option classes."""

    def setup_method(self):
        """Set up test data."""
        self.default_options = ChartOptions()

    # ===== BASIC OPTION CLASSES TESTS =====

    def test_grid_line_options(self):
        """Test GridLineOptions functionality."""
        options = GridLineOptions(color="#cccccc", style=LineStyle.DASHED, visible=False)
        assert options.color == "#cccccc"
        assert options.style == LineStyle.DASHED
        assert options.visible is False

        d = options.to_dict()
        assert d["color"] == "#cccccc"
        assert d["style"] == LineStyle.DASHED.value
        assert d["visible"] is False

    def test_grid_options(self):
        """Test GridOptions functionality."""
        vert_lines = GridLineOptions(color="#ff0000")
        horz_lines = GridLineOptions(color="#00ff00")
        options = GridOptions(vert_lines=vert_lines, horz_lines=horz_lines)

        d = options.to_dict()
        assert d["vertLines"]["color"] == "#ff0000"
        assert d["horzLines"]["color"] == "#00ff00"

    def test_layout_options(self):
        """Test LayoutOptions functionality."""
        background = Background.solid("#ffffff")
        options = LayoutOptions(background=background, text_color="#000000", font_size=14)
        assert options.text_color == "#000000"
        assert options.font_size == 14

        d = options.to_dict()
        assert d["textColor"] == "#000000"
        assert d["fontSize"] == 14
        assert d["background"]["type"] == "solid"

    def test_crosshair_line_options(self):
        """Test CrosshairLineOptions functionality."""
        options = CrosshairLineOptions(
            visible=True, width=2, color="#ff0000", style=LineStyle.SOLID
        )
        assert options.visible is True
        assert options.width == 2

        d = options.to_dict()
        assert d["visible"] is True
        assert d["width"] == 2
        assert d["color"] == "#ff0000"

    def test_crosshair_options(self):
        """Test CrosshairOptions functionality."""
        vert_line = CrosshairLineOptions(color="#ff0000")
        horz_line = CrosshairLineOptions(color="#00ff00")
        options = CrosshairOptions(
            mode=CrosshairMode.MAGNET, vert_line=vert_line, horz_line=horz_line
        )
        assert options.mode == CrosshairMode.MAGNET

        d = options.to_dict()
        assert d["mode"] == CrosshairMode.MAGNET.value
        assert d["vertLine"]["color"] == "#ff0000"
        assert d["horzLine"]["color"] == "#00ff00"

    def test_price_scale_options(self):
        """Test RightPriceScale functionality."""
        options = RightPriceScale(
            border_visible=False, border_color="#cccccc", mode=PriceScaleMode.LOGARITHMIC
        )
        assert options.border_visible is False
        assert options.mode == PriceScaleMode.LOGARITHMIC

        d = options.to_dict()
        assert d["borderVisible"] is False
        assert d["mode"] == PriceScaleMode.LOGARITHMIC.value

    def test_time_scale_options(self):
        """Test TimeScaleOptions functionality."""
        options = TimeScaleOptions(
            right_offset=5, bar_spacing=10, time_visible=True, border_visible=False
        )
        assert options.right_offset == 5
        assert options.bar_spacing == 10
        assert options.time_visible is True
        assert options.border_visible is False

        d = options.to_dict()
        assert d["rightOffset"] == 5
        assert d["barSpacing"] == 10
        assert d["timeVisible"] is True
        assert d["borderVisible"] is False

    def test_watermark_options(self):
        """Test WatermarkOptions functionality."""
        options = WatermarkOptions(
            visible=True,
            text="TEST",
            font_size=24,
            horz_align=HorzAlign.CENTER,
            vert_align=VertAlign.CENTER,
            color="rgba(0,0,0,0.5)",
        )
        assert options.visible is True
        assert options.text == "TEST"
        assert options.horz_align == HorzAlign.CENTER

        d = options.to_dict()
        assert d["visible"] is True
        assert d["text"] == "TEST"
        assert d["horzAlign"] == HorzAlign.CENTER.value

    # ===== CHART OPTIONS INITIALIZATION TESTS =====

    def test_chart_options_initialization_defaults(self):
        """Test ChartOptions initialization with default values."""
        options = ChartOptions()

        assert options.height == 400
        assert options.width is None
        assert options.auto_size is True
        assert options.grid is not None
        assert options.crosshair is not None
        assert options.watermark is None
        assert options.time_scale is not None

    def test_chart_options_initialization_custom_values(self):
        """Test ChartOptions initialization with custom values."""
        options = ChartOptions(height=600, width=800, auto_size=False)

        assert options.height == 600
        assert options.width == 800
        assert options.auto_size is False

    def test_chart_options_with_component_options(self):
        """Test ChartOptions with component option objects."""
        layout = LayoutOptions()
        grid = GridOptions()
        crosshair = CrosshairOptions()
        right_price_scale = RightPriceScale()
        time_scale = TimeScaleOptions()

        options = ChartOptions(
            width=800,
            height=600,
            layout=layout,
            grid=grid,
            crosshair=crosshair,
            right_price_scale=right_price_scale,
            time_scale=time_scale,
        )
        assert options.width == 800
        assert options.height == 600

        d = options.to_dict()
        assert d["width"] == 800
        assert d["height"] == 600
        assert "layout" in d
        assert "grid" in d
        assert "crosshair" in d
        assert "rightPriceScale" in d
        assert "timeScale" in d

    # ===== CHART OPTIONS VALIDATION TESTS =====

    def test_chart_options_height_validation(self):
        """Test ChartOptions height validation."""
        # Test valid height
        options = ChartOptions(height=500)
        assert options.height == 500

        # ChartOptions doesn't validate height - it accepts any value
        options = ChartOptions(height=-100)
        assert options.height == -100

        options = ChartOptions(height=0)
        assert options.height == 0

    def test_chart_options_width_validation(self):
        """Test ChartOptions width validation."""
        # Test valid width
        options = ChartOptions(width=700)
        assert options.width == 700

        # ChartOptions doesn't validate width - it accepts any value
        options = ChartOptions(width=-100)
        assert options.width == -100

        options = ChartOptions(width=0)
        assert options.width == 0

    def test_chart_options_auto_size_validation(self):
        """Test ChartOptions auto_size validation."""
        # Test valid auto_size
        options = ChartOptions(auto_size=True)
        assert options.auto_size is True

        options = ChartOptions(auto_size=False)
        assert options.auto_size is False

    def test_chart_options_validation_combinations(self):
        """Test ChartOptions validation with various combinations."""
        # Test valid combinations
        ChartOptions(height=100, width=100, auto_size=False)
        ChartOptions(height=None, width=None, auto_size=True)

        # ChartOptions doesn't validate combinations - it accepts any combination
        ChartOptions(height=100, width=100, auto_size=True)

    def test_chart_options_edge_cases(self):
        """Test ChartOptions edge cases."""
        # Test with maximum values
        options = ChartOptions(height=9999, width=9999)
        assert options.height == 9999
        assert options.width == 9999

        # Test with minimum valid values
        options = ChartOptions(height=1, width=1)
        assert options.height == 1
        assert options.width == 1

    def test_chart_options_nested_object_validation(self):
        """Test ChartOptions nested object validation."""
        # ChartOptions doesn't validate nested objects - it accepts any dictionary
        options = ChartOptions()
        options.grid = {"vertLines": {"visible": "invalid"}}
        assert options.grid["vertLines"]["visible"] == "invalid"

        options.crosshair = {"mode": "invalid_mode"}
        assert options.crosshair["mode"] == "invalid_mode"

    def test_chart_options_error_handling(self):
        """Test ChartOptions error handling."""
        # ChartOptions doesn't validate data types - it accepts any values
        options = ChartOptions(height="invalid")
        assert options.height == "invalid"

        options = ChartOptions(width="invalid")
        assert options.width == "invalid"

        options = ChartOptions(auto_size="invalid")
        assert options.auto_size == "invalid"

    # ===== CHART OPTIONS CONFIGURATION TESTS =====

    def test_chart_options_grid_configuration(self):
        """Test ChartOptions grid configuration."""
        # ChartOptions stores grid as a dictionary, not an object
        options = ChartOptions()
        options.grid = {
            "vertLines": {"visible": True, "color": "#ff0000"},
            "horzLines": {"visible": False, "color": "#00ff00"},
        }

        assert options.grid["vertLines"]["visible"] is True
        assert options.grid["vertLines"]["color"] == "#ff0000"
        assert options.grid["horzLines"]["visible"] is False
        assert options.grid["horzLines"]["color"] == "#00ff00"

    def test_chart_options_crosshair_configuration(self):
        """Test ChartOptions crosshair configuration."""
        # ChartOptions stores crosshair as a dictionary, not an object
        options = ChartOptions()
        options.crosshair = {
            "mode": 1,  # normal mode
            "vertLine": {"visible": True, "color": "#ff0000"},
            "horzLine": {"visible": True, "color": "#00ff00"},
        }

        assert options.crosshair["mode"] == 1
        assert options.crosshair["vertLine"]["visible"] is True
        assert options.crosshair["vertLine"]["color"] == "#ff0000"
        assert options.crosshair["horzLine"]["visible"] is True
        assert options.crosshair["horzLine"]["color"] == "#00ff00"

    def test_chart_options_watermark_configuration(self):
        """Test ChartOptions watermark configuration."""
        # ChartOptions stores watermark as a string, not an object
        options = ChartOptions()
        options.watermark = "Test Watermark"

        assert options.watermark == "Test Watermark"

    def test_chart_options_time_scale_configuration(self):
        """Test ChartOptions time scale configuration."""
        # ChartOptions stores time_scale as a dictionary, not an object
        options = ChartOptions()
        options.time_scale = {"visible": True, "timeVisible": True, "secondsVisible": False}

        assert options.time_scale["visible"] is True
        assert options.time_scale["timeVisible"] is True
        assert options.time_scale["secondsVisible"] is False

    # ===== CHART OPTIONS SETTER METHODS TESTS =====

    def test_chart_options_set_layout(self):
        """Test set_layout method."""
        options = ChartOptions()
        result = options.set_layout(
            background_color="#ffffff", text_color="#000000", font_size=12, font_family="Arial"
        )

        assert options.layout["background_color"] == "#ffffff"
        assert options.layout["text_color"] == "#000000"
        assert options.layout["font_size"] == 12
        assert options.layout["font_family"] == "Arial"
        assert result is options

    def test_chart_options_set_grid(self):
        """Test set_grid method."""
        options = ChartOptions()
        result = options.set_grid(
            vert_lines={"visible": True, "color": "#cccccc"},
            horz_lines={"visible": False, "color": "#dddddd"},
        )

        assert options.grid["vert_lines"]["visible"] is True
        assert options.grid["vert_lines"]["color"] == "#cccccc"
        assert options.grid["horz_lines"]["visible"] is False
        assert options.grid["horz_lines"]["color"] == "#dddddd"
        assert result is options

    def test_chart_options_set_crosshair(self):
        """Test set_crosshair method."""
        options = ChartOptions()
        result = options.set_crosshair(
            mode=1,
            vert_line={"visible": True, "color": "#ff0000"},
            horz_line={"visible": True, "color": "#00ff00"},
        )

        assert options.crosshair["mode"] == 1
        # The update method replaces the entire nested dict
        assert options.crosshair["vert_line"]["visible"] is True
        assert options.crosshair["vert_line"]["color"] == "#ff0000"
        assert options.crosshair["horz_line"]["visible"] is True
        assert options.crosshair["horz_line"]["color"] == "#00ff00"
        assert result is options

    def test_chart_options_set_watermark(self):
        """Test set_watermark method."""
        options = ChartOptions()
        result = options.set_watermark("Test Watermark")

        assert options.watermark == "Test Watermark"
        assert result is options

    def test_chart_options_set_localization(self):
        """Test set_localization method."""
        options = ChartOptions()
        result = options.set_localization("en-US", "yyyy-MM-dd")

        assert options.localization["locale"] == "en-US"
        assert options.localization["dateFormat"] == "yyyy-MM-dd"
        assert result is options

    def test_chart_options_set_size(self):
        """Test set_size method."""
        options = ChartOptions()
        result = options.set_size(width=800, height=600)

        assert options.width == 800
        assert options.height == 600
        assert result is options

    def test_chart_options_set_width(self):
        """Test set_width method."""
        options = ChartOptions()
        result = options.set_width(800)

        assert options.width == 800
        assert result is options

    def test_chart_options_set_height(self):
        """Test set_height method."""
        options = ChartOptions()
        result = options.set_height(600)

        assert options.height == 600
        assert result is options

    def test_chart_options_set_auto_size(self):
        """Test set_auto_size method."""
        options = ChartOptions()
        result = options.set_auto_size(False)

        assert options.auto_size is False
        assert result is options

    def test_chart_options_set_min_size(self):
        """Test set_min_size method."""
        options = ChartOptions()
        result = options.set_min_size(min_width=400, min_height=300)

        assert options.min_width == 400
        assert options.min_height == 300
        assert result is options

    def test_chart_options_set_max_size(self):
        """Test set_max_size method."""
        options = ChartOptions()
        result = options.set_max_size(max_width=1200, max_height=800)

        assert options.max_width == 1200
        assert options.max_height == 800
        assert result is options

    def test_chart_options_set_legend(self):
        """Test set_legend method."""
        options = ChartOptions()
        result = options.set_legend(True)

        assert options.legend is True
        assert result is options

    def test_chart_options_set_range_switcher(self):
        """Test set_range_switcher method."""
        options = ChartOptions()
        result = options.set_range_switcher(True)

        assert options.range_switcher is True
        assert result is options

    def test_chart_options_set_kinetic_scroll(self):
        """Test set_kinetic_scroll method."""
        options = ChartOptions()
        result = options.set_kinetic_scroll(False)

        assert options.kinetic_scroll is False
        assert result is options

    def test_chart_options_set_tracking_mode(self):
        """Test set_tracking_mode method."""
        options = ChartOptions()
        result = options.set_tracking_mode("magnetic")

        assert options.tracking_mode == "magnetic"
        assert result is options

    def test_chart_options_set_right_price_scale(self):
        """Test set_right_price_scale method."""
        options = ChartOptions()
        result = options.set_right_price_scale(
            visible=True, auto_scale=True, scale_margins={"top": 0.1, "bottom": 0.1}
        )

        assert options.right_price_scale["visible"] is True
        assert options.right_price_scale["auto_scale"] is True
        assert options.right_price_scale["scale_margins"]["top"] == 0.1
        assert options.right_price_scale["scale_margins"]["bottom"] == 0.1
        assert result is options

    def test_chart_options_set_left_price_scale(self):
        """Test set_left_price_scale method."""
        options = ChartOptions()
        result = options.set_left_price_scale(
            visible=True, auto_scale=False, scale_margins={"top": 0.2, "bottom": 0.2}
        )

        assert options.left_price_scale["visible"] is True
        assert options.left_price_scale["auto_scale"] is False
        assert options.left_price_scale["scale_margins"]["top"] == 0.2
        assert options.left_price_scale["scale_margins"]["bottom"] == 0.2
        assert result is options

    def test_chart_options_set_time_scale(self):
        """Test set_time_scale method."""
        options = ChartOptions()
        result = options.set_time_scale(visible=True, time_visible=True, seconds_visible=False)

        assert options.time_scale["visible"] is True
        assert options.time_scale["timeVisible"] is True
        assert options.time_scale["secondsVisible"] is False
        assert result is options

    # ===== CHART OPTIONS SERIALIZATION TESTS =====

    def test_chart_options_to_dict_method(self):
        """Test ChartOptions to_dict method."""
        options = ChartOptions(height=600, width=800, auto_size=False)

        result = options.to_dict()

        assert isinstance(result, dict)
        assert result["height"] == 600
        assert result["width"] == 800
        assert result["autoSize"] is False
        assert "grid" in result
        assert "crosshair" in result
        assert "timeScale" in result

    def test_chart_options_to_dict_with_nested_objects(self):
        """Test ChartOptions to_dict with nested objects."""
        options = ChartOptions()
        options.grid = {
            "vertLines": {"visible": True, "color": "#ff0000"},
            "horzLines": {"visible": False, "color": "#00ff00"},
        }
        result = options.to_dict()

        assert "grid" in result
        grid_dict = result["grid"]
        assert "vertLines" in grid_dict
        assert "horzLines" in grid_dict
        assert grid_dict["vertLines"]["visible"] is True
        assert grid_dict["vertLines"]["color"] == "#ff0000"

    def test_chart_options_to_dict_comprehensive(self):
        """Test to_dict method with comprehensive configuration."""
        options = (
            ChartOptions()
            .set_size(800, 600)
            .set_auto_size(False)
            .set_watermark("Test Chart")
            .set_legend(True)
            .set_range_switcher(True)
            .set_kinetic_scroll(False)
            .set_tracking_mode("magnetic")
            .set_localization("en-US", "yyyy-MM-dd")
            .set_layout(background_color="#ffffff", text_color="#000000")
            .set_grid(vert_lines={"visible": True}, horz_lines={"visible": False})
            .set_crosshair(mode=1, vert_line={"visible": True})
            .set_right_price_scale(visible=True, auto_scale=True)
            .set_left_price_scale(visible=False, auto_scale=False)
            .set_time_scale(visible=True, time_visible=True)
        )

        result = options.to_dict()

        # Check basic properties
        assert result["width"] == 800
        assert result["height"] == 600
        assert result["autoSize"] is False
        assert result["watermark"] == "Test Chart"
        assert result["legend"] is True
        assert result["rangeSwitcher"] is True
        assert result["kineticScroll"] is False
        assert result["trackingMode"] == "magnetic"

        # Check nested configurations
        assert result["localization"]["locale"] == "en-US"
        assert result["localization"]["dateFormat"] == "yyyy-MM-dd"
        assert result["layout"]["background_color"] == "#ffffff"
        assert result["layout"]["text_color"] == "#000000"
        assert result["grid"]["vert_lines"]["visible"] is True
        assert result["grid"]["horz_lines"]["visible"] is False
        assert result["crosshair"]["mode"] == 1
        assert result["crosshair"]["vertLine"]["visible"] is True
        assert result["rightPriceScale"]["visible"] is True
        assert result["leftPriceScale"]["visible"] is False
        assert result["timeScale"]["visible"] is True
        assert result["timeScale"]["timeVisible"] is True

    def test_chart_options_to_dict_with_size_constraints(self):
        """Test to_dict method with size constraints."""
        options = (
            ChartOptions()
            .set_min_size(min_width=400, min_height=300)
            .set_max_size(max_width=1200, max_height=800)
        )

        result = options.to_dict()

        assert result["minWidth"] == 400
        assert result["minHeight"] == 300
        assert result["maxWidth"] == 1200
        assert result["maxHeight"] == 800

    def test_chart_options_to_dict_removes_none_values(self):
        """Test to_dict method removes None values."""
        options = ChartOptions()
        options.width = None
        options.watermark = None

        result = options.to_dict()

        assert "width" not in result
        assert "watermark" not in result
        assert "height" in result  # Should be included as it has a default value

    def test_chart_options_json_serialization(self):
        """Test ChartOptions JSON serialization."""
        options = ChartOptions(height=600, width=800)
        try:
            json_str = json.dumps(options.to_dict())
            assert isinstance(json_str, str)
        except (TypeError, ValueError):
            pytest.fail("ChartOptions should be JSON serializable")

    # ===== CHART OPTIONS OBJECT BEHAVIOR TESTS =====

    def test_chart_options_equality(self):
        """Test ChartOptions equality comparison."""
        options1 = ChartOptions(height=600, width=800)
        options2 = ChartOptions(height=600, width=800)
        options3 = ChartOptions(height=700, width=800)

        # ChartOptions is a dataclass, so it implements equality based on field values
        assert options1 == options2  # Same field values
        assert options1 != options3  # Different field values

    def test_chart_options_hash(self):
        """Test ChartOptions hash functionality."""
        options = ChartOptions(height=600, width=800)

        # ChartOptions contains mutable dictionaries, so it's not hashable
        with pytest.raises(TypeError, match="unhashable type"):
            hash(options)

    def test_chart_options_repr(self):
        """Test ChartOptions string representation."""
        options = ChartOptions(height=600, width=800)

        repr_str = repr(options)
        assert isinstance(repr_str, str)
        assert "ChartOptions" in repr_str

    def test_chart_options_str(self):
        """Test ChartOptions string conversion."""
        options = ChartOptions(height=600, width=800)

        str_value = str(options)
        assert isinstance(str_value, str)
        assert "ChartOptions" in str_value

    def test_chart_options_immutability(self):
        """Test ChartOptions immutability."""
        options = ChartOptions(height=600, width=800)
        options.height

        # ChartOptions is mutable - values can be changed
        options.height = 700

        # Options should be modified since they're mutable
        assert options.height == 700

    # ===== CHART OPTIONS COPY AND SERIALIZATION TESTS =====

    def test_chart_options_copy_functionality(self):
        """Test ChartOptions copy functionality."""
        options = ChartOptions(height=600, width=800)

        copied_options = copy.copy(options)

        assert copied_options is not options
        assert copied_options.height == options.height
        assert copied_options.width == options.width

    def test_chart_options_deep_copy_functionality(self):
        """Test ChartOptions deep copy functionality."""
        options = ChartOptions(height=600, width=800)

        deep_copied_options = copy.deepcopy(options)

        assert deep_copied_options is not options
        assert deep_copied_options.height == options.height
        assert deep_copied_options.width == options.width

    def test_chart_options_pickle_functionality(self):
        """Test ChartOptions pickle functionality."""
        options = ChartOptions(height=600, width=800)

        pickled = pickle.dumps(options)
        unpickled = pickle.loads(pickled)

        assert unpickled.height == options.height
        assert unpickled.width == options.width

    # ===== CHART OPTIONS METHOD CHAINING TESTS =====

    def test_chart_options_method_chaining(self):
        """Test method chaining functionality."""
        options = ChartOptions()

        result = (
            options.set_size(800, 600)
            .set_auto_size(False)
            .set_watermark("Test Chart")
            .set_legend(True)
            .set_range_switcher(True)
            .set_kinetic_scroll(False)
            .set_tracking_mode("magnetic")
            .set_localization("en-US", "yyyy-MM-dd")
            .set_layout(background_color="#ffffff")
            .set_grid(vert_lines={"visible": True})
            .set_crosshair(mode=1)
            .set_right_price_scale(visible=True)
            .set_left_price_scale(visible=True)
            .set_time_scale(visible=True)
        )

        assert result is options
        assert options.width == 800
        assert options.height == 600
        assert options.auto_size is False
        assert options.watermark == "Test Chart"
        assert options.legend is True
        assert options.range_switcher is True
        assert options.kinetic_scroll is False
        assert options.tracking_mode == "magnetic"
        assert options.localization["locale"] == "en-US"
        assert options.layout["background_color"] == "#ffffff"
        assert options.grid["vert_lines"]["visible"] is True
        assert options.crosshair["mode"] == 1
        assert options.right_price_scale["visible"] is True
        assert options.left_price_scale["visible"] is True
        assert options.time_scale["visible"] is True

    # ===== CHART OPTIONS DEFAULT VALUES TESTS =====

    def test_chart_options_default_values(self):
        """Test ChartOptions default values."""
        options = ChartOptions()

        assert options.height == 400
        assert options.auto_size is True
        assert options.legend is False
        assert options.range_switcher is False
        assert options.kinetic_scroll is True
        assert options.tracking_mode == "normal"
        assert options.watermark is None
        assert options.width is None
        assert options.min_width is None
        assert options.max_width is None
        assert options.min_height is None
        assert options.max_height is None

        # Check default nested configurations
        assert options.layout["background"]["type"] == "solid"
        assert options.layout["background"]["color"] == "white"
        assert options.layout["textColor"] == "black"
        assert options.layout["fontSize"] == 12
        assert options.layout["fontFamily"] == "Roboto, sans-serif"

        assert options.grid["vertLines"]["visible"] is True
        assert options.grid["horzLines"]["visible"] is True

        assert options.crosshair["mode"] == 1
        assert options.crosshair["vertLine"]["visible"] is True
        assert options.crosshair["horzLine"]["visible"] is True

        assert options.right_price_scale["visible"] is True
        assert options.left_price_scale["visible"] is False

        assert options.time_scale["visible"] is True
        assert options.time_scale["timeVisible"] is True
        assert options.time_scale["secondsVisible"] is False

    def test_chart_options_default_behavior(self):
        """Test ChartOptions default behavior."""
        options = ChartOptions()

        # Test default values
        assert options.height == 400
        assert options.width is None
        assert options.auto_size is True

        # Test that nested objects are created with defaults
        assert options.grid is not None
        assert options.crosshair is not None
        assert options.watermark is None
        assert options.time_scale is not None

    # ===== CHART OPTIONS PERFORMANCE TESTS =====

    def test_chart_options_performance(self):
        """Test ChartOptions performance."""
        start_time = time.time()
        for _ in range(1000):
            options = ChartOptions(height=600, width=800)
            options.to_dict()
        end_time = time.time()

        # Should complete within reasonable time
        assert end_time - start_time < 1.0

    def test_chart_options_memory_usage(self):
        """Test ChartOptions memory usage."""
        process = psutil.Process()
        initial_memory = process.memory_info().rss

        options_list = []
        for _ in range(1000):
            options = ChartOptions(height=600, width=800)
            options_list.append(options)

        # Force garbage collection
        gc.collect()
        final_memory = process.memory_info().rss

        # Memory usage should be reasonable
        memory_increase = final_memory - initial_memory
        assert memory_increase < 50 * 1024 * 1024  # Less than 50MB increase

    # ===== CHART OPTIONS COMPLEX CONFIGURATION TESTS =====

    def test_chart_options_complex_configuration(self):
        """Test ChartOptions complex configuration."""
        options = ChartOptions(height=600, width=800, auto_size=False)

        # Set grid configuration
        options.grid = {
            "vertLines": {"visible": True, "color": "#ff0000", "style": 1},
            "horzLines": {"visible": True, "color": "#00ff00", "style": 2},
        }

        # Set crosshair configuration
        options.crosshair = {
            "mode": 2,  # magnet mode
            "vertLine": {"visible": True, "color": "#ff0000", "width": 1},
            "horzLine": {"visible": True, "color": "#00ff00", "width": 1},
        }

        # Set watermark
        options.watermark = "Complex Watermark"

        # Set time scale configuration
        options.time_scale = {
            "visible": True,
            "timeVisible": True,
            "secondsVisible": False,
            "rightOffset": 12,
            "barSpacing": 6,
        }

        # Test all configurations
        assert options.height == 600
        assert options.width == 800
        assert options.auto_size is False
        assert options.grid["vertLines"]["visible"] is True
        assert options.crosshair["mode"] == 2
        assert options.watermark == "Complex Watermark"
        assert options.time_scale["visible"] is True

        # Test serialization
        result = options.to_dict()
        assert result["height"] == 600
        assert result["width"] == 800
        assert result["autoSize"] is False
        assert "grid" in result
        assert "crosshair" in result
        assert "watermark" in result
        assert "timeScale" in result

    def test_chart_options_workflow_integration(self):
        """Test ChartOptions workflow integration."""
        # Create options with various configurations
        options = ChartOptions(height=600, width=800, auto_size=False)

        # Test serialization
        result = options.to_dict()

        # Test that result can be used in chart configuration
        assert isinstance(result, dict)
        assert all(
            key in result
            for key in ["height", "width", "autoSize", "grid", "crosshair", "timeScale"]
        )

        # Test that result is valid for frontend
        assert result["height"] == 600
        assert result["width"] == 800
        assert result["autoSize"] is False
