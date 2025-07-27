"""
Chart options configuration for streamlit-lightweight-charts.

This module provides the main ChartOptions class for configuring chart display,
behavior, and appearance. ChartOptions serves as the central configuration
container for all chart-related settings including layout, interaction,
localization, and trade visualization features.
"""

from dataclasses import dataclass, field
from typing import Dict, Optional

from streamlit_lightweight_charts_pro.charts.options.base_options import Options
from streamlit_lightweight_charts_pro.charts.options.interaction_options import (
    CrosshairOptions,
    KineticScrollOptions,
    TrackingModeOptions,
)
from streamlit_lightweight_charts_pro.charts.options.layout_options import (
    GridOptions,
    LayoutOptions,
)
from streamlit_lightweight_charts_pro.charts.options.localization_options import LocalizationOptions
from streamlit_lightweight_charts_pro.charts.options.price_scale_options import PriceScaleOptions
from streamlit_lightweight_charts_pro.charts.options.time_scale_options import TimeScaleOptions
from streamlit_lightweight_charts_pro.charts.options.trade_visualization_options import (
    TradeVisualizationOptions,
)


@dataclass
class ChartOptions(Options):
    """
    Configuration options for chart display and behavior.

    This class encapsulates all the configuration options that control how a chart
    is displayed, including its size, layout, grid settings, and various interactive
    features. It provides a comprehensive interface for customizing chart appearance
    and behavior.

    Attributes:
        width (Optional[int]): Chart width in pixels. If None, uses 100% of container width.
        height (int): Chart height in pixels. Defaults to 400.
        auto_size (bool): Whether to automatically size the chart to fit its container.
        layout (LayoutOptions): Chart layout configuration (background, text colors, etc.).
        left_price_scale (Optional[PriceScaleOptions]): Left price scale configuration.
        right_price_scale (PriceScaleOptions): Right price scale configuration.
        overlay_price_scales (Dict[str, PriceScaleOptions]): Overlay price scale configurations.
        time_scale (TimeScaleOptions): Time scale configuration (axis, time formatting, etc.).
        crosshair (CrosshairOptions): Crosshair configuration for mouse interactions.
        grid (GridOptions): Grid configuration (horizontal and vertical grid lines).
        handle_scroll (bool): Whether to enable scroll interactions.
        handle_scale (bool): Whether to enable scale interactions.
        kinetic_scroll (Optional[KineticScrollOptions]): Kinetic scroll options.
        tracking_mode (Optional[TrackingModeOptions]): Mouse tracking mode for crosshair and tooltips.
        localization (Optional[LocalizationOptions]): Localization settings for date/time formatting.
        add_default_pane (bool): Whether to add a default pane to the chart.
        trade_visualization (Optional[TradeVisualizationOptions]): Trade visualization configuration 
            options.

    Raises:
        TypeError: If any attribute is assigned an invalid type during initialization.

    Example:
        ```python
        from streamlit_lightweight_charts_pro import ChartOptions
        from streamlit_lightweight_charts_pro.charts.options.layout_options import LayoutOptions

        # Create custom chart options
        options = ChartOptions(
            width=800,
            height=600,
            layout=LayoutOptions(background_color="#ffffff"),
            handle_scroll=True,
            handle_scale=True
        )
        ```
    """

    # Size and layout options
    width: Optional[int] = None
    height: int = 400
    auto_size: bool = True

    # Layout and appearance
    layout: LayoutOptions = field(default_factory=LayoutOptions)
    left_price_scale: Optional[PriceScaleOptions] = None
    right_price_scale: PriceScaleOptions = field(default_factory=PriceScaleOptions)
    overlay_price_scales: Dict[str, PriceScaleOptions] = field(default_factory=dict)
    time_scale: TimeScaleOptions = field(default_factory=TimeScaleOptions)

    # Interaction options
    crosshair: CrosshairOptions = field(default_factory=CrosshairOptions)
    grid: GridOptions = field(default_factory=GridOptions)
    handle_scroll: bool = True
    handle_scale: bool = True
    kinetic_scroll: Optional[KineticScrollOptions] = None
    tracking_mode: Optional[TrackingModeOptions] = None

    # Localization and UI
    localization: Optional[LocalizationOptions] = None
    add_default_pane: bool = True

    # Trade visualization options
    trade_visualization: Optional[TradeVisualizationOptions] = None

    def __post_init__(self):
        """
        Post-initialization validation of all chart options.

        Validates that all attributes have the correct types and raises
        TypeError for any invalid assignments.

        Raises:
            TypeError: If any attribute has an invalid type.
        """
        super().__post_init__()
        # Validate size fields
        if self.width is not None and not isinstance(self.width, int):
            raise TypeError(f"width must be an int or None, got {type(self.width)}")
        if not isinstance(self.height, int):
            raise TypeError(f"height must be an int, got {type(self.height)}")
        if not isinstance(self.auto_size, bool):
            raise TypeError(f"auto_size must be a bool, got {type(self.auto_size)}")

        # Validate layout and scale fields
        if not isinstance(self.layout, LayoutOptions):
            raise TypeError(f"layout must be a LayoutOptions instance, got {type(self.layout)}")
        if self.left_price_scale is not None and not isinstance(
            self.left_price_scale, PriceScaleOptions
        ):
            raise TypeError(
                f"left_price_scale must be a PriceScaleOptions instance or None, "
                f"got {type(self.left_price_scale)}"
            )
        if not isinstance(self.right_price_scale, PriceScaleOptions):
            raise TypeError(
                f"right_price_scale must be a PriceScaleOptions instance, "
                f"got {type(self.right_price_scale)}"
            )
        if not isinstance(self.overlay_price_scales, dict):
            raise TypeError(
                f"overlay_price_scales must be a dict, got {type(self.overlay_price_scales)}"
            )
        for key, value in self.overlay_price_scales.items():
            if not isinstance(value, PriceScaleOptions):
                raise TypeError(
                    f"overlay_price_scales[{key}] must be a PriceScaleOptions instance, "
                    f"got {type(value)}"
                )
        if not isinstance(self.time_scale, TimeScaleOptions):
            raise TypeError(
                f"time_scale must be a TimeScaleOptions instance, got {type(self.time_scale)}"
            )

        # Validate interaction fields
        if not isinstance(self.crosshair, CrosshairOptions):
            raise TypeError(
                f"crosshair must be a CrosshairOptions instance, got {type(self.crosshair)}"
            )
        if not isinstance(self.grid, GridOptions):
            raise TypeError(f"grid must be a GridOptions instance, got {type(self.grid)}")
        if not isinstance(self.handle_scroll, bool):
            raise TypeError(f"handle_scroll must be a bool, got {type(self.handle_scroll)}")
        if not isinstance(self.handle_scale, bool):
            raise TypeError(f"handle_scale must be a bool, got {type(self.handle_scale)}")
        if self.kinetic_scroll is not None and not isinstance(
            self.kinetic_scroll, KineticScrollOptions
        ):
            raise TypeError(
                f"kinetic_scroll must be a KineticScrollOptions instance or None, "
                f"got {type(self.kinetic_scroll)}"
            )
        if self.tracking_mode is not None and not isinstance(
            self.tracking_mode, TrackingModeOptions
        ):
            raise TypeError(
                f"tracking_mode must be a TrackingModeOptions instance or None, "
                f"got {type(self.tracking_mode)}"
            )

        # Validate localization and UI fields
        if self.localization is not None and not isinstance(self.localization, LocalizationOptions):
            raise TypeError(
                f"localization must be a LocalizationOptions instance or None, "
                f"got {type(self.localization)}"
            )
        if not isinstance(self.add_default_pane, bool):
            raise TypeError(f"add_default_pane must be a bool, got {type(self.add_default_pane)}")
        if self.trade_visualization is not None and not isinstance(
            self.trade_visualization, TradeVisualizationOptions
        ):
            raise TypeError(
                f"trade_visualization must be a TradeVisualizationOptions instance or None, "
                f"got {type(self.trade_visualization)}"
            )
