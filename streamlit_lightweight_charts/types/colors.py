"""Color-related classes for streamlit-lightweight-charts."""

from typing import Optional, Dict, Any
from dataclasses import dataclass, field
from .enums import ColorType


@dataclass
class Color:
    """Base class for color representations."""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert color to dictionary representation."""
        raise NotImplementedError


@dataclass
class SolidColor(Color):
    """Solid color representation."""
    
    color: str
    type: ColorType = field(default=ColorType.SOLID, init=False)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            'type': self.type.value,
            'color': self.color
        }


@dataclass
class VerticalGradientColor(Color):
    """Vertical gradient color representation."""
    
    top_color: str
    bottom_color: str
    type: ColorType = field(default=ColorType.VERTICAL_GRADIENT, init=False)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            'type': self.type.value,
            'topColor': self.top_color,
            'bottomColor': self.bottom_color
        }


class Background:
    """Background color that can be either solid or gradient."""
    
    def __init__(self, color: Optional[Color] = None):
        """Initialize background with a color."""
        self.color = color or SolidColor(color='#FFFFFF')
    
    @classmethod
    def solid(cls, color: str) -> 'Background':
        """Create a solid background."""
        return cls(SolidColor(color=color))
    
    @classmethod
    def gradient(cls, top_color: str, bottom_color: str) -> 'Background':
        """Create a gradient background."""
        return cls(VerticalGradientColor(top_color=top_color, bottom_color=bottom_color))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return self.color.to_dict()