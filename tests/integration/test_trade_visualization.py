from streamlit_lightweight_charts.charts import CandlestickChart
from streamlit_lightweight_charts.data.models import OhlcData
from streamlit_lightweight_charts.data.trade import (
    Trade,
    TradeType,
    TradeVisualizationOptions,
)


def test_candlestick_chart_with_trades():
    ohlc = [
        OhlcData("2023-01-01", 1, 2, 0, 1.5),
        OhlcData("2023-01-02", 1.5, 2.5, 1, 2),
    ]
    trades = [Trade("2023-01-01", 1.1, "2023-01-02", 1.9, 10, TradeType.LONG)]
    chart = CandlestickChart(
        ohlc, trades=trades, trade_visualization_options=TradeVisualizationOptions()
    )
    config = chart.to_frontend_config()
    assert "series" in config
    found_trade = False
    for s in config["series"]:
        # Check for trade-related keys that add_trades_to_series adds
        if any(key in s for key in ["markers", "shapes", "annotations"]):
            found_trade = True
    assert found_trade
