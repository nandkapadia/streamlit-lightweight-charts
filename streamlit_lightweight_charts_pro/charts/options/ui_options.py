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
@chainable_field("type", str)
@chainable_field("position", str)
@chainable_field("symbol_name", str)
@chainable_field("font_size", int)
@chainable_field("font_family", str)
@chainable_field("font_weight", str)
@chainable_field("color", str)
@chainable_field("background_color", str)
@chainable_field("border_color", str)
@chainable_field("border_width", int)
@chainable_field("border_radius", int)
@chainable_field("padding", int)
@chainable_field("margin", int)
@chainable_field("z_index", int)
@chainable_field("show_last_value", bool)
@chainable_field("show_time", bool)
@chainable_field("show_symbol", bool)
@chainable_field("price_format", str)
@chainable_field("custom_template", str)
class LegendOptions(Options):
    """Legend configuration."""

    visible: bool = True
    type: str = "simple"
    position: str = "top-right"
    symbol_name: str = ""
    font_size: int = 12
    font_family: str = "Arial, sans-serif"
    font_weight: str = "normal"
    color: str = "#131722"
    background_color: str = "rgba(255, 255, 255, 0.9)"
    border_color: str = "#e1e3e6"
    border_width: int = 1
    border_radius: int = 4
    padding: int = 8
    margin: int = 4
    z_index: int = 1000
    show_last_value: bool = False
    show_time: bool = False
    show_symbol: bool = True
    price_format: str = ""
    custom_template: str = ""
