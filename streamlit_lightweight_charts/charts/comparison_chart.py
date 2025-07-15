"""Comparison chart for multiple instruments."""

from typing import List, Optional, Tuple

import pandas as pd

from ..utils import df_to_line_data
from .chart import Chart
from .options import ChartOptions
from .series import LineSeries, LineSeriesOptions


class ComparisonChart(Chart):
    """
    Chart for comparing multiple instruments.

    Normalizes multiple series to percentage change for easy comparison.
    """

    def __init__(
        self,
        dataframes: List[Tuple[str, pd.DataFrame]],
        value_column: str = "close",
        normalize: bool = True,
        chart_options: Optional[ChartOptions] = None,
        colors: Optional[List[str]] = None,
        time_column: Optional[str] = None,
    ):
        """
        Initialize comparison chart.

        Args:
            dataframes: List of (name, DataFrame) tuples
            value_column: Column to compare
            normalize: Whether to normalize to percentage change
            chart_options: Chart options
            colors: Colors for each series
            time_column: Time column (if None, uses index)
        """
        # Default colors
        if colors is None:
            default_colors = [
                "#2196F3",
                "#FF9800",
                "#4CAF50",
                "#F44336",
                "#9C27B0",
                "#00BCD4",
                "#FFEB3B",
                "#795548",
            ]
            colors = default_colors[: len(dataframes)]

        series_list = []

        for (name, df), color in zip(dataframes, colors):
            # Normalize if requested
            if normalize:
                # Calculate percentage change from first value
                values = df[value_column]
                first_value = values.iloc[0]
                df[f"{value_column}_normalized"] = ((values / first_value) - 1) * 100
                data_column = f"{value_column}_normalized"
            else:
                data_column = value_column

            # Convert to line data
            data = df_to_line_data(df, value_column=data_column, time_column=time_column)

            # Create series
            series = LineSeries(data=data, options=LineSeriesOptions(color=color, line_width=2))
            series_list.append(series)

        # Update chart options for percentage display if normalized
        if normalize:
            if chart_options is None:
                chart_options = ChartOptions()

            # Set price scale to show percentage
            from ..type_definitions import PriceScaleMode

            chart_options.right_price_scale.mode = PriceScaleMode.PERCENTAGE

        # Initialize parent chart
        super().__init__(series=series_list, options=chart_options)

        # Store metadata
        self.series_names = [name for name, _ in dataframes]
        self.normalized = normalize
