"""
Utility functions for converting pandas DataFrames to chart data.

This module provides a comprehensive set of utility functions for converting
pandas DataFrames into the various data formats required by the charting library.
It supports conversion to line data, OHLC data, histogram data, and baseline data,
with flexible column mapping and automatic time handling.

The functions handle common financial data formats and provide sensible defaults
for typical use cases while allowing customization for specific requirements.
"""

from typing import Any, Dict, List, Optional, Union

import pandas as pd

from ..data import BaselineData, HistogramData, OhlcData, SingleValueData


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
            data.append(SingleValueData(time=timestamp, value=row[value_column]))
    else:
        # Use specified column as time values
        for _, row in df.iterrows():
            data.append(SingleValueData(time=row[time_column], value=row[value_column]))

    return data


def df_to_ohlc_data(
    df: pd.DataFrame,
    open_column: str = "open",
    high_column: str = "high",
    low_column: str = "low",
    close_column: str = "close",
    time_column: Optional[str] = None,
) -> List[OhlcData]:
    """
    Convert a pandas DataFrame to OHLC chart data.

    This function converts a DataFrame with OHLC (Open, High, Low, Close) data
    into a list of OhlcData objects suitable for candlestick charts and bar charts.
    It supports flexible column naming and automatic time handling.

    Args:
        df: DataFrame containing OHLC data. Should have columns for open, high,
            low, and close prices.
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
        List of OhlcData objects ready for use in candlestick or bar charts.

    Example:
        ```python
        # Using DataFrame index as time
        df = pd.DataFrame({
            'open': [100, 101, 102],
            'high': [105, 106, 107],
            'low': [98, 99, 100],
            'close': [102, 103, 104]
        }, index=pd.date_range('2024-01-01', periods=3))
        ohlc_data = df_to_ohlc_data(df)

        # Using custom column names
        df = pd.DataFrame({
            'date': ['2024-01-01', '2024-01-02'],
            'o': [100, 101], 'h': [105, 106],
            'l': [98, 99], 'c': [102, 103]
        })
        ohlc_data = df_to_ohlc_data(
            df, open_column='o', high_column='h',
            low_column='l', close_column='c', time_column='date'
        )
        ```
    """
    data = []

    if time_column is None:
        # Use DataFrame index as time values
        for timestamp, row in df.iterrows():
            data.append(
                OhlcData(
                    time=timestamp,
                    open_=row[open_column],
                    high=row[high_column],
                    low=row[low_column],
                    close=row[close_column],
                )
            )
    else:
        # Use specified column as time values
        for _, row in df.iterrows():
            data.append(
                OhlcData(
                    time=row[time_column],
                    open_=row[open_column],
                    high=row[high_column],
                    low=row[low_column],
                    close=row[close_column],
                )
            )

    return data


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

            data.append(HistogramData(time=timestamp, value=value, color=color))
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

            data.append(HistogramData(time=row[time_column], value=value, color=color))

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
            data.append(BaselineData(time=timestamp, value=row[value_column]))
    else:
        # Use specified column as time values
        for _, row in df.iterrows():
            data.append(BaselineData(time=row[time_column], value=row[value_column]))

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

    return df.resample(freq).agg(agg_dict)


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
