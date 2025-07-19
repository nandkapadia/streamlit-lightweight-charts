import pandas as pd

from streamlit_lightweight_charts_pro.charts import SinglePaneChart, MultiPaneChart
from streamlit_lightweight_charts_pro.charts.series import (
    CandlestickSeries,
    HistogramSeries,
    LineSeries,
)


def test_price_volume_chart():
    """Test creating a price-volume chart using the ultra-simplified API."""
    df = pd.DataFrame(
        {
            "datetime": ["2023-01-01", "2023-01-02"],
            "open": [100, 105],
            "high": [110, 115],
            "low": [95, 100],
            "close": [105, 110],
            "volume": [1000, 1500],
        }
    )

    # Create candlestick series for price
    candlestick_series = CandlestickSeries(data=df, up_color="#26a69a", down_color="#ef5350")

    # Create histogram series for volume with explicit column mapping
    volume_df = df[["datetime", "volume"]].copy()
    volume_df = volume_df.rename(columns={"volume": "value"})
    histogram_series = HistogramSeries(
        data=volume_df, 
        color="#2196F3",
        column_mapping={'time': 'datetime', 'value': 'value'}  # Explicit mapping
    )

    # Create multi-pane chart
    chart = MultiPaneChart(
        [SinglePaneChart([candlestick_series]), SinglePaneChart([histogram_series])]
    )

    config = chart.to_frontend_config()
    assert isinstance(config, dict)
    assert "charts" in config
    assert len(config["charts"]) >= 2

    price_chart = config["charts"][0]
    assert "series" in price_chart
    assert any(s["type"] == "Candlestick" for s in price_chart["series"])

    volume_chart = config["charts"][1]
    assert "series" in volume_chart
    assert any(s["type"] == "Histogram" for s in volume_chart["series"])


def test_comparison_chart():
    """Test creating a comparison chart using the ultra-simplified API."""
    # Create DataFrames for comparison
    base_df = pd.DataFrame({"datetime": ["2023-01-01", "2023-01-02"], "close": [100, 110]})
    compare_df = pd.DataFrame({"datetime": ["2023-01-01", "2023-01-02"], "close": [95, 105]})

    # Create line series for each stock
    stock_a_series = LineSeries(data=base_df, color="#FF6B6B", line_width=2)

    stock_b_series = LineSeries(data=compare_df, color="#4ECDC4", line_width=2)

    # Create single pane chart with both series
    chart = SinglePaneChart([stock_a_series, stock_b_series])

    config = chart.to_frontend_config()
    assert "series" in config
    assert len(config["series"]) >= 2


def test_price_volume_chart_with_trades():
    """Test creating a price-volume chart with trade visualization."""
    df = pd.DataFrame(
        {
            "datetime": ["2023-01-01"],
            "open": [100],
            "high": [110],
            "low": [95],
            "close": [105],
            "volume": [1000],
        }
    )

    from streamlit_lightweight_charts_pro.data.trade import (
        Trade,
        TradeType,
        TradeVisualizationOptions,
        TradeVisualization,
    )

    trades = [Trade("2023-01-01", 100.0, "2023-01-02", 105.0, 10, TradeType.LONG)]
    trade_options = TradeVisualizationOptions(style=TradeVisualization.MARKERS)

    # Create candlestick series with trades
    candlestick_series = CandlestickSeries(
        data=df,
        trades=trades,
        trade_visualization_options=trade_options,
        up_color="#26a69a",
        down_color="#ef5350",
    )

    # Create histogram series for volume with explicit column mapping
    volume_df = df[["datetime", "volume"]].copy()
    volume_df = volume_df.rename(columns={"volume": "value"})
    histogram_series = HistogramSeries(
        data=volume_df, 
        color="#2196F3",
        column_mapping={'time': 'datetime', 'value': 'value'}  # Explicit mapping
    )

    # Create multi-pane chart
    chart = MultiPaneChart(
        [SinglePaneChart([candlestick_series]), SinglePaneChart([histogram_series])]
    )

    config = chart.to_frontend_config()
    price_chart = config["charts"][0]
    found_trades = False
    for series in price_chart["series"]:
        # Check for trade-related keys that add_trades_to_series adds
        if any(key in series for key in ["trades", "tradeVisualizationOptions"]):
            found_trades = True
            break
    assert found_trades
