"""
Trade visualization options for streamlit-lightweight-charts.

This module provides the TradeVisualizationOptions class for configuring
how trades are visualized on charts, including markers, rectangles, lines,
arrows, and zones.
"""

from dataclasses import dataclass

from streamlit_lightweight_charts_pro.charts.options.base_options import Options
from streamlit_lightweight_charts_pro.type_definitions.enums import TradeVisualization
from streamlit_lightweight_charts_pro.utils import chainable_field
from streamlit_lightweight_charts_pro.utils.data_utils import is_valid_color


@dataclass
@chainable_field("style", TradeVisualization)
@chainable_field(
    "entry_marker_color_long",
    str,
    validator=lambda v: TradeVisualizationOptions._validate_color_static(
        v, "entry_marker_color_long"
    ),
)
@chainable_field(
    "entry_marker_color_short",
    str,
    validator=lambda v: TradeVisualizationOptions._validate_color_static(
        v, "entry_marker_color_short"
    ),
)
@chainable_field(
    "exit_marker_color_profit",
    str,
    validator=lambda v: TradeVisualizationOptions._validate_color_static(
        v, "exit_marker_color_profit"
    ),
)
@chainable_field(
    "exit_marker_color_loss",
    str,
    validator=lambda v: TradeVisualizationOptions._validate_color_static(
        v, "exit_marker_color_loss"
    ),
)
@chainable_field("marker_size", int)
@chainable_field("show_pnl_in_markers", bool)
@chainable_field("rectangle_fill_opacity", float)
@chainable_field("rectangle_border_width", int)
@chainable_field(
    "rectangle_color_profit",
    str,
    validator=lambda v: TradeVisualizationOptions._validate_color_static(
        v, "rectangle_color_profit"
    ),
)
@chainable_field(
    "rectangle_color_loss",
    str,
    validator=lambda v: TradeVisualizationOptions._validate_color_static(v, "rectangle_color_loss"),
)
@chainable_field(
    "rectangle_fill_color_profit",
    str,
    validator=lambda v: TradeVisualizationOptions._validate_color_static(
        v, "rectangle_fill_color_profit"
    ),
)
@chainable_field(
    "rectangle_border_color_profit",
    str,
    validator=lambda v: TradeVisualizationOptions._validate_color_static(
        v, "rectangle_border_color_profit"
    ),
)
@chainable_field(
    "rectangle_border_color_loss",
    str,
    validator=lambda v: TradeVisualizationOptions._validate_color_static(
        v, "rectangle_border_color_loss"
    ),
)
@chainable_field("line_width", int)
@chainable_field("line_style", str)
@chainable_field(
    "line_color_profit",
    str,
    validator=lambda v: TradeVisualizationOptions._validate_color_static(v, "line_color_profit"),
)
@chainable_field(
    "line_color_loss",
    str,
    validator=lambda v: TradeVisualizationOptions._validate_color_static(v, "line_color_loss"),
)
@chainable_field("arrow_size", int)
@chainable_field(
    "arrow_color_profit",
    str,
    validator=lambda v: TradeVisualizationOptions._validate_color_static(v, "arrow_color_profit"),
)
@chainable_field(
    "arrow_color_loss",
    str,
    validator=lambda v: TradeVisualizationOptions._validate_color_static(v, "arrow_color_loss"),
)
@chainable_field("zone_opacity", float)
@chainable_field(
    "zone_color_long",
    str,
    validator=lambda v: TradeVisualizationOptions._validate_color_static(v, "zone_color_long"),
)
@chainable_field(
    "zone_color_short",
    str,
    validator=lambda v: TradeVisualizationOptions._validate_color_static(v, "zone_color_short"),
)
@chainable_field("zone_extend_bars", int)
@chainable_field("show_trade_id", bool)
@chainable_field("show_quantity", bool)
@chainable_field("show_trade_type", bool)
@chainable_field("annotation_font_size", int)
@chainable_field(
    "annotation_background",
    str,
    validator=lambda v: TradeVisualizationOptions._validate_color_static(
        v, "annotation_background"
    ),
)
class TradeVisualizationOptions(Options):
    """
    Options for trade visualization.

    This class provides comprehensive configuration options for how trades
    are displayed on charts, including various visual styles and customization
    options for markers, rectangles, lines, arrows, and zones.

    Attributes:
        style: The visualization style to use (markers, rectangles, both, etc.)
        entry_marker_color_long: Color for long entry markers
        entry_marker_color_short: Color for short entry markers
        exit_marker_color_profit: Color for profitable exit markers
        exit_marker_color_loss: Color for loss exit markers
        marker_size: Size of markers in pixels
        show_pnl_in_markers: Whether to show P&L in marker text
        rectangle_fill_opacity: Opacity for rectangle fill (0.0 to 1.0)
        rectangle_border_width: Width of rectangle borders
        rectangle_color_profit: Color for profitable trade rectangles
        rectangle_color_loss: Color for loss trade rectangles
        rectangle_fill_color_profit: Fill color for profitable trade rectangles
        rectangle_border_color_profit: Border color for profitable trade rectangles
        rectangle_border_color_loss: Border color for loss trade rectangles
        line_width: Width of connecting lines
        line_style: Style of connecting lines (solid, dashed, etc.)
        line_color_profit: Color for profitable trade lines
        line_color_loss: Color for loss trade lines
        arrow_size: Size of arrows in pixels
        arrow_color_profit: Color for profitable trade arrows
        arrow_color_loss: Color for loss trade arrows
        zone_opacity: Opacity for zone fills (0.0 to 1.0)
        zone_color_long: Color for long trade zones
        zone_color_short: Color for short trade zones
        zone_extend_bars: Number of bars to extend zones
        show_trade_id: Whether to show trade ID in annotations
        show_quantity: Whether to show quantity in annotations
        show_trade_type: Whether to show trade type in annotations
        annotation_font_size: Font size for annotations
        annotation_background: Background color for annotations
    """

    style: TradeVisualization = TradeVisualization.BOTH

    # Marker options
    entry_marker_color_long: str = "#2196F3"
    entry_marker_color_short: str = "#FF9800"
    exit_marker_color_profit: str = "#4CAF50"
    exit_marker_color_loss: str = "#F44336"
    marker_size: int = 20
    show_pnl_in_markers: bool = True

    # Rectangle options
    rectangle_fill_opacity: float = 0.2
    rectangle_border_width: int = 1
    rectangle_color_profit: str = "#4CAF50"
    rectangle_color_loss: str = "#F44336"
    rectangle_fill_color_profit: str = "#4CAF50"
    rectangle_border_color_profit: str = "#4CAF50"
    rectangle_border_color_loss: str = "#F44336"

    # Line options
    line_width: int = 2
    line_style: str = "dashed"
    line_color_profit: str = "#4CAF50"
    line_color_loss: str = "#F44336"

    # Arrow options
    arrow_size: int = 10
    arrow_color_profit: str = "#4CAF50"
    arrow_color_loss: str = "#F44336"

    # Zone options
    zone_opacity: float = 0.1
    zone_color_long: str = "#2196F3"
    zone_color_short: str = "#FF9800"
    zone_extend_bars: int = 2  # Extend zone by this many bars

    # Annotation options
    show_trade_id: bool = True
    show_quantity: bool = True
    show_trade_type: bool = True
    annotation_font_size: int = 12
    annotation_background: str = "rgba(255, 255, 255, 0.8)"

    def __post_init__(self):
        """Post-initialization processing."""
        # Convert style to enum if it's a string
        if isinstance(self.style, str):
            self.style = TradeVisualization(self.style.lower())

    @staticmethod
    def _validate_color_static(color: str, property_name: str) -> str:
        """Static version of color validator for decorator use."""
        if not is_valid_color(color):
            raise ValueError(
                f"Invalid color format for {property_name}: {color!r}. Must be hex or rgba."
            )
        return color
