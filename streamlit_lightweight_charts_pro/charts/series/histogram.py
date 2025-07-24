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
    series = HistogramSeries(
        data=data,
        color="#2196F3",
        base=0
    )
"""

from typing import Any, Dict, List, Optional, Sequence, Union

import pandas as pd

from streamlit_lightweight_charts_pro.charts.series.base import Series
from streamlit_lightweight_charts_pro.data import SingleValueData
from streamlit_lightweight_charts_pro.type_definitions import ChartType, ColumnNames


class HistogramSeries(Series):
    """Histogram series for lightweight charts."""

    def __init__(
        self,
        data: Union[Sequence[SingleValueData], pd.DataFrame],
        column_mapping: Optional[Dict[str, str]] = None,
        color: str = "#2196F3",
        visible: bool = True,
        price_scale_id: str = "right",
        price_line_visible: bool = False,
        base_line_visible: bool = False,
        price_line_width: int = 1,
        price_line_color: str = "#2196F3",
        price_line_style: str = "solid",
        base_line_width: int = 1,
        base_line_color: str = "#FF9800",
        base_line_style: str = "solid",
        price_format: Optional[Dict[str, Any]] = None,
        markers: Optional[List[Any]] = None,
        pane_id: int = 0,
        height: Optional[int] = None,
        up_color: Optional[str] = None,
        down_color: Optional[str] = None,
        base: Optional[float] = 0.0,
    ):
        """
        Histogram series for lightweight charts.

        Args:
            data: Data for the histogram series.
            column_mapping: Optional dict mapping expected columns to user columns.
            visible: Whether the series is visible.
            price_scale_id: ID of the price scale to which this series belongs.
            price_line_visible: Whether to show the price line.
            base_line_visible: Whether to show the base line.
            price_line_width: Width of the price line.
            price_line_color: Color of the price line.
            price_line_style: Style of the price line.
            base_line_width: Width of the base line.
            base_line_color: Color of the base line.
            base_line_style: Style of the base line.
            price_format: Optional dictionary for price formatting.
            markers: Optional list of marker configurations.
            pane_id: ID of the pane to which this series belongs.
            height: Optional height for the series.
            up_color: Color for up bars.
            down_color: Color for down bars.
        """
        self.color = color
        self.up_color = up_color
        self.down_color = down_color
        self.base = base

        super().__init__(
            data=data,
            column_mapping=column_mapping,
            visible=visible,
            price_scale_id=price_scale_id,
            price_line_visible=price_line_visible,
            base_line_visible=base_line_visible,
            price_line_width=price_line_width,
            price_line_color=price_line_color,
            price_line_style=price_line_style,
            base_line_width=base_line_width,
            base_line_color=base_line_color,
            base_line_style=base_line_style,
            price_format=price_format,
            markers=markers,
            pane_id=pane_id,
            height=height,
        )

    @property
    def chart_type(self) -> ChartType:
        """Get the chart type for this series."""
        return ChartType.HISTOGRAM

    def _get_columns(self) -> Dict[str, str]:
        """
        Return the column mapping for histogram series, using self.column_mapping if set.
        """
        # Use self.column_mapping if provided, else default mapping
        if self.column_mapping:
            return self.column_mapping
        return {
            ColumnNames.TIME: ColumnNames.DATETIME,
            ColumnNames.VALUE: ColumnNames.CLOSE,
        }

    def _process_dataframe(self, df: pd.DataFrame) -> List[SingleValueData]:
        """
        Process pandas DataFrame into SingleValueData format.

        This method converts a pandas DataFrame into a list of SingleValueData
        objects for histogram chart visualization.

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

        column_mapping.get(ColumnNames.OPEN, ColumnNames.OPEN)
        column_mapping.get(ColumnNames.CLOSE, ColumnNames.CLOSE)

        if time_col not in df.columns or value_col not in df.columns:
            raise ValueError(f"DataFrame must contain columns: {time_col} and {value_col}")

        if self.up_color and self.down_color:
            if ColumnNames.OPEN.value in df.columns and ColumnNames.CLOSE.value in df.columns:
                df["color"] = [
                    self.up_color if close >= open_ else self.down_color
                    for open_, close in zip(df[ColumnNames.OPEN.value], df[ColumnNames.CLOSE.value])
                ]
        else:
            df["color"] = None  # Optional fallback if color is needed

        # Build SingleValueData
        return [
            SingleValueData(time=t, value=v, color=c)
            for t, v, c in zip(df[time_col], df[value_col], df["color"])
        ]

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert series to dictionary representation.

        This method creates a dictionary representation of the histogram series
        that can be consumed by the frontend React component.

        Returns:
            Dict[str, Any]: Dictionary containing series configuration for the frontend.
        """
        # Validate pane configuration
        self._validate_pane_config()

        # Get base configuration
        config = {
            "type": "histogram",
            "data": self.data_dict,
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
        """Get options dictionary for histogram series."""
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
            "color": self.color,
            "base": self.base,
        }

        # Add price scale configuration if present
        # price_scale_config removed

        return options
