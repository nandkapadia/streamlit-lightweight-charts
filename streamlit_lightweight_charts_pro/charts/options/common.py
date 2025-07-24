from dataclasses import dataclass


@dataclass
class LineStyleOptions:
    """Line options for chart."""

    color: str = "#2196F3"
    width: int = 2
    style: str = "solid"
    visible: bool = True


@dataclass
class CrosshairMarkerOptions:
    """Crosshair marker options for chart."""

    visible: bool = True
    radius: int = 4
    border_color: str = ""
    background_color: str = ""
    border_width: int = 2
