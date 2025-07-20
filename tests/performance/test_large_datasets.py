import time

import pandas as pd

from streamlit_lightweight_charts_pro.charts import SinglePaneChart
from streamlit_lightweight_charts_pro.charts.series import CandlestickSeries, LineSeries
from streamlit_lightweight_charts_pro.data.models import SingleValueData


def test_large_line_chart_performance():
    """Test performance of large line chart with ultra-simplified API."""
    # Create large dataset
    n_points = 10000
    df = pd.DataFrame(
        {
            "datetime": pd.date_range("2023-01-01", periods=n_points, freq="h"),
            "close": range(n_points),
        }
    )

    start_time = time.time()
    series = LineSeries(df, color="#ff0000")
    series_time = time.time() - start_time

    start_time = time.time()
    chart = SinglePaneChart(series)
    chart_time = time.time() - start_time

    start_time = time.time()
    chart.to_frontend_config()
    serialization_time = time.time() - start_time

    # Performance assertions
    assert series_time < 2.0  # Should create series in under 2 seconds
    assert chart_time < 0.5  # Should create chart in under 0.5 seconds
    assert serialization_time < 0.5  # Should serialize in under 0.5 seconds
    assert len(series.data) == n_points


def test_large_candlestick_chart_performance():
    """Test performance of large candlestick chart with ultra-simplified API."""
    # Create large OHLC dataset
    n_points = 5000
    df = pd.DataFrame(
        {
            "datetime": pd.date_range("2023-01-01", periods=n_points, freq="h"),
            "open": range(n_points),
            "high": [x + 1 for x in range(n_points)],
            "low": [x - 1 for x in range(n_points)],
            "close": [x + 0.5 for x in range(n_points)],
        }
    )

    start_time = time.time()
    series = CandlestickSeries(df, up_color="#00ff00", down_color="#ff0000")
    series_time = time.time() - start_time

    start_time = time.time()
    chart = SinglePaneChart(series)
    chart_time = time.time() - start_time

    start_time = time.time()
    chart.to_frontend_config()
    serialization_time = time.time() - start_time

    # Performance assertions
    assert series_time < 2.0
    assert chart_time < 0.5
    assert serialization_time < 0.5
    assert len(series.data) == n_points


def test_memory_usage():
    """Test memory usage with ultra-simplified API."""
    import os

    import psutil

    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss

    # Create large dataset
    n_points = 5000
    data = [SingleValueData(f"2023-01-{i:02d}", i) for i in range(n_points)]
    series = LineSeries(data, color="#ff0000")
    chart = SinglePaneChart(series)
    chart.to_frontend_config()

    final_memory = process.memory_info().rss
    memory_increase = final_memory - initial_memory

    # Memory increase should be reasonable (less than 100MB for 5000 points)
    assert memory_increase < 100 * 1024 * 1024  # 100MB


def test_many_series_performance():
    """Test performance with many series using ultra-simplified API."""
    # Test chart with many series
    n_series = 10
    n_points = 1000

    series_list = []
    for i in range(n_series):
        data = [SingleValueData(f"2023-01-{j:02d}", j + i) for j in range(n_points)]
        series_list.append(LineSeries(data, color=f"#{i:06x}"))

    start_time = time.time()
    chart = SinglePaneChart(series_list)
    chart_time = time.time() - start_time

    start_time = time.time()
    config = chart.to_frontend_config()
    serialization_time = time.time() - start_time

    assert chart_time < 1.0
    assert serialization_time < 1.0
    # Fixed: Access correct nested structure
    assert len(config["charts"][0]["series"]) == n_series


def test_dataframe_conversion_performance():
    """Test performance of DataFrame to Series conversion."""
    # Create large DataFrame
    n_points = 10000
    df = pd.DataFrame(
        {
            "datetime": pd.date_range("2023-01-01", periods=n_points, freq="h"),
            "close": range(n_points),
        }
    )

    start_time = time.time()
    series = LineSeries(df, color="#ff0000", line_width=2)
    conversion_time = time.time() - start_time

    # Test that conversion is fast
    assert conversion_time < 2.0
    assert len(series.data) == n_points

    # Test that styling is applied
    options = series._get_options_dict()
    assert options["color"] == "#ff0000"
    assert options["lineWidth"] == 2
