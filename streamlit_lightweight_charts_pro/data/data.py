"""
Data classes and utilities for streamlit-lightweight-charts.

This module provides the base data class and utility functions for time format conversion
used throughout the library for representing financial data points. The Data class serves
as the foundation for all chart data structures, providing standardized serialization
and time normalization capabilities.
"""

import math
from abc import ABC
from dataclasses import dataclass, fields
from enum import Enum
from typing import Dict

from streamlit_lightweight_charts_pro.logging_config import get_logger
from streamlit_lightweight_charts_pro.type_definitions.enums import ColumnNames
from streamlit_lightweight_charts_pro.utils.data_utils import normalize_time, snake_to_camel

logger = get_logger(__name__)


# The following disables are for custom class property pattern, which pylint does not recognize.
# pylint: disable=no-self-argument, no-member, invalid-name
# Note: 'classproperty' intentionally uses snake_case for compatibility with Python conventions.


class classproperty(property):
    """
    Descriptor to create class-level properties.
    
    This pattern is correct, but pylint may not recognize it and will warn about missing 'self'.
    """

    def __get__(self, obj, cls):
        """Get the class property value."""
        return self.fget(cls)


@dataclass
class Data(ABC):
    """
    Abstract base class for chart data points.

    All chart data classes should inherit from Data. Handles time normalization and
    serialization to camelCase dict for frontend communication. Provides standardized
    column management for DataFrame conversion operations.

    Attributes:
        time (int): UNIX timestamp in seconds representing the data point time.

    See also:
        LineData: Single value data points for line charts.
        OhlcData: OHLC data points for candlestick charts.
        OhlcvData: OHLCV data points with volume information.

    Note:
        - All imports must be at the top of the file unless justified.
        - Use specific exceptions and lazy string formatting for logging.
        - Time values are automatically normalized to seconds.
        - NaN values are converted to 0.0 for frontend compatibility.
    """

    REQUIRED_COLUMNS = {"time"}  # Required columns for DataFrame conversion
    OPTIONAL_COLUMNS = set()  # Optional columns for DataFrame conversion

    time: int

    @classproperty
    def required_columns(cls):  # pylint: disable=no-self-argument
        """
        Return the union of all REQUIRED_COLUMNS from the class and its parents.

        This method traverses the class hierarchy to collect all required columns
        defined in REQUIRED_COLUMNS class attributes.

        Returns:
            set: All required columns from the class hierarchy.
        """
        required = set()
        for base in cls.__mro__:  # pylint: disable=no-member
            if hasattr(base, "REQUIRED_COLUMNS"):
                required |= getattr(base, "REQUIRED_COLUMNS")
        return required

    @classproperty
    def optional_columns(cls):  # pylint: disable=no-self-argument
        """
        Return the union of all OPTIONAL_COLUMNS from the class and its parents.

        This method traverses the class hierarchy to collect all optional columns
        defined in OPTIONAL_COLUMNS class attributes.

        Returns:
            set: All optional columns from the class hierarchy.
        """
        optional = set()
        for base in cls.__mro__:  # pylint: disable=no-member
            if hasattr(base, "OPTIONAL_COLUMNS"):
                optional |= getattr(base, "OPTIONAL_COLUMNS")
        return optional

    def __post_init__(self):
        """Post-initialization processing to normalize time values."""
        # Normalize time to ensure consistent format
        self.time = normalize_time(self.time)

    def to_dict(self) -> Dict[str, object]:
        """
        Serialize the data class to a dict with camelCase keys for frontend.

        Converts the data point to a dictionary format suitable for frontend
        communication. Handles time normalization, NaN conversion, NumPy type
        conversion, and enum value extraction.

        Returns:
            Dict[str, object]: Serialized data with camelCase keys ready for
                frontend consumption.

        Note:
            - NaN values are converted to 0.0
            - NumPy scalar types are converted to Python native types
            - Enum values are extracted using their .value property
            - Time column uses standardized ColumnNames.TIME.value
        """
        result = {}
        for f in fields(self):
            name = f.name
            value = getattr(self, name)
            # Skip None values and empty strings
            if value is None or value == "":
                continue
            # Handle NaN for floats
            if isinstance(value, float) and math.isnan(value):
                value = 0.0
            # Convert NumPy types to Python native types for JSON serialization
            if hasattr(value, "item"):  # NumPy scalar types
                value = value.item()
            # Convert enums to their values
            if isinstance(value, Enum):
                value = value.value
            # Use enum value for known columns
            if name == "time":
                key = ColumnNames.TIME.value
            elif name == "value":
                key = ColumnNames.VALUE.value
            else:
                key = snake_to_camel(name)
            result[key] = value
        return result
