import pytest

from streamlit_lightweight_charts_pro.charts.options.price_line_options import PriceLineOptions
from streamlit_lightweight_charts_pro.type_definitions.enums import LineStyle


def test_standard_construction():
    opts = PriceLineOptions(
        id="pl1",
        price=123.45,
        color="#2196F3",
        line_width=2,
        line_style=LineStyle.DASHED,
        line_visible=False,
        axis_label_visible=False,
        title="Test Line",
        axis_label_color="#FFFFFF",
        axis_label_text_color="rgba(0,0,0,1)",
    )
    assert opts.id == "pl1"
    assert opts.price == 123.45
    assert opts.color == "#2196F3"
    assert opts.line_width == 2
    assert opts.line_style == LineStyle.DASHED
    assert not opts.line_visible
    assert not opts.axis_label_visible
    assert opts.title == "Test Line"
    assert opts.axis_label_color == "#FFFFFF"
    assert opts.axis_label_text_color == "rgba(0,0,0,1)"


def test_default_values():
    opts = PriceLineOptions()
    assert opts.id is None
    assert opts.price == 0.0
    assert opts.color == ""
    assert opts.line_width == 1
    assert opts.line_style == LineStyle.SOLID
    assert opts.line_visible is True
    assert opts.axis_label_visible is True
    assert opts.title == ""
    assert opts.axis_label_color is None
    assert opts.axis_label_text_color is None


def test_color_validation():
    PriceLineOptions(color="#123456")
    PriceLineOptions(color="rgba(1,2,3,0.5)")
    with pytest.raises(ValueError):
        PriceLineOptions(color="notacolor")


def test_axis_label_color_validation():
    PriceLineOptions(axis_label_color="#123456")
    PriceLineOptions(axis_label_color="rgba(1,2,3,0.5)")
    with pytest.raises(ValueError):
        PriceLineOptions(axis_label_color="notacolor")


def test_axis_label_text_color_validation():
    PriceLineOptions(axis_label_text_color="#123456")
    PriceLineOptions(axis_label_text_color="rgba(1,2,3,0.5)")
    with pytest.raises(ValueError):
        PriceLineOptions(axis_label_text_color="notacolor")


def test_line_width_validation():
    PriceLineOptions(line_width=1)
    PriceLineOptions(line_width=5)
    with pytest.raises(ValueError):
        PriceLineOptions(line_width=0)
    with pytest.raises(ValueError):
        PriceLineOptions(line_width=-1)
    with pytest.raises(ValueError):
        PriceLineOptions(line_width=1.5)


def test_price_validation():
    PriceLineOptions(price=0)
    PriceLineOptions(price=123.45)
    with pytest.raises(ValueError):
        PriceLineOptions(price="notanumber")


def test_optional_fields_omitted():
    opts = PriceLineOptions(price=10.0)
    assert opts.id is None
    assert opts.axis_label_color is None
    assert opts.axis_label_text_color is None
