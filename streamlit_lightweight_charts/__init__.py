"""Streamlit Lightweight Charts - OOP wrapper for TradingView Lightweight Charts."""

from .charts import (
    Chart, MultiPaneChart,
    CandlestickChart, LineChart, AreaChart,
    BarChart, HistogramChart, BaselineChart,
    PriceVolumeChart, ComparisonChart,
    ChartOptions, LayoutOptions, GridOptions, CrosshairOptions,
    PriceScaleOptions, TimeScaleOptions, WatermarkOptions,
    AreaSeries, LineSeries, BarSeries, CandlestickSeries,
    HistogramSeries, BaselineSeries,
    AreaSeriesOptions, LineSeriesOptions, BarSeriesOptions,
    CandlestickSeriesOptions, HistogramSeriesOptions, BaselineSeriesOptions
)
from .data import (
    SingleValueData, OhlcData, HistogramData, BaselineData,
    Marker, MarkerShape, MarkerPosition,
    Trade, TradeType, TradeVisualization, TradeVisualizationOptions
)
from .types import (
    ChartType, ColorType, LineStyle, LineType,
    CrosshairMode, PriceScaleMode,
    Background, SolidColor, VerticalGradientColor
)
from .utils import (
    df_to_line_data, df_to_ohlc_data, df_to_histogram_data,
    df_to_baseline_data, df_to_data, resample_df_for_charts,
    candlestick_chart_from_df, line_chart_from_df, area_chart_from_df,
    bar_chart_from_df, histogram_chart_from_df, baseline_chart_from_df
)

__version__ = "0.8.0"

__all__ = [
    # Charts
    'Chart',
    'MultiPaneChart',
    # Specialized Charts
    'CandlestickChart',
    'LineChart',
    'AreaChart',
    'BarChart',
    'HistogramChart',
    'BaselineChart',
    # Composite Charts
    'PriceVolumeChart',
    'ComparisonChart',
    # Options
    'ChartOptions',
    'LayoutOptions',
    'GridOptions',
    'CrosshairOptions',
    'PriceScaleOptions',
    'TimeScaleOptions',
    'WatermarkOptions',
    # Series
    'AreaSeries',
    'LineSeries',
    'BarSeries',
    'CandlestickSeries',
    'HistogramSeries',
    'BaselineSeries',
    # Series Options
    'AreaSeriesOptions',
    'LineSeriesOptions',
    'BarSeriesOptions',
    'CandlestickSeriesOptions',
    'HistogramSeriesOptions',
    'BaselineSeriesOptions',
    # Data
    'SingleValueData',
    'OhlcData',
    'HistogramData',
    'BaselineData',
    'Marker',
    'MarkerShape',
    'MarkerPosition',
    'Trade',
    'TradeType',
    'TradeVisualization',
    'TradeVisualizationOptions',
    # Types
    'ChartType',
    'ColorType',
    'LineStyle',
    'LineType',
    'CrosshairMode',
    'PriceScaleMode',
    'Background',
    'SolidColor',
    'VerticalGradientColor',
    # Utils - DataFrame converters
    'df_to_line_data',
    'df_to_ohlc_data',
    'df_to_histogram_data',
    'df_to_baseline_data',
    'df_to_data',
    'resample_df_for_charts',
    # Utils - Chart builders
    'candlestick_chart_from_df',
    'line_chart_from_df',
    'area_chart_from_df',
    'bar_chart_from_df',
    'histogram_chart_from_df',
    'baseline_chart_from_df'
]
