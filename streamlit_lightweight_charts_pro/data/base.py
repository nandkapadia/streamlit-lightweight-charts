"""
Base data classes and utilities for streamlit-lightweight-charts.

This module provides the base data class and utility functions for time format conversion
used throughout the library for representing financial data points.
"""

import math
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional, Union

import pandas as pd

from streamlit_lightweight_charts_pro.logging_config import get_logger
from streamlit_lightweight_charts_pro.type_definitions import ColumnNames

# Initialize logger
logger = get_logger("data.base")


def to_utc_timestamp(
    time_value: Union[str, int, float, datetime, pd.Timestamp],
) -> Union[str, int]:
    """
    Convert various time formats to UTC timestamp or date string.

    This utility function normalizes different time input formats into
    a consistent format for internal use. It handles strings, timestamps,
    datetime objects, and pandas Timestamps.

    Args:
        time_value: Time value in various formats:
            - str: Date string (e.g., "2024-01-01")
            - int/float: Unix timestamp in seconds
            - datetime: Python datetime object
            - pd.Timestamp: Pandas Timestamp object

    Returns:
        Normalized time representation:
            - str: Date string if input was a valid date string
            - int: Unix timestamp in seconds for other formats

    Raises:
        ValueError: If the time format is not supported.

    Example:
        ```python
        # String date
        to_utc_timestamp("2024-01-01")  # Returns 1545436800

        # Unix timestamp
        to_utc_timestamp(1704067200)  # Returns 1704067200

        # Datetime object
        to_utc_timestamp(datetime(2024, 1, 1))  # Returns 1704067200
        ```
    """
    if isinstance(time_value, str):
        # Try to parse as date string and convert to timestamp
        try:
            # Parse the date string and convert to timestamp
            dt = pd.to_datetime(time_value)
            return int(dt.timestamp())
        except (ValueError, TypeError):
            # If not parseable, return as is
            return time_value
    elif isinstance(time_value, (int, float)):
        # Already a timestamp - convert to int for consistency
        return int(time_value)
    elif isinstance(time_value, datetime):
        # Convert datetime to UTC timestamp
        return int(time_value.timestamp())
    elif isinstance(time_value, pd.Timestamp):
        # Convert pandas Timestamp to UTC timestamp
        return int(time_value.timestamp())
    else:
        raise ValueError(f"Unsupported time type: {type(time_value)}")


def from_utc_timestamp(time_value: Optional[Union[str, int]]) -> pd.Timestamp:
    """
    Convert UTC timestamp or date string to pandas Timestamp.

    This utility function converts normalized time representations back
    to pandas Timestamp objects for consistent time handling.

    Args:
        time_value: Time value to convert:
            - str: Date string (e.g., "2024-01-01")
            - int: Unix timestamp in seconds
            - None: Not allowed

    Returns:
        Pandas Timestamp object representing the time.

    Raises:
        ValueError: If time_value is None or format is not supported.

    Example:
        ```python
        from_utc_timestamp("2024-01-01")  # Returns pd.Timestamp('2024-01-01')
        from_utc_timestamp(1704067200)    # Returns pd.Timestamp('2024-01-01 00:00:00')
        ```
    """
    if time_value is None:
        raise ValueError("time_value cannot be None")
    elif isinstance(time_value, str):
        return pd.to_datetime(time_value)
    elif isinstance(time_value, (int, float)):
        return pd.to_datetime(time_value, unit="s")
    else:
        raise ValueError(f"Unsupported time type: {type(time_value)}")


@dataclass
class BaseData:
    """
    Base class for all data points in charts.

    This abstract base class provides common functionality for all data point
    types, including time handling and dictionary conversion. It enforces
    that all data points must have a time component.

    Attributes:
        _time: Internal time representation (UTC timestamp or date string).
    """

    _time: Optional[Union[str, int]] = field(default=None, init=False, repr=False)

    def __post_init__(self):
        """
        Validate that time is provided after initialization.

        Raises:
            ValueError: If time is not set during initialization.
        """
        if self._time is None:
            raise ValueError("time must be provided")

    @property
    def time(self) -> pd.Timestamp:
        """
        Get time as pandas Timestamp.

        Returns:
            Pandas Timestamp object representing the data point time.
        """
        return from_utc_timestamp(self._time)

    @time.setter
    def time(self, value: Union[str, int, float, datetime, pd.Timestamp]) -> None:
        """
        Set time from various formats.

        Args:
            value: Time value in various formats:
                - str: Date string (e.g., "2024-01-01")
                - int/float: Unix timestamp in seconds
                - datetime: Python datetime object
                - pd.Timestamp: Pandas Timestamp object
        """
        self._time = to_utc_timestamp(value)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert data point to dictionary representation.

        This method creates a dictionary representation of the data point
        suitable for serialization or frontend consumption.

        Returns:
            Dictionary containing the data point's attributes, excluding
            private fields (those starting with '_').
        """
        result = {}
        # Add time as the first field
        result[ColumnNames.TIME] = self._time
        # Add all other non-private fields
        for key, value in self.__dict__.items():
            if not key.startswith("_") and value is not None:
                # Replace NaN or pd.NA with 0
                if (isinstance(value, float) and math.isnan(value)) or value is pd.NA:
                    result[key] = 0
                else:
                    result[key] = value
        return result
