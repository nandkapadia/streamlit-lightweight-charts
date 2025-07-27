"""
Bar series for streamlit-lightweight-charts.

This module provides the BarSeries class for creating bar charts that display
OHLC data as bars. Bar series are commonly used for price charts and volume overlays.

The BarSeries class supports various styling options including bar color, base value,
and animation effects. It also supports markers and price line configurations.

Example:
    from streamlit_lightweight_charts_pro.charts.series import BarSeries
    from streamlit_lightweight_charts_pro.data import SingleValueData

    # Create bar data
    data = [
        SingleValueData("2024-01-01", 100),
        SingleValueData("2024-01-02", 105)
    ]

    # Create bar series with styling
    series = BarSeries(data=data)
    series.color = "#26a69a"
    series.base = 0
"""

from typing import List, Optional, Union

import pandas as pd

from streamlit_lightweight_charts_pro.charts.series.base import Series
from streamlit_lightweight_charts_pro.data import BarData
from streamlit_lightweight_charts_pro.type_definitions import ChartType


class BarSeries(Series):
    """
    Bar series for lightweight charts.

    This class represents a bar series that displays data as bars.
    It's commonly used for price charts, volume overlays, and other
    bar-based visualizations.

    The BarSeries supports various styling options including bar colors,
    base value, and animation effects.

    Attributes:
        color: Color of the bars (set via property).
        base: Base value for the bars (set via property).
        up_color: Color for up bars (set via property).
        down_color: Color for down bars (set via property).
        open_visible: Whether open values are visible (set via property).
        thin_bars: Whether to use thin bars (set via property).
        price_lines: List of PriceLineOptions for price lines (set after construction)
        price_format: PriceFormatOptions for price formatting (set after construction)
        markers: List of markers to display on this series (set after construction)
    """

    DATA_CLASS = BarData

    @property
    def chart_type(self) -> ChartType:
        """Get the chart type for this series."""
        return ChartType.BAR

    def __init__(
        self,
        data: Union[List[BarData], pd.DataFrame, pd.Series],
        column_mapping: Optional[dict] = None,
        visible: bool = True,
        price_scale_id: str = "right",
        pane_id: Optional[int] = 0,
        overlay: Optional[bool] = True,
    ):
        super().__init__(
            data=data,
            column_mapping=column_mapping,
            visible=visible,
            price_scale_id=price_scale_id,
            pane_id=pane_id,
            overlay=overlay,
        )

        # Initialize properties with default values
        self._up_color = "#26a69a"
        self._down_color = "#ef5350"
        self._open_visible = True
        self._thin_bars = True

    @property
    def up_color(self) -> str:
        """
        Get the color for up bars.

        Returns:
            str: The up bar color value.
        """
        return self._up_color

    @up_color.setter
    def up_color(self, value: str) -> None:
        """
        Set the color for up bars.

        Args:
            value (str): The up bar color value.
        """
        if not isinstance(value, str):
            raise TypeError("up_color must be a string")
        self._up_color = value

    @property
    def down_color(self) -> str:
        """
        Get the color for down bars.

        Returns:
            str: The down bar color value.
        """
        return self._down_color

    @down_color.setter
    def down_color(self, value: str) -> None:
        """
        Set the color for down bars.

        Args:
            value (str): The down bar color value.
        """
        if not isinstance(value, str):
            raise TypeError("down_color must be a string")
        self._down_color = value

    @property
    def open_visible(self) -> bool:
        """
        Get whether open values are visible.

        Returns:
            bool: True if open values are visible, False otherwise.
        """
        return self._open_visible

    @open_visible.setter
    def open_visible(self, value: bool) -> None:
        """
        Set whether open values should be visible.

        Args:
            value (bool): True if open values should be visible, False otherwise.
        """
        if not isinstance(value, bool):
            raise TypeError("open_visible must be a boolean")
        self._open_visible = value

    @property
    def thin_bars(self) -> bool:
        """
        Get whether to use thin bars.

        Returns:
            bool: True if thin bars should be used, False otherwise.
        """
        return self._thin_bars

    @thin_bars.setter
    def thin_bars(self, value: bool) -> None:
        """
        Set whether to use thin bars.

        Args:
            value (bool): True if thin bars should be used, False otherwise.
        """
        if not isinstance(value, bool):
            raise TypeError("thin_bars must be a boolean")
        self._thin_bars = value
