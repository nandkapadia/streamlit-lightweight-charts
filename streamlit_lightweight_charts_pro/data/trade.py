"""Trade data model for visualizing trades on charts."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, Union

import pandas as pd

from .base import from_utc_timestamp, to_utc_timestamp


class TradeType(str, Enum):
    """Trade type enumeration."""

    LONG = "long"
    SHORT = "short"


class TradeVisualization(str, Enum):
    """Trade visualization style options."""

    MARKERS = "markers"  # Just entry/exit markers
    RECTANGLES = "rectangles"  # Rectangle from entry to exit
    BOTH = "both"  # Both markers and rectangles
    LINES = "lines"  # Lines connecting entry to exit
    ARROWS = "arrows"  # Arrows from entry to exit
    ZONES = "zones"  # Colored zones with transparency


@dataclass
class Trade:
    """
    Represents a single trade with entry and exit information.

    Attributes:
        entry_time: Entry datetime (accepts pd.Timestamp, datetime, or string)
        entry_price: Entry price
        exit_time: Exit datetime (accepts pd.Timestamp, datetime, or string)
        exit_price: Exit price
        quantity: Trade quantity/size
        trade_type: Type of trade (long or short)
        id: Optional trade identifier
        notes: Optional trade notes
        text: Optional tooltip text for the trade
    """

    entry_time: Union[pd.Timestamp, datetime, str, int, float]
    entry_price: Union[float, str, int]
    exit_time: Union[pd.Timestamp, datetime, str, int, float]
    exit_price: Union[float, str, int]
    quantity: Union[float, str, int]
    trade_type: Union[TradeType, str] = TradeType.LONG
    id: Optional[str] = None
    notes: Optional[str] = None
    text: Optional[str] = None

    def __post_init__(self):
        self.entry_price = float(self.entry_price)
        self.exit_price = float(self.exit_price)
        self.quantity = int(self.quantity)

        # Convert times to UTC timestamps
        self._entry_timestamp = to_utc_timestamp(self.entry_time)
        self._exit_timestamp = to_utc_timestamp(self.exit_time)

        # Ensure exit time is after entry time
        if isinstance(self._entry_timestamp, (int, float)) and isinstance(
            self._exit_timestamp, (int, float)
        ):
            if self._exit_timestamp <= self._entry_timestamp:
                raise ValueError("Exit time must be after entry time")
        elif isinstance(self._entry_timestamp, str) and isinstance(self._exit_timestamp, str):
            # Compare as strings for date strings
            if self._exit_timestamp <= self._entry_timestamp:
                raise ValueError("Exit time must be after entry time")

        # Convert trade type to enum
        if isinstance(self.trade_type, str):
            self.trade_type = TradeType(self.trade_type.lower())

        # Generate tooltip text if not provided
        if self.text is None:
            self.text = self.generate_tooltip_text()

    def generate_tooltip_text(self) -> str:
        """Generate tooltip text for the trade."""
        pnl = self.pnl
        pnl_pct = self.pnl_percentage
        win_loss = "Win" if pnl > 0 else "Loss"

        # Format dates
        from_utc_timestamp(self._entry_timestamp)
        from_utc_timestamp(self._exit_timestamp)

        tooltip_parts = [
            f"Entry: {self.entry_price:.2f}",
            f"Exit: {self.exit_price:.2f}",
            f"Qty: {self.quantity:.2f}",
            f"P&L: {pnl:.2f} ({pnl_pct:.1f}%)",
            f"{win_loss}",
        ]

        # Add custom notes if provided
        if self.notes:
            tooltip_parts.append(f"Notes: {self.notes}")

        return "\n".join(tooltip_parts)

    @property
    def entry_timestamp(self) -> Union[int, str]:
        """Get entry time as UTC timestamp."""
        return self._entry_timestamp

    @property
    def exit_timestamp(self) -> Union[int, str]:
        """Get exit time as UTC timestamp."""
        return self._exit_timestamp

    @property
    def pnl(self) -> float:
        """Calculate profit/loss for the trade."""
        if self.trade_type == TradeType.LONG:
            return (self.exit_price - self.entry_price) * self.quantity
        else:  # SHORT
            return (self.entry_price - self.exit_price) * self.quantity

    @property
    def pnl_percentage(self) -> float:
        """Calculate profit/loss percentage."""
        if self.trade_type == TradeType.LONG:
            return ((self.exit_price - self.entry_price) / self.entry_price) * 100
        else:  # SHORT
            return ((self.entry_price - self.exit_price) / self.entry_price) * 100

    @property
    def is_profitable(self) -> bool:
        """Check if trade is profitable."""
        return self.pnl > 0

    def to_markers(
        self,
        entry_color: Optional[str] = None,
        exit_color: Optional[str] = None,
        show_pnl: bool = True,
    ) -> list:
        """
        Convert trade to marker representations.

        Args:
            entry_color: Color for entry marker
            exit_color: Color for exit marker
            show_pnl: Whether to show P&L in marker text

        Returns:
            List of marker dictionaries
        """
        from ..data import Marker, MarkerPosition, MarkerShape

        # Default colors based on trade type and profit
        if entry_color is None:
            entry_color = "#2196F3" if self.trade_type == TradeType.LONG else "#FF9800"

        if exit_color is None:
            exit_color = "#4CAF50" if self.is_profitable else "#F44336"

        markers = []

        # Entry marker
        entry_text = f"Entry: ${self.entry_price:.2f}"
        if self.id:
            entry_text = f"{self.id} - {entry_text}"

        entry_marker = Marker(
            time=self._entry_timestamp,
            position=(
                MarkerPosition.BELOW_BAR
                if self.trade_type == TradeType.LONG
                else MarkerPosition.ABOVE_BAR
            ),
            shape=(
                MarkerShape.ARROW_UP
                if self.trade_type == TradeType.LONG
                else MarkerShape.ARROW_DOWN
            ),
            color=entry_color,
            text=entry_text,
        )
        markers.append(entry_marker)

        # Exit marker
        exit_text = f"Exit: ${self.exit_price:.2f}"
        if show_pnl:
            exit_text += f" (P&L: ${self.pnl:.2f}, {self.pnl_percentage:+.1f}%)"

        exit_marker = Marker(
            time=self._exit_timestamp,
            position=(
                MarkerPosition.ABOVE_BAR
                if self.trade_type == TradeType.LONG
                else MarkerPosition.BELOW_BAR
            ),
            shape=(
                MarkerShape.ARROW_DOWN
                if self.trade_type == TradeType.LONG
                else MarkerShape.ARROW_UP
            ),
            color=exit_color,
            text=exit_text,
        )
        markers.append(exit_marker)

        return markers

    def to_dict(self) -> dict:
        """Convert trade to dictionary for serialization."""
        return {
            "entryTime": self.entry_timestamp,
            "entryPrice": self.entry_price,
            "exitTime": self.exit_timestamp,
            "exitPrice": self.exit_price,
            "quantity": self.quantity,
            "tradeType": self.trade_type.value,
            "id": self.id,
            "notes": self.notes,
            "text": self.text,
            "pnl": self.pnl,
            "pnlPercentage": self.pnl_percentage,
            "isProfitable": self.is_profitable,
        }


@dataclass
class TradeVisualizationOptions:
    """Options for trade visualization."""

    style: TradeVisualization = TradeVisualization.BOTH

    # Marker options
    entry_marker_color_long: str = "#2196F3"
    entry_marker_color_short: str = "#FF9800"
    exit_marker_color_profit: str = "#4CAF50"
    exit_marker_color_loss: str = "#F44336"
    marker_size: int = 20
    show_pnl_in_markers: bool = True

    # Rectangle options
    rectangle_fill_opacity: float = 0.2
    rectangle_border_width: int = 1
    rectangle_color_profit: str = "#4CAF50"
    rectangle_color_loss: str = "#F44336"

    # Line options
    line_width: int = 2
    line_style: str = "dashed"
    line_color_profit: str = "#4CAF50"
    line_color_loss: str = "#F44336"

    # Arrow options
    arrow_size: int = 10
    arrow_color_profit: str = "#4CAF50"
    arrow_color_loss: str = "#F44336"

    # Zone options
    zone_opacity: float = 0.1
    zone_color_long: str = "#2196F3"
    zone_color_short: str = "#FF9800"
    zone_extend_bars: int = 2  # Extend zone by this many bars

    # Annotation options
    show_trade_id: bool = True
    show_quantity: bool = True
    show_trade_type: bool = True
    annotation_font_size: int = 12
    annotation_background: str = "rgba(255, 255, 255, 0.8)"

    def to_dict(self) -> dict:
        """Convert options to dictionary."""
        return {
            "style": self.style.value,
            "entry_marker_color_long": self.entry_marker_color_long,
            "entry_marker_color_short": self.entry_marker_color_short,
            "exit_marker_color_profit": self.exit_marker_color_profit,
            "exit_marker_color_loss": self.exit_marker_color_loss,
            "marker_size": self.marker_size,
            "show_pnl_in_markers": self.show_pnl_in_markers,
            "rectangle_fill_opacity": self.rectangle_fill_opacity,
            "rectangle_border_width": self.rectangle_border_width,
            "rectangle_color_profit": self.rectangle_color_profit,
            "rectangle_color_loss": self.rectangle_color_loss,
            "line_width": self.line_width,
            "line_style": self.line_style,
            "line_color_profit": self.line_color_profit,
            "line_color_loss": self.line_color_loss,
            "arrow_size": self.arrow_size,
            "arrow_color_profit": self.arrow_color_profit,
            "arrow_color_loss": self.arrow_color_loss,
            "zone_opacity": self.zone_opacity,
            "zone_color_long": self.zone_color_long,
            "zone_color_short": self.zone_color_short,
            "zone_extend_bars": self.zone_extend_bars,
            "show_trade_id": self.show_trade_id,
            "show_quantity": self.show_quantity,
            "show_trade_type": self.show_trade_type,
            "annotation_font_size": self.annotation_font_size,
            "annotation_background": self.annotation_background,
        }
