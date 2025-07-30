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
        is_valid_color("rgba(255, 0, 0, 1)")  # True
        is_valid_color("")  # True (no color)
        is_valid_color("invalid")  # False
        ```
    """
    if not isinstance(color, str):
        return False

    # Accept empty strings as valid (meaning "no color")
    if color == "":
        return True

    # Check for hex colors (#RRGGBB, #RGB, #RRGGBBAA)
    if color.startswith("#"):
        hex_pattern = r"^#[0-9A-Fa-f]{3}(?:[0-9A-Fa-f]{1,5})?$"
        return bool(re.match(hex_pattern, color))

    # Check for rgba colors only (not rgb)
    rgba_pattern = r"^rgba\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*[\d.]+\s*\)$"
    return bool(re.match(rgba_pattern, color))


def validate_price_format_type(type_value: str) -> str:
    """
    Validate price format type.

    Args:
        type_value: Type string to validate

    Returns:
        str: Validated type string

    Raises:
        ValueError: If type is not valid

    Example:
        ```python
        validate_price_format_type("price")  # "price"
        validate_price_format_type("volume")  # "volume"
        validate_price_format_type("invalid")  # ValueError
        ```
    """
    valid_types = {"price", "volume", "percent", "custom"}
    if type_value not in valid_types:
        raise ValueError(
            f"Invalid type: {type_value!r}. Must be one of 'price', 'volume', 'percent', 'custom'."
        )
    return type_value


def validate_precision(precision: int) -> int:
    """
    Validate precision value.

    Args:
        precision: Precision value to validate

    Returns:
        int: Validated precision value

    Raises:
        ValueError: If precision is not valid

    Example:
        ```python
        validate_precision(5)  # 5
        validate_precision(-1)  # ValueError
        ```
    """
    if not isinstance(precision, int) or precision < 0:
        raise ValueError(f"precision must be a non-negative integer, got {precision}")
    return precision


def validate_min_move(min_move: float) -> float:
    """
    Validate minimum move value.

    Args:
        min_move: Minimum move value to validate

    Returns:
        float: Validated minimum move value

    Raises:
        ValueError: If min_move is not valid

    Example:
        ```python
        validate_min_move(0.001)  # 0.001
        validate_min_move(0)  # ValueError
        ```
    """
    if not isinstance(min_move, (int, float)) or min_move <= 0:
        raise ValueError(f"min_move must be a positive number, got {min_move}")
    return float(min_move)
