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
@chainable_field("symbolName", str)
@chainable_field("fontSize", int)
@chainable_field("fontFamily", str)
@chainable_field("fontWeight", str)
@chainable_field("color", str)
@chainable_field("backgroundColor", str)
@chainable_field("borderColor", str)
@chainable_field("borderWidth", int)
@chainable_field("borderRadius", int)
@chainable_field("padding", int)
@chainable_field("margin", int)
@chainable_field("zIndex", int)
@chainable_field("showLastValue", bool)
@chainable_field("showTime", bool)
@chainable_field("showSymbol", bool)
@chainable_field("priceFormat", str)
@chainable_field("customTemplate", str)
class LegendOptions(Options):
    """Legend configuration."""

    visible: bool = True
    type: str = "simple"
    position: str = "top-right"
    symbolName: str = ""
    fontSize: int = 12
    fontFamily: str = "Arial, sans-serif"
    fontWeight: str = "normal"
    color: str = "#131722"
    backgroundColor: str = "rgba(255, 255, 255, 0.9)"
    borderColor: str = "#e1e3e6"
    borderWidth: int = 1
    borderRadius: int = 4
    padding: int = 8
    margin: int = 4
    zIndex: int = 1000
    showLastValue: bool = False
    showTime: bool = False
    showSymbol: bool = True
    priceFormat: str = ""
    customTemplate: str = ""
