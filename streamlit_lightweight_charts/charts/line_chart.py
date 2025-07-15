"""LineChart specialized chart class."""

from typing import List, Optional

from ..data import Marker, SingleValueData
from .chart import Chart
from .options import ChartOptions
from .series import LineSeries, LineSeriesOptions


class LineChart(Chart):
    """
    Specialized chart for line data.

    Validates single value data and provides line-specific methods.
    """

    def __init__(
        self,
        data: List[SingleValueData],
        options: Optional[ChartOptions] = None,
        series_options: Optional[LineSeriesOptions] = None,
        markers: Optional[List[Marker]] = None,
    ):
        """
        Initialize line chart.

        Args:
            data: List of single value data points
            options: Chart options
            series_options: Line series options
            markers: Optional list of markers
        """
        # Validate data type
        if not all(isinstance(d, SingleValueData) for d in data):
            raise TypeError(
                "LineChart requires List[SingleValueData]. "
                "Use df_to_line_data() to convert from DataFrame."
            )

        series = LineSeries(
            data=data, options=series_options or LineSeriesOptions(), markers=markers
        )

        super().__init__(series=[series], options=options)

        # Store reference to main series
        self.line_series = series

    def add_line(
        self,
        data: List[SingleValueData],
        options: Optional[LineSeriesOptions] = None,
        markers: Optional[List[Marker]] = None,
    ) -> "LineChart":
        """
        Add another line to the chart.

        Args:
            data: Line data points
            options: Line series options
            markers: Optional markers

        Returns:
            Self for method chaining
        """
        series = LineSeries(data=data, options=options or LineSeriesOptions(), markers=markers)
        self.add_series(series)
        return self
