"""
Chart options configuration for streamlit-lightweight-charts.

This module provides the ChartOptions class which encapsulates all configuration
options for charts including layout, grid, watermark, legend, and various
display settings. It supports method chaining for fluent API usage.

The ChartOptions class provides a comprehensive set of options for customizing
chart appearance and behavior, making it easy to create professional-looking
financial charts with consistent styling.

Example:
    ```python
    from streamlit_lightweight_charts_pro.charts.options import ChartOptions

    # Create options with method chaining
    options = (ChartOptions()
               .set_size(800, 600)
               .set_auto_size(True)
               .set_watermark("My Chart")
               .set_legend(True)
               .set_kinetic_scroll(True))
    ```
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from ...type_definitions import LineStyle


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
    """

    # Size and layout options
    width: Optional[int] = None
    height: int = 400
    auto_size: bool = True
    min_width: Optional[int] = None
    max_width: Optional[int] = None
    min_height: Optional[int] = None
    max_height: Optional[int] = None

    # Display options
    watermark: Optional[str] = None
    legend: bool = False
    range_switcher: bool = False
    kinetic_scroll: bool = True
    tracking_mode: str = "normal"
    fit_content_on_load: bool = True

    # Localization
    localization: Dict[str, Any] = field(default_factory=dict)

    # Layout configuration
    layout: Dict[str, Any] = field(
        default_factory=lambda: {
            "background": {"type": "solid", "color": "white"},
            "textColor": "black",
            "fontSize": 12,
            "fontFamily": "Roboto, sans-serif",
        }
    )

    # Grid configuration
    grid: Dict[str, Any] = field(
        default_factory=lambda: {
            "vertLines": {"visible": True, "color": "#e1e3e6"},
            "horzLines": {"visible": True, "color": "#e1e3e6"},
        }
    )

    # Crosshair configuration
    crosshair: Dict[str, Any] = field(
        default_factory=lambda: {
            "mode": 1,  # 0: hidden, 1: normal, 2: magnetic
            "vertLine": {
                "visible": True,
                "color": "#9B7DFF",
                "width": 1,
                "style": LineStyle.SOLID,
                "labelVisible": True,
            },
            "horzLine": {
                "visible": True,
                "color": "#9B7DFF",
                "width": 1,
                "style": LineStyle.SOLID,
                "labelVisible": True,
            },
        }
    )

    # Price scale configurations
    right_price_scale: Dict[str, Any] = field(
        default_factory=lambda: {
            "visible": True,
            "borderColor": "#e1e3e6",
            "scaleMargins": {"top": 0.1, "bottom": 0.1},
        }
    )

    left_price_scale: Dict[str, Any] = field(
        default_factory=lambda: {
            "visible": False,
            "borderColor": "#e1e3e6",
            "scaleMargins": {"top": 0.1, "bottom": 0.1},
        }
    )

    # Time scale configuration
    time_scale: Dict[str, Any] = field(
        default_factory=lambda: {
            "visible": True,
            "borderColor": "#e1e3e6",
            "timeVisible": True,
            "secondsVisible": False,
            "rightOffset": 12,
            "barSpacing": 3,
            "fixLeftEdge": False,
            "lockVisibleTimeRangeOnResize": False,
            "rightBarStaysOnScroll": False,
            "borderVisible": False,
        }
    )

    def set_size(self, width: Optional[int] = None, height: Optional[int] = None) -> "ChartOptions":
        """
        Set chart size.

        Updates the chart's width and/or height. Returns self for
        method chaining.

        Args:
            width: Chart width in pixels. If None, width is not changed.
            height: Chart height in pixels. If None, height is not changed.

        Returns:
            ChartOptions: Self for method chaining.

        Example:
            ```python
            options.set_size(width=800, height=600)
            ```
        """
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height
        return self

    def set_width(self, width: int) -> "ChartOptions":
        """
        Set chart width.

        Updates the chart's width. Returns self for method chaining.

        Args:
            width: Chart width in pixels.

        Returns:
            ChartOptions: Self for method chaining.

        Example:
            ```python
            options.set_width(800)
            ```
        """
        self.width = width
        return self

    def set_height(self, height: int) -> "ChartOptions":
        """
        Set chart height.

        Updates the chart's height. Returns self for method chaining.

        Args:
            height: Chart height in pixels.

        Returns:
            ChartOptions: Self for method chaining.

        Example:
            ```python
            options.set_height(600)
            ```
        """
        self.height = height
        return self

    def set_auto_size(self, auto_size: bool = True) -> "ChartOptions":
        """
        Set auto-sizing.

        Enables or disables automatic sizing of the chart. Returns self
        for method chaining.

        Args:
            auto_size: Whether to enable auto-sizing. Defaults to True.

        Returns:
            ChartOptions: Self for method chaining.

        Example:
            ```python
            options.set_auto_size(True)
            ```
        """
        self.auto_size = auto_size
        return self

    def set_min_size(
        self, min_width: Optional[int] = None, min_height: Optional[int] = None
    ) -> "ChartOptions":
        """
        Set minimum chart size.

        Sets the minimum width and/or height when auto-sizing is enabled.
        Returns self for method chaining.

        Args:
            min_width: Minimum width in pixels. If None, min_width is not changed.
            min_height: Minimum height in pixels. If None, min_height is not changed.

        Returns:
            ChartOptions: Self for method chaining.

        Example:
            ```python
            options.set_min_size(min_width=400, min_height=300)
            ```
        """
        if min_width is not None:
            self.min_width = min_width
        if min_height is not None:
            self.min_height = min_height
        return self

    def set_max_size(
        self, max_width: Optional[int] = None, max_height: Optional[int] = None
    ) -> "ChartOptions":
        """
        Set maximum chart size.

        Sets the maximum width and/or height when auto-sizing is enabled.
        Returns self for method chaining.

        Args:
            max_width: Maximum width in pixels. If None, max_width is not changed.
            max_height: Maximum height in pixels. If None, max_height is not changed.

        Returns:
            ChartOptions: Self for method chaining.

        Example:
            ```python
            options.set_max_size(max_width=1200, max_height=800)
            ```
        """
        if max_width is not None:
            self.max_width = max_width
        if max_height is not None:
            self.max_height = max_height
        return self

    def set_watermark(self, watermark: Optional[str]) -> "ChartOptions":
        """
        Set chart watermark.

        Sets the watermark text to display on the chart. Returns self
        for method chaining.

        Args:
            watermark: Watermark text to display. If None, removes watermark.

        Returns:
            ChartOptions: Self for method chaining.

        Example:
            ```python
            options.set_watermark("My Financial Chart")
            ```
        """
        self.watermark = watermark
        return self

    def set_legend(self, show_legend: bool = True) -> "ChartOptions":
        """
        Set legend visibility.

        Shows or hides the chart legend. Returns self for method chaining.

        Args:
            show_legend: Whether to show the legend. Defaults to True.

        Returns:
            ChartOptions: Self for method chaining.

        Example:
            ```python
            options.set_legend(True)
            ```
        """
        self.legend = show_legend
        return self

    def set_range_switcher(self, show_range_switcher: bool = True) -> "ChartOptions":
        """
        Set range switcher visibility.

        Shows or hides the range switcher (1D, 1W, 1M, etc.). Returns self
        for method chaining.

        Args:
            show_range_switcher: Whether to show the range switcher. Defaults to True.

        Returns:
            ChartOptions: Self for method chaining.

        Example:
            ```python
            options.set_range_switcher(True)
            ```
        """
        self.range_switcher = show_range_switcher
        return self

    def set_kinetic_scroll(self, enable_kinetic_scroll: bool = True) -> "ChartOptions":
        """
        Set kinetic scrolling.

        Enables or disables kinetic scrolling for touch devices. Returns self
        for method chaining.

        Args:
            enable_kinetic_scroll: Whether to enable kinetic scrolling. Defaults to True.

        Returns:
            ChartOptions: Self for method chaining.

        Example:
            ```python
            options.set_kinetic_scroll(True)
            ```
        """
        self.kinetic_scroll = enable_kinetic_scroll
        return self

    def set_tracking_mode(self, mode: str) -> "ChartOptions":
        """
        Set mouse tracking mode.

        Sets the mouse tracking mode for crosshair and tooltips. Returns self
        for method chaining.

        Args:
            mode: Tracking mode ("normal", "magnetic", or "crosshair").

        Returns:
            ChartOptions: Self for method chaining.

        Example:
            ```python
            options.set_tracking_mode("magnetic")
            ```
        """
        self.tracking_mode = mode
        return self

    def set_fit_content_on_load(self, fit_content: bool = True) -> "ChartOptions":
        """
        Set whether to fit content on load.

        Controls whether the chart automatically fits to its content when
        first displayed. Returns self for method chaining.

        Args:
            fit_content: Whether to fit content on load. Defaults to True.

        Returns:
            ChartOptions: Self for method chaining.

        Example:
            ```python
            options.set_fit_content_on_load(True)
            ```
        """
        self.fit_content_on_load = fit_content
        return self

    def set_localization(self, locale: str, date_format: str = "yyyy-MM-dd") -> "ChartOptions":
        """
        Set localization settings.

        Sets the localization settings for date/time formatting. Returns self
        for method chaining.

        Args:
            locale: Locale string (e.g., "en-US", "de-DE").
            date_format: Date format string. Defaults to "yyyy-MM-dd".

        Returns:
            ChartOptions: Self for method chaining.

        Example:
            ```python
            options.set_localization("en-US", "MM/dd/yyyy")
            ```
        """
        self.localization = {
            "locale": locale,
            "dateFormat": date_format,
        }
        return self

    def set_layout(self, **kwargs) -> "ChartOptions":
        """
        Set layout configuration.

        Updates layout configuration options. Returns self for method chaining.

        Args:
            **kwargs: Layout options to update (background, textColor, fontSize, etc.).

        Returns:
            ChartOptions: Self for method chaining.

        Example:
            ```python
            options.set_layout(
                background={"type": "solid", "color": "#f8f9fa"},
                textColor="#333333",
                fontSize=14
            )
            ```
        """
        self.layout.update(kwargs)
        return self

    def set_grid(self, **kwargs) -> "ChartOptions":
        """
        Set grid configuration.

        Updates grid configuration options. Returns self for method chaining.

        Args:
            **kwargs: Grid options to update (vertLines, horzLines, etc.).

        Returns:
            ChartOptions: Self for method chaining.

        Example:
            ```python
            options.set_grid(
                vertLines={"visible": True, "color": "#cccccc"},
                horzLines={"visible": False}
            )
            ```
        """
        self.grid.update(kwargs)
        return self

    def set_crosshair(self, **kwargs) -> "ChartOptions":
        """
        Set crosshair configuration.

        Updates crosshair configuration options. Returns self for method chaining.

        Args:
            **kwargs: Crosshair options to update (mode, vertLine, horzLine, etc.).

        Returns:
            ChartOptions: Self for method chaining.

        Example:
            ```python
            options.set_crosshair(
                mode=2,  # magnetic mode
                vertLine={"color": "#ff0000", "width": 2}
            )
            ```
        """
        self.crosshair.update(kwargs)
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
        self.right_price_scale.update(kwargs)
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
        self.left_price_scale.update(kwargs)
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
        self.time_scale.update(kwargs)
        return self

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert options to dictionary for serialization.

        Creates a dictionary representation of all chart options
        suitable for JSON serialization or frontend consumption.

        Returns:
            Dict[str, Any]: Dictionary containing all chart options
                in a format suitable for the frontend component.
        """
        result = {
            "width": self.width,
            "height": self.height,
            "autoSize": self.auto_size,
            "watermark": self.watermark,
            "legend": self.legend,
            "rangeSwitcher": self.range_switcher,
            "kineticScroll": self.kinetic_scroll,
            "trackingMode": self.tracking_mode,
            "fitContentOnLoad": self.fit_content_on_load,
            "localization": self.localization,
            "layout": self.layout,
            "grid": self.grid,
            "crosshair": self.crosshair,
            "rightPriceScale": self.right_price_scale,
            "leftPriceScale": self.left_price_scale,
            "timeScale": self.time_scale,
        }

        # Add size constraints only if they are set
        if self.min_width is not None:
            result["minWidth"] = self.min_width
        if self.max_width is not None:
            result["maxWidth"] = self.max_width
        if self.min_height is not None:
            result["minHeight"] = self.min_height
        if self.max_height is not None:
            result["maxHeight"] = self.max_height

        # Remove None values for cleaner output
        return {k: v for k, v in result.items() if v is not None}
