"""BaselineChart specialized chart class."""

from typing import List, Optional

from ..data import BaselineData, Marker
from .chart import Chart
from .options import ChartOptions
from .series import BaselineSeries, BaselineSeriesOptions


class BaselineChart(Chart):
    """
    Specialized chart for baseline data.

    Validates baseline data and provides baseline-specific methods.
    """

    def __init__(
        self,
        data: List[BaselineData],
        options: Optional[ChartOptions] = None,
        series_options: Optional[BaselineSeriesOptions] = None,
        markers: Optional[List[Marker]] = None,
    ):
        """
        Initialize baseline chart.

        Args:
            data: List of baseline data points
            options: Chart options
            series_options: Baseline series options
            markers: Optional list of markers
        """
        # Validate data type
        if not all(isinstance(d, BaselineData) for d in data):
            raise TypeError(
                "BaselineChart requires List[BaselineData]. "
                "Use df_to_baseline_data() to convert from DataFrame."
            )

        series = BaselineSeries(
            data=data,
            options=series_options or BaselineSeriesOptions(),
            markers=markers,
        )

        super().__init__(series=[series], options=options)

        # Store reference to main series
        self.baseline_series = series
