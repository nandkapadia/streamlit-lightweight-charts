"""Price-Volume composite chart."""

from typing import Optional, List, Union
import pandas as pd
from .chart import Chart, MultiPaneChart
from .specialized_charts import (
    CandlestickChart, LineChart, AreaChart,
    BarChart, HistogramChart
)
from .options import ChartOptions, LayoutOptions, PriceScaleMargins
from .series import (
    CandlestickSeriesOptions, HistogramSeriesOptions,
    LineSeriesOptions, AreaSeriesOptions, BarSeriesOptions
)
from ..data import Marker
from ..utils import (
    df_to_ohlc_data, df_to_histogram_data,
    df_to_line_data
)


class PriceVolumeChart(MultiPaneChart):
    """
    Composite chart with price chart on top and volume histogram below.
    
    This is the most common chart type for financial data, combining
    price action with volume information.
    """
    
    def __init__(
        self,
        df: pd.DataFrame,
        price_type: str = 'candlestick',
        price_height: int = 400,
        volume_height: int = 100,
        price_options: Optional[ChartOptions] = None,
        volume_options: Optional[ChartOptions] = None,
        price_series_options: Optional[Union[CandlestickSeriesOptions, LineSeriesOptions, AreaSeriesOptions, BarSeriesOptions]] = None,
        volume_series_options: Optional[HistogramSeriesOptions] = None,
        price_column: str = 'close',
        volume_column: str = 'volume',
        time_column: Optional[str] = None,
        sync_crosshair: bool = True
    ):
        """
        Initialize a price-volume composite chart.
        
        Args:
            df: DataFrame with OHLC and volume data
            price_type: Type of price chart ('candlestick', 'line', 'area', 'bar')
            price_height: Height of price chart
            volume_height: Height of volume chart
            price_options: Options for price chart
            volume_options: Options for volume chart
            price_series_options: Series options for price chart
            volume_series_options: Series options for volume chart
            price_column: Column name for price (used if price_type is 'line' or 'area')
            volume_column: Column name for volume
            time_column: Column name for time (if None, uses index)
            sync_crosshair: Whether to synchronize crosshairs between charts
        """
        # Create price chart based on type
        if price_type == 'candlestick':
            price_chart = self._create_candlestick_chart(
                df, price_height, price_options, price_series_options, time_column
            )
        elif price_type == 'line':
            price_chart = self._create_line_chart(
                df, price_column, price_height, price_options, price_series_options, time_column
            )
        elif price_type == 'area':
            price_chart = self._create_area_chart(
                df, price_column, price_height, price_options, price_series_options, time_column
            )
        elif price_type == 'bar':
            price_chart = self._create_bar_chart(
                df, price_height, price_options, price_series_options, time_column
            )
        else:
            raise ValueError(f"Unknown price type: {price_type}")
        
        # Create volume chart
        volume_chart = self._create_volume_chart(
            df, volume_column, volume_height, volume_options, volume_series_options, time_column
        )
        
        # Set up crosshair sync if enabled
        if sync_crosshair:
            self._setup_crosshair_sync(price_chart, volume_chart)
        
        # Initialize parent with both charts
        super().__init__([price_chart, volume_chart])
        
        # Store references for convenience
        self.price_chart = price_chart
        self.volume_chart = volume_chart
    
    def _create_candlestick_chart(
        self,
        df: pd.DataFrame,
        height: int,
        options: Optional[ChartOptions],
        series_options: Optional[CandlestickSeriesOptions],
        time_column: Optional[str]
    ) -> CandlestickChart:
        """Create candlestick price chart."""
        data = df_to_ohlc_data(df, time_column=time_column)
        
        chart_options = options or ChartOptions(height=height)
        chart_options.height = height
        
        return CandlestickChart(
            data=data,
            options=chart_options,
            series_options=series_options or CandlestickSeriesOptions(
                up_color='#26a69a',
                down_color='#ef5350'
            )
        )
    
    def _create_line_chart(
        self,
        df: pd.DataFrame,
        price_column: str,
        height: int,
        options: Optional[ChartOptions],
        series_options: Optional[LineSeriesOptions],
        time_column: Optional[str]
    ) -> LineChart:
        """Create line price chart."""
        data = df_to_line_data(df, value_column=price_column, time_column=time_column)
        
        chart_options = options or ChartOptions(height=height)
        chart_options.height = height
        
        return LineChart(
            data=data,
            options=chart_options,
            series_options=series_options or LineSeriesOptions(
                color='#2196F3',
                line_width=2
            )
        )
    
    def _create_area_chart(
        self,
        df: pd.DataFrame,
        price_column: str,
        height: int,
        options: Optional[ChartOptions],
        series_options: Optional[AreaSeriesOptions],
        time_column: Optional[str]
    ) -> AreaChart:
        """Create area price chart."""
        data = df_to_line_data(df, value_column=price_column, time_column=time_column)
        
        chart_options = options or ChartOptions(height=height)
        chart_options.height = height
        
        return AreaChart(
            data=data,
            options=chart_options,
            series_options=series_options or AreaSeriesOptions(
                top_color='rgba(33, 150, 243, 0.56)',
                bottom_color='rgba(33, 150, 243, 0.04)',
                line_color='#2196F3'
            )
        )
    
    def _create_bar_chart(
        self,
        df: pd.DataFrame,
        height: int,
        options: Optional[ChartOptions],
        series_options: Optional[BarSeriesOptions],
        time_column: Optional[str]
    ) -> BarChart:
        """Create bar price chart."""
        data = df_to_ohlc_data(df, time_column=time_column)
        
        chart_options = options or ChartOptions(height=height)
        chart_options.height = height
        
        return BarChart(
            data=data,
            options=chart_options,
            series_options=series_options
        )
    
    def _create_volume_chart(
        self,
        df: pd.DataFrame,
        volume_column: str,
        height: int,
        options: Optional[ChartOptions],
        series_options: Optional[HistogramSeriesOptions],
        time_column: Optional[str]
    ) -> HistogramChart:
        """Create volume histogram chart."""
        # Determine colors based on price movement
        if 'close' in df.columns and 'open' in df.columns:
            # Color based on whether close > open
            df['volume_color'] = df.apply(
                lambda row: '#26a69a' if row['close'] >= row['open'] else '#ef5350',
                axis=1
            )
            data = df_to_histogram_data(
                df,
                value_column=volume_column,
                color_column='volume_color',
                time_column=time_column
            )
        else:
            # Default coloring
            data = df_to_histogram_data(
                df,
                value_column=volume_column,
                time_column=time_column
            )
        
        # Create volume chart options
        chart_options = options or ChartOptions(height=height)
        chart_options.height = height
        
        # Adjust margins for volume chart
        if chart_options.right_price_scale is None:
            from .options import PriceScaleOptions
            chart_options.right_price_scale = PriceScaleOptions()
        
        chart_options.right_price_scale.scale_margins = PriceScaleMargins(
            top=0.1,
            bottom=0
        )
        
        # Hide time scale for volume chart (shown on price chart)
        chart_options.time_scale.visible = False
        
        return HistogramChart(
            data=data,
            options=chart_options,
            series_options=series_options or HistogramSeriesOptions()
        )
    
    def _setup_crosshair_sync(self, price_chart: Chart, volume_chart: Chart):
        """Set up crosshair synchronization between charts."""
        # Ensure both charts have the same crosshair mode
        from ..types import CrosshairMode
        price_chart.options.crosshair.mode = CrosshairMode.NORMAL
        volume_chart.options.crosshair.mode = CrosshairMode.NORMAL
    
    def add_price_indicator(
        self,
        indicator_data: List,
        options: Optional[LineSeriesOptions] = None,
        markers: Optional[List[Marker]] = None
    ) -> 'PriceVolumeChart':
        """
        Add an indicator to the price chart.
        
        Args:
            indicator_data: Indicator data points
            options: Line series options for the indicator
            markers: Optional markers
            
        Returns:
            Self for method chaining
        """
        if isinstance(self.price_chart, LineChart):
            self.price_chart.add_line(
                data=indicator_data,
                options=options,
                markers=markers
            )
        else:
            # For non-line charts, add as overlay
            from .series import LineSeries
            series = LineSeries(
                data=indicator_data,
                options=options or LineSeriesOptions(),
                markers=markers
            )
            self.price_chart.add_series(series)
        
        return self
    
    def add_trades(
        self,
        trades: List['Trade'],
        visualization_options: Optional['TradeVisualizationOptions'] = None
    ) -> 'PriceVolumeChart':
        """
        Add trades to the price chart (only works with CandlestickChart).
        
        Args:
            trades: List of trades to add
            visualization_options: Options for visualizing trades
            
        Returns:
            Self for method chaining
        """
        if hasattr(self.price_chart, 'add_trades'):
            self.price_chart.add_trades(trades, visualization_options)
        else:
            raise TypeError(
                f"Trade visualization is only supported for CandlestickChart price type, "
                f"not {type(self.price_chart).__name__}"
            )
        
        return self