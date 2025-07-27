"""
Histogram series for streamlit-lightweight-charts.

This module provides the HistogramSeries class for creating histogram charts that display
volume or other single-value data as bars. Histogram series are commonly used for volume overlays
and technical indicators.

The HistogramSeries class supports various styling options including bar color, base value,
and animation effects. It also supports markers and price line configurations.

Example:
    from streamlit_lightweight_charts_pro.charts.series import HistogramSeries
    from streamlit_lightweight_charts_pro.data import SingleValueData

    # Create histogram data
    data = [
        SingleValueData("2024-01-01", 1000),
        SingleValueData("2024-01-02", 1200)
    ]

    # Create histogram series with styling
    series = HistogramSeries(data=data)
    series.color = "#2196F3"
    series.base = 0
"""

from typing import List, Optional, Sequence, Union

import numpy as np
import pandas as pd

from streamlit_lightweight_charts_pro.charts.series.base import Series
from streamlit_lightweight_charts_pro.data import Data
from streamlit_lightweight_charts_pro.data.histogram_data import HistogramData
from streamlit_lightweight_charts_pro.data.ohlcv_data import OhlcvData
from streamlit_lightweight_charts_pro.type_definitions import ChartType


class HistogramSeries(Series):
    """
    Histogram series for lightweight charts.

    This class represents a histogram series that displays data as bars.
    It's commonly used for volume overlays, technical indicators, and other
    bar-based visualizations.

    The HistogramSeries supports various styling options including bar color,
    base value, and animation effects.

    Attributes:
        color: Color of the bars (set via property).
        base: Base value for the bars (set via property).
        price_lines: List of PriceLineOptions for price lines (set after construction)
        price_format: PriceFormatOptions for price formatting (set after construction)
        markers: List of markers to display on this series (set after construction)
    """

    DATA_CLASS = HistogramData

    @property
    def chart_type(self) -> ChartType:
        """Get the chart type for this series."""
        return ChartType.HISTOGRAM

    @classmethod
    def create_volume_series(
        cls,
        data: Union[Sequence[OhlcvData], pd.DataFrame],
        column_mapping: dict,
        up_color: str = "rgba(38,166,154,0.5)",
        down_color: str = "rgba(239,83,80,0.5)",
        **kwargs,
    ) -> "HistogramSeries":
        """
        Create a histogram series for volume data with colors based on price movement.

        This factory method processes OHLCV data and creates a HistogramSeries
        with volume bars colored based on whether the candle is bullish (close >= open)
        or bearish (close < open).

        Args:
            data: OHLCV data as DataFrame or list of OhlcvData objects
            column_mapping: Column mapping for DataFrame input
            up_color: Color for bullish candles (close >= open), default teal
            down_color: Color for bearish candles (close < open), default red
            **kwargs: Additional arguments passed to HistogramSeries constructor

        Returns:
            HistogramSeries: Configured histogram series with colored volume data

        Example:
            ```python
            # From DataFrame
            volume_series = HistogramSeries.create_volume_series(
                df,
                column_mapping={'time': 'datetime', 'volume': 'vol', 'open': 'o', 'close': 'c'},
                up_color="rgba(76,175,80,0.5)",
                down_color="rgba(244,67,54,0.5)"
            )

            # From OHLCV data list
            volume_series = HistogramSeries.create_volume_series(ohlcv_list, {})
            ```
        """
        volume_data = []

        # Handle None or empty data
        if data is None:
            return cls(data=volume_data, **kwargs)

        if isinstance(data, pd.DataFrame):
            # Handle DataFrame input - ultra-optimized vectorized approach
            time_col = column_mapping.get("time", "time")
            volume_col = column_mapping.get("volume", "volume")
            open_col = column_mapping.get("open", "open")
            close_col = column_mapping.get("close", "close")

            # Extract columns as numpy arrays for maximum speed
            # Convert pandas timestamps to seconds (not nanoseconds)
            if hasattr(data[time_col], "dt"):
                times = data[time_col].apply(lambda x: x.timestamp()).values
            else:
                times = data[time_col].values
            volumes = data[volume_col].values
            opens = data[open_col].values
            closes = data[close_col].values

            # Ultra-fast color assignment using boolean indexing
            is_bullish = closes >= opens
            colors = np.full(len(data), down_color, dtype=object)
            colors[is_bullish] = up_color

            # Bulk create HistogramData objects using map for maximum speed
            volume_data = list(
                map(
                    lambda args: HistogramData(time=args[0], value=args[1], color=args[2]),
                    zip(times, volumes, colors),
                )
            )
        else:
            # Handle list of OHLCV data objects
            for item in data:
                # All items should be OhlcvData with volume
                color = up_color if item.close >= item.open else down_color
                volume_data.append(HistogramData(time=item.time, value=item.volume, color=color))

        # Create and return the histogram series
        return cls(data=volume_data, **kwargs)

    def __init__(
        self,
        data: Union[List[Data], pd.DataFrame, pd.Series],
        column_mapping: Optional[dict] = None,
        visible: bool = True,
        price_scale_id: str = "right",
        pane_id: Optional[int] = 0,
        overlay: Optional[bool] = True,
    ):
        """
        Initialize a histogram series with data and configuration.

        Args:
            data: Series data as a list of data objects, pandas DataFrame, or pandas Series.
            column_mapping: Optional column mapping for DataFrame/Series input.
            visible: Whether the series is visible. Defaults to True.
            price_scale_id: ID of the price scale to attach to. Defaults to "right".
            pane_id: The pane index this series belongs to. Defaults to 0.
            overlay: Whether the series overlays another. Defaults to True.

        Raises:
            ValueError: If data is not a valid type (list of Data, DataFrame, or Series).
            ValueError: If DataFrame/Series is provided without column_mapping.

        Example:
            ```python
            # Basic series with list of data objects
            series = HistogramSeries(data=histogram_data)

            # Series with DataFrame
            series = HistogramSeries(
                data=df,
                column_mapping={'time': 'datetime', 'value': 'volume'}
            )

            # Series with Series
            series = HistogramSeries(
                data=series_data,
                column_mapping={'time': 'index', 'value': 'values'}
            )
            ```
        """
        super().__init__(
            data=data,
            column_mapping=column_mapping,
            visible=visible,
            price_scale_id=price_scale_id,
            pane_id=pane_id,
            overlay=overlay,
        )

        # Initialize properties with default values
        self._color = "#26a69a"
        self._base = 0

    @property
    def color(self) -> str:
        """
        Get the color of the bars.

        Returns:
            str: The bar color value.
        """
        return self._color

    @color.setter
    def color(self, value: str) -> None:
        """
        Set the color of the bars.

        Args:
            value (str): The bar color value.
        """
        if not isinstance(value, str):
            raise TypeError("color must be a string")
        self._color = value

    @property
    def base(self) -> float:
        """
        Get the base value for the bars.

        Returns:
            float: The base value.
        """
        return self._base

    @base.setter
    def base(self, value: float) -> None:
        """
        Set the base value for the bars.

        Args:
            value (float): The base value.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("base must be a number")
        self._base = float(value)
