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
from streamlit_lightweight_charts_pro.utils import chainable_property
from streamlit_lightweight_charts_pro.utils.data_utils import is_valid_color


@chainable_property("upper_line_options", LineOptions, allow_none=True)
@chainable_property("middle_line_options", LineOptions, allow_none=True)
@chainable_property("lower_line_options", LineOptions, allow_none=True)
@chainable_property("upper_fill_color", str, validator=lambda v: BandSeries._validate_color_static(v, "upper_fill_color"))
@chainable_property("lower_fill_color", str, validator=lambda v: BandSeries._validate_color_static(v, "lower_fill_color"))
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
    ):
        """
        Initialize BandSeries.

        Args:
            data: List of data points or DataFrame
            column_mapping: Column mapping for DataFrame conversion
            visible: Whether the series is visible
            price_scale_id: ID of the price scale
            pane_id: The pane index this series belongs to
        """
        super().__init__(
            data=data,
            column_mapping=column_mapping,
            visible=visible,
            price_scale_id=price_scale_id,
            pane_id=pane_id,
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
    
    @staticmethod
    def _validate_color_static(color: str, property_name: str) -> str:
        """Static version of color validator for decorator use."""
        if not is_valid_color(color):
            raise ValueError(
                f"Invalid color format for {property_name}: {color!r}. Must be hex or rgba."
            )
        return color


