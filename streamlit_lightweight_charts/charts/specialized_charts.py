"""Specialized chart classes for different chart types."""

from typing import List, Optional, Union
from .chart import Chart
from .options import ChartOptions
from .series import (
    LineSeries, AreaSeries, BarSeries, CandlestickSeries,
    HistogramSeries, BaselineSeries,
    LineSeriesOptions, AreaSeriesOptions, BarSeriesOptions,
    CandlestickSeriesOptions, HistogramSeriesOptions, BaselineSeriesOptions
)
from ..data import (
    SingleValueData, OhlcData, HistogramData, BaselineData, Marker
)


class CandlestickChart(Chart):
    """Specialized chart for candlestick data with OHLC validation."""
    
    def __init__(
        self,
        data: List[OhlcData],
        options: Optional[ChartOptions] = None,
        series_options: Optional[CandlestickSeriesOptions] = None,
        markers: Optional[List[Marker]] = None
    ):
        """
        Initialize a candlestick chart.
        
        Args:
            data: List of OHLC data points
            options: Chart configuration options
            series_options: Candlestick series specific options
            markers: Optional list of markers
            
        Raises:
            TypeError: If data is not List[OhlcData]
            ValueError: If data is empty
        """
        # Validate data
        if not isinstance(data, list):
            raise TypeError("Data must be a list of OhlcData")
        
        if not data:
            raise ValueError("Data list cannot be empty")
        
        if not all(isinstance(item, OhlcData) for item in data):
            raise TypeError("All data items must be OhlcData instances")
        
        # Create candlestick series
        series = CandlestickSeries(
            data=data,
            options=series_options or CandlestickSeriesOptions(),
            markers=markers
        )
        
        # Initialize parent Chart
        super().__init__(series=series, options=options)
    
    def update_data(self, data: List[OhlcData]) -> 'CandlestickChart':
        """
        Update chart data with validation.
        
        Args:
            data: New OHLC data
            
        Returns:
            Self for method chaining
        """
        if not all(isinstance(item, OhlcData) for item in data):
            raise TypeError("All data items must be OhlcData instances")
        
        self.series[0].data = data
        return self


class LineChart(Chart):
    """Specialized chart for line data."""
    
    def __init__(
        self,
        data: List[SingleValueData],
        options: Optional[ChartOptions] = None,
        series_options: Optional[LineSeriesOptions] = None,
        markers: Optional[List[Marker]] = None
    ):
        """
        Initialize a line chart.
        
        Args:
            data: List of single value data points
            options: Chart configuration options
            series_options: Line series specific options
            markers: Optional list of markers
            
        Raises:
            TypeError: If data is not List[SingleValueData]
            ValueError: If data is empty
        """
        # Validate data
        if not isinstance(data, list):
            raise TypeError("Data must be a list of SingleValueData")
        
        if not data:
            raise ValueError("Data list cannot be empty")
        
        if not all(isinstance(item, SingleValueData) for item in data):
            raise TypeError("All data items must be SingleValueData instances")
        
        # Create line series
        series = LineSeries(
            data=data,
            options=series_options or LineSeriesOptions(),
            markers=markers
        )
        
        # Initialize parent Chart
        super().__init__(series=series, options=options)
    
    def add_line(
        self,
        data: List[SingleValueData],
        options: Optional[LineSeriesOptions] = None,
        markers: Optional[List[Marker]] = None
    ) -> 'LineChart':
        """
        Add another line series to the chart.
        
        Args:
            data: List of single value data points
            options: Line series specific options
            markers: Optional list of markers
            
        Returns:
            Self for method chaining
        """
        if not all(isinstance(item, SingleValueData) for item in data):
            raise TypeError("All data items must be SingleValueData instances")
        
        series = LineSeries(
            data=data,
            options=options or LineSeriesOptions(),
            markers=markers
        )
        self.add_series(series)
        return self


class AreaChart(Chart):
    """Specialized chart for area data."""
    
    def __init__(
        self,
        data: List[SingleValueData],
        options: Optional[ChartOptions] = None,
        series_options: Optional[AreaSeriesOptions] = None,
        markers: Optional[List[Marker]] = None
    ):
        """
        Initialize an area chart.
        
        Args:
            data: List of single value data points
            options: Chart configuration options
            series_options: Area series specific options
            markers: Optional list of markers
            
        Raises:
            TypeError: If data is not List[SingleValueData]
            ValueError: If data is empty
        """
        # Validate data
        if not isinstance(data, list):
            raise TypeError("Data must be a list of SingleValueData")
        
        if not data:
            raise ValueError("Data list cannot be empty")
        
        if not all(isinstance(item, SingleValueData) for item in data):
            raise TypeError("All data items must be SingleValueData instances")
        
        # Create area series
        series = AreaSeries(
            data=data,
            options=series_options or AreaSeriesOptions(),
            markers=markers
        )
        
        # Initialize parent Chart
        super().__init__(series=series, options=options)


class BarChart(Chart):
    """Specialized chart for bar data (OHLC bars)."""
    
    def __init__(
        self,
        data: List[OhlcData],
        options: Optional[ChartOptions] = None,
        series_options: Optional[BarSeriesOptions] = None,
        markers: Optional[List[Marker]] = None
    ):
        """
        Initialize a bar chart.
        
        Args:
            data: List of OHLC data points
            options: Chart configuration options
            series_options: Bar series specific options
            markers: Optional list of markers
            
        Raises:
            TypeError: If data is not List[OhlcData]
            ValueError: If data is empty
        """
        # Validate data
        if not isinstance(data, list):
            raise TypeError("Data must be a list of OhlcData")
        
        if not data:
            raise ValueError("Data list cannot be empty")
        
        if not all(isinstance(item, OhlcData) for item in data):
            raise TypeError("All data items must be OhlcData instances")
        
        # Create bar series
        series = BarSeries(
            data=data,
            options=series_options or BarSeriesOptions(),
            markers=markers
        )
        
        # Initialize parent Chart
        super().__init__(series=series, options=options)


class HistogramChart(Chart):
    """Specialized chart for histogram data."""
    
    def __init__(
        self,
        data: List[HistogramData],
        options: Optional[ChartOptions] = None,
        series_options: Optional[HistogramSeriesOptions] = None,
        markers: Optional[List[Marker]] = None
    ):
        """
        Initialize a histogram chart.
        
        Args:
            data: List of histogram data points
            options: Chart configuration options
            series_options: Histogram series specific options
            markers: Optional list of markers
            
        Raises:
            TypeError: If data is not List[HistogramData]
            ValueError: If data is empty
        """
        # Validate data
        if not isinstance(data, list):
            raise TypeError("Data must be a list of HistogramData")
        
        if not data:
            raise ValueError("Data list cannot be empty")
        
        if not all(isinstance(item, HistogramData) for item in data):
            raise TypeError("All data items must be HistogramData instances")
        
        # Create histogram series
        series = HistogramSeries(
            data=data,
            options=series_options or HistogramSeriesOptions(),
            markers=markers
        )
        
        # Initialize parent Chart
        super().__init__(series=series, options=options)


class BaselineChart(Chart):
    """Specialized chart for baseline data."""
    
    def __init__(
        self,
        data: List[BaselineData],
        options: Optional[ChartOptions] = None,
        series_options: Optional[BaselineSeriesOptions] = None,
        markers: Optional[List[Marker]] = None,
        base_value: Optional[float] = None
    ):
        """
        Initialize a baseline chart.
        
        Args:
            data: List of baseline data points
            options: Chart configuration options
            series_options: Baseline series specific options
            markers: Optional list of markers
            base_value: Optional base value for the baseline
            
        Raises:
            TypeError: If data is not List[BaselineData]
            ValueError: If data is empty
        """
        # Validate data
        if not isinstance(data, list):
            raise TypeError("Data must be a list of BaselineData")
        
        if not data:
            raise ValueError("Data list cannot be empty")
        
        if not all(isinstance(item, BaselineData) for item in data):
            raise TypeError("All data items must be BaselineData instances")
        
        # Set base value if provided
        if series_options is None:
            series_options = BaselineSeriesOptions()
        
        if base_value is not None:
            series_options.base_value = {'type': 'price', 'price': base_value}
        
        # Create baseline series
        series = BaselineSeries(
            data=data,
            options=series_options,
            markers=markers
        )
        
        # Initialize parent Chart
        super().__init__(series=series, options=options)