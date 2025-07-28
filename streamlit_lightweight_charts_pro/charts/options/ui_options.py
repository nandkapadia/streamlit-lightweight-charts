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

    def __post_init__(self):
        super().__post_init__()


@dataclass
@chainable_field("visible", bool)
@chainable_field("ranges", list)
class RangeSwitcherOptions(Options):
    """Range switcher configuration."""

    visible: bool = True
    ranges: List[RangeConfig] = field(default_factory=list)

    def __post_init__(self):
        super().__post_init__()


@dataclass
@chainable_field("visible", bool)
@chainable_field("position", str)
class LegendOptions(Options):
    """Legend configuration."""

    visible: bool = True
    position: str = "top"

    def __post_init__(self):
        super().__post_init__()
