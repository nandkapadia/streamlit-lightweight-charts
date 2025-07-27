"""UI option classes for streamlit-lightweight-charts."""

from dataclasses import dataclass, field
from typing import List

from streamlit_lightweight_charts_pro.charts.options.base_options import Options


@dataclass
class RangeConfig(Options):
    """Range configuration for range switcher."""

    text: str = ""
    tooltip: str = ""

    def __post_init__(self):
        super().__post_init__()
        # Handle None values gracefully
        if self.text is None:
            self.text = ""
        elif not isinstance(self.text, str):
            raise TypeError(f"text must be a string, got {type(self.text)}")

        if self.tooltip is None:
            self.tooltip = ""
        elif not isinstance(self.tooltip, str):
            raise TypeError(f"tooltip must be a string, got {type(self.tooltip)}")


@dataclass
class RangeSwitcherOptions(Options):
    """Range switcher configuration."""

    visible: bool = True
    ranges: List[RangeConfig] = field(default_factory=list)

    def __post_init__(self):
        super().__post_init__()
        if not isinstance(self.visible, bool):
            raise TypeError(f"visible must be a boolean, got {type(self.visible)}")

        # Handle None ranges gracefully
        if self.ranges is None:
            self.ranges = []
        elif not isinstance(self.ranges, list):
            raise TypeError(f"ranges must be a list, got {type(self.ranges)}")

        for i, range_config in enumerate(self.ranges):
            if not isinstance(range_config, RangeConfig):
                raise TypeError(
                    f"ranges[{i}] must be a RangeConfig instance, got {type(range_config)}"
                )


@dataclass
class LegendOptions(Options):
    """Legend configuration."""

    visible: bool = True
    position: str = "top"

    def __post_init__(self):
        super().__post_init__()
        if not isinstance(self.visible, bool):
            raise TypeError(f"visible must be a boolean, got {type(self.visible)}")
        if not isinstance(self.position, str):
            raise TypeError(f"position must be a string, got {type(self.position)}")
