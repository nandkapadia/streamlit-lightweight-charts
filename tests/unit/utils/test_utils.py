import pandas as pd

from streamlit_lightweight_charts_pro.type_definitions import ColumnNames
from streamlit_lightweight_charts_pro.utils.dataframe_converter import (
    df_to_line_data,
    df_to_ohlc_data,
)


def test_df_to_line_data():
    df = pd.DataFrame(
        {ColumnNames.TIME: ["2023-01-01", "2023-01-02"], ColumnNames.VALUE: [1.0, 2.0]}
    )
    data = df_to_line_data(df, value_column=ColumnNames.VALUE, time_column=ColumnNames.TIME)
    assert len(data) == 2
    assert data[0].value == 1.0
    assert data[1].value == 2.0


def test_df_to_ohlc_data():
    df = pd.DataFrame(
        {
            ColumnNames.TIME: ["2023-01-01", "2023-01-02"],
            ColumnNames.OPEN: [1, 2],
            ColumnNames.HIGH: [2, 3],
            ColumnNames.LOW: [0, 1],
            ColumnNames.CLOSE: [1.5, 2.5],
        }
    )
    data = df_to_ohlc_data(df)
    assert len(data) == 2
    assert data[0].open == 1
    assert data[1].close == 2.5
