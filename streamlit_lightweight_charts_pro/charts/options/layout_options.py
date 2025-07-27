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


@dataclass
class GridLineOptions(Options):
    """Grid line configuration."""

    color: str = "#e1e3e6"
    style: LineStyle = LineStyle.SOLID
    visible: bool = False

    def __post_init__(self):
        super().__post_init__()
        # Validate color
        if not isinstance(self.color, str):
            raise TypeError(f"color must be a string, got {type(self.color)}")
        # Validate style
        if not isinstance(self.style, LineStyle):
            raise TypeError(f"style must be a LineStyle enum, got {type(self.style)}")
        # Validate visible
        if not isinstance(self.visible, bool):
            raise TypeError(f"visible must be a bool, got {type(self.visible)}")


@dataclass
class GridOptions(Options):
    """Grid configuration for chart."""

    vert_lines: GridLineOptions = field(default_factory=lambda: GridLineOptions(visible=False))
    horz_lines: GridLineOptions = field(default_factory=lambda: GridLineOptions(visible=True))

    def __post_init__(self):
        super().__post_init__()
        if not isinstance(self.vert_lines, GridLineOptions):
            raise TypeError(
                f"vert_lines must be a GridLineOptions instance, " f"got {type(self.vert_lines)}"
            )
        if not isinstance(self.horz_lines, GridLineOptions):
            raise TypeError(
                f"horz_lines must be a GridLineOptions instance, " f"got {type(self.horz_lines)}"
            )


@dataclass
class PaneOptions(Options):
    """Pane configuration for chart."""

    separator_color: str = "#e1e3ea"
    separator_hover_color: str = "#ffffff"
    enable_resize: bool = True

    def __post_init__(self):
        super().__post_init__()
        if not isinstance(self.separator_color, str):
            raise TypeError(f"separator_color must be a string, got {type(self.separator_color)}")
        if not isinstance(self.separator_hover_color, str):
            raise TypeError(
                f"separator_hover_color must be a string, "
                f"got {type(self.separator_hover_color)}"
            )
        if not isinstance(self.enable_resize, bool):
            raise TypeError(f"enable_resize must be a bool, got {type(self.enable_resize)}")


@dataclass
class LayoutOptions(Options):
    """Layout configuration for chart."""

    background_options: BackgroundSolid = field(
        default_factory=lambda: BackgroundSolid(color="#ffffff")
    )
    text_color: str = "#131722"
    font_size: int = 11
    font_family: str = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    pane_options: Optional[PaneOptions] = None

    def __post_init__(self):
        super().__post_init__()
        # Validate background
        if not isinstance(self.background_options, (BackgroundSolid, BackgroundGradient)):
            raise TypeError(
                f"background_options must be a BackgroundSolid or BackgroundGradient, "
                f"got {type(self.background_options)}"
            )
        # Validate panes
        if self.pane_options is not None and not isinstance(self.pane_options, PaneOptions):
            raise TypeError(
                f"pane_options must be a PaneOptions instance or None, "
                f"got {type(self.pane_options)}"
            )


@dataclass
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
        if not isinstance(self.visible, bool):
            raise TypeError(f"visible must be a bool, got {type(self.visible)}")
        if not isinstance(self.text, str):
            raise TypeError(f"text must be a string, got {type(self.text)}")
        if not isinstance(self.font_size, int):
            raise TypeError(f"font_size must be an int, got {type(self.font_size)}")
        if not isinstance(self.horz_align, HorzAlign):
            raise TypeError(f"horz_align must be a HorzAlign enum, got {type(self.horz_align)}")
        if not isinstance(self.vert_align, VertAlign):
            raise TypeError(f"vert_align must be a VertAlign enum, got {type(self.vert_align)}")
        if not isinstance(self.color, str):
            raise TypeError(f"color must be a string, got {type(self.color)}")
