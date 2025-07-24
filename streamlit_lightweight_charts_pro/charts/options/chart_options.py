"""
Chart options configuration for streamlit-lightweight-charts.

This module provides the ChartOptions class which encapsulates all configuration
options for charts including layout, grid, watermark, legend, and various
display settings. It supports method chaining for fluent API usage.

The ChartOptions class provides a comprehensive set of options for customizing
chart appearance and behavior, making it easy to create professional-looking
financial charts with consistent styling.

Example:
    from streamlit_lightweight_charts_pro.charts.options import ChartOptions

    # Create options with method chaining
    options = (ChartOptions()
               .set_size(800, 600)
               .set_auto_size(True)
               .set_watermark("My Chart")
               .set_legend(True)
               .set_kinetic_scroll(True))
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from streamlit_lightweight_charts_pro.charts.options.layout_options import (
    LayoutOptions,
    GridOptions,
    WatermarkOptions,
    GridLineOptions,
)
from streamlit_lightweight_charts_pro.charts.options.interaction_options import (
    CrosshairOptions,
    CrosshairMode,
    CrosshairLineOptions,
)
from streamlit_lightweight_charts_pro.charts.options.price_scale_options import PriceScaleOptions
from streamlit_lightweight_charts_pro.charts.options.time_scale_options import TimeScaleOptions


@dataclass
class ChartOptions:
    """
    Configuration options for chart display and behavior.

    This class encapsulates all the configuration options that control
    how a chart is displayed, including its size, layout, grid settings,
    watermark, legend, and various interactive features.

    The class supports method chaining for fluent API usage, allowing
    for intuitive configuration of chart options.

    Attributes:
        width: Chart width in pixels. If None, uses 100% of container width.
        height: Chart height in pixels. Defaults to 400.
        auto_size: Whether to automatically size the chart to fit its container.
        min_width: Minimum width in pixels when auto-sizing is enabled.
        max_width: Maximum width in pixels when auto-sizing is enabled.
        min_height: Minimum height in pixels when auto-sizing is enabled.
        max_height: Maximum height in pixels when auto-sizing is enabled.
        watermark: Optional watermark text to display on the chart.
        legend: Whether to show the chart legend.
        range_switcher: Whether to show the range switcher (1D, 1W, 1M, etc.).
        kinetic_scroll: Whether to enable kinetic scrolling for touch devices.
        tracking_mode: Mouse tracking mode for crosshair and tooltips.
        localization: Localization settings for date/time formatting.
        layout: Chart layout configuration (background, text colors, etc.).
        grid: Grid configuration (horizontal and vertical grid lines).
        crosshair: Crosshair configuration for mouse interactions.
        right_price_scale: Right price scale configuration.
        left_price_scale: Left price scale configuration.
        time_scale: Time scale configuration (axis, time formatting, etc.).
        legend_position: Optional position for the chart legend.
        tooltip: Optional tooltip configuration.
    """

    # Size and layout options
    width: Optional[int] = None
    height: int = 400
    auto_size: bool = True
    min_width: Optional[int] = None
    max_width: Optional[int] = None
    min_height: Optional[int] = None
    max_height: Optional[int] = None
    watermark: Any = None
    legend: bool = False
    range_switcher: bool = False
    kinetic_scroll: bool = True
    tracking_mode: str = "normal"
    fit_content_on_load: bool = True
    localization: Dict[str, Any] = field(default_factory=dict)
    layout: LayoutOptions = field(default_factory=LayoutOptions)
    grid: GridOptions = field(default_factory=GridOptions)
    crosshair: CrosshairOptions = field(default_factory=CrosshairOptions)
    right_price_scale: PriceScaleOptions = field(default_factory=PriceScaleOptions)
    left_price_scale: PriceScaleOptions = field(
        default_factory=lambda: PriceScaleOptions(visible=False)
    )
    overlay_price_scales: Dict[str, PriceScaleOptions] = field(default_factory=dict)
    time_scale: TimeScaleOptions = field(default_factory=TimeScaleOptions)
    legend_position: str = None  # Add this field to the dataclass
    tooltip: dict = None  # Add this field to the dataclass

    def __post_init__(self):
        if isinstance(self.watermark, str):
            self.watermark = self.watermark  # keep as string
        elif isinstance(self.watermark, dict):
            self.watermark = WatermarkOptions(**self.watermark)
        elif self.watermark is not None and not isinstance(self.watermark, WatermarkOptions):
            self.watermark = WatermarkOptions()
        self._watermark_text = (
            self.watermark.text
            if isinstance(self.watermark, WatermarkOptions)
            else (self.watermark if isinstance(self.watermark, str) else None)
        )

    @property
    def watermark_text(self):
        return self.watermark.text if isinstance(self.watermark, WatermarkOptions) else None

    def set_size(self, width: Optional[int] = None, height: Optional[int] = None) -> "ChartOptions":
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height
        return self

    def set_width(self, width: int) -> "ChartOptions":
        self.width = width
        return self

    def set_height(self, height: int) -> "ChartOptions":
        self.height = height
        return self

    def set_auto_size(self, auto_size: bool = True) -> "ChartOptions":
        self.auto_size = auto_size
        return self

    def set_min_size(
        self, min_width: Optional[int] = None, min_height: Optional[int] = None
    ) -> "ChartOptions":
        if min_width is not None:
            self.min_width = min_width
        if min_height is not None:
            self.min_height = min_height
        return self

    def set_max_size(
        self, max_width: Optional[int] = None, max_height: Optional[int] = None
    ) -> "ChartOptions":
        if max_width is not None:
            self.max_width = max_width
        if max_height is not None:
            self.max_height = max_height
        return self

    def set_watermark(self, watermark: Any) -> "ChartOptions":
        if watermark is None:
            self.watermark = None
        elif isinstance(watermark, str):
            self.watermark = WatermarkOptions(text=watermark)
        elif isinstance(watermark, dict):
            self.watermark = WatermarkOptions(**watermark)
        elif isinstance(watermark, WatermarkOptions):
            self.watermark = watermark
        else:
            self.watermark = None
        self._watermark_text = (
            self.watermark.text
            if isinstance(self.watermark, WatermarkOptions)
            else (self.watermark if isinstance(self.watermark, str) else None)
        )
        return self

    def set_legend(self, show_legend: bool = True) -> "ChartOptions":
        self.legend = show_legend
        return self

    def set_range_switcher(self, show_range_switcher: bool = True) -> "ChartOptions":
        self.range_switcher = show_range_switcher
        return self

    def set_kinetic_scroll(self, enable_kinetic_scroll: bool = True) -> "ChartOptions":
        self.kinetic_scroll = enable_kinetic_scroll
        return self

    def set_tracking_mode(self, mode: str) -> "ChartOptions":
        self.tracking_mode = mode
        return self

    def set_localization(self, locale: str, date_format: str = "yyyy-MM-dd") -> "ChartOptions":
        self.localization = {"locale": locale, "dateFormat": date_format}
        return self

    def set_grid_dict(self, value: dict):
        if value is None:
            self.grid = GridOptions()
        else:
            # Convert nested dicts to GridLineOptions
            if "vertLines" in value:
                value["vert_lines"] = value.pop("vertLines")
            if "horzLines" in value:
                value["horz_lines"] = value.pop("horzLines")
            if "vert_lines" in value and isinstance(value["vert_lines"], dict):
                value["vert_lines"] = GridLineOptions(**value["vert_lines"])
            if "horz_lines" in value and isinstance(value["horz_lines"], dict):
                value["horz_lines"] = GridLineOptions(**value["horz_lines"])
            self.grid = GridOptions(**value)
        return self

    def set_crosshair_dict(self, value: dict):
        if value is None:
            self.crosshair = CrosshairOptions()
        else:
            if "vertLine" in value:
                value["vert_line"] = value.pop("vertLine")
            if "horzLine" in value:
                value["horz_line"] = value.pop("horzLine")
            if "vert_line" in value and isinstance(value["vert_line"], dict):
                value["vert_line"] = CrosshairLineOptions(**value["vert_line"])
            if "horz_line" in value and isinstance(value["horz_line"], dict):
                value["horz_line"] = CrosshairLineOptions(**value["horz_line"])
            self.crosshair = CrosshairOptions(**value)
        return self

    def set_watermark_dict(self, value: dict):
        if value is None:
            self.watermark = WatermarkOptions()
        elif isinstance(value, str):
            self.watermark = WatermarkOptions(text=value)
        else:
            self.watermark = WatermarkOptions(**value)
        return self

    def set_time_scale_dict(self, value: dict):
        if value is None:
            self.time_scale = TimeScaleOptions()
        else:
            # Map camelCase keys to snake_case
            if "timeVisible" in value:
                value["time_visible"] = value.pop("timeVisible")
            if "secondsVisible" in value:
                value["seconds_visible"] = value.pop("secondsVisible")
            if "borderVisible" in value:
                value["border_visible"] = value.pop("borderVisible")
            if "borderColor" in value:
                value["border_color"] = value.pop("borderColor")
            if "fixLeftEdge" in value:
                value["fix_left_edge"] = value.pop("fixLeftEdge")
            if "fixRightEdge" in value:
                value["fix_right_edge"] = value.pop("fixRightEdge")
            if "lockVisibleTimeRangeOnResize" in value:
                value["lock_visible_time_range_on_resize"] = value.pop(
                    "lockVisibleTimeRangeOnResize"
                )
            if "rightBarStaysOnScroll" in value:
                value["right_bar_stays_on_scroll"] = value.pop("rightBarStaysOnScroll")
            if "shiftVisibleRangeOnNewBar" in value:
                value["shift_visible_range_on_new_bar"] = value.pop("shiftVisibleRangeOnNewBar")
            if "allowShiftVisibleRangeOnWhitespaceAccess" in value:
                value["allow_shift_visible_range_on_whitespace_access"] = value.pop(
                    "allowShiftVisibleRangeOnWhitespaceAccess"
                )
            if "tickMarkFormatter" in value:
                value["tick_mark_formatter"] = value.pop("tickMarkFormatter")
            self.time_scale = TimeScaleOptions(**value)
        return self

    def set_layout(self, **kwargs):
        for k, v in kwargs.items():
            if k == "background_color":
                if hasattr(self.layout, "background") and hasattr(self.layout.background, "color"):
                    self.layout.background.color = v
            elif hasattr(self.layout, k):
                setattr(self.layout, k, v)
        return self

    def set_grid(self, vert_lines=None, horz_lines=None, **kwargs):
        """
        Set grid configuration.
        Accepts dicts for vert_lines and horz_lines and converts them to GridLineOptions.
        """
        if vert_lines is not None:
            if isinstance(vert_lines, dict):
                self.grid.vert_lines = GridLineOptions(**vert_lines)
            else:
                self.grid.vert_lines = vert_lines
        if horz_lines is not None:
            if isinstance(horz_lines, dict):
                self.grid.horz_lines = GridLineOptions(**horz_lines)
            else:
                self.grid.horz_lines = horz_lines
        for k, v in kwargs.items():
            if hasattr(self.grid, k):
                setattr(self.grid, k, v)
        return self

    def set_crosshair(self, mode=None, vert_line=None, horz_line=None, **kwargs):
        """
        Set crosshair configuration.
        Ensures mode is always stored as a CrosshairMode enum.
        """
        if mode is not None:
            if isinstance(mode, int):
                self.crosshair.mode = CrosshairMode(mode)
            else:
                self.crosshair.mode = mode
        if vert_line is not None:
            if isinstance(vert_line, dict):
                self.crosshair.vert_line = CrosshairLineOptions(**vert_line)
            else:
                self.crosshair.vert_line = vert_line
        if horz_line is not None:
            if isinstance(horz_line, dict):
                self.crosshair.horz_line = CrosshairLineOptions(**horz_line)
            else:
                self.crosshair.horz_line = horz_line
        for k, v in kwargs.items():
            if hasattr(self.crosshair, k):
                setattr(self.crosshair, k, v)
        return self

    def set_right_price_scale(self, **kwargs) -> "ChartOptions":
        """
        Set right price scale configuration.

        Updates right price scale configuration options. Returns self
        for method chaining.

        Args:
            **kwargs: Right price scale options to update.

        Returns:
            ChartOptions: Self for method chaining.

        Example:
            ```python
            options.set_right_price_scale(
                visible=True,
                borderColor="#333333",
                scaleMargins={"top": 0.2, "bottom": 0.2}
            )
            ```
        """
        for k, v in kwargs.items():
            if hasattr(self.right_price_scale, k):
                setattr(self.right_price_scale, k, v)
        return self

    def set_left_price_scale(self, **kwargs) -> "ChartOptions":
        """
        Set left price scale configuration.

        Updates left price scale configuration options. Returns self
        for method chaining.

        Args:
            **kwargs: Left price scale options to update.

        Returns:
            ChartOptions: Self for method chaining.

        Example:
            ```python
            options.set_left_price_scale(
                visible=True,
                borderColor="#333333"
            )
            ```
        """
        for k, v in kwargs.items():
            if hasattr(self.left_price_scale, k):
                setattr(self.left_price_scale, k, v)
        return self

    def set_time_scale(self, **kwargs) -> "ChartOptions":
        """
        Set time scale configuration.

        Updates time scale configuration options. Returns self for
        method chaining.

        Args:
            **kwargs: Time scale options to update.

        Returns:
            ChartOptions: Self for method chaining.

        Example:
            ```python
            options.set_time_scale(
                timeVisible=True,
                secondsVisible=False,
                rightOffset=20,
                barSpacing=5
            )
            ```
        """
        for k, v in kwargs.items():
            if hasattr(self.time_scale, k):
                setattr(self.time_scale, k, v)
        return self

    def to_dict(self) -> Dict[str, Any]:
        result = {}
        if self.width is not None:
            result["width"] = self.width
        if self.height is not None:
            result["height"] = self.height
        result["autoSize"] = self.auto_size
        if self.min_width is not None:
            result["minWidth"] = self.min_width
        if self.max_width is not None:
            result["maxWidth"] = self.max_width
        if self.min_height is not None:
            result["minHeight"] = self.min_height
        if self.max_height is not None:
            result["maxHeight"] = self.max_height
        if self.watermark is not None:
            result["watermark"] = (
                self.watermark.to_dict() if hasattr(self.watermark, "to_dict") else self.watermark
            )
        result["legend"] = self.legend
        result["rangeSwitcher"] = self.range_switcher
        result["kineticScroll"] = self.kinetic_scroll
        result["trackingMode"] = self.tracking_mode
        result["fitContentOnLoad"] = self.fit_content_on_load
        result["localization"] = self.localization
        if self.layout is not None:
            result["layout"] = (
                self.layout.to_dict() if hasattr(self.layout, "to_dict") else self.layout
            )
        if self.grid is not None:
            result["grid"] = (
                self.grid.to_dict() if hasattr(self.grid, "to_dict") else self.grid
            )
        if self.crosshair is not None:
            result["crosshair"] = (
                self.crosshair.to_dict() if hasattr(self.crosshair, "to_dict") else self.crosshair
            )
        if self.right_price_scale is not None:
            result["rightPriceScale"] = (
                self.right_price_scale.to_dict() if hasattr(self.right_price_scale, "to_dict") else self.right_price_scale
            )
        if self.left_price_scale is not None:
            result["PriceScaleOptions"] = (
                self.left_price_scale.to_dict() if hasattr(self.left_price_scale, "to_dict") else self.left_price_scale
            )
        if self.time_scale is not None:
            result["timeScale"] = (
                self.time_scale.to_dict() if hasattr(self.time_scale, "to_dict") else self.time_scale
            )
        if self.tooltip is not None:
            result["tooltip"] = self.tooltip
        if self.overlay_price_scales:
            result["PriceScaleOptionss"] = {
                k: (v.to_dict() if hasattr(v, "to_dict") else v)
                for k, v in self.overlay_price_scales.items()
            }
        return result

    def __eq__(self, other):
        if not isinstance(other, ChartOptions):
            return False
        # Compare all fields, using .to_dict() for nested option objects
        field_names = [
            "width",
            "height",
            "auto_size",
            "min_width",
            "max_width",
            "min_height",
            "max_height",
            "watermark",
            "legend",
            "range_switcher",
            "kinetic_scroll",
            "tracking_mode",
            "fit_content_on_load",
            "localization",
            "layout",
            "grid",
            "crosshair",
            "right_price_scale",
            "left_price_scale",
            "overlay_price_scales",
            "time_scale",
            "legend_position",
            "tooltip",
        ]
        for field_name in field_names:
            v1 = getattr(self, field_name, None)
            v2 = getattr(other, field_name, None)
            if field_name == "watermark":
                # Allow WatermarkOptions == str if .text matches
                if v1 is None and v2 is None:
                    continue
                if hasattr(v1, "text") and isinstance(v2, str):
                    if v1.text != v2:
                        return False
                    continue
                if hasattr(v2, "text") and isinstance(v1, str):
                    if v2.text != v1:
                        return False
                    continue
                if hasattr(v1, "to_dict") and hasattr(v2, "to_dict"):
                    if v1.to_dict() != v2.to_dict():
                        return False
                    continue
                if v1 != v2:
                    return False
            elif field_name == "tooltip":
                if v1 is None and v2 is None:
                    continue
                if v1 is not None and v2 is not None:
                    if v1 != v2:
                        return False
                    continue
                if v1 is None or v2 is None:
                    return False
            elif hasattr(v1, "to_dict") and hasattr(v2, "to_dict"):
                if v1.to_dict() != v2.to_dict():
                    return False
            else:
                if v1 != v2:
                    return False
        return True
