"""
Chart classes for streamlit-lightweight-charts.

This module provides the core chart classes for creating single-pane and multi-pane charts.
It includes the base Chart class for single-pane charts and MultiPaneChart for creating
synchronized multi-pane charts similar to TradingView.

The Chart class supports multiple series, annotations, and comprehensive configuration
options, while MultiPaneChart enables creating professional trading dashboards with
synchronized crosshairs and time ranges.
"""

from typing import Any, Dict, List, Optional, Union

from ..data import Annotation, AnnotationManager
from .options import ChartOptions
from .series import Series


class Chart:
    """
    Main chart class for creating single-pane charts.

    This class represents a single chart pane that can contain multiple series,
    annotations, and configuration options. It provides a fluent interface for
    building charts and supports both rendering and configuration export.

    Attributes:
        series: List of series objects to display in the chart.
        options: Chart configuration options including layout, grid, and styling.
        annotation_manager: Manager for handling chart annotations and layers.
    """

    def __init__(
        self,
        series: Union[Series, List[Series]],
        options: Optional[ChartOptions] = None,
        annotations: Optional[List[Annotation]] = None,
    ):
        """
        Initialize a chart with series and optional configuration.

        Args:
            series: Single series or list of series to display in the chart.
                Can be any series type (LineSeries, CandlestickSeries, etc.).
            options: Chart configuration options. If None, default options will be used.
            annotations: Optional list of annotations to add to the chart.
                These will be added to a default layer named "default".

        Example:
            ```python
            # Create a chart with a single series
            line_series = LineSeries(data=line_data)
            chart = Chart(series=line_series)

            # Create a chart with multiple series
            chart = Chart(series=[price_series, volume_series])

            # Create a chart with custom options and annotations
            chart = Chart(
                series=candlestick_series,
                options=ChartOptions(height=500),
                annotations=[text_annotation]
            )
            ```
        """
        # Normalize series to list for consistent handling
        self.series = series if isinstance(series, list) else [series]
        self.options = options or ChartOptions()
        self.annotation_manager = AnnotationManager()

        # Add annotations if provided during initialization
        if annotations:
            default_layer = self.annotation_manager.create_layer("default")
            for annotation in annotations:
                default_layer.add_annotation(annotation)

    def render(self, key: Optional[str] = None) -> Any:
        """
        Render the chart using Streamlit.

        This method converts the chart to a Streamlit component and renders it
        in the current Streamlit app.

        Args:
            key: Unique key for the Streamlit component. Used to prevent conflicts
                when multiple charts are rendered on the same page.

        Returns:
            The rendered Streamlit component result.

        Example:
            ```python
            chart = Chart(series=line_series)
            chart.render(key="my_chart")
            ```
        """
        from ..rendering import render_chart

        return render_chart(self, key=key)

    def add_series(self, series: Series) -> "Chart":
        """
        Add a series to the chart.

        This method allows adding additional series to an existing chart,
        supporting method chaining for fluent API usage.

        Args:
            series: Series object to add to the chart.

        Returns:
            Self for method chaining.

        Example:
            ```python
            chart = Chart(series=price_series)
            chart.add_series(volume_series).add_series(macd_series)
            ```
        """
        self.series.append(series)
        return self

    def update_options(self, **kwargs) -> "Chart":
        """
        Update chart options using keyword arguments.

        This method allows updating chart options dynamically. Only valid
        option attributes will be updated.

        Args:
            **kwargs: Options to update. Valid options include any attribute
                of ChartOptions (height, width, layout, grid, etc.).

        Returns:
            Self for method chaining.

        Example:
            ```python
            chart.update_options(height=600, width=800)
            ```
        """
        for key, value in kwargs.items():
            if hasattr(self.options, key):
                setattr(self.options, key, value)
        return self

    def add_annotation(self, annotation: Annotation, layer_name: str = "default") -> "Chart":
        """
        Add an annotation to the chart.

        This method adds a single annotation to a specified layer. If the layer
        doesn't exist, it will be created automatically.

        Args:
            annotation: Annotation object to add to the chart.
            layer_name: Name of the layer to add the annotation to.
                If the layer doesn't exist, it will be created.

        Returns:
            Self for method chaining.

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
    ) -> "Chart":
        """
        Add multiple annotations to the chart.

        This method adds multiple annotations to a specified layer, creating
        the layer if it doesn't exist.

        Args:
            annotations: List of annotation objects to add to the chart.
            layer_name: Name of the layer to add the annotations to.
                If the layer doesn't exist, it will be created.

        Returns:
            Self for method chaining.

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

    def create_annotation_layer(self, name: str) -> "Chart":
        """
        Create a new annotation layer.

        This method creates a new empty annotation layer that can be used
        to organize annotations into groups.

        Args:
            name: Name of the layer to create.

        Returns:
            Self for method chaining.

        Example:
            ```python
            chart.create_annotation_layer("technical_analysis")
            ```
        """
        self.annotation_manager.create_layer(name)
        return self

    def hide_annotation_layer(self, name: str) -> "Chart":
        """
        Hide an annotation layer.

        This method hides a specific annotation layer, making all its
        annotations invisible.

        Args:
            name: Name of the layer to hide.

        Returns:
            Self for method chaining.

        Example:
            ```python
            chart.hide_annotation_layer("events")
            ```
        """
        layer = self.annotation_manager.get_layer(name)
        if layer:
            layer.hide()
        return self

    def show_annotation_layer(self, name: str) -> "Chart":
        """
        Show an annotation layer.

        This method shows a previously hidden annotation layer, making
        all its annotations visible again.

        Args:
            name: Name of the layer to show.

        Returns:
            Self for method chaining.

        Example:
            ```python
            chart.show_annotation_layer("events")
            ```
        """
        layer = self.annotation_manager.get_layer(name)
        if layer:
            layer.show()
        return self

    def clear_annotations(self, layer_name: Optional[str] = None) -> "Chart":
        """
        Clear annotations from a layer or all layers.

        This method removes all annotations from a specific layer or from
        all layers if no layer name is specified.

        Args:
            layer_name: Name of the layer to clear. If None, clears all layers.

        Returns:
            Self for method chaining.

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
        can be consumed by the frontend React component.

        Returns:
            Dictionary containing chart configuration for the frontend,
            including chart options, series data, and annotations.
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
            "annotations": [ann.to_dict() for ann in self.annotation_manager.get_all_annotations()],
            "annotationLayers": annotation_layers,
        }


class MultiPaneChart:
    """
    Chart class for creating multi-pane synchronized charts.

    This class enables creating professional trading dashboards with multiple
    synchronized chart panes, similar to TradingView. Each pane can contain
    different chart types (candlestick, line, histogram, etc.) and all panes
    are automatically synchronized for crosshair movement and time range changes.

    MultiPaneChart is ideal for creating comprehensive trading analysis views
    with price charts, volume indicators, technical indicators, and other
    financial data displayed in separate but synchronized panes.

    Attributes:
        charts: List of Chart objects, each representing a separate pane
            in the multi-pane layout.
    """

    def __init__(self, charts: Optional[List[Chart]] = None):
        """
        Initialize a multi-pane chart with optional initial charts.

        Args:
            charts: List of Chart objects to display in separate panes.
                Each chart will become a separate synchronized pane.
                If None, starts with an empty multi-pane chart.

        Example:
            ```python
            # Create empty multi-pane chart
            multi_chart = MultiPaneChart()

            # Create multi-pane chart with initial charts
            price_chart = Chart(series=candlestick_series)
            volume_chart = Chart(series=volume_series)
            multi_chart = MultiPaneChart(charts=[price_chart, volume_chart])
            ```
        """
        self.charts = charts or []

    def add_pane(self, chart: Chart) -> "MultiPaneChart":
        """
        Add a chart pane to the multi-pane chart.

        This method adds a new chart as a separate pane in the multi-pane layout.
        The new pane will be automatically synchronized with existing panes
        for crosshair movement and time range changes.

        Args:
            chart: Chart object to add as a new pane. Can be any Chart instance
                with any combination of series types.

        Returns:
            Self for method chaining.

        Example:
            ```python
            multi_chart = MultiPaneChart()
            multi_chart.add_pane(price_chart).add_pane(volume_chart).add_pane(rsi_chart)
            ```
        """
        self.charts.append(chart)
        return self

    def render(self, key: Optional[str] = None) -> Any:
        """
        Render the multi-pane chart using Streamlit with synchronization enabled.

        This method renders the multi-pane chart as a Streamlit component with
        automatic synchronization between all panes. Crosshair movement and
        time range changes will be synchronized across all chart panes.

        Args:
            key: Unique key for the Streamlit component. Used to prevent conflicts
                when multiple charts are rendered on the same page.

        Returns:
            The rendered Streamlit component result with synchronized panes.

        Example:
            ```python
            multi_chart = MultiPaneChart()
            multi_chart.add_pane(price_chart).add_pane(volume_chart)
            multi_chart.render(key="trading_dashboard")
            ```
        """
        from ..rendering import render_multi_pane_chart

        return render_multi_pane_chart(self, key=key)

    def to_frontend_config(self) -> List[Dict[str, Any]]:
        """
        Convert multi-pane chart to frontend-compatible configuration.

        This method converts all chart panes into a list of frontend-compatible
        configurations that can be consumed by the React component. Each chart
        pane becomes a separate configuration object in the list.

        Returns:
            List of chart configurations for the frontend, where each element
            represents a separate pane in the multi-pane layout.
        """
        return [chart.to_frontend_config() for chart in self.charts]
