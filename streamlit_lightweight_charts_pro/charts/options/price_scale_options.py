"""Price scale option classes for streamlit-lightweight-charts."""

from dataclasses import dataclass, field

from streamlit_lightweight_charts_pro.charts.options.base_options import Options
from streamlit_lightweight_charts_pro.type_definitions.enums import PriceScaleMode


@dataclass
class PriceScaleMargins(Options):
    """Price scale margins configuration."""

    top: float = 0.1
    bottom: float = 0.1

    def __post_init__(self):
        super().__post_init__()
        if not isinstance(self.top, (int, float)):
            raise TypeError(f"top must be a number, got {type(self.top)}")
        if not isinstance(self.bottom, (int, float)):
            raise TypeError(f"bottom must be a number, got {type(self.bottom)}")


@dataclass
class PriceScaleOptions(Options):
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
    scale_margins: PriceScaleMargins = field(default_factory=PriceScaleMargins)

    # Identification
    price_scale_id: str = ""

    def __post_init__(self):
        super().__post_init__()
        # Validate core fields
        if not isinstance(self.visible, bool):
            raise TypeError(f"visible must be a bool, got {type(self.visible)}")
        if not isinstance(self.auto_scale, bool):
            raise TypeError(f"auto_scale must be a bool, got {type(self.auto_scale)}")
        if not isinstance(self.mode, PriceScaleMode):
            raise TypeError(f"mode must be a PriceScaleMode enum, got {type(self.mode)}")
        if not isinstance(self.invert_scale, bool):
            raise TypeError(f"invert_scale must be a bool, got {type(self.invert_scale)}")

        # Validate visual appearance fields
        if not isinstance(self.border_visible, bool):
            raise TypeError(f"border_visible must be a bool, got {type(self.border_visible)}")
        if not isinstance(self.border_color, str):
            raise TypeError(f"border_color must be a string, got {type(self.border_color)}")
        if not isinstance(self.text_color, str):
            raise TypeError(f"text_color must be a string, got {type(self.text_color)}")

        # Validate tick and label fields
        if not isinstance(self.ticks_visible, bool):
            raise TypeError(f"ticks_visible must be a bool, got {type(self.ticks_visible)}")
        if not isinstance(self.ensure_edge_tick_marks_visible, bool):
            raise TypeError(
                f"ensure_edge_tick_marks_visible must be a bool, "
                f"got {type(self.ensure_edge_tick_marks_visible)}"
            )
        if not isinstance(self.align_labels, bool):
            raise TypeError(f"align_labels must be a bool, got {type(self.align_labels)}")
        if not isinstance(self.entire_text_only, bool):
            raise TypeError(f"entire_text_only must be a bool, got {type(self.entire_text_only)}")

        # Validate size and positioning fields
        if not isinstance(self.minimum_width, int):
            raise TypeError(f"minimum_width must be an int, got {type(self.minimum_width)}")
        if self.scale_margins is not None and not isinstance(self.scale_margins, PriceScaleMargins):
            raise TypeError(
                f"scale_margins must be a PriceScaleMargins instance or None, "
                f"got {type(self.scale_margins)}"
            )

        # Validate identification fields
        if not isinstance(self.price_scale_id, str):
            raise TypeError(f"price_scale_id must be a string, got {type(self.price_scale_id)}")
