"""UI option classes for streamlit-lightweight-charts."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


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