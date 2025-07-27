"""
AreaData module for area series data points.

This module defines the AreaData class which represents data points for area series,
including optional color properties for line, top, and bottom colors.
"""

from dataclasses import dataclass
from typing import Optional

from streamlit_lightweight_charts_pro.data.single_value_data import SingleValueData
from streamlit_lightweight_charts_pro.utils.data_utils import is_valid_color


@dataclass
class AreaData(SingleValueData):
    """
    Data class for area series data points.

    This class represents a single data point for area series, extending SingleValueData
    with optional color properties for line, top, and bottom colors.

    Attributes:
            time: The time of the data point (inherited from SingleValueData)
    value: The price value of the data point (inherited from SingleValueData)
        lineColor: Optional line color for this specific data point
        topColor: Optional top color for the area fill
        bottomColor: Optional bottom color for the area fill
    """

    # Required columns from SingleValueData
    REQUIRED_COLUMNS = set()

    # Optional columns specific to AreaData
    OPTIONAL_COLUMNS = {"lineColor", "topColor", "bottomColor"}

    # Optional color properties
    lineColor: Optional[str] = None
    topColor: Optional[str] = None
    bottomColor: Optional[str] = None

    def __post_init__(self):
        """Validate and normalize data after initialization."""
        # Call parent's __post_init__ for time normalization and value validation
        super().__post_init__()

        # Validate color properties if provided (and not empty)
        if (
            self.lineColor is not None
            and self.lineColor.strip()
            and not is_valid_color(self.lineColor)
        ):
            raise ValueError(f"Invalid lineColor format: {self.lineColor}")

        if (
            self.topColor is not None
            and self.topColor.strip()
            and not is_valid_color(self.topColor)
        ):
            raise ValueError(f"Invalid topColor format: {self.topColor}")

        if (
            self.bottomColor is not None
            and self.bottomColor.strip()
            and not is_valid_color(self.bottomColor)
        ):
            raise ValueError(f"Invalid bottomColor format: {self.bottomColor}")

    def to_dict(self):
        """
        Convert the AreaData to a dictionary for frontend consumption.

        Returns:
            dict: Dictionary representation with camelCase keys and validated data.
        """
        result = super().to_dict()

        # Remove None, empty, and whitespace-only color values that were added by parent
        for color_key in ["lineColor", "topColor", "bottomColor"]:
            value = result.get(color_key)
            if value is None or value == "" or (isinstance(value, str) and value.strip() == ""):
                result.pop(color_key, None)

        # Add color properties only if they are not None and not empty
        if self.lineColor and self.lineColor.strip():
            result["lineColor"] = self.lineColor

        if self.topColor and self.topColor.strip():
            result["topColor"] = self.topColor

        if self.bottomColor and self.bottomColor.strip():
            result["bottomColor"] = self.bottomColor

        return result
