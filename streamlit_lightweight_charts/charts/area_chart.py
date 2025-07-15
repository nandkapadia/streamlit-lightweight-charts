"""AreaChart specialized chart class."""

from typing import List, Optional

from ..data import Marker, SingleValueData
from .chart import Chart
from .options import ChartOptions
from .series import AreaSeries, AreaSeriesOptions


class AreaChart(Chart):
    """
    Specialized chart for area data.

    Validates single value data and provides area-specific methods.
    """

    def __init__(
        self,
        data: List[SingleValueData],
        options: Optional[ChartOptions] = None,
        series_options: Optional[AreaSeriesOptions] = None,
        markers: Optional[List[Marker]] = None,
    ):
        """
        Initialize area chart.

        Args:
            data: List of single value data points
            options: Chart options
            series_options: Area series options
            markers: Optional list of markers
        """
        # Validate data type
        if not all(isinstance(d, SingleValueData) for d in data):
            raise TypeError(
                "AreaChart requires List[SingleValueData]. "
                "Use df_to_line_data() to convert from DataFrame."
            )

        series = AreaSeries(
            data=data, options=series_options or AreaSeriesOptions(), markers=markers
        )

        super().__init__(series=[series], options=options)

        # Store reference to main series
        self.area_series = series
