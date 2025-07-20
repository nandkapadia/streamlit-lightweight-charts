"""
Data model classes for streamlit-lightweight-charts.

This module provides the core data models used throughout the library for
representing financial data points, markers, and other chart elements. It includes
base classes for different data types (OHLC, single value, histogram, etc.) and
utility functions for time format conversion.

The data models are designed to be flexible and support various input formats
while maintaining consistency in the internal representation.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional, Union

import pandas as pd


class MarkerShape(str, Enum):
    """
    Marker shape enumeration for chart markers.

    Defines the available shapes for chart markers that can be displayed
    on charts to highlight specific data points or events.

    Attributes:
        CIRCLE: Circular marker shape.
        SQUARE: Square marker shape.
        ARROW_UP: Upward-pointing arrow marker.
        ARROW_DOWN: Downward-pointing arrow marker.
    """

    CIRCLE = "circle"
    SQUARE = "square"
    ARROW_UP = "arrowUp"
    ARROW_DOWN = "arrowDown"


class MarkerPosition(str, Enum):
    """
    Marker position enumeration for chart markers.

    Defines where markers should be positioned relative to the data bars
    or points on the chart.

    Attributes:
        ABOVE_BAR: Position marker above the data bar/point.
        BELOW_BAR: Position marker below the data bar/point.
        IN_BAR: Position marker inside the data bar/point.
    """

    ABOVE_BAR = "aboveBar"
    BELOW_BAR = "belowBar"
    IN_BAR = "inBar"


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
        result["time"] = self._time
        # Add all other non-private fields
        for key, value in self.__dict__.items():
            if not key.startswith("_") and value is not None:
                result[key] = value
        return result


@dataclass
class SingleValueData(BaseData):
    """
    Data point for line and area charts.

    This class represents a single value data point with a time and value.
    It's used for line charts, area charts, and other single-value series.

    Attributes:
        value: The numeric value for this data point.
    """

    value: float

    def __init__(self, time: Union[str, int, float, datetime, pd.Timestamp], value: float):
        """
        Initialize a single value data point.

        Args:
            time: Time for this data point in various formats.
            value: Numeric value for this data point.

        Example:
            ```python
            # Using date string
            data = SingleValueData("2024-01-01", 100.5)

            # Using timestamp
            data = SingleValueData(1704067200, 100.5)

            # Using datetime
            data = SingleValueData(datetime(2024, 1, 1), 100.5)
            ```
        """
        self.time = time
        self.value = value


@dataclass
class OhlcData(BaseData):
    """
    Data point for candlestick and bar charts.

    This class represents an OHLC (Open, High, Low, Close) data point,
    commonly used in financial charts for candlestick and bar representations.

    Attributes:
        open: Opening price for the period.
        high: Highest price during the period.
        low: Lowest price during the period.
        close: Closing price for the period.
    """

    open: float
    high: float
    low: float
    close: float

    def __init__(
        self,
        time: Union[str, int, float, datetime, pd.Timestamp],
        open_: float,
        high: float,
        low: float,
        close: float,
    ):
        """
        Initialize an OHLC data point.

        Args:
            time: Time for this data point in various formats.
            open_: Opening price for the period.
            high: Highest price during the period.
            low: Lowest price during the period.
            close: Closing price for the period.

        Example:
            ```python
            # Create OHLC data point
            ohlc = OhlcData("2024-01-01", 100.0, 105.0, 98.0, 102.0)

            # Access OHLC values
            print(f"Open: {ohlc.open}, High: {ohlc.high}")
            ```
        """
        self.time = time
        self.open = open_
        self.high = high
        self.low = low
        self.close = close


@dataclass
class OhlcvData(BaseData):
    """
    Data point for candlestick charts with volume.

    This class represents an OHLCV (Open, High, Low, Close, Volume) data point,
    commonly used in financial charts for candlestick representations with volume.

    Attributes:
        open: Opening price for the period.
        high: Highest price during the period.
        low: Lowest price during the period.
        close: Closing price for the period.
        volume: Trading volume for the period.
    """

    open: float
    high: float
    low: float
    close: float
    volume: float

    def __init__(
        self,
        time: Union[str, int, float, datetime, pd.Timestamp],
        open_: float,
        high: float,
        low: float,
        close: float,
        volume: float,
    ):
        """
        Initialize an OHLCV data point.

        Args:
            time: Time for this data point in various formats.
            open_: Opening price for the period.
            high: Highest price during the period.
            low: Lowest price during the period.
            close: Closing price for the period.
            volume: Trading volume for the period.

        Example:
            ```python
            # Create OHLCV data point
            ohlcv = OhlcvData("2024-01-01", 100.0, 105.0, 98.0, 102.0, 1000000)

            # Access OHLCV values
            print(f"Open: {ohlcv.open}, Volume: {ohlcv.volume}")
            ```
        """
        self.time = time
        self.open = open_
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume


@dataclass
class HistogramData(BaseData):
    """
    Data point for histogram charts.

    This class represents a histogram data point with a time, value, and
    optional color. It's used for volume charts and other histogram series.

    Attributes:
        value: The numeric value for this histogram bar.
        color: Optional color for this histogram bar. If None, default
            color will be used.
    """

    value: float
    color: Optional[str] = None

    def __init__(
        self,
        time: Union[str, int, float, datetime, pd.Timestamp],
        value: float,
        color: Optional[str] = None,
    ):
        """
        Initialize a histogram data point.

        Args:
            time: Time for this data point in various formats.
            value: Numeric value for this histogram bar.
            color: Optional color for this histogram bar. Can be any valid
                CSS color string (hex, rgb, named color, etc.).

        Example:
            ```python
            # Basic histogram data
            hist = HistogramData("2024-01-01", 1000000)

            # Histogram data with custom color
            hist = HistogramData("2024-01-01", 1000000, "#26a69a")
            ```
        """
        self.time = time
        self.value = value
        self.color = color


@dataclass
class BaselineData(BaseData):
    """
    Data point for baseline charts.

    This class represents a baseline data point with a time and value.
    It's used for baseline charts that show values relative to a baseline.

    Attributes:
        value: The numeric value for this data point.
    """

    value: float

    def __init__(self, time: Union[str, int, float, datetime, pd.Timestamp], value: float):
        """
        Initialize a baseline data point.

        Args:
            time: Time for this data point in various formats.
            value: Numeric value for this data point.

        Example:
            ```python
            # Create baseline data point
            baseline = BaselineData("2024-01-01", 5.2)
            ```
        """
        self.time = time
        self.value = value


@dataclass
class Marker:
    """
    Chart marker definition for highlighting data points.

    This class represents a marker that can be displayed on charts to
    highlight specific data points, events, or annotations.

    Attributes:
        _time: Internal time representation (UTC timestamp or date string).
        position: Where to position the marker relative to the data point.
        color: Color of the marker.
        shape: Shape of the marker.
        text: Optional text to display with the marker.
        size: Optional size of the marker.
    """

    _time: Optional[Union[str, int]] = field(default=None, init=False, repr=False)
    position: MarkerPosition
    color: str
    shape: MarkerShape
    text: Optional[str] = None
    size: Optional[int] = None

    def __init__(
        self,
        time: Union[str, int, float, datetime, pd.Timestamp],
        position: MarkerPosition,
        color: str,
        shape: MarkerShape,
        text: Optional[str] = None,
        size: Optional[int] = None,
    ):
        """
        Initialize a chart marker with time and visual properties.

        Args:
            time: Time for this marker in various formats.
            position: Where to position the marker relative to the data point.
            color: Color of the marker. Can be any valid CSS color string.
            shape: Shape of the marker (circle, square, arrow, etc.).
            text: Optional text to display with the marker.
            size: Optional size of the marker in pixels.

        Example:
            ```python
            # Create a simple marker
            marker = Marker(
                time="2024-01-01",
                position=MarkerPosition.ABOVE_BAR,
                color="#26a69a",
                shape=MarkerShape.CIRCLE
            )

            # Create a marker with text and size
            marker = Marker(
                time="2024-01-01",
                position=MarkerPosition.BELOW_BAR,
                color="red",
                shape=MarkerShape.ARROW_UP,
                text="Buy Signal",
                size=12
            )
            ```
        """
        self.time = time
        self.position = position
        self.color = color
        self.shape = shape
        self.text = text
        self.size = size

    @property
    def time(self) -> pd.Timestamp:
        """
        Get time as pandas Timestamp.

        Returns:
            Pandas Timestamp object representing the marker time.
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
        Convert marker to dictionary representation.

        This method creates a dictionary representation of the marker
        suitable for serialization or frontend consumption.

        Returns:
            Dictionary containing the marker's attributes including
            time, position, color, shape, and optional text and size.
        """
        result = {
            "time": self._time,
            "position": self.position.value,
            "color": self.color,
            "shape": self.shape.value,
        }
        # Add optional fields only if they are set
        if self.text is not None:
            result["text"] = self.text
        if self.size is not None:
            result["size"] = self.size
        return result
