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
        column_mapping: Optional[Dict[str, str]] = None,
        markers: Optional[List[Any]] = None,
        price_scale: Optional[Dict[str, Any]] = None,
        # Histogram-specific options
        color: str = "#26a69a",
        base: float = 0,
        **kwargs,
    ):
        """Initialize histogram series."""
        super().__init__(
            data=data,
            column_mapping=column_mapping,
            markers=markers,
            price_scale=price_scale,
            **kwargs,
        )

        # Histogram-specific styling options
        self.color = color
        self.base = base

    @property
    def chart_type(self) -> ChartType:
        """Get the chart type for this series."""
        return ChartType.HISTOGRAM

    def _convert_dataframe(
        self, df: pd.DataFrame, column_mapping: Optional[Dict[str, str]] = None
    ) -> List[HistogramData]:
        """Convert DataFrame to HistogramData format."""
        if column_mapping is None:
            column_mapping = {"time": "datetime", "value": "close"}

        time_col = column_mapping.get("time", "datetime")
        value_col = column_mapping.get("value", "close")

        if time_col not in df.columns or value_col not in df.columns:
            raise ValueError(f"DataFrame must contain columns: {time_col} and {value_col}")

        # Use vectorized operations for better performance
        times = df[time_col].astype(str).tolist()
        values = df[value_col].astype(float).tolist()

        return [HistogramData(time=time, value=value) for time, value in zip(times, values)]

    def _get_options_dict(self) -> Dict[str, Any]:
        """Get options dictionary for histogram series."""
        options = self._base_dict()

        # Add histogram-specific options
        options.update(
            {
                "color": self.color,
                "base": self.base,
            }
        )

        return options
