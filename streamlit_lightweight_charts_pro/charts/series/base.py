"""
Base series class for streamlit-lightweight-charts.

This module provides the base Series class that defines the common interface
for all series types in the library. It includes core functionality for
data handling, configuration, and frontend integration.

The Series class serves as the foundation for all series implementations,
providing a consistent interface for series creation, configuration, and
rendering. It supports method chaining for fluent API usage.

Example:
    from streamlit_lightweight_charts_pro.charts.series.base import Series

    class MyCustomSeries(Series):
        def to_frontend_config(self):
            return {"type": "custom", "data": self.data}
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

import pandas as pd

from streamlit_lightweight_charts_pro.data import BaseData, Marker
from streamlit_lightweight_charts_pro.logging_config import get_logger
from streamlit_lightweight_charts_pro.type_definitions import MarkerPosition
from streamlit_lightweight_charts_pro.type_definitions.enums import ColumnNames, MarkerShape

# Initialize logger
logger = get_logger(__name__)


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
        pane_id: The pane index this series belongs to.
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
        pane_id: Optional[int] = 0,
        height: Optional[int] = None,
        overlay: Optional[bool] = True,
        column_mapping: Optional[dict] = None,
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
            pane_id: The pane index this series belongs to. Defaults to 0.

        Example:
            ```python
            # Basic series
            series = LineSeries(data=line_data)

            # With configuration
            series = LineSeries(
                data=line_data,
                visible=True,
                price_line_visible=True,
                price_line_color="#ff0000",
                pane_id=1
            )
            ```
        """
        self.column_mapping = column_mapping

        if isinstance(data, (pd.Series, pd.DataFrame)):
            # Process data input
            self.data = self._normalize_input_data(data)
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
        self.pane_id = pane_id
        self.height = height
        self.overlay = overlay

    def _get_columns(self) -> Dict[str, str]:
        """
        Get the columns to use for the series.
        """
        raise NotImplementedError("Subclasses must implement _get_columns")

    def _normalize_input_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Normalize input data to ensure consistent format.

        This method ensures that the input data is in a consistent format
        for processing. It handles cases where the data is a pandas Series
        or a pandas DataFrame.

        Args:
            data: Pandas DataFrame to normalize.

        Returns:
            pd.DataFrame: Normalized pandas DataFrame.
        """
        if isinstance(data, pd.Series):
            data = data.to_frame()

        columns_mapping = self._get_columns()

        data = self._process_index_columns(data, columns_mapping.values())

        if not all(col in data.columns for col in columns_mapping.values()):
            missing = [col for col in columns_mapping.values() if col not in data.columns]
            raise ValueError(f"Columns {missing} are missing in the data")

        data = self._process_dataframe(data)

        return data

    def _process_index_columns(self, data: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """
        Ensure that all columns in `columns` are available as regular columns,
        even if they are currently part of the index.

        Special handling:
        - If the index is a DatetimeIndex and we need 'datetime',
        assign that name and reset the index.
        - If the index is a MultiIndex, reset it only if any desired column is in it.
        """
        if isinstance(data.index, pd.DatetimeIndex):
            idx_name = data.index.name
            if idx_name is None and ColumnNames.DATETIME in columns:
                data.index.name = ColumnNames.DATETIME
                data = data.reset_index()
            elif idx_name in columns:
                data = data.reset_index()

        elif isinstance(data.index, pd.MultiIndex):
            index_names = list(data.index.names)
            if any(col in index_names for col in columns):
                for i, name in enumerate(index_names):
                    if name is None:
                        index_names[i] = f"level_{i}"
                data.index.names = index_names
                data = data.reset_index()

        return data

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
            format_type: Type of price format ("price", ColumnNames.VOLUME, "percent").
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

    def _validate_pane_config(self):
        """
        Validate pane configuration for the series.

        This method ensures that pane_id is properly set based on the overlay setting.
        It should be called by subclasses in their to_dict() method.

        Raises:
            ValueError: If overlay is False and pane_id is None.
        """
        if self.overlay is False and self.pane_id is None:
            raise ValueError("If overlay is False, pane_id must be defined for the series.")
        if self.overlay is True and self.pane_id is None:
            self.pane_id = 0

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert series to dictionary representation.

        This method must be implemented by subclasses to convert the
        series object into a format that can be consumed by the frontend
        React component.

        Returns:
            Dict[str, Any]: Dictionary representation of the series.

        Raises:
            NotImplementedError: If the subclass doesn't implement this method.
        """

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
                logger.info(f"Value range: {range_info['min_value']} - {range_info['max_value']}")
            ```
        """
        if not self.data:
            return None

        # Extract values and times
        values = []
        times = []

        for item in self.data:
            if hasattr(item, ColumnNames.VALUE):
                if item.value is not None:
                    values.append(item.value)
            elif hasattr(item, ColumnNames.CLOSE):
                if item.close is not None:
                    values.append(item.close)
            elif hasattr(item, ColumnNames.HIGH):
                if item.high is not None and item.low is not None:
                    values.extend([item.high, item.low])

            times.append(item._time)  # pylint: disable=protected-access

        if not values:
            return {
                "min_value": None,
                "max_value": None,
                "min_time": min(times),
                "max_time": max(times),
            }

        return {
            "min_value": min(values),
            "max_value": max(values),
            "min_time": min(times),
            "max_time": max(times),
        }
