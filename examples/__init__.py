"""
Examples package for streamlit-lightweight-charts-pro.

This package contains example applications demonstrating various chart types
and features of the streamlit-lightweight-charts-pro library.
"""

# Import data_samples to make it available at the package level
from .data_samples import (
    get_line_data,
    get_bar_data,
    get_candlestick_data,
    get_volume_data,
    get_baseline_data,
    get_multi_area_data_1,
    get_multi_area_data_2,
    get_volume_histogram_data,
    get_dataframe_line_data,
    get_dataframe_candlestick_data,
    get_dataframe_volume_data,
    get_sample_data_for_chart_type,
    get_all_sample_datasets,
)

__all__ = [
    'get_line_data',
    'get_bar_data',
    'get_candlestick_data',
    'get_volume_data',
    'get_baseline_data',
    'get_multi_area_data_1',
    'get_multi_area_data_2',
    'get_volume_histogram_data',
    'get_dataframe_line_data',
    'get_dataframe_candlestick_data',
    'get_dataframe_volume_data',
    'get_sample_data_for_chart_type',
    'get_all_sample_datasets',
] 