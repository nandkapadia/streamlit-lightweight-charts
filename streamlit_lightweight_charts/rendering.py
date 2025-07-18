"""
Chart rendering functionality for streamlit-lightweight-charts.

This module provides the core rendering functionality for converting chart objects
into Streamlit components. It handles both the new OOP API and legacy dictionary-based
API, ensuring backward compatibility while providing a clean interface for chart rendering.

The module includes functions for rendering single charts, multi-pane charts, and
managing chart synchronization across multiple panes.
"""

import os
from typing import Any, Dict, List, Optional, Union

import streamlit.components.v1 as components

from .charts import Chart, MultiPaneChart


def _get_component_func():
    """
    Get the component function from the main module.

    This function retrieves the Streamlit component function that was declared
    in the main __init__.py file. It includes a fallback mechanism in case
    the import fails.

    Returns:
        The Streamlit component function for rendering charts.

    Raises:
        ImportError: If the component function cannot be imported from the main module.
    """
    try:
        # Import the main module and get the component function
        from . import _component_func  # pylint: disable=import-outside-toplevel

        return _component_func
    except ImportError:
        # Fallback: declare the component if import fails
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        build_dir = os.path.join(parent_dir, "frontend", "build")

        return components.declare_component("streamlit_lightweight_charts", path=build_dir)


def render_chart(
    charts: Union[List[Union[Chart, Dict[str, Any]]], Chart, Dict[str, Any], MultiPaneChart],
    key: Optional[str] = None,
    height: int = 400,
    width: Optional[int] = None,
    sync_config: Optional[Dict[str, Any]] = None,
) -> Any:
    """
    Render lightweight charts using Streamlit component.

    This is the main rendering function that converts chart objects or configurations
    into Streamlit components. It supports multiple input formats and automatically
    handles chart synchronization for multi-pane charts.

    Args:
        charts: Chart object(s) or chart configuration(s). Can be:
            - A single Chart object
            - A MultiPaneChart object
            - A dictionary with chart configuration
            - A list of any of the above
        key: Unique key for the Streamlit component. Used to prevent conflicts
            when multiple charts are rendered on the same page.
        height: Chart height in pixels. Defaults to 400.
        width: Chart width in pixels. Defaults to 800.
        sync_config: Configuration for chart synchronization. Should contain:
            - enabled: bool - Whether to enable synchronization
            - crosshair: bool - Whether to sync crosshair across charts
            - timeRange: bool - Whether to sync time range across charts
            Defaults to {"enabled": False, "crosshair": True, "timeRange": True}.

    Returns:
        The rendered Streamlit component result.

    Example:
        ```python
        # Render a single chart
        chart = CandlestickChart(data=ohlc_data)
        render_chart(chart, key="candlestick", height=500)

        # Render a multi-pane chart with synchronization
        multi_chart = MultiPaneChart()
        multi_chart.add_pane(price_chart)
        multi_chart.add_pane(volume_chart)
        render_chart(multi_chart, key="multi_pane", sync_config={"enabled": True})
        ```
    """
    # Convert to list of chart configs for consistent processing
    chart_configs = []

    if isinstance(charts, MultiPaneChart):
        # MultiPaneChart case: extract all individual charts
        chart_configs = [chart.to_frontend_config() for chart in charts.charts]
    elif isinstance(charts, (Chart, dict)):
        # Single chart case: wrap in list for consistent processing
        if isinstance(charts, Chart):
            chart_configs = [charts.to_frontend_config()]
        else:
            chart_configs = [charts]
    else:
        # List case: process each chart individually
        for chart in charts:
            if isinstance(chart, Chart):
                chart_configs.append(chart.to_frontend_config())
            else:
                chart_configs.append(chart)

    # Check if any chart has auto-sizing enabled
    has_auto_sizing = False
    for chart_config in chart_configs:
        chart_options = chart_config.get("chart", {})
        if (chart_options.get("autoSize") or 
            chart_options.get("autoWidth") or 
            chart_options.get("autoHeight")):
            has_auto_sizing = True
            break

    # Create component configuration with default synchronization settings
    component_config = {
        "charts": chart_configs,
        "syncConfig": sync_config or {"enabled": False, "crosshair": True, "timeRange": True},
        "height": height,  # Always pass the height to the frontend
        "width": width,    # Pass width (can be None for 100% width)
    }
    return _get_component_func()(config=component_config, key=key)


def render_multi_pane_chart(
    chart: MultiPaneChart,
    key: Optional[str] = None,
    height: Optional[int] = None,
    width: Optional[int] = None,
) -> Any:
    """
    Render a multi-pane chart specifically with synchronization enabled.

    This is a convenience function for rendering MultiPaneChart objects with
    automatic synchronization enabled. It's equivalent to calling render_chart
    with sync_config={"enabled": True, "crosshair": True, "timeRange": True}.

    Args:
        chart: MultiPaneChart object to render. Should contain multiple chart
            panes that will be synchronized.
        key: Unique key for the Streamlit component. Used to prevent conflicts
            when multiple charts are rendered on the same page.
        height: Chart height in pixels. Defaults to 400.
        width: Chart width in pixels. Defaults to 800.

    Returns:
        The rendered Streamlit component result with synchronization enabled.

    Example:
        ```python
        # Create and render a synchronized multi-pane chart
        multi_chart = MultiPaneChart()
        multi_chart.add_pane(price_chart)
        multi_chart.add_pane(volume_chart)
        multi_chart.add_pane(rsi_chart)

        render_multi_pane_chart(multi_chart, key="trading_view_style")
        ```
    """
    return render_chart(
        charts=chart,
        key=key,
        height=height or 400,  # Use provided height or default to 400
        width=width,  # Pass through the width parameter (can be None for 100%)
        sync_config={"enabled": True, "crosshair": True, "timeRange": True},
    )
