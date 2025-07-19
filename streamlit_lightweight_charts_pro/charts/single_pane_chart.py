"""
Single pane chart implementation for streamlit-lightweight-charts.

This module provides the SinglePaneChart class, which is the primary chart
type for displaying financial data in a single pane. It supports multiple
series types, annotations, and comprehensive customization options.

The SinglePaneChart class extends BaseChart and provides a complete
implementation for rendering interactive financial charts with method
chaining support for fluent API usage.

Example:
    ```python
    from streamlit_lightweight_charts_pro import SinglePaneChart, LineSeries
    from streamlit_lightweight_charts_pro.data import SingleValueData
    
    # Create data
    data = [SingleValueData("2024-01-01", 100), SingleValueData("2024-01-02", 105)]
    
    # Create chart with method chaining
    chart = (SinglePaneChart(series=LineSeries(data))
             .update_options(height=400)
             .add_annotation(create_text_annotation("2024-01-01", 100, "Start")))
    
    # Render in Streamlit
    chart.render(key="my_chart")
    ```
"""

from typing import Any, Dict, List, Optional, Union

from .base_chart import BaseChart
from .options import ChartOptions
from .series import Series
from ..data.annotation import Annotation, AnnotationManager


class SinglePaneChart(BaseChart):
    """
    Single pane chart for displaying financial data.
    
    This class represents a single pane chart that can display multiple
    series of financial data. It supports various chart types including
    candlestick, line, area, bar, and histogram series. The chart
    includes comprehensive annotation support and method chaining for
    fluent API usage.
    
    Attributes:
        series: List of series objects to display in the chart
        options: Chart configuration options including layout, grid, etc.
        annotation_manager: Manager for chart annotations and layers
        
    Example:
        ```python
        # Basic usage
        chart = SinglePaneChart(series=LineSeries(data))
        
        # With method chaining
        chart = (SinglePaneChart(series=LineSeries(data))
                 .update_options(height=400)
                 .add_annotation(text_annotation))
        ```
    """

    def __init__(
        self,
        series: Union[Series, List[Series]],
        options: Optional[ChartOptions] = None,
        annotations: Optional[List[Annotation]] = None,
    ):
        """
        Initialize a single pane chart.
        
        Args:
            series: Single series object or list of series objects to display.
                Each series represents a different data visualization (line,
                candlestick, area, etc.).
            options: Optional chart configuration options. If not provided,
                default options will be used.
            annotations: Optional list of annotations to add to the chart.
                Annotations can include text, arrows, shapes, etc.
                
        Example:
            ```python
            # Single series
            chart = SinglePaneChart(series=LineSeries(data))
            
            # Multiple series
            chart = SinglePaneChart(series=[line_series, candlestick_series])
            
            # With options and annotations
            chart = SinglePaneChart(
                series=line_series,
                options=ChartOptions(height=500),
                annotations=[text_annotation]
            )
            ```
        """
        # Convert single series to list for consistent handling
        if isinstance(series, Series):
            self.series = [series]
        else:
            self.series = series

        # Use provided options or create default ones
        self.options = options or ChartOptions()
        
        # Initialize annotation manager
        self.annotation_manager = AnnotationManager()
        
        # Add initial annotations if provided
        if annotations:
            # Create default layer and add all annotations to it
            default_layer = self.annotation_manager.create_layer("default")
            for annotation in annotations:
                default_layer.add_annotation(annotation)

    def add_series(self, series: Series) -> "SinglePaneChart":
        """
        Add a series to the chart.
        
        This method adds a new series to the chart and returns self for
        method chaining. The series will be displayed in the chart according
        to its type and configuration.
        
        Args:
            series: Series object to add to the chart.
                
        Returns:
            SinglePaneChart: Self for method chaining.
            
        Example:
            ```python
            chart = SinglePaneChart(series=price_series)
            chart.add_series(volume_series).add_series(macd_series)
            ```
        """
        self.series.append(series)
        return self

    def update_options(self, **kwargs) -> "SinglePaneChart":
        """
        Update chart options using keyword arguments.
        
        This method allows updating chart options dynamically. Only valid
        option attributes will be updated. Returns self for method chaining.
        
        Args:
            **kwargs: Options to update. Valid options include any attribute
                of ChartOptions (height, width, layout, grid, etc.).
                
        Returns:
            SinglePaneChart: Self for method chaining.
            
        Example:
            ```python
            chart.update_options(height=600, width=800)
            ```
        """
        for key, value in kwargs.items():
            if hasattr(self.options, key):
                setattr(self.options, key, value)
        return self

    def add_annotation(
        self, annotation: Annotation, layer_name: str = "default"
    ) -> "SinglePaneChart":
        """
        Add an annotation to the chart.
        
        This method adds a single annotation to a specified layer. If the layer
        doesn't exist, it will be created automatically. Returns self for
        method chaining.
        
        Args:
            annotation: Annotation object to add to the chart.
            layer_name: Name of the layer to add the annotation to.
                If the layer doesn't exist, it will be created.
                
        Returns:
            SinglePaneChart: Self for method chaining.
            
        Example:
            ```python
            text_ann = create_text_annotation("2024-01-01", 100, "Important event")
            chart.add_annotation(text_ann, layer_name="events")
            ```
        """
        layer = self.annotation_manager.get_layer(layer_name)
        if layer is None:
            layer = self.annotation_manager.create_layer(layer_name)
        layer.add_annotation(annotation)
        return self

    def add_annotations(
        self, annotations: List[Annotation], layer_name: str = "default"
    ) -> "SinglePaneChart":
        """
        Add multiple annotations to the chart.
        
        This method adds multiple annotations to a specified layer, creating
        the layer if it doesn't exist. Returns self for method chaining.
        
        Args:
            annotations: List of annotation objects to add to the chart.
            layer_name: Name of the layer to add the annotations to.
                If the layer doesn't exist, it will be created.
                
        Returns:
            SinglePaneChart: Self for method chaining.
            
        Example:
            ```python
            annotations = [
                create_text_annotation("2024-01-01", 100, "Event 1"),
                create_arrow_annotation("2024-01-02", 105, "Event 2")
            ]
            chart.add_annotations(annotations, layer_name="events")
            ```
        """
        for annotation in annotations:
            self.add_annotation(annotation, layer_name)
        return self

    def create_annotation_layer(self, name: str) -> "SinglePaneChart":
        """
        Create a new annotation layer.
        
        This method creates a new empty annotation layer that can be used
        to organize annotations into groups. Returns self for method chaining.
        
        Args:
            name: Name of the layer to create.
                
        Returns:
            SinglePaneChart: Self for method chaining.
            
        Example:
            ```python
            chart.create_annotation_layer("technical_analysis")
            ```
        """
        self.annotation_manager.create_layer(name)
        return self

    def hide_annotation_layer(self, name: str) -> "SinglePaneChart":
        """
        Hide an annotation layer.
        
        This method hides a specific annotation layer, making all its
        annotations invisible. Returns self for method chaining.
        
        Args:
            name: Name of the layer to hide.
                
        Returns:
            SinglePaneChart: Self for method chaining.
            
        Example:
            ```python
            chart.hide_annotation_layer("events")
            ```
        """
        layer = self.annotation_manager.get_layer(name)
        if layer:
            layer.hide()
        return self

    def show_annotation_layer(self, name: str) -> "SinglePaneChart":
        """
        Show an annotation layer.
        
        This method shows a previously hidden annotation layer, making
        all its annotations visible again. Returns self for method chaining.
        
        Args:
            name: Name of the layer to show.
                
        Returns:
            SinglePaneChart: Self for method chaining.
            
        Example:
            ```python
            chart.show_annotation_layer("events")
            ```
        """
        layer = self.annotation_manager.get_layer(name)
        if layer:
            layer.show()
        return self

    def clear_annotations(self, layer_name: Optional[str] = None) -> "SinglePaneChart":
        """
        Clear annotations from a layer or all layers.
        
        This method removes all annotations from a specific layer or from
        all layers if no layer name is specified. Returns self for method chaining.
        
        Args:
            layer_name: Name of the layer to clear. If None, clears all layers.
                
        Returns:
            SinglePaneChart: Self for method chaining.
            
        Example:
            ```python
            # Clear specific layer
            chart.clear_annotations("events")
            
            # Clear all annotations
            chart.clear_annotations()
            ```
        """
        if layer_name:
            layer = self.annotation_manager.get_layer(layer_name)
            if layer:
                layer.clear_annotations()
        else:
            self.annotation_manager.clear_all_layers()
        return self

    def to_frontend_config(self) -> Dict[str, Any]:
        """
        Convert chart to frontend-compatible configuration.
        
        This method converts the chart object into a dictionary format that
        can be consumed by the frontend React component. It includes chart
        options, series data, and annotations.
        
        Returns:
            Dict[str, Any]: Dictionary containing chart configuration for the
                frontend, including chart options, series data, and annotations.
                
        Example:
            ```python
            config = chart.to_frontend_config()
            # Returns: {
            #     "chartId": "chart-123",
            #     "chart": {...},
            #     "series": [...],
            #     "annotations": [...]
            # }
            ```
        """
        # Convert annotation layers to frontend format
        annotation_layers = []
        for layer_name, layer in self.annotation_manager.layers.items():
            annotation_layers.append(
                {
                    "name": layer_name,
                    "annotations": [ann.to_dict() for ann in layer.annotations],
                    "visible": layer.visible,
                    "opacity": layer.opacity,
                }
            )

        return {
            "chartId": f"chart-{id(self)}",  # Unique chart identifier
            "chart": self.options.to_dict(),
            "series": [s.to_frontend_config() for s in self.series],
            "annotations": annotation_layers,
        }
