"""Utilities for visualizing trades on charts."""

from typing import List, Dict, Any, Optional
from ..data import Trade, TradeVisualization, TradeVisualizationOptions
from ..types import LineStyle
import json


def trades_to_visual_elements(
    trades: List[Trade],
    options: TradeVisualizationOptions,
    chart_data: Optional[List[Dict]] = None
) -> Dict[str, Any]:
    """
    Convert trades to visual elements based on visualization options.
    
    Args:
        trades: List of trades to visualize
        options: Visualization options
        chart_data: Optional chart data for calculating positions
        
    Returns:
        Dictionary with visual elements (markers, shapes, etc.)
    """
    result = {
        'markers': [],
        'shapes': [],
        'annotations': []
    }
    
    for trade in trades:
        if options.style in [TradeVisualization.MARKERS, TradeVisualization.BOTH]:
            # Add markers for entry and exit
            markers = trade.to_markers(
                entry_color=(options.entry_marker_color_long 
                           if trade.trade_type.value == 'long' 
                           else options.entry_marker_color_short),
                exit_color=(options.exit_marker_color_profit 
                          if trade.is_profitable 
                          else options.exit_marker_color_loss),
                show_pnl=options.show_pnl_in_markers
            )
            result['markers'].extend([m.to_dict() for m in markers])
        
        if options.style in [TradeVisualization.RECTANGLES, TradeVisualization.BOTH]:
            # Add rectangle shape
            rect = create_trade_rectangle(trade, options)
            result['shapes'].append(rect)
        
        elif options.style == TradeVisualization.LINES:
            # Add line connecting entry to exit
            line = create_trade_line(trade, options)
            result['shapes'].append(line)
        
        elif options.style == TradeVisualization.ARROWS:
            # Add arrow from entry to exit
            arrow = create_trade_arrow(trade, options)
            result['shapes'].append(arrow)
        
        elif options.style == TradeVisualization.ZONES:
            # Add colored zone
            zone = create_trade_zone(trade, options, chart_data)
            result['shapes'].append(zone)
        
        # Add trade annotation if enabled
        if any([options.show_trade_id, options.show_quantity, options.show_trade_type]):
            annotation = create_trade_annotation(trade, options)
            result['annotations'].append(annotation)
    
    return result


def create_trade_rectangle(trade: Trade, options: TradeVisualizationOptions) -> Dict[str, Any]:
    """Create rectangle shape for trade."""
    color = (options.rectangle_color_profit 
             if trade.is_profitable 
             else options.rectangle_color_loss)
    
    return {
        'type': 'rectangle',
        'time1': trade.entry_timestamp,
        'price1': trade.entry_price,
        'time2': trade.exit_timestamp,
        'price2': trade.exit_price,
        'fillColor': f'{color}{int(options.rectangle_fill_opacity * 255):02x}',
        'borderColor': color,
        'borderWidth': options.rectangle_border_width,
        'borderStyle': 'solid'
    }


def create_trade_line(trade: Trade, options: TradeVisualizationOptions) -> Dict[str, Any]:
    """Create line shape for trade."""
    color = (options.line_color_profit 
             if trade.is_profitable 
             else options.line_color_loss)
    
    return {
        'type': 'trendLine',
        'time1': trade.entry_timestamp,
        'price1': trade.entry_price,
        'time2': trade.exit_timestamp,
        'price2': trade.exit_price,
        'lineColor': color,
        'lineWidth': options.line_width,
        'lineStyle': get_line_style_value(options.line_style)
    }


def create_trade_arrow(trade: Trade, options: TradeVisualizationOptions) -> Dict[str, Any]:
    """Create arrow shape for trade."""
    color = (options.arrow_color_profit 
             if trade.is_profitable 
             else options.arrow_color_loss)
    
    # Create arrow as a line with arrow head
    return {
        'type': 'arrow',
        'time1': trade.entry_timestamp,
        'price1': trade.entry_price,
        'time2': trade.exit_timestamp,
        'price2': trade.exit_price,
        'lineColor': color,
        'lineWidth': options.line_width,
        'arrowSize': options.arrow_size,
        'text': f"{trade.pnl_percentage:+.1f}%"
    }


def create_trade_zone(
    trade: Trade, 
    options: TradeVisualizationOptions,
    chart_data: Optional[List[Dict]] = None
) -> Dict[str, Any]:
    """Create colored zone for trade."""
    color = (options.zone_color_long 
             if trade.trade_type.value == 'long' 
             else options.zone_color_short)
    
    # Calculate extended time if chart data is available
    time1 = trade.entry_timestamp
    time2 = trade.exit_timestamp
    
    if chart_data and options.zone_extend_bars > 0:
        # Find the time step and extend
        for i, bar in enumerate(chart_data):
            if bar['time'] >= trade.entry_timestamp:
                if i >= options.zone_extend_bars:
                    time1 = chart_data[i - options.zone_extend_bars]['time']
                break
        
        for i, bar in enumerate(reversed(chart_data)):
            if bar['time'] <= trade.exit_timestamp:
                idx = len(chart_data) - i - 1
                if idx + options.zone_extend_bars < len(chart_data):
                    time2 = chart_data[idx + options.zone_extend_bars]['time']
                break
    
    # Get min/max prices for zone height
    if trade.trade_type.value == 'long':
        top_price = max(trade.entry_price, trade.exit_price) * 1.01
        bottom_price = min(trade.entry_price, trade.exit_price) * 0.99
    else:
        top_price = max(trade.entry_price, trade.exit_price) * 1.01
        bottom_price = min(trade.entry_price, trade.exit_price) * 0.99
    
    return {
        'type': 'rectangle',
        'time1': time1,
        'price1': bottom_price,
        'time2': time2,
        'price2': top_price,
        'fillColor': f'{color}{int(options.zone_opacity * 255):02x}',
        'borderColor': 'transparent',
        'borderWidth': 0
    }


def create_trade_annotation(trade: Trade, options: TradeVisualizationOptions) -> Dict[str, Any]:
    """Create annotation for trade."""
    # Build annotation text
    text_parts = []
    
    if options.show_trade_id and trade.id:
        text_parts.append(f"#{trade.id}")
    
    if options.show_trade_type:
        text_parts.append(trade.trade_type.value.upper())
    
    if options.show_quantity:
        text_parts.append(f"Qty: {trade.quantity}")
    
    text_parts.append(f"P&L: {trade.pnl_percentage:+.1f}%")
    
    # Position annotation at midpoint
    mid_time = (trade.entry_timestamp + trade.exit_timestamp) / 2 if isinstance(trade.entry_timestamp, (int, float)) else trade.entry_timestamp
    mid_price = (trade.entry_price + trade.exit_price) / 2
    
    return {
        'type': 'text',
        'time': mid_time,
        'price': mid_price,
        'text': ' | '.join(text_parts),
        'fontSize': options.annotation_font_size,
        'backgroundColor': options.annotation_background,
        'color': '#000000',
        'padding': 4
    }


def get_line_style_value(style: str) -> int:
    """Convert line style string to numeric value."""
    style_map = {
        'solid': 0,
        'dotted': 1,
        'dashed': 2,
        'large_dashed': 3,
        'sparse_dotted': 4
    }
    return style_map.get(style, 2)  # Default to dashed


def create_trade_shapes_series(
    trades: List[Trade],
    options: TradeVisualizationOptions
) -> Dict[str, Any]:
    """
    Create a shapes series configuration for trades.
    
    This creates a separate series that can be added to the chart
    specifically for trade visualization.
    """
    visual_elements = trades_to_visual_elements(trades, options)
    
    # Create a custom series for shapes
    return {
        'type': 'Custom',
        'data': [],  # No data points, just shapes
        'options': {
            'priceScaleId': 'right',
            'lastValueVisible': False,
            'priceLineVisible': False
        },
        'shapes': visual_elements['shapes'],
        'annotations': visual_elements['annotations']
    }


def add_trades_to_series(
    series_config: Dict[str, Any],
    trades: List[Trade],
    options: TradeVisualizationOptions
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
    if visual_elements['markers']:
        if 'markers' not in series_config:
            series_config['markers'] = []
        series_config['markers'].extend(visual_elements['markers'])
    
    # Add shapes if available
    if visual_elements['shapes']:
        if 'shapes' not in series_config:
            series_config['shapes'] = []
        series_config['shapes'].extend(visual_elements['shapes'])
    
    # Add annotations if available
    if visual_elements['annotations']:
        if 'annotations' not in series_config:
            series_config['annotations'] = []
        series_config['annotations'].extend(visual_elements['annotations'])
    
    return series_config