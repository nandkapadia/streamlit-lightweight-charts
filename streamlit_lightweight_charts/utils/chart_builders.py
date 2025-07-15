"""
Utility functions for building specialized charts from DataFrames.

This module provides high-level convenience functions for creating chart objects
directly from pandas DataFrames. These functions combine DataFrame conversion
with chart creation, providing a streamlined workflow for common use cases.

Each function handles the conversion from DataFrame to appropriate data format
and creates the corresponding chart object with the specified options and markers.
"""

# pylint: disable=import-outside-toplevel

from typing import Any, List, Optional

import pandas as pd

from ..data import Marker
from .dataframe_converter import (
    df_to_baseline_data,
    df_to_histogram_data,
    df_to_line_data,
    df_to_ohlc_data,
)


def candlestick_chart_from_df(
    df: pd.DataFrame,
    chart_options: Optional[Any] = None,
    series_options: Optional[Any] = None,
    markers: Optional[List[Marker]] = None,
    open_column: str = "open",
    high_column: str = "high",
    low_column: str = "low",
    close_column: str = "close",
    time_column: Optional[str] = None,
) -> Any:
    """
    Create a CandlestickChart directly from a DataFrame.

    This function combines DataFrame to OHLC data conversion with candlestick
    chart creation, providing a convenient one-step process for creating
    candlestick charts from pandas DataFrames.

    Args:
        df: DataFrame containing OHLC data. Should have columns for open, high,
            low, and close prices.
        chart_options: Chart configuration options. If None, default options
            will be used.
        series_options: Candlestick series specific options. If None, default
            series options will be used.
        markers: Optional list of markers to display on the chart.
        open_column: Name of the column containing opening prices.
            Defaults to "open".
        high_column: Name of the column containing highest prices.
            Defaults to "high".
        low_column: Name of the column containing lowest prices.
            Defaults to "low".
        close_column: Name of the column containing closing prices.
            Defaults to "close".
        time_column: Name of the column containing time values. If None,
            uses the DataFrame index as time values.

    Returns:
        CandlestickChart instance ready for rendering.

    Example:
        ```python
        # Create candlestick chart from DataFrame
        df = pd.DataFrame({
            'open': [100, 101, 102],
            'high': [105, 106, 107],
            'low': [98, 99, 100],
            'close': [102, 103, 104]
        }, index=pd.date_range('2024-01-01', periods=3))

        chart = candlestick_chart_from_df(df)
        chart.render(key="candlestick")
        ```
    """
    # Import here to avoid circular dependency
    from ..charts import CandlestickChart

    # Convert DataFrame to OHLC data using the converter utility
    data = df_to_ohlc_data(
        df,
        open_column=open_column,
        high_column=high_column,
        low_column=low_column,
        close_column=close_column,
        time_column=time_column,
    )

    # Create and return the candlestick chart
    return CandlestickChart(
        data=data, options=chart_options, series_options=series_options, markers=markers
    )


def line_chart_from_df(
    df: pd.DataFrame,
    chart_options: Optional[Any] = None,
    series_options: Optional[Any] = None,
    markers: Optional[List[Marker]] = None,
    value_column: str = "close",
    time_column: Optional[str] = None,
) -> Any:
    """
    Create a LineChart directly from a DataFrame.

    This function combines DataFrame to line data conversion with line chart
    creation, providing a convenient one-step process for creating line charts
    from pandas DataFrames.

    Args:
        df: DataFrame containing the data to plot. Should have numeric values
            in the value_column.
        chart_options: Chart configuration options. If None, default options
            will be used.
        series_options: Line series specific options. If None, default
            series options will be used.
        markers: Optional list of markers to display on the chart.
        value_column: Name of the column containing the numeric values to plot.
            Defaults to "close" for typical financial data.
        time_column: Name of the column containing time values. If None,
            uses the DataFrame index as time values.

    Returns:
        LineChart instance ready for rendering.

    Example:
        ```python
        # Create line chart from DataFrame
        df = pd.DataFrame({
            'price': [100, 101, 102, 103]
        }, index=pd.date_range('2024-01-01', periods=4))

        chart = line_chart_from_df(df, value_column='price')
        chart.render(key="line_chart")
        ```
    """
    # Import here to avoid circular dependency
    from ..charts import LineChart

    # Convert DataFrame to line data using the converter utility
    data = df_to_line_data(df, value_column=value_column, time_column=time_column)

    # Create and return the line chart
    return LineChart(
        data=data, options=chart_options, series_options=series_options, markers=markers
    )


def area_chart_from_df(
    df: pd.DataFrame,
    chart_options: Optional[Any] = None,
    series_options: Optional[Any] = None,
    markers: Optional[List[Marker]] = None,
    value_column: str = "close",
    time_column: Optional[str] = None,
) -> Any:
    """
    Create an AreaChart directly from a DataFrame.

    This function combines DataFrame to line data conversion with area chart
    creation, providing a convenient one-step process for creating area charts
    from pandas DataFrames.

    Args:
        df: DataFrame containing the data to plot. Should have numeric values
            in the value_column.
        chart_options: Chart configuration options. If None, default options
            will be used.
        series_options: Area series specific options. If None, default
            series options will be used.
        markers: Optional list of markers to display on the chart.
        value_column: Name of the column containing the numeric values to plot.
            Defaults to "close" for typical financial data.
        time_column: Name of the column containing time values. If None,
            uses the DataFrame index as time values.

    Returns:
        AreaChart instance ready for rendering.

    Example:
        ```python
        # Create area chart from DataFrame
        df = pd.DataFrame({
            'volume': [1000000, 1200000, 800000, 1500000]
        }, index=pd.date_range('2024-01-01', periods=4))

        chart = area_chart_from_df(df, value_column='volume')
        chart.render(key="area_chart")
        ```
    """
    # Import here to avoid circular dependency
    from ..charts import AreaChart

    # Convert DataFrame to line data (same format as line charts)
    data = df_to_line_data(df, value_column=value_column, time_column=time_column)

    # Create and return the area chart
    return AreaChart(
        data=data, options=chart_options, series_options=series_options, markers=markers
    )


def bar_chart_from_df(
    df: pd.DataFrame,
    chart_options: Optional[Any] = None,
    series_options: Optional[Any] = None,
    markers: Optional[List[Marker]] = None,
    open_column: str = "open",
    high_column: str = "high",
    low_column: str = "low",
    close_column: str = "close",
    time_column: Optional[str] = None,
) -> Any:
    """
    Create a BarChart directly from a DataFrame.

    This function combines DataFrame to OHLC data conversion with bar chart
    creation, providing a convenient one-step process for creating bar charts
    from pandas DataFrames.

    Args:
        df: DataFrame containing OHLC data. Should have columns for open, high,
            low, and close prices.
        chart_options: Chart configuration options. If None, default options
            will be used.
        series_options: Bar series specific options. If None, default
            series options will be used.
        markers: Optional list of markers to display on the chart.
        open_column: Name of the column containing opening prices.
            Defaults to "open".
        high_column: Name of the column containing highest prices.
            Defaults to "high".
        low_column: Name of the column containing lowest prices.
            Defaults to "low".
        close_column: Name of the column containing closing prices.
            Defaults to "close".
        time_column: Name of the column containing time values. If None,
            uses the DataFrame index as time values.

    Returns:
        BarChart instance ready for rendering.

    Example:
        ```python
        # Create bar chart from DataFrame
        df = pd.DataFrame({
            'open': [100, 101, 102],
            'high': [105, 106, 107],
            'low': [98, 99, 100],
            'close': [102, 103, 104]
        }, index=pd.date_range('2024-01-01', periods=3))

        chart = bar_chart_from_df(df)
        chart.render(key="bar_chart")
        ```
    """
    # Import here to avoid circular dependency
    from ..charts import BarChart

    # Convert DataFrame to OHLC data using the converter utility
    data = df_to_ohlc_data(
        df,
        open_column=open_column,
        high_column=high_column,
        low_column=low_column,
        close_column=close_column,
        time_column=time_column,
    )

    # Create and return the bar chart
    return BarChart(
        data=data, options=chart_options, series_options=series_options, markers=markers
    )


def histogram_chart_from_df(
    df: pd.DataFrame,
    chart_options: Optional[Any] = None,
    series_options: Optional[Any] = None,
    value_column: str = "volume",
    color_column: Optional[str] = None,
    time_column: Optional[str] = None,
    positive_color: str = "#26a69a",
    negative_color: str = "#ef5350",
) -> Any:
    """
    Create a HistogramChart directly from a DataFrame.

    This function combines DataFrame to histogram data conversion with histogram
    chart creation, providing a convenient one-step process for creating histogram
    charts from pandas DataFrames.

    Args:
        df: DataFrame containing the data to plot. Should have numeric values
            in the value_column.
        chart_options: Chart configuration options. If None, default options
            will be used.
        series_options: Histogram series specific options. If None, default
            series options will be used.
        value_column: Name of the column containing the numeric values to plot.
            Defaults to "volume" for typical financial data.
        color_column: Name of the column containing color values. If None,
            colors are automatically assigned based on value sign.
        time_column: Name of the column containing time values. If None,
            uses the DataFrame index as time values.
        positive_color: Color to use for positive values when color_column
            is not specified. Defaults to "#26a69a" (green).
        negative_color: Color to use for negative values when color_column
            is not specified. Defaults to "#ef5350" (red).

    Returns:
        HistogramChart instance ready for rendering.

    Example:
        ```python
        # Create histogram chart from DataFrame
        df = pd.DataFrame({
            'volume': [1000000, -500000, 750000, -300000]
        }, index=pd.date_range('2024-01-01', periods=4))

        chart = histogram_chart_from_df(df, value_column='volume')
        chart.render(key="histogram")
        ```
    """
    # Import here to avoid circular dependency
    from ..charts import HistogramChart

    # Convert DataFrame to histogram data using the converter utility
    data = df_to_histogram_data(
        df,
        value_column=value_column,
        color_column=color_column,
        time_column=time_column,
        positive_color=positive_color,
        negative_color=negative_color,
    )

    # Create and return the histogram chart
    return HistogramChart(data=data, options=chart_options, series_options=series_options)


def baseline_chart_from_df(
    df: pd.DataFrame,
    chart_options: Optional[Any] = None,
    series_options: Optional[Any] = None,
    markers: Optional[List[Marker]] = None,
    value_column: str = "value",
    time_column: Optional[str] = None,
) -> Any:
    """
    Create a BaselineChart directly from a DataFrame.

    This function combines DataFrame to baseline data conversion with baseline
    chart creation, providing a convenient one-step process for creating baseline
    charts from pandas DataFrames.

    Args:
        df: DataFrame containing the data to plot. Should have numeric values
            in the value_column.
        chart_options: Chart configuration options. If None, default options
            will be used.
        series_options: Baseline series specific options. If None, default
            series options will be used.
        markers: Optional list of markers to display on the chart.
        value_column: Name of the column containing the numeric values to plot.
            Defaults to "value".
        time_column: Name of the column containing time values. If None,
            uses the DataFrame index as time values.

    Returns:
        BaselineChart instance ready for rendering.

    Example:
        ```python
        # Create baseline chart from DataFrame
        df = pd.DataFrame({
            'returns': [0.05, -0.02, 0.03, -0.01, 0.04]
        }, index=pd.date_range('2024-01-01', periods=5))

        chart = baseline_chart_from_df(df, value_column='returns')
        chart.render(key="baseline")
        ```
    """
    # Import here to avoid circular dependency
    from ..charts import BaselineChart

    # Convert DataFrame to baseline data using the converter utility
    data = df_to_baseline_data(df, value_column=value_column, time_column=time_column)

    # Create and return the baseline chart
    return BaselineChart(
        data=data, options=chart_options, series_options=series_options, markers=markers
    )
