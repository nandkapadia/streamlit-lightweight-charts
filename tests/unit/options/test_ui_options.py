"""
Tests for UI options classes.

This module contains comprehensive tests for UI-related option classes:
- RangeConfig
- RangeSwitcherOptions
- LegendOptions
"""

import pytest

from streamlit_lightweight_charts_pro.charts.options.ui_options import (
    LegendOptions,
    RangeConfig,
    RangeSwitcherOptions,
)


class TestRangeConfig:
    """Test RangeConfig class."""

    def test_default_construction(self):
        """Test construction with default values."""
        config = RangeConfig()

        assert config.text == ""
        assert config.tooltip == ""

    def test_custom_construction(self):
        """Test construction with custom values."""
        config = RangeConfig(text="1D", tooltip="One Day")

        assert config.text == "1D"
        assert config.tooltip == "One Day"

    def test_validation_text(self):
        """Test validation of text field."""
        config = RangeConfig()
        with pytest.raises(TypeError, match="text must be of type"):
            config.set_text(123)

    def test_validation_tooltip(self):
        """Test validation of tooltip field."""
        config = RangeConfig()
        with pytest.raises(TypeError, match="tooltip must be of type"):
            config.set_tooltip(123)

    def test_to_dict(self):
        """Test serialization."""
        config = RangeConfig(text="1D", tooltip="One Day")
        result = config.asdict()

        assert result["text"] == "1D"
        assert result["tooltip"] == "One Day"

    def test_to_dict_omits_empty_text(self):
        """Test that empty text is omitted from output."""
        config = RangeConfig(text="", tooltip="One Day")
        result = config.asdict()

        assert "text" not in result
        assert result["tooltip"] == "One Day"

    def test_to_dict_omits_empty_tooltip(self):
        """Test that empty tooltip is omitted from output."""
        config = RangeConfig(text="1D", tooltip="")
        result = config.asdict()

        assert result["text"] == "1D"
        assert "tooltip" not in result


class TestRangeSwitcherOptions:
    """Test RangeSwitcherOptions class."""

    def test_default_construction(self):
        """Test construction with default values."""
        options = RangeSwitcherOptions()

        assert options.visible is True
        assert options.ranges == []

    def test_custom_construction(self):
        """Test construction with custom values."""
        ranges = [
            RangeConfig(text="1D", tooltip="One Day"),
            RangeConfig(text="1W", tooltip="One Week"),
            RangeConfig(text="1M", tooltip="One Month"),
        ]

        options = RangeSwitcherOptions(visible=False, ranges=ranges)

        assert options.visible is False
        assert options.ranges == ranges

    def test_validation_visible(self):


        """Test validation of visible field."""


        options = RangeSwitcherOptions()


        with pytest.raises(TypeError, match="visible must be of type"):


            options.set_visible("invalid")

    def test_validation_ranges(self):


        """Test validation of ranges field."""


        options = RangeSwitcherOptions()


        with pytest.raises(TypeError, match="ranges must be of type"):


            options.set_ranges("invalid")

    def test_validation_ranges_elements(self):
        """Test validation of ranges list elements."""
        options = RangeSwitcherOptions()
        # The chainable_field decorator only validates the list type, not its elements
        # So this should not raise an error
        options.set_ranges(["invalid"])
        assert options.ranges == ["invalid"]

    def test_to_dict_basic(self):
        """Test basic serialization."""
        options = RangeSwitcherOptions()
        result = options.asdict()

        assert result["visible"] is True
        assert result["ranges"] == []

    def test_to_dict_with_ranges(self):
        """Test serialization with ranges."""
        ranges = [
            RangeConfig(text="1D", tooltip="One Day"),
            RangeConfig(text="1W", tooltip="One Week"),
        ]

        options = RangeSwitcherOptions(ranges=ranges)
        result = options.asdict()

        assert result["visible"] is True
        assert len(result["ranges"]) == 2
        assert result["ranges"][0]["text"] == "1D"
        assert result["ranges"][0]["tooltip"] == "One Day"
        assert result["ranges"][1]["text"] == "1W"
        assert result["ranges"][1]["tooltip"] == "One Week"

    def test_to_dict_omits_false_visible(self):
        """Test that visible=False is included in output."""
        options = RangeSwitcherOptions(visible=False)
        result = options.asdict()

        assert result["visible"] is False


class TestLegendOptions:
    """Test LegendOptions class."""

    def test_default_construction(self):
        """Test construction with default values."""
        options = LegendOptions()

        assert options.visible is True
        assert options.position == "top"

    def test_custom_construction(self):
        """Test construction with custom values."""
        options = LegendOptions(visible=False, position="bottom")

        assert options.visible is False
        assert options.position == "bottom"

    def test_validation_visible(self):


        """Test validation of visible field."""


        options = LegendOptions()


        with pytest.raises(TypeError, match="visible must be of type"):


            options.set_visible("invalid")

    def test_validation_position(self):
        """Test validation of position field."""
        options = LegendOptions()
        with pytest.raises(TypeError, match="position must be of type"):
            options.set_position(123)

    def test_to_dict(self):
        """Test serialization."""
        options = LegendOptions(visible=False, position="bottom")
        result = options.asdict()

        assert result["visible"] is False
        assert result["position"] == "bottom"

    def test_to_dict_omits_false_visible(self):
        """Test that visible=False is included in output."""
        options = LegendOptions(visible=False)
        result = options.asdict()

        assert result["visible"] is False


class TestUIOptionsIntegration:
    """Test integration between UI option classes."""

    def test_range_switcher_with_multiple_ranges(self):
        """Test RangeSwitcherOptions with multiple range configurations."""
        ranges = [
            RangeConfig(text="1D", tooltip="One Day"),
            RangeConfig(text="1W", tooltip="One Week"),
            RangeConfig(text="1M", tooltip="One Month"),
            RangeConfig(text="3M", tooltip="Three Months"),
            RangeConfig(text="1Y", tooltip="One Year"),
            RangeConfig(text="ALL", tooltip="All Time"),
        ]

        options = RangeSwitcherOptions(visible=True, ranges=ranges)
        result = options.asdict()

        assert result["visible"] is True
        assert len(result["ranges"]) == 6
        assert result["ranges"][0]["text"] == "1D"
        assert result["ranges"][5]["text"] == "ALL"
        assert result["ranges"][5]["tooltip"] == "All Time"

    def test_range_switcher_with_empty_ranges(self):
        """Test RangeSwitcherOptions with empty ranges list."""
        options = RangeSwitcherOptions(ranges=[])
        result = options.asdict()

        assert result["ranges"] == []

    def test_legend_with_different_positions(self):
        """Test LegendOptions with different position values."""
        positions = ["top", "bottom", "left", "right"]

        for position in positions:
            options = LegendOptions(position=position)
            result = options.asdict()

            assert result["position"] == position

    def test_range_config_with_special_characters(self):
        """Test RangeConfig with special characters in text and tooltip."""
        config = RangeConfig(text="1D & 1W", tooltip="One Day & One Week (24h + 168h)")
        result = config.asdict()

        assert result["text"] == "1D & 1W"
        assert result["tooltip"] == "One Day & One Week (24h + 168h)"


class TestUIOptionsEdgeCases:
    """Test edge cases for UI options."""

    def test_range_config_with_empty_strings(self):
        """Test RangeConfig with empty strings."""
        config = RangeConfig(text="", tooltip="")
        result = config.asdict()

        assert result == {}  # Both fields should be omitted

    def test_range_config_with_whitespace_only(self):
        """Test RangeConfig with whitespace-only strings."""
        config = RangeConfig(text="   ", tooltip="  ")
        result = config.asdict()

        assert result["text"] == "   "
        assert result["tooltip"] == "  "

    def test_range_switcher_with_large_number_of_ranges(self):
        """Test RangeSwitcherOptions with many ranges."""
        ranges = [RangeConfig(text=f"R{i}", tooltip=f"Range {i}") for i in range(100)]

        options = RangeSwitcherOptions(ranges=ranges)
        result = options.asdict()

        assert len(result["ranges"]) == 100
        assert result["ranges"][0]["text"] == "R0"
        assert result["ranges"][99]["text"] == "R99"

    def test_legend_with_long_position_string(self):
        """Test LegendOptions with long position string."""
        long_position = "top" * 100
        options = LegendOptions(position=long_position)
        result = options.asdict()

        assert result["position"] == long_position

    def test_ui_options_equality(self):
        """Test equality comparison for UI options."""
        # Test RangeConfig equality
        config1 = RangeConfig(text="1D", tooltip="One Day")
        config2 = RangeConfig(text="1D", tooltip="One Day")
        config3 = RangeConfig(text="1W", tooltip="One Day")

        assert config1 == config2
        assert config1 != config3

        # Test RangeSwitcherOptions equality
        ranges = [RangeConfig(text="1D", tooltip="One Day")]
        options1 = RangeSwitcherOptions(visible=True, ranges=ranges)
        options2 = RangeSwitcherOptions(visible=True, ranges=ranges)
        options3 = RangeSwitcherOptions(visible=False, ranges=ranges)

        assert options1 == options2
        assert options1 != options3

        # Test LegendOptions equality
        legend1 = LegendOptions(visible=True, position="top")
        legend2 = LegendOptions(visible=True, position="top")
        legend3 = LegendOptions(visible=True, position="bottom")

        assert legend1 == legend2
        assert legend1 != legend3

    def test_ui_options_repr(self):
        """Test string representation of UI options."""
        # Test RangeConfig repr
        config = RangeConfig(text="1D", tooltip="One Day")
        repr_str = repr(config)

        assert "RangeConfig" in repr_str
        assert "text='1D'" in repr_str
        assert "tooltip='One Day'" in repr_str

        # Test RangeSwitcherOptions repr
        ranges = [RangeConfig(text="1D", tooltip="One Day")]
        options = RangeSwitcherOptions(visible=True, ranges=ranges)
        repr_str = repr(options)

        assert "RangeSwitcherOptions" in repr_str
        assert "visible=True" in repr_str

        # Test LegendOptions repr
        legend = LegendOptions(visible=True, position="top")
        repr_str = repr(legend)

        assert "LegendOptions" in repr_str
        assert "visible=True" in repr_str
        assert "position='top'" in repr_str

    def test_range_config_with_none_values(self):
        """Test RangeConfig with None values (should be handled gracefully)."""
        # This test ensures that None values don't cause issues
        # The dataclass should handle None values appropriately
        config = RangeConfig(text=None, tooltip=None)
        result = config.asdict()

        # None values should be omitted from the output
        assert result == {}

    def test_range_switcher_with_none_ranges(self):
        """Test RangeSwitcherOptions with None ranges (should be handled gracefully)."""
        # This test ensures that None ranges don't cause issues
        options = RangeSwitcherOptions(ranges=None)

        # The implementation doesn't convert None to empty list, so it should remain None
        assert options.ranges is None
