"""
Background data model for background shade series.

This module provides the BackgroundData class for creating background shading
based on indicator values. The background color is interpolated between
minColor and maxColor based on the data value.

Example:
    ```python
    from streamlit_lightweight_charts_pro.data.background_data import BackgroundData
    
    # Create background data with custom colors
    data = BackgroundData(
        time="2024-01-01",
        value=0.75,
        minColor="#FF0000",  # Red for low values
        maxColor="#00FF00"   # Green for high values
    )
    ```
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional

from streamlit_lightweight_charts_pro.data.single_value_data import SingleValueData
from streamlit_lightweight_charts_pro.utils.data_utils import is_valid_color


@dataclass
class BackgroundData(SingleValueData):
    """
    Data point for background shade series.
    
    This class represents a single data point for background shading that changes
    color based on indicator values. The color is interpolated between minColor
    and maxColor based on the value.
    
    Attributes:
        time: The timestamp for this data point (inherited from SingleValueData)
        value: The indicator value (0.0 to 1.0 recommended for color interpolation)
        minColor: Color for minimum values (default: "#FFFFFF" - white)
        maxColor: Color for maximum values (default: "#2196F3" - blue)
        
    Raises:
        ValueError: If minColor or maxColor are not valid color formats
        
    Example:
        ```python
        # Create background data for RSI indicator
        data = BackgroundData(
            time="2024-01-01 10:00:00",
            value=0.7,  # RSI normalized to 0-1 range
            minColor="#FFE5E5",  # Light red for oversold
            maxColor="#E5FFE5"   # Light green for overbought
        )
        ```
    """
    
    minColor: str = "#FFFFFF"
    maxColor: str = "#2196F3"
    
    def __post_init__(self):
        """Validate color values after initialization."""
        super().__post_init__()
        
        if not is_valid_color(self.minColor):
            raise ValueError(
                f"Invalid minColor format: {self.minColor!r}. "
                f"Must be hex or rgba format."
            )
        
        if not is_valid_color(self.maxColor):
            raise ValueError(
                f"Invalid maxColor format: {self.maxColor!r}. "
                f"Must be hex or rgba format."
            )
    
    @property
    def required_columns(self) -> set:
        """Get required columns for DataFrame conversion."""
        return super().required_columns | {"minColor", "maxColor"}
    
    @property
    def optional_columns(self) -> set:
        """Get optional columns for DataFrame conversion."""
        return super().optional_columns
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary for frontend consumption.
        
        Returns:
            Dict[str, Any]: Dictionary with time, value, minColor, and maxColor
            
        Example:
            ```python
            data = BackgroundData(time="2024-01-01", value=0.5)
            dict_data = data.to_dict()
            # {'time': 1704067200, 'value': 0.5, 
            #  'minColor': '#FFFFFF', 'maxColor': '#2196F3'}
            ```
        """
        result = super().to_dict()
        result["minColor"] = self.minColor
        result["maxColor"] = self.maxColor
        return result