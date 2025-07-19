from streamlit_lightweight_charts_pro.charts.options import (
    ChartOptions,
    CrosshairLineOptions,
    CrosshairOptions,
    GridLineOptions,
    GridOptions,
    LayoutOptions,
    TimeScaleOptions,
    WatermarkOptions,
    RightPriceScale,
)
from streamlit_lightweight_charts_pro.type_definitions.colors import Background
from streamlit_lightweight_charts_pro.type_definitions.enums import (
    CrosshairMode,
    HorzAlign,
    LineStyle,
    PriceScaleMode,
    VertAlign,
)


def test_grid_line_options():
    options = GridLineOptions(color="#cccccc", style=LineStyle.DASHED, visible=False)
    assert options.color == "#cccccc"
    assert options.style == LineStyle.DASHED
    assert options.visible is False

    d = options.to_dict()
    assert d["color"] == "#cccccc"
    assert d["style"] == LineStyle.DASHED.value
    assert d["visible"] is False


def test_grid_options():
    vert_lines = GridLineOptions(color="#ff0000")
    horz_lines = GridLineOptions(color="#00ff00")
    options = GridOptions(vert_lines=vert_lines, horz_lines=horz_lines)

    d = options.to_dict()
    assert d["vertLines"]["color"] == "#ff0000"
    assert d["horzLines"]["color"] == "#00ff00"


def test_layout_options():
    background = Background.solid("#ffffff")
    options = LayoutOptions(background=background, text_color="#000000", font_size=14)
    assert options.text_color == "#000000"
    assert options.font_size == 14

    d = options.to_dict()
    assert d["textColor"] == "#000000"
    assert d["fontSize"] == 14
    assert d["background"]["type"] == "solid"


def test_crosshair_line_options():
    options = CrosshairLineOptions(visible=True, width=2, color="#ff0000", style=LineStyle.SOLID)
    assert options.visible is True
    assert options.width == 2

    d = options.to_dict()
    assert d["visible"] is True
    assert d["width"] == 2
    assert d["color"] == "#ff0000"


def test_crosshair_options():
    vert_line = CrosshairLineOptions(color="#ff0000")
    horz_line = CrosshairLineOptions(color="#00ff00")
    options = CrosshairOptions(mode=CrosshairMode.MAGNET, vert_line=vert_line, horz_line=horz_line)
    assert options.mode == CrosshairMode.MAGNET

    d = options.to_dict()
    assert d["mode"] == CrosshairMode.MAGNET.value
    assert d["vertLine"]["color"] == "#ff0000"
    assert d["horzLine"]["color"] == "#00ff00"


def test_price_scale_options():
    options = RightPriceScale(
        border_visible=False, border_color="#cccccc", mode=PriceScaleMode.LOGARITHMIC
    )
    assert options.border_visible is False
    assert options.mode == PriceScaleMode.LOGARITHMIC

    d = options.to_dict()
    assert d["borderVisible"] is False
    assert d["mode"] == PriceScaleMode.LOGARITHMIC.value


def test_time_scale_options():
    options = TimeScaleOptions(
        right_offset=5, bar_spacing=10, time_visible=True, border_visible=False
    )
    assert options.right_offset == 5
    assert options.bar_spacing == 10
    assert options.time_visible is True
    assert options.border_visible is False

    d = options.to_dict()
    assert d["rightOffset"] == 5
    assert d["barSpacing"] == 10
    assert d["timeVisible"] is True
    assert d["borderVisible"] is False


def test_watermark_options():
    options = WatermarkOptions(
        visible=True,
        text="TEST",
        font_size=24,
        horz_align=HorzAlign.CENTER,
        vert_align=VertAlign.CENTER,
        color="rgba(0,0,0,0.5)",
    )
    assert options.visible is True
    assert options.text == "TEST"
    assert options.horz_align == HorzAlign.CENTER

    d = options.to_dict()
    assert d["visible"] is True
    assert d["text"] == "TEST"
    assert d["horzAlign"] == HorzAlign.CENTER.value


def test_chart_options():
    layout = LayoutOptions()
    grid = GridOptions()
    crosshair = CrosshairOptions()
    right_price_scale = RightPriceScale()
    time_scale = TimeScaleOptions()

    options = ChartOptions(
        width=800,
        height=600,
        layout=layout,
        grid=grid,
        crosshair=crosshair,
        right_price_scale=right_price_scale,
        time_scale=time_scale,
    )
    assert options.width == 800
    assert options.height == 600

    d = options.to_dict()
    assert d["width"] == 800
    assert d["height"] == 600
    assert "layout" in d
    assert "grid" in d
    assert "crosshair" in d
    assert "rightPriceScale" in d
    assert "timeScale" in d
