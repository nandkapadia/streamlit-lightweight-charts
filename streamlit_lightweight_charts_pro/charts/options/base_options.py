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

from streamlit_lightweight_charts_pro.utils.data_utils import snake_to_camel


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
        result = options.to_dict()
        # Returns: {"backgroundColor": "#ffffff", "textColor": "#000000", "isVisible": True}
        ```
    """

    def to_dict(self) -> Dict[str, Any]:
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
                value = value.to_dict()
            elif isinstance(value, list):
                # Handle lists of Options objects
                value = [item.to_dict() if isinstance(item, Options) else item for item in value]

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

    def __post_init__(self):
        """
        Post-initialization processing.

        Subclasses can override this method to add custom validation and processing
        after the dataclass is initialized. This is the recommended place to add
        type validation, value normalization, and other initialization logic.

        Example:
            ```python
            def __post_init__(self):
                super().__post_init__()
                if self.width < 0:
                    raise ValueError("Width must be non-negative")
            ```
        """
