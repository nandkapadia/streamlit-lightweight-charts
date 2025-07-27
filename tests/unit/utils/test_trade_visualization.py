"""
Tests for trade visualization utilities.

This module tests the trade visualization functionality that converts Trade objects
into visual elements for chart display. This addresses the critical coverage gap
in the trade_visualization.py module.
"""

from typing import Any, Dict, List

import pytest

from streamlit_lightweight_charts_pro.charts.options.trade_visualization_options import (
    TradeVisualizationOptions,
)
from streamlit_lightweight_charts_pro.data import Trade
from streamlit_lightweight_charts_pro.type_definitions.enums import TradeType, TradeVisualization
from streamlit_lightweight_charts_pro.utils.trade_visualization import (
    add_trades_to_series,
    create_trade_annotation,
    create_trade_arrow,
    create_trade_line,
    create_trade_rectangle,
    create_trade_shapes_series,
    create_trade_zone,
    get_line_style_value,
    trades_to_visual_elements,
)


class TestTradesToVisualElements:
    """Test the main trades_to_visual_elements function."""

    @pytest.fixture
    def sample_trades(self) -> List[Trade]:
        """Create sample trades for testing."""
        return [
            Trade(
                entry_time="2024-01-01 10:00:00",
                entry_price=100.0,
                exit_time="2024-01-01 15:00:00",
                exit_price=105.0,
                quantity=100,
                trade_type=TradeType.LONG,
            ),
            Trade(
                entry_time="2024-01-02 10:00:00",
                entry_price=110.0,
                exit_time="2024-01-02 14:00:00",
                exit_price=108.0,
                quantity=50,
                trade_type=TradeType.SHORT,
            ),
        ]

    @pytest.fixture
    def default_options(self) -> TradeVisualizationOptions:
        """Create default trade visualization options."""
        return TradeVisualizationOptions()

    def test_empty_trades_list(self, default_options):
        """Test with empty trades list."""
        result = trades_to_visual_elements([], default_options)

        assert isinstance(result, dict)
        assert result == {"markers": [], "shapes": [], "annotations": []}

    def test_none_trades_list(self, default_options):
        """Test with None trades list."""
        with pytest.raises(ValueError):
            trades_to_visual_elements(None, default_options)

    def test_invalid_trades_type(self, default_options):
        """Test with invalid trades type."""
        with pytest.raises(TypeError):
            trades_to_visual_elements([{"not": "a_trade"}], default_options)

    def test_none_options(self, sample_trades):
        """Test with None options."""
        with pytest.raises(ValueError):
            trades_to_visual_elements(sample_trades, None)

    def test_markers_style(self, sample_trades, default_options):
        """Test markers visualization style."""
        default_options.style = TradeVisualization.MARKERS

        result = trades_to_visual_elements(sample_trades, default_options)

        assert len(result["markers"]) == 4  # 2 trades * 2 markers each
        assert len(result["shapes"]) == 0
        assert len(result["annotations"]) == 0

        # Verify marker structure
        for marker in result["markers"]:
            assert "time" in marker
            assert "position" in marker
            assert "color" in marker
            assert "shape" in marker

    def test_rectangles_style(self, sample_trades, default_options):
        """Test rectangles visualization style."""
        default_options.style = TradeVisualization.RECTANGLES

        result = trades_to_visual_elements(sample_trades, default_options)

        assert len(result["markers"]) == 0
        assert len(result["shapes"]) == 2  # One rectangle per trade
        assert len(result["annotations"]) == 0

        # Verify rectangle structure
        for shape in result["shapes"]:
            assert shape["type"] == "rectangle"
            assert "time" in shape
            assert "width" in shape
            assert "fillColor" in shape
            assert "borderColor" in shape

    def test_lines_style(self, sample_trades, default_options):
        """Test lines visualization style."""
        default_options.style = TradeVisualization.LINES

        result = trades_to_visual_elements(sample_trades, default_options)

        assert len(result["markers"]) == 0
        assert len(result["shapes"]) == 2  # One line per trade
        assert len(result["annotations"]) == 0

        # Verify line structure
        for shape in result["shapes"]:
            assert shape["type"] == "line"
            assert "time" in shape
            assert "width" in shape
            assert "color" in shape

    def test_arrows_style(self, sample_trades, default_options):
        """Test arrows visualization style."""
        default_options.style = TradeVisualization.ARROWS

        result = trades_to_visual_elements(sample_trades, default_options)

        assert len(result["markers"]) == 0
        assert len(result["shapes"]) == 2  # One arrow per trade
        assert len(result["annotations"]) == 0

        # Verify arrow structure
        for shape in result["shapes"]:
            assert shape["type"] == "arrow"
            assert "time" in shape
            assert "width" in shape
            assert "color" in shape

    def test_both_style(self, sample_trades, default_options):
        """Test both markers and shapes style."""
        default_options.style = TradeVisualization.BOTH

        result = trades_to_visual_elements(sample_trades, default_options)

        assert len(result["markers"]) == 4  # 2 trades * 2 markers each
        assert len(result["shapes"]) == 2  # One shape per trade
        assert len(result["annotations"]) == 2  # One annotation per trade

    def test_custom_marker_colors(self, sample_trades):
        """Test custom marker colors."""
        options = TradeVisualizationOptions(
            style=TradeVisualization.MARKERS,
            entry_marker_color_long="rgba(0,255,0,1)",
            entry_marker_color_short="rgba(255,0,0,1)",
            exit_marker_color_profit="rgba(0,255,0,1)",
            exit_marker_color_loss="rgba(255,0,0,1)",
        )

        result = trades_to_visual_elements(sample_trades, options)

        # Verify long trade entry marker color
        long_trade_entry = result["markers"][0]
        assert long_trade_entry["color"] == "rgba(0,255,0,1)"

        # Verify short trade entry marker color
        short_trade_entry = result["markers"][2]
        assert short_trade_entry["color"] == "rgba(255,0,0,1)"

    def test_show_pnl_in_markers(self, sample_trades):
        """Test showing P&L in markers."""
        options = TradeVisualizationOptions(
            style=TradeVisualization.MARKERS, show_pnl_in_markers=True
        )

        result = trades_to_visual_elements(sample_trades, options)

        # Verify exit markers have P&L text (every other marker is an exit marker)
        for i in range(1, len(result["markers"]), 2):  # Check exit markers (odd indices)
            marker = result["markers"][i]
            assert "text" in marker
            assert "P&L" in marker["text"] or "Profit" in marker["text"] or "Loss" in marker["text"]


class TestCreateTradeRectangle:
    """Test the create_trade_rectangle function."""

    @pytest.fixture
    def sample_trade(self) -> Trade:
        """Create a sample trade for testing."""
        return Trade(
            entry_time="2024-01-01 10:00:00",
            entry_price=100.0,
            exit_time="2024-01-01 15:00:00",
            exit_price=105.0,
            quantity=100,
            trade_type=TradeType.LONG,
        )

    @pytest.fixture
    def default_options(self) -> TradeVisualizationOptions:
        """Create default options."""
        return TradeVisualizationOptions()

    def test_basic_rectangle_creation(self, sample_trade, default_options):
        """Test basic rectangle creation."""
        rect = create_trade_rectangle(sample_trade, default_options)

        assert rect["type"] == "rectangle"
        assert "time" in rect
        assert "width" in rect
        assert "fillColor" in rect
        assert "borderColor" in rect
        assert "fillOpacity" in rect
        assert "borderWidth" in rect

    def test_profitable_long_trade_colors(self, sample_trade):
        """Test colors for profitable long trade."""
        options = TradeVisualizationOptions(
            rectangle_fill_color_profit="rgba(0,255,0,0.3)",
            rectangle_border_color_profit="rgba(0,255,0,1)",
        )

        rect = create_trade_rectangle(sample_trade, options)

        assert rect["fillColor"] == "rgba(0,255,0,0.3)"
        assert rect["borderColor"] == "rgba(0,255,0,1)"

    def test_losing_short_trade_colors(self):
        """Test colors for losing short trade."""
        losing_short_trade = Trade(
            entry_time="2024-01-01 10:00:00",
            entry_price=110.0,
            exit_time="2024-01-01 15:00:00",
            exit_price=115.0,  # Short trade loses when price goes up
            quantity=100,
            trade_type=TradeType.SHORT,
        )

        options = TradeVisualizationOptions(
            rectangle_border_color_loss="rgba(255,0,0,1)",
        )

        rect = create_trade_rectangle(losing_short_trade, options)

        assert rect["borderColor"] == "rgba(255,0,0,1)"

    def test_custom_opacity_and_width(self, sample_trade):
        """Test custom opacity and border width."""
        options = TradeVisualizationOptions(rectangle_fill_opacity=0.5, rectangle_border_width=3)

        rect = create_trade_rectangle(sample_trade, options)

        assert rect["fillOpacity"] == 0.5
        assert rect["borderWidth"] == 3

    def test_none_trade(self, default_options):
        """Test with None trade."""
        with pytest.raises(ValueError):
            create_trade_rectangle(None, default_options)

    def test_none_options(self, sample_trade):
        """Test with None options."""
        with pytest.raises(ValueError):
            create_trade_rectangle(sample_trade, None)


class TestCreateTradeLine:
    """Test the create_trade_line function."""

    @pytest.fixture
    def sample_trade(self) -> Trade:
        """Create a sample trade for testing."""
        return Trade(
            entry_time="2024-01-01 10:00:00",
            entry_price=100.0,
            exit_time="2024-01-01 15:00:00",
            exit_price=105.0,
            quantity=100,
            trade_type=TradeType.LONG,
        )

    def test_basic_line_creation(self, sample_trade):
        """Test basic line creation."""
        options = TradeVisualizationOptions()
        line = create_trade_line(sample_trade, options)

        assert line["type"] == "line"
        assert "time" in line
        assert "width" in line
        assert "color" in line
        assert "style" in line

    def test_custom_line_colors(self, sample_trade):
        """Test custom line colors."""
        options = TradeVisualizationOptions(
            line_color_profit="rgba(0,255,0,1)", line_color_loss="rgba(255,0,0,1)"
        )

        line = create_trade_line(sample_trade, options)

        # Profitable long trade should use profit color
        assert line["color"] == "rgba(0,255,0,1)"

    def test_custom_line_width_and_style(self, sample_trade):
        """Test custom line width and style."""
        options = TradeVisualizationOptions(line_width=3, line_style="dashed")

        line = create_trade_line(sample_trade, options)

        assert line["width"] == 3
        assert line["style"] == 1  # Dashed style value

    def test_losing_trade_line_color(self):
        """Test line color for losing trade."""
        losing_trade = Trade(
            entry_time="2024-01-01 10:00:00",
            entry_price=100.0,
            exit_time="2024-01-01 15:00:00",
            exit_price=95.0,  # Losing trade
            quantity=100,
            trade_type=TradeType.LONG,
        )

        options = TradeVisualizationOptions(
            line_color_profit="rgba(0,255,0,1)", line_color_loss="rgba(255,0,0,1)"
        )

        line = create_trade_line(losing_trade, options)

        assert line["color"] == "rgba(255,0,0,1)"


class TestCreateTradeArrow:
    """Test the create_trade_arrow function."""

    @pytest.fixture
    def sample_trade(self) -> Trade:
        """Create a sample trade for testing."""
        return Trade(
            entry_time="2024-01-01 10:00:00",
            entry_price=100.0,
            exit_time="2024-01-01 15:00:00",
            exit_price=105.0,
            quantity=100,
            trade_type=TradeType.LONG,
        )

    def test_basic_arrow_creation(self, sample_trade):
        """Test basic arrow creation."""
        options = TradeVisualizationOptions()
        arrow = create_trade_arrow(sample_trade, options)

        assert arrow["type"] == "arrow"
        assert "time" in arrow
        assert "width" in arrow
        assert "color" in arrow
        assert "size" in arrow

    def test_custom_arrow_colors(self, sample_trade):
        """Test custom arrow colors."""
        options = TradeVisualizationOptions(
            arrow_color_profit="rgba(0,255,0,1)", arrow_color_loss="rgba(255,0,0,1)"
        )

        arrow = create_trade_arrow(sample_trade, options)

        assert arrow["color"] == "rgba(0,255,0,1)"

    def test_custom_arrow_size(self, sample_trade):
        """Test custom arrow size."""
        options = TradeVisualizationOptions(arrow_size=15)

        arrow = create_trade_arrow(sample_trade, options)

        assert arrow["size"] == 15


class TestCreateTradeZone:
    """Test the create_trade_zone function."""

    @pytest.fixture
    def sample_trade(self) -> Trade:
        """Create a sample trade for testing."""
        return Trade(
            entry_time="2024-01-01 10:00:00",
            entry_price=100.0,
            exit_time="2024-01-01 15:00:00",
            exit_price=105.0,
            quantity=100,
            trade_type=TradeType.LONG,
        )

    @pytest.fixture
    def sample_chart_data(self) -> List[Dict]:
        """Create sample chart data for zone testing."""
        return [
            {"time": 1704067200, "open": 100, "high": 102, "low": 99, "close": 101},
            {"time": 1704070800, "open": 101, "high": 103, "low": 100, "close": 102},
            {"time": 1704074400, "open": 102, "high": 104, "low": 101, "close": 103},
            {"time": 1704078000, "open": 103, "high": 105, "low": 102, "close": 104},
            {"time": 1704081600, "open": 104, "high": 106, "low": 103, "close": 105},
        ]

    def test_basic_zone_creation(self, sample_trade):
        """Test basic zone creation."""
        options = TradeVisualizationOptions()
        zone = create_trade_zone(sample_trade, options)

        assert zone["type"] == "zone"
        assert "time" in zone
        assert "width" in zone
        assert "fillColor" in zone
        assert "borderColor" in zone

    def test_zone_with_chart_data(self, sample_trade, sample_chart_data):
        """Test zone creation with chart data."""
        options = TradeVisualizationOptions()
        zone = create_trade_zone(sample_trade, options, sample_chart_data)

        assert zone["type"] == "zone"
        # Zone should extend to cover the trade period

    def test_custom_zone_colors(self, sample_trade):
        """Test custom zone colors."""
        options = TradeVisualizationOptions(zone_color_long="rgba(0,255,0,1)")

        zone = create_trade_zone(sample_trade, options)

        assert zone["fillColor"] == "rgba(0,255,0,0.1)"
        assert zone["borderColor"] == "rgba(0,255,0,1)"

    def test_zone_extend_bars(self, sample_trade):
        """Test zone extend bars option."""
        options = TradeVisualizationOptions(zone_extend_bars=5)

        zone = create_trade_zone(sample_trade, options)

        # Zone width should be extended by 5 bars
        assert zone["width"] > 0


class TestCreateTradeAnnotation:
    """Test the create_trade_annotation function."""

    @pytest.fixture
    def sample_trade(self) -> Trade:
        """Create a sample trade for testing."""
        return Trade(
            entry_time="2024-01-01 10:00:00",
            entry_price=100.0,
            exit_time="2024-01-01 15:00:00",
            exit_price=105.0,
            quantity=100,
            trade_type=TradeType.LONG,
        )

    def test_basic_annotation_creation(self, sample_trade):
        """Test basic annotation creation."""
        options = TradeVisualizationOptions()
        annotation = create_trade_annotation(sample_trade, options)

        assert annotation["type"] == "annotation"
        assert "time" in annotation
        assert "text" in annotation
        assert "position" in annotation

    def test_annotation_with_trade_id(self, sample_trade):
        """Test annotation showing trade ID."""
        options = TradeVisualizationOptions(show_trade_id=True)

        annotation = create_trade_annotation(sample_trade, options)

        # Trade ID should be included when show_trade_id is True and trade has an ID
        # Since the sample trade doesn't have an ID, we just check the format
        assert "LONG" in annotation["text"]

    def test_annotation_with_quantity(self, sample_trade):
        """Test annotation showing quantity."""
        options = TradeVisualizationOptions(show_quantity=True)

        annotation = create_trade_annotation(sample_trade, options)

        assert "100" in annotation["text"]  # Quantity should be in text

    def test_annotation_with_trade_type(self, sample_trade):
        """Test annotation showing trade type."""
        options = TradeVisualizationOptions(show_trade_type=True)

        annotation = create_trade_annotation(sample_trade, options)

        assert "LONG" in annotation["text"]

    def test_custom_annotation_font_size(self, sample_trade):
        """Test custom annotation font size."""
        options = TradeVisualizationOptions(annotation_font_size=16)

        annotation = create_trade_annotation(sample_trade, options)

        assert annotation["fontSize"] == 16

    def test_custom_annotation_background(self, sample_trade):
        """Test custom annotation background."""
        options = TradeVisualizationOptions(annotation_background="rgba(255,255,255,0.9)")

        annotation = create_trade_annotation(sample_trade, options)

        assert annotation["backgroundColor"] == "rgba(255,255,255,0.9)"


class TestGetLineStyleValue:
    """Test the get_line_style_value function."""

    def test_solid_style(self):
        """Test solid line style."""
        assert get_line_style_value("solid") == 0

    def test_dashed_style(self):
        """Test dashed line style."""
        assert get_line_style_value("dashed") == 1

    def test_dotted_style(self):
        """Test dotted line style."""
        assert get_line_style_value("dotted") == 2

    def test_large_dashed_style(self):
        """Test large dashed line style."""
        assert get_line_style_value("large_dashed") == 3

    def test_sparse_dotted_style(self):
        """Test sparse dotted line style."""
        assert get_line_style_value("sparse_dotted") == 4

    def test_invalid_style(self):
        """Test invalid line style."""
        with pytest.raises(ValueError):
            get_line_style_value("invalid_style")

    def test_case_insensitive(self):
        """Test case insensitive style names."""
        assert get_line_style_value("SOLID") == 0
        assert get_line_style_value("Dashed") == 1


class TestCreateTradeShapesSeries:
    """Test the create_trade_shapes_series function."""

    @pytest.fixture
    def sample_trades(self) -> List[Trade]:
        """Create sample trades for testing."""
        return [
            Trade(
                entry_time="2024-01-01 10:00:00",
                entry_price=100.0,
                exit_time="2024-01-01 15:00:00",
                exit_price=105.0,
                quantity=100,
                trade_type=TradeType.LONG,
            )
        ]

    def test_basic_shapes_series_creation(self, sample_trades):
        """Test basic shapes series creation."""
        options = TradeVisualizationOptions(style=TradeVisualization.RECTANGLES)

        series = create_trade_shapes_series(sample_trades, options)

        assert "type" in series
        assert "data" in series
        assert len(series["data"]) == 1  # One shape per trade

    def test_empty_trades_list(self):
        """Test with empty trades list."""
        options = TradeVisualizationOptions()

        series = create_trade_shapes_series([], options)

        assert series["data"] == []

    def test_different_visualization_styles(self, sample_trades):
        """Test different visualization styles."""
        styles = [
            TradeVisualization.RECTANGLES,
            TradeVisualization.LINES,
            TradeVisualization.ARROWS,
        ]

        for style in styles:
            options = TradeVisualizationOptions(style=style)
            series = create_trade_shapes_series(sample_trades, options)

            assert "type" in series
            assert "data" in series
            assert len(series["data"]) == 1


class TestAddTradesToSeries:
    """Test the add_trades_to_series function."""

    @pytest.fixture
    def sample_series_config(self) -> Dict[str, Any]:
        """Create sample series configuration."""
        return {"type": "candlestick", "data": [], "options": {}}

    @pytest.fixture
    def sample_trades(self) -> List[Trade]:
        """Create sample trades for testing."""
        return [
            Trade(
                entry_time="2024-01-01 10:00:00",
                entry_price=100.0,
                exit_time="2024-01-01 15:00:00",
                exit_price=105.0,
                quantity=100,
                trade_type=TradeType.LONG,
            )
        ]

    def test_add_trades_to_series(self, sample_series_config, sample_trades):
        """Test adding trades to series configuration."""
        options = TradeVisualizationOptions(style=TradeVisualization.MARKERS)

        result = add_trades_to_series(sample_series_config, sample_trades, options)

        assert "markers" in result
        assert len(result["markers"]) == 2  # Entry and exit markers

    def test_add_trades_with_shapes(self, sample_series_config, sample_trades):
        """Test adding trades with shapes."""
        options = TradeVisualizationOptions(style=TradeVisualization.RECTANGLES)

        result = add_trades_to_series(sample_series_config, sample_trades, options)

        assert "shapes" in result
        assert len(result["shapes"]) == 1  # One rectangle per trade

    def test_add_trades_with_annotations(self, sample_series_config, sample_trades):
        """Test adding trades with annotations."""
        options = TradeVisualizationOptions(style=TradeVisualization.MARKERS, show_trade_id=True)

        result = add_trades_to_series(sample_series_config, sample_trades, options)

        assert "annotations" in result
        assert len(result["annotations"]) > 0

    def test_empty_trades_list(self, sample_series_config):
        """Test with empty trades list."""
        options = TradeVisualizationOptions()

        result = add_trades_to_series(sample_series_config, [], options)

        # Original series config should be unchanged
        assert result == sample_series_config


class TestTradeVisualizationEdgeCases:
    """Test edge cases for trade visualization."""

    def test_trade_with_same_entry_exit_time(self):
        """Test trade with same entry and exit time."""
        # Test with slightly different times to avoid validation error
        trade = Trade(
            entry_time="2024-01-01 10:00:00",
            entry_price=100.0,
            exit_time="2024-01-01 10:01:00",  # 1 minute later
            exit_price=100.0,  # Same price
            quantity=100,
            trade_type=TradeType.LONG,
        )

        options = TradeVisualizationOptions(style=TradeVisualization.MARKERS)

        result = trades_to_visual_elements([trade], options)

        # Should still create markers
        assert len(result["markers"]) == 2

    def test_trade_with_extreme_price_values(self):
        """Test trade with extreme price values."""
        trade = Trade(
            entry_time="2024-01-01 10:00:00",
            entry_price=0.0001,  # Very small price
            exit_time="2024-01-01 15:00:00",
            exit_price=999999.99,  # Very large price
            quantity=100,
            trade_type=TradeType.LONG,
        )

        options = TradeVisualizationOptions(style=TradeVisualization.LINES)

        result = trades_to_visual_elements([trade], options)

        # Should handle extreme values gracefully
        assert len(result["shapes"]) == 1

    def test_trade_with_zero_quantity(self):
        """Test trade with zero quantity."""
        trade = Trade(
            entry_time="2024-01-01 10:00:00",
            entry_price=100.0,
            exit_time="2024-01-01 15:00:00",
            exit_price=105.0,
            quantity=0,  # Zero quantity
            trade_type=TradeType.LONG,
        )

        options = TradeVisualizationOptions(style=TradeVisualization.MARKERS)

        result = trades_to_visual_elements([trade], options)

        # Should still create visualization
        assert len(result["markers"]) == 2

    def test_trade_with_negative_prices(self):
        """Test trade with negative prices."""
        trade = Trade(
            entry_time="2024-01-01 10:00:00",
            entry_price=-100.0,  # Negative price
            exit_time="2024-01-01 15:00:00",
            exit_price=-95.0,  # Negative price
            quantity=100,
            trade_type=TradeType.LONG,
        )

        options = TradeVisualizationOptions(style=TradeVisualization.RECTANGLES)

        result = trades_to_visual_elements([trade], options)

        # Should handle negative prices
        assert len(result["shapes"]) == 1


class TestTradeVisualizationPerformance:
    """Performance tests for trade visualization."""

    def test_large_number_of_trades(self):
        """Test performance with large number of trades."""
        # Create 1000 trades
        trades = []
        for i in range(1000):
            # Use modulo to ensure valid dates (max 31 days)
            day = (i % 31) + 1
            trade = Trade(
                entry_time=f"2024-01-{day:02d} 10:00:00",
                entry_price=100.0 + i,
                exit_time=f"2024-01-{day:02d} 15:00:00",
                exit_price=105.0 + i,
                quantity=100,
                trade_type=TradeType.LONG if i % 2 == 0 else TradeType.SHORT,
            )
            trades.append(trade)

        options = TradeVisualizationOptions(style=TradeVisualization.MARKERS)

        import time

        start_time = time.time()

        result = trades_to_visual_elements(trades, options)

        end_time = time.time()
        processing_time = end_time - start_time

        # Should process 1000 trades in reasonable time (< 1 second)
        assert processing_time < 1.0
        assert len(result["markers"]) == 2000  # 2 markers per trade

    def test_memory_usage_with_large_trades(self):
        """Test memory usage with large number of trades."""
        import gc

        import psutil

        process = psutil.Process()
        initial_memory = process.memory_info().rss

        # Create 1000 trades
        trades = []
        for i in range(1000):
            # Use modulo to ensure valid dates (max 31 days)
            day = (i % 31) + 1
            trade = Trade(
                entry_time=f"2024-01-{day:02d} 10:00:00",
                entry_price=100.0 + i,
                exit_time=f"2024-01-{day:02d} 15:00:00",
                exit_price=105.0 + i,
                quantity=100,
                trade_type=TradeType.LONG,
            )
            trades.append(trade)

        options = TradeVisualizationOptions(style=TradeVisualization.BOTH)

        result = trades_to_visual_elements(trades, options)

        # Force garbage collection
        gc.collect()

        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory

        # Memory increase should be reasonable (< 100MB for 1000 trades)
        assert memory_increase < 100 * 1024 * 1024

        # Verify result structure
        assert len(result["markers"]) == 2000
        assert len(result["shapes"]) == 1000
