"""Composite chart classes for common chart combinations."""

from typing import Optional, List, Tuple, Union
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


class PriceWithMAChart(Chart):
    """
    Price chart with moving averages.
    
    Common setup for technical analysis with price and multiple moving averages.
    """
    
    def __init__(
        self,
        df: pd.DataFrame,
        ma_periods: List[int] = [20, 50, 200],
        price_type: str = 'candlestick',
        price_column: str = 'close',
        chart_options: Optional[ChartOptions] = None,
        price_series_options: Optional[Union[CandlestickSeriesOptions, LineSeriesOptions]] = None,
        ma_colors: Optional[List[str]] = None,
        time_column: Optional[str] = None
    ):
        """
        Initialize price chart with moving averages.
        
        Args:
            df: DataFrame with price data
            ma_periods: List of MA periods to calculate
            price_type: Type of price chart ('candlestick' or 'line')
            price_column: Column to use for MA calculation
            chart_options: Chart options
            price_series_options: Price series options
            ma_colors: Colors for each MA (if None, uses defaults)
            time_column: Time column (if None, uses index)
        """
        # Default MA colors
        if ma_colors is None:
            default_colors = ['#2196F3', '#FF9800', '#4CAF50', '#F44336', '#9C27B0']
            ma_colors = default_colors[:len(ma_periods)]
        
        # Create price series
        if price_type == 'candlestick':
            from .series import CandlestickSeries
            price_data = df_to_ohlc_data(df, time_column=time_column)
            price_series = CandlestickSeries(
                data=price_data,
                options=price_series_options or CandlestickSeriesOptions()
            )
        else:
            from .series import LineSeries
            price_data = df_to_line_data(df, value_column=price_column, time_column=time_column)
            price_series = LineSeries(
                data=price_data,
                options=price_series_options or LineSeriesOptions()
            )
        
        # Initialize with price series
        series_list = [price_series]
        
        # Calculate and add moving averages
        for period, color in zip(ma_periods, ma_colors):
            ma_column = f'MA{period}'
            df[ma_column] = df[price_column].rolling(window=period).mean()
            
            # Convert to line data (skip NaN values)
            ma_data = df_to_line_data(
                df.dropna(subset=[ma_column]),
                value_column=ma_column,
                time_column=time_column
            )
            
            # Create MA series
            from .series import LineSeries
            ma_series = LineSeries(
                data=ma_data,
                options=LineSeriesOptions(
                    color=color,
                    line_width=2
                )
            )
            series_list.append(ma_series)
        
        # Initialize parent chart
        super().__init__(series=series_list, options=chart_options)
        
        # Store references
        self.price_series = price_series
        self.ma_series = series_list[1:]  # All except price


class ComparisonChart(Chart):
    """
    Chart for comparing multiple instruments.
    
    Normalizes multiple series to percentage change for easy comparison.
    """
    
    def __init__(
        self,
        dataframes: List[Tuple[str, pd.DataFrame]],
        value_column: str = 'close',
        normalize: bool = True,
        chart_options: Optional[ChartOptions] = None,
        colors: Optional[List[str]] = None,
        time_column: Optional[str] = None
    ):
        """
        Initialize comparison chart.
        
        Args:
            dataframes: List of (name, DataFrame) tuples
            value_column: Column to compare
            normalize: Whether to normalize to percentage change
            chart_options: Chart options
            colors: Colors for each series
            time_column: Time column (if None, uses index)
        """
        # Default colors
        if colors is None:
            default_colors = [
                '#2196F3', '#FF9800', '#4CAF50', '#F44336',
                '#9C27B0', '#00BCD4', '#FFEB3B', '#795548'
            ]
            colors = default_colors[:len(dataframes)]
        
        series_list = []
        
        for (name, df), color in zip(dataframes, colors):
            # Normalize if requested
            if normalize:
                # Calculate percentage change from first value
                values = df[value_column]
                first_value = values.iloc[0]
                df[f'{value_column}_normalized'] = ((values / first_value) - 1) * 100
                data_column = f'{value_column}_normalized'
            else:
                data_column = value_column
            
            # Convert to line data
            data = df_to_line_data(
                df,
                value_column=data_column,
                time_column=time_column
            )
            
            # Create series
            from .series import LineSeries
            series = LineSeries(
                data=data,
                options=LineSeriesOptions(
                    color=color,
                    line_width=2
                )
            )
            series_list.append(series)
        
        # Update chart options for percentage display if normalized
        if normalize:
            if chart_options is None:
                chart_options = ChartOptions()
            
            # Set price scale to show percentage
            from ..types import PriceScaleMode
            chart_options.right_price_scale.mode = PriceScaleMode.PERCENTAGE
        
        # Initialize parent chart
        super().__init__(series=series_list, options=chart_options)
        
        # Store metadata
        self.series_names = [name for name, _ in dataframes]
        self.normalized = normalize


class BollingerBandsChart(Chart):
    """
    Price chart with Bollinger Bands.
    
    Shows price with upper and lower Bollinger Bands.
    """
    
    def __init__(
        self,
        df: pd.DataFrame,
        period: int = 20,
        std_dev: float = 2.0,
        price_type: str = 'line',
        price_column: str = 'close',
        chart_options: Optional[ChartOptions] = None,
        price_color: str = '#2196F3',
        band_color: str = '#9E9E9E',
        fill_opacity: float = 0.1,
        time_column: Optional[str] = None
    ):
        """
        Initialize Bollinger Bands chart.
        
        Args:
            df: DataFrame with price data
            period: Period for moving average
            std_dev: Number of standard deviations
            price_type: Type of price display ('line' or 'candlestick')
            price_column: Column for calculations
            chart_options: Chart options
            price_color: Color for price line
            band_color: Color for bands
            fill_opacity: Opacity for band fill
            time_column: Time column (if None, uses index)
        """
        # Calculate Bollinger Bands
        df['BB_MA'] = df[price_column].rolling(window=period).mean()
        df['BB_STD'] = df[price_column].rolling(window=period).std()
        df['BB_Upper'] = df['BB_MA'] + (df['BB_STD'] * std_dev)
        df['BB_Lower'] = df['BB_MA'] - (df['BB_STD'] * std_dev)
        
        # Remove NaN values
        df_clean = df.dropna(subset=['BB_MA', 'BB_Upper', 'BB_Lower'])
        
        series_list = []
        
        # Add price series
        if price_type == 'candlestick':
            from .series import CandlestickSeries
            price_data = df_to_ohlc_data(df_clean, time_column=time_column)
            price_series = CandlestickSeries(
                data=price_data,
                options=CandlestickSeriesOptions()
            )
        else:
            from .series import LineSeries
            price_data = df_to_line_data(
                df_clean,
                value_column=price_column,
                time_column=time_column
            )
            price_series = LineSeries(
                data=price_data,
                options=LineSeriesOptions(
                    color=price_color,
                    line_width=2
                )
            )
        series_list.append(price_series)
        
        # Add middle band (MA)
        ma_data = df_to_line_data(
            df_clean,
            value_column='BB_MA',
            time_column=time_column
        )
        from .series import LineSeries
        ma_series = LineSeries(
            data=ma_data,
            options=LineSeriesOptions(
                color=band_color,
                line_width=1
            )
        )
        series_list.append(ma_series)
        
        # Add upper band
        upper_data = df_to_line_data(
            df_clean,
            value_column='BB_Upper',
            time_column=time_column
        )
        upper_series = LineSeries(
            data=upper_data,
            options=LineSeriesOptions(
                color=band_color,
                line_width=1
            )
        )
        series_list.append(upper_series)
        
        # Add lower band
        lower_data = df_to_line_data(
            df_clean,
            value_column='BB_Lower',
            time_column=time_column
        )
        lower_series = LineSeries(
            data=lower_data,
            options=LineSeriesOptions(
                color=band_color,
                line_width=1
            )
        )
        series_list.append(lower_series)
        
        # TODO: Add area fill between bands when supported
        
        # Initialize parent chart
        super().__init__(series=series_list, options=chart_options)