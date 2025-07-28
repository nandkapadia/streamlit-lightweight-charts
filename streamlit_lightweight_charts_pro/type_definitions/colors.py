"""
Color-related classes for streamlit-lightweight-charts.

This module provides Background classes for chart backgrounds with proper validation.
"""

import re
from abc import ABC
from dataclasses import dataclass
from typing import Union

from streamlit_lightweight_charts_pro.charts.options.base_options import Options
from streamlit_lightweight_charts_pro.type_definitions.enums import BackgroundStyle


def _is_valid_color(color: str) -> bool:
    """
    Validate if a color string is in a valid format.

    Args:
        color: Color string to validate

    Returns:
        True if valid, False otherwise
    """
    if not color or not isinstance(color, str):
        return False

    # Hex color pattern
    hex_pattern = r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
    if re.match(hex_pattern, color):
        return True

    # RGB/RGBA pattern - allow negative numbers for alpha
    rgba_pattern = r"^rgba?\(\s*-?\d+\s*,\s*-?\d+\s*,\s*-?\d+\s*(?:,\s*-?[\d.]+\s*)?\)$"
    if re.match(rgba_pattern, color):
        return True

    # Named colors (basic support)
    named_colors = {
        "black",
        "white",
        "red",
        "green",
        "blue",
        "yellow",
        "cyan",
        "magenta",
        "gray",
        "grey",
        "orange",
        "purple",
        "brown",
        "pink",
        "lime",
        "navy",
        "teal",
        "silver",
        "gold",
        "maroon",
        "olive",
        "aqua",
        "fuchsia",
    }
    if color.lower() in named_colors:
        return True

    return False


@dataclass
class BackgroundSolid(Options, ABC):
    """
    Solid background color configuration.

    Attributes:
        color: The color string in any valid CSS format.
        style: The background style (always SOLID for this class).
    """

    color: str = "#ffffff"
    style: BackgroundStyle = BackgroundStyle.SOLID

    def __post_init__(self):
        """Post-initialization validation."""
        super().__post_init__()
        if not _is_valid_color(self.color):
            raise ValueError(
                f"Invalid color format: {self.color!r}. Must be hex, rgba, or named color."
            )


@dataclass
class BackgroundGradient(Options, ABC):
    """
    Gradient background configuration.

    Attributes:
        top_color: The top color string in any valid CSS format.
        bottom_color: The bottom color string in any valid CSS format.
        style: The background style (always VERTICAL_GRADIENT for this class).
    """

    top_color: str = "#ffffff"
    bottom_color: str = "#000000"
    style: BackgroundStyle = BackgroundStyle.VERTICAL_GRADIENT

    def __post_init__(self):
        """Post-initialization validation."""
        super().__post_init__()
        if not _is_valid_color(self.top_color):
            raise ValueError(
                f"Invalid top_color format: {self.top_color!r}. Must be hex, rgba, or named color."
            )
        if not _is_valid_color(self.bottom_color):
            raise ValueError(
                f"Invalid bottom_color format: {self.bottom_color!r}. "
                f"Must be hex, rgba, or named color."
            )


Background = Union[BackgroundSolid, BackgroundGradient]
