"""Histogram series for streamlit-lightweight-charts."""

from typing import Any, Dict, List, Optional, Sequence, Union

import pandas as pd

from streamlit_lightweight_charts_pro.charts.series.base import Series
from streamlit_lightweight_charts_pro.data import HistogramData
from streamlit_lightweight_charts_pro.type_definitions import ChartType


class HistogramSeries(Series):
    """Histogram series for lightweight charts."""

    def __init__(
        self,
        data: Union[Sequence[HistogramData], pd.DataFrame],
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
        price_scale_config: Optional[Dict[str, Any]] = None,
        # Histogram-specific options
        column_mapping: Optional[Dict[str, str]] = None,
        color: str = "#2196F3",  # TradingView light blue/teal for volume
        base: float = 0,
    ):
        """Initialize histogram series."""
        # Store column mapping first
        self.column_mapping = column_mapping

        # Histogram-specific styling options
        self.color = color
        self.base = base

        # Call parent constructor after setting column_mapping
        super().__init__(
            data=data,
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
            price_scale_config=price_scale_config,
        )

    @property
    def chart_type(self) -> ChartType:
        """Get the chart type for this series."""
        return ChartType.HISTOGRAM

    def _process_dataframe(self, df: pd.DataFrame) -> List[HistogramData]:
        """
        Process pandas DataFrame into HistogramData format.

        This method converts a pandas DataFrame into a list of HistogramData
        objects for histogram chart visualization.

        Args:
            df: Pandas DataFrame to process.

        Returns:
            List[HistogramData]: List of processed data objects.

        Raises:
            ValueError: If required columns are missing from the DataFrame.
        """
        # Use default column mapping if none provided
        column_mapping = self.column_mapping or {"time": "datetime", "value": "close"}

        time_col = column_mapping.get("time", "datetime")
        value_col = column_mapping.get("value", "close")

        if time_col not in df.columns or value_col not in df.columns:
            raise ValueError(f"DataFrame must contain columns: {time_col} and {value_col}")

        # Use vectorized operations for better performance
        times = df[time_col].astype(str).tolist()
        values = df[value_col].astype(float).tolist()

        return [HistogramData(time=time, value=value) for time, value in zip(times, values)]

    def to_frontend_config(self) -> Dict[str, Any]:
        """
        Convert series to frontend-compatible configuration.

        This method creates a dictionary representation of the histogram series
        that can be consumed by the frontend React component.

        Returns:
            Dict[str, Any]: Dictionary containing series configuration for the frontend.
        """
        # Get base configuration
        config = {
            "type": "histogram",
            "data": [item.to_dict() for item in self.data],
            "options": self._get_options_dict(),
        }

        # Add markers if present
        if self.markers:
            config["markers"] = [marker.to_dict() for marker in self.markers]

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
        }

        # Add histogram-specific options
        options.update(
            {
                "color": self.color,
                "base": self.base,
            }
        )

        # Add price scale configuration if present
        if self.price_scale_config:
            options["priceScale"] = self.price_scale_config

        return options
