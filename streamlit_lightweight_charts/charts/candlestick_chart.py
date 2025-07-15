"""
CandlestickChart specialized chart class.

This module provides a specialized chart class for creating candlestick charts,
which are commonly used in financial analysis to display price movements over time.
The CandlestickChart class includes built-in support for trade visualization,
technical indicators, and candlestick-specific features.
"""

from typing import List, Optional

from ..data import (
    Annotation,
    Marker,
    OhlcData,
    SingleValueData,
    Trade,
    TradeVisualizationOptions,
)
from .chart import Chart
from .options import ChartOptions
from .series import (
    CandlestickSeries,
    CandlestickSeriesOptions,
    LineSeries,
    LineSeriesOptions,
)


class CandlestickChart(Chart):
    """
    Specialized chart for candlestick data with enhanced trading features.

    This class extends the base Chart class to provide candlestick-specific
    functionality, including trade visualization, technical indicators, and
    OHLC data validation. It's designed for financial analysis and trading
    applications.

    The CandlestickChart automatically validates that input data is in OHLC
    format and provides convenient methods for adding trades, indicators,
    and other trading-related features.

    Attributes:
        candlestick_series: The main candlestick series containing price data.
        _trades: Internal list of trades for visualization.
        _trade_options: Options for trade visualization styling.
    """

    def __init__(
        self,
        data: List[OhlcData],
        options: Optional[ChartOptions] = None,
        series_options: Optional[CandlestickSeriesOptions] = None,
        markers: Optional[List[Marker]] = None,
        trades: Optional[List[Trade]] = None,
        trade_visualization_options: Optional[TradeVisualizationOptions] = None,
        annotations: Optional[List["Annotation"]] = None,
    ):
        """
        Initialize a candlestick chart with OHLC data and optional features.

        Args:
            data: List of OHLC data points. Each point must contain open, high,
                low, and close prices for a specific time period.
            options: Chart configuration options. If None, default options will be used.
            series_options: Candlestick series specific options. If None, default
                candlestick options will be used.
            markers: Optional list of markers to display on the chart for highlighting
                specific data points or events.
            trades: Optional list of trades to visualize on the chart. These will be
                displayed as buy/sell markers with customizable styling.
            trade_visualization_options: Options for styling trade visualizations.
                Controls colors, shapes, and other visual aspects of trade markers.
            annotations: Optional list of annotations to add to the chart.

        Raises:
            TypeError: If any data point is not an OhlcData instance.

        Example:
            ```python
            # Create basic candlestick chart
            ohlc_data = [
                OhlcData("2024-01-01", 100, 105, 98, 102),
                OhlcData("2024-01-02", 102, 108, 101, 106),
                OhlcData("2024-01-03", 106, 110, 104, 108)
            ]
            chart = CandlestickChart(data=ohlc_data)

            # Create chart with trades and custom options
            trades = [Trade("2024-01-02", 102, TradeType.BUY)]
            chart = CandlestickChart(
                data=ohlc_data,
                trades=trades,
                trade_visualization_options=TradeVisualizationOptions()
            )
            ```
        """
        # Validate that all data points are OHLC format
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
            trade_visualization_options=trade_visualization_options,
        )

        # Initialize the base chart with the candlestick series
        super().__init__(series=[series], options=options, annotations=annotations)

        # Store references for easy access and modification
        self.candlestick_series = series
        self._trades = trades
        self._trade_options = trade_visualization_options

    def add_trades(
        self,
        trades: List[Trade],
        visualization_options: Optional[TradeVisualizationOptions] = None,
    ) -> "CandlestickChart":
        """
        Add multiple trades to the chart for visualization.

        This method allows adding multiple trades at once, which will be
        displayed as buy/sell markers on the chart with customizable styling.

        Args:
            trades: List of Trade objects to add to the chart. Each trade should
                have a timestamp, price, and trade type (buy/sell).
            visualization_options: Options for styling the trade visualizations.
                If None, existing options will be preserved.

        Returns:
            Self for method chaining.

        Example:
            ```python
            trades = [
                Trade("2024-01-02", 102, TradeType.BUY),
                Trade("2024-01-03", 108, TradeType.SELL)
            ]
            chart.add_trades(trades)
            ```
        """
        # Initialize trades list if it doesn't exist
        if self._trades is None:
            self._trades = []
        self._trades.extend(trades)

        # Update visualization options if provided
        if visualization_options is not None:
            self._trade_options = visualization_options

        # Update the series with new trades and options
        self.candlestick_series.trades = self._trades
        self.candlestick_series.trade_visualization_options = self._trade_options

        return self

    def add_trade(
        self,
        trade: Trade,
        visualization_options: Optional[TradeVisualizationOptions] = None,
    ) -> "CandlestickChart":
        """
        Add a single trade to the chart for visualization.

        Convenience method for adding a single trade. Delegates to add_trades()
        for consistency.

        Args:
            trade: Trade object to add to the chart.
            visualization_options: Options for styling the trade visualization.
                If None, existing options will be preserved.

        Returns:
            Self for method chaining.

        Example:
            ```python
            trade = Trade("2024-01-02", 102, TradeType.BUY)
            chart.add_trade(trade)
            ```
        """
        return self.add_trades([trade], visualization_options)

    def clear_trades(self) -> "CandlestickChart":
        """
        Clear all trades from the chart.

        This method removes all trade visualizations from the chart,
        leaving only the candlestick data.

        Returns:
            Self for method chaining.

        Example:
            ```python
            chart.clear_trades()
            ```
        """
        self._trades = []
        self.candlestick_series.trades = []
        return self

    def set_trade_visualization(self, options: TradeVisualizationOptions) -> "CandlestickChart":
        """
        Set trade visualization options for styling.

        This method allows updating the visual appearance of trade markers
        without changing the trade data itself.

        Args:
            options: Trade visualization options containing styling preferences
                for buy/sell markers, colors, shapes, etc.

        Returns:
            Self for method chaining.

        Example:
            ```python
            options = TradeVisualizationOptions(
                buy_color="#26a69a",
                sell_color="#ef5350",
                marker_size=8
            )
            chart.set_trade_visualization(options)
            ```
        """
        self._trade_options = options
        self.candlestick_series.trade_visualization_options = options
        return self

    def add_indicator(
        self,
        data: List[SingleValueData],
        options: Optional[LineSeriesOptions] = None,
        markers: Optional[List[Marker]] = None,
    ) -> "CandlestickChart":
        """
        Add a technical indicator as a line series overlay.

        This method allows adding technical indicators (like moving averages,
        RSI, MACD, etc.) as line series that overlay on the candlestick chart.
        The indicator will be synchronized with the main price data.

        Args:
            data: List of SingleValueData points representing the indicator values.
                Each point should have a time and value.
            options: Line series options for styling the indicator line.
                If None, default line options will be used.
            markers: Optional markers to display on the indicator line
                for highlighting specific points.

        Returns:
            Self for method chaining.

        Example:
            ```python
            # Add a 20-period moving average
            ma_data = [
                SingleValueData("2024-01-01", 101.5),
                SingleValueData("2024-01-02", 102.3),
                SingleValueData("2024-01-03", 103.1)
            ]
            ma_options = LineSeriesOptions(color="#FF6B6B", line_width=2)
            chart.add_indicator(ma_data, options=ma_options)
            ```
        """
        # Create a line series for the indicator
        series = LineSeries(data=data, options=options or LineSeriesOptions(), markers=markers)
        # Add the indicator series to the chart
        self.add_series(series)
        return self
