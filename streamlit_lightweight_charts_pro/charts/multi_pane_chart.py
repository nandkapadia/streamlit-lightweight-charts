"""
Multi-pane chart class for streamlit-lightweight-charts.

This module provides the MultiPaneChart class for creating synchronized multi-pane charts
similar to TradingView. It enables creating professional trading dashboards with multiple
synchronized chart panes, where each pane can contain different chart types and all panes
are automatically synchronized for crosshair movement and time range changes.
"""

from typing import Any, Dict, List, Optional

from .base_chart import BaseChart
from .single_pane_chart import SinglePaneChart


class MultiPaneChart(BaseChart):
    """
    Chart class for creating multi-pane synchronized charts.

    This class enables creating professional trading dashboards with multiple
    synchronized chart panes, similar to TradingView. Each pane can contain
    different chart types (candlestick, line, histogram, etc.) and all panes
    are automatically synchronized for crosshair movement and time range changes.

    MultiPaneChart is ideal for creating comprehensive trading analysis views
    with price charts, volume indicators, technical indicators, and other
    financial data displayed in separate but synchronized panes.

    Attributes:
        charts: List of Chart objects, each representing a separate pane
            in the multi-pane layout.
    """

    def __init__(self, charts: Optional[List[SinglePaneChart]] = None):
        """
        Initialize a multi-pane chart with optional initial charts.

        Args:
            charts: List of SinglePaneChart objects to display in separate panes.
                Each chart will become a separate synchronized pane.
                If None, starts with an empty multi-pane chart.

        Example:
            ```python
            # Create empty multi-pane chart
            multi_chart = MultiPaneChart()

            # Create multi-pane chart with initial charts
            price_chart = SinglePaneChart(series=candlestick_series)
            volume_chart = SinglePaneChart(series=volume_series)
            multi_chart = MultiPaneChart(charts=[price_chart, volume_chart])
            ```
        """
        self.charts = charts or []

    def add_pane(self, chart: SinglePaneChart) -> None:
        """
        Add a chart pane to the multi-pane chart.

        This method adds a new chart as a separate pane in the multi-pane layout.
        The new pane will be automatically synchronized with existing panes
        for crosshair movement and time range changes.

        Args:
            chart: SinglePaneChart object to add as a new pane. Can be any SinglePaneChart instance
                with any combination of series types.

        Example:
            ```python
            multi_chart = MultiPaneChart()
            multi_chart.add_pane(price_chart)
            multi_chart.add_pane(volume_chart)
            multi_chart.add_pane(rsi_chart)
            ```
        """
        self.charts.append(chart)

    def to_frontend_config(self) -> Dict[str, Any]:
        """
        Convert multi-pane chart to frontend-compatible configuration.

        This method converts all chart panes into a frontend-compatible
        configuration that can be consumed by the React component. The
        configuration includes all chart panes and synchronization settings.

        Returns:
            Dictionary containing multi-pane chart configuration for the frontend,
            including all chart panes and synchronization settings.
        """
        # Convert all individual charts to frontend configurations
        chart_configs = []
        for chart in self.charts:
            chart_configs.append(chart.to_frontend_config())

        return {
            "charts": chart_configs,
            "syncConfig": {"enabled": True, "crosshair": True, "timeRange": True},
        }
