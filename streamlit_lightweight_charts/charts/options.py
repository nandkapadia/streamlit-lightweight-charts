"""Chart option classes for streamlit-lightweight-charts."""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from ..type_definitions import (
    Background,
    CrosshairMode,
    HorzAlign,
    LineStyle,
    PriceScaleMode,
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
        '-apple-system, BlinkMacSystemFont, "Trebuchet MS", Roboto, Ubuntu, sans-serif'
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
class CrosshairOptions:
    """Crosshair configuration for chart."""

    mode: CrosshairMode = CrosshairMode.MAGNET
    vert_line: CrosshairLineOptions = field(default_factory=CrosshairLineOptions)
    horz_line: CrosshairLineOptions = field(default_factory=CrosshairLineOptions)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "mode": self.mode.value,
            "vertLine": self.vert_line.to_dict(),
            "horzLine": self.horz_line.to_dict(),
        }


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

    border_visible: bool = True
    border_color: str = "rgba(197, 203, 206, 0.8)"
    mode: PriceScaleMode = PriceScaleMode.NORMAL
    align_labels: bool = True
    scale_margins: PriceScaleMargins = field(default_factory=PriceScaleMargins)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "borderVisible": self.border_visible,
            "borderColor": self.border_color,
            "mode": self.mode.value,
            "alignLabels": self.align_labels,
            "scaleMargins": self.scale_margins.to_dict(),
        }


@dataclass
class TimeScaleOptions:
    """Time scale configuration."""

    right_offset: int = 0
    bar_spacing: int = 6
    min_bar_spacing: float = 0.5
    visible: bool = True
    time_visible: bool = True
    border_visible: bool = True
    border_color: str = "rgba(197, 203, 206, 0.8)"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "rightOffset": self.right_offset,
            "barSpacing": self.bar_spacing,
            "minBarSpacing": self.min_bar_spacing,
            "visible": self.visible,
            "timeVisible": self.time_visible,
            "borderVisible": self.border_visible,
            "borderColor": self.border_color,
        }


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
class ChartOptions:
    """Main chart configuration options."""

    width: Optional[int] = None
    height: int = 400
    layout: LayoutOptions = field(default_factory=LayoutOptions)
    grid: GridOptions = field(default_factory=GridOptions)
    crosshair: CrosshairOptions = field(default_factory=CrosshairOptions)
    right_price_scale: PriceScaleOptions = field(default_factory=PriceScaleOptions)
    left_price_scale: Optional[PriceScaleOptions] = None
    overlay_price_scales: Optional[Dict[str, Any]] = None
    time_scale: TimeScaleOptions = field(default_factory=TimeScaleOptions)
    watermark: Optional[WatermarkOptions] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        result = {
            "height": self.height,
            "layout": self.layout.to_dict(),
            "grid": self.grid.to_dict(),
            "crosshair": self.crosshair.to_dict(),
            "rightPriceScale": self.right_price_scale.to_dict(),
            "timeScale": self.time_scale.to_dict(),
        }

        if self.width is not None:
            result["width"] = self.width

        if self.left_price_scale is not None:
            result["leftPriceScale"] = self.left_price_scale.to_dict()

        if self.overlay_price_scales is not None:
            result["overlayPriceScales"] = self.overlay_price_scales

        if self.watermark is not None:
            result["watermark"] = self.watermark.to_dict()

        return result
