from streamlit_lightweight_charts.data.trade import (
    Trade,
    TradeType,
    TradeVisualization,
    TradeVisualizationOptions,
)
from streamlit_lightweight_charts.utils.trade_visualization import (
    trades_to_visual_elements,
)


def test_trade_creation():
    trade = Trade("2023-01-01", 100.0, "2023-01-02", 110.0, 10, TradeType.LONG)
    assert trade.entry_time == "2023-01-01"
    assert trade.exit_time == "2023-01-02"
    assert trade.entry_price == 100.0
    assert trade.exit_price == 110.0
    assert trade.quantity == 10
    assert trade.trade_type == TradeType.LONG


def test_trade_pnl_calculation():
    # Long profitable trade
    long_trade = Trade("2023-01-01", 100.0, "2023-01-02", 110.0, 10, TradeType.LONG)
    assert long_trade.pnl == 100.0  # (110-100) * 10
    assert long_trade.pnl_percentage == 10.0  # (110-100)/100 * 100
    assert long_trade.is_profitable is True

    # Short profitable trade
    short_trade = Trade("2023-01-01", 110.0, "2023-01-02", 100.0, 10, TradeType.SHORT)
    assert short_trade.pnl == 100.0  # (110-100) * 10
    assert short_trade.is_profitable is True

    # Losing trade
    losing_trade = Trade("2023-01-01", 110.0, "2023-01-02", 100.0, 10, TradeType.LONG)
    assert losing_trade.pnl == -100.0
    assert losing_trade.is_profitable is False


def test_trade_serialization():
    trade = Trade("2023-01-01", 100.0, "2023-01-02", 110.0, 10, TradeType.LONG, notes="Test trade")
    trade_dict = trade.to_dict()
    assert trade_dict["entryTime"] == "2023-01-01"
    assert trade_dict["exitTime"] == "2023-01-02"
    assert trade_dict["entryPrice"] == 100.0
    assert trade_dict["exitPrice"] == 110.0
    assert trade_dict["quantity"] == 10
    assert trade_dict["tradeType"] == "long"
    assert trade_dict["notes"] == "Test trade"


def test_trade_visualization_options():
    options = TradeVisualizationOptions(
        style="markers",
        entry_marker_color_long="#00ff00",
        exit_marker_color_profit="#ff0000",
        marker_size=8,
    )
    assert options.style == "markers"
    assert options.entry_marker_color_long == "#00ff00"
    assert options.exit_marker_color_profit == "#ff0000"
    assert options.marker_size == 8


def test_trade_type_enum():
    assert TradeType.LONG.value == "long"
    assert TradeType.SHORT.value == "short"


def test_trade_visualization():
    trade = Trade("2023-01-01", 100.0, "2023-01-02", 110.0, 10, TradeType.LONG)
    options = TradeVisualizationOptions(style=TradeVisualization.MARKERS)
    viz_elements = trades_to_visual_elements([trade], options)
    assert "markers" in viz_elements
    assert len(viz_elements["markers"]) == 2  # Entry and exit markers
