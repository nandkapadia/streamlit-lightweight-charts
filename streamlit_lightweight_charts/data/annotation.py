"""Annotation system for charts."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

import pandas as pd

from .base import from_utc_timestamp, to_utc_timestamp


class AnnotationType(str, Enum):
    """Annotation type enumeration."""

    TEXT = "text"
    ARROW = "arrow"
    SHAPE = "shape"
    LINE = "line"
    RECTANGLE = "rectangle"
    CIRCLE = "circle"


class AnnotationPosition(str, Enum):
    """Annotation position enumeration."""

    ABOVE = "above"
    BELOW = "below"
    INLINE = "inline"


@dataclass
class Annotation:
    """
    Represents a chart annotation.

    Attributes:
        time: Annotation time (accepts pd.Timestamp, datetime, or string)
        price: Price level for the annotation
        text: Annotation text
        annotation_type: Type of annotation
        position: Position of the annotation
        color: Annotation color
        background_color: Background color
        font_size: Font size
        font_weight: Font weight
        text_color: Text color
        border_color: Border color
        border_width: Border width
        opacity: Annotation opacity
        show_time: Whether to show time in annotation
        tooltip: Optional tooltip text
    """

    time: Union[pd.Timestamp, datetime, str, int, float]
    price: float
    text: str
    annotation_type: Union[AnnotationType, str] = AnnotationType.TEXT
    position: Union[AnnotationPosition, str] = AnnotationPosition.ABOVE
    color: str = "#2196F3"
    background_color: str = "rgba(255, 255, 255, 0.9)"
    font_size: int = 12
    font_weight: str = "normal"
    text_color: str = "#000000"
    border_color: str = "#CCCCCC"
    border_width: int = 1
    opacity: float = 1.0
    show_time: bool = False
    tooltip: Optional[str] = None

    def __post_init__(self):
        """Validate and process annotation data."""
        # Convert time to UTC timestamp
        self._timestamp = to_utc_timestamp(self.time)

        # Convert enums if strings
        if isinstance(self.annotation_type, str):
            self.annotation_type = AnnotationType(self.annotation_type.lower())

        if isinstance(self.position, str):
            self.position = AnnotationPosition(self.position.lower())

        # Validate price
        if not isinstance(self.price, (int, float)):
            raise ValueError("Price must be a number")

        # Validate text
        if not self.text:
            raise ValueError("Annotation text cannot be empty")

        # Validate opacity
        if not 0 <= self.opacity <= 1:
            raise ValueError("Opacity must be between 0 and 1")

        # Validate font size
        if self.font_size <= 0:
            raise ValueError("Font size must be positive")

        # Validate border width
        if self.border_width < 0:
            raise ValueError("Border width must be non-negative")

    @property
    def timestamp(self) -> Union[int, str]:
        """Get time as UTC timestamp."""
        return self._timestamp

    @property
    def datetime(self) -> pd.Timestamp:
        """Get time as pandas Timestamp."""
        return from_utc_timestamp(self._timestamp)

    def to_dict(self) -> Dict[str, Any]:
        """Convert annotation to dictionary for serialization."""
        return {
            "time": self.timestamp,
            "price": self.price,
            "text": self.text,
            "type": self.annotation_type.value,
            "position": self.position.value,
            "color": self.color,
            "background_color": self.background_color,
            "font_size": self.font_size,
            "font_weight": self.font_weight,
            "text_color": self.text_color,
            "border_color": self.border_color,
            "border_width": self.border_width,
            "opacity": self.opacity,
            "show_time": self.show_time,
            "tooltip": self.tooltip,
        }


@dataclass
class AnnotationLayer:
    """
    Manages a layer of annotations for a chart.

    This allows grouping annotations and applying bulk operations.
    """

    name: str
    annotations: List[Annotation]
    visible: bool = True
    opacity: float = 1.0

    def __post_init__(self):
        """Validate annotation layer."""
        if not self.name:
            raise ValueError("Layer name cannot be empty")

        if not 0 <= self.opacity <= 1:
            raise ValueError("Opacity must be between 0 and 1")

    def add_annotation(self, annotation: Annotation) -> "AnnotationLayer":
        """Add annotation to layer."""
        self.annotations.append(annotation)
        return self

    def remove_annotation(self, index: int) -> "AnnotationLayer":
        """Remove annotation by index."""
        if 0 <= index < len(self.annotations):
            self.annotations.pop(index)
        return self

    def clear_annotations(self) -> "AnnotationLayer":
        """Clear all annotations from layer."""
        self.annotations.clear()
        return self

    def hide(self) -> "AnnotationLayer":
        """Hide the layer."""
        self.visible = False
        return self

    def show(self) -> "AnnotationLayer":
        """Show the layer."""
        self.visible = True
        return self

    def set_opacity(self, opacity: float) -> "AnnotationLayer":
        """Set layer opacity."""
        if not 0 <= opacity <= 1:
            raise ValueError("Opacity must be between 0 and 1")
        self.opacity = opacity
        return self

    def filter_by_time_range(
        self,
        start_time: Union[pd.Timestamp, datetime, str, int, float],
        end_time: Union[pd.Timestamp, datetime, str, int, float],
    ) -> List[Annotation]:
        """Filter annotations by time range."""
        start_ts = to_utc_timestamp(start_time)
        end_ts = to_utc_timestamp(end_time)

        return [
            annotation
            for annotation in self.annotations
            if start_ts <= annotation.timestamp <= end_ts
        ]

    def filter_by_price_range(self, min_price: float, max_price: float) -> List[Annotation]:
        """Filter annotations by price range."""
        return [
            annotation
            for annotation in self.annotations
            if min_price <= annotation.price <= max_price
        ]

    def to_dict(self) -> Dict[str, Any]:
        """Convert layer to dictionary for serialization."""
        return {
            "name": self.name,
            "visible": self.visible,
            "opacity": self.opacity,
            "annotations": [annotation.to_dict() for annotation in self.annotations],
        }


class AnnotationManager:
    """
    Manages multiple annotation layers for a chart.
    """

    def __init__(self):
        self.layers: Dict[str, AnnotationLayer] = {}

    def create_layer(self, name: str) -> AnnotationLayer:
        """Create a new annotation layer."""
        layer = AnnotationLayer(name=name, annotations=[])
        self.layers[name] = layer
        return layer

    def get_layer(self, name: str) -> Optional[AnnotationLayer]:
        """Get annotation layer by name."""
        return self.layers.get(name)

    def remove_layer(self, name: str) -> bool:
        """Remove annotation layer by name."""
        if name in self.layers:
            del self.layers[name]
            return True
        return False

    def clear_all_layers(self) -> None:
        """Clear all annotation layers."""
        self.layers.clear()

    def get_all_annotations(self) -> List[Annotation]:
        """Get all annotations from all visible layers."""
        all_annotations = []
        for layer in self.layers.values():
            if layer.visible:
                all_annotations.extend(layer.annotations)
        return all_annotations

    def hide_all_layers(self) -> None:
        """Hide all annotation layers."""
        for layer in self.layers.values():
            layer.hide()

    def show_all_layers(self) -> None:
        """Show all annotation layers."""
        for layer in self.layers.values():
            layer.show()

    def to_dict(self) -> Dict[str, Any]:
        """Convert manager to dictionary for serialization."""
        return {"layers": {name: layer.to_dict() for name, layer in self.layers.items()}}


# Factory functions for common annotation types
def create_text_annotation(
    time: Union[pd.Timestamp, datetime, str, int, float],
    price: float,
    text: str,
    **kwargs,
) -> Annotation:
    """Create a text annotation."""
    return Annotation(
        time=time, price=price, text=text, annotation_type=AnnotationType.TEXT, **kwargs
    )


def create_arrow_annotation(
    time: Union[pd.Timestamp, datetime, str, int, float],
    price: float,
    text: str,
    **kwargs,
) -> Annotation:
    """Create an arrow annotation."""
    return Annotation(
        time=time,
        price=price,
        text=text,
        annotation_type=AnnotationType.ARROW,
        **kwargs,
    )


def create_shape_annotation(
    time: Union[pd.Timestamp, datetime, str, int, float],
    price: float,
    text: str,
    **kwargs,
) -> Annotation:
    """Create a shape annotation."""
    return Annotation(
        time=time,
        price=price,
        text=text,
        annotation_type=AnnotationType.SHAPE,
        **kwargs,
    )
