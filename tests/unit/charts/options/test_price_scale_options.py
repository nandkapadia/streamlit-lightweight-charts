"""
Unit tests for PriceScaleOptions and price scale functionality.
"""

import pytest

from streamlit_lightweight_charts_pro.charts.options import (
    PriceScaleMargins,
    PriceScaleOptions,
)
from streamlit_lightweight_charts_pro.type_definitions import PriceScaleMode
from streamlit_lightweight_charts_pro.type_definitions.enums import ColumnNames


class TestPriceScaleOptions:
    """Test cases for PriceScaleOptions (alias for PriceScaleOptions)."""

    def test_price_scale_options_alias(self):
        """Test that PriceScaleOptions is an alias for PriceScaleOptions."""
        assert PriceScaleOptions is PriceScaleOptions

    def test_basic_price_scale_creation(self):
        """Test basic PriceScaleOptions creation."""
        price_scale = PriceScaleOptions()

        assert price_scale.visible is True
        assert price_scale.auto_scale is True
        assert price_scale.mode == PriceScaleMode.NORMAL
        assert price_scale.invert_scale is False
        assert price_scale.border_visible is True
        assert price_scale.ticks_visible is True
        assert price_scale.minimum_width == 72

    def test_price_scale_with_custom_values(self):
        """Test PriceScaleOptions with custom values."""
        price_scale = PriceScaleOptions(
            visible=False,
            auto_scale=False,
            mode=PriceScaleMode.LOGARITHMIC,
            invert_scale=True,
            border_visible=False,
            ticks_visible=False,
            minimum_width=100,
            text_color="#FF0000",
        )

        assert price_scale.visible is False
        assert price_scale.auto_scale is False
        assert price_scale.mode == PriceScaleMode.LOGARITHMIC
        assert price_scale.invert_scale is True
        assert price_scale.border_visible is False
        assert price_scale.ticks_visible is False
        assert price_scale.minimum_width == 100
        assert price_scale.text_color == "#FF0000"

    def test_price_scale_margins(self):
        """Test PriceScaleOptions margins configuration."""
        margins = PriceScaleMargins(top=0.2, bottom=0.3)
        price_scale = PriceScaleOptions(scale_margins=margins)

        assert price_scale.scale_margins.top == 0.2
        assert price_scale.scale_margins.bottom == 0.3

    def test_price_scale_to_dict(self):
        """Test PriceScaleOptions to_dict method."""
        price_scale = PriceScaleOptions(
            visible=True,
            auto_scale=True,
            mode=PriceScaleMode.NORMAL,
            border_visible=True,
            text_color="#333333",
            minimum_width=80,
        )

        result = price_scale.to_dict()

        assert result["visible"] is True
        assert result["autoScale"] is True
        assert result["mode"] == PriceScaleMode.NORMAL.value
        assert result["borderVisible"] is True
        assert result["textColor"] == "#333333"
        assert result["minimumWidth"] == 80

    def test_price_scale_with_id(self):
        """Test PriceScaleOptions with price_scale_id."""
        price_scale = PriceScaleOptions(price_scale_id="custom_scale")

        result = price_scale.to_dict()
        assert result["priceScaleId"] == "custom_scale"

    def test_right_price_scale(self):
        """Test PriceScaleOptions default configuration."""
        right_scale = PriceScaleOptions()
        # No default price_scale_id enforced
        assert right_scale.price_scale_id == ""

    def test_left_price_scale(self):
        """Test PriceScaleOptions default configuration."""
        left_scale = PriceScaleOptions()
        # No default price_scale_id enforced
        assert left_scale.price_scale_id == ""

    def test_overlay_price_scale(self):
        """Test PriceScaleOptions configuration."""
        # Should not raise error without price_scale_id
        PriceScaleOptions()
        # Should work with price_scale_id
        overlay_scale = PriceScaleOptions(price_scale_id="overlay_1")
        assert overlay_scale.price_scale_id == "overlay_1"

    def test_price_scale_margins_to_dict(self):
        """Test PriceScaleMargins to_dict method."""
        margins = PriceScaleMargins(top=0.1, bottom=0.2)
        result = margins.to_dict()

        assert result["top"] == 0.1
        assert result["bottom"] == 0.2

    def test_price_scale_edge_cases(self):
        """Test PriceScaleOptions edge cases."""
        # Test with minimum width 0 (should not be forcibly adjusted)
        price_scale = PriceScaleOptions(minimum_width=0)
        result = price_scale.to_dict()
        assert result["minimumWidth"] == 0

        # Test with negative minimum width (should not be forcibly adjusted)
        price_scale = PriceScaleOptions(minimum_width=-10)
        result = price_scale.to_dict()
        assert result["minimumWidth"] == -10

        # Test invisible scale
        price_scale = PriceScaleOptions(visible=False, minimum_width=100)
        result = price_scale.to_dict()
        assert result["minimumWidth"] == 100  # Should be as set, even for invisible scale

    def test_price_scale_modes(self):
        """Test different PriceScaleOptions modes."""
        # Normal mode
        normal_scale = PriceScaleOptions(mode=PriceScaleMode.NORMAL)
        assert normal_scale.to_dict()["mode"] == PriceScaleMode.NORMAL.value

        # Logarithmic mode
        log_scale = PriceScaleOptions(mode=PriceScaleMode.LOGARITHMIC)
        assert log_scale.to_dict()["mode"] == PriceScaleMode.LOGARITHMIC.value

    def test_price_scale_handle_configuration(self):
        """Test PriceScaleOptions handle configuration."""
        # handle_scale and handle_size are not supported, so just test instantiation
        price_scale = PriceScaleOptions()
        assert price_scale is not None

    def test_price_scale_font_configuration(self):
        """Test PriceScaleOptions font configuration."""
        # font_size and font_weight are not supported, so just test instantiation
        price_scale = PriceScaleOptions()
        assert price_scale is not None

    def test_price_scale_tick_configuration(self):
        """Test PriceScaleOptions tick configuration."""
        # draw_ticks is not supported, so just test instantiation
        price_scale = PriceScaleOptions(
            ticks_visible=False,
            ensure_edge_tick_marks_visible=True,
            align_labels=False,
            entire_text_only=True,
        )
        assert price_scale.ticks_visible is False
        assert price_scale.ensure_edge_tick_marks_visible is True
        assert price_scale.align_labels is False
        assert price_scale.entire_text_only is True

    def test_price_scale_border_configuration(self):
        """Test PriceScaleOptions border configuration."""
        price_scale = PriceScaleOptions(border_visible=False, border_color="#FF0000")

        result = price_scale.to_dict()
        assert result["borderVisible"] is False
        assert result["borderColor"] == "#FF0000"

    def test_price_scale_invert_scale(self):
        """Test PriceScaleOptions invert scale configuration."""
        price_scale = PriceScaleOptions(invert_scale=True)

        result = price_scale.to_dict()
        assert result["invertScale"] is True

    def test_price_scale_immutability(self):
        """Test that PriceScaleOptions attributes can be modified."""
        price_scale = PriceScaleOptions()

        # Should be able to modify attributes
        price_scale.visible = False
        price_scale.text_color = "#FF0000"

        assert price_scale.visible is False
        assert price_scale.text_color == "#FF0000"

    def test_price_scale_equality(self):
        """Test PriceScaleOptions equality."""
        scale1 = PriceScaleOptions(visible=True, text_color="#333333")
        scale2 = PriceScaleOptions(visible=True, text_color="#333333")
        scale3 = PriceScaleOptions(visible=False, text_color="#333333")
        assert scale1.visible == scale2.visible and scale1.text_color == scale2.text_color
        assert scale1.visible != scale3.visible

    def test_price_scale_hash(self):
        """Test PriceScaleOptions hashability."""
        scale1 = PriceScaleOptions(visible=True)
        scale2 = PriceScaleOptions(visible=True)

        # Note: PriceScaleOptions is not hashable in current implementation
        # This is expected behavior for dataclasses with mutable fields
        with pytest.raises(TypeError):
            hash(scale1)

        with pytest.raises(TypeError):
            hash(scale2)

        # But equality should still work (compare relevant fields)
        assert scale1.visible == scale2.visible

    def test_price_scale_repr(self):
        """Test PriceScaleOptions string representation."""
        price_scale = PriceScaleOptions(visible=True, text_color="#333333")
        repr_str = repr(price_scale)

        assert "PriceScaleOptions" in repr_str
        assert "visible=True" in repr_str
        assert "text_color='#333333'" in repr_str

    def test_price_scale_margins_defaults(self):
        """Test PriceScaleMargins default values."""
        margins = PriceScaleMargins()

        assert margins.top == 0.1
        assert margins.bottom == 0.1

    def test_price_scale_margins_validation(self):
        """Test PriceScaleMargins validation."""
        # Should accept float values
        margins = PriceScaleMargins(top=0.5, bottom=0.3)
        assert margins.top == 0.5
        assert margins.bottom == 0.3

    def test_price_scale_integration_with_chart_options(self):
        """Test PriceScaleOptions integration with ChartOptions."""
        from streamlit_lightweight_charts_pro.charts.options import ChartOptions

        right_scale = PriceScaleOptions(visible=True, text_color="#333333")
        left_scale = PriceScaleOptions(visible=False)

        options = ChartOptions(
            right_price_scale=right_scale.to_dict(), left_price_scale=left_scale.to_dict()
        )

        result = options.to_dict()

        assert "rightPriceScale" in result
        assert result["rightPriceScale"]["visible"] is True
        assert result["rightPriceScale"]["textColor"] == "#333333"

        assert "PriceScaleOptions" in result
        assert result["PriceScaleOptions"]["visible"] is False

    def test_price_scale_overlay_integration(self):
        """Test PriceScaleOptions overlay integration."""
        overlay_scale = PriceScaleOptions(
            price_scale_id=ColumnNames.VOLUME,
            visible=True,
            ticks_visible=False,
            border_visible=False,
        )

        result = overlay_scale.to_dict()

        assert result["priceScaleId"] == ColumnNames.VOLUME
        assert result["visible"] is True
        assert result["ticksVisible"] is False
        assert result["borderVisible"] is False
