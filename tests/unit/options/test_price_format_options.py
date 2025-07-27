import pytest

from streamlit_lightweight_charts_pro.charts.options.price_format_options import PriceFormatOptions


def test_standard_construction():
    opts = PriceFormatOptions(
        type="price", precision=4, min_move=0.001, formatter="custom_formatter"
    )
    assert opts.type == "price"
    assert opts.precision == 4
    assert opts.min_move == 0.001
    assert opts.formatter == "custom_formatter"


def test_default_values():
    opts = PriceFormatOptions()
    assert opts.type == "price"
    assert opts.precision == 2
    assert opts.min_move == 0.01
    assert opts.formatter is None


def test_type_validation():
    PriceFormatOptions(type="price")
    PriceFormatOptions(type="volume")
    PriceFormatOptions(type="percent")
    PriceFormatOptions(type="custom")
    with pytest.raises(ValueError):
        PriceFormatOptions(type="invalid")


def test_precision_validation():
    PriceFormatOptions(precision=0)
    PriceFormatOptions(precision=5)
    with pytest.raises(ValueError):
        PriceFormatOptions(precision=-1)
    with pytest.raises(ValueError):
        PriceFormatOptions(precision=1.5)
    with pytest.raises(ValueError):
        PriceFormatOptions(precision="two")


def test_min_move_validation():
    PriceFormatOptions(min_move=0.01)
    PriceFormatOptions(min_move=1)
    with pytest.raises(ValueError):
        PriceFormatOptions(min_move=0)
    with pytest.raises(ValueError):
        PriceFormatOptions(min_move=-0.1)
    with pytest.raises(ValueError):
        PriceFormatOptions(min_move="small")


def test_optional_fields_omitted():
    opts = PriceFormatOptions(type="price", precision=2, min_move=0.01)
    assert opts.formatter is None


def test_custom_formatter():
    opts = PriceFormatOptions(type="custom", precision=2, min_move=0.01, formatter="myfmt")
    assert opts.formatter == "myfmt"
