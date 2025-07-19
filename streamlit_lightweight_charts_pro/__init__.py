"""
Streamlit Lightweight Charts Pro - Enhanced Financial Charting Library.

This package provides a comprehensive set of tools for creating interactive
financial charts in Streamlit applications with method chaining support.

The library offers a fluent API for building complex financial visualizations
including candlestick charts, line charts, area charts, volume charts, and more.
It supports advanced features like annotations, trade visualization, multi-pane
charts, and seamless pandas DataFrame integration.

Key Features:
    - Fluent API with method chaining for intuitive chart creation
    - Support for all major chart types (candlestick, line, area, bar, histogram)
    - Advanced annotation system with layers and styling
    - Trade visualization with buy/sell markers
    - Multi-pane synchronized charts
    - Responsive design with auto-sizing options
    - Comprehensive customization options

Example Usage:
    ```python
    from streamlit_lightweight_charts_pro import (
        SinglePaneChart, LineSeries, create_chart, create_text_annotation
    )
    from streamlit_lightweight_charts_pro.data import SingleValueData

    # Create data
    data = [SingleValueData("2024-01-01", 100), SingleValueData("2024-01-02", 105)]

    # Method 1: Direct chart creation
    chart = SinglePaneChart(series=LineSeries(data, color="#ff0000"))
    chart.render(key="my_chart")

    # Method 2: Fluent API with method chaining
    chart = (create_chart()
             .add_line_series(data, color="#ff0000")
             .set_height(400)
             .add_annotation(create_text_annotation("2024-01-01", 100, "Start"))
             .build())
    chart.render(key="my_chart")
    ```

Version: 1.0.0
Author: Streamlit Lightweight Charts Contributors
License: MIT
"""

# TODO: Need to implement the Y Axis Scaling when cursor is on the Y Axis
# TODO: Need to implement tooltips for the chart
# TODO: Need to implement legend for the chart

# Import core components
from .charts import (
    ChartBuilder,
    MultiPaneChart,
    PriceVolumeChart,
    SinglePaneChart,
    create_chart,
)
from .charts.options import ChartOptions
from .charts.series import (
    AreaSeries,
    BarSeries,
    BaselineSeries,
    CandlestickSeries,
    HistogramSeries,
    LineSeries,
    Series,
)
from .data import (
    Annotation,
    BaselineData,
    HistogramData,
    Marker,
    MarkerPosition,
    MarkerShape,
    OhlcData,
    OhlcvData,
    SingleValueData,
)
from .data.annotation import (
    AnnotationLayer,
    AnnotationManager,
    create_arrow_annotation,
    create_shape_annotation,
    create_text_annotation,
)
from .data.trade import (
    Trade,
    TradeType,
    TradeVisualization,
    TradeVisualizationOptions,
)
from .type_definitions import ChartType, LineStyle

# Version information
__version__ = "1.0.0"

# Export all public components
__all__ = [
    # Core chart classes
    "SinglePaneChart",
    "MultiPaneChart",
    "PriceVolumeChart",
    "create_chart",
    "ChartBuilder",
    # Series classes
    "AreaSeries",
    "BarSeries",
    "BaselineSeries",
    "CandlestickSeries",
    "HistogramSeries",
    "LineSeries",
    "Series",
    # Options
    "ChartOptions",
    # Data models
    "Annotation",
    "BaselineData",
    "HistogramData",
    "Marker",
    "OhlcData",
    "OhlcvData",
    "SingleValueData",
    # Annotation system
    "AnnotationManager",
    "AnnotationLayer",
    "create_text_annotation",
    "create_arrow_annotation",
    "create_shape_annotation",
    # Trade visualization
    "Trade",
    "TradeType",
    "TradeVisualizationOptions",
    "TradeVisualization",
    # Type definitions
    "ChartType",
    "LineStyle",
    "MarkerShape",
    "MarkerPosition",
    # Version
    "__version__",
]
