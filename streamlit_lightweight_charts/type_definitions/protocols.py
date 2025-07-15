"""Type protocols for streamlit-lightweight-charts."""

from datetime import datetime
from typing import Any, Dict, List, Optional, Protocol, Union, runtime_checkable

import pandas as pd


@runtime_checkable
class ChartDataProtocol(Protocol):
    """Protocol for chart data objects."""

    def to_dict(self) -> Dict[str, Any]:
        """Convert data to dictionary representation."""
        ...


@runtime_checkable
class TimeSeriesDataProtocol(Protocol):
    """Protocol for time series data objects."""

    time: Union[pd.Timestamp, datetime, str, int, float]

    def to_dict(self) -> Dict[str, Any]:
        """Convert data to dictionary representation."""
        ...


@runtime_checkable
class SeriesOptionsProtocol(Protocol):
    """Protocol for series options objects."""

    def to_dict(self) -> Dict[str, Any]:
        """Convert options to dictionary representation."""
        ...


@runtime_checkable
class ChartOptionsProtocol(Protocol):
    """Protocol for chart options objects."""

    def to_dict(self) -> Dict[str, Any]:
        """Convert options to dictionary representation."""
        ...


@runtime_checkable
class SeriesProtocol(Protocol):
    """Protocol for series objects."""

    data: List[ChartDataProtocol]
    options: Optional[SeriesOptionsProtocol]

    def to_dict(self) -> Dict[str, Any]:
        """Convert series to dictionary representation."""
        ...


@runtime_checkable
class ChartProtocol(Protocol):
    """Protocol for chart objects."""

    series: List[SeriesProtocol]
    options: Optional[ChartOptionsProtocol]

    def render(self, key: Optional[str] = None) -> Any:
        """Render the chart."""
        ...

    def to_dict(self) -> Dict[str, Any]:
        """Convert chart to dictionary representation."""
        ...


@runtime_checkable
class MarkerProtocol(Protocol):
    """Protocol for marker objects."""

    time: Union[pd.Timestamp, datetime, str, int, float]
    position: str
    shape: str
    color: str
    text: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert marker to dictionary representation."""
        ...


@runtime_checkable
class TradeProtocol(Protocol):
    """Protocol for trade objects."""

    entry_time: Union[pd.Timestamp, datetime, str, int, float]
    entry_price: float
    exit_time: Union[pd.Timestamp, datetime, str, int, float]
    exit_price: float
    quantity: float

    @property
    def pnl(self) -> float:
        """Get profit/loss."""
        ...

    @property
    def pnl_percentage(self) -> float:
        """Get profit/loss percentage."""
        ...

    @property
    def is_profitable(self) -> bool:
        """Check if trade is profitable."""
        ...

    def to_dict(self) -> Dict[str, Any]:
        """Convert trade to dictionary representation."""
        ...


@runtime_checkable
class AnnotationProtocol(Protocol):
    """Protocol for annotation objects."""

    time: Union[pd.Timestamp, datetime, str, int, float]
    price: float
    text: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert annotation to dictionary representation."""
        ...


@runtime_checkable
class TooltipProtocol(Protocol):
    """Protocol for tooltip objects."""

    content: str
    position: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert tooltip to dictionary representation."""
        ...


@runtime_checkable
class VisualizationOptionsProtocol(Protocol):
    """Protocol for visualization options objects."""

    def to_dict(self) -> Dict[str, Any]:
        """Convert options to dictionary representation."""
        ...


# Type aliases for better readability
ChartData = Union[ChartDataProtocol, Dict[str, Any]]
SeriesOptions = Union[SeriesOptionsProtocol, Dict[str, Any]]
ChartOptions = Union[ChartOptionsProtocol, Dict[str, Any]]
TimeValue = Union[pd.Timestamp, datetime, str, int, float]
NumericValue = Union[int, float]
