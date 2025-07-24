"""
Band data classes for streamlit-lightweight-charts.

This module provides data classes for band data points used in
band charts such as Bollinger Bands and other envelope indicators.
"""

from datetime import datetime
from typing import Union

import pandas as pd

from streamlit_lightweight_charts_pro.data.base import BaseData


class BandData(BaseData):
    """
    Data point for band charts (e.g., Bollinger Bands).

    This class represents a band data point with upper, middle, and lower values.
    It's used for band charts that show multiple lines simultaneously,
    such as Bollinger Bands, Keltner Channels, or other envelope indicators.

    Attributes:
        upper: The upper band value.
        middle: The middle band value (usually the main line).
        lower: The lower band value.
    """

    upper: float
    middle: float
    lower: float

    def __init__(
        self,
        time: Union[str, int, float, datetime, pd.Timestamp],
        upper: float,
        middle: float,
        lower: float,
    ):
        """
        Initialize a band data point.

        Args:
            time: Time for this data point in various formats.
            upper: Upper band value.
            middle: Middle band value (main line).
            lower: Lower band value.

        Example:
            ```python
            # Create band data point (Bollinger Bands example)
            band = BandData("2024-01-01", 105.0, 100.0, 95.0)

            # Access band values
            logger.info(f"Upper: {band.upper}, Middle: {band.middle}, Lower: {band.lower}")
            ```
        """
        self.time = time
        self.upper = upper
        self.middle = middle
        self.lower = lower
