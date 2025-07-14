"""Data model classes for streamlit-lightweight-charts."""

from typing import Union, Optional, Dict, Any, List
from dataclasses import dataclass, asdict
from enum import Enum


class MarkerShape(str, Enum):
    """Marker shape enumeration."""
    
    CIRCLE = 'circle'
    SQUARE = 'square'
    ARROW_UP = 'arrowUp'
    ARROW_DOWN = 'arrowDown'


class MarkerPosition(str, Enum):
    """Marker position enumeration."""
    
    ABOVE_BAR = 'aboveBar'
    BELOW_BAR = 'belowBar'
    IN_BAR = 'inBar'


@dataclass
class BaseData:
    """Base class for all data points."""
    
    time: Union[str, int, float]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        result = asdict(self)
        # Remove None values
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class SingleValueData(BaseData):
    """Data point for line, area charts."""
    
    value: float


@dataclass
class OhlcData(BaseData):
    """Data point for candlestick and bar charts."""
    
    open: float
    high: float
    low: float
    close: float


@dataclass
class HistogramData(BaseData):
    """Data point for histogram charts."""
    
    value: float
    color: Optional[str] = None


@dataclass
class BaselineData(BaseData):
    """Data point for baseline charts."""
    
    value: float


@dataclass
class Marker:
    """Chart marker definition."""
    
    time: Union[str, int, float]
    position: MarkerPosition
    color: str
    shape: MarkerShape
    text: Optional[str] = None
    size: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        result = {
            'time': self.time,
            'position': self.position.value,
            'color': self.color,
            'shape': self.shape.value
        }
        if self.text is not None:
            result['text'] = self.text
        if self.size is not None:
            result['size'] = self.size
        return result