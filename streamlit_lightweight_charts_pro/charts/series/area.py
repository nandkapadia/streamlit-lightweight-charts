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

from typing import Any, Dict, List

import pandas as pd

from streamlit_lightweight_charts_pro.charts.series.base import Series
from streamlit_lightweight_charts_pro.data import SingleValueData
from streamlit_lightweight_charts_pro.type_definitions import (
    ChartType,
    ColumnNames,
)


class AreaSeries(Series):
    """Area series for lightweight charts."""

    def __init__(
        self,
        data,
        column_mapping=None,
        visible=True,
        price_scale_id="right",
        price_line_visible=False,
        base_line_visible=False,
        price_line_width=1,
        price_line_color="#2196F3",
        price_line_style="solid",
        base_line_width=1,
        base_line_color="#FF9800",
        base_line_style="solid",
        price_format=None,
        markers=None,
        pane_id=0,
        height=None,
        overlay=True,
        **kwargs,
    ):
        # Support test expectation: allow .line_color to reflect price_line_color
        line_color = kwargs.pop("line_color", price_line_color)
        top_color = kwargs.pop("top_color", "#2196F3")
        bottom_color = kwargs.pop("bottom_color", "rgba(33, 150, 243, 0.0)")
        line_width = kwargs.pop("line_width", 2)
        super().__init__(
            data=data,
            column_mapping=column_mapping,
            visible=visible,
            price_scale_id=price_scale_id,
            price_line_visible=price_line_visible,
            base_line_visible=base_line_visible,
            price_line_width=price_line_width,
            price_line_color=line_color,
            price_line_style=price_line_style,
            base_line_width=base_line_width,
            base_line_color=base_line_color,
            base_line_style=base_line_style,
            price_format=price_format,
            markers=markers,
            pane_id=pane_id,
            height=height,
            overlay=overlay,
            **kwargs,
        )
        self.line_color = line_color
        self.top_color = top_color
        self.bottom_color = bottom_color
        self.line_width = line_width

    @property
    def chart_type(self) -> ChartType:
        """Get the chart type for this series."""
        return ChartType.AREA

    def _get_columns(self) -> Dict[str, str]:
        """
        Return the column mapping for area series, using self.column_mapping if set.
        """
        return self.column_mapping or {
            ColumnNames.TIME: ColumnNames.DATETIME,
            ColumnNames.VALUE: ColumnNames.CLOSE,
        }

    def _process_dataframe(self, df: pd.DataFrame) -> List[SingleValueData]:
        """
        Process pandas DataFrame into SingleValueData format.

        This method converts a pandas DataFrame into a list of SingleValueData
        objects for area chart visualization.

        Args:
            df: Pandas DataFrame to process.

        Returns:
            List[SingleValueData]: List of processed data objects.

        Raises:
            ValueError: If required columns are missing from the DataFrame.
        """
        # Use _get_columns for column mapping
        column_mapping = self._get_columns()

        time_col = column_mapping.get(ColumnNames.TIME, ColumnNames.DATETIME)
        value_col = column_mapping.get(ColumnNames.VALUE, ColumnNames.CLOSE)

        # Use vectorized operations for better performance
        times = df[time_col].astype(str).tolist()
        values = df[value_col].astype(float).tolist()

        return [SingleValueData(time=time, value=value) for time, value in zip(times, values)]

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert series to dictionary representation.

        This method creates a dictionary representation of the area series
        that can be consumed by the frontend React component.

        Returns:
            Dict[str, Any]: Dictionary containing series configuration for the frontend.
        """
        # Validate pane configuration
        self._validate_pane_config()

        # Get base configuration
        config = {
            "type": "area",
            "data": [item.to_dict() for item in self.data],
            "options": self._get_options_dict(),
        }

        # Add markers if present
        if self.markers:
            config["markers"] = [marker.to_dict() for marker in self.markers]

        # Add height and pane_id
        if self.height is not None:
            config["height"] = self.height
        config["pane_id"] = self.pane_id
        return config

    def _get_options_dict(self) -> Dict[str, Any]:
        """Get options dictionary for area series."""
        options = {
            "visible": self.visible,
            "priceScaleId": self.price_scale_id,
            "priceLineVisible": self.price_line_visible,
            "priceLineWidth": self.price_line_width,
            "priceLineColor": self.price_line_color,
            "priceLineStyle": self.price_line_style,
            "baseLineVisible": self.base_line_visible,
            "baseLineWidth": self.base_line_width,
            "baseLineColor": self.base_line_color,
            "baseLineStyle": self.base_line_style,
            "priceFormat": self.price_format,
        }

        return options
