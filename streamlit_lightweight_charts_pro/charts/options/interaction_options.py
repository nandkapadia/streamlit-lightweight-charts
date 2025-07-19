"""Interaction option classes for streamlit-lightweight-charts."""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from streamlit_lightweight_charts_pro.type_definitions import (
    CrosshairMode,
    LineStyle,
    TrackingActivationMode,
    TrackingExitMode,
)


@dataclass
class CrosshairLineOptions:
    """Crosshair line configuration."""

    visible: bool = True
    width: int = 1
    color: str = "rgba(224, 227, 235, 0.2)"
    style: LineStyle = LineStyle.DASHED

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "visible": self.visible,
            "width": self.width,
            "color": self.color,
            "style": self.style.value,
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


@dataclass
class CrosshairOptions:
    """Crosshair configuration for chart."""

    mode: CrosshairMode = CrosshairMode.MAGNET
    vert_line: CrosshairLineOptions = field(default_factory=CrosshairLineOptions)
    horz_line: CrosshairLineOptions = field(default_factory=CrosshairLineOptions)
    sync: Optional[CrosshairSyncOptions] = None
    group_id: Optional[str] = None

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


@dataclass
class TrackingModeOptions:
    """Tracking mode configuration for chart."""

    exit_mode: TrackingExitMode = TrackingExitMode.EXIT_ON_MOVE
    activation_mode: TrackingActivationMode = TrackingActivationMode.ON_MOUSE_ENTER

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "exitMode": self.exit_mode.value,
            "activationMode": self.activation_mode.value,
        }
