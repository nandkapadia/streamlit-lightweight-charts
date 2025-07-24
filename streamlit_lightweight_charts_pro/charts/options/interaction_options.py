"""Interaction option classes for streamlit-lightweight-charts."""

from dataclasses import dataclass
from typing import Any, Dict, Optional, Union

from streamlit_lightweight_charts_pro.type_definitions.enums import (
    LineStyle,
    CrosshairMode,
    TrackingExitMode,
    TrackingActivationMode,
)


class CrosshairLineOptions:
    """Crosshair line configuration."""

    def __init__(
        self,
        color: str = "#758696",
        width: int = 1,
        style: Union[int, LineStyle] = LineStyle.SOLID,
        visible: bool = True,
    ):
        self.color = color
        self.width = width
        # Accept both int and Enum for style
        if isinstance(style, int):
            self.style = LineStyle(style)
        else:
            self.style = style
        self.visible = visible

    def __getitem__(self, key):
        if key == "color":
            return self.color
        if key == "width":
            return self.width
        if key == "style":
            return self.style.value
        if key == "visible":
            return self.visible
        raise KeyError(key)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "color": self.color,
            "width": self.width,
            "style": self.style.value,
            "visible": self.visible,
        }


@dataclass
class CrosshairSyncOptions:
    """Crosshair synchronization configuration."""

    group_id: str = "default"
    suppress_crosshair_move: bool = False
    suppress_mouse_move: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "groupId": self.group_id,
            "suppressCrosshairMove": self.suppress_crosshair_move,
            "suppressMouseMove": self.suppress_mouse_move,
        }


class CrosshairOptions:
    """Crosshair configuration for chart."""

    def __init__(
        self,
        mode: Union[int, CrosshairMode] = 1,  # Default to magnetic (1) for test compatibility
        vert_line: CrosshairLineOptions = None,
        horz_line: CrosshairLineOptions = None,
        sync: Optional["CrosshairSyncOptions"] = None,
        group_id: Optional[str] = None,
    ):
        # Accept both int and Enum for mode
        if isinstance(mode, int):
            self.mode = CrosshairMode(mode)
        else:
            self.mode = mode
        self.vert_line = vert_line or CrosshairLineOptions()
        self.horz_line = horz_line or CrosshairLineOptions()
        self.sync = sync
        self.group_id = group_id

    def __getitem__(self, key):
        if key == "mode":
            return self.mode.value
        if key in ("vert_line", "vertLine"):
            return self.vert_line
        if key in ("horz_line", "horzLine"):
            return self.horz_line
        d = self.to_dict()
        if key in d:
            return d[key]
        raise KeyError(key)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        result = {
            "mode": self.mode.value,
            "vertLine": self.vert_line.to_dict(),
            "horzLine": self.horz_line.to_dict(),
        }

        if self.sync is not None:
            result["sync"] = self.sync.to_dict()

        if self.group_id is not None:
            result["groupId"] = self.group_id

        return result


@dataclass
class KineticScrollOptions:
    """Kinetic scroll configuration for chart."""

    touch: bool = True
    mouse: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "touch": self.touch,
            "mouse": self.mouse,
        }


class TrackingModeOptions:
    """Tracking mode configuration for chart."""

    def __init__(
        self,
        exit_mode: Union[str, TrackingExitMode] = TrackingExitMode.EXIT_ON_MOVE,
        activation_mode: Union[str, TrackingActivationMode] = TrackingActivationMode.ON_MOUSE_ENTER,
    ):
        # Accept both str and Enum for exit_mode
        if isinstance(exit_mode, str):
            self.exit_mode = TrackingExitMode(exit_mode)
        else:
            self.exit_mode = exit_mode
        # Accept both str and Enum for activation_mode
        if isinstance(activation_mode, str):
            self.activation_mode = TrackingActivationMode(activation_mode)
        else:
            self.activation_mode = activation_mode

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {"exitMode": self.exit_mode.value, "activationMode": self.activation_mode.value}
