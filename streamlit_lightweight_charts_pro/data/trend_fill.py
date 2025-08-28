"""
Trend fill data classes for streamlit-lightweight-charts.

This module provides TrendFillData class for creating trend-based fill charts
that display fills between trend lines and candle body midpoints, similar to
Supertrend indicators with dynamic trend-colored backgrounds.

The class now properly handles upper and lower trend lines based on trend direction:
- Uptrend (+1): Shows lower trend line below price as support
- Downtrend (-1): Shows upper trend line above price as resistance
"""

import math
from dataclasses import dataclass
from typing import Optional

from streamlit_lightweight_charts_pro.data.data import Data


@dataclass
class TrendFillData(Data):
    """
    Trend fill data for lightweight charts.

    This data class represents a single data point for trend fill charts,
    with intuitive upper/lower trend line handling:

    - Uptrend (+1): Uses lower_trend line below price as support
    - Downtrend (-1): Uses upper_trend line above price as resistance
    - Neutral (0): No trend line displayed

    The fill area is created between the active trend line and base line,
    with colors automatically selected based on trend direction.

    Attributes:
        time: Time value for the data point
        base_line: Base line value (e.g., candle body midpoint, price level)
        trend_direction: Trend direction indicator (-1 for downtrend, 1 for uptrend, 0 for neutral)

        # Trend line fields
        upper_trend: Value of the upper trend line (used when trend_direction == -1)
        lower_trend: Value of the lower trend line (used when trend_direction == 1)

        # Fill color fields
        uptrend_fill_color: Optional custom uptrend fill color
        downtrend_fill_color: Optional custom downtrend fill color
    """

    REQUIRED_COLUMNS = {"base_line", "upper_trend", "lower_trend", "trend_direction"}
    OPTIONAL_COLUMNS = {
        "uptrend_fill_color",
        "downtrend_fill_color",
    }

    # Core fields
    base_line: float = 0
    upper_trend: float = 0
    lower_trend: float = 0
    trend_direction: int = 0

    # Trend line fields (intuitive naming)

    # Fill color fields
    uptrend_fill_color: Optional[str] = None
    downtrend_fill_color: Optional[str] = None

    def __post_init__(self):
        """Validate and process data after initialization."""
        super().__post_init__()

        # Handle NaN values for all trend line fields
        if isinstance(self.upper_trend, float) and math.isnan(self.upper_trend):
            self.upper_trend = None
        if isinstance(self.lower_trend, float) and math.isnan(self.lower_trend):
            self.lower_trend = None
        if isinstance(self.base_line, float) and math.isnan(self.base_line):
            self.base_line = None

        # Validate trend_direction
        if not isinstance(self.trend_direction, int):
            raise ValueError(
                f"trend_direction must be an integer, got {type(self.trend_direction)}"
            )

        if self.trend_direction not in [-1, 0, 1]:
            raise ValueError(f"trend_direction must be -1, 0, or 1, got {self.trend_direction}")

        # Validate fill colors if provided
        if self.uptrend_fill_color is not None and not isinstance(self.uptrend_fill_color, str):
            raise ValueError(
                f"uptrend_fill_color must be a string, got {type(self.uptrend_fill_color)}"
            )
        if self.downtrend_fill_color is not None and not isinstance(self.downtrend_fill_color, str):
            raise ValueError(
                f"downtrend_fill_color must be a string, got {type(self.downtrend_fill_color)}"
            )

    @property
    def is_uptrend(self) -> bool:
        """Check if this data point represents an uptrend."""
        return self.trend_direction == 1

    @property
    def is_downtrend(self) -> bool:
        """Check if this data point represents a downtrend."""
        return self.trend_direction == -1

    @property
    def is_neutral(self) -> bool:
        """Check if this data point represents a neutral trend."""
        return self.trend_direction == 0

    @property
    def has_valid_fill_data(self) -> bool:
        """
        Check if this data point has valid data for creating fills.

        Returns True if we have a valid trend line and base line,
        with the appropriate trend line based on direction.
        """
        if self.trend_direction == 0 or self.base_line is None:
            return False

        # Check if we have the appropriate trend line for the direction
        if self.trend_direction == 1:  # Uptrend needs lower trend line
            return self.lower_trend is not None
        elif self.trend_direction == -1:  # Downtrend needs upper trend line
            return self.upper_trend is not None

        return False

    @property
    def has_valid_uptrend_fill(self) -> bool:
        """Check if this data point has valid uptrend fill data."""
        return (
            self.base_line is not None
            and self.trend_direction == 1
            and self.lower_trend is not None
        )

    @property
    def has_valid_downtrend_fill(self) -> bool:
        """Check if this data point has valid downtrend fill data."""
        return (
            self.base_line is not None
            and self.trend_direction == -1
            and self.upper_trend is not None
        )

    @property
    def active_trend_line(self) -> Optional[float]:
        """
        Get the active trend line value based on trend direction.

        Returns the appropriate trend line value for the current trend direction:
        - Uptrend (+1): Returns lower_trend (support line below price)
        - Downtrend (-1): Returns upper_trend (resistance line above price)
        """
        if self.trend_direction == 1:  # Uptrend - use lower trend as support
            return self.lower_trend
        elif self.trend_direction == -1:  # Downtrend - use upper trend as resistance
            return self.upper_trend
        return None

    @property
    def active_fill_color(self) -> Optional[str]:
        """
        Get the active fill color based on trend direction.

        Returns the appropriate fill color for the current trend direction,
        prioritizing direction-specific colors.
        """
        if self.trend_direction == 1:  # Uptrend
            return self.uptrend_fill_color
        elif self.trend_direction == -1:  # Downtrend
            return self.downtrend_fill_color
        return None

    @property
    def trend_line_type(self) -> Optional[str]:
        """
        Get the type of trend line being displayed.

        Returns:
            'upper' for downtrend (resistance above price)
            'lower' for uptrend (support below price)
            None for neutral
        """
        if self.trend_direction == 1:
            return "lower"
        elif self.trend_direction == -1:
            return "upper"
        return None
