"""Specialized chart classes for specific data types."""

from typing import List, Optional, Union
from .chart import Chart
from .series import (
    CandlestickSeries, LineSeries, AreaSeries,
    BarSeries, HistogramSeries, BaselineSeries,
    CandlestickSeriesOptions, LineSeriesOptions, AreaSeriesOptions,
    BarSeriesOptions, HistogramSeriesOptions, BaselineSeriesOptions
)
from .options import ChartOptions
from ..data import (
    OhlcData, SingleValueData, HistogramData, BaselineData,
    Marker, Trade, TradeVisualizationOptions
)


class CandlestickChart(Chart):
    """
    Specialized chart for candlestick data.
    
    Validates that data is OHLC format and provides candlestick-specific methods.
    """
    
    def __init__(
        self,
        data: List[OhlcData],
        options: Optional[ChartOptions] = None,
        series_options: Optional[CandlestickSeriesOptions] = None,
        markers: Optional[List[Marker]] = None,
        trades: Optional[List[Trade]] = None,
        trade_visualization_options: Optional[TradeVisualizationOptions] = None
    ):
        """
        Initialize candlestick chart.
        
        Args:
            data: List of OHLC data points
            options: Chart options
            series_options: Candlestick series options
            markers: Optional list of markers
            trades: Optional list of trades to visualize
            trade_visualization_options: Options for trade visualization
        """
        # Validate data type
        if not all(isinstance(d, OhlcData) for d in data):
            raise TypeError(
                "CandlestickChart requires List[OhlcData]. "
                "Use df_to_ohlc_data() to convert from DataFrame."
            )
        
        # Create candlestick series with trades if provided
        series = CandlestickSeries(
            data=data,
            options=series_options or CandlestickSeriesOptions(),
            markers=markers,
            trades=trades,
            trade_visualization_options=trade_visualization_options
        )
        
        super().__init__(series=[series], options=options)
        
        # Store reference to main series and trades
        self.candlestick_series = series
        self._trades = trades
        self._trade_options = trade_visualization_options
    
    def add_trades(
        self,
        trades: List[Trade],
        visualization_options: Optional[TradeVisualizationOptions] = None
    ) -> 'CandlestickChart':
        """
        Add trades to the chart.
        
        Args:
            trades: List of trades to add
            visualization_options: Options for visualizing trades
            
        Returns:
            Self for method chaining
        """
        if self._trades is None:
            self._trades = []
        self._trades.extend(trades)
        
        # Update visualization options if provided
        if visualization_options is not None:
            self._trade_options = visualization_options
        
        # Update the series with new trades
        self.candlestick_series.trades = self._trades
        self.candlestick_series.trade_visualization_options = self._trade_options
        
        return self
    
    def add_trade(
        self,
        trade: Trade,
        visualization_options: Optional[TradeVisualizationOptions] = None
    ) -> 'CandlestickChart':
        """
        Add a single trade to the chart.
        
        Args:
            trade: Trade to add
            visualization_options: Options for visualizing trades
            
        Returns:
            Self for method chaining
        """
        return self.add_trades([trade], visualization_options)
    
    def clear_trades(self) -> 'CandlestickChart':
        """
        Clear all trades from the chart.
        
        Returns:
            Self for method chaining
        """
        self._trades = []
        self.candlestick_series.trades = []
        return self
    
    def set_trade_visualization(
        self,
        options: TradeVisualizationOptions
    ) -> 'CandlestickChart':
        """
        Set trade visualization options.
        
        Args:
            options: Trade visualization options
            
        Returns:
            Self for method chaining
        """
        self._trade_options = options
        self.candlestick_series.trade_visualization_options = options
        return self
    
    def add_indicator(
        self,
        data: List[SingleValueData],
        options: Optional[LineSeriesOptions] = None,
        markers: Optional[List[Marker]] = None
    ) -> 'CandlestickChart':
        """
        Add a technical indicator as a line series.
        
        Args:
            data: Indicator data points
            options: Line series options
            markers: Optional markers for the indicator
            
        Returns:
            Self for method chaining
        """
        series = LineSeries(
            data=data,
            options=options or LineSeriesOptions(),
            markers=markers
        )
        self.add_series(series)
        return self


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
        markers: Optional[List[Marker]] = None
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
            data=data,
            options=series_options or LineSeriesOptions(),
            markers=markers
        )
        
        super().__init__(series=[series], options=options)
        
        # Store reference to main series
        self.line_series = series
    
    def add_line(
        self,
        data: List[SingleValueData],
        options: Optional[LineSeriesOptions] = None,
        markers: Optional[List[Marker]] = None
    ) -> 'LineChart':
        """
        Add another line to the chart.
        
        Args:
            data: Line data points
            options: Line series options
            markers: Optional markers
            
        Returns:
            Self for method chaining
        """
        series = LineSeries(
            data=data,
            options=options or LineSeriesOptions(),
            markers=markers
        )
        self.add_series(series)
        return self


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
        markers: Optional[List[Marker]] = None
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
            data=data,
            options=series_options or AreaSeriesOptions(),
            markers=markers
        )
        
        super().__init__(series=[series], options=options)
        
        # Store reference to main series
        self.area_series = series


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
        markers: Optional[List[Marker]] = None
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
        
        series = BarSeries(
            data=data,
            options=series_options or BarSeriesOptions(),
            markers=markers
        )
        
        super().__init__(series=[series], options=options)
        
        # Store reference to main series
        self.bar_series = series


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
        markers: Optional[List[Marker]] = None
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
            markers=markers
        )
        
        super().__init__(series=[series], options=options)
        
        # Store reference to main series
        self.baseline_series = series