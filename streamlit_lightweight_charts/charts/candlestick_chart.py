"""CandlestickChart specialized chart class."""

from typing import List, Optional
from .chart import Chart
from .series import (
    CandlestickSeries, LineSeries,
    CandlestickSeriesOptions, LineSeriesOptions
)
from .options import ChartOptions
from ..data import (
    OhlcData, SingleValueData, Marker, Trade, TradeVisualizationOptions, Annotation
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
        trade_visualization_options: Optional[TradeVisualizationOptions] = None,
        annotations: Optional[List['Annotation']] = None
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
            annotations: Optional list of annotations
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
        
        super().__init__(series=[series], options=options, annotations=annotations)
        
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