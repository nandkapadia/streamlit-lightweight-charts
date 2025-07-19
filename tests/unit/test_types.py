from streamlit_lightweight_charts_pro.type_definitions.colors import (
    Background,
    VerticalGradientColor,
)
from streamlit_lightweight_charts_pro.type_definitions.enums import (
    ChartType,
    ColorType,
    HorzAlign,
    LineStyle,
    VertAlign,
)


def test_chart_type_enum():
    assert ChartType.LINE.value == "Line"
    assert ChartType.CANDLESTICK.value == "Candlestick"


def test_line_style_enum():
    assert LineStyle.SOLID == 0
    assert LineStyle.DASHED == 2


def test_horz_vert_align():
    assert HorzAlign.CENTER.value == "center"
    assert VertAlign.TOP.value == "top"


def test_background_color():
    bg = Background.solid("#fff")
    assert bg.color.color == "#fff"
    d = bg.to_dict()
    assert d["type"] == "solid"
    assert d["color"] == "#fff"


def test_vertical_gradient_color():
    grad = VerticalGradientColor("#fff", "#000")
    assert grad.type == ColorType.VERTICAL_GRADIENT
    assert grad.top_color == "#fff"
    assert grad.bottom_color == "#000"
    d = grad.to_dict()
    assert d["type"] == "gradient"
    assert d["topColor"] == "#fff"
    assert d["bottomColor"] == "#000"
