"""
Chart builder for streamlit-lightweight-charts.

This module provides the ChartBuilder class that implements a fluent API
for creating charts with method chaining. It serves as a convenient
factory for building complex charts with multiple series and annotations.

The ChartBuilder supports all major chart types and provides methods
for configuring chart options, adding series, and managing annotations
in a chainable manner.

Example:
    ```python
    from streamlit_lightweight_charts_pro.charts.chart_builder import ChartBuilder

    chart = (ChartBuilder()
             .add_line_series(data, color="#ff0000")
             .add_candlestick_series(ohlc_data)
             .set_height(600)
             .set_width(800)
             .add_annotation(text_ann)
             .build())
    ```
"""

from typing import Any, List, Optional

from ..data.annotation import Annotation
from .options import ChartOptions
from .series import (
    AreaSeries,
    BarSeries,
    BaselineSeries,
    CandlestickSeries,
    HistogramSeries,
    LineSeries,
)
from .single_pane_chart import SinglePaneChart


class ChartBuilder:
    """
    Fluent builder for creating charts with method chaining.

    This class provides a convenient way to create and configure charts
    using a fluent API with method chaining. It allows for intuitive
    chart creation by chaining method calls together.

    The ChartBuilder supports all major chart types and provides methods
    for configuring chart options, adding series, and managing annotations.

    Attributes:
        series: List of series objects to be added to the chart
        options: Chart configuration options
        annotations: List of annotations to be added to the chart

    Example:
        ```python
        chart = (ChartBuilder()
                .add_line_series(data, color="#ff0000")
                .add_candlestick_series(ohlc_data)
                .set_height(600)
                .set_width(800)
                .add_annotation(text_ann)
                .build())
        ```
    """

    def __init__(self):
        """
        Initialize the chart builder.

        Creates a new ChartBuilder instance with empty series list,
        default chart options, and empty annotations list.

        Example:
            ```python
            builder = ChartBuilder()
            ```
        """
        self.series = []
        self.options = ChartOptions()
        self.annotations = []

    def add_line_series(self, data: Any, **kwargs) -> "ChartBuilder":
        """
        Add a line series to the chart.

        Creates a LineSeries with the provided data and configuration,
        then adds it to the chart. Returns self for method chaining.

        Args:
            data: Data for the line series. Can be a list of data objects
                or a pandas DataFrame.
            **kwargs: Additional configuration options for the line series
                (color, line_width, etc.).

        Returns:
            ChartBuilder: Self for method chaining.

        Example:
            ```python
            builder.add_line_series(data, color="#ff0000", line_width=2)
            ```
        """
        series = LineSeries(data=data, **kwargs)
        self.series.append(series)
        return self

    def add_candlestick_series(self, data: Any, **kwargs) -> "ChartBuilder":
        """
        Add a candlestick series to the chart.

        Creates a CandlestickSeries with the provided OHLC data and
        configuration, then adds it to the chart. Returns self for
        method chaining.

        Args:
            data: OHLC data for the candlestick series. Can be a list of
                OhlcData objects or a pandas DataFrame.
            **kwargs: Additional configuration options for the candlestick
                series (up_color, down_color, etc.).

        Returns:
            ChartBuilder: Self for method chaining.

        Example:
            ```python
            builder.add_candlestick_series(ohlc_data, up_color="#4CAF50")
            ```
        """
        series = CandlestickSeries(data=data, **kwargs)
        self.series.append(series)
        return self

    def add_area_series(self, data: Any, **kwargs) -> "ChartBuilder":
        """
        Add an area series to the chart.

        Creates an AreaSeries with the provided data and configuration,
        then adds it to the chart. Returns self for method chaining.

        Args:
            data: Data for the area series. Can be a list of data objects
                or a pandas DataFrame.
            **kwargs: Additional configuration options for the area series
                (color, fill_color, etc.).

        Returns:
            ChartBuilder: Self for method chaining.

        Example:
            ```python
            builder.add_area_series(data, color="#2196F3", fill_color="#E3F2FD")
            ```
        """
        series = AreaSeries(data=data, **kwargs)
        self.series.append(series)
        return self

    def add_bar_series(self, data: Any, **kwargs) -> "ChartBuilder":
        """
        Add a bar series to the chart.

        Creates a BarSeries with the provided data and configuration,
        then adds it to the chart. Returns self for method chaining.

        Args:
            data: Data for the bar series. Can be a list of data objects
                or a pandas DataFrame.
            **kwargs: Additional configuration options for the bar series
                (color, border_color, etc.).

        Returns:
            ChartBuilder: Self for method chaining.

        Example:
            ```python
            builder.add_bar_series(data, color="#FF9800", border_color="#F57C00")
            ```
        """
        series = BarSeries(data=data, **kwargs)
        self.series.append(series)
        return self

    def add_histogram_series(self, data: Any, **kwargs) -> "ChartBuilder":
        """
        Add a histogram series to the chart.

        Creates a HistogramSeries with the provided data and configuration,
        then adds it to the chart. Returns self for method chaining.

        Args:
            data: Data for the histogram series. Can be a list of data objects
                or a pandas DataFrame.
            **kwargs: Additional configuration options for the histogram series
                (color, base, etc.).

        Returns:
            ChartBuilder: Self for method chaining.

        Example:
            ```python
            builder.add_histogram_series(volume_data, color="#9C27B0", base=0)
            ```
        """
        series = HistogramSeries(data=data, **kwargs)
        self.series.append(series)
        return self

    def add_baseline_series(self, data: Any, **kwargs) -> "ChartBuilder":
        """
        Add a baseline series to the chart.

        Creates a BaselineSeries with the provided data and configuration,
        then adds it to the chart. Returns self for method chaining.

        Args:
            data: Data for the baseline series. Can be a list of BaselineData
                objects or a pandas DataFrame.
            **kwargs: Additional configuration options for the baseline series
                (base_value, top_fill_color, etc.).

        Returns:
            ChartBuilder: Self for method chaining.

        Example:
            ```python
            builder.add_baseline_series(data, base_value=100, top_fill_color="#4CAF50")
            ```
        """
        series = BaselineSeries(data=data, **kwargs)
        self.series.append(series)
        return self

    def set_size(self, width: Optional[int] = None, height: Optional[int] = None) -> "ChartBuilder":
        """
        Set chart size.

        Updates the chart's width and/or height. Returns self for
        method chaining.

        Args:
            width: Chart width in pixels. If None, width is not changed.
            height: Chart height in pixels. If None, height is not changed.

        Returns:
            ChartBuilder: Self for method chaining.

        Example:
            ```python
            builder.set_size(width=800, height=600)
            ```
        """
        self.options.set_size(width, height)
        return self

    def set_height(self, height: int) -> "ChartBuilder":
        """
        Set chart height.

        Updates the chart's height. Returns self for method chaining.

        Args:
            height: Chart height in pixels.

        Returns:
            ChartBuilder: Self for method chaining.

        Example:
            ```python
            builder.set_height(400)
            ```
        """
        self.options.height = height
        return self

    def set_width(self, width: int) -> "ChartBuilder":
        """
        Set chart width.

        Updates the chart's width. Returns self for method chaining.

        Args:
            width: Chart width in pixels.

        Returns:
            ChartBuilder: Self for method chaining.

        Example:
            ```python
            builder.set_width(800)
            ```
        """
        self.options.width = width
        return self

    def set_auto_size(self, auto_size: bool = True) -> "ChartBuilder":
        """
        Set auto-sizing.

        Enables or disables automatic sizing of the chart. Returns self
        for method chaining.

        Args:
            auto_size: Whether to enable auto-sizing. Defaults to True.

        Returns:
            ChartBuilder: Self for method chaining.

        Example:
            ```python
            builder.set_auto_size(True)
            ```
        """
        self.options.auto_size = auto_size
        return self

    def add_annotation(self, annotation: Annotation) -> "ChartBuilder":
        """
        Add an annotation to the chart.

        Adds a single annotation to the chart. Returns self for
        method chaining.

        Args:
            annotation: Annotation object to add to the chart.

        Returns:
            ChartBuilder: Self for method chaining.

        Example:
            ```python
            text_ann = create_text_annotation("2024-01-01", 100, "Event")
            builder.add_annotation(text_ann)
            ```
        """
        self.annotations.append(annotation)
        return self

    def add_annotations(self, annotations: List[Annotation]) -> "ChartBuilder":
        """
        Add multiple annotations to the chart.

        Adds multiple annotations to the chart. Returns self for
        method chaining.

        Args:
            annotations: List of annotation objects to add to the chart.

        Returns:
            ChartBuilder: Self for method chaining.

        Example:
            ```python
            annotations = [ann1, ann2, ann3]
            builder.add_annotations(annotations)
            ```
        """
        self.annotations.extend(annotations)
        return self

    def build(self) -> SinglePaneChart:
        """
        Build and return the chart.

        Creates a SinglePaneChart instance with all configured series,
        options, and annotations. Raises an error if no series have
        been added.

        Returns:
            SinglePaneChart: The configured chart instance.

        Raises:
            ValueError: If no series have been added to the chart.

        Example:
            ```python
            chart = builder.build()
            chart.render(key="my_chart")
            ```
        """
        if not self.series:
            raise ValueError("At least one series must be added to the chart")

        return SinglePaneChart(
            series=self.series, options=self.options, annotations=self.annotations
        )


def create_chart() -> ChartBuilder:
    """
    Create a new chart builder for fluent chart creation.

    This is a convenience function that creates a new ChartBuilder instance,
    allowing for a more concise syntax when creating charts with the fluent API.

    Returns:
        ChartBuilder: A new chart builder instance.

    Example:
        ```python
        chart = (create_chart()
                .add_line_series(data, color="#ff0000")
                .set_height(600)
                .build())
        ```
    """
    return ChartBuilder() 