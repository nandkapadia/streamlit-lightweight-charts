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
from streamlit_lightweight_charts_pro.utils import chainable_field
from streamlit_lightweight_charts_pro.utils.data_utils import is_valid_color


@dataclass
@chainable_field("color", str, validator=lambda v: CrosshairLineOptions._validate_color_static(v, "color"))
@chainable_field("width", int)
@chainable_field("style", LineStyle)
@chainable_field("visible", bool)
@chainable_field("label_visible", bool)
class CrosshairLineOptions(Options):
    """Crosshair line configuration."""

    color: str = "#758696"
    width: int = 1
    style: LineStyle = LineStyle.SOLID
    visible: bool = True
    label_visible: bool = True

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
@chainable_field("group_id", int)
@chainable_field("suppress_series_animations", bool)
class CrosshairSyncOptions(Options):
    """Crosshair synchronization configuration."""

    group_id: int = 1
    suppress_series_animations: bool = True

    def __post_init__(self):
        super().__post_init__()


@dataclass
@chainable_field("mode", CrosshairMode)
@chainable_field("vert_line", CrosshairLineOptions)
@chainable_field("horz_line", CrosshairLineOptions)
class CrosshairOptions(Options):
    """Crosshair configuration for chart."""

    mode: CrosshairMode = CrosshairMode.NORMAL
    vert_line: CrosshairLineOptions = field(default_factory=CrosshairLineOptions)
    horz_line: CrosshairLineOptions = field(default_factory=CrosshairLineOptions)

    def __post_init__(self):
        super().__post_init__()


@dataclass
@chainable_field("touch", bool)
@chainable_field("mouse", bool)
class KineticScrollOptions(Options):
    """Kinetic scroll configuration for chart."""

    touch: bool = True
    mouse: bool = False

    def __post_init__(self):
        super().__post_init__()


@dataclass
@chainable_field("exit_on_escape", bool)
class TrackingModeOptions(Options):
    """Tracking mode configuration for chart."""

    exit_on_escape: bool = True

    def __post_init__(self):
        super().__post_init__()
