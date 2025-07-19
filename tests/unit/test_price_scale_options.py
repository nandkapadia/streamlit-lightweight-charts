"""
Unit tests for PriceScaleOptions and price scale functionality.
"""

import pytest
from unittest.mock import Mock, patch

from streamlit_lightweight_charts_pro.charts import (
    PriceScaleOptions,
    PriceScale,
    RightPriceScale,
    LeftPriceScale,
    OverlayPriceScale,
    PriceScaleMargins,
)
from streamlit_lightweight_charts_pro.type_definitions import PriceScaleMode


class TestPriceScaleOptions:
    """Test cases for PriceScaleOptions (alias for PriceScale)."""

    def test_price_scale_options_alias(self):
        """Test that PriceScaleOptions is an alias for PriceScale."""
        assert PriceScaleOptions is PriceScale

    def test_basic_price_scale_creation(self):
        """Test basic PriceScale creation."""
        price_scale = PriceScaleOptions()

        assert price_scale.visible is True
        assert price_scale.auto_scale is True
        assert price_scale.mode == PriceScaleMode.NORMAL
        assert price_scale.invert_scale is False
        assert price_scale.border_visible is True
        assert price_scale.ticks_visible is True
        assert price_scale.minimum_width == 72

    def test_price_scale_with_custom_values(self):
        """Test PriceScale with custom values."""
        price_scale = PriceScaleOptions(
            visible=False,
            auto_scale=False,
            mode=PriceScaleMode.LOGARITHMIC,
            invert_scale=True,
            border_visible=False,
            ticks_visible=False,
            minimum_width=100,
            text_color="#FF0000",
            font_size=14,
        )

        assert price_scale.visible is False
        assert price_scale.auto_scale is False
        assert price_scale.mode == PriceScaleMode.LOGARITHMIC
        assert price_scale.invert_scale is True
        assert price_scale.border_visible is False
        assert price_scale.ticks_visible is False
        assert price_scale.minimum_width == 100
        assert price_scale.text_color == "#FF0000"
        assert price_scale.font_size == 14

    def test_price_scale_margins(self):
        """Test PriceScale margins configuration."""
        margins = PriceScaleMargins(top=0.2, bottom=0.3)
        price_scale = PriceScaleOptions(scale_margins=margins)

        assert price_scale.scale_margins.top == 0.2
        assert price_scale.scale_margins.bottom == 0.3

    def test_price_scale_to_dict(self):
        """Test PriceScale to_dict method."""
        price_scale = PriceScaleOptions(
            visible=True,
            auto_scale=True,
            mode=PriceScaleMode.NORMAL,
            border_visible=True,
            text_color="#333333",
            font_size=12,
            minimum_width=80,
        )

        result = price_scale.to_dict()

        assert result["visible"] is True
        assert result["autoScale"] is True
        assert result["mode"] == PriceScaleMode.NORMAL.value
        assert result["borderVisible"] is True
        assert result["textColor"] == "#333333"
        assert result["fontSize"] == 12
        assert result["minimumWidth"] == 80

    def test_price_scale_with_id(self):
        """Test PriceScale with price_scale_id."""
        price_scale = PriceScaleOptions(price_scale_id="custom_scale")

        result = price_scale.to_dict()
        assert result["priceScaleId"] == "custom_scale"

    def test_right_price_scale(self):
        """Test RightPriceScale default configuration."""
        right_scale = RightPriceScale()

        assert right_scale.price_scale_id == "right"
        assert right_scale.visible is True
        assert right_scale.auto_scale is True

    def test_left_price_scale(self):
        """Test LeftPriceScale default configuration."""
        left_scale = LeftPriceScale()

        assert left_scale.price_scale_id == "left"
        assert left_scale.visible is True
        assert left_scale.auto_scale is True

    def test_overlay_price_scale(self):
        """Test OverlayPriceScale configuration."""
        # Should raise error without price_scale_id
        with pytest.raises(ValueError):
            OverlayPriceScale()

        # Should work with price_scale_id
        overlay_scale = OverlayPriceScale(price_scale_id="overlay_1")
        assert overlay_scale.price_scale_id == "overlay_1"

    def test_price_scale_margins_to_dict(self):
        """Test PriceScaleMargins to_dict method."""
        margins = PriceScaleMargins(top=0.1, bottom=0.2)
        result = margins.to_dict()

        assert result["top"] == 0.1
        assert result["bottom"] == 0.2

    def test_price_scale_edge_cases(self):
        """Test PriceScale edge cases."""
        # Test with minimum width 0 (should be adjusted)
        price_scale = PriceScaleOptions(minimum_width=0)
        result = price_scale.to_dict()
        assert result["minimumWidth"] == 72  # Should be adjusted to minimum

        # Test with negative minimum width
        price_scale = PriceScaleOptions(minimum_width=-10)
        result = price_scale.to_dict()
        assert result["minimumWidth"] == 72  # Should be adjusted to minimum

        # Test invisible scale
        price_scale = PriceScaleOptions(visible=False, minimum_width=100)
        result = price_scale.to_dict()
        assert result["minimumWidth"] == 0  # Should be 0 for invisible scale

    def test_price_scale_modes(self):
        """Test different PriceScale modes."""
        # Normal mode
        normal_scale = PriceScaleOptions(mode=PriceScaleMode.NORMAL)
        assert normal_scale.to_dict()["mode"] == PriceScaleMode.NORMAL.value

        # Logarithmic mode
        log_scale = PriceScaleOptions(mode=PriceScaleMode.LOGARITHMIC)
        assert log_scale.to_dict()["mode"] == PriceScaleMode.LOGARITHMIC.value

    def test_price_scale_handle_configuration(self):
        """Test PriceScale handle configuration."""
        price_scale = PriceScaleOptions(handle_scale=True, handle_size=25)

        result = price_scale.to_dict()
        assert result["handleScale"] is True
        assert result["handleSize"] == 25

    def test_price_scale_font_configuration(self):
        """Test PriceScale font configuration."""
        price_scale = PriceScaleOptions(font_size=16, font_weight="bold")

        result = price_scale.to_dict()
        assert result["fontSize"] == 16
        assert result["fontWeight"] == "bold"

    def test_price_scale_tick_configuration(self):
        """Test PriceScale tick configuration."""
        price_scale = PriceScaleOptions(
            ticks_visible=False,
            draw_ticks=False,
            ensure_edge_tick_marks_visible=True,
            align_labels=False,
            entire_text_only=True,
        )

        result = price_scale.to_dict()
        assert result["ticksVisible"] is False
        assert result["drawTicks"] is False
        assert result["ensureEdgeTickMarksVisible"] is True
        assert result["alignLabels"] is False
        assert result["entireTextOnly"] is True

    def test_price_scale_border_configuration(self):
        """Test PriceScale border configuration."""
        price_scale = PriceScaleOptions(border_visible=False, border_color="#FF0000")

        result = price_scale.to_dict()
        assert result["borderVisible"] is False
        assert result["borderColor"] == "#FF0000"

    def test_price_scale_invert_scale(self):
        """Test PriceScale invert scale configuration."""
        price_scale = PriceScaleOptions(invert_scale=True)

        result = price_scale.to_dict()
        assert result["invertScale"] is True

    def test_price_scale_immutability(self):
        """Test that PriceScale attributes can be modified."""
        price_scale = PriceScaleOptions()

        # Should be able to modify attributes
        price_scale.visible = False
        price_scale.text_color = "#FF0000"

        assert price_scale.visible is False
        assert price_scale.text_color == "#FF0000"

    def test_price_scale_equality(self):
        """Test PriceScale equality."""
        scale1 = PriceScaleOptions(visible=True, text_color="#333333")
        scale2 = PriceScaleOptions(visible=True, text_color="#333333")
        scale3 = PriceScaleOptions(visible=False, text_color="#333333")

        assert scale1 == scale2
        assert scale1 != scale3

    def test_price_scale_hash(self):
        """Test PriceScale hashability."""
        scale1 = PriceScaleOptions(visible=True)
        scale2 = PriceScaleOptions(visible=True)

        # Note: PriceScaleOptions is not hashable in current implementation
        # This is expected behavior for dataclasses with mutable fields
        with pytest.raises(TypeError):
            hash(scale1)

        with pytest.raises(TypeError):
            hash(scale2)

        # But equality should still work
        assert scale1 == scale2

    def test_price_scale_repr(self):
        """Test PriceScale string representation."""
        price_scale = PriceScaleOptions(visible=True, text_color="#333333")
        repr_str = repr(price_scale)

        assert "PriceScale" in repr_str
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
        """Test PriceScale integration with ChartOptions."""
        from streamlit_lightweight_charts_pro.charts import ChartOptions

        right_scale = RightPriceScale(visible=True, text_color="#333333")
        left_scale = LeftPriceScale(visible=False)

        options = ChartOptions(right_price_scale=right_scale, left_price_scale=left_scale)

        result = options.to_dict()

        assert "rightPriceScale" in result
        assert result["rightPriceScale"]["visible"] is True
        assert result["rightPriceScale"]["textColor"] == "#333333"

        assert "leftPriceScale" in result
        assert result["leftPriceScale"]["visible"] is False

    def test_price_scale_overlay_integration(self):
        """Test PriceScale overlay integration."""
        from streamlit_lightweight_charts_pro.charts import ChartOptions

        overlay_scale = OverlayPriceScale(
            price_scale_id="volume", visible=True, ticks_visible=False, border_visible=False
        )

        options = ChartOptions(overlay_price_scales={"volume": overlay_scale.to_dict()})

        result = options.to_dict()

        assert "overlayPriceScales" in result
        assert "volume" in result["overlayPriceScales"]
        assert result["overlayPriceScales"]["volume"]["visible"] is True
        assert result["overlayPriceScales"]["volume"]["ticksVisible"] is False
        assert result["overlayPriceScales"]["volume"]["borderVisible"] is False
