"""
Streamlit Lightweight Charts Pro - Professional Financial Charting Library.

A comprehensive Python library for creating interactive financial charts in Streamlit
applications. Built on top of TradingView's Lightweight Charts library, this package
provides a fluent API for building sophisticated financial visualizations with
method chaining support.

The library offers enterprise-grade features for financial data visualization
including candlestick charts, line charts, area charts, volume charts, and more.
It supports advanced features like annotations, trade visualization, multi-pane
charts, and seamless pandas DataFrame integration.

Key Features:
    - Fluent API with method chaining for intuitive chart creation
    - Support for all major chart types (candlestick, line, area, bar, histogram)
    - Advanced annotation system with layers and styling
    - Trade visualization with buy/sell markers and PnL display
    - Multi-pane synchronized charts with overlay price scales
    - Responsive design with auto-sizing options
    - Comprehensive customization options for all chart elements
    - Seamless pandas DataFrame integration
    - Type-safe API with comprehensive type hints

Example Usage:
    ```python
    from streamlit_lightweight_charts_pro import (
        Chart, LineSeries, create_text_annotation
    )
    from streamlit_lightweight_charts_pro.data import SingleValueData

    # Create data
    data = [SingleValueData("2024-01-01", 100), SingleValueData("2024-01-02", 105)]

    # Method 1: Direct chart creation
    chart = Chart(series=LineSeries(data, color="#ff0000"))
    chart.render(key="my_chart")

    # Method 2: Fluent API with method chaining
    chart = (Chart()
             .add_series(LineSeries(data, color="#ff0000"))
             .update_options(height=400)
             .add_annotation(create_text_annotation("2024-01-01", 100, "Start")))
    chart.render(key="my_chart")
    ```

For detailed documentation and examples, visit the project repository.

Version: 0.1.0
Author: Streamlit Lightweight Charts Contributors
License: MIT
"""

# TODO: Need to implement tooltips for the chart
# TODO: Need to implement legend for the chart
# TODO: Need to implement background shadding series

# Import core components
from streamlit_lightweight_charts_pro.charts import (
    Chart,
)
from streamlit_lightweight_charts_pro.charts.options import ChartOptions
from streamlit_lightweight_charts_pro.charts.options.trade_visualization_options import (
    TradeVisualizationOptions,
)
from streamlit_lightweight_charts_pro.charts.series import (
    AreaSeries,
    BarSeries,
    BaselineSeries,
    CandlestickSeries,
    HistogramSeries,
    LineSeries,
    Series,
)
from streamlit_lightweight_charts_pro.data import (
    Annotation,
    Marker,
)
from streamlit_lightweight_charts_pro.data.annotation import (
    AnnotationLayer,
    AnnotationManager,
    create_arrow_annotation,
    create_shape_annotation,
    create_text_annotation,
)
from streamlit_lightweight_charts_pro.data.trade import (
    Trade,
    TradeType,
)

# Import logging configuration
from streamlit_lightweight_charts_pro.logging_config import get_logger, setup_logging
from streamlit_lightweight_charts_pro.type_definitions import ChartType, LineStyle, MarkerPosition
from streamlit_lightweight_charts_pro.type_definitions.enums import (
    ColumnNames,
    MarkerShape,
    TradeVisualization,
)

# Version information
__version__ = "0.1.0"

# Export all public components
__all__ = [
    # Logging
    "get_logger",
    "setup_logging",
    # Core chart classes
    "Chart",
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
    "Marker",
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
    "ColumnNames",
    # Version
    "__version__",
]
