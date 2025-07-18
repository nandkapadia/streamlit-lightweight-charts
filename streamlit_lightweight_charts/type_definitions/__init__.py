"""Types module for streamlit-lightweight-charts."""

from .colors import Background, SolidColor, VerticalGradientColor
from .enums import (
    ChartType,
    ColorType,
    CrosshairMode,
    HorzAlign,
    LastPriceAnimationMode,
    LineStyle,
    LineType,
    PriceScaleMode,
    TrackingActivationMode,
    TrackingExitMode,
    VertAlign,
)
from .protocols import (
    AnnotationProtocol,
    ChartData,
    ChartDataProtocol,
    ChartOptions,
    ChartOptionsProtocol,
    ChartProtocol,
    MarkerProtocol,
    NumericValue,
    SeriesOptions,
    SeriesOptionsProtocol,
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
    "PriceScaleMode",
    "LastPriceAnimationMode",
    "HorzAlign",
    "VertAlign",
    "TrackingExitMode",
    "TrackingActivationMode",
    # Colors
    "Background",
    "SolidColor",
    "VerticalGradientColor",
    # Protocols
    "ChartDataProtocol",
    "TimeSeriesDataProtocol",
    "SeriesOptionsProtocol",
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
    "SeriesOptions",
    "ChartOptions",
    "TimeValue",
    "NumericValue",
]
