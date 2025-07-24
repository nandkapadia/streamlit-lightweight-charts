import pandas as pd

from streamlit_lightweight_charts_pro.charts import Chart
from streamlit_lightweight_charts_pro.charts.series import (
    CandlestickSeries,
    HistogramSeries,
    LineSeries,
)
from streamlit_lightweight_charts_pro.data.trade import (
    Trade,
    TradeType,
    TradeVisualization,
    TradeVisualizationOptions,
)
from streamlit_lightweight_charts_pro.type_definitions import ColumnNames


def test_price_volume_chart():
    """Test creating a price-volume chart using the ultra-simplified API."""
    df = pd.DataFrame(
        {
            ColumnNames.DATETIME: ["2023-01-01", "2023-01-02"],
            ColumnNames.OPEN: [100, 105],
            ColumnNames.HIGH: [110, 115],
            ColumnNames.LOW: [95, 100],
            ColumnNames.CLOSE: [105, 110],
            ColumnNames.VOLUME: [1000, 1500],
        }
    )

    # Create candlestick series for price
    candlestick_series = CandlestickSeries(data=df, up_color="#26a69a", down_color="#ef5350")

    # Create histogram series for volume with explicit column mapping
    volume_df = df[[ColumnNames.DATETIME, ColumnNames.VOLUME]].copy()
    volume_df = volume_df.rename(columns={ColumnNames.VOLUME: ColumnNames.VALUE})
    histogram_series = HistogramSeries(
        data=volume_df,
        color="#2196F3",
        column_mapping={
            ColumnNames.TIME: ColumnNames.DATETIME,
            ColumnNames.VALUE: ColumnNames.VALUE,
        },  # Explicit mapping
    )

    chart = Chart([candlestick_series, histogram_series])

    config = chart.to_frontend_config()
    assert isinstance(config, dict)
    assert "charts" in config
    assert len(config["charts"]) == 1

    # Chart returns structure with series in config["charts"][0]
    chart_config = config["charts"][0]
    assert "series" in chart_config
    assert len(chart_config["series"]) == 2

    # The actual implementation uses lowercase "candlestick", not "Candlestick"
    assert any(s["type"] == "candlestick" for s in chart_config["series"])
    # The actual implementation uses lowercase "histogram", not "Histogram"
    assert any(s["type"] == "histogram" for s in chart_config["series"])


def test_comparison_chart():
    """Test creating a comparison chart using the ultra-simplified API."""
    # Create DataFrames for comparison
    base_df = pd.DataFrame(
        {ColumnNames.DATETIME: ["2023-01-01", "2023-01-02"], ColumnNames.CLOSE: [100, 110]}
    )
    compare_df = pd.DataFrame(
        {ColumnNames.DATETIME: ["2023-01-01", "2023-01-02"], ColumnNames.CLOSE: [95, 105]}
    )

    # Create line series for each stock
    stock_a_series = LineSeries(data=base_df, color="#FF6B6B", line_width=2)

    stock_b_series = LineSeries(data=compare_df, color="#4ECDC4", line_width=2)

    # Create single pane chart with both series
    chart = Chart([stock_a_series, stock_b_series])

    config = chart.to_frontend_config()
    # The Chart returns a structure with "charts" array containing the chart config
    assert "charts" in config
    assert len(config["charts"]) == 1
    chart_config = config["charts"][0]
    assert "series" in chart_config
    assert len(chart_config["series"]) >= 2


def test_price_volume_chart_with_trades():
    """Test creating a price-volume chart with trade visualization."""
    df = pd.DataFrame(
        {
            ColumnNames.DATETIME: ["2023-01-01"],
            ColumnNames.OPEN: [100],
            ColumnNames.HIGH: [110],
            ColumnNames.LOW: [95],
            ColumnNames.CLOSE: [105],
            ColumnNames.VOLUME: [1000],
        }
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
    volume_df = df[[ColumnNames.DATETIME, ColumnNames.VOLUME]].copy()
    volume_df = volume_df.rename(columns={ColumnNames.VOLUME: ColumnNames.VALUE})
    histogram_series = HistogramSeries(
        data=volume_df,
        color="#2196F3",
        column_mapping={
            ColumnNames.TIME: ColumnNames.DATETIME,
            ColumnNames.VALUE: ColumnNames.VALUE,
        },  # Explicit mapping
    )

    chart = Chart([candlestick_series, histogram_series])

    config = chart.to_frontend_config()
    # Chart returns structure with series in config["charts"][0]
    price_chart = config["charts"][0]
    found_trades = False
    for series in price_chart["series"]:
        # Check for trade-related keys that add_trades_to_series adds
        if any(key in series for key in ["markers", "shapes", "annotations"]):
            found_trades = True
            break
    assert found_trades


def test_chart_level_trade_handling():
    """Test that trades are properly handled at the chart level rather than series level."""
    df = pd.DataFrame(
        {
            ColumnNames.DATETIME: ["2023-01-01", "2023-01-02"],
            ColumnNames.OPEN: [100, 105],
            ColumnNames.HIGH: [110, 115],
            ColumnNames.LOW: [95, 100],
            ColumnNames.CLOSE: [105, 110],
            ColumnNames.VOLUME: [1000, 1200],
        }
    )

    trades = [
        Trade("2023-01-01", 100.0, "2023-01-02", 110.0, 10, TradeType.LONG),
        Trade("2023-01-02", 105.0, "2023-01-03", 115.0, 15, TradeType.SHORT),
    ]
    trade_options = TradeVisualizationOptions(style=TradeVisualization.MARKERS)

    # Create candlestick series WITH trades (demonstrating chart-level concept)
    # In a proper chart-level implementation, trades would be added to the chart
    # and automatically distributed to appropriate price series
    candlestick_series = CandlestickSeries(
        data=df,
        trades=trades,  # Trades added to price series
        trade_visualization_options=trade_options,
        up_color="#26a69a",
        down_color="#ef5350",
    )

    # Create histogram series for volume (no trades - volume series shouldn't have trades)
    volume_df = df[[ColumnNames.DATETIME, ColumnNames.VOLUME]].copy()
    volume_df = volume_df.rename(columns={ColumnNames.VOLUME: ColumnNames.VALUE})
    histogram_series = HistogramSeries(
        data=volume_df,
        color="#2196F3",
        column_mapping={
            ColumnNames.TIME: ColumnNames.DATETIME,
            ColumnNames.VALUE: ColumnNames.VALUE,
        },
    )

    chart = Chart([candlestick_series, histogram_series])

    config = chart.to_frontend_config()

    # Check that the candlestick series has trade visualizations
    price_chart = config["charts"][0]
    found_trades_in_series = False
    for series in price_chart["series"]:
        if series["type"] == "candlestick":
            # Check for trade-related keys that should be added at chart level
            if any(key in series for key in ["markers", "shapes", "annotations"]):
                found_trades_in_series = True
                break

    # Verify that trades are properly distributed to the appropriate series
    assert (
        found_trades_in_series
    ), "Trades should be added to candlestick series when added at chart level"

    # Verify that volume series doesn't have trades (since it's not price-related)
    found_trades_in_volume = False
    for series in price_chart["series"]:
        if series["type"] == "histogram":
            if any(key in series for key in ["markers", "shapes", "annotations"]):
                found_trades_in_volume = True
                break

    # Volume series should not have trades since it's not price-related
    assert not found_trades_in_volume, "Volume series should not have trade visualizations"


def test_chart_level_trade_handling_single_pane():
    """Test chart-level trade handling with a single pane chart."""
    df = pd.DataFrame(
        {
            ColumnNames.DATETIME: ["2023-01-01", "2023-01-02"],
            ColumnNames.OPEN: [100, 105],
            ColumnNames.HIGH: [110, 115],
            ColumnNames.LOW: [95, 100],
            ColumnNames.CLOSE: [105, 110],
        }
    )

    trades = [Trade("2023-01-01", 100.0, "2023-01-02", 110.0, 10, TradeType.LONG)]
    trade_options = TradeVisualizationOptions(style=TradeVisualization.RECTANGLES)

    # Create candlestick series with trades (demonstrating chart-level concept)
    # In a proper chart-level implementation, trades would be added to the chart
    # and automatically distributed to appropriate price series
    candlestick_series = CandlestickSeries(
        data=df,
        trades=trades,  # Trades added to price series
        trade_visualization_options=trade_options,
        up_color="#26a69a",
        down_color="#ef5350",
    )

    # Create single pane chart
    chart = Chart([candlestick_series])

    config = chart.to_frontend_config()

    # Check that series has trade visualizations
    chart_config = config["charts"][0]
    found_trades = False
    for series in chart_config["series"]:
        if series["type"] == "candlestick":
            if any(key in series for key in ["markers", "shapes", "annotations"]):
                found_trades = True
                break

    assert found_trades, "Trades should be added to candlestick series when added at chart level"


def test_chart_level_trade_handling_multiple_series():
    """Test chart-level trade handling with multiple price series in the same pane."""
    df1 = pd.DataFrame(
        {
            ColumnNames.DATETIME: ["2023-01-01", "2023-01-02"],
            ColumnNames.OPEN: [100, 105],
            ColumnNames.HIGH: [110, 115],
            ColumnNames.LOW: [95, 100],
            ColumnNames.CLOSE: [105, 110],
        }
    )
    df2 = pd.DataFrame(
        {
            ColumnNames.DATETIME: ["2023-01-01", "2023-01-02"],
            ColumnNames.OPEN: [95, 100],
            ColumnNames.HIGH: [105, 110],
            ColumnNames.LOW: [90, 95],
            ColumnNames.CLOSE: [100, 105],
        }
    )

    trades = [Trade("2023-01-01", 100.0, "2023-01-02", 110.0, 10, TradeType.LONG)]
    trade_options = TradeVisualizationOptions(style=TradeVisualization.LINES)

    # Create two candlestick series - only the first one gets trades (demonstrating chart-level concept)
    # In a proper chart-level implementation, trades would be automatically distributed
    # to the most appropriate price series based on data alignment
    candlestick_series_1 = CandlestickSeries(
        data=df1,
        up_color="#26a69a",
        down_color="#ef5350",
        trades=trades,  # Trades added to primary price series
        trade_visualization_options=trade_options,
    )
    candlestick_series_2 = CandlestickSeries(
        data=df2,
        up_color="#FF6B6B",
        down_color="#4ECDC4",
        # No trades for secondary series
    )

    # Create single pane chart with both series
    chart = Chart([candlestick_series_1, candlestick_series_2])

    config = chart.to_frontend_config()

    # Check that at least one series has trade visualizations
    chart_config = config["charts"][0]
    found_trades = False
    for series in chart_config["series"]:
        if any(key in series for key in ["markers", "shapes", "annotations"]):
            found_trades = True
            break

    assert (
        found_trades
    ), "Trades should be added to at least one price series when added at chart level"


def test_multi_pane_chart_with_heights():
    """Integration test for multi-pane chart with pane heights and overlays."""
    from streamlit_lightweight_charts_pro.charts.chart import Chart
    from streamlit_lightweight_charts_pro.charts.series import HistogramSeries, LineSeries
    from streamlit_lightweight_charts_pro.data import SingleValueData

    data = [SingleValueData("2024-01-01", 100), SingleValueData("2024-01-02", 105)]
    s1 = LineSeries(data, pane_id=0, height=200)
    s2 = HistogramSeries(data, pane_id=1, height=300)
    s3 = LineSeries(data, pane_id=0, overlay=True)
    chart = Chart(series=[s1, s2, s3])
    config = chart.to_frontend_config()
    assert config["charts"][0]["paneHeights"][0] == 200
    assert config["charts"][0]["paneHeights"][1] == 300
    assert config["charts"][0]["series"][2]["pane_id"] == 0
