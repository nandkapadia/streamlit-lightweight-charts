"""Price scale option classes for streamlit-lightweight-charts."""

from dataclasses import dataclass, field
from typing import Any, Dict

from streamlit_lightweight_charts_pro.type_definitions import PriceScaleMode


@dataclass
class PriceScaleMargins:
    """Price scale margins configuration."""

    top: float = 0.1
    bottom: float = 0.1

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {"top": self.top, "bottom": self.bottom}


@dataclass
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
    text_color: str = "#333333"
    font_size: int = 11
    font_weight: str = "400"

    # Tick and label configuration
    ticks_visible: bool = True
    draw_ticks: bool = True
    ensure_edge_tick_marks_visible: bool = False
    align_labels: bool = True
    entire_text_only: bool = False

    # Size and positioning
    minimum_width: int = 72
    scale_margins: PriceScaleMargins = field(default_factory=PriceScaleMargins)

    # Interaction
    handle_scale: bool = False
    handle_size: int = 20

    # Identification
    price_scale_id: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation for lightweight-charts v5.x."""
        # Ensure minimumWidth is never 0 to prevent invisible Y-axis labels
        safe_minimum_width = max(self.minimum_width, 72) if self.visible else 0

        result = {
            "visible": self.visible,
            "autoScale": self.auto_scale,
            "mode": self.mode.value,
            "invertScale": self.invert_scale,
            "borderVisible": self.border_visible,
            "borderColor": self.border_color,
            "textColor": self.text_color,
            "fontSize": self.font_size,
            "fontWeight": self.font_weight,
            "ticksVisible": self.ticks_visible,
            "drawTicks": self.draw_ticks,
            "ensureEdgeTickMarksVisible": self.ensure_edge_tick_marks_visible,
            "alignLabels": self.align_labels,
            "entireTextOnly": self.entire_text_only,
            "minimumWidth": safe_minimum_width,
            "scaleMargins": self.scale_margins.to_dict(),
            "handleScale": self.handle_scale,
            "handleSize": self.handle_size,
        }

        if self.price_scale_id:
            result["priceScaleId"] = self.price_scale_id

        return result


@dataclass
class RightPriceScaleOptions(PriceScaleOptions):
    """Right price scale configuration."""

    def __post_init__(self):
        """Set default values specific to right price scale."""
        if not self.price_scale_id:
            self.price_scale_id = "right"


@dataclass
class LeftPriceScaleOptions(PriceScaleOptions):
    """Left price scale configuration."""

    def __post_init__(self):
        """Set default values specific to left price scale."""
        if not self.price_scale_id:
            self.price_scale_id = "left"


@dataclass
class OverlayPriceScaleOptions(PriceScaleOptions):
    """Overlay price scale configuration."""

    def __post_init__(self):
        """Ensure overlay price scale has a unique ID."""
        if not self.price_scale_id:
            raise ValueError("Overlay price scale must have a unique price_scale_id")


# Backward compatibility aliases
PriceScale = PriceScaleOptions
RightPriceScale = RightPriceScaleOptions
LeftPriceScale = LeftPriceScaleOptions
OverlayPriceScale = OverlayPriceScaleOptions
