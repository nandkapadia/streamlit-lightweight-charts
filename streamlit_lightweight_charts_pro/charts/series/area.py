"""
Area series for streamlit-lightweight-charts.

This module provides the AreaSeries class for creating area charts that display
continuous data points with filled areas under the line. Area series are commonly
used for price charts, indicators, and trend analysis.

The AreaSeries class supports various styling options including area color,
line color, width, style, and animation effects. It also supports markers and price
line configurations.

Example:
    from streamlit_lightweight_charts_pro.charts.series import AreaSeries
    from streamlit_lightweight_charts_pro.data import SingleValueData

    # Create area data
    data = [
        SingleValueData("2024-01-01", 100),
        SingleValueData("2024-01-02", 105),
        SingleValueData("2024-01-03", 102)
    ]

    # Create area series with styling
    series = AreaSeries(
        data=data,
        top_color="rgba(33, 150, 243, 0.4)",
        bottom_color="rgba(33, 150, 243, 0.0)",
        line_color="#2196F3",
        line_width=2
    )
"""

from typing import List, Optional, Union

import pandas as pd

from streamlit_lightweight_charts_pro.charts.options.line_options import LineOptions
from streamlit_lightweight_charts_pro.charts.series.base import Series
from streamlit_lightweight_charts_pro.data.area_data import AreaData
from streamlit_lightweight_charts_pro.type_definitions import (
    ChartType,
)


class AreaSeries(Series):
    """
    Area series for lightweight charts.

    This class represents an area series that displays continuous data points
    with filled areas under the line. It's commonly used for price charts,
    technical indicators, and trend analysis.

    The AreaSeries supports various styling options including area colors,
    line styling via LineOptions, and gradient effects.

    Attributes:
        line_options: LineOptions instance for line styling (optional).
        top_color: Color of the top part of the area.
        bottom_color: Color of the bottom part of the area.
        relative_gradient: Whether gradient is relative to base value.
        invert_filled_area: Whether to invert the filled area.
        price_lines: List of PriceLineOptions for price lines (set after construction)
        price_format: PriceFormatOptions for price formatting (set after construction)
        markers: List of markers to display on this series (set after construction)
    """

    DATA_CLASS = AreaData

    def __init__(
        self,
        data: Union[List[AreaData], pd.DataFrame, pd.Series],
        column_mapping: Optional[dict] = None,
        visible: bool = True,
        price_scale_id: str = "right",
        pane_id: Optional[int] = 0,
        overlay: Optional[bool] = True,
    ):
        """
        Initialize AreaSeries.

        Args:
            data: List of data points or DataFrame
            column_mapping: Column mapping for DataFrame conversion
            visible: Whether the series is visible
            price_scale_id: ID of the price scale
            pane_id: The pane index this series belongs to
            overlay: Whether this series overlays others
            top_color: Color of the top part of the area
            bottom_color: Color of the bottom part of the area
            relative_gradient: Gradient is relative to base value
            invert_filled_area: Invert filled area
        """
        super().__init__(
            data=data,
            column_mapping=column_mapping,
            visible=visible,
            price_scale_id=price_scale_id,
            pane_id=pane_id,
            overlay=overlay,
        )

        # Initialize properties before using setters
        self._line_options = LineOptions()
        self._top_color = "#2196F3"
        self._bottom_color = "rgba(33, 150, 243, 0.0)"
        self._relative_gradient = False
        self._invert_filled_area = False

    @property
    def chart_type(self) -> ChartType:
        """Get the chart type for this series."""
        return ChartType.AREA

    @property
    def line_options(self) -> Optional[LineOptions]:
        """
        Get the line options for this series.

        Returns:
            Optional[LineOptions]: The line styling options, or None if not set.
        """
        return self._line_options

    @line_options.setter
    def line_options(self, value: Optional[LineOptions]) -> None:
        """
        Set the line options for this series.

        Args:
            value (Optional[LineOptions]): The line styling options to set.
        """
        if value is not None and not isinstance(value, LineOptions):
            raise TypeError("line_options must be an instance of LineOptions or None")
        self._line_options = value

    @property
    def top_color(self) -> str:
        """
        Get the top color of the area.

        Returns:
            str: The top color value.
        """
        return self._top_color

    @top_color.setter
    def top_color(self, value: str) -> None:
        """
        Set the top color of the area.

        Args:
            value (str): The top color value.
        """
        if not isinstance(value, str):
            raise TypeError("top_color must be a string")
        self._top_color = value

    @property
    def bottom_color(self) -> str:
        """
        Get the bottom color of the area.

        Returns:
            str: The bottom color value.
        """
        return self._bottom_color

    @bottom_color.setter
    def bottom_color(self, value: str) -> None:
        """
        Set the bottom color of the area.

        Args:
            value (str): The bottom color value.
        """
        if not isinstance(value, str):
            raise TypeError("bottom_color must be a string")
        self._bottom_color = value

    @property
    def relative_gradient(self) -> bool:
        """
        Get whether the gradient is relative to base value.

        Returns:
            bool: True if gradient is relative, False otherwise.
        """
        return self._relative_gradient

    @relative_gradient.setter
    def relative_gradient(self, value: bool) -> None:
        """
        Set whether the gradient is relative to base value.

        Args:
            value (bool): True if gradient should be relative, False otherwise.
        """
        if not isinstance(value, bool):
            raise TypeError("relative_gradient must be a boolean")
        self._relative_gradient = value

    @property
    def invert_filled_area(self) -> bool:
        """
        Get whether the filled area is inverted.

        Returns:
            bool: True if filled area is inverted, False otherwise.
        """
        return self._invert_filled_area

    @invert_filled_area.setter
    def invert_filled_area(self, value: bool) -> None:
        """
        Set whether the filled area should be inverted.

        Args:
            value (bool): True if filled area should be inverted, False otherwise.
        """
        if not isinstance(value, bool):
            raise TypeError("invert_filled_area must be a boolean")
        self._invert_filled_area = value
