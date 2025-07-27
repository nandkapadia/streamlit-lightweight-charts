"""
Band series for streamlit-lightweight-charts.

This module provides the BandSeries class for creating band charts (e.g., Bollinger Bands)
that display upper, middle, and lower bands. Band series are commonly used for technical
indicators and volatility analysis.

The BandSeries class supports various styling options for each band, fill colors, and
animation effects. It also supports markers and price line configurations.

Example:
    from streamlit_lightweight_charts_pro.charts.series import BandSeries
    from streamlit_lightweight_charts_pro.data import BandData

    # Create band data
    data = [
        BandData("2024-01-01", upper=110, middle=105, lower=100),
        BandData("2024-01-02", upper=112, middle=107, lower=102)
    ]

    # Create band series with styling
    series = BandSeries(data=data)
    series.upper_line_options.color = "#4CAF50"
    series.lower_line_options.color = "#F44336"
    series.upper_fill_color = "rgba(76, 175, 80, 0.1)"
    series.lower_fill_color = "rgba(244, 67, 54, 0.1)"
"""

from typing import List, Optional, Union

import pandas as pd

from streamlit_lightweight_charts_pro.charts.options.line_options import LineOptions
from streamlit_lightweight_charts_pro.charts.series.base import Series
from streamlit_lightweight_charts_pro.data.band import BandData
from streamlit_lightweight_charts_pro.type_definitions import (
    ChartType,
)


class BandSeries(Series):
    """
    Band series for lightweight charts (e.g., Bollinger Bands).

    This class represents a band series that displays upper, middle, and lower bands.
    It's commonly used for technical indicators like Bollinger Bands, Keltner Channels,
    and other envelope indicators.

    The BandSeries supports various styling options including separate line styling
    for each band via LineOptions, fill colors, and gradient effects.

    Attributes:
        upper_line_options: LineOptions instance for upper band styling.
        middle_line_options: LineOptions instance for middle band styling.
        lower_line_options: LineOptions instance for lower band styling.
        upper_fill_color: Fill color for upper band area.
        lower_fill_color: Fill color for lower band area.
        price_lines: List of PriceLineOptions for price lines (set after construction)
        price_format: PriceFormatOptions for price formatting (set after construction)
        markers: List of markers to display on this series (set after construction)
    """

    DATA_CLASS = BandData

    def __init__(
        self,
        data: Union[List[BandData], pd.DataFrame, pd.Series],
        column_mapping: Optional[dict] = None,
        visible: bool = True,
        price_scale_id: str = "right",
        pane_id: Optional[int] = 0,
        overlay: Optional[bool] = True,
    ):
        """
        Initialize BandSeries.

        Args:
            data: List of data points or DataFrame
            column_mapping: Column mapping for DataFrame conversion
            visible: Whether the series is visible
            price_scale_id: ID of the price scale
            pane_id: The pane index this series belongs to
            overlay: Whether this series overlays others
        """
        super().__init__(
            data=data,
            column_mapping=column_mapping,
            visible=visible,
            price_scale_id=price_scale_id,
            pane_id=pane_id,
            overlay=overlay,
        )

        # Initialize line options with default values
        self._upper_line_options = LineOptions(color="#4CAF50", line_width=2, line_style="solid")
        self._middle_line_options = LineOptions(color="#2196F3", line_width=2, line_style="solid")
        self._lower_line_options = LineOptions(color="#F44336", line_width=2, line_style="solid")

        # Initialize fill colors
        self._upper_fill_color = "rgba(76, 175, 80, 0.1)"
        self._lower_fill_color = "rgba(244, 67, 54, 0.1)"

    @property
    def chart_type(self) -> ChartType:
        """Get the chart type for this series."""
        return ChartType.BAND

    @property
    def upper_line_options(self) -> LineOptions:
        """Get the upper line options."""
        return self._upper_line_options

    @upper_line_options.setter
    def upper_line_options(self, value: LineOptions) -> None:
        """Set the upper line options."""
        if not isinstance(value, LineOptions):
            raise TypeError("upper_line_options must be a LineOptions instance")
        self._upper_line_options = value

    @property
    def middle_line_options(self) -> LineOptions:
        """Get the middle line options."""
        return self._middle_line_options

    @middle_line_options.setter
    def middle_line_options(self, value: LineOptions) -> None:
        """Set the middle line options."""
        if not isinstance(value, LineOptions):
            raise TypeError("middle_line_options must be a LineOptions instance")
        self._middle_line_options = value

    @property
    def lower_line_options(self) -> LineOptions:
        """Get the lower line options."""
        return self._lower_line_options

    @lower_line_options.setter
    def lower_line_options(self, value: LineOptions) -> None:
        """Set the lower line options."""
        if not isinstance(value, LineOptions):
            raise TypeError("lower_line_options must be a LineOptions instance")
        self._lower_line_options = value

    @property
    def upper_fill_color(self) -> str:
        """Get the upper fill color."""
        return self._upper_fill_color

    @upper_fill_color.setter
    def upper_fill_color(self, value: str) -> None:
        """Set the upper fill color."""
        if not isinstance(value, str):
            raise TypeError("upper_fill_color must be a string")
        self._upper_fill_color = value

    @property
    def lower_fill_color(self) -> str:
        """Get the lower fill color."""
        return self._lower_fill_color

    @lower_fill_color.setter
    def lower_fill_color(self, value: str) -> None:
        """Set the lower fill color."""
        if not isinstance(value, str):
            raise TypeError("lower_fill_color must be a string")
        self._lower_fill_color = value
