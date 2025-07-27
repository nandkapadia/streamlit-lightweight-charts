"""
Utilities for visualizing trades on charts.

This module provides comprehensive utilities for converting trade data into
visual elements that can be displayed on financial charts. It supports multiple
visualization styles including markers, rectangles, lines, arrows, and zones,
with extensive customization options for colors, sizes, and annotations.

The module handles the conversion of Trade objects into frontend-compatible
visual representations that can be rendered by the charting library.
"""

from typing import Any, Dict, List, Optional

from streamlit_lightweight_charts_pro.charts.options.trade_visualization_options import (
    TradeVisualizationOptions,
)
from streamlit_lightweight_charts_pro.data import Trade
from streamlit_lightweight_charts_pro.type_definitions import ColumnNames
from streamlit_lightweight_charts_pro.type_definitions.enums import TradeVisualization
from streamlit_lightweight_charts_pro.utils.data_utils import to_utc_timestamp


def trades_to_visual_elements(
    trades: List["Trade"],
    options: "TradeVisualizationOptions",
    chart_data: Optional[List[Dict]] = None,
) -> Dict[str, Any]:
    """
    Convert trades to visual elements based on visualization options.

    This function processes a list of trades and converts them into visual
    elements (markers, shapes, annotations) based on the specified visualization
    style and options. It supports multiple visualization styles and can
    generate different types of visual representations for the same trade data.

    Args:
        trades: List of Trade objects to visualize. Each trade should have
            entry/exit timestamps, prices, and trade type information.
        options: TradeVisualizationOptions object containing styling preferences
            and visualization configuration.
        chart_data: Optional chart data for calculating extended positions
            and zone boundaries. Used primarily for zone-style visualizations.

    Returns:
        Dictionary containing visual elements organized by type:
            - markers: List of marker configurations
            - shapes: List of shape configurations (rectangles, lines, arrows, zones)
            - annotations: List of text annotation configurations

    Raises:
        ValueError: If trades or options is None.
        TypeError: If any item in trades is not a Trade object.

    Example:
        ```python
        trades = [
            Trade("2024-01-01", 100, TradeType.LONG, exit_time="2024-01-03", exit_price=105),
            Trade("2024-01-02", 102, TradeType.SHORT, exit_time="2024-01-04", exit_price=98)
        ]

        options = TradeVisualizationOptions(
            style=TradeVisualization.BOTH,
            show_pnl_in_markers=True,
            rectangle_fill_opacity=0.3
        )

        visual_elements = trades_to_visual_elements(trades, options)
        # Returns dict with markers, shapes, and annotations
        ```
    """
    if trades is None:
        raise ValueError("trades cannot be None")
    if options is None:
        raise ValueError("options cannot be None")
    
    result = {"markers": [], "shapes": [], "annotations": []}

    # Validate that all trades are Trade objects
    for trade in trades:
        if not isinstance(trade, Trade):
            raise TypeError(f"All items in trades must be Trade objects, got {type(trade)}")

    for trade in trades:
        # Add markers if marker style is enabled
        if options.style in [TradeVisualization.MARKERS, TradeVisualization.BOTH]:
            # Create markers for entry and exit points
            markers = trade.to_markers(
                entry_color=(
                    options.entry_marker_color_long
                    if trade.trade_type.value == "long"
                    else options.entry_marker_color_short
                ),
                exit_color=(
                    options.exit_marker_color_profit
                    if trade.is_profitable
                    else options.exit_marker_color_loss
                ),
                show_pnl=options.show_pnl_in_markers,
            )
            result["markers"].extend([m.to_dict() for m in markers])

        # Add shapes based on visualization style
        if options.style in [TradeVisualization.RECTANGLES, TradeVisualization.BOTH]:
            # Create rectangle shape covering the trade period
            rect = create_trade_rectangle(trade, options)
            result["shapes"].append(rect)

        elif options.style == TradeVisualization.LINES:
            # Create line connecting entry to exit
            line = create_trade_line(trade, options)
            result["shapes"].append(line)

        elif options.style == TradeVisualization.ARROWS:
            # Create arrow from entry to exit
            arrow = create_trade_arrow(trade, options)
            result["shapes"].append(arrow)

        elif options.style == TradeVisualization.ZONES:
            # Create colored zone covering the trade period
            zone = create_trade_zone(trade, options, chart_data)
            result["shapes"].append(zone)

        # Only add annotations if we're using BOTH style and annotation options are enabled
        if (options.style == TradeVisualization.BOTH and
            any([options.show_trade_id, options.show_quantity, options.show_trade_type])):
            annotation = create_trade_annotation(trade, options)
            result["annotations"].append(annotation)

    return result


def create_trade_rectangle(trade: "Trade", options: "TradeVisualizationOptions") -> Dict[str, Any]:
    """
    Create rectangle shape for trade visualization.

    Creates a rectangle that covers the entire trade period from entry to exit,
    with styling based on whether the trade was profitable or not.

    Args:
        trade: Trade object containing entry/exit information.
        options: TradeVisualizationOptions containing rectangle styling preferences.

    Returns:
        Dictionary containing rectangle shape configuration for the frontend.

    Raises:
        ValueError: If trade or options is None.

    Example:
        ```python
        trade = Trade("2024-01-01", 100, TradeType.LONG,
                     exit_time="2024-01-03", exit_price=105)
        options = TradeVisualizationOptions(
            rectangle_color_profit="#26a69a",
            rectangle_color_loss="#ef5350",
            rectangle_fill_opacity=0.3,
            rectangle_border_width=2
        )
        rect = create_trade_rectangle(trade, options)
        ```
    """
    if trade is None:
        raise ValueError("trade cannot be None")
    if options is None:
        raise ValueError("options cannot be None")
    
    # Determine colors based on trade profitability
    if trade.is_profitable:
        fill_color = options.rectangle_fill_color_profit
        border_color = options.rectangle_border_color_profit
    else:
        fill_color = options.rectangle_color_loss
        border_color = options.rectangle_border_color_loss

    return {
        "type": "rectangle",
        "time": trade.entry_timestamp,
        "width": trade.exit_timestamp - trade.entry_timestamp if isinstance(trade.exit_timestamp, (int, float)) and isinstance(trade.entry_timestamp, (int, float)) else 0,
        "price1": trade.entry_price,
        "price2": trade.exit_price,
        "fillColor": fill_color,
        "borderColor": border_color,
        "borderWidth": options.rectangle_border_width,
        "borderStyle": "solid",
        "fillOpacity": options.rectangle_fill_opacity,
    }


def create_trade_line(trade: "Trade", options: "TradeVisualizationOptions") -> Dict[str, Any]:
    """
    Create line shape for trade visualization.

    Creates a line that connects the entry point to the exit point of a trade,
    with styling based on trade profitability.

    Args:
        trade: Trade object containing entry/exit information.
        options: TradeVisualizationOptions containing line styling preferences.

    Returns:
        Dictionary containing line shape configuration for the frontend.

    Raises:
        ValueError: If trade or options is None.

    Example:
        ```python
        trade = Trade("2024-01-01", 100, TradeType.LONG,
                     exit_time="2024-01-03", exit_price=105)
        options = TradeVisualizationOptions(
            line_color_profit="#26a69a",
            line_color_loss="#ef5350",
            line_width=2,
            line_style="dashed"
        )
        line = create_trade_line(trade, options)
        ```
    """
    if trade is None:
        raise ValueError("trade cannot be None")
    if options is None:
        raise ValueError("options cannot be None")
    
    # Determine color based on trade profitability
    color = options.line_color_profit if trade.is_profitable else options.line_color_loss

    return {
        "type": "line",
        "time": trade.entry_timestamp,
        "width": options.line_width,
        "price1": trade.entry_price,
        "price2": trade.exit_price,
        "color": color,
        "style": get_line_style_value(options.line_style),
    }


def create_trade_arrow(trade: "Trade", options: "TradeVisualizationOptions") -> Dict[str, Any]:
    """
    Create arrow shape for trade visualization.

    Creates an arrow that points from the entry point to the exit point of a trade,
    with styling based on trade profitability and optional PnL text.

    Args:
        trade: Trade object containing entry/exit information.
        options: TradeVisualizationOptions containing arrow styling preferences.

    Returns:
        Dictionary containing arrow shape configuration for the frontend.

    Raises:
        ValueError: If trade or options is None.

    Example:
        ```python
        trade = Trade("2024-01-01", 100, TradeType.LONG,
                     exit_time="2024-01-03", exit_price=105)
        options = TradeVisualizationOptions(
            arrow_color_profit="#26a69a",
            arrow_color_loss="#ef5350",
            arrow_size=10
        )
        arrow = create_trade_arrow(trade, options)
        ```
    """
    if trade is None:
        raise ValueError("trade cannot be None")
    if options is None:
        raise ValueError("options cannot be None")
    # Determine color based on trade profitability
    color = options.arrow_color_profit if trade.is_profitable else options.arrow_color_loss

    # Create arrow as a line with arrow head and PnL text
    return {
        "type": "arrow",
        "time": trade.entry_timestamp,
        "price": trade.entry_price,
        "color": color,
        "size": options.arrow_size,
        "width": trade.exit_timestamp - trade.entry_timestamp if isinstance(trade.exit_timestamp, (int, float)) and isinstance(trade.entry_timestamp, (int, float)) else 0,
        "text": f"{trade.pnl_percentage:+.1f}%",
    }


def create_trade_zone(
    trade: "Trade",
    options: "TradeVisualizationOptions",
    chart_data: Optional[List[Dict]] = None,
) -> Dict[str, Any]:
    """
    Create colored zone for trade visualization.

    Creates a colored zone that covers the trade period and extends beyond
    the entry/exit points if specified. The zone can be extended by a number
    of bars to provide context around the trade.

    Args:
        trade: Trade object containing entry/exit information.
        options: TradeVisualizationOptions containing zone styling preferences.
        chart_data: Optional chart data for calculating extended zone boundaries.
            Used when zone_extend_bars is greater than 0.

    Returns:
        Dictionary containing zone shape configuration for the frontend.

    Example:
        ```python
        trade = Trade("2024-01-01", 100, TradeType.LONG,
                     exit_time="2024-01-03", exit_price=105)
        options = TradeVisualizationOptions(
            zone_color_long="#26a69a",
            zone_color_short="#ef5350",
            zone_opacity=0.2,
            zone_extend_bars=2
        )
        zone = create_trade_zone(trade, options, chart_data)
        ```
    """
    # Determine color based on trade type
    color = (
        options.zone_color_long if trade.trade_type.value == "long" else options.zone_color_short
    )

    # Calculate extended time boundaries if chart data is available
    time1 = trade.entry_timestamp
    time2 = trade.exit_timestamp

    if chart_data and options.zone_extend_bars > 0:
        # Convert chart data timestamps to integers for comparison

        # Extend the zone by the specified number of bars
        for i, bar_ in enumerate(chart_data):
            bar_time = (
                to_utc_timestamp(bar_[ColumnNames.TIME])
                if isinstance(bar_[ColumnNames.TIME], str)
                else bar_[ColumnNames.TIME]
            )
            if bar_time >= trade.entry_timestamp:
                if i >= options.zone_extend_bars:
                    prev_bar_time = chart_data[i - options.zone_extend_bars][ColumnNames.TIME]
                    time1 = (
                        to_utc_timestamp(prev_bar_time)
                        if isinstance(prev_bar_time, str)
                        else prev_bar_time
                    )
                break

        for i, bar_ in enumerate(reversed(chart_data)):
            bar_time = (
                to_utc_timestamp(bar_[ColumnNames.TIME])
                if isinstance(bar_[ColumnNames.TIME], str)
                else bar_[ColumnNames.TIME]
            )
            if bar_time <= trade.exit_timestamp:
                idx = len(chart_data) - i - 1
                if idx + options.zone_extend_bars < len(chart_data):
                    next_bar_time = chart_data[idx + options.zone_extend_bars][ColumnNames.TIME]
                    time2 = (
                        to_utc_timestamp(next_bar_time)
                        if isinstance(next_bar_time, str)
                        else next_bar_time
                    )
                break

    # Calculate zone height with some padding
    if trade.trade_type.value == "long":
        top_price = max(trade.entry_price, trade.exit_price) * 1.01
        bottom_price = min(trade.entry_price, trade.exit_price) * 0.99
    else:
        top_price = max(trade.entry_price, trade.exit_price) * 1.01
        bottom_price = min(trade.entry_price, trade.exit_price) * 0.99

    return {
        "type": "zone",
        "time": time1,
        "width": time2 - time1 if isinstance(time2, (int, float)) and isinstance(time1, (int, float)) else 0,
        "price1": bottom_price,
        "price2": top_price,
        "fillColor": f"{color}{int(options.zone_opacity * 255):02x}" if not color.startswith("rgba") else color.replace("1)", f"{options.zone_opacity})"),
        "borderColor": color,
        "borderWidth": 0,
    }


def create_trade_annotation(trade: "Trade", options: "TradeVisualizationOptions") -> Dict[str, Any]:
    """
    Create annotation for trade visualization.

    Creates a text annotation that displays trade information such as trade ID,
    trade type, quantity, and PnL based on the annotation options.

    Args:
        trade: Trade object containing trade information.
        options: TradeVisualizationOptions containing annotation preferences.

    Returns:
        Dictionary containing annotation configuration for the frontend.

    Example:
        ```python
        trade = Trade("2024-01-01", 100, TradeType.LONG,
                     exit_time="2024-01-03", exit_price=105, quantity=100)
        options = TradeVisualizationOptions(
            show_trade_id=True,
            show_trade_type=True,
            show_quantity=True,
            show_pnl=True
        )
        annotation = create_trade_annotation(trade, options)
        ```
    """
    # Build annotation text based on enabled options
    text_parts = []

    if options.show_trade_id and trade.id:
        text_parts.append(f"#{trade.id}")

    if options.show_trade_type:
        text_parts.append(trade.trade_type.value.upper())

    if options.show_quantity:
        text_parts.append(f"Qty: {trade.quantity}")

    text_parts.append(f"P&L: {trade.pnl_percentage:+.1f}%")

    # Position annotation at midpoint
    mid_time = (
        (trade.entry_timestamp + trade.exit_timestamp) / 2
        if isinstance(trade.entry_timestamp, (int, float))
        else trade.entry_timestamp
    )
    mid_price = (trade.entry_price + trade.exit_price) / 2

    return {
        "type": "annotation",
        ColumnNames.TIME: mid_time,
        "price": mid_price,
        "position": "inBar",
        "text": " | ".join(text_parts),
        "fontSize": options.annotation_font_size,
        "backgroundColor": options.annotation_background,
        "color": "#000000",
        "padding": 4,
    }


def get_line_style_value(style: str) -> int:
    """
    Convert line style string to numeric value.
    
    Args:
        style: Line style string (solid, dotted, dashed, etc.)
        
    Returns:
        int: Numeric value for the line style
        
    Raises:
        ValueError: If style is not recognized
    """
    style_map = {
        "solid": 0,
        "dotted": 2,
        "dashed": 1,
        "large_dashed": 3,
        "sparse_dotted": 4,
    }
    
    if style.lower() not in style_map:
        raise ValueError(f"Invalid line style: {style}")
    
    return style_map[style.lower()]


def create_trade_shapes_series(
    trades: List["Trade"], options: "TradeVisualizationOptions"
) -> Dict[str, Any]:
    """
    Create a shapes series configuration for trades.

    This creates a separate series that can be added to the chart
    specifically for trade visualization.
    """
    visual_elements = trades_to_visual_elements(trades, options)

    # Create a custom series for shapes
    return {
        "type": "Custom",
        "data": visual_elements["shapes"],  # Return shapes as data
        "options": {
            "priceScaleId": "right",
            "lastValueVisible": False,
            "priceLineVisible": False,
        },
        "shapes": visual_elements["shapes"],
        "annotations": visual_elements["annotations"],
    }


def add_trades_to_series(
    series_config: Dict[str, Any],
    trades: List["Trade"],
    options: "TradeVisualizationOptions",
) -> Dict[str, Any]:
    """
    Add trade visualizations to an existing series configuration.

    Args:
        series_config: Existing series configuration
        trades: List of trades to add
        options: Visualization options

    Returns:
        Updated series configuration with trade visualizations
    """
    visual_elements = trades_to_visual_elements(trades, options)

    # Add markers if the style includes markers
    if visual_elements["markers"]:
        if "markers" not in series_config:
            series_config["markers"] = []
        series_config["markers"].extend(visual_elements["markers"])

    # Add shapes if available
    if visual_elements["shapes"]:
        if "shapes" not in series_config:
            series_config["shapes"] = []
        series_config["shapes"].extend(visual_elements["shapes"])

    # Add annotations if annotation options are enabled (regardless of style)
    if any([options.show_trade_id, options.show_quantity, options.show_trade_type]):
        if "annotations" not in series_config:
            series_config["annotations"] = []
        
        # Create annotations for each trade
        for trade in trades:
            annotation = create_trade_annotation(trade, options)
            series_config["annotations"].append(annotation)

    return series_config
