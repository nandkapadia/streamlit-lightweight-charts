import pandas as pd
import pytest

from streamlit_lightweight_charts_pro.charts.options.line_options import LineOptions
from streamlit_lightweight_charts_pro.charts.options.price_format_options import PriceFormatOptions
from streamlit_lightweight_charts_pro.charts.options.price_line_options import PriceLineOptions
from streamlit_lightweight_charts_pro.charts.series.line import LineSeries
from streamlit_lightweight_charts_pro.data import Marker
from streamlit_lightweight_charts_pro.data.line_data import LineData


@pytest.fixture
def line_options():
    return LineOptions(color="#2196F3", line_width=2)


@pytest.fixture
def line_data():
    return [
        LineData(time=1704067200, value=100.0, color="#2196F3"),
        LineData(time=1704153600, value=105.0, color="#2196F3"),
    ]


@pytest.fixture
def df():
    return pd.DataFrame(
        {
            "datetime": ["2024-01-01", "2024-01-02"],
            "close": [100.0, 105.0],
            "color": ["#2196F3", "#2196F3"],
        }
    )


@pytest.fixture
def column_mapping():
    return {"time": "datetime", "value": "close", "color": "color"}


def test_construction(line_data, line_options):
    series = LineSeries(data=line_data)
    assert series.data == line_data
    # Set line_options after construction since it's no longer a constructor parameter
    series.line_options = line_options
    assert series.line_options == line_options


def test_from_dataframe(df, column_mapping, line_options):
    series = LineSeries.from_dataframe(df, column_mapping)
    assert len(series.data) == 2
    assert isinstance(series.data[0], LineData)
    assert series.data[0].value == 100.0
    assert series.data[1].color == "#2196F3"


def test_missing_required_column_in_mapping(df, line_options):
    bad_mapping = {"value": "close", "color": "color"}  # missing 'time'
    with pytest.raises(ValueError):
        LineSeries.from_dataframe(df, bad_mapping)


def test_missing_required_column_in_dataframe(line_options):
    bad_df = pd.DataFrame({"close": [100.0, 105.0], "color": ["#2196F3", "#2196F3"]})
    mapping = {"time": "datetime", "value": "close", "color": "color"}
    with pytest.raises(ValueError):
        LineSeries.from_dataframe(bad_df, mapping)


def test_to_dict_structure(line_data, line_options):
    series = LineSeries(data=line_data)
    d = series.asdict()
    assert d["type"] == "line"
    assert isinstance(d["data"], list)
    assert "options" in d
    # priceLines should only be present when price lines are added


def test_set_price_format_and_price_lines(line_data, line_options):
    series = LineSeries(data=line_data)
    pf = PriceFormatOptions(type="price", precision=2)
    pl = PriceLineOptions(price=100.0, color="#2196F3")
    series.price_format = pf
    series.add_price_line(pl)
    assert series.price_format == pf
    assert pl in series.price_lines


def test_set_markers(line_data, line_options):
    series = LineSeries(data=line_data)
    m1 = Marker(time=1704067200, position="aboveBar", color="#2196F3", shape="circle")
    m2 = Marker(time=1704153600, position="belowBar", color="#2196F3", shape="circle")
    series.markers = [m1, m2]
    assert series.markers == [m1, m2]


def test_empty_data(line_options):
    series = LineSeries(data=[])
    assert series.data == []
    d = series.asdict()
    assert d["data"] == []


def test_extra_columns_in_dataframe(line_options):
    df = pd.DataFrame(
        {"datetime": ["2024-01-01"], "close": [100.0], "color": ["#2196F3"], "extra": [123]}
    )
    mapping = {"time": "datetime", "value": "close", "color": "color"}
    series = LineSeries.from_dataframe(df, mapping)
    assert len(series.data) == 1
    assert series.data[0].value == 100.0


def test_nan_handling(line_options):
    df = pd.DataFrame({"datetime": ["2024-01-01"], "close": [float("nan")], "color": ["#2196F3"]})
    mapping = {"time": "datetime", "value": "close", "color": "color"}
    series = LineSeries.from_dataframe(df, mapping)
    assert series.data[0].value == 0.0


def test_method_chaining(line_data, line_options):
    series = LineSeries(data=line_data)
    m1 = Marker(time=1704067200, position="aboveBar", color="#2196F3", shape="circle")
    m2 = Marker(time=1704153600, position="belowBar", color="#2196F3", shape="circle")
    pl = PriceLineOptions(price=100.0, color="#2196F3")
    # Chain multiple mutators
    result = (
        series.set_visible(False)
        .add_marker(m1.time, m1.position, m1.color, m1.shape)
        .add_markers([m2])
        .add_price_line(pl)
        .clear_markers()
        .clear_price_lines()
    )
    assert result is series
    assert series.visible is False
    assert series.markers == []
    assert series.price_lines == []


def test_add_marker_chaining(line_data, line_options):
    series = LineSeries(data=line_data)
    m = Marker(time=1704067200, position="aboveBar", color="#2196F3", shape="circle")
    result = series.add_marker(m.time, m.position, m.color, m.shape)
    assert result is series
    assert len(series.markers) == 1


def test_add_price_line_chaining(line_data, line_options):
    series = LineSeries(data=line_data)
    pl = PriceLineOptions(price=100.0, color="#2196F3")
    result = series.add_price_line(pl)
    assert result is series
    assert pl in series.price_lines


def test_clear_markers_chaining(line_data, line_options):
    series = LineSeries(data=line_data)
    m = Marker(time=1704067200, position="aboveBar", color="#2196F3", shape="circle")
    series.add_marker(m.time, m.position, m.color, m.shape)
    result = series.clear_markers()
    assert result is series
    assert series.markers == []


def test_clear_price_lines_chaining(line_data, line_options):
    series = LineSeries(data=line_data)
    pl = PriceLineOptions(price=100.0, color="#2196F3")
    series.add_price_line(pl)
    result = series.clear_price_lines()
    assert result is series
    assert series.price_lines == []
