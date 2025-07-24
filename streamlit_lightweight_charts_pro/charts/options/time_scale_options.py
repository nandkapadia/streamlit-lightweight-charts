"""Scale option classes for streamlit-lightweight-charts."""

from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional


@dataclass
class TimeScaleOptions:
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

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        result = {
            "rightOffset": self.right_offset,
            "leftOffset": self.left_offset,
            "barSpacing": self.bar_spacing,
            "minBarSpacing": self.min_bar_spacing,
            "visible": self.visible,
            "timeVisible": self.time_visible,
            "secondsVisible": self.seconds_visible,
            "borderVisible": self.border_visible,
            "borderColor": self.border_color,
            "fixLeftEdge": self.fix_left_edge,
            "fixRightEdge": self.fix_right_edge,
            "lockVisibleTimeRangeOnResize": self.lock_visible_time_range_on_resize,
            "rightBarStaysOnScroll": self.right_bar_stays_on_scroll,
            "shiftVisibleRangeOnNewBar": self.shift_visible_range_on_new_bar,
            "allowShiftVisibleRangeOnWhitespaceAccess": (
                self.allow_shift_visible_range_on_whitespace_access
            ),
        }

        if self.tick_mark_formatter is not None:
            result["tickMarkFormatter"] = self.tick_mark_formatter

        return result

    def __getitem__(self, key):
        return self.to_dict()[key]
