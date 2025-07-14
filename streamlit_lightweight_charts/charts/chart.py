"""Chart classes for streamlit-lightweight-charts."""

from typing import List, Optional, Dict, Any, Union
from ..rendering import render_chart
from .options import ChartOptions
from .series import Series
from ..data import Annotation, AnnotationManager


class Chart:
    """Main chart class for creating single-pane charts."""
    
    def __init__(
        self,
        series: Union[Series, List[Series]],
        options: Optional[ChartOptions] = None,
        annotations: Optional[List[Annotation]] = None
    ):
        """
        Initialize a chart.
        
        Args:
            series: Single series or list of series to display
            options: Chart configuration options
            annotations: Optional list of annotations
        """
        self.series = series if isinstance(series, list) else [series]
        self.options = options or ChartOptions()
        self.annotation_manager = AnnotationManager()
        
        # Add annotations if provided
        if annotations:
            default_layer = self.annotation_manager.create_layer('default')
            for annotation in annotations:
                default_layer.add_annotation(annotation)
    
    def render(self, key: Optional[str] = None) -> Any:
        """
        Render the chart using Streamlit.
        
        Args:
            key: Unique key for the Streamlit component
            
        Returns:
            Rendered chart component
        """
        chart_data = {
            'chart': self.options.to_dict(),
            'series': [s.to_dict() for s in self.series],
            'annotations': [ann.to_dict() for ann in self.annotation_manager.get_all_annotations()]
        }
        return render_chart([chart_data], key=key)
    
    def add_series(self, series: Series) -> 'Chart':
        """
        Add a series to the chart.
        
        Args:
            series: Series to add
            
        Returns:
            Self for method chaining
        """
        self.series.append(series)
        return self
    
    def update_options(self, **kwargs) -> 'Chart':
        """
        Update chart options.
        
        Args:
            **kwargs: Options to update
            
        Returns:
            Self for method chaining
        """
        for key, value in kwargs.items():
            if hasattr(self.options, key):
                setattr(self.options, key, value)
        return self
    
    def add_annotation(self, annotation: Annotation, layer_name: str = 'default') -> 'Chart':
        """
        Add an annotation to the chart.
        
        Args:
            annotation: Annotation to add
            layer_name: Name of the layer to add to
            
        Returns:
            Self for method chaining
        """
        layer = self.annotation_manager.get_layer(layer_name)
        if layer is None:
            layer = self.annotation_manager.create_layer(layer_name)
        layer.add_annotation(annotation)
        return self
    
    def add_annotations(self, annotations: List[Annotation], layer_name: str = 'default') -> 'Chart':
        """
        Add multiple annotations to the chart.
        
        Args:
            annotations: List of annotations to add
            layer_name: Name of the layer to add to
            
        Returns:
            Self for method chaining
        """
        for annotation in annotations:
            self.add_annotation(annotation, layer_name)
        return self
    
    def create_annotation_layer(self, name: str) -> 'Chart':
        """
        Create a new annotation layer.
        
        Args:
            name: Name of the layer
            
        Returns:
            Self for method chaining
        """
        self.annotation_manager.create_layer(name)
        return self
    
    def hide_annotation_layer(self, name: str) -> 'Chart':
        """
        Hide an annotation layer.
        
        Args:
            name: Name of the layer to hide
            
        Returns:
            Self for method chaining
        """
        layer = self.annotation_manager.get_layer(name)
        if layer:
            layer.hide()
        return self
    
    def show_annotation_layer(self, name: str) -> 'Chart':
        """
        Show an annotation layer.
        
        Args:
            name: Name of the layer to show
            
        Returns:
            Self for method chaining
        """
        layer = self.annotation_manager.get_layer(name)
        if layer:
            layer.show()
        return self
    
    def clear_annotations(self, layer_name: Optional[str] = None) -> 'Chart':
        """
        Clear annotations from a layer or all layers.
        
        Args:
            layer_name: Name of the layer to clear, or None to clear all layers
            
        Returns:
            Self for method chaining
        """
        if layer_name:
            layer = self.annotation_manager.get_layer(layer_name)
            if layer:
                layer.clear_annotations()
        else:
            self.annotation_manager.clear_all_layers()
        return self


class MultiPaneChart:
    """Chart class for creating multi-pane charts."""
    
    def __init__(self, charts: Optional[List[Chart]] = None):
        """
        Initialize a multi-pane chart.
        
        Args:
            charts: List of charts to display in separate panes
        """
        self.charts = charts or []
    
    def add_pane(self, chart: Chart) -> 'MultiPaneChart':
        """
        Add a pane to the multi-pane chart.
        
        Args:
            chart: Chart to add as a new pane
            
        Returns:
            Self for method chaining
        """
        self.charts.append(chart)
        return self
    
    def render(self, key: Optional[str] = None) -> Any:
        """
        Render the multi-pane chart using Streamlit.
        
        Args:
            key: Unique key for the Streamlit component
            
        Returns:
            Rendered chart component
        """
        charts_data = []
        for chart in self.charts:
            charts_data.append({
                'chart': chart.options.to_dict(),
                'series': [s.to_dict() for s in chart.series]
            })
        return render_chart(charts_data, key=key)