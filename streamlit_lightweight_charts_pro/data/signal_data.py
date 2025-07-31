"""
Signal data for background coloring in charts.

This module provides the SignalData class for creating signal-based background
coloring in financial charts. Signal data consists of time points with binary
or ternary values that determine background colors for specific time periods.
"""

from dataclasses import dataclass
from typing import Union
from datetime import datetime


@dataclass
class SignalData:
    """
    Signal data point for background coloring.
    
    SignalData represents a single time point with a signal value that determines
    the background color for that time period. This is commonly used in financial
    charts to highlight specific market conditions, trading signals, or events.
    
    Attributes:
        time (Union[str, datetime]): Time point for the signal. Can be a string
            in ISO format (YYYY-MM-DD) or a datetime object.
        value (int): Signal value that determines background color.
            0: First color (typically neutral/white)
            1: Second color (typically highlight color)
            2: Third color (optional, for ternary signals)
    
    Example:
        ```python
        # Create signal data for background coloring
        signal_data = [
            SignalData("2024-01-01", 0),  # White background
            SignalData("2024-01-02", 1),  # Red background
            SignalData("2024-01-03", 0),  # White background
            SignalData("2024-01-04", 1),  # Red background
        ]
        
        # Use with SignalSeries
        signal_series = SignalSeries(
            data=signal_data,
            color_0="#ffffff",  # White for value=0
            color_1="#ff0000"   # Red for value=1
        )
        ```
    """
    
    time: Union[str, datetime]
    value: int
    
    def __post_init__(self):
        """Validate signal data after initialization."""
        if not isinstance(self.value, int):
            raise ValueError("Signal value must be an integer")
        
        if self.value < 0 or self.value > 2:
            raise ValueError("Signal value must be 0, 1, or 2")
        
        # Convert datetime to string if needed
        if isinstance(self.time, datetime):
            self.time = self.time.strftime("%Y-%m-%d")
        
        # Validate time format
        if isinstance(self.time, str):
            try:
                datetime.strptime(self.time, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Time must be in YYYY-MM-DD format or datetime object")
    
    def asdict(self) -> dict:
        """
        Convert signal data to dictionary format for serialization.
        
        Returns:
            dict: Dictionary representation of the signal data.
        """
        return {
            "time": self.time,
            "value": self.value
        }
    
    def __repr__(self) -> str:
        """String representation of the signal data."""
        return f"SignalData(time='{self.time}', value={self.value})"
    
    def __eq__(self, other) -> bool:
        """Equality comparison for signal data."""
        if not isinstance(other, SignalData):
            return False
        return self.time == other.time and self.value == other.value 