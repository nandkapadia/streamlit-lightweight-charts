"""
OHLC data classes for streamlit-lightweight-charts.

This module provides data classes for OHLC (Open, High, Low, Close) data points
used in candlestick and bar charts.
"""

from datetime import datetime
from typing import Union

import pandas as pd

from streamlit_lightweight_charts_pro.data.base import BaseData


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
            logger.info(f"Open: {ohlc.open}, High: {ohlc.high}")
            ```
        """
        self.time = time
        self.open = open_
        self.high = high
        self.low = low
        self.close = close


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
            logger.info(f"Open: {ohlcv.open}, Volume: {ohlcv.volume}")
            ```
        """
        self.time = time
        self.open = open_
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
