"""Chart option classes for streamlit-lightweight-charts."""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional, List, Callable

from ..type_definitions import (
    Background,
    CrosshairMode,
    HorzAlign,
    LineStyle,
    PriceScaleMode,
    TrackingActivationMode,
    TrackingExitMode,
    VertAlign,
)


@dataclass
class GridLineOptions:
    """Grid line configuration."""

    color: str = "rgba(197, 203, 206, 0.5)"
    style: LineStyle = LineStyle.SOLID
    visible: bool = True

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {"color": self.color, "style": self.style.value, "visible": self.visible}


@dataclass
class GridOptions:
    """Grid configuration for chart."""

    vert_lines: GridLineOptions = field(default_factory=GridLineOptions)
    horz_lines: GridLineOptions = field(default_factory=GridLineOptions)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "vertLines": self.vert_lines.to_dict(),
            "horzLines": self.horz_lines.to_dict(),
        }


@dataclass
class LayoutOptions:
    """Layout configuration for chart."""

    background: Background = field(default_factory=lambda: Background.solid("#FFFFFF"))
    text_color: str = "#191919"
    font_size: int = 12
    font_family: str = (
        '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Helvetica Neue", sans-serif'
    )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "background": self.background.to_dict(),
            "textColor": self.text_color,
            "fontSize": self.font_size,
            "fontFamily": self.font_family,
        }


@dataclass
class CrosshairLineOptions:
    """Crosshair line configuration."""

    visible: bool = True
    width: int = 1
    color: str = "rgba(224, 227, 235, 0.2)"
    style: LineStyle = LineStyle.DASHED

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "visible": self.visible,
            "width": self.width,
            "color": self.color,
            "style": self.style.value,
        }


@dataclass
class CrosshairSyncOptions:
    """Crosshair synchronization configuration."""

    group_id: str = "default"
    suppress_crosshair_move: bool = False
    suppress_mouse_move: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "groupId": self.group_id,
            "suppressCrosshairMove": self.suppress_crosshair_move,
            "suppressMouseMove": self.suppress_mouse_move,
        }


@dataclass
class CrosshairOptions:
    """Crosshair configuration for chart."""

    mode: CrosshairMode = CrosshairMode.MAGNET
    vert_line: CrosshairLineOptions = field(default_factory=CrosshairLineOptions)
    horz_line: CrosshairLineOptions = field(default_factory=CrosshairLineOptions)
    sync: Optional[CrosshairSyncOptions] = None
    group_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        result = {
            "mode": self.mode.value,
            "vertLine": self.vert_line.to_dict(),
            "horzLine": self.horz_line.to_dict(),
        }

        if self.sync is not None:
            result["sync"] = self.sync.to_dict()

        if self.group_id is not None:
            result["groupId"] = self.group_id

        return result


@dataclass
class PriceScaleMargins:
    """Price scale margins configuration."""

    top: float = 0.1
    bottom: float = 0.1

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {"top": self.top, "bottom": self.bottom}


@dataclass
class PriceScaleOptions:
    """Price scale configuration."""

    auto_scale: bool = True
    mode: PriceScaleMode = PriceScaleMode.NORMAL
    invert_scale: bool = False
    align_labels: bool = True
    scale_margins: PriceScaleMargins = field(default_factory=PriceScaleMargins)
    border_visible: bool = True
    border_color: str = "rgba(197, 203, 206, 0.8)"
    text_color: str = "#333333"
    font_size: int = 11
    font_weight: str = "400"
    entire_text_only: bool = False
    visible: bool = True
    ticks_visible: bool = True
    minimum_width: int = 72
    ensure_edge_tick_marks_visible: bool = False
    handle_scale: bool = False
    handle_size: int = 20
    draw_ticks: bool = True
    price_scale_id: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        # Ensure minimumWidth is never 0 to prevent invisible Y-axis labels
        safe_minimum_width = max(self.minimum_width, 72) if self.visible else 0
        
        result = {
            "autoScale": self.auto_scale,
            "mode": self.mode.value,
            "invertScale": self.invert_scale,
            "alignLabels": self.align_labels,
            "scaleMargins": self.scale_margins.to_dict(),
            "borderVisible": self.border_visible,
            "borderColor": self.border_color,
            "fontSize": self.font_size,
            "fontWeight": self.font_weight,
            "textColor": self.text_color,
            "entireTextOnly": self.entire_text_only,
            "visible": self.visible,
            "ticksVisible": self.ticks_visible,
            "minimumWidth": safe_minimum_width,
            "ensureEdgeTickMarksVisible": self.ensure_edge_tick_marks_visible,
            "handleScale": self.handle_scale,
            "handleSize": self.handle_size,
            "drawTicks": self.draw_ticks,
        }

        if self.price_scale_id:
            result["priceScaleId"] = self.price_scale_id

        return result


@dataclass
class TimeScaleOptions:
    """Time scale configuration."""

    right_offset: int = 0
    left_offset: int = 0
    bar_spacing: int = 6
    min_bar_spacing: float = 0.5
    visible: bool = True
    time_visible: bool = True
    seconds_visible: bool = False
    border_visible: bool = True
    border_color: str = "rgba(197, 203, 206, 0.8)"
    fix_left_edge: bool = False
    fix_right_edge: bool = False
    lock_visible_time_range_on_resize: bool = False
    right_bar_stays_on_scroll: bool = False
    shift_visible_range_on_new_bar: bool = False
    allow_shift_visible_range_on_whitespace_access: bool = False
    tick_mark_formatter: Optional[Callable] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        result = {
            "rightOffset": self.right_offset,
            "leftOffset": self.left_offset,
            "barSpacing": self.bar_spacing,
            "minBarSpacing": self.min_bar_spacing,
            "visible": self.visible,
            "timeVisible": self.time_visible,
            "secondsVisible": self.seconds_visible,
            "borderVisible": self.border_visible,
            "borderColor": self.border_color,
            "fixLeftEdge": self.fix_left_edge,
            "fixRightEdge": self.fix_right_edge,
            "lockVisibleTimeRangeOnResize": self.lock_visible_time_range_on_resize,
            "rightBarStaysOnScroll": self.right_bar_stays_on_scroll,
            "shiftVisibleRangeOnNewBar": self.shift_visible_range_on_new_bar,
            "allowShiftVisibleRangeOnWhitespaceAccess": self.allow_shift_visible_range_on_whitespace_access,
        }

        if self.tick_mark_formatter is not None:
            result["tickMarkFormatter"] = self.tick_mark_formatter

        return result


@dataclass
class WatermarkOptions:
    """Watermark configuration."""

    visible: bool = False
    text: str = ""
    font_size: int = 48
    horz_align: HorzAlign = HorzAlign.CENTER
    vert_align: VertAlign = VertAlign.CENTER
    color: str = "rgba(171, 71, 188, 0.3)"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "visible": self.visible,
            "text": self.text,
            "fontSize": self.font_size,
            "horzAlign": self.horz_align.value,
            "vertAlign": self.vert_align.value,
            "color": self.color,
        }


@dataclass
class RangeConfig:
    """Range configuration for range switcher."""

    label: str
    seconds: Optional[int] = None  # None for "ALL" range

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "label": self.label,
            "seconds": self.seconds,
        }


@dataclass
class RangeSwitcherOptions:
    """Range switcher configuration."""

    visible: bool = False
    ranges: List[RangeConfig] = field(
        default_factory=lambda: [
            RangeConfig("1D", 86400),
            RangeConfig("1W", 604800),
            RangeConfig("1M", 2592000),
            RangeConfig("3M", 7776000),
            RangeConfig("6M", 15552000),
            RangeConfig("1Y", 31536000),
            RangeConfig("ALL", None),
        ]
    )
    position: str = "top-right"  # "top-left", "top-right", "bottom-left", "bottom-right"
    default_range: str = "1M"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "visible": self.visible,
            "ranges": [range_config.to_dict() for range_config in self.ranges],
            "position": self.position,
            "defaultRange": self.default_range,
        }


@dataclass
class LegendOptions:
    """Legend configuration."""

    visible: bool = False
    type: str = "simple"  # "simple" or "3line"
    position: str = "top-left"  # "top-left", "top-right", "bottom-left", "bottom-right"
    symbol_name: str = ""
    font_size: int = 14
    font_family: str = "sans-serif"
    font_weight: str = "300"
    color: str = "black"
    background_color: str = "transparent"
    border_color: str = "transparent"
    border_width: int = 0
    border_radius: int = 0
    padding: int = 8
    margin: int = 12
    z_index: int = 1
    show_last_value: bool = True
    show_time: bool = True
    show_symbol: bool = True
    price_format: str = "2"  # Number of decimal places
    custom_template: Optional[str] = None  # Custom HTML template

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "visible": self.visible,
            "type": self.type,
            "position": self.position,
            "symbolName": self.symbol_name,
            "fontSize": self.font_size,
            "fontFamily": self.font_family,
            "fontWeight": self.font_weight,
            "color": self.color,
            "backgroundColor": self.background_color,
            "borderColor": self.border_color,
            "borderWidth": self.border_width,
            "borderRadius": self.border_radius,
            "padding": self.padding,
            "margin": self.margin,
            "zIndex": self.z_index,
            "showLastValue": self.show_last_value,
            "showTime": self.show_time,
            "showSymbol": self.show_symbol,
            "priceFormat": self.price_format,
            "customTemplate": self.custom_template,
        }


@dataclass
class LocalizationOptions:
    """Localization configuration for chart."""

    locale: str = "en-US"
    date_format: str = "yyyy-MM-dd"
    time_format: str = "HH:mm:ss"
    price_formatter: Optional[Callable] = None
    percentage_formatter: Optional[Callable] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        result = {
            "locale": self.locale,
            "dateFormat": self.date_format,
            "timeFormat": self.time_format,
        }

        if self.price_formatter is not None:
            result["priceFormatter"] = self.price_formatter

        if self.percentage_formatter is not None:
            result["percentageFormatter"] = self.percentage_formatter

        return result


@dataclass
class TrackingModeOptions:
    """Tracking mode configuration for chart."""

    exit_mode: TrackingExitMode = TrackingExitMode.EXIT_ON_MOVE
    activation_mode: TrackingActivationMode = TrackingActivationMode.ON_MOUSE_ENTER

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "exitMode": self.exit_mode.value,
            "activationMode": self.activation_mode.value,
        }


@dataclass
class KineticScrollOptions:
    """Kinetic scroll configuration for chart."""

    touch: bool = True
    mouse: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "touch": self.touch,
            "mouse": self.mouse,
        }


@dataclass
class ChartOptions:
    """Main chart configuration options."""

    width: Optional[int] = None
    height: int = 400
    auto_size: bool = False  # Auto-size to container
    auto_width: bool = False  # Auto-size width only
    auto_height: bool = False  # Auto-size height only
    min_width: Optional[int] = None  # Minimum width when auto-sizing
    min_height: Optional[int] = None  # Minimum height when auto-sizing
    max_width: Optional[int] = None  # Maximum width when auto-sizing
    max_height: Optional[int] = None  # Maximum height when auto-sizing
    layout: LayoutOptions = field(default_factory=LayoutOptions)
    grid: GridOptions = field(default_factory=GridOptions)
    crosshair: CrosshairOptions = field(default_factory=CrosshairOptions)
    right_price_scale: PriceScaleOptions = field(default_factory=PriceScaleOptions)
    left_price_scale: Optional[PriceScaleOptions] = None
    overlay_price_scales: Optional[Dict[str, Any]] = None
    time_scale: TimeScaleOptions = field(default_factory=TimeScaleOptions)
    watermark: Optional[WatermarkOptions] = None
    legend: Optional[LegendOptions] = None
    range_switcher: Optional[RangeSwitcherOptions] = None
    handle_scroll: bool = True
    handle_scale: bool = True
    kinetic_scroll: Optional[KineticScrollOptions] = None
    tracking_mode: Optional[TrackingModeOptions] = None
    localization: Optional[LocalizationOptions] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        result = {
            "height": self.height,
            "layout": self.layout.to_dict(),
            "grid": self.grid.to_dict(),
            "crosshair": self.crosshair.to_dict(),
            "rightPriceScale": self.right_price_scale.to_dict(),
            "timeScale": self.time_scale.to_dict(),
            "handleScroll": self.handle_scroll,
            "handleScale": self.handle_scale,
        }

        if self.width is not None:
            result["width"] = self.width

        # Add auto-sizing options
        if self.auto_size:
            result["autoSize"] = True
        if self.auto_width:
            result["autoWidth"] = True
        if self.auto_height:
            result["autoHeight"] = True
        if self.min_width is not None:
            result["minWidth"] = self.min_width
        if self.min_height is not None:
            result["minHeight"] = self.min_height
        if self.max_width is not None:
            result["maxWidth"] = self.max_width
        if self.max_height is not None:
            result["maxHeight"] = self.max_height

        if self.left_price_scale is not None:
            result["leftPriceScale"] = self.left_price_scale.to_dict()

        if self.overlay_price_scales is not None:
            result["overlayPriceScales"] = self.overlay_price_scales

        if self.watermark is not None:
            result["watermark"] = self.watermark.to_dict()

        if self.legend is not None:
            result["legend"] = self.legend.to_dict()

        if self.range_switcher is not None:
            result["rangeSwitcher"] = self.range_switcher.to_dict()

        if self.kinetic_scroll is not None:
            result["kineticScroll"] = self.kinetic_scroll.to_dict()

        if self.tracking_mode is not None:
            result["trackingMode"] = self.tracking_mode.to_dict()

        if self.localization is not None:
            result["localization"] = self.localization.to_dict()

        return result
