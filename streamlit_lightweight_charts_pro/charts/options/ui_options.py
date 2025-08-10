"""UI option classes for streamlit-lightweight-charts."""

from dataclasses import dataclass, field
from typing import List

from streamlit_lightweight_charts_pro.charts.options.base_options import Options
from streamlit_lightweight_charts_pro.utils import chainable_field


@dataclass
@chainable_field("text", str)
@chainable_field("tooltip", str)
class RangeConfig(Options):
    """Range configuration for range switcher."""

    text: str = ""
    tooltip: str = ""


@dataclass
@chainable_field("visible", bool)
@chainable_field("ranges", list)
class RangeSwitcherOptions(Options):
    """Range switcher configuration."""

    visible: bool = True
    ranges: List[RangeConfig] = field(default_factory=list)


@dataclass
@chainable_field("visible", bool)
@chainable_field("position", str)
@chainable_field("symbol_name", str)
@chainable_field("background_color", str)
@chainable_field("border_color", str)
@chainable_field("border_width", int)
@chainable_field("border_radius", int)
@chainable_field("padding", int)
@chainable_field("margin", int)
@chainable_field("z_index", int)
@chainable_field("price_format", str)
@chainable_field("text", str)
class LegendOptions(Options):
    """
    Legend configuration with support for custom HTML templates.

    The text supports placeholders that will be replaced by the frontend:
    - {title}: Series title/name
    - {value}: Current value of the series
    - {time}: Current time
    - {color}: Series color
    - {type}: Series type (Line, Candlestick, etc.)
    - Any other field from the series data can be accessed as {field_name}

    Example templates:
    - "<span style='color: {color}'>{title}: {value}</span>"
    - "<div><strong>{title}</strong><br/>Price: ${value}</div>"
    - "<span class='legend-item'>{title} - {value} ({type})</span>"
    """

    visible: bool = True
    position: str = "top-right"
    symbol_name: str = ""
    background_color: str = "rgba(255, 255, 255, 0.9)"
    border_color: str = "#e1e3e6"
    border_width: int = 1
    border_radius: int = 4
    padding: int = 5  # Changed from 8 to 5 as requested
    margin: int = 4
    z_index: int = 1000
    price_format: str = ""
    text: str = ""
