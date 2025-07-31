"""
Base options class for streamlit-lightweight-charts.

This module provides the base Options class that all option classes should inherit from.
It provides common functionality for serialization, validation, and frontend communication
through standardized dictionary conversion with camelCase key formatting.
"""

from abc import ABC
from dataclasses import dataclass, fields
from enum import Enum
from typing import Any, Dict

from streamlit_lightweight_charts_pro.logging_config import get_logger
from streamlit_lightweight_charts_pro.utils.data_utils import snake_to_camel

# Initialize logger
logger = get_logger(__name__)


@dataclass
class Options(ABC):
    """
    Abstract base class for all option classes.

    This class provides common functionality for option classes including automatic
    camelCase key conversion for frontend serialization, enum value conversion,
    and standardized validation patterns. All option classes in the library should
    inherit from this base class to ensure consistent behavior.

    The class implements a sophisticated serialization system that handles:
    - Automatic snake_case to camelCase key conversion
    - Enum value extraction and conversion
    - Nested option object serialization
    - List serialization with recursive option handling
    - Special handling for _options fields with flattening logic

    Attributes:
        Inherited by subclasses with specific option attributes.

    Example:
        ```python
        @dataclass
        class MyOptions(Options):
            background_color: str = "#ffffff"
            text_color: str = "#000000"
            is_visible: bool = True

        options = MyOptions()
        result = options.asdict()
        # Returns: {"backgroundColor": "#ffffff", "textColor": "#000000", "isVisible": True}
        ```
    """

    def update(self, updates: Dict[str, Any]) -> "Options":
        """
        Update options with a dictionary of values.

        This method provides a flexible way to update option properties using a dictionary.
        It handles both simple properties and nested objects, automatically creating
        nested Options instances when needed.

        Args:
            updates: Dictionary of updates to apply. Keys can be in snake_case or camelCase.
                Values can be simple types or dictionaries for nested objects.

        Returns:
            Options: Self for method chaining.

        Raises:
            ValueError: If an update key doesn't correspond to a valid field.
            TypeError: If a value type is incompatible with the field type.

        Example:
            ```python
            options = MyOptions()

            # Update simple properties
            options.update({
                "background_color": "#ff0000",
                "is_visible": False
            })

            # Update nested objects
            options.update({
                "line_options": {
                    "color": "#00ff00",
                    "line_width": 3
                }
            })

            # Method chaining
            options.update({"color": "red"}).update({"width": 100})
            ```
        """
        for key, value in updates.items():
            if value is None:
                continue  # Skip None values for method chaining

            # Convert camelCase to snake_case for field lookup
            field_name = self._camel_to_snake(key)

            # Check if field exists
            if not hasattr(self, field_name):
                # Try the original key in case it's already snake_case
                if hasattr(self, key):
                    field_name = key
                else:
                    # Ignore invalid fields instead of raising an error
                    logger.debug("Ignoring invalid option field: %s", key)
                    continue

            # Get field info for type checking
            field_info = None
            for field in fields(self):
                if field.name == field_name:
                    field_info = field
                    break

            if field_info is None:
                # Ignore fields not found in dataclass fields
                logger.debug(
                    "Ignoring field %s not found in %s", field_name, self.__class__.__name__
                )
                continue

            # Handle nested Options objects
            if isinstance(value, dict) and hasattr(field_info.type, "__origin__"):
                # Check if field type is a nested Options class
                field_type = field_info.type
                if hasattr(field_type, "__origin__") and field_type.__origin__ is not None:
                    # Handle Optional[Options] or similar
                    if hasattr(field_type, "__args__"):
                        for arg in field_type.__args__:
                            if isinstance(arg, type) and issubclass(arg, Options):
                                # Create new instance of nested Options
                                current_value = getattr(self, field_name)
                                if current_value is None:
                                    current_value = arg()
                                current_value.update(value)
                                setattr(self, field_name, current_value)
                                break
                        else:
                            # Not a nested Options, set directly
                            setattr(self, field_name, value)
                else:
                    # Direct Options type
                    current_value = getattr(self, field_name)
                    if current_value is None:
                        # Create new instance
                        setattr(self, field_name, field_type(**value))
                    else:
                        # Update existing instance
                        current_value.update(value)
            else:
                # Simple value assignment
                setattr(self, field_name, value)

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
        Convert options to dictionary with camelCase keys for frontend.

        This method provides comprehensive serialization of option objects for
        frontend communication. It handles complex nested structures, enum values,
        and special field flattening patterns.

        The serialization process:
        1. Iterates through all dataclass fields
        2. Skips None values, empty strings, and empty dictionaries
        3. Converts enum values to their .value property
        4. Recursively serializes nested Options objects
        5. Handles lists of Options objects
        6. Converts field names from snake_case to camelCase
        7. Applies special flattening logic for _options fields

        Returns:
            Dict[str, Any]: Dictionary with camelCase keys ready for frontend
                consumption. All nested structures are properly serialized and
                enum values are converted to their primitive representations.

        Note:
            - Empty dictionaries and None values are omitted from output
            - Enum values are automatically converted to their .value property
            - Nested Options objects are recursively serialized
            - Lists containing Options objects are handled recursively
            - background_options fields are flattened into the parent result
        """
        result = {}
        for f in fields(self):
            name = f.name
            value = getattr(self, name)

            # Skip None values, empty strings, and empty dictionaries
            if value is None or value == "" or value == {}:
                continue

            # Convert enum values to their .value property
            if isinstance(value, Enum):
                value = value.value
            elif (
                hasattr(value, "value")
                and hasattr(value, "__class__")
                and hasattr(value.__class__, "__bases__")
            ):
                # Check if it's an enum-like object
                for base in value.__class__.__bases__:
                    if hasattr(base, "__name__") and "Enum" in base.__name__:
                        value = value.value
                        break

            # Handle nested Options objects
            if isinstance(value, Options):
                value = value.asdict()
            elif isinstance(value, list):
                # Handle lists of Options objects
                value = [item.asdict() if isinstance(item, Options) else item for item in value]
            elif isinstance(value, dict):
                # Handle dictionaries of Options objects
                # Only convert if any value is an Options object
                if any(isinstance(v, Options) for v in value.values()):
                    value = {
                        str(k): (v.asdict() if isinstance(v, Options) else v) 
                        for k, v in value.items()
                    }
            # Convert to camelCase key
            key = snake_to_camel(name)

            # Special handling for fields ending in _options: flatten them
            if name.endswith("_options") and isinstance(value, dict):
                # Only flatten specific fields that should be flattened
                if name == "background_options":
                    # Merge the nested options into the parent result
                    result.update(value)
                else:
                    # For other _options fields, keep them nested but with camelCase key
                    result[key] = value
            else:
                result[key] = value

        return result
