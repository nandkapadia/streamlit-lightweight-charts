from streamlit_lightweight_charts_pro.charts import Chart
from streamlit_lightweight_charts_pro.charts.series import CandlestickSeries
from streamlit_lightweight_charts_pro.data import OhlcData
from streamlit_lightweight_charts_pro.data.trade import (
    Trade,
    TradeType,
    TradeVisualizationOptions,
)


def test_candlestick_chart_with_trades():
    """Test candlestick chart with trade visualization using ultra-simplified API."""
    ohlc = [
        OhlcData("2023-01-01", 1, 2, 0, 1.5),
        OhlcData("2023-01-02", 1.5, 2.5, 1, 2),
    ]
    trades = [Trade("2023-01-01", 1.1, "2023-01-02", 1.9, 10, TradeType.LONG)]

    from streamlit_lightweight_charts_pro.data.trade import TradeVisualization

    # Create candlestick series with trades
    candlestick_series = CandlestickSeries(
        data=ohlc,
        trades=trades,
        trade_visualization_options=TradeVisualizationOptions(style=TradeVisualization.MARKERS),
        up_color="#26a69a",
        down_color="#ef5350",
    )

    # Create single pane chart
    chart = Chart([candlestick_series])

    config = chart.to_frontend_config()
    # The Chart returns a structure with "charts" array containing the chart config
    assert "charts" in config
    assert len(config["charts"]) == 1

    chart_config = config["charts"][0]
    assert "series" in chart_config
    found_trade = False
    for s in chart_config["series"]:
        # Check for trade-related keys that add_trades_to_series adds
        if any(key in s for key in ["markers", "shapes", "annotations"]):
            found_trade = True
            break
    assert found_trade
