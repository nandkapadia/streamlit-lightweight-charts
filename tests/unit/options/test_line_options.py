import pytest

from streamlit_lightweight_charts_pro.charts.options.line_options import LineOptions
from streamlit_lightweight_charts_pro.type_definitions.enums import (
    LastPriceAnimationMode,
    LineStyle,
    LineType,
)


def test_standard_construction():
    opts = LineOptions(
        color="#2196F3",
        line_style=LineStyle.DASHED,
        line_width=4,
        line_type=LineType.CURVED,
        line_visible=False,
        point_markers_visible=True,
        point_markers_radius=6,
        crosshair_marker_visible=False,
        crosshair_marker_radius=5,
        crosshair_marker_border_color="#FFFFFF",
        crosshair_marker_background_color="#000000",
        crosshair_marker_border_width=3,
        last_price_animation=LastPriceAnimationMode.CONTINUOUS,
    )
    assert opts.color == "#2196F3"
    assert opts.line_style == LineStyle.DASHED
    assert opts.line_width == 4
    assert opts.line_type == LineType.CURVED
    assert not opts.line_visible
    assert opts.point_markers_visible
    assert opts.point_markers_radius == 6
    assert not opts.crosshair_marker_visible
    assert opts.crosshair_marker_radius == 5
    assert opts.crosshair_marker_border_color == "#FFFFFF"
    assert opts.crosshair_marker_background_color == "#000000"
    assert opts.crosshair_marker_border_width == 3
    assert opts.last_price_animation == LastPriceAnimationMode.CONTINUOUS


def test_default_values():
    opts = LineOptions()
    assert opts.color == "#2196f3"
    assert opts.line_style == LineStyle.SOLID
    assert opts.line_width == 3
    assert opts.line_type == LineType.SIMPLE
    assert opts.line_visible is True
    assert opts.point_markers_visible is False
    assert opts.point_markers_radius is None
    assert opts.crosshair_marker_visible is True
    assert opts.crosshair_marker_radius == 4
    assert opts.crosshair_marker_border_color == ""
    assert opts.crosshair_marker_background_color == ""
    assert opts.crosshair_marker_border_width == 2
    assert opts.last_price_animation == LastPriceAnimationMode.DISABLED


def test_color_validation():
    LineOptions(color="#123456")
    LineOptions(color="rgba(1,2,3,0.5)")
    with pytest.raises(ValueError):
        LineOptions(color="notacolor")


def test_crosshair_marker_border_color_validation():
    LineOptions(crosshair_marker_border_color="#123456")
    LineOptions(crosshair_marker_border_color="rgba(1,2,3,0.5)")
    with pytest.raises(ValueError):
        LineOptions(crosshair_marker_border_color="notacolor")


def test_crosshair_marker_background_color_validation():
    LineOptions(crosshair_marker_background_color="#123456")
    LineOptions(crosshair_marker_background_color="rgba(1,2,3,0.5)")
    with pytest.raises(ValueError):
        LineOptions(crosshair_marker_background_color="notacolor")


def test_line_width_validation():
    LineOptions(line_width=1)
    LineOptions(line_width=5)
    with pytest.raises(ValueError):
        LineOptions(line_width=0)
    with pytest.raises(ValueError):
        LineOptions(line_width=-1)
    with pytest.raises(ValueError):
        LineOptions(line_width=1.5)


def test_point_markers_radius_validation():
    LineOptions(point_markers_radius=2)
    LineOptions(point_markers_radius=None)
    with pytest.raises(ValueError):
        LineOptions(point_markers_radius=0)
    with pytest.raises(ValueError):
        LineOptions(point_markers_radius=-1)
    with pytest.raises(ValueError):
        LineOptions(point_markers_radius=1.5)


def test_crosshair_marker_radius_validation():
    LineOptions(crosshair_marker_radius=1)
    with pytest.raises(ValueError):
        LineOptions(crosshair_marker_radius=0)
    with pytest.raises(ValueError):
        LineOptions(crosshair_marker_radius=-1)
    with pytest.raises(ValueError):
        LineOptions(crosshair_marker_radius=1.5)


def test_crosshair_marker_border_width_validation():
    LineOptions(crosshair_marker_border_width=1)
    with pytest.raises(ValueError):
        LineOptions(crosshair_marker_border_width=0)
    with pytest.raises(ValueError):
        LineOptions(crosshair_marker_border_width=-1)
    with pytest.raises(ValueError):
        LineOptions(crosshair_marker_border_width=1.5)


def test_optional_fields_omitted():
    opts = LineOptions()
    assert opts.point_markers_radius is None
    assert opts.crosshair_marker_border_color == ""
    assert opts.crosshair_marker_background_color == ""
