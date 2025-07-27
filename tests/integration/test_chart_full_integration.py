import pandas as pd

from streamlit_lightweight_charts_pro.charts import Chart
from streamlit_lightweight_charts_pro.charts.options.line_options import LineOptions
from streamlit_lightweight_charts_pro.charts.options.trade_visualization_options import (
    TradeVisualizationOptions,
)
from streamlit_lightweight_charts_pro.charts.series.candlestick import CandlestickSeries
from streamlit_lightweight_charts_pro.charts.series.histogram import HistogramSeries
from streamlit_lightweight_charts_pro.charts.series.line import LineSeries
from streamlit_lightweight_charts_pro.data.annotation import Annotation
from streamlit_lightweight_charts_pro.data.line_data import LineData
from streamlit_lightweight_charts_pro.data.ohlcv_data import OhlcvData
from streamlit_lightweight_charts_pro.data.trade import Trade


def create_sample_ohlcv_data(n=10):
    return [
        OhlcvData(
            time=1640995200 + i * 60 * 60,
            open=100 + i,
            high=105 + i,
            low=95 + i,
            close=102 + i,
            volume=1000 + i * 10,
        )
        for i in range(n)
    ]


def create_sample_line_data(n=10):
    return [LineData(time=1640995200 + i * 60 * 60, value=100 + i) for i in range(n)]


def test_multi_series_chart_with_price_scales():
    """Test chart with multiple series and different price scales."""
    line_series = LineSeries(
        data=create_sample_line_data(),
        line_options=LineOptions(color="#2196f3"),
        price_scale_id="left",
    )
    candle_series = CandlestickSeries(data=create_sample_ohlcv_data(), price_scale_id="right")
    volume_series = HistogramSeries(data=create_sample_ohlcv_data(), price_scale_id="overlay1")
    chart = Chart(series=[line_series, candle_series, volume_series])
    config = chart.to_frontend_config()
    assert len(config["charts"][0]["series"]) == 3
    assert {s["priceScaleId"] for s in config["charts"][0]["series"]} == {
        "left",
        "right",
        "overlay1",
    }


def test_dataframe_to_chart_pipeline():
    """Test DataFrame → Series → Chart → JSON pipeline."""
    df = pd.DataFrame(
        {
            "time": pd.date_range("2024-01-01", periods=10, freq="1h"),
            "open": range(100, 110),
            "high": range(105, 115),
            "low": range(95, 105),
            "close": range(102, 112),
            "volume": range(1000, 1010),
        }
    )
    column_mapping = {
        "time": "time",
        "open": "open",
        "high": "high",
        "low": "low",
        "close": "close",
        "volume": "volume",
    }
    chart = Chart.from_price_volume_dataframe(
        data=df, column_mapping=column_mapping, price_type="candlestick"
    )
    config = chart.to_frontend_config()
    assert "charts" in config
    assert len(config["charts"][0]["series"]) == 2  # price + volume


def test_chart_with_annotations_and_trades():
    """Test chart with annotations and trade visualization integration."""
    line_series = LineSeries(data=create_sample_line_data(), line_options=LineOptions())
    chart = Chart(series=[line_series])
    # Add annotation
    annotation = Annotation(
        time=1640995200, price=100, position="above", text="Test", color="#ff0000"
    )
    chart.add_annotation(annotation)
    # Add trade visualization
    trades = [
        Trade(
            entry_time=1640995200,
            entry_price=100,
            exit_time=1640998800,
            exit_price=110,
            quantity=1,
            trade_type="long",
        )
    ]
    chart.options.trade_visualization = TradeVisualizationOptions()
    chart.add_trade_visualization(trades)
    config = chart.to_frontend_config()
    assert "annotations" in config["charts"][0]
    assert len(config["charts"][0]["annotations"]) >= 1
    # Check that trade visualization markers were added to series
    series_with_markers = [
        s for s in config["charts"][0]["series"] if "markers" in s and len(s["markers"]) > 0
    ]
    assert len(series_with_markers) > 0


def test_serialization_idempotency():
    """Test that serialization is idempotent and matches frontend expectations."""
    line_series = LineSeries(data=create_sample_line_data(), line_options=LineOptions())
    chart = Chart(series=[line_series])
    config1 = chart.to_frontend_config()
    config2 = chart.to_frontend_config()
    assert config1 == config2
    assert "charts" in config1
    assert isinstance(config1["charts"], list)
    assert "series" in config1["charts"][0]
    assert isinstance(config1["charts"][0]["series"], list)
