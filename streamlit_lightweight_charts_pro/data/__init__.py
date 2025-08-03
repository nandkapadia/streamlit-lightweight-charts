"""
Data model classes for streamlit-lightweight-charts.

This module provides the core data models used throughout the library for
representing financial data points, markers, and other chart elements.

The data models are designed to be flexible and support various input formats
while maintaining consistency in the internal representation.
"""

from streamlit_lightweight_charts_pro.charts.options.trade_visualization_options import (
    TradeVisualizationOptions,
)

# Import annotation classes
from streamlit_lightweight_charts_pro.data.annotation import (
    Annotation,
    AnnotationLayer,
    AnnotationManager,
    AnnotationPosition,
    AnnotationType,
    create_arrow_annotation,
    create_shape_annotation,
    create_text_annotation,
)

# Import area and bar data classes
from streamlit_lightweight_charts_pro.data.area_data import AreaData

# Import band data classes
from streamlit_lightweight_charts_pro.data.band import BandData
from streamlit_lightweight_charts_pro.data.bar_data import BarData
from streamlit_lightweight_charts_pro.data.baseline_data import BaselineData

# Import OHLC data classes
from streamlit_lightweight_charts_pro.data.candlestick_data import CandlestickData

# Import base data classes
from streamlit_lightweight_charts_pro.data.data import Data
from streamlit_lightweight_charts_pro.data.histogram_data import HistogramData

# Import single value data classes
from streamlit_lightweight_charts_pro.data.line_data import LineData

# Import marker classes
from streamlit_lightweight_charts_pro.data.marker import Marker
from streamlit_lightweight_charts_pro.data.ohlcv_data import OhlcvData
from streamlit_lightweight_charts_pro.data.single_value_data import SingleValueData

# Import trade classes
from streamlit_lightweight_charts_pro.data.trade import (
    TradeData,
    TradeType,
)
from streamlit_lightweight_charts_pro.type_definitions.enums import TradeVisualization

# Import signal data classes
from streamlit_lightweight_charts_pro.data.signal_data import SignalData

# Re-export all classes for backward compatibility
__all__ = [
    # Base data classes
    "Data",
    # Single value data classes
    "SingleValueData",
    "LineData",
    "HistogramData",
    # Area and bar data classes
    "AreaData",
    "BarData",
    "BaselineData",
    # OHLC data classes
    "CandlestickData",
    "OhlcvData",
    # Band data classes
    "BandData",
    # Marker classes
    "Marker",
    # Trade classes
    "TradeData",
    "TradeType",
    "TradeVisualization",
    "TradeVisualizationOptions",
    # Annotation classes
    "Annotation",
    "AnnotationLayer",
    "AnnotationManager",
    "AnnotationPosition",
    "AnnotationType",
    "create_arrow_annotation",
    "create_shape_annotation",
    "create_text_annotation",
    # Signal data classes
    "SignalData",
]
