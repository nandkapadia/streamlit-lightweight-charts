"""
Enum definitions for streamlit-lightweight-charts.

This module contains all the enumeration types used throughout the library
for defining chart types, styling options, and configuration parameters.
These enums ensure type safety and provide a consistent interface for
chart configuration.
"""

from enum import Enum, IntEnum


class ChartType(str, Enum):
    """
    Chart type enumeration.

    Defines the available chart types that can be created and rendered.
    Each chart type corresponds to a specific visualization style and
    data format requirements.

    Attributes:
        AREA: Area chart - filled area below a line.
        BAND: Band chart - multiple lines with fill areas (e.g., Bollinger Bands).
        BASELINE: Baseline chart - values relative to a baseline.
        HISTOGRAM: Histogram chart - bar chart for volume or distribution.
        LINE: Line chart - simple line connecting data points.
        BAR: Bar chart - OHLC bars for price data.
        CANDLESTICK: Candlestick chart - traditional Japanese candlesticks.
    """

    AREA = "Area"
    BAND = "Band"
    BASELINE = "Baseline"
    HISTOGRAM = "Histogram"
    LINE = "Line"
    BAR = "Bar"
    CANDLESTICK = "Candlestick"


class ColorType(str, Enum):
    """
    Color type enumeration.

    Defines how colors should be applied to chart elements.
    Controls whether colors are solid or use gradient effects.

    Attributes:
        SOLID: Solid color - uniform color across the element.
        VERTICAL_GRADIENT: Vertical gradient - color gradient from top to bottom.
    """

    SOLID = "solid"
    VERTICAL_GRADIENT = "gradient"


class LineStyle(IntEnum):
    """
    Line style enumeration.

    Defines the visual style of lines in charts, including borders,
    grid lines, and series lines.

    Attributes:
        SOLID: Solid line - continuous line without breaks.
        DOTTED: Dotted line - series of dots.
        DASHED: Dashed line - series of short dashes.
        LARGE_DASHED: Large dashed line - series of long dashes.
    """

    SOLID = 0
    DOTTED = 1
    DASHED = 2
    LARGE_DASHED = 3


class LineType(IntEnum):
    """
    Line type enumeration.

    Defines how lines should be drawn between data points.
    Controls the interpolation method used for line series.

    Attributes:
        SIMPLE: Simple line - straight lines between points.
        CURVED: Curved line - smooth curves between points.
    """

    SIMPLE = 0
    CURVED = 1


class CrosshairMode(IntEnum):
    """
    Crosshair mode enumeration.

    Defines how the crosshair behaves when hovering over the chart.
    Controls whether the crosshair snaps to data points or moves freely.

    Attributes:
        NORMAL: Normal mode - crosshair moves freely across the chart.
        MAGNET: Magnet mode - crosshair snaps to nearest data points.
    """

    NORMAL = 0
    MAGNET = 1


class LastPriceAnimationMode(IntEnum):
    """
    Last price animation mode enumeration.

    Defines how the last price line should be animated when new data
    is added to the chart.

    Attributes:
        DISABLED: No animation - last price line updates instantly.
        CONTINUOUS: Continuous animation - smooth transitions for all updates.
        ON_DATA_UPDATE: Update animation - animation only when new data arrives.
    """

    DISABLED = 0
    CONTINUOUS = 1
    ON_DATA_UPDATE = 2


class PriceScaleMode(IntEnum):
    """
    Price scale mode enumeration.

    Defines how the price scale (y-axis) should be displayed and calculated.
    Controls the scale type and reference point for price values.

    Attributes:
        NORMAL: Normal scale - linear price scale.
        LOGARITHMIC: Logarithmic scale - log-based price scale.
        PERCENTAGE: Percentage scale - values as percentages.
        INDEXED_TO_100: Indexed scale - values relative to 100.
    """

    NORMAL = 0
    LOGARITHMIC = 1
    PERCENTAGE = 2
    INDEXED_TO_100 = 3


class HorzAlign(str, Enum):
    """
    Horizontal alignment enumeration.

    Defines horizontal text alignment for labels, annotations, and
    other text elements on the chart.

    Attributes:
        LEFT: Left alignment - text aligned to the left.
        CENTER: Center alignment - text centered horizontally.
        RIGHT: Right alignment - text aligned to the right.
    """

    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"


class VertAlign(str, Enum):
    """
    Vertical alignment enumeration.

    Defines vertical text alignment for labels, annotations, and
    other text elements on the chart.

    Attributes:
        TOP: Top alignment - text aligned to the top.
        CENTER: Center alignment - text centered vertically.
        BOTTOM: Bottom alignment - text aligned to the bottom.
    """

    TOP = "top"
    CENTER = "center"
    BOTTOM = "bottom"


class TrackingExitMode(str, Enum):
    """
    Tracking exit mode enumeration.

    Defines when the tracking mode should exit.

    Attributes:
        EXIT_ON_MOVE: Exit tracking mode when mouse moves.
        EXIT_ON_CROSS: Exit tracking mode when crosshair crosses series.
        NEVER_EXIT: Never exit tracking mode automatically.
    """

    EXIT_ON_MOVE = "EXIT_ON_MOVE"
    EXIT_ON_CROSS = "EXIT_ON_CROSS"
    NEVER_EXIT = "NEVER_EXIT"


class TrackingActivationMode(str, Enum):
    """
    Tracking activation mode enumeration.

    Defines when the tracking mode should be activated.

    Attributes:
        ON_MOUSE_ENTER: Activate tracking mode when mouse enters chart.
        ON_TOUCH_START: Activate tracking mode when touch starts.
    """

    ON_MOUSE_ENTER = "ON_MOUSE_ENTER"
    ON_TOUCH_START = "ON_TOUCH_START"
