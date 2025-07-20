"""Extended tests for trade visualization utilities to improve coverage."""

from streamlit_lightweight_charts_pro.data import (
    Trade,
    TradeType,
    TradeVisualization,
    TradeVisualizationOptions,
)
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


class TestTradeVisualizationExtended:
    """Extended test cases for trade visualization functionality."""

    def setup_method(self):
        """Set up test data."""
        self.sample_trades = [
            Trade(
                entry_time="2024-01-01T10:00:00",
                entry_price=100.0,
                trade_type=TradeType.LONG,
                exit_time="2024-01-01T14:00:00",
                exit_price=105.0,
                quantity=100,
            ),
            Trade(
                entry_time="2024-01-02T09:00:00",
                entry_price=102.0,
                trade_type=TradeType.SHORT,
                exit_time="2024-01-02T15:00:00",
                exit_price=98.0,
                quantity=50,
            ),
        ]
        
        self.options = TradeVisualizationOptions(
            style=TradeVisualization.BOTH,
            show_pnl_in_markers=True,
            show_trade_id=True,
            show_quantity=True,
            show_trade_type=True,
        )

    def test_trades_to_visual_elements_markers_only(self):
        """Test trades_to_visual_elements with markers only style."""
        options = TradeVisualizationOptions(style=TradeVisualization.MARKERS)
        
        result = trades_to_visual_elements(self.sample_trades, options)
        
        assert "markers" in result
        assert "shapes" in result
        assert "annotations" in result
        assert len(result["markers"]) > 0
        assert len(result["shapes"]) == 0
        # Annotations are created when any annotation option is enabled (default is True)
        assert len(result["annotations"]) == 2

    def test_trades_to_visual_elements_rectangles_only(self):
        """Test trades_to_visual_elements with rectangles only style."""
        options = TradeVisualizationOptions(style=TradeVisualization.RECTANGLES)
        
        result = trades_to_visual_elements(self.sample_trades, options)
        
        assert len(result["shapes"]) == 2
        assert all(shape["type"] == "rectangle" for shape in result["shapes"])

    def test_trades_to_visual_elements_lines_only(self):
        """Test trades_to_visual_elements with lines only style."""
        options = TradeVisualizationOptions(style=TradeVisualization.LINES)
        
        result = trades_to_visual_elements(self.sample_trades, options)
        
        assert len(result["shapes"]) == 2
        assert all(shape["type"] == "trendLine" for shape in result["shapes"])

    def test_trades_to_visual_elements_arrows_only(self):
        """Test trades_to_visual_elements with arrows only style."""
        options = TradeVisualizationOptions(style=TradeVisualization.ARROWS)
        
        result = trades_to_visual_elements(self.sample_trades, options)
        
        assert len(result["shapes"]) == 2
        assert all(shape["type"] == "arrow" for shape in result["shapes"])

    def test_trades_to_visual_elements_zones_only(self):
        """Test trades_to_visual_elements with zones only style."""
        options = TradeVisualizationOptions(style=TradeVisualization.ZONES)
        chart_data = [{"time": "2024-01-01T10:00:00", "value": 100}]
        
        result = trades_to_visual_elements(self.sample_trades, options, chart_data)
        
        assert len(result["shapes"]) == 2
        # Zones are actually rectangles with transparent borders
        assert all(shape["type"] == "rectangle" for shape in result["shapes"])

    def test_trades_to_visual_elements_with_annotations(self):
        """Test trades_to_visual_elements with annotation options enabled."""
        options = TradeVisualizationOptions(
            style=TradeVisualization.MARKERS,
            show_trade_id=True,
            show_quantity=True,
            show_trade_type=True,
        )
        
        result = trades_to_visual_elements(self.sample_trades, options)
        
        assert len(result["annotations"]) == 2
        for annotation in result["annotations"]:
            assert "text" in annotation
            assert "time" in annotation

    def test_create_trade_rectangle_profitable_trade(self):
        """Test create_trade_rectangle with profitable trade."""
        trade = self.sample_trades[0]  # Profitable long trade
        options = TradeVisualizationOptions(
            rectangle_color_profit="#26a69a",
            rectangle_color_loss="#ef5350",
            rectangle_fill_opacity=0.3,
            rectangle_border_width=2,
        )
        
        result = create_trade_rectangle(trade, options)
        
        assert result["type"] == "rectangle"
        assert result["time1"] == trade.entry_timestamp
        assert result["time2"] == trade.exit_timestamp
        assert result["price1"] == trade.entry_price
        assert result["price2"] == trade.exit_price
        # The actual implementation uses int() for opacity conversion, 
        # so 0.3 * 255 = 76.5 -> 76 -> 4c
        assert result["fillColor"] == "#26a69a4c"  # Color with opacity
        assert result["borderColor"] == "#26a69a"
        assert result["borderWidth"] == 2

    def test_create_trade_rectangle_loss_trade(self):
        """Test create_trade_rectangle with loss trade."""
        trade = self.sample_trades[1]  # Profitable short trade (loss for long)
        options = TradeVisualizationOptions(
            rectangle_color_profit="#26a69a",
            rectangle_color_loss="#ef5350",
            rectangle_fill_opacity=0.5,
            rectangle_border_width=1,
        )
        
        result = create_trade_rectangle(trade, options)
        
        # Short trade is profitable, so it uses profit color
        assert result["borderColor"] == "#26a69a"
        # The actual implementation uses int() for opacity conversion, 
        # so 0.5 * 255 = 127.5 -> 127 -> 7f
        assert result["fillColor"] == "#26a69a7f"  # Color with opacity

    def test_create_trade_line_profitable_trade(self):
        """Test create_trade_line with profitable trade."""
        trade = self.sample_trades[0]
        options = TradeVisualizationOptions(
            line_color_profit="#26a69a",
            line_color_loss="#ef5350",
            line_width=3,
            line_style="dashed",
        )
        
        result = create_trade_line(trade, options)
        
        assert result["type"] == "trendLine"
        assert result["time1"] == trade.entry_timestamp
        assert result["time2"] == trade.exit_timestamp
        assert result["price1"] == trade.entry_price
        assert result["price2"] == trade.exit_price
        assert result["lineColor"] == "#26a69a"
        assert result["lineWidth"] == 3
        # The actual implementation maps "dashed" to 2, not 1
        assert result["lineStyle"] == 2  # Dashed style

    def test_create_trade_arrow_with_pnl(self):
        """Test create_trade_arrow with PnL text."""
        trade = self.sample_trades[0]
        options = TradeVisualizationOptions(
            arrow_color_profit="#26a69a", arrow_color_loss="#ef5350", arrow_size=10, line_width=2
        )
        
        result = create_trade_arrow(trade, options)
        
        assert result["type"] == "arrow"
        assert result["lineColor"] == "#26a69a"
        assert result["arrowSize"] == 10
        assert result["text"] == "+5.0%"
        assert result["lineWidth"] == 2

    def test_create_trade_zone_with_chart_data(self):
        """Test create_trade_zone with chart data for extension."""
        trade = self.sample_trades[0]
        options = TradeVisualizationOptions(
            zone_color_long="#26a69a", zone_color_short="#ef5350", zone_extend_bars=5
        )
        chart_data = [
            {"time": "2024-01-01T09:00:00", "value": 99},
            {"time": "2024-01-01T10:00:00", "value": 100},
            {"time": "2024-01-01T11:00:00", "value": 101},
            {"time": "2024-01-01T12:00:00", "value": 102},
            {"time": "2024-01-01T13:00:00", "value": 103},
            {"time": "2024-01-01T14:00:00", "value": 105},
            {"time": "2024-01-01T15:00:00", "value": 106},
        ]
        
        result = create_trade_zone(trade, options, chart_data)
        
        # Zones are actually rectangles with transparent borders
        assert result["type"] == "rectangle"
        # Zones use borderColor, not lineColor
        assert result["borderColor"] == "transparent"
        assert "time1" in result
        assert "time2" in result

    def test_create_trade_zone_without_chart_data(self):
        """Test create_trade_zone without chart data."""
        trade = self.sample_trades[0]
        options = TradeVisualizationOptions(zone_color_long="#26a69a", zone_color_short="#ef5350")
        
        result = create_trade_zone(trade, options)
        
        # Zones are actually rectangles with transparent borders
        assert result["type"] == "rectangle"
        assert result["time1"] == trade.entry_timestamp
        assert result["time2"] == trade.exit_timestamp

    def test_create_trade_annotation_with_all_options(self):
        """Test create_trade_annotation with all annotation options enabled."""
        trade = self.sample_trades[0]
        options = TradeVisualizationOptions(
            show_trade_id=True, show_quantity=True, show_trade_type=True, annotation_font_size=12
        )
        
        result = create_trade_annotation(trade, options)
        
        assert result["type"] == "text"
        # Annotation is positioned at midpoint between entry and exit
        expected_mid_time = (trade.entry_timestamp + trade.exit_timestamp) / 2
        assert result["time"] == expected_mid_time
        assert result["text"] is not None
        assert "LONG" in result["text"]
        assert "100" in result["text"]  # Quantity
        # The actual implementation uses "#000000" as default color
        assert result["color"] == "#000000"
        assert result["fontSize"] == 12

    def test_create_trade_annotation_partial_options(self):
        """Test create_trade_annotation with partial annotation options."""
        trade = self.sample_trades[0]
        options = TradeVisualizationOptions(
            show_trade_id=False, show_quantity=True, show_trade_type=False
        )
        
        result = create_trade_annotation(trade, options)
        
        assert result["type"] == "text"
        assert "100" in result["text"]  # Quantity
        assert "LONG" not in result["text"]  # Trade type disabled

    def test_get_line_style_value_solid(self):
        """Test get_line_style_value with solid style."""
        result = get_line_style_value("solid")
        assert result == 0

    def test_get_line_style_value_dashed(self):
        """Test get_line_style_value with dashed style."""
        result = get_line_style_value("dashed")
        # The actual implementation maps "dashed" to 2, not 1
        assert result == 2

    def test_get_line_style_value_dotted(self):
        """Test get_line_style_value with dotted style."""
        result = get_line_style_value("dotted")
        # The actual implementation maps "dotted" to 1, not 2
        assert result == 1

    def test_get_line_style_value_large_dashed(self):
        """Test get_line_style_value with large-dashed style."""
        result = get_line_style_value("large_dashed")
        # The actual implementation maps "large_dashed" to 3
        assert result == 3

    def test_get_line_style_value_sparse_dotted(self):
        """Test get_line_style_value with sparse-dotted style."""
        result = get_line_style_value("sparse_dotted")
        # The actual implementation maps "sparse_dotted" to 4
        assert result == 4

    def test_get_line_style_value_invalid(self):
        """Test get_line_style_value with invalid style."""
        result = get_line_style_value("invalid")
        # The actual implementation defaults to 2 (dashed), not 0
        assert result == 2

    def test_create_trade_shapes_series(self):
        """Test create_trade_shapes_series function."""
        options = TradeVisualizationOptions(style=TradeVisualization.RECTANGLES)
        
        result = create_trade_shapes_series(self.sample_trades, options)
        
        assert "type" in result
        # The actual implementation uses "Custom" type, not "shapes"
        assert result["type"] == "Custom"
        assert "data" in result
        assert len(result["data"]) == 0  # No data points, just shapes

    def test_add_trades_to_series(self):
        """Test add_trades_to_series function."""
        series_config = {"type": "line", "data": []}
        options = TradeVisualizationOptions(style=TradeVisualization.MARKERS)
        
        result = add_trades_to_series(series_config, self.sample_trades, options)
        
        assert result["type"] == "line"
        assert "markers" in result
        assert len(result["markers"]) > 0

    def test_trades_to_visual_elements_empty_trades(self):
        """Test trades_to_visual_elements with empty trades list."""
        result = trades_to_visual_elements([], self.options)
        
        assert result["markers"] == []
        assert result["shapes"] == []
        assert result["annotations"] == []

    def test_trades_to_visual_elements_none_chart_data(self):
        """Test trades_to_visual_elements with None chart_data."""
        options = TradeVisualizationOptions(style=TradeVisualization.ZONES)
        
        result = trades_to_visual_elements(self.sample_trades, options, None)
        
        assert len(result["shapes"]) == 2
        # Zones are actually rectangles with transparent borders
        assert all(shape["type"] == "rectangle" for shape in result["shapes"])

    def test_create_trade_annotation_no_options(self):
        """Test create_trade_annotation with no annotation options enabled."""
        trade = self.sample_trades[0]
        options = TradeVisualizationOptions(
            show_trade_id=False, show_quantity=False, show_trade_type=False
        )
        
        result = create_trade_annotation(trade, options)
        
        assert result["type"] == "text"
        # The actual implementation always includes P&L, even when no other options are enabled
        assert "P&L: +5.0%" in result["text"]
