"""Data model classes for streamlit-lightweight-charts."""

from typing import Union, Optional, Dict, Any, List
from dataclasses import dataclass, asdict, field
from enum import Enum
from datetime import datetime
import pandas as pd


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


def to_utc_timestamp(time_value: Union[str, int, float, datetime, pd.Timestamp]) -> Union[str, int]:
    """
    Convert various time formats to UTC timestamp.
    
    Args:
        time_value: Time in various formats
        
    Returns:
        UTC timestamp (int) or date string (str) for compatibility
    """
    if isinstance(time_value, str):
        # Try to parse as date string
        try:
            # Check if it's already a date string in YYYY-MM-DD format
            pd.to_datetime(time_value)
            return time_value
        except:
            # If not parseable, return as is
            return time_value
    elif isinstance(time_value, (int, float)):
        # Already a timestamp
        return int(time_value)
    elif isinstance(time_value, datetime):
        # Convert datetime to UTC timestamp
        return int(time_value.timestamp())
    elif isinstance(time_value, pd.Timestamp):
        # Convert pandas Timestamp to UTC timestamp
        return int(time_value.timestamp())
    else:
        raise ValueError(f"Unsupported time type: {type(time_value)}")


def from_utc_timestamp(time_value: Union[str, int]) -> pd.Timestamp:
    """
    Convert UTC timestamp or date string to pandas Timestamp.
    
    Args:
        time_value: UTC timestamp or date string
        
    Returns:
        Pandas Timestamp
    """
    if isinstance(time_value, str):
        return pd.to_datetime(time_value)
    elif isinstance(time_value, (int, float)):
        return pd.to_datetime(time_value, unit='s')
    else:
        raise ValueError(f"Unsupported time type: {type(time_value)}")


@dataclass
class BaseData:
    """Base class for all data points."""
    
    _time: Union[str, int] = field(default=None, init=False, repr=False)
    
    def __post_init__(self):
        """Initialize time if not set."""
        if self._time is None:
            raise ValueError("time must be provided")
    
    @property
    def time(self) -> pd.Timestamp:
        """
        Get time as pandas Timestamp.
        
        Returns:
            Pandas Timestamp
        """
        return from_utc_timestamp(self._time)
    
    @time.setter
    def time(self, value: Union[str, int, float, datetime, pd.Timestamp]):
        """
        Set time from various formats.
        
        Args:
            value: Time in various formats (string, timestamp, datetime, pd.Timestamp)
        """
        self._time = to_utc_timestamp(value)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        result = {}
        # Add time
        result['time'] = self._time
        # Add other fields
        for key, value in self.__dict__.items():
            if not key.startswith('_') and value is not None:
                result[key] = value
        return result


@dataclass
class SingleValueData(BaseData):
    """Data point for line, area charts."""
    
    value: float
    
    def __init__(self, time: Union[str, int, float, datetime, pd.Timestamp], value: float):
        """Initialize with time and value."""
        self.time = time
        self.value = value


@dataclass
class OhlcData(BaseData):
    """Data point for candlestick and bar charts."""
    
    open: float
    high: float
    low: float
    close: float
    
    def __init__(
        self,
        time: Union[str, int, float, datetime, pd.Timestamp],
        open: float,
        high: float,
        low: float,
        close: float
    ):
        """Initialize with time and OHLC values."""
        self.time = time
        self.open = open
        self.high = high
        self.low = low
        self.close = close


@dataclass
class HistogramData(BaseData):
    """Data point for histogram charts."""
    
    value: float
    color: Optional[str] = None
    
    def __init__(
        self,
        time: Union[str, int, float, datetime, pd.Timestamp],
        value: float,
        color: Optional[str] = None
    ):
        """Initialize with time, value, and optional color."""
        self.time = time
        self.value = value
        self.color = color


@dataclass
class BaselineData(BaseData):
    """Data point for baseline charts."""
    
    value: float
    
    def __init__(self, time: Union[str, int, float, datetime, pd.Timestamp], value: float):
        """Initialize with time and value."""
        self.time = time
        self.value = value


@dataclass
class Marker:
    """Chart marker definition."""
    
    _time: Union[str, int] = field(default=None, init=False, repr=False)
    position: MarkerPosition
    color: str
    shape: MarkerShape
    text: Optional[str] = None
    size: Optional[int] = None
    
    def __init__(
        self,
        time: Union[str, int, float, datetime, pd.Timestamp],
        position: MarkerPosition,
        color: str,
        shape: MarkerShape,
        text: Optional[str] = None,
        size: Optional[int] = None
    ):
        """Initialize marker with time and properties."""
        self.time = time
        self.position = position
        self.color = color
        self.shape = shape
        self.text = text
        self.size = size
    
    @property
    def time(self) -> pd.Timestamp:
        """
        Get time as pandas Timestamp.
        
        Returns:
            Pandas Timestamp
        """
        return from_utc_timestamp(self._time)
    
    @time.setter
    def time(self, value: Union[str, int, float, datetime, pd.Timestamp]):
        """
        Set time from various formats.
        
        Args:
            value: Time in various formats (string, timestamp, datetime, pd.Timestamp)
        """
        self._time = to_utc_timestamp(value)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        result = {
            'time': self._time,
            'position': self.position.value,
            'color': self.color,
            'shape': self.shape.value
        }
        if self.text is not None:
            result['text'] = self.text
        if self.size is not None:
            result['size'] = self.size
        return result