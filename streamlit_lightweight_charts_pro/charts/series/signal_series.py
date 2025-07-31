"""
Signal series for background coloring in charts.

This module provides the SignalSeries class for creating signal-based background
coloring in financial charts. SignalSeries creates vertical background bands
that span the entire chart height, colored based on signal values at specific
time points.
"""

from typing import List, Optional, Union
from streamlit_lightweight_charts_pro.charts.series.base import Series
from streamlit_lightweight_charts_pro.data.signal_data import SignalData
from streamlit_lightweight_charts_pro.charts.options.signal_options import SignalOptions


class SignalSeries(Series):
    """
    Signal series for background coloring in charts.
    
    SignalSeries creates vertical background bands that span the entire chart
    height, colored based on signal values at specific time points. This is
    commonly used in financial charts to highlight specific market conditions,
    trading signals, or events.
    
    The series takes signal data with binary or ternary values and maps them
    to background colors for specific time periods. The background bands
    appear across all chart panes and provide visual context for the data.
    
    Attributes:
        data (List[SignalData]): List of signal data points.
        options (SignalOptions): Configuration options for the signal series.
        series_type (str): Type identifier for the series.
    
    Example:
        ```python
        # Create signal data
        signal_data = [
            SignalData("2024-01-01", 0),  # White background
            SignalData("2024-01-02", 1),  # Red background
            SignalData("2024-01-03", 0),  # White background
            SignalData("2024-01-04", 1),  # Red background
        ]
        
        # Create signal series
        signal_series = SignalSeries(
            data=signal_data,
            color_0="#ffffff",  # White for value=0
            color_1="#ff0000"   # Red for value=1
        )
        
        # Add to chart
        chart.add_series(signal_series)
        ```
    """
    
    def __init__(
        self,
        data: List[SignalData],
        color_0: str = "#ffffff",
        color_1: str = "#ff0000",
        color_2: Optional[str] = None,
        opacity: float = 0.3,
        options: Optional[SignalOptions] = None,
    ):
        """
        Initialize SignalSeries.
        
        Args:
            data (List[SignalData]): List of signal data points.
            color_0 (str, optional): Background color for value=0. Defaults to "#ffffff".
            color_1 (str, optional): Background color for value=1. Defaults to "#ff0000".
            color_2 (Optional[str], optional): Background color for value=2. Defaults to None.
            opacity (float, optional): Opacity of background bands (0.0 to 1.0). Defaults to 0.3.
            options (Optional[SignalOptions], optional): Signal options. Defaults to None.
        
        Raises:
            ValueError: If data is empty or invalid.
            ValueError: If opacity is not between 0.0 and 1.0.
        """
        if not data:
            raise ValueError("Signal data cannot be empty")
        
        if not isinstance(data, list):
            raise ValueError("Data must be a list of SignalData objects")
        
        if not all(isinstance(item, SignalData) for item in data):
            raise ValueError("All data items must be SignalData objects")
        
        if not (0.0 <= opacity <= 1.0):
            raise ValueError("Opacity must be between 0.0 and 1.0")
        
        # Initialize options
        if options is None:
            options = SignalOptions()
        
        # Set colors and opacity
        options.set_color_0(color_0)
        options.set_color_1(color_1)
        if color_2:
            options.set_color_2(color_2)
        options.set_opacity(opacity)
        
        super().__init__(data=data, options=options)
        self.series_type = "signal"
    
    def asdict(self) -> dict:
        """
        Convert signal series to dictionary format for frontend serialization.
        
        Returns:
            dict: Dictionary representation of the signal series.
        """
        series_dict = {
            "type": self.series_type,
            "data": [item.asdict() for item in self.data],
            "options": self.options.asdict() if self.options else {}
        }
        
        return series_dict
    
    def add_signal(self, signal: SignalData) -> "SignalSeries":
        """
        Add a signal data point to the series.
        
        Args:
            signal (SignalData): Signal data point to add.
        
        Returns:
            SignalSeries: Self for method chaining.
        
        Raises:
            ValueError: If signal is not a SignalData object.
        """
        if not isinstance(signal, SignalData):
            raise ValueError("Signal must be a SignalData object")
        
        self.data.append(signal)
        return self
    
    def add_signals(self, signals: List[SignalData]) -> "SignalSeries":
        """
        Add multiple signal data points to the series.
        
        Args:
            signals (List[SignalData]): List of signal data points to add.
        
        Returns:
            SignalSeries: Self for method chaining.
        
        Raises:
            ValueError: If signals is not a list or contains invalid items.
        """
        if not isinstance(signals, list):
            raise ValueError("Signals must be a list")
        
        if not all(isinstance(item, SignalData) for item in signals):
            raise ValueError("All signals must be SignalData objects")
        
        self.data.extend(signals)
        return self
    
    def get_signals_by_value(self, value: int) -> List[SignalData]:
        """
        Get all signal data points with a specific value.
        
        Args:
            value (int): Signal value to filter by.
        
        Returns:
            List[SignalData]: List of signal data points with the specified value.
        """
        return [signal for signal in self.data if signal.value == value]
    
    def get_time_range(self) -> tuple:
        """
        Get the time range of the signal data.
        
        Returns:
            tuple: (start_time, end_time) as strings.
        """
        if not self.data:
            return None, None
        
        times = [signal.time for signal in self.data]
        return min(times), max(times)
    
    def __repr__(self) -> str:
        """String representation of the signal series."""
        return f"SignalSeries(data_points={len(self.data)}, options={self.options})" 