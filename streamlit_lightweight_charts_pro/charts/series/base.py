"""
Base series class for streamlit-lightweight-charts.

This module provides the base Series class that defines the common interface
for all series types in the library. It includes core functionality for
data handling, configuration, and frontend integration.

The Series class serves as the foundation for all series implementations,
providing a consistent interface for series creation, configuration, and
rendering. It supports method chaining for fluent API usage and includes
comprehensive data validation and conversion capabilities.

Example:
    ```python
    from streamlit_lightweight_charts_pro.charts.series.base import Series

    class MyCustomSeries(Series):
        def to_frontend_config(self):
            return {"type": "custom", "data": self.data}
    ```
"""

from abc import ABC
from typing import Any, Dict, List, Optional, Type, Union

import pandas as pd

# Import options classes for dynamic creation
from streamlit_lightweight_charts_pro.charts.options import (
    LineOptions,
    PriceFormatOptions,
    PriceLineOptions,
)
from streamlit_lightweight_charts_pro.data import Data
from streamlit_lightweight_charts_pro.data.data import classproperty
from streamlit_lightweight_charts_pro.data.marker import Marker
from streamlit_lightweight_charts_pro.logging_config import get_logger
from streamlit_lightweight_charts_pro.type_definitions import MarkerPosition
from streamlit_lightweight_charts_pro.type_definitions.enums import MarkerShape
from streamlit_lightweight_charts_pro.utils import chainable_property
from streamlit_lightweight_charts_pro.utils.data_utils import snake_to_camel

# Initialize logger
logger = get_logger(__name__)


# pylint: disable=no-member, invalid-name
@chainable_property("price_scale_id")
@chainable_property("price_format")
@chainable_property("price_lines")
@chainable_property("markers")
@chainable_property("pane_id")
class Series(ABC):
    """
    Abstract base class for all series types.

    This class defines the common interface and functionality that all series
    classes must implement. It provides core data handling, configuration
    methods, and frontend integration capabilities with comprehensive support
    for pandas DataFrame integration, markers, price lines, and formatting.

    All series classes should inherit from this base class and implement
    the required abstract methods. The class supports method chaining for
    fluent API usage and provides extensive customization options.

    Key Features:
        - DataFrame integration with column mapping
        - Marker and price line management
        - Price scale and pane configuration
        - Visibility and formatting controls
        - Comprehensive data validation
        - Method chaining support

    Attributes:
        data (List[Data]): List of data points for this series.
        visible (bool): Whether the series is currently visible.
        price_scale_id (str): ID of the price scale this series is attached to.
        price_format (PriceFormatOptions): Price formatting configuration.
        price_lines (List[PriceLineOptions]): List of price lines for this series.
        markers (List[Marker]): List of markers to display on this series.
        pane_id (int): The pane index this series belongs to.

    Note:
        Subclasses must define a class-level DATA_CLASS attribute for from_dataframe to work.
        The data_class property will always pick the most-derived DATA_CLASS in the MRO.
    """

    def __init__(
        self,
        data: Union[List[Data], pd.DataFrame, pd.Series],
        column_mapping: Optional[dict] = None,
        visible: bool = True,
        price_scale_id: str = "right",
        pane_id: Optional[int] = 0,
    ):
        """
        Initialize a series with data and configuration.

        Creates a new series instance with the provided data and configuration options.
        The constructor supports multiple data input types including lists of Data
        objects, pandas DataFrames, and pandas Series with automatic validation
        and conversion.

        Args:
            data (Union[List[Data], pd.DataFrame, pd.Series]): Series data as a list
                of data objects, pandas DataFrame, or pandas Series.
            column_mapping (Optional[dict]): Optional column mapping for DataFrame/Series
                input. Required when providing DataFrame or Series data.
            visible (bool, optional): Whether the series is visible. Defaults to True.
            price_scale_id (str, optional): ID of the price scale to attach to.
                Defaults to "right".
            pane_id (Optional[int], optional): The pane index this series belongs to.
                Defaults to 0.

        Raises:
            ValueError: If data is not a valid type (list of Data objects, DataFrame, or Series).
            ValueError: If DataFrame/Series is provided without column_mapping.
            ValueError: If all items in data list are not instances of Data or its subclasses.

        Example:
            ```python
            # Basic series with list of data objects
            series = LineSeries(data=line_data)

            # Series with DataFrame
            series = LineSeries(
                data=df,
                column_mapping={'time': 'datetime', 'value': 'close'}
            )

            # Series with Series
            series = LineSeries(
                data=series_data,
                column_mapping={'time': 'index', 'value': 'values'}
            )

            # Series with custom configuration
            series = LineSeries(
                data=line_data,
                visible=False,
                price_scale_id="left",
                pane_id=1
            )
            ```
        """
        # Validate and process data
        if data is None:
            self.data = []
        elif isinstance(data, (pd.DataFrame, pd.Series)):
            if column_mapping is None:
                raise ValueError(
                    "column_mapping is required when providing DataFrame or Series data"
                )
            # Process DataFrame/Series using from_dataframe logic
            self.data = self._process_dataframe_input(data, column_mapping)
        elif isinstance(data, list):
            # Validate that all items are Data instances
            if data and not all(isinstance(item, Data) for item in data):
                raise ValueError(
                    "All items in data list must be instances of Data or its subclasses"
                )
            self.data = data
        else:
            raise ValueError(
                f"data must be a list of SingleValueData objects, DataFrame, or Series, "
                f"got {type(data)}"
            )

        self.visible = visible
        self._price_scale_id = price_scale_id
        self._price_format = None
        self._price_lines = []
        self._markers = []
        self._pane_id = pane_id
        self.column_mapping = column_mapping

    @staticmethod
    def prepare_index(df: pd.DataFrame, column_mapping: Dict[str, str]) -> pd.DataFrame:
        """
        Prepare index for column mapping.

        Handles all index-related column mapping cases:
        - Time column mapping with DatetimeIndex
        - Level position mapping (e.g., "0", "1")
        - "index" mapping (first unnamed level or level 0)
        - Named level mapping (e.g., "date", "symbol")
        - Single index reset for non-time columns

        Args:
            df: DataFrame to prepare
            column_mapping: Mapping of required fields to column names

        Returns:
            DataFrame with prepared index

        Raises:
            ValueError: If time column is not found and no DatetimeIndex is available
        """
        # Handle time column mapping first (special case for DatetimeIndex)
        if "time" in column_mapping:
            time_col = column_mapping["time"]
            if time_col not in df.columns:
                # Handle single DatetimeIndex
                if isinstance(df.index, pd.DatetimeIndex):
                    if df.index.name is None:
                        # Set name and reset index to make it a regular column
                        df.index.name = time_col
                        df = df.reset_index()
                    elif df.index.name == time_col:
                        # Index name already matches, just reset to make it a regular column
                        df = df.reset_index()

                # Handle MultiIndex with DatetimeIndex level
                elif isinstance(df.index, pd.MultiIndex):
                    for i, level in enumerate(df.index.levels):
                        if isinstance(level, pd.DatetimeIndex):
                            if df.index.names[i] is None:
                                # Set name for this level and reset it
                                new_names = list(df.index.names)
                                new_names[i] = time_col
                                df.index.names = new_names
                                df = df.reset_index(level=time_col)
                                break
                            elif df.index.names[i] == time_col:
                                # Level name already matches, reset this level
                                df = df.reset_index(level=time_col)
                                break
                    else:
                        # No DatetimeIndex level found, check if any level name matches
                        if time_col in df.index.names:
                            # Reset the matching level
                            df = df.reset_index(level=time_col)
                        else:
                            # No matching level found
                            raise ValueError(
                                f"Time column '{time_col}' not found in DataFrame columns and no "
                                f"DatetimeIndex available in the index"
                            )
                else:
                    # No DatetimeIndex found
                    # Check if time_col is "index" and we have a regular index to reset
                    if time_col == "index":
                        # Reset the index to make it a regular column
                        idx_name = df.index.name
                        df = df.reset_index()
                        new_col_name = idx_name if idx_name is not None else "index"
                        column_mapping["time"] = new_col_name
                    else:
                        raise ValueError(
                            f"Time column '{time_col}' not found in DataFrame columns and no "
                            f"DatetimeIndex available in the index"
                        )

        # Handle other index columns
        for field, col_name in column_mapping.items():
            if field == "time":
                continue  # Already handled above

            if col_name not in df.columns:
                if isinstance(df.index, pd.MultiIndex):
                    level_names = list(df.index.names)

                    # Integer string or int: treat as level position
                    try:
                        level_idx = int(col_name)
                        if 0 <= level_idx < len(df.index.levels):
                            df = df.reset_index(level=level_idx)
                            level_name = level_names[level_idx]
                            # Update column mapping to use actual column name
                            new_col_name = (
                                level_name if level_name is not None else f"level_{level_idx}"
                            )
                            column_mapping[field] = new_col_name
                            continue
                    except (ValueError, IndexError):
                        pass

                    # 'index': use first unnamed level if any, else first level
                    if col_name == "index":
                        unnamed_levels = [i for i, name in enumerate(level_names) if name is None]
                        level_idx = unnamed_levels[0] if unnamed_levels else 0
                        df = df.reset_index(level=level_idx)
                        level_name = level_names[level_idx]
                        new_col_name = (
                            level_name if level_name is not None else f"level_{level_idx}"
                        )
                        column_mapping[field] = new_col_name
                        continue

                    # Named level
                    if col_name in level_names:
                        level_idx = level_names.index(col_name)
                        df = df.reset_index(level=level_idx)
                        continue

                else:
                    # Single index
                    if col_name == "index" or col_name == df.index.name:
                        idx_name = df.index.name
                        df = df.reset_index()
                        new_col_name = idx_name if idx_name is not None else "index"
                        column_mapping[field] = new_col_name
                        continue

        return df

    def _process_dataframe_input(
        self, data: Union[pd.DataFrame, pd.Series], column_mapping: Dict[str, str]
    ) -> List[Data]:
        """
        Process DataFrame or Series input into a list of Data objects.

        This method duplicates the logic from from_dataframe to handle
        DataFrame/Series input in the constructor. It validates the input
        data structure and converts it to the appropriate Data objects
        based on the series type.

        Args:
            data (Union[pd.DataFrame, pd.Series]): DataFrame or Series to process.
            column_mapping (Dict[str, str]): Mapping of required fields to column names.

        Returns:
            List[Data]: List of processed data objects suitable for the series type.

        Raises:
            ValueError: If required columns are missing from the DataFrame/Series.
            ValueError: If the data structure is invalid for the series type.
            ValueError: If time column is not found and no DatetimeIndex is available.

        Note:
            This method uses the data_class property to determine the appropriate
            Data class for conversion.
        """
        # Convert Series to DataFrame if needed (do this first)
        if isinstance(data, pd.Series):
            data = data.to_frame()

        data_class = self.data_class
        required = data_class.required_columns
        optional = data_class.optional_columns

        # Check if all required columns are mapped
        missing_required = required - set(column_mapping.keys())
        if missing_required:
            raise ValueError(f"DataFrame is missing required column mapping: {missing_required}")

        # Prepare index for all column mappings
        df = self.prepare_index(data, column_mapping)

        # Check if all required columns are present in the DataFrame
        mapped_columns = set(column_mapping.values())
        available_columns = set(df.columns.tolist())
        missing_columns = mapped_columns - available_columns

        if missing_columns:
            raise ValueError(f"DataFrame is missing required column: {missing_columns}")

        # Create data objects
        result = []
        for _, row in df.iterrows():
            kwargs = {}
            # Process both required and optional columns
            for key in required.union(optional):
                if key in column_mapping:
                    col_name = column_mapping[key]
                    if col_name in df.columns:
                        value = row[col_name]
                        kwargs[key] = value
            data_obj = data_class(**kwargs)
            result.append(data_obj)

        return result

    @property
    def data_dict(self) -> List[Dict[str, Any]]:
        """
        Get the data in dictionary format.

        Converts the series data to a list of dictionaries suitable for
        frontend serialization. Handles various data formats including
        dictionaries, lists of dictionaries, or lists of objects with
        asdict() methods.

        Returns:
            List[Dict[str, Any]]: List of data dictionaries ready for
                frontend consumption.

        Example:
            ```python
            # Get data as dictionaries
            data_dicts = series.data_dict

            # Access individual data points
            for data_point in data_dicts:
                print(f"Time: {data_point['time']}, Value: {data_point['value']}")
            ```
        """
        if isinstance(self.data, dict):
            return self.data
        if isinstance(self.data, list):
            if len(self.data) == 0:
                return self.data
            # If already list of dicts
            if isinstance(self.data[0], dict):
                return self.data
                # If list of objects with asdict
        if hasattr(self.data[0], "asdict"):
            return [item.asdict() for item in self.data]
        # Fallback: return as-is
        return self.data

    def set_visible(self, visible: bool) -> "Series":
        """
        Set series visibility.

        Shows or hides the series on the chart. This method provides a
        convenient way to control series visibility with method chaining support.

        Args:
            visible (bool): Whether the series should be visible on the chart.

        Returns:
            Series: Self for method chaining.

        Example:
            ```python
            # Hide the series
            series.set_visible(False)

            # Show the series
            series.set_visible(True)

            # Method chaining
            series.set_visible(False).add_marker(marker)
            ```
        """
        self.visible = visible
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

        Creates and adds a marker to the series for highlighting specific data points
        or events. Markers can be positioned above, below, or on the data point and
        support various shapes and colors.

        Args:
            time (Union[str, int, float, pd.Timestamp]): Time for the marker in various
                formats (timestamp, datetime string, or numeric).
            position (MarkerPosition): Position of the marker relative to the data point
                (e.g., above, below, on).
            color (str): Color of the marker in CSS color format (hex, rgb, named).
            shape (MarkerShape): Shape of the marker (circle, square, arrow, etc.).
            text (Optional[str], optional): Optional text to display with the marker.
                Defaults to None.
            size (Optional[int], optional): Optional size of the marker in pixels.
                Defaults to None.

        Returns:
            Series: Self for method chaining.

        Example:
            ```python
            from streamlit_lightweight_charts_pro.type_definitions import MarkerPosition
            from streamlit_lightweight_charts_pro.type_definitions.enums import MarkerShape

            # Add a simple marker
            series.add_marker(
                time="2024-01-01 10:00:00",
                position=MarkerPosition.ABOVE,
                color="red",
                shape=MarkerShape.CIRCLE
            )

            # Add a marker with text and size
            series.add_marker(
                time=1640995200,
                position=MarkerPosition.BELOW,
                color="#00ff00",
                shape=MarkerShape.ARROW_UP,
                text="Buy Signal",
                size=12
            )

            # Method chaining
            series.add_marker(marker1).add_marker(marker2)
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
        self._markers.append(marker)
        return self

    def add_markers(self, markers: List[Marker]) -> "Series":
        """
        Add multiple markers to this series.

        Adds a list of markers to the series. Returns self for method chaining.

        Args:
            markers: List of marker objects to add.

        Returns:
            Series: Self for method chaining.
        """
        self._markers.extend(markers)
        return self

    def clear_markers(self) -> "Series":
        """
        Clear all markers from this series.

        Removes all markers from the series. Returns self for method chaining.

        Returns:
            Series: Self for method chaining.
        """
        self._markers.clear()
        return self

    def add_price_line(self, price_line: PriceLineOptions) -> "Series":
        """
        Add a price line option to this series.

        Args:
            price_line (PriceLineOptions): The price line option to add.

        Returns:
            Series: Self for method chaining.
        """
        self._price_lines.append(price_line)
        return self

    def clear_price_lines(self) -> "Series":
        """
        Remove all price line options from this series.

        Returns:
            Series: Self for method chaining.
        """
        self._price_lines.clear()
        return self

    def _validate_pane_config(self) -> None:
        """
        Validate pane configuration for the series.

        This method ensures that pane_id is properly set.
        It should be called by subclasses in their asdict() method.

        Raises:
            ValueError: If pane_id is negative.
        """
        if self._pane_id is not None and self._pane_id < 0:
            raise ValueError("pane_id must be non-negative")
        if self._pane_id is None:
            self._pane_id = 0

    def update(self, updates: Dict[str, Any]) -> "Series":
        """
        Update series configuration with a dictionary of values.

        This method provides a flexible way to update series properties using a dictionary.
        It handles both simple properties and nested objects, automatically creating
        nested Options instances when needed.

        Args:
            updates: Dictionary of updates to apply. Keys can be in snake_case or camelCase.
                Values can be simple types or dictionaries for nested objects.

        Returns:
            Series: Self for method chaining.

        Raises:
            ValueError: If an update key doesn't correspond to a valid attribute.
            TypeError: If a value type is incompatible with the attribute type.

        Example:
            ```python
            series = LineSeries(data=data)

            # Update simple properties
            series.update({
                "visible": False,
                "price_scale_id": "left"
            })

            # Update nested options
            series.update({
                "line_options": {
                    "color": "#ff0000",
                    "line_width": 3
                }
            })

            # Method chaining
            series.update({"visible": True}).update({"pane_id": 1})
            ```
        """
        for key, value in updates.items():
            if value is None:
                continue  # Skip None values for method chaining

            # Convert camelCase to snake_case for attribute lookup
            attr_name = self._camel_to_snake(key)

            # Check if attribute exists
            if not hasattr(self, attr_name):
                # Try the original key in case it's already snake_case
                if hasattr(self, key):
                    attr_name = key
                else:
                    raise ValueError(f"Invalid series attribute: {key}")

            # Handle nested Options objects
            current_value = getattr(self, attr_name)
            if isinstance(value, dict) and hasattr(current_value, "update"):
                # Update existing Options object
                current_value.update(value)
            elif isinstance(value, dict) and current_value is None:
                # Create new Options object if current is None
                # This requires knowing the type, so we'll need to handle specific cases
                if attr_name.endswith("_options"):
                    # Try to create appropriate Options class
                    options_class_name = attr_name.replace("_", " ").title().replace(" ", "")
                    try:
                        # Use pre-imported options classes
                        options_classes = {
                            "line_options": LineOptions,
                            "price_format": PriceFormatOptions,
                        }
                        if attr_name in options_classes:
                            setattr(self, attr_name, options_classes[attr_name](**value))
                        else:
                            # Fallback to direct assignment
                            setattr(self, attr_name, value)
                    except (ImportError, TypeError):
                        # Fallback to direct assignment
                        setattr(self, attr_name, value)
                else:
                    setattr(self, attr_name, value)
            else:
                # Simple value assignment
                setattr(self, attr_name, value)

        return self

    def _camel_to_snake(self, camel_case: str) -> str:
        """
        Convert camelCase to snake_case.

        Args:
            camel_case: String in camelCase format.

        Returns:
            String in snake_case format.
        """
        import re  # pylint: disable=import-outside-toplevel

        return re.sub(r"(?<!^)(?=[A-Z])", "_", camel_case).lower()

    def asdict(self) -> Dict[str, Any]:
        """
        Convert series to dictionary representation.

        This method creates a dictionary representation of the series
        that can be consumed by the frontend React component.

        Returns:
            Dict[str, Any]: Dictionary containing series configuration for the frontend.
        """
        # Validate pane configuration
        self._validate_pane_config()

        # Get base configuration
        config = {
            "type": self.chart_type.value,
            "data": self.data_dict,
        }

        # Add options from attributes that have asdict() method
        options = {}
        for attr_name in dir(self):
            if attr_name.startswith("_"):
                continue
            # Skip data attribute as it's handled separately
            if attr_name == "data":
                continue
            # Skip class attributes (like DATA_CLASS)
            if attr_name.isupper():
                continue
            # Skip class properties (like data_class)
            if attr_name == "data_class":
                continue

            attr_value = getattr(self, attr_name)
            # Only process instance attributes, not classes
            if (
                hasattr(attr_value, "asdict")
                and callable(getattr(attr_value, "asdict"))
                and not isinstance(attr_value, type)
            ):
                # For any options object, flatten the options instead of nesting
                if attr_name.endswith("_options"):
                    options.update(attr_value.asdict())
                else:
                    # Convert snake_case to camelCase for the key
                    key = snake_to_camel(attr_name)
                    options[key] = attr_value.asdict()

            # Also include individual option attributes that are not None and not empty strings
            elif (
                not callable(attr_value)
                and not isinstance(attr_value, type)
                and attr_value is not None
                and attr_value != ""
                and attr_name
                not in [
                    "markers",
                    "price_lines",
                    "pane_id",
                    "visible",
                    "data_dict",
                    "chart_type",
                    "data_class",
                    "column_mapping",
                    "required_columns",
                    "optional_columns",
                ]
            ):
                # Convert snake_case to camelCase for the key
                key = snake_to_camel(attr_name)
                options[key] = attr_value

        if options:
            config["options"] = options

        # Add markers if present
        if self._markers:
            config["markers"] = [marker.asdict() for marker in self._markers]

        # Add price lines if present
        if self._price_lines:
            config["priceLines"] = [pl.asdict() for pl in self._price_lines]

        # Add pane_id
        config["pane_id"] = self._pane_id

        # Add visible property
        config["visible"] = self.visible

        # Add price_scale_id
        config["priceScaleId"] = self._price_scale_id

        return config

    @classproperty
    def data_class(cls) -> Type[Data]:  # pylint: disable=no-self-argument
        """
        Return the first DATA_CLASS found in the MRO (most-derived class wins).
        """
        for base in cls.__mro__:
            if hasattr(base, "DATA_CLASS"):
                return getattr(base, "DATA_CLASS")
        raise NotImplementedError("No DATA_CLASS defined in the class hierarchy.")

    @classmethod
    def from_dataframe(
        cls,
        df: Union[pd.DataFrame, pd.Series],
        column_mapping: Dict[str, str],
        price_scale_id: str = "right",
        **kwargs,
    ) -> "Series":
        """
        Create a Series instance from a pandas DataFrame or Series.

        Args:
            df (Union[pd.DataFrame, pd.Series]): The input DataFrame or Series.
            column_mapping (dict): Mapping of required fields
                (e.g., {'time': 'datetime', 'value': 'close', ...}).
            price_scale_id (str): Price scale ID (default 'right').
            **kwargs: Additional arguments for the Series constructor.

        Returns:
            Series: An instance of the Series (or subclass) with normalized data.

        Raises:
            NotImplementedError: If the subclass does not define DATA_CLASS.
            ValueError: If required columns are missing in column_mapping or DataFrame.
            AttributeError: If the data class does not define REQUIRED_COLUMNS.
        """
        # Convert Series to DataFrame if needed
        if isinstance(df, pd.Series):
            df = df.to_frame()

        data_class = cls.data_class
        required = data_class.required_columns
        optional = data_class.optional_columns

        # Check required columns in column_mapping
        missing_mapping = [col for col in required if col not in column_mapping]
        if missing_mapping:
            raise ValueError(
                f"Missing required columns in column_mapping: {missing_mapping}\n"
                f"Required columns: {required}\n"
                f"Column mapping: {column_mapping}"
            )
        else:
            pass  # Removed print

        # Prepare index for all column mappings
        df = cls.prepare_index(df, column_mapping)

        # Check required columns in DataFrame (including index) - after processing
        for key in required:
            col = column_mapping[key]
            if col not in df.columns:
                raise ValueError(f"DataFrame is missing required column: {col}")
            else:
                pass  # Removed print

        # Build data objects
        data = []
        for i in range(len(df)):
            kwargs_data = {}
            for key in required.union(optional):
                if key in column_mapping:
                    col = column_mapping[key]
                    if col in df.columns:
                        value = df.iloc[i][col]
                        kwargs_data[key] = value
                    else:
                        raise ValueError(f"DataFrame is missing required column: {col}")
                else:
                    # Skip optional columns that are not in column_mapping
                    continue

            data.append(data_class(**kwargs_data))

        result = cls(data=data, price_scale_id=price_scale_id, **kwargs)
        return result
