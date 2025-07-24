"""Types module for streamlit-lightweight-charts."""

from streamlit_lightweight_charts_pro.type_definitions.colors import Background, SolidColor, VerticalGradientColor
from streamlit_lightweight_charts_pro.type_definitions.enums import (
    ChartType,
    ColorType,
    CrosshairMode,
    HorzAlign,
    LastPriceAnimationMode,
    LineStyle,
    LineType,
    MarkerPosition,
    MarkerShape,
    PriceScaleMode,
    TrackingActivationMode,
    TrackingExitMode,
    VertAlign,
    ColumnNames,
)
from streamlit_lightweight_charts_pro.type_definitions.protocols import (
    AnnotationProtocol,
    ChartData,
    ChartDataProtocol,
    ChartOptions,
    ChartOptionsProtocol,
    ChartProtocol,
    MarkerProtocol,
    NumericValue,
    SeriesProtocol,
    TimeSeriesDataProtocol,
    TimeValue,
    TooltipProtocol,
    TradeProtocol,
    VisualizationOptionsProtocol,
)

__all__ = [
    # Enums
    "ChartType",
    "ColorType",
    "LineStyle",
    "LineType",
    "CrosshairMode",
    "MarkerPosition",
    "MarkerShape",
    "PriceScaleMode",
    "LastPriceAnimationMode",
    "HorzAlign",
    "VertAlign",
    "TrackingExitMode",
    "TrackingActivationMode",
    "ColumnNames",
    # Colors
    "Background",
    "SolidColor",
    "VerticalGradientColor",
    # Protocols
    "ChartDataProtocol",
    "TimeSeriesDataProtocol",
    "ChartOptionsProtocol",
    "SeriesProtocol",
    "ChartProtocol",
    "MarkerProtocol",
    "TradeProtocol",
    "AnnotationProtocol",
    "TooltipProtocol",
    "VisualizationOptionsProtocol",
    # Type aliases
    "ChartData",
    "ChartOptions",
    "TimeValue",
    "NumericValue",
]
