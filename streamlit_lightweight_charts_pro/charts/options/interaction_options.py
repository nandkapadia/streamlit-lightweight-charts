"""
Interaction options configuration for streamlit-lightweight-charts.

This module provides interaction-related option classes for configuring
crosshair behavior, kinetic scrolling, and tracking modes.
"""

from dataclasses import dataclass, field

from streamlit_lightweight_charts_pro.charts.options.base_options import Options
from streamlit_lightweight_charts_pro.type_definitions.enums import (
    CrosshairMode,
    LineStyle,
)


@dataclass
class CrosshairLineOptions(Options):
    """Crosshair line configuration."""

    color: str = "#758696"
    width: int = 1
    style: LineStyle = LineStyle.SOLID
    visible: bool = True
    label_visible: bool = True

    def __post_init__(self):
        super().__post_init__()
        if not isinstance(self.color, str):
            raise TypeError(f"color must be a string, got {type(self.color)}")
        if not isinstance(self.width, int):
            raise TypeError(f"width must be an int, got {type(self.width)}")
        if not isinstance(self.style, LineStyle):
            raise TypeError(f"style must be a LineStyle enum, got {type(self.style)}")
        if not isinstance(self.visible, bool):
            raise TypeError(f"visible must be a bool, got {type(self.visible)}")
        if not isinstance(self.label_visible, bool):
            raise TypeError(f"label_visible must be a bool, got {type(self.label_visible)}")


@dataclass
class CrosshairSyncOptions(Options):
    """Crosshair synchronization configuration."""

    group_id: int = 1
    suppress_series_animations: bool = True

    def __post_init__(self):
        super().__post_init__()
        if not isinstance(self.group_id, int):
            raise TypeError(f"group_id must be an integer, got {type(self.group_id)}")
        if not isinstance(self.suppress_series_animations, bool):
            raise TypeError(
                f"suppress_series_animations must be a bool, "
                f"got {type(self.suppress_series_animations)}"
            )


@dataclass
class CrosshairOptions(Options):
    """Crosshair configuration for chart."""

    mode: CrosshairMode = CrosshairMode.NORMAL
    vert_line: CrosshairLineOptions = field(default_factory=CrosshairLineOptions)
    horz_line: CrosshairLineOptions = field(default_factory=CrosshairLineOptions)

    def __post_init__(self):
        super().__post_init__()
        if not isinstance(self.mode, CrosshairMode):
            raise TypeError(f"mode must be a CrosshairMode enum, got {type(self.mode)}")
        if not isinstance(self.vert_line, CrosshairLineOptions):
            raise TypeError(
                f"vert_line must be a CrosshairLineOptions instance, got {type(self.vert_line)}"
            )
        if not isinstance(self.horz_line, CrosshairLineOptions):
            raise TypeError(
                f"horz_line must be a CrosshairLineOptions instance, got {type(self.horz_line)}"
            )


@dataclass
class KineticScrollOptions(Options):
    """Kinetic scroll configuration for chart."""

    touch: bool = True
    mouse: bool = False

    def __post_init__(self):
        super().__post_init__()
        if not isinstance(self.touch, bool):
            raise TypeError(f"touch must be a bool, got {type(self.touch)}")
        if not isinstance(self.mouse, bool):
            raise TypeError(f"mouse must be a bool, got {type(self.mouse)}")


@dataclass
class TrackingModeOptions(Options):
    """Tracking mode configuration for chart."""

    exit_on_escape: bool = True

    def __post_init__(self):
        super().__post_init__()
        if not isinstance(self.exit_on_escape, bool):
            raise TypeError(f"exit_on_escape must be a bool, got {type(self.exit_on_escape)}")
