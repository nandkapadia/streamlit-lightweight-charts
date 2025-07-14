"""HistogramChart specialized chart class."""

from typing import List, Optional
from .chart import Chart
from .series import HistogramSeries, HistogramSeriesOptions
from .options import ChartOptions
from ..data import HistogramData


class HistogramChart(Chart):
    """
    Specialized chart for histogram data.
    
    Validates histogram data and provides histogram-specific methods.
    """
    
    def __init__(
        self,
        data: List[HistogramData],
        options: Optional[ChartOptions] = None,
        series_options: Optional[HistogramSeriesOptions] = None
    ):
        """
        Initialize histogram chart.
        
        Args:
            data: List of histogram data points
            options: Chart options
            series_options: Histogram series options
        """
        # Validate data type
        if not all(isinstance(d, HistogramData) for d in data):
            raise TypeError(
                "HistogramChart requires List[HistogramData]. "
                "Use df_to_histogram_data() to convert from DataFrame."
            )
        
        series = HistogramSeries(
            data=data,
            options=series_options or HistogramSeriesOptions()
        )
        
        super().__init__(series=[series], options=options)
        
        # Store reference to main series
        self.histogram_series = series