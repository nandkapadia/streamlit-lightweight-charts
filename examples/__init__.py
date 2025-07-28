"""
Examples package for streamlit-lightweight-charts-pro.

This package contains example applications demonstrating various chart types
and features of the streamlit-lightweight-charts-pro library.
"""

import os
import sys
from pathlib import Path


def _setup_examples_path():
    """Add the project root to Python path for examples to work from any directory."""
    # Get the project root (two levels up from this file)
    project_root = Path(__file__).parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))


# Setup path when package is imported
_setup_examples_path()

# Import data_samples to make it available at the package level
from .data_samples import (
    get_all_sample_datasets,
    get_bar_data,
    get_baseline_data,
    get_candlestick_data,
    get_dataframe_candlestick_data,
    get_dataframe_line_data,
    get_dataframe_volume_data,
    get_line_data,
    get_multi_area_data_1,
    get_multi_area_data_2,
    get_sample_data_for_chart_type,
    get_volume_data,
    get_volume_histogram_data,
)

__all__ = [
    "get_line_data",
    "get_bar_data",
    "get_candlestick_data",
    "get_volume_data",
    "get_baseline_data",
    "get_multi_area_data_1",
    "get_multi_area_data_2",
    "get_volume_histogram_data",
    "get_dataframe_line_data",
    "get_dataframe_candlestick_data",
    "get_dataframe_volume_data",
    "get_sample_data_for_chart_type",
    "get_all_sample_datasets",
]
