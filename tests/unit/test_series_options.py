from streamlit_lightweight_charts.charts.series import (
    AreaSeriesOptions,
    BarSeriesOptions,
    BaselineSeriesOptions,
    CandlestickSeriesOptions,
    HistogramSeriesOptions,
    LineSeriesOptions,
)
from streamlit_lightweight_charts.type_definitions.enums import LineStyle, LineType


def test_area_series_options():
    options = AreaSeriesOptions(
        top_color="rgba(0,255,0,0.5)",
        bottom_color="rgba(0,255,0,0.0)",
        line_color="#00ff00",
        line_width=3,
    )
    assert options.top_color == "rgba(0,255,0,0.5)"
    assert options.line_width == 3

    d = options.to_dict()
    assert d["topColor"] == "rgba(0,255,0,0.5)"
    assert d["lineWidth"] == 3
    assert d["lineStyle"] == LineStyle.SOLID.value


def test_line_series_options():
    options = LineSeriesOptions(
        color="#ff0000",
        line_style=LineStyle.DASHED,
        line_width=2,
        line_type=LineType.CURVED,
    )
    assert options.color == "#ff0000"
    assert options.line_style == LineStyle.DASHED

    d = options.to_dict()
    assert d["color"] == "#ff0000"
    assert d["lineStyle"] == LineStyle.DASHED.value
    assert d["lineType"] == LineType.CURVED.value


def test_bar_series_options():
    options = BarSeriesOptions(up_color="#00ff00", down_color="#ff0000", thin_bars=True)
    assert options.up_color == "#00ff00"
    assert options.thin_bars is True

    d = options.to_dict()
    assert d["upColor"] == "#00ff00"
    assert d["thinBars"] is True


def test_candlestick_series_options():
    options = CandlestickSeriesOptions(
        up_color="#00ff00",
        down_color="#ff0000",
        wick_visible=False,
        border_visible=True,
    )
    assert options.up_color == "#00ff00"
    assert options.wick_visible is False
    assert options.border_visible is True

    d = options.to_dict()
    assert d["upColor"] == "#00ff00"
    assert d["wickVisible"] is False
    assert d["borderVisible"] is True


def test_histogram_series_options():
    options = HistogramSeriesOptions(color="#ff00ff", base=10.0)
    assert options.color == "#ff00ff"
    assert options.base == 10.0

    d = options.to_dict()
    assert d["color"] == "#ff00ff"
    assert d["base"] == 10.0


def test_baseline_series_options():
    options = BaselineSeriesOptions(
        base_value={"type": "price", "price": 50.0},
        top_line_color="#00ff00",
        bottom_line_color="#ff0000",
    )
    assert options.base_value["price"] == 50.0
    assert options.top_line_color == "#00ff00"

    d = options.to_dict()
    assert d["baseValue"]["price"] == 50.0
    assert d["topLineColor"] == "#00ff00"
