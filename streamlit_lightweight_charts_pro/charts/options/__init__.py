"""Chart options package for streamlit-lightweight-charts.

This package contains all chart option classes organized by functionality:
- base_options.py: Base Options class for all option classes
- chart_options.py: Main ChartOptions class
- layout_options.py: Layout, Grid, Watermark options
- interaction_options.py: Crosshair, KineticScroll, TrackingMode options
- scale_options.py: TimeScale options
- price_scale_options.py: PriceScaleOptions options
- ui_options.py: Legend and RangeSwitcher options
- localization_options.py: Localization options
- trade_visualization_options.py: Trade visualization options
"""

from streamlit_lightweight_charts_pro.charts.options.base_options import Options
from streamlit_lightweight_charts_pro.charts.options.chart_options import ChartOptions
from streamlit_lightweight_charts_pro.charts.options.interaction_options import (
    CrosshairLineOptions,
    CrosshairOptions,
    CrosshairSyncOptions,
    KineticScrollOptions,
    TrackingModeOptions,
)
from streamlit_lightweight_charts_pro.charts.options.layout_options import (
    GridLineOptions,
    GridOptions,
    LayoutOptions,
    PaneHeightOptions,
    WatermarkOptions,
)
from streamlit_lightweight_charts_pro.charts.options.line_options import LineOptions
from streamlit_lightweight_charts_pro.charts.options.localization_options import LocalizationOptions
from streamlit_lightweight_charts_pro.charts.options.price_format_options import PriceFormatOptions
from streamlit_lightweight_charts_pro.charts.options.price_line_options import PriceLineOptions
from streamlit_lightweight_charts_pro.charts.options.price_scale_options import (
    PriceScaleMargins,
    PriceScaleOptions,
)
from streamlit_lightweight_charts_pro.charts.options.time_scale_options import TimeScaleOptions
from streamlit_lightweight_charts_pro.charts.options.trade_visualization_options import (
    TradeVisualizationOptions,
)
from streamlit_lightweight_charts_pro.charts.options.signal_options import SignalOptions
from streamlit_lightweight_charts_pro.charts.options.ui_options import (
    LegendOptions,
    RangeConfig,
    RangeSwitcherOptions,
)

__all__ = [
    # Base options class
    "Options",
    # Main chart options
    "ChartOptions",
    # Line options
    "LineOptions",
    # Price options
    "PriceLineOptions",
    "PriceFormatOptions",
    # Layout options
    "GridLineOptions",
    "GridOptions",
    "LayoutOptions",
    "PaneHeightOptions",
    "WatermarkOptions",
    # Interaction options
    "CrosshairLineOptions",
    "CrosshairOptions",
    "CrosshairSyncOptions",
    "KineticScrollOptions",
    "TrackingModeOptions",
    # Scale options
    "TimeScaleOptions",
    "PriceScaleOptions",
    "PriceScaleMargins",
    # UI options
    "LegendOptions",
    "RangeConfig",
    "RangeSwitcherOptions",
    # Localization options
    "LocalizationOptions",
    # Trade visualization options
    "TradeVisualizationOptions",
    # Signal options
    "SignalOptions",
]
