import pandas as pd

from streamlit_lightweight_charts.data.trade import (
    Trade,
    TradeType,
    TradeVisualizationOptions,
)
from streamlit_lightweight_charts.utils.chart_builders import (
    area_chart_from_df,
    candlestick_chart_from_df,
    line_chart_from_df,
)
from streamlit_lightweight_charts.utils.trade_visualization import (
    add_trades_to_series,
    create_trade_shapes_series,
    trades_to_visual_elements,
)


def test_candlestick_chart_from_df():
    df = pd.DataFrame(
        {
            "time": ["2023-01-01", "2023-01-02"],
            "open": [100, 105],
            "high": [110, 115],
            "low": [95, 100],
            "close": [105, 110],
        }
    )
    chart = candlestick_chart_from_df(df)
    assert chart is not None
    config = chart.to_frontend_config()
    assert "series" in config
    assert any(s["type"] == "Candlestick" for s in config["series"])


def test_line_chart_from_df():
    df = pd.DataFrame({"time": ["2023-01-01", "2023-01-02"], "value": [100, 110]})
    chart = line_chart_from_df(df, value_column="value")
    assert chart is not None
    config = chart.to_frontend_config()
    assert "series" in config
    assert any(s["type"] == "Line" for s in config["series"])


def test_area_chart_from_df():
    df = pd.DataFrame({"time": ["2023-01-01", "2023-01-02"], "value": [100, 110]})
    chart = area_chart_from_df(df, value_column="value")
    assert chart is not None
    config = chart.to_frontend_config()
    assert "series" in config
    assert any(s["type"] == "Area" for s in config["series"])


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
