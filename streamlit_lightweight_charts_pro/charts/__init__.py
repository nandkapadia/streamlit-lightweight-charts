"""
Chart classes for streamlit-lightweight-charts.

This module provides all chart classes including SinglePaneChart, MultiPaneChart,
PriceVolumeChart, and various series types for creating interactive financial charts.

The module also includes a ChartBuilder class that provides a fluent API for
creating charts with method chaining, making chart creation more intuitive and
readable.

Example:
    ```python
    from streamlit_lightweight_charts_pro.charts import (
        SinglePaneChart, create_chart, ChartBuilder
    )

    # Using ChartBuilder directly
    builder = ChartBuilder()
    chart = (builder
             .add_line_series(data, color="#ff0000")
             .set_height(400)
             .build())

    # Using convenience function
    chart = (create_chart()
             .add_line_series(data, color="#ff0000")
             .set_height(400)
             .build())
    ```
"""

from streamlit_lightweight_charts_pro.charts.chart_builder import ChartBuilder, create_chart
from streamlit_lightweight_charts_pro.charts.multi_pane_chart import MultiPaneChart
from streamlit_lightweight_charts_pro.charts.price_volume_chart import PriceVolumeChart
from streamlit_lightweight_charts_pro.charts.series import (
    AreaSeries,
    BarSeries,
    BaselineSeries,
    CandlestickSeries,
    HistogramSeries,
    LineSeries,
)
from streamlit_lightweight_charts_pro.charts.single_pane_chart import SinglePaneChart

__all__ = [
    "SinglePaneChart",
    "MultiPaneChart",
    "PriceVolumeChart",
    "ChartBuilder",
    "create_chart",
    "AreaSeries",
    "LineSeries",
    "CandlestickSeries",
    "BarSeries",
    "HistogramSeries",
    "BaselineSeries",
]
