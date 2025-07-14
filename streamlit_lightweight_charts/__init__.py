import os
from typing import Dict, List, Optional, Any, Union, Callable
from enum import Enum
import streamlit as st
import streamlit.components.v1 as components

_COMPONENT_NAME = "streamlit_lightweight_charts"
_RELEASE = True

# Enums for better type safety
class SeriesType(str, Enum):
    AREA = "Area"
    BASELINE = "Baseline"
    HISTOGRAM = "Histogram"
    LINE = "Line"
    BAR = "Bar"
    CANDLESTICK = "Candlestick"


class PriceScaleMode(int, Enum):
    NORMAL = 0
    LOGARITHMIC = 1
    PERCENTAGE = 2
    INDEXED_TO_100 = 3


class CrosshairMode(int, Enum):
    NORMAL = 0
    MAGNET = 1


class LineStyle(int, Enum):
    SOLID = 0
    DOTTED = 1
    DASHED = 2
    LARGE_DASHED = 3

class TradeType(str, Enum):
    BUY = "buy"
    SELL = "sell"
    LONG = "long"
    SHORT = "short"

class MarkerShape(str, Enum):
    ARROW_UP = "arrowUp"
    ARROW_DOWN = "arrowDown"
    CIRCLE = "circle"
    SQUARE = "square"
    TRIANGLE_UP = "triangleUp"
    TRIANGLE_DOWN = "triangleDown"
    FLAG = "flag"


class PriceLineSource(int, Enum):
    LAST_VISIBLE = 0
    LAST_BAR = 1


parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "frontend", "build")

if not _RELEASE:
    _component_func = components.declare_component(
        _COMPONENT_NAME,
        url="http://localhost:3001",
    )
else:
    _component_func = components.declare_component(_COMPONENT_NAME, path=build_dir)


class Chart:
    """
    Represents a single chart instance with its configuration and series.
    """

    def __init__(
        self,
        width: Optional[int] = None,
        height: Optional[int] = None,
        layout: Optional[Dict[str, Any]] = None,
        grid: Optional[Dict[str, Any]] = None,
        crosshair: Optional[Dict[str, Any]] = None,
        time_scale: Optional[Dict[str, Any]] = None,
        right_price_scale: Optional[Dict[str, Any]] = None,
        left_price_scale: Optional[Dict[str, Any]] = None,
        overlay_price_scales: Optional[Dict[str, Any]] = None,
        watermark: Optional[Dict[str, Any]] = None,
        range_switcher: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        """
        Initialize a chart with configuration options.

        All parameters match the lightweight-charts ChartOptions interface:
        https://tradingview.github.io/lightweight-charts/docs/api/interfaces/ChartOptions
        """
        self.options = {
            k: v
            for k, v in {
                "width": width,
                "height": height,
                "layout": layout,
                "grid": grid,
                "crosshair": crosshair,
                "timeScale": time_scale,
                "rightPriceScale": right_price_scale,
                "leftPriceScale": left_price_scale,
                "overlayPriceScales": overlay_price_scales,
                "watermark": watermark,
                "rangeSwitcher": range_switcher,
                **kwargs,
            }.items()
            if v is not None
        }
        self.series: List[Dict[str, Any]] = []
        self.price_lines: List[Dict[str, Any]] = []
        self.trades: List[Dict[str, Any]] = []
        self.chart_id: Optional[str] = None

    def add_series(
        self,
        series_type: Union[SeriesType, str],
        chart_data: List[Dict[str, Any]],
        name: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None,
        price_scale_id: Optional[str] = None,
        price_scale: Optional[Dict[str, Any]] = None,
        markers: Optional[List[Dict[str, Any]]] = None,
    ) -> "Chart":
        """
        Add a series to the chart.

        Args:
            series_type: Type of series (Area, Line, Candlestick, etc.)
            data: List of data points for the series
            name: Optional name for the series
            options: Series-specific options
            price_scale_id: ID of the price scale to use
            price_scale: Price scale configuration
            markers: List of markers to add to the series
        """
        series_config = {
            "type": (
                series_type.value
                if isinstance(series_type, SeriesType)
                else series_type
            ),
            "data": chart_data,
            "options": options or {},
        }

        if name:
            series_config["name"] = name
        if price_scale_id is not None:
            series_config["options"]["priceScaleId"] = price_scale_id
        if price_scale:
            series_config["priceScale"] = price_scale
        if markers:
            series_config["markers"] = markers

        self.series.append(series_config)
        return self

    def add_price_line(
        self,
        price: float,
        color: str = "#000",
        line_width: int = 1,
        line_style: LineStyle = LineStyle.SOLID,
        axis_label_visible: bool = True,
        title: str = "",
    ) -> "Chart":
        """Add a horizontal price line to the chart."""
        self.price_lines.append(
            {
                "price": price,
                "color": color,
                "lineWidth": line_width,
                "lineStyle": line_style.value,
                "axisLabelVisible": axis_label_visible,
                "title": title,
            }
        )
        return self

    def add_trade(
        self,
        trade_type: Union[TradeType, str],
        entry_time: str,
        entry_price: float,
        exit_time: Optional[str] = None,
        exit_price: Optional[float] = None,
        quantity: Optional[float] = None,
        symbol: Optional[str] = None,
        show_markers: bool = True,
        show_rectangle: bool = True,
        marker_color: Optional[str] = None,
        rectangle_color: Optional[str] = None,
        **kwargs
    ) -> "Chart":
        """
        Add a trade to the chart with markers and/or rectangle overlay.
        
        Args:
            trade_type: Type of trade (buy, sell, long, short)
            entry_time: Entry time in 'YYYY-MM-DD' format
            entry_price: Entry price
            exit_time: Exit time in 'YYYY-MM-DD' format (optional for open trades)
            exit_price: Exit price (optional for open trades)
            quantity: Trade quantity
            symbol: Trading symbol
            show_markers: Whether to show entry/exit markers
            show_rectangle: Whether to show trade rectangle
            marker_color: Custom color for markers
            rectangle_color: Custom color for rectangle
            **kwargs: Additional trade properties
        """
        # Determine colors based on trade type
        if marker_color is None:
            marker_color = "#26a69a" if trade_type in [TradeType.BUY, TradeType.LONG] else "#ef5350"
        
        if rectangle_color is None:
            rectangle_color = "rgba(38, 166, 154, 0.1)" if trade_type in [TradeType.BUY, TradeType.LONG] else "rgba(239, 83, 80, 0.1)"
        
        # Create trade configuration
        trade_config = {
            "type": trade_type.value if isinstance(trade_type, TradeType) else trade_type,
            "entryTime": entry_time,
            "entryPrice": entry_price,
            "showMarkers": show_markers,
            "showRectangle": show_rectangle,
            "markerColor": marker_color,
            "rectangleColor": rectangle_color,
            **kwargs
        }
        
        if exit_time:
            trade_config["exitTime"] = exit_time
        if exit_price:
            trade_config["exitPrice"] = exit_price
        if quantity:
            trade_config["quantity"] = quantity
        if symbol:
            trade_config["symbol"] = symbol
        
        self.trades.append(trade_config)
        return self

    def add_trade_marker(
        self,
        time: str,
        price: float,
        trade_type: Union[TradeType, str],
        shape: Union[MarkerShape, str] = MarkerShape.ARROW_UP,
        text: Optional[str] = None,
        color: Optional[str] = None,
        size: int = 2,
        **kwargs
    ) -> "Chart":
        """
        Add a single trade marker to the chart.
        
        Args:
            time: Time in 'YYYY-MM-DD' format
            price: Price level
            trade_type: Type of trade (buy, sell, long, short)
            shape: Marker shape
            text: Optional text to display
            color: Marker color
            size: Marker size
            **kwargs: Additional marker properties
        """
        if color is None:
            color = "#26a69a" if trade_type in [TradeType.BUY, TradeType.LONG] else "#ef5350"
        
        if shape is None:
            shape = MarkerShape.ARROW_UP if trade_type in [TradeType.BUY, TradeType.LONG] else MarkerShape.ARROW_DOWN
        
        marker_config = {
            "time": time,
            "position": "aboveBar" if trade_type in [TradeType.BUY, TradeType.LONG] else "belowBar",
            "color": color,
            "shape": shape.value if isinstance(shape, MarkerShape) else shape,
            "size": size,
            **kwargs
        }
        
        if text:
            marker_config["text"] = text
        
        # Add marker to the first series (usually candlestick)
        if self.series:
            if "markers" not in self.series[0]:
                self.series[0]["markers"] = []
            self.series[0]["markers"].append(marker_config)
        
        return self

    def add_range_switcher(
        self,
        ranges: Optional[List[Dict[str, Any]]] = None,
        position: str = "top-right",
        visible: bool = True,
        default_range: Optional[str] = None,
        **kwargs
    ) -> "Chart":
        """
        Add a range switcher to the chart.
        
        Args:
            ranges: List of range configurations. Each range should have:
                   - label: Display text (e.g., "1D", "1W", "1M")
                   - seconds: Duration in seconds (None for "ALL")
            position: Position of the range switcher ("top-left", "top-right", "bottom-left", "bottom-right")
            visible: Whether the range switcher is visible
            default_range: Default selected range label
            **kwargs: Additional range switcher options
        """
        if ranges is None:
            ranges = [
                {"label": "1D", "seconds": 86400},
                {"label": "1W", "seconds": 604800},
                {"label": "1M", "seconds": 2592000},
                {"label": "3M", "seconds": 7776000},
                {"label": "6M", "seconds": 15552000},
                {"label": "1Y", "seconds": 31536000},
                {"label": "ALL", "seconds": None}
            ]
        
        self.options["rangeSwitcher"] = {
            "ranges": ranges,
            "position": position,
            "visible": visible,
            "defaultRange": default_range,
            **kwargs
        }
        return self

    def to_dict(self) -> Dict[str, Any]:
        """Convert the chart to a dictionary for serialization."""
        result = {"chart": self.options, "series": self.series}
        if self.price_lines:
            result["priceLines"] = self.price_lines
        if self.trades:
            result["trades"] = self.trades
        if self.chart_id:
            result["chartId"] = self.chart_id
        return result


class ChartGroup:
    """
    Manages a group of synchronized charts.
    """

    def __init__(
        self,
        sync_enabled: bool = True,
        sync_crosshair: bool = True,
        sync_time_range: bool = True,
    ):
        self.charts: List[Chart] = []
        self.sync_config = {
            "enabled": sync_enabled,
            "crosshair": sync_crosshair,
            "timeRange": sync_time_range,
        }
        self.callbacks: Dict[str, Any] = {}

    def add_chart(self, chart: Chart) -> "ChartGroup":
        """Add a chart to the group."""
        chart.chart_id = f"chart_{len(self.charts)}"
        self.charts.append(chart)
        return self

    def on_click(self, callback: Callable) -> "ChartGroup":
        """Register a click event callback."""
        self.callbacks["onClick"] = callback
        return self

    def on_crosshair_move(self, callback: Callable) -> "ChartGroup":
        """Register a crosshair move event callback."""
        self.callbacks["onCrosshairMove"] = callback
        return self

    def on_visible_time_range_change(self, callback: Callable) -> "ChartGroup":
        """Register a visible time range change callback."""
        self.callbacks["onVisibleTimeRangeChange"] = callback
        return self
    
    def on_range_switcher_change(self, callback: Callable) -> "ChartGroup":
        """Register a range switcher change callback."""
        self.callbacks["onRangeSwitcherChange"] = callback
        return self
    
    def on_trade_click(self, callback: Callable) -> "ChartGroup":
        """Register a trade click callback."""
        self.callbacks["onTradeClick"] = callback
        return self

    def render(self, key: Optional[str] = None) -> Any:
        """Render the chart group."""
        config = {
            "charts": [chart.to_dict() for chart in self.charts],
            "syncConfig": self.sync_config,
            "callbacks": list(self.callbacks.keys()),
        }

        # Handle callbacks through session state
        if self.callbacks and key:
            callback_key = f"{key}_callbacks"
            if callback_key not in st.session_state:
                st.session_state[callback_key] = {}

        result = _component_func(config=config, key=key)

        # Process callbacks
        if result and self.callbacks and key:
            for event_type, callback in self.callbacks.items():
                if event_type in result:
                    callback(result[event_type])

        return result


def renderLightweightCharts(
    charts: Union[List[Dict], ChartGroup], key: Optional[str] = None
) -> Any:
    """
    Render lightweight charts.

    This function maintains backward compatibility while supporting the new API.

    Parameters:
    -----------
    charts: List[Dict] or ChartGroup
        Either a list of chart configurations (legacy) or a ChartGroup instance
    key: str
        Unique key for the component

    Returns:
    --------
    Any data returned from the frontend component
    """
    if isinstance(charts, ChartGroup):
        return charts.render(key)
    else:
        # Legacy mode - convert to new format
        config = {
            "charts": charts,
            "syncConfig": {
                "enabled": len(charts) > 1,
                "crosshair": False,  # Legacy mode doesn't have full crosshair sync
                "timeRange": True,
            },
        }
        return _component_func(config=config, key=key)


# Utility functions for common chart patterns
def create_candlestick_chart(
    chart_data: List[Dict[str, Any]],
    width: Optional[int] = None,
    height: Optional[int] = None,
    with_range_switcher: bool = False,
    **kwargs,
) -> Chart:
    """Create a candlestick chart with sensible defaults."""
    chart = Chart(
        width=width,
        height=height,
        layout={"background": {"type": "solid", "color": "white"}},
        **kwargs,
    )
    chart.add_series(
        SeriesType.CANDLESTICK,
        chart_data,
        options={
            "upColor": "#26a69a",
            "downColor": "#ef5350",
            "borderVisible": False,
            "wickUpColor": "#26a69a",
            "wickDownColor": "#ef5350",
        },
    )
    
    if with_range_switcher:
        chart.add_range_switcher()
    
    return chart


def create_trade_chart(
    chart_data: List[Dict[str, Any]],
    trades: Optional[List[Dict[str, Any]]] = None,
    width: Optional[int] = None,
    height: Optional[int] = None,
    show_trade_rectangles: bool = True,
    show_trade_markers: bool = True,
    **kwargs,
) -> Chart:
    """
    Create a candlestick chart optimized for displaying trades.
    
    Args:
        chart_data: OHLCV data
        trades: List of trade dictionaries with entry/exit info
        width: Chart width
        height: Chart height
        show_trade_rectangles: Whether to show trade rectangles
        show_trade_markers: Whether to show trade markers
        **kwargs: Additional chart options
    """
    chart = create_candlestick_chart(chart_data, width, height, **kwargs)
    
    if trades:
        for trade in trades:
            chart.add_trade(
                trade_type=trade.get("type", TradeType.BUY),
                entry_time=trade["entry_time"],
                entry_price=trade["entry_price"],
                exit_time=trade.get("exit_time"),
                exit_price=trade.get("exit_price"),
                quantity=trade.get("quantity"),
                symbol=trade.get("symbol"),
                show_markers=show_trade_markers,
                show_rectangle=show_trade_rectangles,
                marker_color=trade.get("marker_color"),
                rectangle_color=trade.get("rectangle_color")
            )
    
    return chart


def create_volume_chart(
    chart_data: List[Dict[str, Any]], width: Optional[int] = None, height: int = 100, **kwargs
) -> Chart:
    """Create a volume histogram chart."""
    chart = Chart(width=width, height=height, time_scale={"visible": False}, **kwargs)
    chart.add_series(
        SeriesType.HISTOGRAM,
        chart_data,
        options={"color": "#26a69a", "priceFormat": {"type": "volume"}},
        price_scale_id="",
        price_scale={"scaleMargins": {"top": 0, "bottom": 0}},
    )
    return chart


def create_line_indicator(
    chart_data: List[Dict[str, Any]],
    name: str,
    color: str = "#2962FF",
    width: Optional[int] = None,
    height: int = 200,
    **kwargs,
) -> Chart:
    """Create a line indicator chart."""
    chart = Chart(width=width, height=height, **kwargs)
    chart.add_series(
        SeriesType.LINE, chart_data, name=name, options={"color": color, "lineWidth": 2}
    )
    return chart


def create_rsi_chart(
    chart_data: List[Dict[str, Any]],
    width: Optional[int] = None,
    height: int = 150,
    overbought: float = 70,
    oversold: float = 30,
    **kwargs,
) -> Chart:
    """Create an RSI indicator chart with overbought/oversold lines."""
    chart = Chart(
        width=width,
        height=height,
        time_scale={"visible": False},
        right_price_scale={"scaleMargins": {"top": 0.1, "bottom": 0.1}},
        **kwargs,
    )

    # Add RSI line
    chart.add_series(
        SeriesType.LINE, chart_data, name="RSI", options={"color": "#9C27B0", "lineWidth": 2}
    )

    # Add overbought/oversold lines
    chart.add_price_line(
        price=overbought,
        color="#FF5252",
        line_width=1,
        line_style=LineStyle.DOTTED,
        title="Overbought",
    )
    chart.add_price_line(
        price=oversold,
        color="#4CAF50",
        line_width=1,
        line_style=LineStyle.DOTTED,
        title="Oversold",
    )

    return chart


def create_macd_chart(
    macd_data: List[Dict[str, Any]],
    signal_data: List[Dict[str, Any]],
    histogram_data: List[Dict[str, Any]],
    width: Optional[int] = None,
    height: int = 200,
    **kwargs,
) -> Chart:
    """Create a MACD indicator chart with signal line and histogram."""
    chart = Chart(width=width, height=height, **kwargs)

    # MACD line
    chart.add_series(
        SeriesType.LINE,
        macd_data,
        name="MACD",
        options={"color": "#2196F3", "lineWidth": 2},
    )

    # Signal line
    chart.add_series(
        SeriesType.LINE,
        signal_data,
        name="Signal",
        options={"color": "#FF9800", "lineWidth": 2},
    )

    # Histogram
    chart.add_series(
        SeriesType.HISTOGRAM,
        histogram_data,
        name="Histogram",
        options={"color": "#26a69a"},
    )

    # Zero line
    chart.add_price_line(
        price=0, color="#666", line_width=1, line_style=LineStyle.SOLID
    )

    return chart


# Theme presets
class Themes:
    """Predefined chart themes."""

    LIGHT = {
        "layout": {
            "background": {"type": "solid", "color": "white"},
            "textColor": "black",
        },
        "grid": {
            "vertLines": {"color": "rgba(197, 203, 206, 0.5)"},
            "horzLines": {"color": "rgba(197, 203, 206, 0.5)"},
        },
        "crosshair": {"color": "rgba(38, 38, 38, 0.8)"},
    }

    DARK = {
        "layout": {
            "background": {"type": "solid", "color": "#131722"},
            "textColor": "#d1d4dc",
        },
        "grid": {
            "vertLines": {"color": "rgba(42, 46, 57, 0.6)"},
            "horzLines": {"color": "rgba(42, 46, 57, 0.6)"},
        },
        "crosshair": {"color": "rgba(198, 198, 198, 0.8)"},
    }

    TRADING_VIEW = {
        "layout": {
            "background": {"type": "solid", "color": "#1e222d"},
            "textColor": "#9598a1",
        },
        "grid": {
            "vertLines": {"color": "rgba(42, 46, 57, 0)"},
            "horzLines": {"color": "rgba(42, 46, 57, 0.6)"},
        },
        "crosshair": {"color": "rgba(152, 152, 152, 0.8)"},
    }

    BINANCE = {
        "layout": {
            "background": {"type": "solid", "color": "#161a1e"},
            "textColor": "#848e9c",
        },
        "grid": {
            "vertLines": {"color": "rgba(132, 142, 156, 0.1)"},
            "horzLines": {"color": "rgba(132, 142, 156, 0.1)"},
        },
        "crosshair": {"color": "rgba(132, 142, 156, 0.8)"},
    }


# Export utility for saving chart screenshots
def export_chart_options(
    background_color: str = "white",
    width: int = 1920,
    height: int = 1080,
    price_scale_width: int = 50,
    time_scale_height: int = 50,
) -> Dict[str, Any]:
    """
    Generate export options for chart screenshots.

    Note: Actual export functionality requires additional frontend implementation.
    """
    return {
        "backgroundColor": background_color,
        "width": width,
        "height": height,
        "priceScaleWidth": price_scale_width,
        "timeScaleHeight": time_scale_height,
    }


# Data formatting utilities
def format_df_for_chart(
    df: Any,  # pandas DataFrame
    time_col: str = "time",
    open_col: str = "open",
    high_col: str = "high",
    low_col: str = "low",
    close_col: str = "close",
    volume_col: Optional[str] = "volume",
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Format a pandas DataFrame for chart consumption.

    Returns a dictionary with formatted data for candlestick and volume series.
    """
    candlestick_data = []
    volume_data = []

    for _, row in df.iterrows():
        time_str = (
            row[time_col].strftime("%Y-%m-%d")
            if hasattr(row[time_col], "strftime")
            else str(row[time_col])
        )

        # Candlestick data
        candlestick_data.append(
            {
                "time": time_str,
                "open": float(row[open_col]),
                "high": float(row[high_col]),
                "low": float(row[low_col]),
                "close": float(row[close_col]),
            }
        )

        # Volume data if available
        if volume_col and volume_col in row:
            volume_data.append({"time": time_str, "value": float(row[volume_col])})

    return {"candlestick": candlestick_data, "volume": volume_data}


def format_series_data(
    timestamps: List[Any], values: List[float], time_format: str = "%Y-%m-%d"
) -> List[Dict[str, Any]]:
    """Format time series data for line/area charts."""
    plotting_data = []
    for time, value in zip(timestamps, values):
        if hasattr(time, "strftime"):
            time_str = time.strftime(time_format)
        else:
            time_str = str(time)

        plotting_data.append({"time": time_str, "value": float(value)})

    return plotting_data


if not _RELEASE:
    import dataSamples as data

    chartOptions = {
        "width": 600,
        "layout": {
            "textColor": "black",
            "background": {"type": "solid", "color": "white"},
        },
    }

    # AREA chart
    seriesAreaChart = [
        {"type": "Area", "data": data.seriesSingleValueData, "options": {}}
    ]
    st.subheader("Area Chart")
    renderLightweightCharts(
        [
            {
                "chart": chartOptions,
                "series": seriesAreaChart,
            }
        ],
        "area",
    )
    st.markdown("---")

    # BASELINE chart
    seriesBaselineChart = [
        {
            "type": "Baseline",
            "data": data.seriesBaselineChart,
            "options": {
                "baseValue": {"type": "price", "price": 25},
                "topLineColor": "rgba( 38, 166, 154, 1)",
                "topFillColor1": "rgba( 38, 166, 154, 0.28)",
                "topFillColor2": "rgba( 38, 166, 154, 0.05)",
                "bottomLineColor": "rgba( 239, 83, 80, 1)",
                "bottomFillColor1": "rgba( 239, 83, 80, 0.05)",
                "bottomFillColor2": "rgba( 239, 83, 80, 0.28)",
            },
        }
    ]
    st.subheader("Baseline Chart")
    renderLightweightCharts(
        [{"chart": chartOptions, "series": seriesBaselineChart}], "baseline"
    )
    st.markdown("---")

    # LINE charts
    seriesLineChart = [
        {"type": "Line", "data": data.seriesSingleValueData, "options": {}}
    ]
    st.subheader("Line Chart")
    renderLightweightCharts(
        [{"chart": chartOptions, "series": seriesLineChart}], "line"
    )
    st.markdown("---")

    # HISTOGRAM chart
    seriesHistogramChart = [
        {
            "type": "Histogram",
            "data": data.seriesHistogramChart,
            "options": {"color": "#26a69a"},
        }
    ]
    st.subheader("Histogram Chart")
    renderLightweightCharts(
        [{"chart": chartOptions, "series": seriesHistogramChart}], "histogram"
    )
    st.markdown("---")

    # BAR chart
    seriesBarChart = [
        {
            "type": "Bar",
            "data": data.seriesBarChart,
            "options": {"upColor": "#26a69a", "downColor": "#ef5350"},
        }
    ]
    st.subheader("Bar Chart")
    renderLightweightCharts([{"chart": chartOptions, "series": seriesBarChart}], "bar")
    st.markdown("---")

    # CANDLESTICK chart
    seriesCandlestickChart = [
        {
            "type": "Candlestick",
            "data": data.seriesCandlestickChart,
            "options": {
                "upColor": "#26a69a",
                "downColor": "#ef5350",
                "borderVisible": False,
                "wickUpColor": "#26a69a",
                "wickDownColor": "#ef5350",
            },
        }
    ]
    st.subheader("Candlestick Chart")
    renderLightweightCharts(
        [{"chart": chartOptions, "series": seriesCandlestickChart}], "candlestick"
    )
    st.markdown("---")

    # OVERLAID AREA chart
    overlaidAreaSeriesOptions = {
        # "width": 600,
        "height": 400,
        "rightPriceScale": {
            "scaleMargins": {
                "top": 0.1,
                "bottom": 0.1,
            },
            "mode": 2,  # PriceScaleMode: 0-Normal, 1-Logarithmic, 2-Percentage, 3-IndexedTo100
            "borderColor": "rgba(197, 203, 206, 0.4)",
        },
        "timeScale": {
            "borderColor": "rgba(197, 203, 206, 0.4)",
        },
        "layout": {
            "background": {"type": "solid", "color": "#100841"},
            "textColor": "#ffffff",
        },
        "grid": {
            "vertLines": {
                "color": "rgba(197, 203, 206, 0.4)",
                "style": 1,  # LineStyle: 0-Solid, 1-Dotted, 2-Dashed, 3-LargeDashed
            },
            "horzLines": {
                "color": "rgba(197, 203, 206, 0.4)",
                "style": 1,  # LineStyle: 0-Solid, 1-Dotted, 2-Dashed, 3-LargeDashed
            },
        },
    }

    seriesOverlaidChart = [
        {
            "type": "Area",
            "data": data.seriesMultipleChartArea01,
            "options": {
                "topColor": "rgba(255, 192, 0, 0.7)",
                "bottomColor": "rgba(255, 192, 0, 0.3)",
                "lineColor": "rgba(255, 192, 0, 1)",
                "lineWidth": 2,
            },
            "markers": [
                {
                    "time": "2019-04-08",
                    "position": "aboveBar",
                    "color": "rgba(255, 192, 0, 1)",
                    "shape": "arrowDown",
                    "text": "H",
                    "size": 3,
                },
                {
                    "time": "2019-05-13",
                    "position": "belowBar",
                    "color": "rgba(255, 192, 0, 1)",
                    "shape": "arrowUp",
                    "text": "L",
                    "size": 3,
                },
            ],
        },
        {
            "type": "Area",
            "data": data.seriesMultipleChartArea02,
            "options": {
                "topColor": "rgba(67, 83, 254, 0.7)",
                "bottomColor": "rgba(67, 83, 254, 0.3)",
                "lineColor": "rgba(67, 83, 254, 1)",
                "lineWidth": 2,
            },
            "markers": [
                {
                    "time": "2019-05-03",
                    "position": "aboveBar",
                    "color": "rgba(67, 83, 254, 1)",
                    "shape": "arrowDown",
                    "text": "PEAK",
                    "size": 3,
                },
            ],
        },
    ]
    st.subheader("Overlaid Series with Markers")
    renderLightweightCharts(
        [{"chart": overlaidAreaSeriesOptions, "series": seriesOverlaidChart}],
        "overlaid",
    )

    st.markdown("---")

    # PRICE AND VOLUME chart
    priceVolumeChartOptions = {
        # "width": 600,
        "height": 400,
        "rightPriceScale": {
            "scaleMargins": {
                "top": 0.2,
                "bottom": 0.25,
            },
            "borderVisible": False,
        },
        "overlayPriceScales": {
            "scaleMargins": {
                "top": 0.7,
                "bottom": 0,
            }
        },
        "layout": {
            "background": {"type": "solid", "color": "#131722"},
            "textColor": "#d1d4dc",
        },
        "grid": {
            "vertLines": {
                "color": "rgba(42, 46, 57, 0)",
            },
            "horzLines": {
                "color": "rgba(42, 46, 57, 0.6)",
            },
        },
    }

    priceVolumeSeries = [
        {
            "type": "Area",
            "data": data.priceVolumeSeriesArea,
            "options": {
                "topColor": "rgba(38,198,218, 0.56)",
                "bottomColor": "rgba(38,198,218, 0.04)",
                "lineColor": "rgba(38,198,218, 1)",
                "lineWidth": 2,
            },
        },
        {
            "type": "Histogram",
            "data": data.priceVolumeSeriesHistogram,
            "options": {
                "color": "#26a69a",
                "priceFormat": {
                    "type": "volume",
                },
                "priceScaleId": "",  # set as an overlay setting,
            },
            "priceScale": {
                "scaleMargins": {
                    "top": 0.7,
                    "bottom": 0,
                }
            },
        },
    ]
    st.subheader("Price and Volume Series Chart")
    renderLightweightCharts(
        [{"chart": priceVolumeChartOptions, "series": priceVolumeSeries}],
        "priceAndVolume",
    )
    st.markdown("---")

    # MULTIPANE charts
    chartMultipaneOptions = [
        {
            "width": 600,
            "height": 400,
            "layout": {
                "background": {"type": "solid", "color": "white"},
                "textColor": "black",
            },
            "grid": {
                "vertLines": {"color": "rgba(197, 203, 206, 0.5)"},
                "horzLines": {"color": "rgba(197, 203, 206, 0.5)"},
            },
            "crosshair": {"mode": 0},
            "priceScale": {"borderColor": "rgba(197, 203, 206, 0.8)"},
            "timeScale": {
                "borderColor": "rgba(197, 203, 206, 0.8)",
                "barSpacing": 15,
                # "fixLeftEdge": True,
            },
            "watermark": {
                "visible": True,
                "fontSize": 48,
                "horzAlign": "center",
                "vertAlign": "center",
                "color": "rgba(171, 71, 188, 0.3)",
                "text": "Watermark Price",
            },
        },
        {
            "width": 600,
            "height": 100,
            "crosshair": {"mode": 0},
            "layout": {
                "background": {"type": "solid", "color": "transparent"},
                "textColor": "black",
            },
            "grid": {
                "vertLines": {
                    "color": "rgba(42, 46, 57, 0)",
                },
                "horzLines": {
                    "color": "rgba(42, 46, 57, 0.6)",
                },
            },
            "timeScale": {
                "visible": False,
            },
        },
        {
            "width": 600,
            "height": 200,
            "layout": {
                "background": {"type": "solid", "color": "white"},
                "textColor": "black",
            },
            "timeScale": {
                "visible": False,
            },
        },
    ]

    seriesCandlestickChart = [
        {
            "type": "Candlestick",
            "data": data.priceCandlestickMultipane,
            "options": {
                "upColor": "#26a69a",
                "downColor": "#ef5350",
                "borderVisible": False,
                "wickUpColor": "#26a69a",
                "wickDownColor": "#ef5350",
            },
        }
    ]

    seriesAreaChart = [
        {
            "type": "Baseline",
            "data": data.priceBaselineMultipane,
            "options": {
                "baseValue": {"type": "price", "price": 180},
                "topLineColor": "rgba( 38, 166, 154, 1)",
                "topFillColor1": "rgba( 38, 166, 154, 0.28)",
                "topFillColor2": "rgba( 38, 166, 154, 0.05)",
                "bottomLineColor": "rgba( 239, 83, 80, 1)",
                "bottomFillColor1": "rgba( 239, 83, 80, 0.05)",
                "bottomFillColor2": "rgba( 239, 83, 80, 0.28)",
            },
        }
    ]

    seriesHistogramChart = [
        {
            "type": "Histogram",
            "data": data.priceVolumeMultipane,
            "options": {
                "color": "#26a69a",
                "priceFormat": {
                    "type": "volume",
                },
                "priceScaleId": "",  # set as an overlay setting,
            },
            "priceScale": {
                "scaleMargins": {
                    "top": 0,
                    "bottom": 0,
                },
                "alignLabels": False,
            },
        }
    ]

    st.subheader("Multipane Chart with Watermark")
    renderLightweightCharts(
        [
            {"chart": chartMultipaneOptions[0], "series": seriesCandlestickChart},
            {"chart": chartMultipaneOptions[1], "series": seriesHistogramChart},
            {"chart": chartMultipaneOptions[2], "series": seriesAreaChart},
        ],
        "multipane",
    )
    st.markdown("---")
