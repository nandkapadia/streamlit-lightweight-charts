"""
DataFrame conversion utilities for streamlit-lightweight-charts.

This module provides utility functions for converting pandas DataFrames
to the internal data structures used by the chart library.
"""

from typing import Any, Dict, List, Optional, Union

import pandas as pd

from streamlit_lightweight_charts.data.models import (
    BaselineData,
    HistogramData,
    OhlcData,
    OhlcvData,
    SingleValueData,
)
from streamlit_lightweight_charts.data.base import to_utc_timestamp


def df_to_line_data(
    df: pd.DataFrame, value_column: str = "close", time_column: Optional[str] = None
) -> List[SingleValueData]:
    """
    Convert a pandas DataFrame to line chart data.

    This function converts a DataFrame into a list of SingleValueData objects
    suitable for line charts and area charts. It automatically handles time
    conversion and supports both index-based and column-based time values.

    Args:
        df: DataFrame containing the data to convert. Should have numeric
            values in the value_column and time information in either the
            index or time_column.
        value_column: Name of the column containing the numeric values to plot.
            Defaults to "close" for typical financial data.
        time_column: Name of the column containing time values. If None,
            uses the DataFrame index as time values.

    Returns:
        List of SingleValueData objects ready for use in line or area charts.

    Example:
        ```python
        # Using DataFrame index as time
        df = pd.DataFrame({'close': [100, 101, 102]},
                         index=pd.date_range('2024-01-01', periods=3))
        line_data = df_to_line_data(df, value_column='close')

        # Using specific time column
        df = pd.DataFrame({
            'date': ['2024-01-01', '2024-01-02', '2024-01-03'],
            'price': [100, 101, 102]
        })
        line_data = df_to_line_data(df, value_column='price', time_column='date')
        ```
    """
    data = []

    if time_column is None:
        # Use DataFrame index as time values
        for timestamp, row in df.iterrows():
            data.append(SingleValueData(time=str(timestamp), value=float(row[value_column])))
    else:
        # Use specified column as time values
        for _, row in df.iterrows():
            data.append(SingleValueData(time=str(row[time_column]), value=float(row[value_column])))

    return data


def df_to_ohlc_data(
    df: pd.DataFrame,
    time_column: Optional[str] = None,
    open_column: str = "open",
    high_column: str = "high",
    low_column: str = "low",
    close_column: str = "close",
) -> List[OhlcData]:
    """
    Convert DataFrame to list of OhlcData objects.

    Args:
        df: DataFrame containing OHLC data
        time_column: Column name for time data (if None, uses index)
        open_column: Column name for open prices
        high_column: Column name for high prices
        low_column: Column name for low prices
        close_column: Column name for close prices

    Returns:
        List of OhlcData objects

    Example:
        ```python
        df = pd.DataFrame({
            'time': ['2024-01-01', '2024-01-02'],
            'open': [100, 102],
            'high': [105, 107],
            'low': [98, 100],
            'close': [102, 104]
        })
        ohlc_data = df_to_ohlc_data(df, time_column='time')
        ```
    """
    ohlc_data = []

    for idx, row in df.iterrows():
        # Get time value
        if time_column and time_column in row:
            time_value = row[time_column]
        else:
            time_value = idx

        # Convert time to proper format
        time_value = to_utc_timestamp(str(time_value))

        # Create OHLC data point
        ohlc_data.append(
            OhlcData(
                time=time_value,
                open_=float(row[open_column]),
                high=float(row[high_column]),
                low=float(row[low_column]),
                close=float(row[close_column]),
            )
        )

    return ohlc_data


def df_to_ohlcv_data(
    df: pd.DataFrame,
    time_column: Optional[str] = None,
    open_column: str = "open",
    high_column: str = "high",
    low_column: str = "low",
    close_column: str = "close",
    volume_column: str = "volume",
) -> List[OhlcvData]:
    """
    Convert DataFrame to list of OhlcvData objects.

    Args:
        df: DataFrame containing OHLCV data
        time_column: Column name for time data (if None, uses index)
        open_column: Column name for open prices
        high_column: Column name for high prices
        low_column: Column name for low prices
        close_column: Column name for close prices
        volume_column: Column name for volume data

    Returns:
        List of OhlcvData objects

    Example:
        ```python
        df = pd.DataFrame({
            'time': ['2024-01-01', '2024-01-02'],
            'open': [100, 102],
            'high': [105, 107],
            'low': [98, 100],
            'close': [102, 104],
            'volume': [1000000, 1200000]
        })
        ohlcv_data = df_to_ohlcv_data(df, time_column='time')
        ```
    """
    ohlcv_data = []

    for idx, row in df.iterrows():
        # Get time value
        if time_column and time_column in row:
            time_value = row[time_column]
        else:
            time_value = idx

        # Convert time to proper format
        time_value = to_utc_timestamp(str(time_value))

        # Create OHLCV data point
        ohlcv_data.append(
            OhlcvData(
                time=time_value,
                open_=float(row[open_column]),
                high=float(row[high_column]),
                low=float(row[low_column]),
                close=float(row[close_column]),
                volume=float(row[volume_column]),
            )
        )

    return ohlcv_data


def df_to_histogram_data(
    df: pd.DataFrame,
    value_column: str = "volume",
    color_column: Optional[str] = None,
    time_column: Optional[str] = None,
    positive_color: str = "#26a69a",
    negative_color: str = "#ef5350",
) -> List[HistogramData]:
    """
    Convert a pandas DataFrame to histogram chart data.

    This function converts a DataFrame into a list of HistogramData objects
    suitable for volume charts and other histogram visualizations. It supports
    automatic color assignment based on value sign or custom color columns.

    Args:
        df: DataFrame containing the data to convert. Should have numeric
            values in the value_column.
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
        List of HistogramData objects ready for use in histogram charts.

    Example:
        ```python
        # Automatic color assignment based on value sign
        df = pd.DataFrame({
            'volume': [1000000, -500000, 750000]
        }, index=pd.date_range('2024-01-01', periods=3))
        hist_data = df_to_histogram_data(df, value_column='volume')

        # Using custom color column
        df = pd.DataFrame({
            'volume': [1000000, 500000, 750000],
            'color': ['#26a69a', '#ef5350', '#26a69a']
        }, index=pd.date_range('2024-01-01', periods=3))
        hist_data = df_to_histogram_data(
            df, value_column='volume', color_column='color'
        )
        ```
    """
    data = []

    if time_column is None:
        # Use DataFrame index as time values
        for timestamp, row in df.iterrows():
            value = row[value_column]

            # Determine color based on available information
            if color_column is not None:
                color = row[color_column]
            else:
                # Use sign-based color assignment
                color = positive_color if value >= 0 else negative_color

            data.append(HistogramData(time=str(timestamp), value=float(value), color=str(color)))
    else:
        # Use specified column as time values
        for _, row in df.iterrows():
            value = row[value_column]

            # Determine color based on available information
            if color_column is not None:
                color = row[color_column]
            else:
                # Use sign-based color assignment
                color = positive_color if value >= 0 else negative_color

            data.append(
                HistogramData(
                    time=str(row[time_column]), 
                    value=float(value), 
                    color=str(color)
                )
            )

    return data


def df_to_baseline_data(
    df: pd.DataFrame, value_column: str = "value", time_column: Optional[str] = None
) -> List[BaselineData]:
    """
    Convert a pandas DataFrame to baseline chart data.

    This function converts a DataFrame into a list of BaselineData objects
    suitable for baseline charts that show values relative to a baseline.

    Args:
        df: DataFrame containing the data to convert. Should have numeric
            values in the value_column.
        value_column: Name of the column containing the numeric values to plot.
            Defaults to "value".
        time_column: Name of the column containing time values. If None,
            uses the DataFrame index as time values.

    Returns:
        List of BaselineData objects ready for use in baseline charts.

    Example:
        ```python
        # Using DataFrame index as time
        df = pd.DataFrame({
            'returns': [0.05, -0.02, 0.03, -0.01]
        }, index=pd.date_range('2024-01-01', periods=4))
        baseline_data = df_to_baseline_data(df, value_column='returns')
        ```
    """
    data = []

    if time_column is None:
        # Use DataFrame index as time values
        for timestamp, row in df.iterrows():
            data.append(BaselineData(time=str(timestamp), value=float(row[value_column])))
    else:
        # Use specified column as time values
        for _, row in df.iterrows():
            data.append(BaselineData(time=str(row[time_column]), value=float(row[value_column])))

    return data


def resample_df_for_charts(
    df: pd.DataFrame, freq: str, agg_dict: Optional[Dict[str, Any]] = None
) -> pd.DataFrame:
    """
    Resample a DataFrame to a different frequency for charting.

    This function resamples a DataFrame with a datetime index to a different
    frequency, applying appropriate aggregation functions for each column.
    It's particularly useful for converting high-frequency data to lower
    frequencies for charting purposes.

    Args:
        df: DataFrame with datetime index to resample.
        freq: Resampling frequency string (e.g., '1D' for daily, '1H' for hourly,
            '5T' for 5 minutes, '1W' for weekly, '1M' for monthly).
        agg_dict: Dictionary mapping column names to aggregation functions.
            If None, uses sensible defaults for common financial columns:
            - 'open': 'first' (first value in period)
            - 'high': 'max' (highest value in period)
            - 'low': 'min' (lowest value in period)
            - 'close': 'last' (last value in period)
            - 'volume': 'sum' (sum of values in period)
            - Other numeric columns: 'mean' (average value in period)

    Returns:
        Resampled DataFrame with the specified frequency.

    Example:
        ```python
        # Resample 1-minute data to daily OHLC
        df_1min = pd.DataFrame({
            'open': [100, 101, 102, ...],
            'high': [105, 106, 107, ...],
            'low': [98, 99, 100, ...],
            'close': [102, 103, 104, ...],
            'volume': [1000, 1500, 2000, ...]
        }, index=pd.date_range('2024-01-01', periods=1440, freq='1T'))

        df_daily = resample_df_for_charts(df_1min, freq='1D')

        # Custom aggregation
        custom_agg = {
            'price': 'ohlc',  # Creates open, high, low, close columns
            'volume': 'sum',
            'trades': 'count'
        }
        df_resampled = resample_df_for_charts(df, freq='1H', agg_dict=custom_agg)
        ```
    """
    if agg_dict is None:
        # Default aggregation for common financial columns
        agg_dict = {}

        # OHLC columns with appropriate aggregations
        if "open" in df.columns:
            agg_dict["open"] = "first"
        if "high" in df.columns:
            agg_dict["high"] = "max"
        if "low" in df.columns:
            agg_dict["low"] = "min"
        if "close" in df.columns:
            agg_dict["close"] = "last"
        if "volume" in df.columns:
            agg_dict["volume"] = "sum"

        # For other numeric columns, use mean as default
        for col in df.select_dtypes(include=["number"]).columns:
            if col not in agg_dict:
                agg_dict[col] = "mean"

    result = df.resample(freq).agg(agg_dict)
    return result.to_frame() if isinstance(result, pd.Series) else result


def df_to_data(
    df: pd.DataFrame, chart_type: str, **kwargs
) -> Union[List[SingleValueData], List[OhlcData], List[HistogramData], List[BaselineData]]:
    """
    Convert DataFrame to appropriate data type based on chart type.

    This is a convenience function that automatically selects the appropriate
    converter function based on the specified chart type. It provides a unified
    interface for converting DataFrames to chart data regardless of the target
    chart type.

    Args:
        df: DataFrame containing the data to convert. Should have appropriate
            columns for the specified chart type.
        chart_type: Type of chart to create data for. Valid options are:
            - 'line' or 'area': Uses df_to_line_data
            - 'candlestick' or 'bar': Uses df_to_ohlc_data
            - 'histogram': Uses df_to_histogram_data
            - 'baseline': Uses df_to_baseline_data
        **kwargs: Additional arguments passed to the specific converter function.
            These vary by chart type and include parameters like value_column,
            time_column, color_column, etc.

    Returns:
        List of appropriate data objects for the specified chart type.

    Raises:
        ValueError: If the chart_type is not recognized.

    Example:
        ```python
        # Convert to line chart data
        line_data = df_to_data(df, 'line', value_column='price')

        # Convert to candlestick data
        ohlc_data = df_to_data(df, 'candlestick')

        # Convert to histogram data with custom colors
        hist_data = df_to_data(
            df, 'histogram',
            value_column='volume',
            positive_color='green',
            negative_color='red'
        )
        ```
    """
    chart_type = chart_type.lower()

    if chart_type in ["line", "area"]:
        return df_to_line_data(df, **kwargs)
    elif chart_type in ["candlestick", "bar"]:
        return df_to_ohlc_data(df, **kwargs)
    elif chart_type == "histogram":
        return df_to_histogram_data(df, **kwargs)
    elif chart_type == "baseline":
        return df_to_baseline_data(df, **kwargs)
    else:
        raise ValueError(f"Unknown chart type: {chart_type}")
