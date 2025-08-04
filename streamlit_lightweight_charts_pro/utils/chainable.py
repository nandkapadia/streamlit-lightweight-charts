"""
Chainable decorators for enabling method chaining on properties and fields.

This module provides decorators that automatically create setter methods
for properties and dataclass fields, allowing both direct assignment and
method chaining styles with optional type validation.
"""

from typing import Any, Callable, Optional, Type, Union, get_args, get_origin

from .data_utils import (
    is_valid_color,
    validate_min_move,
    validate_precision,
    validate_price_format_type,
)


def _is_list_of_markers(value_type) -> bool:
    """Check if the type is List[MarkerBase] or similar."""
    if get_origin(value_type) is list:
        args = get_args(value_type)
        if args:
            arg_type = args[0]
            # Check if it's MarkerBase or a subclass
            try:
                from streamlit_lightweight_charts_pro.data.marker import MarkerBase

                return issubclass(arg_type, MarkerBase) if hasattr(arg_type, "__mro__") else False
            except ImportError:
                # If we can't import MarkerBase, check the name
                return hasattr(arg_type, "__name__") and "Marker" in arg_type.__name__


def _validate_list_of_markers(value, attr_name: str) -> bool:
    """Validate that a value is a list of markers."""
    if not isinstance(value, list):
        raise TypeError(f"{attr_name} must be a list")

    try:
        from streamlit_lightweight_charts_pro.data.marker import MarkerBase

        for item in value:
            if not isinstance(item, MarkerBase):
                raise TypeError(f"All items in {attr_name} must be instances of MarkerBase")
        return True
    except ImportError:
        # If we can't import MarkerBase, just check that all items have marker-like attributes
        for item in value:
            if not hasattr(item, "time") or not hasattr(item, "position"):
                raise TypeError(f"All items in {attr_name} must be valid markers")
        return True


def chainable_property(
    attr_name: str,
    value_type: Optional[Union[Type, tuple]] = None,
    validator: Optional[Union[Callable[[Any], Any], str]] = None,
    allow_none: bool = False,
    top_level: bool = False,
):
    """
    Decorator that creates both a property setter and a chaining method with optional validation.

    This allows both styles:
    - Property style: obj.attr = value
    - Method chaining: obj.set_attr(value).other_method()

    Args:
        attr_name: The name of the attribute to manage
        value_type: Optional type or tuple of types for validation
        validator: Optional validation function or string. If callable, takes a value and returns the validated value.
                  If string, uses built-in validators (e.g., "color" for color validation)
        allow_none: Whether to allow None values
        top_level: Whether this property should be output at the top level in asdict() instead of in options

    Returns:
        Decorator function that creates both property and method

    Example:
        ```python
        @chainable_property("color", str, validator="color")
        @chainable_property("width", int)
        @chainable_property("line_options", LineOptions,
                           allow_none=True)
        @chainable_property("base_value", validator=validate_base_value)
        @chainable_property("price_scale_id", top_level=True)
        class MySeries(Series):
            pass
        ```
    """

    def decorator(cls):
        # Create the setter method name
        setter_name = f"set_{attr_name}"

        # Create the chaining setter method with validation
        def setter_method(self, value):
            # Handle None values
            if value is None and allow_none:
                setattr(self, f"_{attr_name}", None)
                return self

            # Apply type validation if specified
            if value_type is not None:
                if value_type == bool:
                    # For boolean properties, convert truthy/falsy values to bool
                    value = bool(value)
                elif not isinstance(value, value_type):
                    # Create user-friendly error message
                    if value_type == str:
                        raise TypeError(f"{attr_name} must be a string")
                    elif value_type == int:
                        raise TypeError(f"{attr_name} must be an integer")
                    elif value_type == float:
                        raise TypeError(f"{attr_name} must be a number")
                    elif value_type == bool:
                        raise TypeError(f"{attr_name} must be a boolean")
                    elif hasattr(value_type, "__name__"):
                        # For complex types, use a more user-friendly message
                        if allow_none:
                            raise TypeError(
                                f"{attr_name} must be an instance of {value_type.__name__} or None"
                            )
                        else:
                            raise TypeError(
                                f"{attr_name} must be an instance of {value_type.__name__}"
                            )
                    elif isinstance(value_type, tuple):
                        # For tuple types like (int, float), create a user-friendly message
                        type_names = [
                            t.__name__ if hasattr(t, "__name__") else str(t) for t in value_type
                        ]
                        if len(type_names) == 2 and "int" in type_names and "float" in type_names:
                            raise TypeError(f"{attr_name} must be a number")
                        else:
                            raise TypeError(f"{attr_name} must be one of {', '.join(type_names)}")
                    else:
                        raise TypeError(
                            f"{attr_name} must be of type {value_type}, got {type(value)}"
                        )

            # Apply custom validation if specified
            if validator is not None:
                if isinstance(validator, str):
                    # Built-in validators
                    if validator == "color":
                        if not is_valid_color(value):
                            raise ValueError(
                                f"Invalid color format for {attr_name}: {value!r}. Must be hex or rgba."
                            )
                    elif validator == "price_format_type":
                        value = validate_price_format_type(value)
                    elif validator == "precision":
                        value = validate_precision(value)
                    elif validator == "min_move":
                        value = validate_min_move(value)
                    else:
                        raise ValueError(f"Unknown built-in validator: {validator}")
                else:
                    # Custom validator function
                    value = validator(value)

            setattr(self, f"_{attr_name}", value)
            return self

        # Create the property getter
        def property_getter(self):
            return getattr(self, f"_{attr_name}")

        # Create the property setter
        def property_setter(self, value):
            # Handle None values
            if value is None and allow_none:
                setattr(self, f"_{attr_name}", None)
                return

            # Apply type validation if specified
            if value_type is not None:
                if value_type == bool:
                    # For boolean properties, convert truthy/falsy values to bool
                    value = bool(value)
                elif _is_list_of_markers(value_type):
                    # Special handling for List[MarkerBase] and similar types
                    _validate_list_of_markers(value, attr_name)
                elif not isinstance(value, value_type):
                    # Create user-friendly error message
                    if value_type == str:
                        raise TypeError(f"{attr_name} must be a string")
                    elif value_type == int:
                        raise TypeError(f"{attr_name} must be an integer")
                    elif value_type == float:
                        raise TypeError(f"{attr_name} must be a number")
                    elif value_type == bool:
                        raise TypeError(f"{attr_name} must be a boolean")
                    elif hasattr(value_type, "__name__"):
                        # For complex types, use a more user-friendly message
                        if allow_none:
                            raise TypeError(
                                f"{attr_name} must be an instance of {value_type.__name__} or None"
                            )
                        else:
                            raise TypeError(
                                f"{attr_name} must be an instance of {value_type.__name__}"
                            )
                    elif isinstance(value_type, tuple):
                        # For tuple types like (int, float), create a user-friendly message
                        type_names = [
                            t.__name__ if hasattr(t, "__name__") else str(t) for t in value_type
                        ]
                        if len(type_names) == 2 and "int" in type_names and "float" in type_names:
                            raise TypeError(f"{attr_name} must be a number")
                        else:
                            raise TypeError(f"{attr_name} must be one of {', '.join(type_names)}")
                    else:
                        raise TypeError(
                            f"{attr_name} must be of type {value_type}, got {type(value)}"
                        )

            # Apply custom validation if specified
            if validator is not None:
                if isinstance(validator, str):
                    # Built-in validators
                    if validator == "color":
                        if not is_valid_color(value):
                            raise ValueError(
                                f"Invalid color format for {attr_name}: {value!r}. Must be hex or rgba."
                            )
                    elif validator == "price_format_type":
                        value = validate_price_format_type(value)
                    elif validator == "precision":
                        value = validate_precision(value)
                    elif validator == "min_move":
                        value = validate_min_move(value)
                    else:
                        raise ValueError(f"Unknown built-in validator: {validator}")
                else:
                    # Custom validator function
                    value = validator(value)

            setattr(self, f"_{attr_name}", value)

        # Create the property
        prop = property(property_getter, property_setter)

        # Add the property and method to the class
        setattr(cls, attr_name, prop)
        setattr(cls, setter_name, setter_method)

        # Store metadata about serialization
        if not hasattr(cls, "_chainable_properties"):
            cls._chainable_properties = {}

        cls._chainable_properties[attr_name] = {
            "allow_none": allow_none,
            "value_type": value_type,
            "top_level": top_level,
        }

        return cls

    return decorator


def chainable_field(
    field_name: str,
    value_type: Optional[Union[Type, tuple]] = None,
    validator: Optional[Union[Callable[[Any], Any], str]] = None,
):
    """
    Decorator that creates a setter method for dataclass fields with optional validation.

    This allows both styles:
    - Direct assignment: obj.field = value
    - Method chaining: obj.set_field(value).other_method()

    Args:
        field_name: The name of the dataclass field
        value_type: Optional type or tuple of types for validation
        validator: Optional validation function or string. If callable, takes a value and returns the validated value.
                  If string, uses built-in validators (e.g., "color" for color validation)

    Returns:
        Decorator function that creates a setter method

    Example:
        ```python
        @dataclass
        @chainable_field("color", str)
        @chainable_field("width", int)
        @chainable_field("line_options", LineOptions)
        class MyOptions(Options):
            pass
        ```
    """

    def decorator(cls):
        # Create the setter method name
        setter_name = f"set_{field_name}"

        # Create the chaining setter method with validation
        def setter_method(self, value):
            # Apply type validation if specified
            if value_type is not None:
                if _is_list_of_markers(value_type):
                    # Special handling for List[MarkerBase] and similar types
                    _validate_list_of_markers(value, field_name)
                elif not isinstance(value, value_type):
                    raise TypeError(f"{field_name} must be of type {value_type}, got {type(value)}")

            # Apply custom validation if specified
            if validator is not None:
                if isinstance(validator, str):
                    # Built-in validators
                    if validator == "color":
                        if not is_valid_color(value):
                            raise ValueError(
                                f"Invalid color format for {field_name}: {value!r}. Must be hex or rgba."
                            )
                    elif validator == "price_format_type":
                        value = validate_price_format_type(value)
                    elif validator == "precision":
                        value = validate_precision(value)
                    elif validator == "min_move":
                        value = validate_min_move(value)
                    else:
                        raise ValueError(f"Unknown built-in validator: {validator}")
                else:
                    # Custom validator function
                    value = validator(value)

            setattr(self, field_name, value)
            return self

        # Add the method to the class
        setattr(cls, setter_name, setter_method)

        return cls

    return decorator
