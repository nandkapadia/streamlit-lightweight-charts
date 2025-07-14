"""Utility functions for building specialized charts from DataFrames."""

from typing import Optional, List
import pandas as pd
from ..charts import (
    CandlestickChart, LineChart, AreaChart,
    BarChart, HistogramChart, BaselineChart,
    ChartOptions, CandlestickSeriesOptions, LineSeriesOptions,
    AreaSeriesOptions, BarSeriesOptions, HistogramSeriesOptions,
    BaselineSeriesOptions
)
from ..data import Marker
from .dataframe_converter import (
    df_to_line_data, df_to_ohlc_data,
    df_to_histogram_data, df_to_baseline_data
)


def candlestick_chart_from_df(
    df: pd.DataFrame,
    chart_options: Optional[ChartOptions] = None,
    series_options: Optional[CandlestickSeriesOptions] = None,
    markers: Optional[List[Marker]] = None,
    open_column: str = 'open',
    high_column: str = 'high',
    low_column: str = 'low',
    close_column: str = 'close',
    time_column: Optional[str] = None
) -> CandlestickChart:
    """
    Create a CandlestickChart directly from a DataFrame.
    
    Args:
        df: DataFrame with OHLC data
        chart_options: Chart configuration options
        series_options: Candlestick series specific options
        markers: Optional list of markers
        open_column: Column name for open prices
        high_column: Column name for high prices
        low_column: Column name for low prices
        close_column: Column name for close prices
        time_column: Column name for time (if None, uses index)
        
    Returns:
        CandlestickChart instance
    """
    # Convert DataFrame to OHLC data
    data = df_to_ohlc_data(
        df,
        open_column=open_column,
        high_column=high_column,
        low_column=low_column,
        close_column=close_column,
        time_column=time_column
    )
    
    # Create and return chart
    return CandlestickChart(
        data=data,
        options=chart_options,
        series_options=series_options,
        markers=markers
    )


def line_chart_from_df(
    df: pd.DataFrame,
    chart_options: Optional[ChartOptions] = None,
    series_options: Optional[LineSeriesOptions] = None,
    markers: Optional[List[Marker]] = None,
    value_column: str = 'close',
    time_column: Optional[str] = None
) -> LineChart:
    """
    Create a LineChart directly from a DataFrame.
    
    Args:
        df: DataFrame with data
        chart_options: Chart configuration options
        series_options: Line series specific options
        markers: Optional list of markers
        value_column: Column name for values
        time_column: Column name for time (if None, uses index)
        
    Returns:
        LineChart instance
    """
    # Convert DataFrame to line data
    data = df_to_line_data(
        df,
        value_column=value_column,
        time_column=time_column
    )
    
    # Create and return chart
    return LineChart(
        data=data,
        options=chart_options,
        series_options=series_options,
        markers=markers
    )


def area_chart_from_df(
    df: pd.DataFrame,
    chart_options: Optional[ChartOptions] = None,
    series_options: Optional[AreaSeriesOptions] = None,
    markers: Optional[List[Marker]] = None,
    value_column: str = 'close',
    time_column: Optional[str] = None
) -> AreaChart:
    """
    Create an AreaChart directly from a DataFrame.
    
    Args:
        df: DataFrame with data
        chart_options: Chart configuration options
        series_options: Area series specific options
        markers: Optional list of markers
        value_column: Column name for values
        time_column: Column name for time (if None, uses index)
        
    Returns:
        AreaChart instance
    """
    # Convert DataFrame to line data (same as line chart)
    data = df_to_line_data(
        df,
        value_column=value_column,
        time_column=time_column
    )
    
    # Create and return chart
    return AreaChart(
        data=data,
        options=chart_options,
        series_options=series_options,
        markers=markers
    )


def bar_chart_from_df(
    df: pd.DataFrame,
    chart_options: Optional[ChartOptions] = None,
    series_options: Optional[BarSeriesOptions] = None,
    markers: Optional[List[Marker]] = None,
    open_column: str = 'open',
    high_column: str = 'high',
    low_column: str = 'low',
    close_column: str = 'close',
    time_column: Optional[str] = None
) -> BarChart:
    """
    Create a BarChart directly from a DataFrame.
    
    Args:
        df: DataFrame with OHLC data
        chart_options: Chart configuration options
        series_options: Bar series specific options
        markers: Optional list of markers
        open_column: Column name for open prices
        high_column: Column name for high prices
        low_column: Column name for low prices
        close_column: Column name for close prices
        time_column: Column name for time (if None, uses index)
        
    Returns:
        BarChart instance
    """
    # Convert DataFrame to OHLC data
    data = df_to_ohlc_data(
        df,
        open_column=open_column,
        high_column=high_column,
        low_column=low_column,
        close_column=close_column,
        time_column=time_column
    )
    
    # Create and return chart
    return BarChart(
        data=data,
        options=chart_options,
        series_options=series_options,
        markers=markers
    )


def histogram_chart_from_df(
    df: pd.DataFrame,
    chart_options: Optional[ChartOptions] = None,
    series_options: Optional[HistogramSeriesOptions] = None,
    markers: Optional[List[Marker]] = None,
    value_column: str = 'volume',
    color_column: Optional[str] = None,
    time_column: Optional[str] = None,
    positive_color: str = '#26a69a',
    negative_color: str = '#ef5350'
) -> HistogramChart:
    """
    Create a HistogramChart directly from a DataFrame.
    
    Args:
        df: DataFrame with data
        chart_options: Chart configuration options
        series_options: Histogram series specific options
        markers: Optional list of markers
        value_column: Column name for values
        color_column: Column name for colors (optional)
        time_column: Column name for time (if None, uses index)
        positive_color: Color for positive values (if color_column not specified)
        negative_color: Color for negative values (if color_column not specified)
        
    Returns:
        HistogramChart instance
    """
    # Convert DataFrame to histogram data
    data = df_to_histogram_data(
        df,
        value_column=value_column,
        color_column=color_column,
        time_column=time_column,
        positive_color=positive_color,
        negative_color=negative_color
    )
    
    # Create and return chart
    return HistogramChart(
        data=data,
        options=chart_options,
        series_options=series_options,
        markers=markers
    )


def baseline_chart_from_df(
    df: pd.DataFrame,
    chart_options: Optional[ChartOptions] = None,
    series_options: Optional[BaselineSeriesOptions] = None,
    markers: Optional[List[Marker]] = None,
    value_column: str = 'value',
    time_column: Optional[str] = None,
    base_value: Optional[float] = None
) -> BaselineChart:
    """
    Create a BaselineChart directly from a DataFrame.
    
    Args:
        df: DataFrame with data
        chart_options: Chart configuration options
        series_options: Baseline series specific options
        markers: Optional list of markers
        value_column: Column name for values
        time_column: Column name for time (if None, uses index)
        base_value: Optional base value for the baseline
        
    Returns:
        BaselineChart instance
    """
    # Convert DataFrame to baseline data
    data = df_to_baseline_data(
        df,
        value_column=value_column,
        time_column=time_column
    )
    
    # Create and return chart
    return BaselineChart(
        data=data,
        options=chart_options,
        series_options=series_options,
        markers=markers,
        base_value=base_value
    )