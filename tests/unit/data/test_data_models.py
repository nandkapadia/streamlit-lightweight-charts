from datetime import datetime

import pandas as pd

from streamlit_lightweight_charts_pro.data import (
    Marker,
    OhlcData,
    SingleValueData,
)
from streamlit_lightweight_charts_pro.data.base import from_utc_timestamp, to_utc_timestamp
from streamlit_lightweight_charts_pro.type_definitions import ColumnNames, MarkerPosition
from streamlit_lightweight_charts_pro.type_definitions.enums import MarkerShape


def test_single_value_data():
    d = SingleValueData("2023-01-01", 100.0)
    assert d.value == 100.0
    assert pd.to_datetime("2023-01-01") == d.time
    d_dict = d.to_dict()
    assert d_dict[ColumnNames.VALUE] == 100.0
    assert d_dict[ColumnNames.TIME] == 1672531200  # Unix timestamp for 2023-01-01


def test_ohlc_data():
    d = OhlcData("2023-01-01", 1, 2, 0, 1.5)
    assert d.open == 1
    assert d.high == 2
    assert d.low == 0
    assert d.close == 1.5
    d_dict = d.to_dict()
    assert d_dict[ColumnNames.OPEN] == 1
    assert d_dict[ColumnNames.HIGH] == 2
    assert d_dict[ColumnNames.LOW] == 0
    assert d_dict[ColumnNames.CLOSE] == 1.5


def test_histogram_data():
    d = SingleValueData("2023-01-01", 42.0)
    assert d.value == 42.0
    d_dict = d.to_dict()
    assert d_dict[ColumnNames.VALUE] == 42.0


def test_baseline_data():
    d = SingleValueData("2023-01-01", 123.4)
    assert d.value == 123.4
    d_dict = d.to_dict()
    assert d_dict[ColumnNames.VALUE] == 123.4


def test_marker():
    m = Marker(
        "2023-01-01",
        MarkerPosition.ABOVE_BAR,
        "#000",
        MarkerShape.CIRCLE,
        text="A",
        size=10,
    )
    assert m.position == MarkerPosition.ABOVE_BAR
    assert m.shape == MarkerShape.CIRCLE
    d = m.to_dict()
    assert d["position"] == "aboveBar"
    assert d["shape"] == "circle"
    assert d["text"] == "A"
    assert d["size"] == 10


def test_to_utc_timestamp_and_from_utc_timestamp():
    dt = datetime(2023, 1, 1)
    ts = to_utc_timestamp(dt)
    assert isinstance(ts, int)
    dt2 = from_utc_timestamp(ts)
    # Compare dates, accounting for timezone differences
    assert abs((pd.to_datetime(dt) - dt2).total_seconds()) < 86400  # Within 1 day
    # String conversion to timestamp
    assert to_utc_timestamp("2023-01-01") == 1672531200  # Unix timestamp for 2023-01-01
    assert from_utc_timestamp(1672531200) == pd.to_datetime("2023-01-01")
