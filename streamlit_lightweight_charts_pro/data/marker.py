"""
Marker data classes for streamlit-lightweight-charts.

This module provides data classes for chart markers used to highlight
specific data points or events on charts.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional, Union

import pandas as pd

from streamlit_lightweight_charts_pro.data.base import from_utc_timestamp, to_utc_timestamp
from streamlit_lightweight_charts_pro.type_definitions.enums import MarkerShape, MarkerPosition
from streamlit_lightweight_charts_pro.type_definitions import ColumnNames


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
        position: Union[str, MarkerPosition],
        color: str,
        shape: Union[str, MarkerShape],
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
        # Accept both str and Enum for position
        if isinstance(position, str):
            self.position = MarkerPosition(position)
        else:
            self.position = position
        self.color = color
        # Accept both str and Enum for shape
        if isinstance(shape, str):
            self.shape = MarkerShape(shape)
        else:
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
            ColumnNames.TIME: self._time,
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
