from dataclasses import dataclass
from typing import Optional

from streamlit_lightweight_charts_pro.charts.options.base_options import Options
from streamlit_lightweight_charts_pro.type_definitions.enums import LineStyle
from streamlit_lightweight_charts_pro.utils.data_utils import is_valid_color


@dataclass
class PriceLineOptions(Options):
    """
    Encapsulates style and configuration options for a price line,
    matching TradingView's PriceLineOptions.

    See: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/PriceLineOptions

    Attributes:
        id (Optional[str]): Optional ID of the price line.
        price (float): Price line's value.
        color (str): Price line's color (hex or rgba).
        line_width (int): Price line's width in pixels.
        line_style (LineStyle): Price line's style.
        line_visible (bool): Whether the line is displayed.
        axis_label_visible (bool): Whether the price value is shown on the price scale.
        title (str): Title for the price line on the chart pane.
        axis_label_color (Optional[str]): Background color for the axis label.
        axis_label_text_color (Optional[str]): Text color for the axis label.
    """

    id: Optional[str] = None
    price: float = 0.0
    color: str = ""
    line_width: int = 1
    line_style: LineStyle = LineStyle.SOLID
    line_visible: bool = True
    axis_label_visible: bool = True
    title: str = ""
    axis_label_color: Optional[str] = None
    axis_label_text_color: Optional[str] = None

    def __post_init__(self):
        """Post-initialization validation."""
        super().__post_init__()

        if not isinstance(self.price, (int, float)):
            raise ValueError(f"price must be a number, got {type(self.price)}")
        if not isinstance(self.line_width, int) or self.line_width < 1:
            raise ValueError(f"line_width must be a positive integer, got {self.line_width}")
        if self.color and not is_valid_color(self.color):
            raise ValueError(f"Invalid color format: {self.color!r}. Must be hex or rgba.")
        if self.axis_label_color and not is_valid_color(self.axis_label_color):
            raise ValueError(
                f"Invalid axis_label_color: {self.axis_label_color!r}. Must be hex or rgba."
            )
        if self.axis_label_text_color and not is_valid_color(self.axis_label_text_color):
            raise ValueError(
                f"Invalid axis_label_text_color: {self.axis_label_text_color!r}. "
                f"Must be hex or rgba."
            )
