"""
Streamlit Lightweight Charts - Enhanced OOP Implementation

A comprehensive financial charting library for Streamlit with enhanced trade visualization
and annotation systems, built on TradingView's lightweight-charts.

This module provides a complete object-oriented API for creating financial charts in Streamlit
applications, including candlestick charts, line charts, area charts, and more. It supports
advanced features like trade visualization, annotations, multi-pane synchronized charts,
and seamless pandas DataFrame integration.

Example:
    ```python
    from streamlit_lightweight_charts import CandlestickChart, render_chart
    from streamlit_lightweight_charts.data import OhlcData

    # Create candlestick data
    data = [OhlcData("2024-01-01", 100, 105, 98, 102)]

    # Create and render chart
    chart = CandlestickChart(data=data)
    render_chart(chart, key="my_chart")
    ```

Version: 0.8.0
Author: Streamlit Lightweight Charts Contributors
"""

# pylint: disable=wrong-import-position

import os
from typing import Any, Dict, List, Optional

import streamlit.components.v1 as components

# Component setup constants
_COMPONENT_NAME = "streamlit_lightweight_charts"
_RELEASE = True  # Set to False for development mode

# Get the directory containing this file and locate the frontend build
parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "frontend", "build")

# Ensure the frontend build directory exists before proceeding
if not os.path.exists(build_dir):
    raise FileNotFoundError(
        f"Frontend build directory not found: {build_dir}. "
        "Please run 'npm install && npm run build' in the frontend directory."
    )

# Declare the Streamlit component based on release mode
if not _RELEASE:
    # Development mode: use local development server
    _component_func = components.declare_component(
        _COMPONENT_NAME,
        url="http://localhost:3001",
    )
else:
    # Production mode: use built frontend files
    _component_func = components.declare_component(_COMPONENT_NAME, path=build_dir)

# Export the component function for internal use
__all__ = ["_component_func"]

# Import all chart classes
from .charts import (
    AreaChart,
    AreaSeries,
    AreaSeriesOptions,
    BarChart,
    BarSeries,
    BarSeriesOptions,
    BaselineChart,
    BaselineSeries,
    BaselineSeriesOptions,
    CandlestickChart,
    CandlestickSeries,
    CandlestickSeriesOptions,
    Chart,
    ChartOptions,
    ComparisonChart,
    CrosshairLineOptions,
    CrosshairOptions,
    GridLineOptions,
    GridOptions,
    HistogramChart,
    HistogramSeries,
    HistogramSeriesOptions,
    LayoutOptions,
    LegendOptions,
    LineChart,
    LineSeries,
    LineSeriesOptions,
    MultiPaneChart,
    PriceScaleMargins,
    PriceScaleOptions,
    PriceVolumeChart,
    RangeConfig,
    RangeSwitcherOptions,
    Series,
    TimeScaleOptions,
    WatermarkOptions,
)

# Import all data models
from .data import (
    Annotation,
    AnnotationLayer,
    AnnotationManager,
    AnnotationPosition,
    AnnotationType,
    BaselineData,
    HistogramData,
    Marker,
    MarkerPosition,
    MarkerShape,
    OhlcData,
    OhlcvData,
    SingleValueData,
    Trade,
    TradeType,
    TradeVisualization,
    TradeVisualizationOptions,
    create_arrow_annotation,
    create_shape_annotation,
    create_text_annotation,
)

# Import rendering function
from .rendering import render_chart, render_multi_pane_chart
from .type_definitions.colors import (
    Background,
    SolidColor,
    VerticalGradientColor,
)

# Import types and enums
from .type_definitions.enums import (
    ChartType,
    ColorType,
    CrosshairMode,
    HorzAlign,
    LastPriceAnimationMode,
    LineStyle,
    LineType,
    PriceScaleMode,
    VertAlign,
)
from .type_definitions.protocols import ChartData

# Import all utilities
from .utils import (
    add_trades_to_series,
    area_chart_from_df,
    bar_chart_from_df,
    baseline_chart_from_df,
    candlestick_chart_from_df,
    create_trade_shapes_series,
    df_to_baseline_data,
    df_to_data,
    df_to_histogram_data,
    df_to_line_data,
    df_to_ohlc_data,
    df_to_ohlcv_data,
    histogram_chart_from_df,
    line_chart_from_df,
    resample_df_for_charts,
    trades_to_visual_elements,
)


# Original renderLightweightCharts function for backward compatibility
# pylint: disable=invalid-name
def renderLightweightCharts(charts: List[Dict[str, Any]], key: Optional[str] = None) -> Any:
    """
    Original renderLightweightCharts function for backward compatibility.

    This function maintains compatibility with the old dictionary-based API while
    delegating to the new render_chart function.

    Args:
        charts: List of chart configurations as dictionaries. Each dictionary should
            contain 'chart' and 'series' keys with appropriate configuration.
        key: Unique key for the Streamlit component. Used to prevent conflicts when
            multiple charts are rendered on the same page.

    Returns:
        The rendered Streamlit component result.

    Example:
        ```python
        charts_config = [{
            "chart": {"height": 400},
            "series": [{"type": "Line", "data": [...]}]
        }]
        renderLightweightCharts(charts_config, key="my_chart")
        ```
    """
    return render_chart(charts, key=key)


# Import data samples
from .dataSamples import (
    price_volume_series_area,
    series_bar_chart,
    series_baseline_chart,
    series_candlestick_chart,
    series_histogram_chart,
    series_multiple_chart_area_01,
    series_multiple_chart_area_02,
    series_single_value_data,
)

# Version and metadata information
__version__ = "0.8.0"
__author__ = "Streamlit Lightweight Charts Contributors"
__description__ = "Enhanced financial charting library for Streamlit with OOP architecture"

# Main exports - comprehensive list of all public API components
__all__ = [
    # Core chart classes
    "Chart",
    "MultiPaneChart",
    "CandlestickChart",
    "LineChart",
    "AreaChart",
    "BarChart",
    "HistogramChart",
    "BaselineChart",
    "PriceVolumeChart",
    "ComparisonChart",
    # Chart options
    "ChartOptions",
    "LayoutOptions",
    "GridOptions",
    "GridLineOptions",
    "CrosshairOptions",
    "CrosshairLineOptions",
    "PriceScaleOptions",
    "TimeScaleOptions",
    "PriceScaleMargins",
    "WatermarkOptions",
    "LegendOptions",
    # Series classes
    "Series",
    "AreaSeries",
    "LineSeries",
    "BarSeries",
    "CandlestickSeries",
    "HistogramSeries",
    "BaselineSeries",
    "AreaSeriesOptions",
    "LineSeriesOptions",
    "BarSeriesOptions",
    "CandlestickSeriesOptions",
    "HistogramSeriesOptions",
    "BaselineSeriesOptions",
    # Data models
    "SingleValueData",
    "OhlcData",
    "OhlcvData",
    "HistogramData",
    "BaselineData",
    "Marker",
    "MarkerShape",
    "MarkerPosition",
    # Trade visualization
    "Trade",
    "TradeType",
    "TradeVisualization",
    "TradeVisualizationOptions",
    # Annotation system
    "Annotation",
    "AnnotationLayer",
    "AnnotationManager",
    "AnnotationType",
    "AnnotationPosition",
    "create_text_annotation",
    "create_arrow_annotation",
    "create_shape_annotation",
    # Utilities
    "df_to_line_data",
    "df_to_ohlc_data",
    "df_to_ohlcv_data",
    "df_to_histogram_data",
    "df_to_baseline_data",
    "df_to_data",
    "resample_df_for_charts",
    "candlestick_chart_from_df",
    "line_chart_from_df",
    "area_chart_from_df",
    "bar_chart_from_df",
    "histogram_chart_from_df",
    "baseline_chart_from_df",
    "trades_to_visual_elements",
    "create_trade_shapes_series",
    "add_trades_to_series",
    # Types and enums
    "ChartType",
    "ColorType",
    "LineStyle",
    "LineType",
    "CrosshairMode",
    "LastPriceAnimationMode",
    "PriceScaleMode",
    "HorzAlign",
    "VertAlign",
    # Colors
    "SolidColor",
    "VerticalGradientColor",
    "Background",
    # Protocols
    "ChartData",
    # Rendering
    "render_chart",
    "render_multi_pane_chart",
    "renderLightweightCharts",
    # Data samples
    "series_single_value_data",
    "series_baseline_chart",
    "series_histogram_chart",
    "series_bar_chart",
    "series_candlestick_chart",
    "series_multiple_chart_area_01",
    "series_multiple_chart_area_02",
    "price_volume_series_area",
    # Version info
    "__version__",
    "__author__",
    "__description__",
]
