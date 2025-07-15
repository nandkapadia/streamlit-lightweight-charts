"""Series classes for streamlit-lightweight-charts."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Sequence, Union

from ..data import (
    BaselineData,
    HistogramData,
    Marker,
    OhlcData,
    SingleValueData,
    TradeVisualizationOptions,
)
from ..type_definitions import ChartType, LastPriceAnimationMode, LineStyle, LineType
from ..utils.trade_visualization import add_trades_to_series

if TYPE_CHECKING:
    from ..data.trade import Trade


@dataclass
class SeriesOptions(ABC):
    """Base class for series options."""

    price_scale_id: str = ""
    visible: bool = True
    price_line_visible: bool = True
    price_line_width: int = 1
    price_line_color: str = ""
    price_line_style: LineStyle = LineStyle.DASHED
    base_line_visible: bool = True
    base_line_width: int = 1
    base_line_color: str = "#B2B5BE"
    base_line_style: LineStyle = LineStyle.SOLID

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""

    def _base_dict(self) -> Dict[str, Any]:
        """Get base dictionary representation."""
        return {
            "priceScaleId": self.price_scale_id,
            "visible": self.visible,
            "priceLineVisible": self.price_line_visible,
            "priceLineWidth": self.price_line_width,
            "priceLineColor": self.price_line_color,
            "priceLineStyle": self.price_line_style.value,
            "baseLineVisible": self.base_line_visible,
            "baseLineWidth": self.base_line_width,
            "baseLineColor": self.base_line_color,
            "baseLineStyle": self.base_line_style.value,
        }


@dataclass
class AreaSeriesOptions(SeriesOptions):
    """Options for area series."""

    top_color: str = "rgba(46, 220, 135, 0.4)"
    bottom_color: str = "rgba(40, 221, 100, 0)"
    line_color: str = "#33D778"
    line_style: LineStyle = LineStyle.SOLID
    line_width: int = 3
    line_type: LineType = LineType.SIMPLE
    line_visible: bool = True
    point_markers_visible: bool = False
    point_markers_radius: Optional[int] = None
    crosshair_marker_visible: bool = True
    crosshair_marker_radius: int = 4
    crosshair_marker_border_color: str = ""
    crosshair_marker_background_color: str = ""
    crosshair_marker_border_width: int = 2
    last_price_animation: LastPriceAnimationMode = LastPriceAnimationMode.DISABLED

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        result = self._base_dict()
        result.update(
            {
                "topColor": self.top_color,
                "bottomColor": self.bottom_color,
                "lineColor": self.line_color,
                "lineStyle": self.line_style.value,
                "lineWidth": self.line_width,
                "lineType": self.line_type.value,
                "lineVisible": self.line_visible,
                "pointMarkersVisible": self.point_markers_visible,
                "crosshairMarkerVisible": self.crosshair_marker_visible,
                "crosshairMarkerRadius": self.crosshair_marker_radius,
                "crosshairMarkerBorderColor": self.crosshair_marker_border_color,
                "crosshairMarkerBackgroundColor": self.crosshair_marker_background_color,
                "crosshairMarkerBorderWidth": self.crosshair_marker_border_width,
                "lastPriceAnimation": self.last_price_animation.value,
            }
        )
        if self.point_markers_radius is not None:
            result["pointMarkersRadius"] = self.point_markers_radius
        return result


@dataclass
class LineSeriesOptions(SeriesOptions):
    """Options for line series."""

    color: str = "#2196F3"
    line_style: LineStyle = LineStyle.SOLID
    line_width: int = 3
    line_type: LineType = LineType.SIMPLE
    line_visible: bool = True
    point_markers_visible: bool = False
    point_markers_radius: Optional[int] = None
    crosshair_marker_visible: bool = True
    crosshair_marker_radius: int = 4
    crosshair_marker_border_color: str = ""
    crosshair_marker_background_color: str = ""
    crosshair_marker_border_width: int = 2
    last_price_animation: LastPriceAnimationMode = LastPriceAnimationMode.DISABLED

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        result = self._base_dict()
        result.update(
            {
                "color": self.color,
                "lineStyle": self.line_style.value,
                "lineWidth": self.line_width,
                "lineType": self.line_type.value,
                "lineVisible": self.line_visible,
                "pointMarkersVisible": self.point_markers_visible,
                "crosshairMarkerVisible": self.crosshair_marker_visible,
                "crosshairMarkerRadius": self.crosshair_marker_radius,
                "crosshairMarkerBorderColor": self.crosshair_marker_border_color,
                "crosshairMarkerBackgroundColor": self.crosshair_marker_background_color,
                "crosshairMarkerBorderWidth": self.crosshair_marker_border_width,
                "lastPriceAnimation": self.last_price_animation.value,
            }
        )
        if self.point_markers_radius is not None:
            result["pointMarkersRadius"] = self.point_markers_radius
        return result


@dataclass
class BarSeriesOptions(SeriesOptions):
    """Options for bar series."""

    up_color: str = "#26a69a"
    down_color: str = "#ef5350"
    open_visible: bool = True
    thin_bars: bool = True

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        result = self._base_dict()
        result.update(
            {
                "upColor": self.up_color,
                "downColor": self.down_color,
                "openVisible": self.open_visible,
                "thinBars": self.thin_bars,
            }
        )
        return result


@dataclass
class CandlestickSeriesOptions(SeriesOptions):
    """Options for candlestick series."""

    up_color: str = "#26a69a"
    down_color: str = "#ef5350"
    wick_visible: bool = True
    border_visible: bool = True
    border_color: str = "#378658"
    border_up_color: str = "#26a69a"
    border_down_color: str = "#ef5350"
    wick_color: str = "#737375"
    wick_up_color: str = "#26a69a"
    wick_down_color: str = "#ef5350"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        result = self._base_dict()
        result.update(
            {
                "upColor": self.up_color,
                "downColor": self.down_color,
                "wickVisible": self.wick_visible,
                "borderVisible": self.border_visible,
                "borderColor": self.border_color,
                "borderUpColor": self.border_up_color,
                "borderDownColor": self.border_down_color,
                "wickColor": self.wick_color,
                "wickUpColor": self.wick_up_color,
                "wickDownColor": self.wick_down_color,
            }
        )
        return result


@dataclass
class HistogramSeriesOptions(SeriesOptions):
    """Options for histogram series."""

    color: str = "#26a69a"
    base: float = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        result = self._base_dict()
        result.update({"color": self.color, "base": self.base})
        return result


@dataclass
class BaselineSeriesOptions(SeriesOptions):
    """Options for baseline series."""

    base_value: Dict[str, Union[str, float]] = field(
        default_factory=lambda: {"type": "price", "price": 0}
    )
    top_line_color: str = "rgba(38, 166, 154, 1)"
    top_fill_color1: str = "rgba(38, 166, 154, 0.28)"
    top_fill_color2: str = "rgba(38, 166, 154, 0.05)"
    bottom_line_color: str = "rgba(239, 83, 80, 1)"
    bottom_fill_color1: str = "rgba(239, 83, 80, 0.05)"
    bottom_fill_color2: str = "rgba(239, 83, 80, 0.28)"
    line_width: int = 3
    line_style: LineStyle = LineStyle.SOLID
    line_visible: bool = True
    point_markers_visible: bool = False
    point_markers_radius: Optional[int] = None
    crosshair_marker_visible: bool = True
    crosshair_marker_radius: int = 4
    crosshair_marker_border_color: str = ""
    crosshair_marker_background_color: str = ""
    crosshair_marker_border_width: int = 2
    last_price_animation: LastPriceAnimationMode = LastPriceAnimationMode.DISABLED

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        result = self._base_dict()
        result.update(
            {
                "baseValue": self.base_value,
                "topLineColor": self.top_line_color,
                "topFillColor1": self.top_fill_color1,
                "topFillColor2": self.top_fill_color2,
                "bottomLineColor": self.bottom_line_color,
                "bottomFillColor1": self.bottom_fill_color1,
                "bottomFillColor2": self.bottom_fill_color2,
                "lineWidth": self.line_width,
                "lineStyle": self.line_style.value,
                "lineVisible": self.line_visible,
                "pointMarkersVisible": self.point_markers_visible,
                "crosshairMarkerVisible": self.crosshair_marker_visible,
                "crosshairMarkerRadius": self.crosshair_marker_radius,
                "crosshairMarkerBorderColor": self.crosshair_marker_border_color,
                "crosshairMarkerBackgroundColor": self.crosshair_marker_background_color,
                "crosshairMarkerBorderWidth": self.crosshair_marker_border_width,
                "lastPriceAnimation": self.last_price_animation.value,
            }
        )
        if self.point_markers_radius is not None:
            result["pointMarkersRadius"] = self.point_markers_radius
        return result


class Series(ABC):
    """Base class for all series types."""

    def __init__(
        self,
        data: Sequence[Union[SingleValueData, OhlcData, HistogramData, BaselineData]],
        options: Optional[SeriesOptions] = None,
        markers: Optional[List[Marker]] = None,
        price_scale: Optional[Dict[str, Any]] = None,
    ):
        """Initialize a series."""
        self.data = list(data)
        self.options = options or self._default_options()
        self.markers = markers or []
        self.price_scale = price_scale

    @property
    @abstractmethod
    def chart_type(self) -> ChartType:
        """Get the chart type for this series."""

    @abstractmethod
    def _default_options(self) -> SeriesOptions:
        """Get default options for this series type."""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        # Handle data items that might be dictionaries or data model objects
        data_items = []
        for d in self.data:
            if hasattr(d, "to_dict"):
                data_items.append(d.to_dict())
            else:
                data_items.append(d)  # Assume it's already a dictionary

        # Handle options that might be SeriesOptions objects or plain dictionaries
        if hasattr(self.options, "to_dict"):
            options_dict = self.options.to_dict()
        else:
            options_dict = self.options  # Assume it's already a dictionary

        result = {
            "type": self.chart_type.value,
            "data": data_items,
            "options": options_dict,
        }

        if self.markers:
            result["markers"] = [m.to_dict() for m in self.markers]

        if self.price_scale:
            result["priceScale"] = self.price_scale

        return result

    def to_frontend_config(self) -> Dict[str, Any]:
        """Convert to frontend-compatible configuration."""
        return self.to_dict()


class AreaSeries(Series):
    """Area series implementation."""

    @property
    def chart_type(self) -> ChartType:
        """Get the chart type for this series."""
        return ChartType.AREA

    def __init__(
        self,
        data: Sequence[SingleValueData],
        options: Optional[AreaSeriesOptions] = None,
        markers: Optional[List[Marker]] = None,
        price_scale: Optional[Dict[str, Any]] = None,
    ):
        """Initialize an area series."""
        super().__init__(data, options, markers, price_scale)

    def _default_options(self) -> AreaSeriesOptions:
        """Get default options for area series."""
        return AreaSeriesOptions()


class LineSeries(Series):
    """Line series implementation."""

    @property
    def chart_type(self) -> ChartType:
        """Get the chart type for this series."""
        return ChartType.LINE

    def __init__(
        self,
        data: Sequence[SingleValueData],
        options: Optional[LineSeriesOptions] = None,
        markers: Optional[List[Marker]] = None,
        price_scale: Optional[Dict[str, Any]] = None,
    ):
        """Initialize a line series."""
        super().__init__(data, options, markers, price_scale)

    def _default_options(self) -> LineSeriesOptions:
        """Get default options for line series."""
        return LineSeriesOptions()


class BarSeries(Series):
    """Bar series implementation."""

    @property
    def chart_type(self) -> ChartType:
        """Get the chart type for this series."""
        return ChartType.BAR

    def __init__(
        self,
        data: Sequence[OhlcData],
        options: Optional[BarSeriesOptions] = None,
        markers: Optional[List[Marker]] = None,
        price_scale: Optional[Dict[str, Any]] = None,
    ):
        """Initialize a bar series."""
        super().__init__(data, options, markers, price_scale)

    def _default_options(self) -> BarSeriesOptions:
        """Get default options for bar series."""
        return BarSeriesOptions()


class CandlestickSeries(Series):
    """Candlestick series implementation."""

    @property
    def chart_type(self) -> ChartType:
        """Get the chart type for this series."""
        return ChartType.CANDLESTICK

    def __init__(
        self,
        data: Sequence[OhlcData],
        options: Optional[CandlestickSeriesOptions] = None,
        markers: Optional[List[Marker]] = None,
        price_scale: Optional[Dict[str, Any]] = None,
        trades: Optional[List["Trade"]] = None,
        trade_visualization_options: Optional["TradeVisualizationOptions"] = None,
    ):
        """
        Initialize a candlestick series.

        Args:
            data: List of OHLC data points
            options: Candlestick series options
            markers: Optional list of markers
            price_scale: Optional price scale configuration
            trades: Optional list of trades to visualize
            trade_visualization_options: Options for trade visualization
        """
        super().__init__(data, options, markers, price_scale)
        self.trades = trades or []
        self.trade_visualization_options = trade_visualization_options

    def _default_options(self) -> CandlestickSeriesOptions:
        """Get default options for candlestick series."""
        return CandlestickSeriesOptions()

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary representation.

        Includes trade visualizations if trades are present.
        """
        result = super().to_dict()

        # Add trade visualizations if trades are present
        if self.trades:
            # Use default options if not provided
            trade_options = self.trade_visualization_options or TradeVisualizationOptions()
            # Add trade visualizations to the series
            result = add_trades_to_series(result, self.trades, trade_options)

        return result

    def to_frontend_config(self) -> Dict[str, Any]:
        result = self.to_dict()
        return result


class HistogramSeries(Series):
    """Histogram series implementation."""

    @property
    def chart_type(self) -> ChartType:
        """Get the chart type for this series."""
        return ChartType.HISTOGRAM

    def __init__(
        self,
        data: Sequence[HistogramData],
        options: Optional[HistogramSeriesOptions] = None,
        markers: Optional[List[Marker]] = None,
        price_scale: Optional[Dict[str, Any]] = None,
    ):
        """Initialize a histogram series."""
        super().__init__(data, options, markers, price_scale)

    def _default_options(self) -> HistogramSeriesOptions:
        """Get default options for histogram series."""
        return HistogramSeriesOptions()


class BaselineSeries(Series):
    """Baseline series implementation."""

    @property
    def chart_type(self) -> ChartType:
        """Get the chart type for this series."""
        return ChartType.BASELINE

    def __init__(
        self,
        data: Sequence[BaselineData],
        options: Optional[BaselineSeriesOptions] = None,
        markers: Optional[List[Marker]] = None,
        price_scale: Optional[Dict[str, Any]] = None,
    ):
        """Initialize a baseline series."""
        super().__init__(data, options, markers, price_scale)

    def _default_options(self) -> BaselineSeriesOptions:
        """Get default options for baseline series."""
        return BaselineSeriesOptions()
