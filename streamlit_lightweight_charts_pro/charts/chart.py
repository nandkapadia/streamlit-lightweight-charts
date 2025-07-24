"""
Chart implementation for streamlit-lightweight-charts.

This module provides the Chart class, which is the primary chart
type for displaying financial data in a single pane. It supports multiple
series types, annotations, and comprehensive customization options.

The Chart class provides a complete implementation for rendering interactive
financial charts with method chaining support for fluent API usage.

Example:
    ```python
    from streamlit_lightweight_charts_pro import Chart, LineSeries
    from streamlit_lightweight_charts_pro.data import SingleValueData

    # Create data
    data = [SingleValueData("2024-01-01", 100), SingleValueData("2024-01-02", 105)]

    # Create chart with method chaining
    chart = (Chart(series=LineSeries(data))
             .update_options(height=400)
             .add_annotation(create_text_annotation("2024-01-01", 100, "Start")))

    # Render in Streamlit
    chart.render(key="my_chart")
    ```
"""

from typing import Any, Dict, List, Optional, Sequence, Union

import pandas as pd

from streamlit_lightweight_charts_pro.charts.options import ChartOptions
from streamlit_lightweight_charts_pro.charts.options.price_scale_options import (
    PriceScaleMargins,
    PriceScaleOptions,
)
from streamlit_lightweight_charts_pro.charts.series import (
    CandlestickSeries,
    HistogramSeries,
    LineSeries,
    Series,
)
from streamlit_lightweight_charts_pro.component import get_component_func
from streamlit_lightweight_charts_pro.data import OhlcData, OhlcvData
from streamlit_lightweight_charts_pro.data.annotation import Annotation, AnnotationManager
from streamlit_lightweight_charts_pro.type_definitions.enums import ColumnNames, PriceScaleMode


class Chart:
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
        chart = Chart(series=LineSeries(data))

        # With method chaining
        chart = (Chart(series=LineSeries(data))
                 .update_options(height=400)
                 .add_annotation(text_annotation))
        ```
    """

    def __init__(
        self,
        series: Optional[Union[Series, List[Series]]] = None,
        options: Optional[ChartOptions] = None,
        annotations: Optional[List[Annotation]] = None,
    ):
        """
        Initialize a single pane chart.

        Args:
            series: Optional single series object or list of series objects to display.
                Each series represents a different data visualization (line,
                candlestick, area, etc.). If None, an empty chart is created.
            options: Optional chart configuration options. If not provided,
                default options will be used.
            annotations: Optional list of annotations to add to the chart.
                Annotations can include text, arrows, shapes, etc.

        Example:
            ```python
            # Empty chart
            chart = Chart()

            # Single series
            chart = Chart(series=LineSeries(data))

            # Multiple series
            chart = Chart(series=[line_series, candlestick_series])

            # With options and annotations
            chart = Chart(
                series=line_series,
                options=ChartOptions(height=500),
                annotations=[text_annotation]
            )
            ```
        """
        # Convert single series to list for consistent handling
        if series is None:
            self.series = []
        elif isinstance(series, Series):
            self.series = [series]
        else:
            self.series = list(series)

        # Initialize chart options
        self.options = options or ChartOptions()

        # Initialize annotation manager
        self.annotation_manager = AnnotationManager()

        # Add initial annotations if provided
        if annotations:
            for annotation in annotations:
                self.add_annotation(annotation)

    def add_series(self, series: Series) -> "Chart":
        """
        Add a series to the chart.

        Args:
            series: Series object to add to the chart.

        Returns:
            Chart: Self for method chaining.

        Example:
            ```python
            chart.add_series(CandlestickSeries(ohlc_data))
            ```
        """
        self.series.append(series)
        return self

    def update_options(self, **kwargs) -> "Chart":
        """
        Update chart options.

        Args:
            **kwargs: Chart options to update.

        Returns:
            Chart: Self for method chaining.

        Example:
            ```python
            chart.update_options(height=600, width=800, auto_size=True)
            ```
        """
        for key, value in kwargs.items():
            if hasattr(self.options, key):
                setattr(self.options, key, value)
            # Silently ignore invalid attributes for method chaining
        return self

    def add_annotation(self, annotation: Annotation, layer_name: str = "default") -> "Chart":
        """
        Add an annotation to the chart.

        Args:
            annotation: Annotation object to add.
            layer_name: Name of the annotation layer (default: "default").

        Returns:
            Chart: Self for method chaining.

        Example:
            ```python
            chart.add_annotation(create_text_annotation("2024-01-01", 100, "Start"))
            ```
        """
        self.annotation_manager.add_annotation(annotation, layer_name)
        return self

    def add_annotations(
        self, annotations: List[Annotation], layer_name: str = "default"
    ) -> "Chart":
        """
        Add multiple annotations to the chart.

        Args:
            annotations: List of annotation objects to add.
            layer_name: Name of the annotation layer (default: "default").

        Returns:
            Chart: Self for method chaining.

        Example:
            ```python
            annotations = [
                create_text_annotation("2024-01-01", 100, "Start"),
                create_arrow_annotation("2024-01-02", 105, "Trend")
            ]
            chart.add_annotations(annotations)
            ```
        """
        for annotation in annotations:
            self.add_annotation(annotation, layer_name)
        return self

    def create_annotation_layer(self, name: str) -> "Chart":
        """
        Create a new annotation layer.

        Args:
            name: Name of the annotation layer.

        Returns:
            Chart: Self for method chaining.

        Example:
            ```python
            chart.create_annotation_layer("analysis")
            ```
        """
        self.annotation_manager.create_layer(name)
        return self

    def hide_annotation_layer(self, name: str) -> "Chart":
        """
        Hide an annotation layer.

        Args:
            name: Name of the annotation layer to hide.

        Returns:
            Chart: Self for method chaining.

        Example:
            ```python
            chart.hide_annotation_layer("analysis")
            ```
        """
        self.annotation_manager.hide_layer(name)
        return self

    def show_annotation_layer(self, name: str) -> "Chart":
        """
        Show an annotation layer.

        Args:
            name: Name of the annotation layer to show.

        Returns:
            Chart: Self for method chaining.

        Example:
            ```python
            chart.show_annotation_layer("analysis")
            ```
        """
        self.annotation_manager.show_layer(name)
        return self

    def clear_annotations(self, layer_name: Optional[str] = None) -> "Chart":
        """
        Clear annotations from the chart.

        Args:
            layer_name: Name of the layer to clear. If None, clears all layers.

        Returns:
            Chart: Self for method chaining.

        Example:
            ```python
            # Clear specific layer
            chart.clear_annotations("analysis")

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

    def add_overlay_price_scale(self, scale_id: str, options: "PriceScaleOptions") -> "Chart":
        """
        Add or update a custom overlay price scale configuration.

        Args:
            scale_id: The id of the custom price scale (e.g., 'volume', 'indicator1').
            options: A PriceScaleOptions instance (see TradingView Lightweight Charts API).

        Returns:
            Chart: Self for method chaining.

        Example:
            chart.add_overlay_price_scale('volume', PriceScaleOptions(visible=False,
                                           scale_margin_top=0.8, scale_margin_bottom=0,
                                           overlay=True,
                                           autoScale=True,
                                           mode=PriceScaleMode.NORMAL,
                                           ))
        """
        if not isinstance(options, PriceScaleOptions):
            raise TypeError("options must be a PriceScaleOptions instance")
        self.options.overlay_price_scales[scale_id] = options
        return self

    def _create_price_volume_series(
        self,
        data: Union[Sequence[Union[OhlcData, OhlcvData]], pd.DataFrame],
        column_mapping: dict = None,
        price_type: str = "candlestick",
        price_kwargs=None,
        volume_kwargs=None,
        price_pane_id: int = 0,
        volume_pane_id: int = None,
    ) -> tuple:
        price_kwargs = price_kwargs or {}
        volume_kwargs = volume_kwargs or {}

        if volume_pane_id is None:
            volume_pane_id = price_pane_id

        # Price series (default price scale)
        if price_type == "candlestick":
            price_series = CandlestickSeries(
                data=data,
                column_mapping=column_mapping,
                pane_id=price_pane_id,
                price_scale_id="right",
                **price_kwargs,
            )
        elif price_type == "line":
            price_series = LineSeries(
                data=data,
                column_mapping=column_mapping,
                pane_id=price_pane_id,
                price_scale_id="right",
                **price_kwargs,
            )
        else:
            raise ValueError("price_type must be 'candlestick' or 'line'")

        # Set default up/down colors for volume if not provided
        volume_kwargs.setdefault("up_color", "rgba(38,166,154,0.5)")
        volume_kwargs.setdefault("down_color", "rgba(239,83,80,0.5)")

        volume_price_scale = PriceScaleOptions(
            visible=False,
            auto_scale=True,
            border_visible=False,
            mode=PriceScaleMode.NORMAL,
            scale_margins=PriceScaleMargins(top=0.8, bottom=0.0),
            price_scale_id=ColumnNames.VOLUME,
        )
        self.add_overlay_price_scale(ColumnNames.VOLUME, volume_price_scale)

        # need to add a mapping for the volume column
        column_mapping[ColumnNames.VALUE] = ColumnNames.VOLUME

        volume_series = HistogramSeries(
            data=data,
            column_mapping=column_mapping,
            pane_id=volume_pane_id,
            price_scale_id=ColumnNames.VOLUME,
            price_format={"type": "volume", "precision": 0},
            **volume_kwargs,
        )

        return price_series, volume_series

    def add_price_volume_series(
        self,
        data: Union[Sequence[Union[OhlcData, OhlcvData]], pd.DataFrame],
        column_mapping: dict = None,
        price_type: str = "candlestick",
        price_kwargs=None,
        volume_kwargs=None,
        pane_id: int = 0,
    ) -> "Chart":
        price_series, volume_series = self._create_price_volume_series(
            data=data,
            column_mapping=column_mapping,
            price_type=price_type,
            price_kwargs=price_kwargs,
            volume_kwargs=volume_kwargs,
            price_pane_id=pane_id,
            volume_pane_id=pane_id,  # Same pane for both
        )
        self.add_series(price_series)
        self.add_series(volume_series)
        return self

    @classmethod
    def from_price_volume_dataframe(
        cls,
        data: Union[Sequence[Union[OhlcData, OhlcvData]], pd.DataFrame],
        column_mapping: dict = None,
        price_type: str = "candlestick",
        price_kwargs=None,
        volume_kwargs=None,
        pane_id: int = 0,
    ) -> "Chart":
        chart = cls()
        price_series, volume_series = chart._create_price_volume_series(
            data=data,
            column_mapping=column_mapping,
            price_type=price_type,
            price_kwargs=price_kwargs,
            volume_kwargs=volume_kwargs,
            price_pane_id=pane_id,
            volume_pane_id=pane_id,
        )

        chart.add_series(price_series)
        chart.add_series(volume_series)

        return chart

    def to_frontend_config(self) -> Dict[str, Any]:
        series_configs = []
        pane_heights = {}
        for series in self.series:
            series_config = series.to_dict()
            series_configs.append(series_config)
            if series.height is not None:
                pane_id = getattr(series, "pane_id", 0)
                if pane_id not in pane_heights:
                    pane_heights[pane_id] = series.height
        chart_config = self.options.to_dict()
        # Ensure rightPriceScale, PriceScaleOptions, PriceScaleOptionss are present and dicts
        if self.options.right_price_scale is not None:
            chart_config["rightPriceScale"] = self.options.right_price_scale.to_dict()
        if self.options.left_price_scale is not None:
            chart_config["leftPriceScale"] = self.options.left_price_scale.to_dict()

        if self.options.overlay_price_scales is not None:
            chart_config["overlayPriceScales"] = {
                k: (v.to_dict() if hasattr(v, "to_dict") else v)
                for k, v in self.options.overlay_price_scales.items()
            }
        annotations_config = self.annotation_manager.to_dict()
        chart_obj = {
            "chartId": f"chart-{id(self)}",
            "chart": chart_config,
            "series": series_configs,
            "annotations": annotations_config,
            "layout": chart_config.get("layout", {}),
        }
        if pane_heights:
            chart_obj["paneHeights"] = pane_heights
        config = {
            "charts": [chart_obj],
            "syncConfig": {
                "enabled": False,
                "crosshair": False,
                "timeRange": False,
            },
        }
        return config

    def render(self, key: Optional[str] = None) -> Any:
        """
        Render the chart in Streamlit.

        This method converts the chart to frontend configuration and
        renders it using the Streamlit component.

        Args:
            key: Optional unique key for the Streamlit component.

        Returns:
            Any: The rendered Streamlit component.

        Example:
            ```python
            chart.render(key="my_chart")
            ```
        """
        config = self.to_frontend_config()
        component_func = get_component_func()
        return component_func(config=config, key=key)
