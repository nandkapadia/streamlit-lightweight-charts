"""
Layout options configuration for streamlit-lightweight-charts.

This module provides layout-related option classes for configuring
chart appearance, grid settings, panes, and watermarks.
"""

from dataclasses import dataclass, field
from typing import Optional

from streamlit_lightweight_charts_pro.charts.options.base_options import Options
from streamlit_lightweight_charts_pro.type_definitions.colors import (
    BackgroundGradient,
    BackgroundSolid,
)
from streamlit_lightweight_charts_pro.type_definitions.enums import (
    HorzAlign,
    LineStyle,
    VertAlign,
)
from streamlit_lightweight_charts_pro.utils import chainable_field
from streamlit_lightweight_charts_pro.utils.data_utils import is_valid_color


@dataclass
@chainable_field(
    "color", str, validator=lambda v: GridLineOptions._validate_color_static(v, "color")
)
@chainable_field("style", LineStyle)
@chainable_field("visible", bool)
class GridLineOptions(Options):
    """Grid line configuration."""

    color: str = "#e1e3e6"
    style: LineStyle = LineStyle.SOLID
    visible: bool = False

    def __post_init__(self):
        super().__post_init__()

    @staticmethod
    def _validate_color_static(color: str, property_name: str) -> str:
        """Static version of color validator for decorator use."""
        if not is_valid_color(color):
            raise ValueError(
                f"Invalid color format for {property_name}: {color!r}. Must be hex or rgba."
            )
        return color


@dataclass
@chainable_field("vert_lines", GridLineOptions)
@chainable_field("horz_lines", GridLineOptions)
class GridOptions(Options):
    """Grid configuration for chart."""

    vert_lines: GridLineOptions = field(default_factory=lambda: GridLineOptions(visible=False))
    horz_lines: GridLineOptions = field(default_factory=lambda: GridLineOptions(visible=True))

    def __post_init__(self):
        super().__post_init__()


@dataclass
@chainable_field(
    "separator_color",
    str,
    validator=lambda v: PaneOptions._validate_color_static(v, "separator_color"),
)
@chainable_field(
    "separator_hover_color",
    str,
    validator=lambda v: PaneOptions._validate_color_static(v, "separator_hover_color"),
)
@chainable_field("enable_resize", bool)
class PaneOptions(Options):
    """Pane configuration for chart."""

    separator_color: str = "#e1e3ea"
    separator_hover_color: str = "#ffffff"
    enable_resize: bool = True

    def __post_init__(self):
        super().__post_init__()

    @staticmethod
    def _validate_color_static(color: str, property_name: str) -> str:
        """Static version of color validator for decorator use."""
        if not is_valid_color(color):
            raise ValueError(
                f"Invalid color format for {property_name}: {color!r}. Must be hex or rgba."
            )
        return color


@dataclass
@chainable_field("background_options", (BackgroundSolid, BackgroundGradient))
@chainable_field(
    "text_color", str, validator=lambda v: LayoutOptions._validate_color_static(v, "text_color")
)
@chainable_field("font_size", int)
@chainable_field("font_family", str)
@chainable_field("pane_options", PaneOptions)
@chainable_field("attribution_logo", bool)
class LayoutOptions(Options):
    """Layout configuration for chart."""

    background_options: BackgroundSolid = field(
        default_factory=lambda: BackgroundSolid(color="#ffffff")
    )
    text_color: str = "#131722"
    font_size: int = 11
    font_family: str = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    pane_options: Optional[PaneOptions] = None
    attribution_logo: bool = False

    def __post_init__(self):
        super().__post_init__()

    @staticmethod
    def _validate_color_static(color: str, property_name: str) -> str:
        """Static version of color validator for decorator use."""
        if not is_valid_color(color):
            raise ValueError(
                f"Invalid color format for {property_name}: {color!r}. Must be hex or rgba."
            )
        return color


@dataclass
@chainable_field("visible", bool)
@chainable_field("text", str)
@chainable_field("font_size", int)
@chainable_field("horz_align", HorzAlign)
@chainable_field("vert_align", VertAlign)
@chainable_field(
    "color", str, validator=lambda v: WatermarkOptions._validate_color_static(v, "color")
)
class WatermarkOptions(Options):
    """Watermark configuration."""

    visible: bool = True
    text: str = ""
    font_size: int = 96
    horz_align: HorzAlign = HorzAlign.CENTER
    vert_align: VertAlign = VertAlign.CENTER
    color: str = "rgba(255, 255, 255, 0.1)"

    def __post_init__(self):
        super().__post_init__()

    @staticmethod
    def _validate_color_static(color: str, property_name: str) -> str:
        """Static version of color validator for decorator use."""
        if not is_valid_color(color):
            raise ValueError(
                f"Invalid color format for {property_name}: {color!r}. Must be hex or rgba."
            )
        return color
