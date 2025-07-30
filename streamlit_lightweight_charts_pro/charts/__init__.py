"""
Chart classes for streamlit-lightweight-charts.

This module provides all chart classes including Chart and various series types
for creating interactive financial charts.

The Chart class provides a fluent API for creating charts with method chaining,
making chart creation more intuitive and readable.

Example:
    ```python
    from streamlit_lightweight_charts_pro.charts import Chart

    # Using Chart directly
    chart = Chart()
    chart.add_series(LineSeries(data))
    chart.update_options(height=400)
    chart.render()
    ```
"""

from streamlit_lightweight_charts_pro.charts.chart import Chart
from streamlit_lightweight_charts_pro.charts.series import (
    AreaSeries,
    BarSeries,
    BaselineSeries,
    CandlestickSeries,
    HistogramSeries,
    LineSeries,
)

__all__ = [
    "AreaSeries",
    "LineSeries",
    "CandlestickSeries",
    "BarSeries",
    "HistogramSeries",
    "BaselineSeries",
    "Chart",
]
