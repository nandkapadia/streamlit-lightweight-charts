"""Scale option classes for streamlit-lightweight-charts."""

from dataclasses import dataclass
from typing import Callable, Optional

from streamlit_lightweight_charts_pro.charts.options.base_options import Options


@dataclass
class TimeScaleOptions(Options):
    """Time scale configuration."""

    right_offset: int = 0
    left_offset: int = 0
    bar_spacing: int = 6
    min_bar_spacing: float = 0.001
    visible: bool = True
    time_visible: bool = True
    seconds_visible: bool = False
    border_visible: bool = True
    border_color: str = "rgba(197, 203, 206, 0.8)"
    fix_left_edge: bool = False
    fix_right_edge: bool = False
    lock_visible_time_range_on_resize: bool = False
    right_bar_stays_on_scroll: bool = False
    shift_visible_range_on_new_bar: bool = False
    allow_shift_visible_range_on_whitespace_access: bool = False
    tick_mark_formatter: Optional[Callable] = None

    def __getitem__(self, key):
        return self.to_dict()[key]
