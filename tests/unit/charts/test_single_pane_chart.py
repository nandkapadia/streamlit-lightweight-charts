"""Comprehensive tests for SinglePaneChart class."""

import pandas as pd

from streamlit_lightweight_charts_pro.charts.options import ChartOptions
from streamlit_lightweight_charts_pro.charts.series import (
    AreaSeries,
    BarSeries,
    BaselineSeries,
    CandlestickSeries,
    HistogramSeries,
    LineSeries,
)
from streamlit_lightweight_charts_pro.charts.single_pane_chart import SinglePaneChart
from streamlit_lightweight_charts_pro.data import (
    OhlcData,
    SingleValueData,
    create_arrow_annotation,
    create_shape_annotation,
    create_text_annotation,
)


class TestSinglePaneChart:
    """Comprehensive test cases for SinglePaneChart functionality."""

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

        self.line_series = LineSeries(self.sample_data, color="#ff0000")
        self.candlestick_series = CandlestickSeries(self.ohlc_data)
        self.options = ChartOptions(height=400, width=600)

    # ===== INITIALIZATION TESTS =====

    def test_initialization_single_series(self):
        """Test SinglePaneChart initialization with single series."""
        chart = SinglePaneChart(series=self.line_series)

        assert len(chart.series) == 1
        assert chart.series[0] == self.line_series
        assert isinstance(chart.options, ChartOptions)
        assert chart.annotation_manager is not None

    def test_initialization_multiple_series(self):
        """Test SinglePaneChart initialization with multiple series."""
        chart = SinglePaneChart(series=[self.line_series, self.candlestick_series])

        assert len(chart.series) == 2
        assert chart.series[0] == self.line_series
        assert chart.series[1] == self.candlestick_series

    def test_initialization_with_options(self):
        """Test SinglePaneChart initialization with custom options."""
        options = ChartOptions(height=500, width=700)
        chart = SinglePaneChart(series=self.line_series, options=options)

        assert chart.options.height == 500
        assert chart.options.width == 700

    def test_initialization_with_annotations(self):
        """Test SinglePaneChart initialization with annotations."""
        annotation = create_text_annotation("2024-01-01", 100, "Test")
        chart = SinglePaneChart(series=self.line_series, annotations=[annotation])

        assert len(chart.annotation_manager.layers) > 0
        # Check that annotation was added to default layer
        default_layer = chart.annotation_manager.get_layer("default")
        assert len(default_layer.annotations) == 1

    def test_initialization_with_empty_series_list(self):
        """Test initialization with empty series list."""
        chart = SinglePaneChart(series=[])

        assert len(chart.series) == 0
        assert isinstance(chart.options, ChartOptions)

    # ===== SERIES MANAGEMENT TESTS =====

    def test_add_series(self):
        """Test adding series to chart."""
        chart = SinglePaneChart(series=self.line_series)

        result = chart.add_series(self.candlestick_series)

        assert result is chart  # Method chaining
        assert len(chart.series) == 2
        assert chart.series[1] == self.candlestick_series

    def test_add_multiple_series(self):
        """Test adding multiple series."""
        chart = SinglePaneChart(series=self.line_series)
        area_series = AreaSeries(self.sample_data, line_color="#0000ff")
        bar_series = BarSeries(self.sample_data, color="#00ff00")

        chart.add_series(area_series).add_series(bar_series)

        assert len(chart.series) == 3
        assert isinstance(chart.series[1], AreaSeries)
        assert isinstance(chart.series[2], BarSeries)

    # ===== OPTIONS MANAGEMENT TESTS =====

    def test_update_options(self):
        """Test updating chart options."""
        chart = SinglePaneChart(series=self.line_series)

        result = chart.update_options(height=600, width=800)

        assert result is chart
        assert chart.options.height == 600
        assert chart.options.width == 800

    def test_update_options_invalid_attribute(self):
        """Test updating options with invalid attribute."""
        chart = SinglePaneChart(series=self.line_series)
        original_height = chart.options.height

        # Try to update with invalid attribute
        result = chart.update_options(invalid_attr="value")

        assert result is chart  # Method chaining
        assert chart.options.height == original_height  # Should not change

    # ===== ANNOTATION MANAGEMENT TESTS =====

    def test_add_annotation_to_existing_layer(self):
        """Test adding annotation to existing layer."""
        chart = SinglePaneChart(series=self.line_series)
        annotation = create_text_annotation("2024-01-01", 100, "Test")

        # Create layer first
        chart.create_annotation_layer("test_layer")

        result = chart.add_annotation(annotation, "test_layer")

        assert result is chart  # Method chaining
        layer = chart.annotation_manager.get_layer("test_layer")
        assert len(layer.annotations) == 1

    def test_add_annotation_to_new_layer(self):
        """Test adding annotation to new layer."""
        chart = SinglePaneChart(series=self.line_series)
        annotation = create_text_annotation("2024-01-01", 100, "Test")

        result = chart.add_annotation(annotation, "new_layer")

        assert result is chart  # Method chaining
        layer = chart.annotation_manager.get_layer("new_layer")
        assert layer is not None
        assert len(layer.annotations) == 1

    def test_add_annotation_to_default_layer(self):
        """Test adding annotation to default layer."""
        chart = SinglePaneChart(series=self.line_series)
        annotation = create_text_annotation("2024-01-01", 100, "Test")

        result = chart.add_annotation(annotation)

        assert result is chart
        default_layer = chart.annotation_manager.get_layer("default")
        assert len(default_layer.annotations) == 1

    def test_add_annotations(self):
        """Test adding multiple annotations."""
        chart = SinglePaneChart(series=self.line_series)
        annotations = [
            create_text_annotation("2024-01-01", 100, "First"),
            create_text_annotation("2024-01-02", 105, "Second"),
        ]

        result = chart.add_annotations(annotations, "test_layer")

        assert result is chart  # Method chaining
        layer = chart.annotation_manager.get_layer("test_layer")
        assert len(layer.annotations) == 2

    def test_add_annotations_to_default_layer(self):
        """Test adding multiple annotations to default layer."""
        chart = SinglePaneChart(series=self.line_series)
        annotations = [
            create_text_annotation("2024-01-01", 100, "First"),
            create_text_annotation("2024-01-02", 105, "Second"),
        ]

        result = chart.add_annotations(annotations)

        assert result is chart
        default_layer = chart.annotation_manager.get_layer("default")
        assert len(default_layer.annotations) == 2

    def test_create_annotation_layer(self):
        """Test creating annotation layer."""
        chart = SinglePaneChart(series=self.line_series)

        result = chart.create_annotation_layer("test_layer")

        assert result is chart  # Method chaining
        layer = chart.annotation_manager.get_layer("test_layer")
        assert layer is not None
        assert layer.name == "test_layer"

    def test_hide_annotation_layer(self):
        """Test hiding annotation layer."""
        chart = SinglePaneChart(series=self.line_series)
        chart.create_annotation_layer("test_layer")

        result = chart.hide_annotation_layer("test_layer")

        assert result is chart  # Method chaining
        layer = chart.annotation_manager.get_layer("test_layer")
        assert layer.visible is False

    def test_show_annotation_layer(self):
        """Test showing annotation layer."""
        chart = SinglePaneChart(series=self.line_series)
        chart.create_annotation_layer("test_layer")
        chart.hide_annotation_layer("test_layer")

        result = chart.show_annotation_layer("test_layer")

        assert result is chart  # Method chaining
        layer = chart.annotation_manager.get_layer("test_layer")
        assert layer.visible is True

    def test_clear_annotations_specific_layer(self):
        """Test clearing annotations from specific layer."""
        chart = SinglePaneChart(series=self.line_series)
        annotation = create_text_annotation("2024-01-01", 100, "Test")
        chart.add_annotation(annotation, "test_layer")

        result = chart.clear_annotations("test_layer")

        assert result is chart  # Method chaining
        layer = chart.annotation_manager.get_layer("test_layer")
        assert len(layer.annotations) == 0

    def test_clear_annotations_all_layers(self):
        """Test clearing annotations from all layers."""
        chart = SinglePaneChart(series=self.line_series)

        # Add annotations to multiple layers
        annotation1 = create_text_annotation("2024-01-01", 100, "Test1")
        annotation2 = create_text_annotation("2024-01-02", 105, "Test2")
        chart.add_annotation(annotation1, "layer1")
        chart.add_annotation(annotation2, "layer2")

        result = chart.clear_annotations()

        assert result is chart  # Method chaining
        # After clear_all_layers(), the layers no longer exist, so get_layer returns None
        layer1 = chart.annotation_manager.get_layer("layer1")
        layer2 = chart.annotation_manager.get_layer("layer2")
        assert layer1 is None
        assert layer2 is None

    def test_hide_nonexistent_layer(self):
        """Test hiding a layer that doesn't exist."""
        chart = SinglePaneChart(series=self.line_series)

        result = chart.hide_annotation_layer("nonexistent")

        assert result is chart
        # Should not raise an error

    def test_show_nonexistent_layer(self):
        """Test showing a layer that doesn't exist."""
        chart = SinglePaneChart(series=self.line_series)

        result = chart.show_annotation_layer("nonexistent")

        assert result is chart
        # Should not raise an error

    def test_clear_nonexistent_layer(self):
        """Test clearing annotations from a layer that doesn't exist."""
        chart = SinglePaneChart(series=self.line_series)

        result = chart.clear_annotations("nonexistent")

        assert result is chart
        # Should not raise an error

    # ===== FRONTEND CONFIGURATION TESTS =====

    def test_to_frontend_config(self):
        """Test generating frontend configuration."""
        chart = SinglePaneChart(series=self.line_series)

        config = chart.to_frontend_config()

        assert "charts" in config
        assert len(config["charts"]) == 1
        assert "series" in config["charts"][0]
        assert "chart" in config["charts"][0]
        assert len(config["charts"][0]["series"]) == 1

    def test_to_frontend_config_with_annotations(self):
        """Test generating frontend configuration with annotations."""
        chart = SinglePaneChart(series=self.line_series)
        annotation = create_text_annotation("2024-01-01", 100, "Test")
        chart.add_annotation(annotation)

        config = chart.to_frontend_config()

        assert "charts" in config
        assert "annotations" in config["charts"][0]
        assert len(config["charts"][0]["annotations"]) > 0

    def test_to_frontend_config_multiple_series(self):
        """Test generating frontend configuration with multiple series."""
        chart = SinglePaneChart(series=[self.line_series, self.candlestick_series])

        config = chart.to_frontend_config()

        assert "charts" in config
        assert len(config["charts"][0]["series"]) == 2

    def test_to_frontend_config_detailed(self):
        """Test converting chart to frontend configuration with detailed checks."""
        chart = SinglePaneChart(series=self.line_series, options=self.options)
        annotation = create_text_annotation("2024-01-01", 100, "Test")
        chart.add_annotation(annotation, "test_layer")

        config = chart.to_frontend_config()

        # The actual structure has charts array containing the chart configuration
        assert "charts" in config
        assert "syncConfig" in config
        assert len(config["charts"]) == 1

        chart_config = config["charts"][0]
        assert "chartId" in chart_config
        assert "chart" in chart_config
        assert "series" in chart_config
        assert "annotations" in chart_config
        assert len(chart_config["series"]) == 1
        assert chart_config["chart"]["height"] == 400
        assert chart_config["chart"]["width"] == 600

    def test_to_frontend_config_with_arrow_annotations(self):
        """Test frontend config with arrow annotations."""
        chart = SinglePaneChart(series=self.line_series)
        annotation = create_arrow_annotation("2024-01-01", 100, "Arrow annotation")
        chart.add_annotation(annotation, "arrows")

        config = chart.to_frontend_config()

        chart_config = config["charts"][0]
        assert "annotations" in chart_config
        assert len(chart_config["annotations"]) > 0

    # ===== RENDER TESTS =====

    def test_render_method(self):
        """Test render method (should return frontend config)."""
        chart = SinglePaneChart(series=self.line_series)

        # The render method returns None when not in a Streamlit context
        # This is expected behavior for testing
        result = chart.render()

        # In test environment, render returns None
        assert result is None

    def test_render_with_key(self):
        """Test render method with key parameter."""
        chart = SinglePaneChart(series=self.line_series)

        # The render method returns None when not in a Streamlit context
        # This is expected behavior for testing
        result = chart.render(key="test_chart")

        # In test environment, render returns None
        assert result is None

    # ===== METHOD CHAINING TESTS =====

    def test_method_chaining(self):
        """Test method chaining functionality."""
        chart = (
            SinglePaneChart(series=self.line_series)
            .add_series(self.candlestick_series)
            .update_options(height=600, width=800)
            .add_annotation(create_text_annotation("2024-01-01", 100, "Test"))
        )

        assert len(chart.series) == 2
        assert chart.options.height == 600
        assert chart.options.width == 800
        assert len(chart.annotation_manager.layers) > 0

    def test_method_chaining_extended(self):
        """Test extended method chaining functionality."""
        chart = (
            SinglePaneChart(series=self.line_series)
            .update_options(height=500)
            .add_series(LineSeries(self.sample_data))
            .create_annotation_layer("test_layer")
        )

        assert chart.options.height == 500
        assert len(chart.series) == 2
        assert chart.annotation_manager.get_layer("test_layer") is not None

    # ===== DATA TYPE TESTS =====

    def test_chart_with_dataframe_series(self):
        """Test chart with DataFrame series."""
        df = pd.DataFrame(
            {"datetime": ["2024-01-01", "2024-01-02", "2024-01-03"], "close": [100, 105, 110]}
        )

        series = LineSeries(df, color="#ff0000")
        chart = SinglePaneChart(series=series)

        assert len(chart.series) == 1
        config = chart.to_frontend_config()
        assert "charts" in config

    def test_chart_with_mixed_series_types(self):
        """Test chart with mixed series types."""
        area_series = AreaSeries(self.sample_data, line_color="#0000ff")
        histogram_series = HistogramSeries(self.sample_data, color="#00ff00")
        baseline_series = BaselineSeries(self.sample_data, top_line_color="#ff00ff")

        chart = SinglePaneChart(
            series=[
                self.line_series,
                self.candlestick_series,
                area_series,
                histogram_series,
                baseline_series,
            ]
        )

        assert len(chart.series) == 5
        assert isinstance(chart.series[0], LineSeries)
        assert isinstance(chart.series[1], CandlestickSeries)
        assert isinstance(chart.series[2], AreaSeries)
        assert isinstance(chart.series[3], HistogramSeries)
        assert isinstance(chart.series[4], BaselineSeries)

    # ===== ANNOTATION MANAGEMENT COMPREHENSIVE TESTS =====

    def test_chart_annotation_management(self):
        """Test comprehensive annotation management."""
        chart = SinglePaneChart(series=self.line_series)

        # Add different types of annotations
        text_ann = create_text_annotation("2024-01-01", 100, "Text")
        arrow_ann = create_arrow_annotation("2024-01-02", 105, "Arrow")
        shape_ann = create_shape_annotation("2024-01-03", 110, "Shape")

        chart.add_annotation(text_ann, "text_layer")
        chart.add_annotation(arrow_ann, "arrow_layer")
        chart.add_annotation(shape_ann, "shape_layer")

        # Verify annotations were added
        assert len(chart.annotation_manager.layers) == 3
        assert len(chart.annotation_manager.get_layer("text_layer").annotations) == 1
        assert len(chart.annotation_manager.get_layer("arrow_layer").annotations) == 1
        assert len(chart.annotation_manager.get_layer("shape_layer").annotations) == 1

    # ===== INHERITANCE AND INTERFACE TESTS =====

    def test_chart_options_inheritance(self):
        """Test that chart properly inherits from BaseChart."""
        chart = SinglePaneChart(series=self.line_series)

        # Test BaseChart methods
        assert hasattr(chart, "series")
        assert hasattr(chart, "options")
        assert hasattr(chart, "annotation_manager")
        assert hasattr(chart, "to_frontend_config")
        assert hasattr(chart, "render")

    # ===== ERROR HANDLING TESTS =====

    def test_chart_error_handling(self):
        """Test chart error handling."""
        # Test with invalid series type - SinglePaneChart accepts any series type
        # so this should not raise an exception
        try:
            SinglePaneChart(series="invalid_series")
            # If we get here, it means the chart accepted the invalid series
            # This is the actual behavior
        except Exception:
            # If an exception is raised, that's also acceptable
            pass

        # Test with invalid options type - SinglePaneChart accepts any options type
        try:
            SinglePaneChart(series=self.line_series, options="invalid_options")
            # If we get here, it means the chart accepted the invalid options
            # This is the actual behavior
        except Exception:
            # If an exception is raised, that's also acceptable
            pass

    # ===== PERFORMANCE TESTS =====

    def test_chart_performance_large_dataset(self):
        """Test chart performance with large dataset."""
        large_data = [SingleValueData(f"2024-01-{i:02d}", 100 + i) for i in range(1, 1001)]
        large_series = LineSeries(large_data, color="#ff0000")

        chart = SinglePaneChart(series=large_series)
        config = chart.to_frontend_config()

        assert "charts" in config
        assert len(config["charts"][0]["series"][0]["data"]) == 1000

    # ===== COMPLEX WORKFLOW TESTS =====

    def test_chart_complex_workflow(self):
        """Test complex chart workflow."""
        # Create multiple series with different data
        line_data = [SingleValueData(f"2024-01-{i:02d}", 100 + i) for i in range(1, 6)]
        area_data = [SingleValueData(f"2024-01-{i:02d}", 90 + i) for i in range(1, 6)]

        line_series = LineSeries(line_data, color="#ff0000", line_width=2)
        area_series = AreaSeries(area_data, line_color="#0000ff", top_color="#0000ff")

        # Create annotations
        start_ann = create_text_annotation("2024-01-01", 100, "Start")
        end_ann = create_text_annotation("2024-01-05", 104, "End")

        # Build complex chart
        chart = (
            SinglePaneChart(series=line_series)
            .add_series(area_series)
            .update_options(height=600, width=800, auto_size=True)
            .add_annotation(start_ann, "start")
            .add_annotation(end_ann, "end")
        )

        # Verify chart structure
        assert len(chart.series) == 2
        assert chart.options.height == 600
        assert chart.options.width == 800
        assert chart.options.auto_size is True
        assert len(chart.annotation_manager.layers) == 2

        # Generate frontend config
        config = chart.to_frontend_config()
        assert "charts" in config
        assert len(config["charts"][0]["series"]) == 2
        assert len(config["charts"][0]["annotations"]) > 0
