"""BarChart specialized chart class."""

from typing import List, Optional

from ..data import Marker, OhlcData
from .chart import Chart
from .options import ChartOptions
from .series import BarSeries, BarSeriesOptions


class BarChart(Chart):
    """
    Specialized chart for bar data.

    Validates OHLC data and provides bar-specific methods.
    """

    def __init__(
        self,
        data: List[OhlcData],
        options: Optional[ChartOptions] = None,
        series_options: Optional[BarSeriesOptions] = None,
        markers: Optional[List[Marker]] = None,
    ):
        """
        Initialize bar chart.

        Args:
            data: List of OHLC data points
            options: Chart options
            series_options: Bar series options
            markers: Optional list of markers
        """
        # Validate data type
        if not all(isinstance(d, OhlcData) for d in data):
            raise TypeError(
                "BarChart requires List[OhlcData]. "
                "Use df_to_ohlc_data() to convert from DataFrame."
            )

        series = BarSeries(data=data, options=series_options or BarSeriesOptions(), markers=markers)

        super().__init__(series=[series], options=options)

        # Store reference to main series
        self.bar_series = series
