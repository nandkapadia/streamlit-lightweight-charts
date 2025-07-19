import pandas as pd

from streamlit_lightweight_charts_pro.data.trade import (
    Trade,
    TradeType,
    TradeVisualizationOptions,
)
from streamlit_lightweight_charts_pro.utils.trade_visualization import (
    add_trades_to_series,
    create_trade_shapes_series,
    trades_to_visual_elements,
)


def test_trades_to_visual_elements():
    trades = [Trade("2023-01-01", 100, "2023-01-02", 110, 10, TradeType.LONG)]
    options = TradeVisualizationOptions(style="markers")

    elements = trades_to_visual_elements(trades, options)
    assert isinstance(elements, dict)
    assert "markers" in elements
    assert "shapes" in elements
    assert "annotations" in elements
    assert len(elements["markers"]) > 0  # Should have entry and exit markers


def test_create_trade_shapes_series():
    trades = [Trade("2023-01-01", 100, "2023-01-02", 110, 10, TradeType.LONG)]
    options = TradeVisualizationOptions(style="rectangles")

    series = create_trade_shapes_series(trades, options)
    assert isinstance(series, dict)
    assert "data" in series


def test_add_trades_to_series():
    series_config = {
        "type": "Candlestick",
        "data": [{"time": "2023-01-01", "open": 100, "high": 110, "low": 95, "close": 105}],
    }
    trades = [Trade("2023-01-01", 100, "2023-01-02", 110, 10, TradeType.LONG)]
    options = TradeVisualizationOptions(style="markers")

    result = add_trades_to_series(series_config, trades, options)
    assert isinstance(result, dict)
    # Should have trade-related elements added
    assert "trades" in result or "tradeVisualElements" in result or "markers" in result
