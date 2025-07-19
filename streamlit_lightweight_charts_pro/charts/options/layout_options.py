"""Layout option classes for streamlit-lightweight-charts."""

from dataclasses import dataclass, field
from typing import Any, Dict

from streamlit_lightweight_charts_pro.type_definitions import Background, HorzAlign, LineStyle, VertAlign


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