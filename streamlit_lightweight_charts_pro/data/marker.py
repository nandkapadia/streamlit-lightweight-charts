"""
Marker data classes for streamlit-lightweight-charts.

This module provides data classes for chart markers used to highlight
specific data points or events on charts.
"""

from dataclasses import dataclass
from typing import Optional, Union

from streamlit_lightweight_charts_pro.data.data import Data
from streamlit_lightweight_charts_pro.type_definitions.enums import MarkerPosition, MarkerShape


@dataclass
class Marker(Data):
    """
    Chart marker definition for highlighting data points.

    This class represents a marker that can be displayed on charts to
    highlight specific data points, events, or annotations.

    Attributes:
        time: UNIX timestamp in seconds.
        position: Where to position the marker relative to the data point.
        color: Color of the marker.
        shape: Shape of the marker.
        text: Optional text to display with the marker.
        size: Optional size of the marker.
    """

    REQUIRED_COLUMNS = {"position", "shape"}
    OPTIONAL_COLUMNS = {"text", "color", "size"}

    position: Union[str, MarkerPosition] = MarkerPosition.ABOVE_BAR
    color: str = "#2196F3"  # Default blue color
    shape: Union[str, MarkerShape] = MarkerShape.CIRCLE
    text: Optional[str] = None
    size: int = 8  # Default size in pixels

    def __post_init__(self):
        """Post-initialization processing."""
        # Call parent's __post_init__ for time normalization
        super().__post_init__()

        # Convert position to enum if it's a string
        if isinstance(self.position, str):
            self.position = MarkerPosition(self.position)

        # Convert shape to enum if it's a string
        if isinstance(self.shape, str):
            self.shape = MarkerShape(self.shape)
