"""
Data utilities for streamlit-lightweight-charts.

This module provides utility functions for data processing and manipulation
used throughout the library.
"""

import re
from datetime import datetime
from typing import Any

import pandas as pd


def normalize_time(time_value: Any) -> int:
    """
    Convert time input to int UNIX seconds.

    Args:
        time_value: Supported types are int, float, str, datetime, pd.Timestamp, numpy types

    Returns:
        int: UNIX timestamp in seconds

    Raises:
        ValueError: If the input cannot be converted to a UNIX timestamp
        TypeError: If the input type is not supported
    """
    # Handle numpy types by converting to Python native types
    if hasattr(time_value, "item"):
        time_value = time_value.item()
    elif hasattr(time_value, "dtype"):
        # Handle numpy arrays and other numpy objects
        try:
            time_value = time_value.item()
        except (ValueError, TypeError):
            # If item() fails, try to convert to int/float
            time_value = int(time_value) if hasattr(time_value, "__int__") else float(time_value)

    if isinstance(time_value, int):
        return time_value
    if isinstance(time_value, float):
        return int(time_value)
    if isinstance(time_value, str):
        # Try to parse and normalize the string
        try:
            dt = pd.to_datetime(time_value)
            return int(dt.timestamp())
        except (ValueError, TypeError) as exc:
            raise ValueError(f"Invalid time string: {time_value!r}") from exc
    if isinstance(time_value, datetime):
        return int(time_value.timestamp())
    if isinstance(time_value, pd.Timestamp):
        return int(time_value.timestamp())
    raise TypeError(f"Unsupported time type: {type(time_value)}")


def to_utc_timestamp(time_value: Any) -> int:
    """
    Convert time input to int UNIX seconds.

    This is an alias for normalize_time for backward compatibility.

    Args:
        time_value: Supported types are int, float, str, datetime, pd.Timestamp

    Returns:
        int: UNIX timestamp in seconds
    """
    return normalize_time(time_value)


def from_utc_timestamp(timestamp: int) -> str:
    """
    Convert UNIX timestamp to ISO format string.

    Args:
        timestamp: UNIX timestamp in seconds

    Returns:
        str: ISO format datetime string
    """
    return datetime.utcfromtimestamp(timestamp).isoformat()


def snake_to_camel(snake_str: str) -> str:
    """
    Convert snake_case string to camelCase.

    Args:
        snake_str: String in snake_case format

    Returns:
        str: String in camelCase format

    Example:
        ```python
        snake_to_camel("price_scale_id")  # "priceScaleId"
        snake_to_camel("line_color")  # "lineColor"
        ```
    """
    components = snake_str.split("_")
    return components[0] + "".join(word.capitalize() for word in components[1:])


def is_valid_color(color: str) -> bool:
    """
    Check if a color string is valid.

    Args:
        color: Color string to validate

    Returns:
        bool: True if color is valid, False otherwise

    Example:
        ```python
        is_valid_color("#FF0000")  # True
        is_valid_color("rgb(255, 0, 0)")  # True
        is_valid_color("red")  # True
        is_valid_color("invalid")  # False
        ```
    """
    if not isinstance(color, str):
        return False

    # Check for hex colors
    if color.startswith("#") and len(color) in [4, 7, 9]:
        return True

    # Check for RGB/RGBA colors - allow negative numbers for alpha
    rgb_pattern = r"^rgb\(\s*-?\d+\s*,\s*-?\d+\s*,\s*-?\d+\s*\)$"
    rgba_pattern = r"^rgba?\(\s*-?\d+\s*,\s*-?\d+\s*,\s*-?\d+\s*(?:,\s*-?[\d.]+\s*)?\)$"

    if re.match(rgb_pattern, color) or re.match(rgba_pattern, color):
        return True

    # Check for named colors
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
