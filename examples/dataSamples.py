"""
Sample data for streamlit-lightweight-charts examples and testing.

This module contains sample datasets in various formats for demonstrating
different chart types and features. All data is structured according to
the library's data models and can be used directly in examples.

The module provides:
    - Raw data dictionaries for backward compatibility
    - Converted data model objects for the new API
    - Helper functions for data conversion
    - Sample datasets for all chart types

Example:
    ```python
    from examples.dataSamples import (
        get_line_data, get_candlestick_data, get_volume_data
    )

    # Get data as data model objects
    line_data = get_line_data()
    candlestick_data = get_candlestick_data()

    # Use with new API
    chart = SinglePaneChart(series=LineSeries(data=line_data))
    ```
"""

from typing import Dict, List, Union

import pandas as pd

from streamlit_lightweight_charts_pro.data import (
    BaselineData,
    HistogramData,
    OhlcData,
    SingleValueData,
)

# =============================================================================
# RAW DATA DICTIONARIES (for backward compatibility)
# =============================================================================

# Sample data for single value charts (line, area)
series_single_value_data = [
    {"datetime": "2018-12-22", "value": 32.51},
    {"datetime": "2018-12-23", "value": 31.11},
    {"datetime": "2018-12-24", "value": 27.02},
    {"datetime": "2018-12-25", "value": 27.32},
    {"datetime": "2018-12-26", "value": 25.17},
    {"datetime": "2018-12-27", "value": 28.89},
    {"datetime": "2018-12-28", "value": 25.46},
    {"datetime": "2018-12-29", "value": 23.92},
    {"datetime": "2018-12-30", "value": 22.68},
    {"datetime": "2018-12-31", "value": 22.67},
]

# Sample data for baseline charts
series_baseline_chart = [
    {"value": 1, "datetime": 1642425322},
    {"value": 8, "datetime": 1642511722},
    {"value": 10, "datetime": 1642598122},
    {"value": 20, "datetime": 1642684522},
    {"value": 3, "datetime": 1642770922},
    {"value": 43, "datetime": 1642857322},
    {"value": 41, "datetime": 1642943722},
    {"value": 43, "datetime": 1643030122},
    {"value": 56, "datetime": 1643116522},
    {"value": 46, "datetime": 1643202922},
]

# Sample data for histogram charts
series_histogram_chart = [
    {"value": 1, "datetime": 1642425322},
    {"value": 8, "datetime": 1642511722},
    {"value": 10, "datetime": 1642598122},
    {"value": 20, "datetime": 1642684522},
    {"value": 3, "datetime": 1642770922, "color": "red"},
    {"value": 43, "datetime": 1642857322},
    {"value": 41, "datetime": 1642943722, "color": "red"},
    {"value": 43, "datetime": 1643030122},
    {"value": 56, "datetime": 1643116522},
    {"value": 46, "datetime": 1643202922, "color": "red"},
]

# Sample data for bar charts
series_bar_chart = [
    {"open": 10, "high": 10.63, "low": 9.49, "close": 9.55, "datetime": 1642427876},
    {"open": 9.55, "high": 10.30, "low": 9.42, "close": 9.94, "datetime": 1642514276},
    {"open": 9.94, "high": 10.17, "low": 9.92, "close": 9.78, "datetime": 1642600676},
    {"open": 9.78, "high": 10.59, "low": 9.18, "close": 9.51, "datetime": 1642687076},
    {"open": 9.51, "high": 10.46, "low": 9.10, "close": 10.17, "datetime": 1642773476},
    {"open": 10.17, "high": 10.96, "low": 10.16, "close": 10.47, "datetime": 1642859876},
    {"open": 10.47, "high": 11.39, "low": 10.40, "close": 10.81, "datetime": 1642946276},
    {"open": 10.81, "high": 11.60, "low": 10.30, "close": 10.75, "datetime": 1643032676},
    {"open": 10.75, "high": 11.60, "low": 10.49, "close": 10.93, "datetime": 1643119076},
    {"open": 10.93, "high": 11.53, "low": 10.76, "close": 10.96, "datetime": 1643205476},
]

# Sample data for candlestick charts
series_candlestick_chart = [
    {"open": 10, "high": 10.63, "low": 9.49, "close": 9.55, "datetime": 1642427876},
    {"open": 9.55, "high": 10.30, "low": 9.42, "close": 9.94, "datetime": 1642514276},
    {"open": 9.94, "high": 10.17, "low": 9.92, "close": 9.78, "datetime": 1642600676},
    {"open": 9.78, "high": 10.59, "low": 9.18, "close": 9.51, "datetime": 1642687076},
    {"open": 9.51, "high": 10.46, "low": 9.10, "close": 10.17, "datetime": 1642773476},
    {"open": 10.17, "high": 10.96, "low": 10.16, "close": 10.47, "datetime": 1642859876},
    {"open": 10.47, "high": 11.39, "low": 10.40, "close": 10.81, "datetime": 1642946276},
    {"open": 10.81, "high": 11.60, "low": 10.30, "close": 10.75, "datetime": 1643032676},
    {"open": 10.75, "high": 11.60, "low": 10.49, "close": 10.93, "datetime": 1643119076},
    {"open": 10.93, "high": 11.53, "low": 10.76, "close": 10.96, "datetime": 1643205476},
]

# Sample data for multi-chart area series 1
series_multiple_chart_area_01 = [
    {"datetime": "2019-03-01", "value": 42.58},
    {"datetime": "2019-03-04", "value": 42.64},
    {"datetime": "2019-03-05", "value": 42.74},
    {"datetime": "2019-03-06", "value": 42.7},
    {"datetime": "2019-03-07", "value": 42.63},
    {"datetime": "2019-03-08", "value": 42.25},
    {"datetime": "2019-03-11", "value": 42.33},
    {"datetime": "2019-03-12", "value": 42.46},
    {"datetime": "2019-03-13", "value": 43.83},
    {"datetime": "2019-03-14", "value": 43.95},
    {"datetime": "2019-03-15", "value": 43.87},
    {"datetime": "2019-03-18", "value": 44.24},
    {"datetime": "2019-03-19", "value": 44.47},
    {"datetime": "2019-03-20", "value": 44.53},
    {"datetime": "2019-03-21", "value": 44.53},
    {"datetime": "2019-03-22", "value": 43.95},
    {"datetime": "2019-03-25", "value": 43.53},
    {"datetime": "2019-03-26", "value": 43.82},
    {"datetime": "2019-03-27", "value": 43.59},
    {"datetime": "2019-03-28", "value": 43.63},
    {"datetime": "2019-03-29", "value": 43.72},
    {"datetime": "2019-04-01", "value": 44.09},
    {"datetime": "2019-04-02", "value": 44.23},
    {"datetime": "2019-04-03", "value": 44.23},
    {"datetime": "2019-04-04", "value": 44.15},
    {"datetime": "2019-04-05", "value": 44.53},
    {"datetime": "2019-04-08", "value": 45.23},
    {"datetime": "2019-04-09", "value": 44.99},
    {"datetime": "2019-04-10", "value": 45.04},
    {"datetime": "2019-04-11", "value": 44.87},
    {"datetime": "2019-04-12", "value": 44.67},
    {"datetime": "2019-04-15", "value": 44.67},
    {"datetime": "2019-04-16", "value": 44.48},
    {"datetime": "2019-04-17", "value": 44.62},
    {"datetime": "2019-04-18", "value": 44.39},
    {"datetime": "2019-04-22", "value": 45.04},
    {"datetime": "2019-04-23", "value": 45.02},
    {"datetime": "2019-04-24", "value": 44.13},
    {"datetime": "2019-04-25", "value": 43.96},
    {"datetime": "2019-04-26", "value": 43.31},
    {"datetime": "2019-04-29", "value": 43.02},
    {"datetime": "2019-04-30", "value": 43.73},
    {"datetime": "2019-05-01", "value": 43.08},
    {"datetime": "2019-05-02", "value": 42.63},
    {"datetime": "2019-05-03", "value": 43.08},
    {"datetime": "2019-05-06", "value": 42.93},
    {"datetime": "2019-05-07", "value": 42.22},
    {"datetime": "2019-05-08", "value": 42.28},
    {"datetime": "2019-05-09", "value": 41.65},
    {"datetime": "2019-05-10", "value": 41.5},
    {"datetime": "2019-05-13", "value": 41.23},
    {"datetime": "2019-05-14", "value": 41.55},
    {"datetime": "2019-05-15", "value": 41.77},
    {"datetime": "2019-05-16", "value": 42.28},
    {"datetime": "2019-05-17", "value": 42.34},
    {"datetime": "2019-05-20", "value": 42.58},
    {"datetime": "2019-05-21", "value": 42.75},
    {"datetime": "2019-05-22", "value": 42.34},
    {"datetime": "2019-05-23", "value": 41.34},
    {"datetime": "2019-05-24", "value": 41.76},
    {"datetime": "2019-05-28", "value": 41.625},
]

# Sample data for multi-chart area series 2
series_multiple_chart_area_02 = [
    {"datetime": "2019-03-01", "value": 174.97},
    {"datetime": "2019-03-04", "value": 175.85},
    {"datetime": "2019-03-05", "value": 175.53},
    {"datetime": "2019-03-06", "value": 174.52},
    {"datetime": "2019-03-07", "value": 172.5},
    {"datetime": "2019-03-08", "value": 172.91},
    {"datetime": "2019-03-11", "value": 178.9},
    {"datetime": "2019-03-12", "value": 180.91},
    {"datetime": "2019-03-13", "value": 181.71},
    {"datetime": "2019-03-14", "value": 183.73},
    {"datetime": "2019-03-15", "value": 186.12},
    {"datetime": "2019-03-18", "value": 188.02},
    {"datetime": "2019-03-19", "value": 186.53},
    {"datetime": "2019-03-20", "value": 188.16},
    {"datetime": "2019-03-21", "value": 195.09},
    {"datetime": "2019-03-22", "value": 191.05},
    {"datetime": "2019-03-25", "value": 188.74},
    {"datetime": "2019-03-26", "value": 186.79},
    {"datetime": "2019-03-27", "value": 188.47},
    {"datetime": "2019-03-28", "value": 188.72},
    {"datetime": "2019-03-29", "value": 189.95},
    {"datetime": "2019-04-01", "value": 191.24},
    {"datetime": "2019-04-02", "value": 194.02},
    {"datetime": "2019-04-03", "value": 195.35},
    {"datetime": "2019-04-04", "value": 195.69},
    {"datetime": "2019-04-05", "value": 197},
    {"datetime": "2019-04-08", "value": 200.1},
    {"datetime": "2019-04-09", "value": 199.5},
    {"datetime": "2019-04-10", "value": 200.62},
    {"datetime": "2019-04-11", "value": 198.95},
    {"datetime": "2019-04-12", "value": 198.87},
    {"datetime": "2019-04-15", "value": 199.23},
    {"datetime": "2019-04-16", "value": 199.25},
    {"datetime": "2019-04-17", "value": 203.13},
    {"datetime": "2019-04-18", "value": 203.86},
    {"datetime": "2019-04-22", "value": 204.53},
    {"datetime": "2019-04-23", "value": 207.48},
    {"datetime": "2019-04-24", "value": 207.16},
    {"datetime": "2019-04-25", "value": 205.28},
    {"datetime": "2019-04-26", "value": 204.3},
    {"datetime": "2019-04-29", "value": 204.61},
    {"datetime": "2019-04-30", "value": 200.67},
    {"datetime": "2019-05-01", "value": 210.52},
    {"datetime": "2019-05-02", "value": 209.15},
    {"datetime": "2019-05-03", "value": 211.75},
    {"datetime": "2019-05-06", "value": 208.48},
    {"datetime": "2019-05-07", "value": 202.86},
    {"datetime": "2019-05-08", "value": 202.9},
    {"datetime": "2019-05-09", "value": 200.72},
    {"datetime": "2019-05-10", "value": 197.18},
    {"datetime": "2019-05-13", "value": 185.72},
    {"datetime": "2019-05-14", "value": 188.66},
    {"datetime": "2019-05-15", "value": 190.92},
    {"datetime": "2019-05-16", "value": 190.08},
    {"datetime": "2019-05-17", "value": 191.44},
    {"datetime": "2019-05-20", "value": 191.83},
    {"datetime": "2019-05-21", "value": 190.04},
    {"datetime": "2019-05-22", "value": 186.6},
    {"datetime": "2019-05-23", "value": 186.79},
    {"datetime": "2019-05-24", "value": 185.72},
    {"datetime": "2019-05-28", "value": 188.66},
]

# Sample data for volume charts
series_volume_chart = [
    {"value": 1000000, "datetime": 1642425322},
    {"value": 1200000, "datetime": 1642511722},
    {"value": 800000, "datetime": 1642598122},
    {"value": 1500000, "datetime": 1642684522},
    {"value": 900000, "datetime": 1642770922},
    {"value": 2000000, "datetime": 1642857322},
    {"value": 1800000, "datetime": 1642943722},
    {"value": 1600000, "datetime": 1643030122},
    {"value": 2200000, "datetime": 1643116522},
    {"value": 1900000, "datetime": 1643202922},
]

# =============================================================================
# DATA MODEL CONVERSION FUNCTIONS
# =============================================================================


def get_line_data() -> List[SingleValueData]:
    """
    Get sample line chart data as SingleValueData objects.

    Returns:
        List[SingleValueData]: List of single value data points for line charts.

    Example:
        ```python
        from examples.dataSamples import get_line_data

        line_data = get_line_data()
        chart = SinglePaneChart(series=LineSeries(data=line_data))
        ```
    """
    return [
        SingleValueData(time=item["datetime"], value=item["value"])
        for item in series_single_value_data
    ]


def get_candlestick_data() -> List[OhlcData]:
    """
    Get sample candlestick chart data as OhlcData objects.

    Returns:
        List[OhlcData]: List of OHLC data points for candlestick charts.

    Example:
        ```python
        from examples.dataSamples import get_candlestick_data

        ohlc_data = get_candlestick_data()
        chart = SinglePaneChart(series=CandlestickSeries(data=ohlc_data))
        ```
    """
    return [
        OhlcData(
            time=item["datetime"],
            open_=item["open"],
            high=item["high"],
            low=item["low"],
            close=item["close"],
        )
        for item in series_candlestick_chart
    ]


def get_volume_data() -> List[HistogramData]:
    """
    Get sample volume chart data as HistogramData objects.

    Returns:
        List[HistogramData]: List of histogram data points for volume charts.

    Example:
        ```python
        from examples.dataSamples import get_volume_data

        volume_data = get_volume_data()
        chart = SinglePaneChart(series=HistogramSeries(data=volume_data))
        ```
    """
    return [
        HistogramData(time=item["datetime"], value=item["value"], color=item.get("color"))
        for item in series_histogram_chart
    ]


def get_baseline_data() -> List[BaselineData]:
    """
    Get sample baseline chart data as BaselineData objects.

    Returns:
        List[BaselineData]: List of baseline data points for baseline charts.

    Example:
        ```python
        from examples.dataSamples import get_baseline_data

        baseline_data = get_baseline_data()
        chart = SinglePaneChart(series=BaselineSeries(data=baseline_data))
        ```
    """
    return [
        BaselineData(time=item["datetime"], value=item["value"]) for item in series_baseline_chart
    ]


def get_multi_area_data_1() -> List[SingleValueData]:
    """
    Get first multi-area chart data as SingleValueData objects.

    Returns:
        List[SingleValueData]: List of single value data points for area charts.

    Example:
        ```python
        from examples.dataSamples import get_multi_area_data_1

        area_data = get_multi_area_data_1()
        chart = SinglePaneChart(series=AreaSeries(data=area_data))
        ```
    """
    return [
        SingleValueData(time=item["datetime"], value=item["value"])
        for item in series_multiple_chart_area_01
    ]


def get_multi_area_data_2() -> List[SingleValueData]:
    """
    Get second multi-area chart data as SingleValueData objects.

    Returns:
        List[SingleValueData]: List of single value data points for area charts.

    Example:
        ```python
        from examples.dataSamples import get_multi_area_data_2

        area_data = get_multi_area_data_2()
        chart = SinglePaneChart(series=AreaSeries(data=area_data))
        ```
    """
    return [
        SingleValueData(time=item["datetime"], value=item["value"])
        for item in series_multiple_chart_area_02
    ]


def get_volume_histogram_data() -> List[HistogramData]:
    """
    Get sample volume histogram data as HistogramData objects.

    Returns:
        List[HistogramData]: List of histogram data points for volume charts.

    Example:
        ```python
        from examples.dataSamples import get_volume_histogram_data

        volume_data = get_volume_histogram_data()
        chart = SinglePaneChart(series=HistogramSeries(data=volume_data))
        ```
    """
    return [
        HistogramData(time=item["datetime"], value=item["value"]) for item in series_volume_chart
    ]


def get_dataframe_line_data() -> pd.DataFrame:
    """
    Get sample line chart data as a pandas DataFrame.

    Returns:
        pd.DataFrame: DataFrame with datetime and close columns for line charts.

    Example:
        ```python
        from examples.dataSamples import get_dataframe_line_data

        df = get_dataframe_line_data()
        chart = SinglePaneChart(series=LineSeries(data=df))
        ```
    """
    return pd.DataFrame(series_single_value_data)


def get_dataframe_candlestick_data() -> pd.DataFrame:
    """
    Get sample candlestick chart data as a pandas DataFrame.

    Returns:
        pd.DataFrame: DataFrame with OHLC columns for candlestick charts.

    Example:
        ```python
        from examples.dataSamples import get_dataframe_candlestick_data

        df = get_dataframe_candlestick_data()
        chart = SinglePaneChart(series=CandlestickSeries(data=df))
        ```
    """
    return pd.DataFrame(series_candlestick_chart)


def get_dataframe_volume_data() -> pd.DataFrame:
    """
    Get sample volume chart data as a pandas DataFrame.

    Returns:
        pd.DataFrame: DataFrame with datetime and value columns for volume charts.

    Example:
        ```python
        from examples.dataSamples import get_dataframe_volume_data

        df = get_dataframe_volume_data()
        chart = SinglePaneChart(series=HistogramSeries(data=df))
        ```
    """
    return pd.DataFrame(series_volume_chart)


# =============================================================================
# CONVENIENCE FUNCTIONS FOR COMMON USE CASES
# =============================================================================


def get_sample_data_for_chart_type(chart_type: str) -> Union[List, pd.DataFrame]:
    """
    Get sample data for a specific chart type.

    Args:
        chart_type: Type of chart ("line", "candlestick", "volume", "baseline", "area").

    Returns:
        Union[List, pd.DataFrame]: Sample data appropriate for the chart type.

    Raises:
        ValueError: If chart_type is not supported.

    Example:
        ```python
        from examples.dataSamples import get_sample_data_for_chart_type

        # Get data for different chart types
        line_data = get_sample_data_for_chart_type("line")
        candlestick_data = get_sample_data_for_chart_type("candlestick")
        ```
    """
    chart_type = chart_type.lower()

    if chart_type == "line":
        return get_line_data()
    elif chart_type == "candlestick":
        return get_candlestick_data()
    elif chart_type == "volume":
        return get_volume_data()
    elif chart_type == "baseline":
        return get_baseline_data()
    elif chart_type == "area":
        return get_multi_area_data_1()
    elif chart_type == "histogram":
        return get_volume_histogram_data()
    else:
        raise ValueError(f"Unsupported chart type: {chart_type}")


def get_all_sample_datasets() -> Dict[str, Union[List, pd.DataFrame]]:
    """
    Get all available sample datasets.

    Returns:
        Dict[str, Union[List, pd.DataFrame]]: Dictionary mapping chart types to sample data.

    Example:
        ```python
        from examples.dataSamples import get_all_sample_datasets

        datasets = get_all_sample_datasets()
        for chart_type, data in datasets.items():
            print(f"{chart_type}: {len(data)} data points")
        ```
    """
    return {
        "line": get_line_data(),
        "candlestick": get_candlestick_data(),
        "volume": get_volume_data(),
        "baseline": get_baseline_data(),
        "area_1": get_multi_area_data_1(),
        "area_2": get_multi_area_data_2(),
        "histogram": get_volume_histogram_data(),
        "dataframe_line": get_dataframe_line_data(),
        "dataframe_candlestick": get_dataframe_candlestick_data(),
        "dataframe_volume": get_dataframe_volume_data(),
    }
