import pandas as pd

from streamlit_lightweight_charts.utils.dataframe_converter import (
    df_to_baseline_data,
    df_to_histogram_data,
    df_to_line_data,
    df_to_ohlc_data,
)


def test_df_to_line_data():
    df = pd.DataFrame({"time": ["2023-01-01", "2023-01-02"], "value": [1.0, 2.0]})
    data = df_to_line_data(df, value_column="value")
    assert len(data) == 2
    assert data[0].value == 1.0
    assert data[1].value == 2.0


def test_df_to_ohlc_data():
    df = pd.DataFrame(
        {
            "time": ["2023-01-01", "2023-01-02"],
            "open": [1, 2],
            "high": [2, 3],
            "low": [0, 1],
            "close": [1.5, 2.5],
        }
    )
    data = df_to_ohlc_data(df)
    assert len(data) == 2
    assert data[0].open == 1
    assert data[1].close == 2.5


def test_df_to_histogram_data():
    df = pd.DataFrame({"time": ["2023-01-01"], "value": [42.0], "color": ["#ff0"]})
    data = df_to_histogram_data(df, value_column="value", color_column="color")
    assert data[0].value == 42.0
    assert data[0].color == "#ff0"


def test_df_to_baseline_data():
    df = pd.DataFrame({"time": ["2023-01-01"], "value": [123.4]})
    data = df_to_baseline_data(df)
    assert data[0].value == 123.4
