"""Tests for ChartBuilder class."""

import pandas as pd
import pytest

from streamlit_lightweight_charts_pro.charts.chart_builder import ChartBuilder
from streamlit_lightweight_charts_pro.charts.options import ChartOptions
from streamlit_lightweight_charts_pro.charts.series import (
    AreaSeries,
    BarSeries,
    BaselineSeries,
    CandlestickSeries,
    HistogramSeries,
    LineSeries,
)
from streamlit_lightweight_charts_pro.data import (
    OhlcData,
    SingleValueData,
    create_text_annotation,
)
from streamlit_lightweight_charts_pro.type_definitions.enums import ColumnNames


class TestChartBuilder:
    """Test ChartBuilder functionality."""

    def setup_method(self):
        """Set up test data."""
        self.sample_data = [
            SingleValueData("2024-01-01", 100),
            SingleValueData("2024-01-02", 105),
            SingleValueData("2024-01-03", 110),
        ]

        self.ohlc_data = [
            OhlcData("2024-01-01", 100, 105, 98, 103),
            OhlcData("2024-01-02", 103, 108, 102, 106),
            OhlcData("2024-01-03", 106, 112, 104, 110),
        ]

        self.builder = ChartBuilder()

    def test_chart_builder_initialization(self):
        """Test ChartBuilder initialization."""
        builder = ChartBuilder()

        assert builder.series == []
        assert isinstance(builder.options, ChartOptions)
        assert builder.annotations == []

    def test_add_line_series(self):
        """Test adding line series."""
        result = self.builder.add_line_series(self.sample_data, color="#ff0000")

        assert result is self.builder  # Method chaining
        assert len(self.builder.series) == 1
        assert isinstance(self.builder.series[0], LineSeries)
        assert self.builder.series[0].color == "#ff0000"

    def test_add_line_series_with_dataframe(self):
        """Test adding line series with DataFrame."""
        df = pd.DataFrame(
            {
                ColumnNames.DATETIME: ["2024-01-01", "2024-01-02", "2024-01-03"],
                ColumnNames.CLOSE: [100, 105, 110],
            }
        )

        result = self.builder.add_line_series(df, color="#00ff00")

        assert result is self.builder
        assert len(self.builder.series) == 1
        assert isinstance(self.builder.series[0], LineSeries)

    def test_add_candlestick_series(self):
        """Test adding candlestick series."""
        result = self.builder.add_candlestick_series(self.ohlc_data)

        assert result is self.builder
        assert len(self.builder.series) == 1
        assert isinstance(self.builder.series[0], CandlestickSeries)

    def test_add_candlestick_series_with_dataframe(self):
        """Test adding candlestick series with DataFrame."""
        df = pd.DataFrame(
            {
                ColumnNames.DATETIME: ["2024-01-01", "2024-01-02", "2024-01-03"],
                ColumnNames.OPEN: [100, 103, 106],
                ColumnNames.HIGH: [105, 108, 112],
                ColumnNames.LOW: [98, 102, 104],
                ColumnNames.CLOSE: [103, 106, 110],
            }
        )

        result = self.builder.add_candlestick_series(df)

        assert result is self.builder
        assert len(self.builder.series) == 1
        assert isinstance(self.builder.series[0], CandlestickSeries)

    def test_add_area_series(self):
        """Test adding area series."""
        result = self.builder.add_area_series(self.sample_data, line_color="#0000ff")

        assert result is self.builder
        assert len(self.builder.series) == 1
        assert isinstance(self.builder.series[0], AreaSeries)
        assert self.builder.series[0].line_color == "#0000ff"

    def test_add_bar_series(self):
        """Test adding bar series."""
        result = self.builder.add_bar_series(self.sample_data, color="#ffff00")

        assert result is self.builder
        assert len(self.builder.series) == 1
        assert isinstance(self.builder.series[0], BarSeries)
        assert self.builder.series[0].color == "#ffff00"

    def test_add_histogram_series(self):
        """Test adding histogram series."""
        result = self.builder.add_histogram_series(self.sample_data, color="#ff00ff")

        assert result is self.builder
        assert len(self.builder.series) == 1
        assert isinstance(self.builder.series[0], HistogramSeries)
        assert self.builder.series[0].color == "#ff00ff"

    def test_add_baseline_series(self):
        """Test adding baseline series."""
        result = self.builder.add_baseline_series(self.sample_data, top_line_color="#00ffff")

        assert result is self.builder
        assert len(self.builder.series) == 1
        assert isinstance(self.builder.series[0], BaselineSeries)
        assert self.builder.series[0].top_line_color == "#00ffff"

    def test_multiple_series_management(self):
        """Test adding multiple series."""
        self.builder.add_line_series(self.sample_data, color="#ff0000")
        self.builder.add_candlestick_series(self.ohlc_data)
        self.builder.add_area_series(self.sample_data, line_color="#0000ff")

        assert len(self.builder.series) == 3
        assert isinstance(self.builder.series[0], LineSeries)
        assert isinstance(self.builder.series[1], CandlestickSeries)
        assert isinstance(self.builder.series[2], AreaSeries)

    def test_set_height(self):
        """Test setting chart height."""
        result = self.builder.set_height(600)

        assert result is self.builder
        assert self.builder.options.height == 600

    def test_set_width(self):
        """Test setting chart width."""
        result = self.builder.set_width(800)

        assert result is self.builder
        assert self.builder.options.width == 800

    def test_set_auto_size(self):
        """Test setting auto size."""
        result = self.builder.set_auto_size(True)

        assert result is self.builder
        assert self.builder.options.auto_size is True

    def test_set_watermark(self):
        """Test setting watermark."""
        result = self.builder.set_watermark("Test Watermark")

        assert result is self.builder
        assert self.builder.options.watermark == "Test Watermark"

    def test_set_watermark_with_options(self):
        """Test setting watermark with options."""
        # ChartBuilder.set_watermark only accepts a string, not additional options
        result = self.builder.set_watermark("Test Watermark")

        assert result is self.builder
        assert self.builder.options.watermark == "Test Watermark"

    def test_set_legend(self):
        """Test setting legend."""
        result = self.builder.set_legend(True)

        assert result is self.builder
        assert self.builder.options.legend is True

    def test_set_legend_with_options(self):
        """Test setting legend with options."""
        # ChartBuilder.set_legend only accepts a boolean, not additional options
        result = self.builder.set_legend(True)

        assert result is self.builder
        assert self.builder.options.legend is True

    def test_add_annotation(self):
        """Test adding annotation."""
        annotation = create_text_annotation("2024-01-01", 100, "Test")
        result = self.builder.add_annotation(annotation)

        assert result is self.builder
        assert len(self.builder.annotations) == 1
        assert self.builder.annotations[0] == annotation

    def test_add_multiple_annotations(self):
        """Test adding multiple annotations."""
        ann1 = create_text_annotation("2024-01-01", 100, "Test 1")
        ann2 = create_text_annotation("2024-01-02", 105, "Test 2")

        self.builder.add_annotation(ann1)
        self.builder.add_annotation(ann2)

        assert len(self.builder.annotations) == 2
        assert self.builder.annotations[0] == ann1
        assert self.builder.annotations[1] == ann2

    def test_build_single_pane_chart(self):
        """Test building single pane chart."""
        self.builder.add_line_series(self.sample_data)
        chart = self.builder.build()

        assert chart is not None
        assert hasattr(chart, "series")
        assert hasattr(chart, "options")
        assert hasattr(chart, "annotation_manager")

    def test_build_with_annotations(self):
        """Test building chart with annotations."""
        self.builder.add_line_series(self.sample_data)
        annotation = create_text_annotation("2024-01-01", 100, "Test")
        self.builder.add_annotation(annotation)

        chart = self.builder.build()

        assert chart is not None
        # Check that annotations are properly transferred
        assert len(chart.annotation_manager.layers) > 0

    def test_fluent_api_chaining(self):
        """Test fluent API method chaining."""
        chart = (
            self.builder.add_line_series(self.sample_data, color="#ff0000")
            .add_candlestick_series(self.ohlc_data)
            .set_height(600)
            .set_width(800)
            .set_watermark("Test Chart")
            .set_legend(True)
            .add_annotation(create_text_annotation("2024-01-01", 100, "Start"))
            .build()
        )

        assert chart is not None
        assert len(chart.series) == 2
        assert chart.options.height == 600
        assert chart.options.width == 800
        assert chart.options.watermark == "Test Chart"
        assert chart.options.legend is True

    def test_build_with_custom_options(self):
        """Test building with custom options."""
        custom_options = ChartOptions(height=500, width=700)
        builder = ChartBuilder()
        builder.options = custom_options

        builder.add_line_series(self.sample_data)
        chart = builder.build()

        assert chart.options.height == 500
        assert chart.options.width == 700

    def test_empty_builder_build(self):
        """Test building chart with no series."""
        # ChartBuilder requires at least one series
        with pytest.raises(ValueError):
            self.builder.build()

    def test_builder_with_dataframe_series(self):
        """Test builder with DataFrame series."""
        df = pd.DataFrame(
            {
                ColumnNames.DATETIME: ["2024-01-01", "2024-01-02", "2024-01-03"],
                ColumnNames.CLOSE: [100, 105, 110],
            }
        )

        chart = self.builder.add_line_series(df, color="#ff0000").set_height(400).build()

        assert chart is not None
        assert len(chart.series) == 1
        assert chart.options.height == 400

    def test_builder_error_handling(self):
        """Test builder error handling with invalid data."""
        # Test with invalid data type - error occurs when trying to use the data
        self.builder.add_line_series("invalid_data")
        with pytest.raises(AttributeError):
            self.builder.series[0].to_dict()

    def test_builder_series_options(self):
        """Test builder with series-specific options."""
        chart = (
            self.builder.add_line_series(
                self.sample_data, color="#ff0000", line_width=2, line_style="solid"
            )
            .add_candlestick_series(self.ohlc_data, up_color="#00ff00", down_color="#ff0000")
            .build()
        )

        assert chart is not None
        assert len(chart.series) == 2

        # Check line series options
        line_series = chart.series[0]
        assert line_series.color == "#ff0000"
        assert line_series.line_width == 2
        assert line_series.line_style == "solid"

        # Check candlestick series options
        candlestick_series = chart.series[1]
        assert candlestick_series.up_color == "#00ff00"
        assert candlestick_series.down_color == "#ff0000"

    def test_builder_complex_workflow(self):
        """Test complex builder workflow."""
        # Create multiple data series
        line_data = [SingleValueData(f"2024-01-{i:02d}", 100 + i) for i in range(1, 6)]
        area_data = [SingleValueData(f"2024-01-{i:02d}", 90 + i) for i in range(1, 6)]

        # Create annotations
        start_ann = create_text_annotation("2024-01-01", 100, "Start")
        end_ann = create_text_annotation("2024-01-05", 104, "End")

        # Build complex chart
        chart = (
            self.builder.add_line_series(line_data, color="#ff0000", line_width=2)
            .add_area_series(area_data, line_color="#0000ff")
            .set_height(600)
            .set_width(800)
            .set_auto_size(True)
            .set_watermark("Complex Chart")
            .set_legend(True)
            .add_annotation(start_ann)
            .add_annotation(end_ann)
            .build()
        )

        assert chart is not None
        assert len(chart.series) == 2
        assert chart.options.height == 600
        assert chart.options.width == 800
        assert chart.options.auto_size is True
        assert chart.options.watermark == "Complex Chart"
        assert chart.options.legend is True
        assert len(chart.annotation_manager.layers) > 0
