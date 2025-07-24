"""
Color-related classes for streamlit-lightweight-charts.

This module provides classes for representing colors in charts, including
solid colors and gradient effects. It supports both simple color strings
and complex gradient configurations for enhanced visual appeal.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from streamlit_lightweight_charts_pro.type_definitions.enums import ColorType


@dataclass
class Color:
    """
    Base class for color representations.

    This abstract base class defines the interface for all color types
    in the library. It provides a common to_dict() method for serialization.

    All color implementations should inherit from this class and implement
    the to_dict() method to provide frontend-compatible color representations.
    """

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert color to dictionary representation.

        This method should be implemented by subclasses to provide
        a dictionary representation suitable for frontend consumption.

        Returns:
            Dictionary containing the color configuration.

        Raises:
            NotImplementedError: This method must be implemented by subclasses.
        """
        raise NotImplementedError


@dataclass
class SolidColor(Color):
    """
    Solid color representation.

    Represents a uniform color that can be applied to chart elements.
    Supports any valid CSS color format including hex codes, RGB values,
    and named colors.

    Attributes:
        color: Color string in any valid CSS format (hex, rgb, named, etc.).
        type: Color type, automatically set to SOLID.

    Example:
        ```python
        # Hex color
        red_color = SolidColor(color="#FF0000")

        # Named color
        blue_color = SolidColor(color="blue")

        # RGB color
        green_color = SolidColor(color="rgb(0, 255, 0)")
        ```
    """

    color: str
    type: ColorType = field(default=ColorType.SOLID, init=False)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert solid color to dictionary representation.

        Returns:
            Dictionary containing the color type and color value.
        """
        return {"type": self.type.value, "color": self.color}


@dataclass
class VerticalGradientColor(Color):
    """
    Vertical gradient color representation.

    Represents a vertical gradient that transitions from a top color
    to a bottom color. Useful for creating visually appealing backgrounds
    and filled areas.

    Attributes:
        top_color: Color at the top of the gradient.
        bottom_color: Color at the bottom of the gradient.
        type: Color type, automatically set to VERTICAL_GRADIENT.

    Example:
        ```python
        # Blue to white gradient
        gradient = VerticalGradientColor(
            top_color="#0066CC",
            bottom_color="#FFFFFF"
        )

        # Red to transparent gradient
        fade_gradient = VerticalGradientColor(
            top_color="rgba(255, 0, 0, 1)",
            bottom_color="rgba(255, 0, 0, 0)"
        )
        ```
    """

    top_color: str
    bottom_color: str
    type: ColorType = field(default=ColorType.VERTICAL_GRADIENT, init=False)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert gradient color to dictionary representation.

        Returns:
            Dictionary containing the color type, top color, and bottom color.
        """
        return {
            "type": self.type.value,
            "topColor": self.top_color,
            "bottomColor": self.bottom_color,
        }


class Background:
    """
    Background color that can be either solid or gradient.

    This class provides a convenient interface for creating background
    colors with factory methods for common use cases. It supports both
    solid colors and vertical gradients.

    Attributes:
        color: The underlying Color object (SolidColor or VerticalGradientColor).

    Example:
        ```python
        # Solid white background
        bg = Background.solid("#FFFFFF")

        # Gradient background
        bg = Background.gradient("#0066CC", "#FFFFFF")

        # Custom color object
        custom_color = SolidColor(color="#F0F0F0")
        bg = Background(color=custom_color)
        ```
    """

    def __init__(self, color: Optional[Color] = None):
        """
        Initialize background with a color.

        Args:
            color: Color object to use for the background. If None,
                defaults to solid white color.
        """
        self.color = color or SolidColor(color="#FFFFFF")

    @classmethod
    def solid(cls, color: str) -> "Background":
        """
        Create a solid background.

        Factory method for creating a background with a solid color.

        Args:
            color: Color string in any valid CSS format.

        Returns:
            Background instance with solid color.

        Example:
            ```python
            bg = Background.solid("#F5F5F5")
            ```
        """
        return cls(SolidColor(color=color))

    @classmethod
    def gradient(cls, top_color: str, bottom_color: str) -> "Background":
        """
        Create a gradient background.

        Factory method for creating a background with a vertical gradient.

        Args:
            top_color: Color at the top of the gradient.
            bottom_color: Color at the bottom of the gradient.

        Returns:
            Background instance with gradient color.

        Example:
            ```python
            bg = Background.gradient("#0066CC", "#FFFFFF")
            ```
        """
        return cls(VerticalGradientColor(top_color=top_color, bottom_color=bottom_color))

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert background to dictionary representation.

        Returns:
            Dictionary containing the background color configuration.
        """
        # Fix: If self.color is a string, wrap it as SolidColor
        color = self.color
        if isinstance(color, str):
            color = SolidColor(color=color)
        return color.to_dict()
