import time

import pandas as pd

from streamlit_lightweight_charts.charts import CandlestickChart, LineChart
from streamlit_lightweight_charts.data.models import SingleValueData
from streamlit_lightweight_charts.utils.dataframe_converter import (
    df_to_line_data,
    df_to_ohlc_data,
)


def test_large_line_chart_performance():
    # Create large dataset
    n_points = 10000
    df = pd.DataFrame(
        {
            "time": pd.date_range("2023-01-01", periods=n_points, freq="H"),
            "value": range(n_points),
        }
    )

    start_time = time.time()
    data = df_to_line_data(df, value_column="value")
    conversion_time = time.time() - start_time

    start_time = time.time()
    chart = LineChart(data)
    chart_time = time.time() - start_time

    start_time = time.time()
    chart.to_frontend_config()
    serialization_time = time.time() - start_time

    # Performance assertions
    assert conversion_time < 1.0  # Should convert in under 1 second
    assert chart_time < 0.5  # Should create chart in under 0.5 seconds
    assert serialization_time < 0.5  # Should serialize in under 0.5 seconds
    assert len(data) == n_points


def test_large_candlestick_chart_performance():
    # Create large OHLC dataset
    n_points = 5000
    df = pd.DataFrame(
        {
            "time": pd.date_range("2023-01-01", periods=n_points, freq="H"),
            "open": range(n_points),
            "high": [x + 1 for x in range(n_points)],
            "low": [x - 1 for x in range(n_points)],
            "close": [x + 0.5 for x in range(n_points)],
        }
    )

    start_time = time.time()
    data = df_to_ohlc_data(df)
    conversion_time = time.time() - start_time

    start_time = time.time()
    chart = CandlestickChart(data)
    chart_time = time.time() - start_time

    start_time = time.time()
    chart.to_frontend_config()
    serialization_time = time.time() - start_time

    # Performance assertions
    assert conversion_time < 1.0
    assert chart_time < 0.5
    assert serialization_time < 0.5
    assert len(data) == n_points


def test_memory_usage():
    import os

    import psutil

    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss

    # Create large dataset
    n_points = 5000
    data = [SingleValueData(f"2023-01-{i:02d}", i) for i in range(n_points)]
    chart = LineChart(data)
    chart.to_frontend_config()

    final_memory = process.memory_info().rss
    memory_increase = final_memory - initial_memory

    # Memory increase should be reasonable (less than 100MB for 5000 points)
    assert memory_increase < 100 * 1024 * 1024  # 100MB


def test_many_series_performance():
    # Test chart with many series
    n_series = 10
    n_points = 1000

    series_list = []
    for i in range(n_series):
        data = [SingleValueData(f"2023-01-{j:02d}", j + i) for j in range(n_points)]
        from streamlit_lightweight_charts.charts.series import LineSeries

        series_list.append(LineSeries(data))

    start_time = time.time()
    from streamlit_lightweight_charts.charts import Chart

    chart = Chart(series_list)
    chart_time = time.time() - start_time

    start_time = time.time()
    config = chart.to_frontend_config()
    serialization_time = time.time() - start_time

    assert chart_time < 1.0
    assert serialization_time < 1.0
    assert len(config["series"]) == n_series
