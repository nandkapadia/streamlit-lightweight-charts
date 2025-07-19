"""
Base series class for streamlit-lightweight-charts.

This module provides the base Series class that defines the common interface
for all series types in the library. It includes core functionality for
data handling, configuration, and frontend integration.

The Series class serves as the foundation for all series implementations,
providing a consistent interface for series creation, configuration, and
rendering. It supports method chaining for fluent API usage.

Example:
    ```python
    from streamlit_lightweight_charts_pro.charts.series.base import Series
    
    class MyCustomSeries(Series):
        def to_frontend_config(self):
            return {"type": "custom", "data": self.data}
    ```
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

import pandas as pd

from ...data import Marker, MarkerPosition, MarkerShape
from ...data.models import BaseData


def _get_enum_value(value, enum_class):
    """
    Helper function to get enum value, handling both enum objects and strings.
    
    This function safely converts enum values to their string representations,
    handling cases where the value might already be a string or an enum object.
    
    Args:
        value: The value to convert (can be enum object or string)
        enum_class: The enum class to use for conversion
        
    Returns:
        str: The string value of the enum
        
    Example:
        ```python
        # With enum object
        _get_enum_value(LineStyle.SOLID, LineStyle)  # Returns "solid"
        
        # With string
        _get_enum_value("solid", LineStyle)  # Returns "solid"
        ```
    """
    if isinstance(value, enum_class):
        return value.value
    elif isinstance(value, str):
        # Try to convert string to enum
        try:
            return enum_class(value).value
        except ValueError:
            # If conversion fails, return the string as-is
            return value
    else:
        return value


class Series(ABC):
    """
    Abstract base class for all series types.
    
    This class defines the common interface and functionality that all series
    classes must implement. It provides core data handling, configuration
    methods, and frontend integration capabilities.
    
    All series classes should inherit from this base class and implement
    the required abstract methods. The class supports method chaining for
    fluent API usage.
    
    Attributes:
        data: List of data points for this series
        visible: Whether the series is currently visible
        price_scale_id: ID of the price scale this series is attached to
        price_line_visible: Whether to show the price line for this series
        base_line_visible: Whether to show the base line for this series
        price_line_width: Width of the price line in pixels
        price_line_color: Color of the price line
        price_line_style: Style of the price line (solid, dashed, etc.)
        base_line_width: Width of the base line in pixels
        base_line_color: Color of the base line
        base_line_style: Style of the base line
        price_format: Price formatting configuration
        markers: List of markers to display on this series
        price_scale_config: Configuration for the price scale
    """

    def __init__(
        self,
        data: Union[List[BaseData], pd.DataFrame],
        visible: bool = True,
        price_scale_id: str = "right",
        price_line_visible: bool = False,
        base_line_visible: bool = False,
        price_line_width: int = 1,
        price_line_color: str = "#2196F3",
        price_line_style: str = "solid",
        base_line_width: int = 1,
        base_line_color: str = "#FF9800",
        base_line_style: str = "solid",
        price_format: Optional[Dict[str, Any]] = None,
        markers: Optional[List[Marker]] = None,
        price_scale_config: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize a series with data and configuration.
        
        Args:
            data: Series data as a list of data objects or pandas DataFrame.
            visible: Whether the series is visible. Defaults to True.
            price_scale_id: ID of the price scale to attach to. Defaults to "right".
            price_line_visible: Whether to show the price line. Defaults to False.
            base_line_visible: Whether to show the base line. Defaults to False.
            price_line_width: Width of the price line in pixels. Defaults to 1.
            price_line_color: Color of the price line. Defaults to "#2196F3".
            price_line_style: Style of the price line. Defaults to "solid".
            base_line_width: Width of the base line in pixels. Defaults to 1.
            base_line_color: Color of the base line. Defaults to "#FF9800".
            base_line_style: Style of the base line. Defaults to "solid".
            price_format: Price formatting configuration. Defaults to None.
            markers: List of markers to display. Defaults to None.
            price_scale_config: Price scale configuration. Defaults to None.
            
        Example:
            ```python
            # Basic series
            series = LineSeries(data=line_data)
            
            # With configuration
            series = LineSeries(
                data=line_data,
                visible=True,
                price_line_visible=True,
                price_line_color="#ff0000"
            )
            ```
        """
        # Process data input
        if isinstance(data, pd.DataFrame):
            self.data = self._process_dataframe(data)
        else:
            self.data = data

        # Basic configuration
        self.visible = visible
        self.price_scale_id = price_scale_id

        # Price line configuration
        self.price_line_visible = price_line_visible
        self.price_line_width = price_line_width
        self.price_line_color = price_line_color
        self.price_line_style = price_line_style

        # Base line configuration
        self.base_line_visible = base_line_visible
        self.base_line_width = base_line_width
        self.base_line_color = base_line_color
        self.base_line_style = base_line_style

        # Price formatting
        self.price_format = price_format or {"type": "price", "precision": 2}

        # Markers
        self.markers = markers or []

        # Price scale configuration
        self.price_scale_config = price_scale_config or {}

    @abstractmethod
    def _process_dataframe(self, df: pd.DataFrame) -> List[BaseData]:
        """
        Process pandas DataFrame into series data format.
        
        This method must be implemented by subclasses to convert pandas
        DataFrames into the appropriate data format for the series type.
        
        Args:
            df: Pandas DataFrame to process.
                
        Returns:
            List[BaseData]: List of processed data objects.
            
        Raises:
            NotImplementedError: If the subclass doesn't implement this method.
        """
        raise NotImplementedError("Subclasses must implement _process_dataframe")

    def set_visible(self, visible: bool) -> "Series":
        """
        Set series visibility.
        
        Shows or hides the series. Returns self for method chaining.
        
        Args:
            visible: Whether the series should be visible.
                
        Returns:
            Series: Self for method chaining.
            
        Example:
            ```python
            series.set_visible(False)
            ```
        """
        self.visible = visible
        return self

    def set_price_scale(self, price_scale_id: str) -> "Series":
        """
        Set the price scale for this series.
        
        Specifies which price scale (left or right) this series should
        be attached to. Returns self for method chaining.
        
        Args:
            price_scale_id: ID of the price scale ("left" or "right").
                
        Returns:
            Series: Self for method chaining.
            
        Example:
            ```python
            series.set_price_scale("left")
            ```
        """
        self.price_scale_id = price_scale_id
        return self

    def set_price_line(
        self,
        visible: bool = True,
        width: Optional[int] = None,
        color: Optional[str] = None,
        style: Optional[str] = None,
    ) -> "Series":
        """
        Configure the price line for this series.
        
        Sets the price line configuration including visibility, width,
        color, and style. Returns self for method chaining.
        
        Args:
            visible: Whether the price line should be visible.
            width: Width of the price line in pixels.
            color: Color of the price line.
            style: Style of the price line ("solid", "dashed", "dotted").
                
        Returns:
            Series: Self for method chaining.
            
        Example:
            ```python
            series.set_price_line(visible=True, color="#ff0000", width=2)
            ```
        """
        self.price_line_visible = visible
        if width is not None:
            self.price_line_width = width
        if color is not None:
            self.price_line_color = color
        if style is not None:
            self.price_line_style = style
        return self

    def set_base_line(
        self,
        visible: bool = True,
        width: Optional[int] = None,
        color: Optional[str] = None,
        style: Optional[str] = None,
    ) -> "Series":
        """
        Configure the base line for this series.
        
        Sets the base line configuration including visibility, width,
        color, and style. Returns self for method chaining.
        
        Args:
            visible: Whether the base line should be visible.
            width: Width of the base line in pixels.
            color: Color of the base line.
            style: Style of the base line ("solid", "dashed", "dotted").
                
        Returns:
            Series: Self for method chaining.
            
        Example:
            ```python
            series.set_base_line(visible=True, color="#00ff00", width=1)
            ```
        """
        self.base_line_visible = visible
        if width is not None:
            self.base_line_width = width
        if color is not None:
            self.base_line_color = color
        if style is not None:
            self.base_line_style = style
        return self

    def set_price_format(
        self,
        format_type: str = "price",
        precision: int = 2,
        min_move: float = 0.01,
    ) -> "Series":
        """
        Set price formatting for this series.
        
        Configures how prices are formatted and displayed. Returns self
        for method chaining.
        
        Args:
            format_type: Type of price format ("price", "volume", "percent").
            precision: Number of decimal places to display.
            min_move: Minimum price movement for formatting.
                
        Returns:
            Series: Self for method chaining.
            
        Example:
            ```python
            series.set_price_format(format_type="price", precision=4)
            ```
        """
        self.price_format = {
            "type": format_type,
            "precision": precision,
            "minMove": min_move,
        }
        return self

    def add_marker(
        self,
        time: Union[str, int, float, pd.Timestamp],
        position: MarkerPosition,
        color: str,
        shape: MarkerShape,
        text: Optional[str] = None,
        size: Optional[int] = None,
    ) -> "Series":
        """
        Add a marker to this series.
        
        Creates and adds a marker to the series. Returns self for
        method chaining.
        
        Args:
            time: Time for the marker in various formats.
            position: Position of the marker relative to the data point.
            color: Color of the marker.
            shape: Shape of the marker.
            text: Optional text to display with the marker.
            size: Optional size of the marker in pixels.
                
        Returns:
            Series: Self for method chaining.
            
        Example:
            ```python
            series.add_marker(
                time="2024-01-01",
                position=MarkerPosition.ABOVE_BAR,
                color="#ff0000",
                shape=MarkerShape.CIRCLE,
                text="Buy Signal"
            )
            ```
        """
        marker = Marker(
            time=time,
            position=position,
            color=color,
            shape=shape,
            text=text,
            size=size,
        )
        self.markers.append(marker)
        return self

    def add_markers(self, markers: List[Marker]) -> "Series":
        """
        Add multiple markers to this series.
        
        Adds a list of markers to the series. Returns self for
        method chaining.
        
        Args:
            markers: List of marker objects to add.
                
        Returns:
            Series: Self for method chaining.
            
        Example:
            ```python
            markers = [marker1, marker2, marker3]
            series.add_markers(markers)
            ```
        """
        self.markers.extend(markers)
        return self

    def clear_markers(self) -> "Series":
        """
        Clear all markers from this series.
        
        Removes all markers from the series. Returns self for
        method chaining.
        
        Returns:
            Series: Self for method chaining.
            
        Example:
            ```python
            series.clear_markers()
            ```
        """
        self.markers.clear()
        return self

    def set_price_scale_config(self, **kwargs) -> "Series":
        """
        Set price scale configuration for this series.
        
        Updates the price scale configuration options. Returns self
        for method chaining.
        
        Args:
            **kwargs: Price scale configuration options to update.
                
        Returns:
            Series: Self for method chaining.
            
        Example:
            ```python
            series.set_price_scale_config(
                autoScale=True,
                scaleMargins={"top": 0.1, "bottom": 0.1}
            )
            ```
        """
        self.price_scale_config.update(kwargs)
        return self

    @abstractmethod
    def to_frontend_config(self) -> Dict[str, Any]:
        """
        Convert series to frontend-compatible configuration.
        
        This method must be implemented by subclasses to convert the
        series object into a format that can be consumed by the frontend
        React component.
        
        Returns:
            Dict[str, Any]: Frontend-compatible configuration dictionary.
            
        Raises:
            NotImplementedError: If the subclass doesn't implement this method.
        """
        raise NotImplementedError("Subclasses must implement to_frontend_config")

    def get_data_range(self) -> Optional[Dict[str, Union[float, str]]]:
        """
        Get the data range for this series.
        
        Returns the minimum and maximum values and times for the series data.
        Useful for determining chart bounds and scaling.
        
        Returns:
            Optional[Dict[str, Union[float, str]]]: Dictionary containing
                min_value, max_value, min_time, max_time, or None if no data.
                
        Example:
            ```python
            range_info = series.get_data_range()
            if range_info:
                print(f"Value range: {range_info['min_value']} - {range_info['max_value']}")
            ```
        """
        if not self.data:
            return None

        # Extract values and times
        values = []
        times = []
        
        for item in self.data:
            if hasattr(item, 'value'):
                values.append(item.value)
            elif hasattr(item, 'close'):
                values.append(item.close)
            elif hasattr(item, 'high'):
                values.extend([item.high, item.low])
            
            times.append(item.timestamp)

        if not values:
            return None

        return {
            "min_value": min(values),
            "max_value": max(values),
            "min_time": min(times),
            "max_time": max(times),
        } 