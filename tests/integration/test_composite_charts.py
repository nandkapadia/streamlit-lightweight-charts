import pandas as pd

from streamlit_lightweight_charts.charts import ComparisonChart, PriceVolumeChart


def test_price_volume_chart():
    df = pd.DataFrame(
        {
            "time": ["2023-01-01", "2023-01-02"],
            "open": [100, 105],
            "high": [110, 115],
            "low": [95, 100],
            "close": [105, 110],
            "volume": [1000, 1500],
        }
    )
    chart = PriceVolumeChart(df)
    config = chart.to_frontend_config()
    assert isinstance(config, list)
    assert len(config) >= 2
    price_chart = config[0]
    assert "series" in price_chart
    assert any(s["type"] == "Candlestick" for s in price_chart["series"])
    volume_chart = config[1]
    assert "series" in volume_chart
    assert any(s["type"] == "Histogram" for s in volume_chart["series"])


def test_comparison_chart():
    # Create DataFrames for comparison
    base_df = pd.DataFrame({"time": ["2023-01-01", "2023-01-02"], "close": [100, 110]})
    compare_df = pd.DataFrame({"time": ["2023-01-01", "2023-01-02"], "close": [95, 105]})

    # Pass as (name, DataFrame) tuples
    chart = ComparisonChart([("Stock A", base_df), ("Stock B", compare_df)])
    config = chart.to_frontend_config()
    assert "chart" in config
    assert "series" in config
    assert len(config["series"]) >= 2


def test_price_volume_chart_with_trades():
    df = pd.DataFrame(
        {
            "time": ["2023-01-01"],
            "open": [100],
            "high": [110],
            "low": [95],
            "close": [105],
            "volume": [1000],
        }
    )
    from streamlit_lightweight_charts.data.trade import (
        Trade,
        TradeType,
        TradeVisualizationOptions,
    )

    trades = [Trade("2023-01-01", 100.0, "2023-01-02", 105.0, 10, TradeType.LONG)]
    trade_options = TradeVisualizationOptions(style="markers")

    # Create chart first, then add trades
    chart = PriceVolumeChart(df)
    chart = chart.add_trades(trades, trade_options)

    config = chart.to_frontend_config()
    price_chart = config[0]
    found_trades = False
    for series in price_chart["series"]:
        # Check for trade-related keys that add_trades_to_series adds
        if any(key in series for key in ["markers", "shapes", "annotations"]):
            found_trades = True
            break
    assert found_trades
