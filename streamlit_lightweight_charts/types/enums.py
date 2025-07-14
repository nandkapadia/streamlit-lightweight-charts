"""Enum definitions for streamlit-lightweight-charts."""

from enum import Enum, IntEnum


class ChartType(str, Enum):
    """Chart type enumeration."""
    
    AREA = 'Area'
    BASELINE = 'Baseline'
    HISTOGRAM = 'Histogram'
    LINE = 'Line'
    BAR = 'Bar'
    CANDLESTICK = 'Candlestick'


class ColorType(str, Enum):
    """Color type enumeration."""
    
    SOLID = 'solid'
    VERTICAL_GRADIENT = 'gradient'


class LineStyle(IntEnum):
    """Line style enumeration."""
    
    SOLID = 0
    DOTTED = 1
    DASHED = 2
    LARGE_DASHED = 3


class LineType(IntEnum):
    """Line type enumeration."""
    
    SIMPLE = 0
    CURVED = 1


class CrosshairMode(IntEnum):
    """Crosshair mode enumeration."""
    
    NORMAL = 0
    MAGNET = 1


class LastPriceAnimationMode(IntEnum):
    """Last price animation mode enumeration."""
    
    DISABLED = 0
    CONTINUOUS = 1
    ON_DATA_UPDATE = 2


class PriceScaleMode(IntEnum):
    """Price scale mode enumeration."""
    
    NORMAL = 0
    LOGARITHMIC = 1
    PERCENTAGE = 2
    INDEXED_TO_100 = 3


class HorzAlign(str, Enum):
    """Horizontal alignment enumeration."""
    
    LEFT = 'left'
    CENTER = 'center'
    RIGHT = 'right'


class VertAlign(str, Enum):
    """Vertical alignment enumeration."""
    
    TOP = 'top'
    CENTER = 'center'
    BOTTOM = 'bottom'