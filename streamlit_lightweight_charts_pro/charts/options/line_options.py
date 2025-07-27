from dataclasses import dataclass
from typing import Optional

from streamlit_lightweight_charts_pro.charts.options.base_options import Options
from streamlit_lightweight_charts_pro.type_definitions.enums import (
    LastPriceAnimationMode,
    LineStyle,
    LineType,
)
from streamlit_lightweight_charts_pro.utils.data_utils import is_valid_color


@dataclass
class LineOptions(Options):
    """
    Encapsulates style options for a line series, mirroring TradingView's LineStyleOptions.

    See: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/LineStyleOptions

    Attributes:
        color (str): Line color. Default: '#2196f3'.
        line_style (LineStyle): Line style. Default: LineStyle.SOLID.
        line_width (int): Line width in pixels. Default: 3.
        line_type (LineType): Line type. Default: LineType.SIMPLE.
        line_visible (bool): Show series line. Default: True.
        point_markers_visible (bool): Show circle markers on each point. Default: False.
        point_markers_radius (Optional[int]): Circle markers radius in pixels. Default: None.
        crosshair_marker_visible (bool): Show the crosshair marker. Default: True.
        crosshair_marker_radius (int): Crosshair marker radius in pixels. Default: 4.
        crosshair_marker_border_color (str): Crosshair marker border color. Default: ''.
        crosshair_marker_background_color (str): Crosshair marker background color. Default: ''.
        crosshair_marker_border_width (int): Crosshair marker border width in pixels. Default: 2.
        last_price_animation (LastPriceAnimationMode): Last price animation mode. 
            Default: LastPriceAnimationMode.DISABLED.
    """

    color: str = "#2196f3"
    line_style: LineStyle = LineStyle.SOLID
    line_width: int = 3
    line_type: LineType = LineType.SIMPLE
    line_visible: bool = True
    point_markers_visible: bool = False
    point_markers_radius: Optional[int] = None
    crosshair_marker_visible: bool = True
    crosshair_marker_radius: int = 4
    crosshair_marker_border_color: str = ""
    crosshair_marker_background_color: str = ""
    crosshair_marker_border_width: int = 2
    last_price_animation: LastPriceAnimationMode = LastPriceAnimationMode.DISABLED

    def __post_init__(self):
        """Post-initialization validation."""
        super().__post_init__()

        if not is_valid_color(self.color):
            raise ValueError(f"Invalid color format: {self.color!r}. Must be hex or rgba.")
        if self.crosshair_marker_border_color and not is_valid_color(
            self.crosshair_marker_border_color
        ):
            raise ValueError(
                f"Invalid crosshair_marker_border_color: {self.crosshair_marker_border_color!r}."
            )
        if self.crosshair_marker_background_color and not is_valid_color(
            self.crosshair_marker_background_color
        ):
            raise ValueError(
                f"Invalid crosshair_marker_background_color: "
                f"{self.crosshair_marker_background_color!r}."
            )
        if not isinstance(self.line_width, int) or self.line_width < 1:
            raise ValueError(f"line_width must be a positive integer, got {self.line_width}")
        if self.point_markers_radius is not None and (
            not isinstance(self.point_markers_radius, int) or self.point_markers_radius < 1
        ):
            raise ValueError(
                f"point_markers_radius must be a positive integer or None, "
                f"got {self.point_markers_radius}"
            )
        if not isinstance(self.crosshair_marker_radius, int) or self.crosshair_marker_radius < 1:
            raise ValueError(
                f"crosshair_marker_radius must be a positive integer, "
                f"got {self.crosshair_marker_radius}"
            )
        if (
            not isinstance(self.crosshair_marker_border_width, int)
            or self.crosshair_marker_border_width < 1
        ):
            raise ValueError(
                f"crosshair_marker_border_width must be a positive integer, "
                f"got {self.crosshair_marker_border_width}"
            )
