"""
Signal options for background coloring configuration.

This module provides the SignalOptions class for configuring signal-based
background coloring in financial charts. SignalOptions defines colors,
opacity, and other styling properties for background bands.
"""

from typing import Optional
from streamlit_lightweight_charts_pro.charts.options.base_options import Options
from streamlit_lightweight_charts_pro.utils.chainable import chainable_field


class SignalOptions(Options):
    """
    Configuration options for signal series background coloring.
    
    SignalOptions defines the colors, opacity, and styling properties for
    background bands created by SignalSeries. The options control how
    signal values are mapped to visual background colors.
    
    Attributes:
        color_0 (str): Background color for signal value=0.
        color_1 (str): Background color for signal value=1.
        color_2 (Optional[str]): Background color for signal value=2.
        visible (bool): Whether the signal series is visible.
    
    Example:
        ```python
        # Create signal options
        options = SignalOptions()
        options.set_color_0("#ffffff")  # White for value=0
        options.set_color_1("#ff0000")  # Red for value=1
        
        # Use with SignalSeries
        signal_series = SignalSeries(data=signal_data, options=options)
        ```
    """
    
    def __init__(
        self,
        color_0: str = "#ffffff",
        color_1: str = "#ff0000",
        color_2: Optional[str] = None,
        visible: bool = True,
    ):
        """
        Initialize SignalOptions.
        
        Args:
            color_0 (str, optional): Background color for value=0. Defaults to "#ffffff".
            color_1 (str, optional): Background color for value=1. Defaults to "#ff0000".
            color_2 (Optional[str], optional): Background color for value=2. Defaults to None.
            visible (bool, optional): Whether the signal series is visible. Defaults to True.
        
        Raises:
            ValueError: If colors are not valid hex color strings.
        """
        
        # Validate color format (simple hex validation)
        for color_name, color_value in [("color_0", color_0), ("color_1", color_1)]:
            if not self._is_valid_hex_color(color_value):
                raise ValueError(f"{color_name} must be a valid hex color string")
        
        if color_2 and not self._is_valid_hex_color(color_2):
            raise ValueError("color_2 must be a valid hex color string")
        
        super().__init__()
        self.color_0 = color_0
        self.color_1 = color_1
        self.color_2 = color_2
        self.visible = visible
    
    @staticmethod
    def _is_valid_hex_color(color: str) -> bool:
        """
        Validate if a string is a valid hex color.
        
        Args:
            color (str): Color string to validate.
        
        Returns:
            bool: True if valid hex color, False otherwise.
        """
        if not isinstance(color, str):
            return False
        
        if not color.startswith("#"):
            return False
        
        if len(color) not in [4, 7, 9]:  # #RGB, #RRGGBB, #RRGGBBAA
            return False
        
        try:
            int(color[1:], 16)
            return True
        except ValueError:
            return False
    
    @chainable_field
    def set_color_0(self, color: str) -> "SignalOptions":
        """
        Set background color for signal value=0.
        
        Args:
            color (str): Hex color string (e.g., "#ffffff").
        
        Returns:
            SignalOptions: Self for method chaining.
        
        Raises:
            ValueError: If color is not a valid hex color string.
        """
        if not self._is_valid_hex_color(color):
            raise ValueError("Color must be a valid hex color string")
        
        self.color_0 = color
        return self
    
    @chainable_field
    def set_color_1(self, color: str) -> "SignalOptions":
        """
        Set background color for signal value=1.
        
        Args:
            color (str): Hex color string (e.g., "#ff0000").
        
        Returns:
            SignalOptions: Self for method chaining.
        
        Raises:
            ValueError: If color is not a valid hex color string.
        """
        if not self._is_valid_hex_color(color):
            raise ValueError("Color must be a valid hex color string")
        
        self.color_1 = color
        return self
    
    @chainable_field
    def set_color_2(self, color: str) -> "SignalOptions":
        """
        Set background color for signal value=2.
        
        Args:
            color (str): Hex color string (e.g., "#00ff00").
        
        Returns:
            SignalOptions: Self for method chaining.
        
        Raises:
            ValueError: If color is not a valid hex color string.
        """
        if not self._is_valid_hex_color(color):
            raise ValueError("Color must be a valid hex color string")
        
        self.color_2 = color
        return self
    

    
    @chainable_field
    def set_visible(self, visible: bool) -> "SignalOptions":
        """
        Set visibility of the signal series.
        
        Args:
            visible (bool): Whether the signal series should be visible.
        
        Returns:
            SignalOptions: Self for method chaining.
        """
        self.visible = bool(visible)
        return self
    
    def asdict(self) -> dict:
        """
        Convert signal options to dictionary format for serialization.
        
        Returns:
            dict: Dictionary representation of the signal options.
        """
        options_dict = {
            "color0": self.color_0,
            "color1": self.color_1,
            "visible": self.visible,
        }
        
        if self.color_2:
            options_dict["color2"] = self.color_2
        
        return options_dict
    
    def __repr__(self) -> str:
        """String representation of the signal options."""
        return (
            f"SignalOptions(color_0='{self.color_0}', color_1='{self.color_1}', "
            f"color_2='{self.color_2}', visible={self.visible})"
        ) 