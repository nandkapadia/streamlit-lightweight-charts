"""Chart options package for streamlit-lightweight-charts.

This package contains all chart option classes organized by functionality:
- chart_options.py: Main ChartOptions class
- layout_options.py: Layout, Grid, Watermark options
- interaction_options.py: Crosshair, KineticScroll, TrackingMode options
- scale_options.py: TimeScale options
- price_scale_options.py: PriceScale options
- ui_options.py: Legend and RangeSwitcher options
- localization_options.py: Localization options
"""

from streamlit_lightweight_charts_pro.charts.options.chart_options import ChartOptions
from streamlit_lightweight_charts_pro.charts.options.interaction_options import (
    CrosshairLineOptions,
    CrosshairOptions,
    CrosshairSyncOptions,
    KineticScrollOptions,
    TrackingModeOptions,
)
from streamlit_lightweight_charts_pro.charts.options.layout_options import GridLineOptions, GridOptions, LayoutOptions, WatermarkOptions
from streamlit_lightweight_charts_pro.charts.options.localization_options import LocalizationOptions
from streamlit_lightweight_charts_pro.charts.options.price_scale_options import (
    PriceScaleOptions,
    RightPriceScaleOptions,
    LeftPriceScaleOptions,
    OverlayPriceScaleOptions,
    PriceScaleMargins,
    # Backward compatibility aliases
    PriceScale,
    RightPriceScale,
    LeftPriceScale,
    OverlayPriceScale,
)
from streamlit_lightweight_charts_pro.charts.options.scale_options import TimeScaleOptions
from streamlit_lightweight_charts_pro.charts.options.ui_options import LegendOptions, RangeConfig, RangeSwitcherOptions

__all__ = [
    # Main chart options
    "ChartOptions",
    # Layout options
    "GridLineOptions",
    "GridOptions", 
    "LayoutOptions",
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
    "RightPriceScaleOptions", 
    "LeftPriceScaleOptions",
    "OverlayPriceScaleOptions",
    "PriceScaleMargins",
    # Backward compatibility aliases
    "PriceScale",
    "RightPriceScale",
    "LeftPriceScale",
    "OverlayPriceScale",
    # UI options
    "LegendOptions",
    "RangeConfig",
    "RangeSwitcherOptions",
    # Localization options
    "LocalizationOptions",
] 