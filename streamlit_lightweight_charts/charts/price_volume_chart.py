"""Price-Volume composite chart."""

from typing import Any, Dict, List, Optional, Union

import pandas as pd

from ..data import HistogramData, Marker, OhlcData, SingleValueData
from ..utils import df_to_histogram_data, df_to_line_data, df_to_ohlc_data
from .chart import Chart
from .options import ChartOptions, PriceScaleMargins, PriceScaleOptions
from .series import (
    AreaSeries,
    AreaSeriesOptions,
    BarSeries,
    BarSeriesOptions,
    CandlestickSeries,
    CandlestickSeriesOptions,
    HistogramSeries,
    HistogramSeriesOptions,
    LineSeries,
    LineSeriesOptions,
)


class PriceVolumeChart(Chart):
    """
    Single chart with price series and volume histogram overlay.

    The volume is displayed as a histogram overlay on the same chart,
    using an independent Y-axis and scaled to not exceed 25% of the chart height.
    """

    def __init__(
        self,
        df: pd.DataFrame,
        price_type: str = "candlestick",
        height: int = 500,
        options: Optional[ChartOptions] = None,
        price_series_options: Optional[
            Union[
                CandlestickSeriesOptions,
                LineSeriesOptions,
                AreaSeriesOptions,
                BarSeriesOptions,
            ]
        ] = None,
        volume_series_options: Optional[HistogramSeriesOptions] = None,
        price_column: str = "close",
        volume_column: str = "volume",
        time_column: Optional[str] = None,
    ):
        """
        Initialize a price-volume chart with overlay volume.

        Args:
            df: DataFrame with OHLC and volume data
            price_type: Type of price chart ('candlestick', 'line', 'area', 'bar')
            height: Height of the chart
            options: Chart configuration options
            price_series_options: Series options for price chart
            volume_series_options: Series options for volume histogram
            price_column: Column name for price (used if price_type is 'line' or 'area')
            volume_column: Column name for volume
            time_column: Column name for time (if None, uses index)
        """
        # Create chart options with volume overlay configuration
        chart_options = options or ChartOptions(height=height)
        chart_options.height = height

        # Configure price scale for main price series
        if chart_options.right_price_scale is None:
            chart_options.right_price_scale = PriceScaleOptions()
        chart_options.right_price_scale.scale_margins = PriceScaleMargins(top=0.1, bottom=0.25)

        # Configure left price scale for volume (independent Y-axis)
        if chart_options.left_price_scale is None:
            chart_options.left_price_scale = PriceScaleOptions()
        chart_options.left_price_scale.scale_margins = PriceScaleMargins(top=0.8, bottom=0)
        chart_options.left_price_scale.visible = False  # Hide the scale but keep the axis

        # Create price series
        price_series = self._create_price_series(
            df, price_type, price_column, price_series_options, time_column
        )

        # Create volume series as overlay
        volume_series = self._create_volume_series(
            df, volume_column, volume_series_options, time_column
        )

        # Initialize parent with both series
        super().__init__([price_series, volume_series], options=chart_options)

        # Store references for convenience
        self.price_series = price_series
        self.volume_series = volume_series

    def _create_price_series(
        self,
        df: pd.DataFrame,
        price_type: str,
        price_column: str,
        series_options: Optional[
            Union[
                CandlestickSeriesOptions,
                LineSeriesOptions,
                AreaSeriesOptions,
                BarSeriesOptions,
            ]
        ],
        time_column: Optional[str],
    ) -> Union[CandlestickSeries, LineSeries, AreaSeries, BarSeries]:
        """Create price series based on type."""
        if price_type == "candlestick":
            data = df_to_ohlc_data(df, time_column=time_column)
            options = series_options or CandlestickSeriesOptions(
                up_color="#26a69a", down_color="#ef5350"
            )
            return CandlestickSeries(data=data, options=options)

        elif price_type == "line":
            data = df_to_line_data(df, value_column=price_column, time_column=time_column)
            options = series_options or LineSeriesOptions(color="#2196F3", line_width=2)
            return LineSeries(data=data, options=options)

        elif price_type == "area":
            data = df_to_line_data(df, value_column=price_column, time_column=time_column)
            options = series_options or AreaSeriesOptions(
                top_color="rgba(33, 150, 243, 0.56)",
                bottom_color="rgba(33, 150, 243, 0.04)",
                line_color="#2196F3",
            )
            return AreaSeries(data=data, options=options)

        elif price_type == "bar":
            data = df_to_ohlc_data(df, time_column=time_column)
            options = series_options or BarSeriesOptions()
            return BarSeries(data=data, options=options)

        else:
            raise ValueError(f"Unknown price type: {price_type}")

    def _create_volume_series(
        self,
        df: pd.DataFrame,
        volume_column: str,
        series_options: Optional[HistogramSeriesOptions],
        time_column: Optional[str],
    ) -> HistogramSeries:
        """Create volume histogram series as overlay."""
        # Prepare volume data with color based on price movement
        volume_data = self._prepare_volume_data(df, volume_column, time_column)

        # Create volume series options
        options = series_options or HistogramSeriesOptions(color="#26a69a")

        # Set price scale ID to use left price scale (independent Y-axis)
        options.price_scale_id = "left"

        return HistogramSeries(data=volume_data, options=options)

    def _prepare_volume_data(
        self, df: pd.DataFrame, volume_column: str, time_column: Optional[str]
    ) -> List[HistogramData]:
        """Prepare volume data with color based on price movement."""
        volume_data = []

        # Ensure we have the required columns
        if volume_column not in df.columns:
            raise ValueError(f"Volume column '{volume_column}' not found in DataFrame")

        # Determine time column
        time_col = time_column if time_column else df.index.name or "time"

        # Check if we have OHLC data for color determination
        has_ohlc = all(col in df.columns for col in ["open", "close"])

        for idx, row in df.iterrows():
            # Get time value
            if time_col == "time" and time_col in df.columns:
                time_value = row[time_col]
            else:
                time_value = idx

            # Get volume value
            volume_value = float(row[volume_column]) if pd.notna(row[volume_column]) else 0.0

            # Determine color based on price movement if OHLC data is available
            if has_ohlc:
                color = (
                    "rgba(38, 166, 154, 0.4)"  # Green for up
                    if row["close"] >= row["open"]
                    else "rgba(239, 83, 80, 0.4)"  # Red for down
                )
            else:
                color = "rgba(38, 166, 154, 0.4)"  # Default green

            volume_data.append(
                HistogramData(
                    time=time_value,
                    value=volume_value,
                    color=color,
                )
            )

        return volume_data

    def add_price_indicator(
        self,
        indicator_data: List[SingleValueData],
        options: Optional[LineSeriesOptions] = None,
        markers: Optional[List[Marker]] = None,
    ) -> "PriceVolumeChart":
        """
        Add a price indicator to the chart.

        Args:
            indicator_data: List of indicator data points
            options: Series options for the indicator
            markers: Optional markers for the indicator

        Returns:
            Self for method chaining
        """
        indicator_series = LineSeries(
            data=indicator_data,
            options=options or LineSeriesOptions(color="#FF9800", line_width=1),
            markers=markers,
        )
        self.add_series(indicator_series)
        return self

    def add_trades(
        self,
        trades: List["Trade"],
        visualization_options: Optional["TradeVisualizationOptions"] = None,
    ) -> "PriceVolumeChart":
        """
        Add trade visualizations to the candlestick series.

        Args:
            trades: List of trades to visualize
            visualization_options: Options for trade visualization

        Returns:
            Self for method chaining
        """
        # Only add trades if we have a candlestick series
        if isinstance(self.price_series, CandlestickSeries):
            self.price_series.trades = trades
            self.price_series.trade_visualization_options = visualization_options

        return self
