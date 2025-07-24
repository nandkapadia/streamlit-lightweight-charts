"""Price scale option classes for streamlit-lightweight-charts."""

from dataclasses import dataclass
from typing import Any, Dict

from streamlit_lightweight_charts_pro.type_definitions.enums import PriceScaleMode


@dataclass
class PriceScaleMargins:
    """Price scale margins configuration."""

    top: float = 0.1
    bottom: float = 0.1

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {"top": self.top, "bottom": self.bottom}


class PriceScaleOptions:
    """Price scale configuration for lightweight-charts v5.x."""

    # Core visibility and behavior
    visible: bool = True
    auto_scale: bool = True
    mode: PriceScaleMode = PriceScaleMode.NORMAL
    invert_scale: bool = False

    # Visual appearance
    border_visible: bool = True
    border_color: str = "rgba(197, 203, 206, 0.8)"
    text_color: str = "#131722"  # TradingView dark gray text

    # Tick and label configuration
    ticks_visible: bool = True
    ensure_edge_tick_marks_visible: bool = False
    align_labels: bool = True
    entire_text_only: bool = False

    # Size and positioning
    minimum_width: int = 72
    scale_margins: PriceScaleMargins = None

    # Identification
    price_scale_id: str = ""

    def __init__(
        self,
        visible: bool = True,
        auto_scale: bool = True,
        mode: PriceScaleMode = PriceScaleMode.NORMAL,
        invert_scale: bool = False,
        border_visible: bool = True,
        border_color: str = "rgba(197, 203, 206, 0.8)",
        text_color: str = "#131722",
        ticks_visible: bool = True,
        ensure_edge_tick_marks_visible: bool = False,
        align_labels: bool = True,
        entire_text_only: bool = False,
        minimum_width: int = 72,
        scale_margins: PriceScaleMargins = None,
        price_scale_id: str = "",
    ):
        self.visible = visible
        self.auto_scale = auto_scale
        self.mode = mode
        self.invert_scale = invert_scale
        self.border_visible = border_visible
        self.border_color = border_color
        self.text_color = text_color
        self.ticks_visible = ticks_visible
        self.ensure_edge_tick_marks_visible = ensure_edge_tick_marks_visible
        self.align_labels = align_labels
        self.entire_text_only = entire_text_only
        self.minimum_width = minimum_width
        self.scale_margins = scale_margins or PriceScaleMargins()
        self.price_scale_id = price_scale_id

    def __getitem__(self, key):
        # Only allow snake_case keys for attribute access
        allowed_keys = {
            "visible": "visible",
            "auto_scale": "auto_scale",
            "mode": "mode",
            "invert_scale": "invert_scale",
            "border_visible": "border_visible",
            "border_color": "border_color",
            "text_color": "text_color",
            "font_size": "font_size",
            "font_weight": "font_weight",
            "ticks_visible": "ticks_visible",
            "draw_ticks": "draw_ticks",
            "ensure_edge_tick_marks_visible": "ensure_edge_tick_marks_visible",
            "align_labels": "align_labels",
            "entire_text_only": "entire_text_only",
            "minimum_width": "minimum_width",
            "scale_margins": "scale_margins",
            "handle_scale": "handle_scale",
            "handle_size": "handle_size",
            "price_scale_id": "price_scale_id",
        }
        if key not in allowed_keys:
            raise KeyError(f"Only snake_case keys are allowed: {key}")
        attr = allowed_keys[key]
        return getattr(self, attr)

    def to_dict(self) -> Dict[str, Any]:
        # Defensive conversion: always output a plain dict for scaleMargins
        scale_margins_dict = self.scale_margins
        scale_margins_dict = dict(self.scale_margins.to_dict())

        result = {
            "visible": self.visible,
            "autoScale": self.auto_scale,
            "mode": self.mode.value,
            "invertScale": self.invert_scale,
            "borderVisible": self.border_visible,
            "borderColor": self.border_color,
            "textColor": self.text_color,
            "ticksVisible": self.ticks_visible,
            "ensureEdgeTickMarksVisible": self.ensure_edge_tick_marks_visible,
            "alignLabels": self.align_labels,
            "entireTextOnly": self.entire_text_only,
            "minimumWidth": self.minimum_width,
            "scaleMargins": scale_margins_dict,
        }
        if self.price_scale_id:
            result["priceScaleId"] = self.price_scale_id
        return result

    def __eq__(self, other):
        if not isinstance(other, PriceScaleOptions):
            return False
        # Compare all attributes
        return all(
            getattr(self, attr) == getattr(other, attr)
            for attr in [
                "visible",
                "auto_scale",
                "mode",
                "invert_scale",
                "border_visible",
                "border_color",
                "text_color",
                "font_size",
                "font_weight",
                "ticks_visible",
                "draw_ticks",
                "ensure_edge_tick_marks_visible",
                "align_labels",
                "entire_text_only",
                "minimum_width",
                "scale_margins",
                "handle_scale",
                "handle_size",
                "price_scale_id",
            ]
        )

    def __hash__(self):
        # Not hashable due to mutable fields, so raise TypeError
        raise TypeError("PriceScaleOptions is not hashable")

    def __repr__(self):
        attrs = [
            f"visible={self.visible!r}",
            f"auto_scale={self.auto_scale!r}",
            f"mode={self.mode!r}",
            f"invert_scale={self.invert_scale!r}",
            f"border_visible={self.border_visible!r}",
            f"border_color={self.border_color!r}",
            f"text_color={self.text_color!r}",
            f"ticks_visible={self.ticks_visible!r}",
            f"ensure_edge_tick_marks_visible={self.ensure_edge_tick_marks_visible!r}",
            f"align_labels={self.align_labels!r}",
            f"entire_text_only={self.entire_text_only!r}",
            f"minimum_width={self.minimum_width!r}",
            f"scale_margins={self.scale_margins!r}",
            f"price_scale_id={self.price_scale_id!r}",
        ]
        return f"PriceScaleOptions({', '.join(attrs)})"
