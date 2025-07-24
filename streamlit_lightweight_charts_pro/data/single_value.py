"""
Single value data classes for streamlit-lightweight-charts.

This module provides data classes for single value data points used in
line charts, area charts, baseline charts, and histogram charts.

Note: All single-value data types (line, area, baseline, histogram) now use
the same SingleValueData class for consistency and reduced code duplication.
"""

from datetime import datetime
from typing import Optional, Union

import pandas as pd

from streamlit_lightweight_charts_pro.data.base import BaseData


class SingleValueData(BaseData):
    """
    Data point for line, area, baseline, and histogram charts.

    This class represents a single value data point with a time, value, and optional color.
    It's used for line charts, area charts, baseline charts, histogram charts, and other
    single-value series.

    Attributes:
        value: The numeric value for this data point.
        color: Optional color for this data point. If None, default color will be used.
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
        Initialize a single value data point.

        Args:
            time: Time for this data point in various formats.
            value: Numeric value for this data point.
            color: Optional color for this data point. Can be any valid CSS color
                string (hex, rgb, named color, etc.). If None, default color will be used.

        Note:
            self.time is always stored as a pandas.Timestamp for consistency and
            to support UNIX time conversion for the frontend.
        """
        if isinstance(time, pd.Timestamp):
            self.time = time
        elif isinstance(time, datetime):
            self.time = pd.Timestamp(time)
        elif isinstance(time, (int, float)):
            # Assume UNIX timestamp in seconds
            self.time = pd.to_datetime(time, unit='s')
        elif isinstance(time, str):
            self.time = pd.to_datetime(time)
        else:
            raise ValueError(f"Unsupported time type: {type(time)}")
        self.value = value
        self.color = color
