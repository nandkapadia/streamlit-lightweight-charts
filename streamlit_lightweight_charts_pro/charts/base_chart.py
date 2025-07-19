"""
Base chart class for streamlit-lightweight-charts.

This module provides the base chart class that defines the common interface
for all chart types in the library. It includes the core rendering functionality
and configuration methods that are shared between single-pane and multi-pane charts.

The BaseChart class serves as the foundation for all chart implementations,
providing a consistent interface for chart creation, configuration, and rendering
in Streamlit applications.

Example:
    ```python
    from streamlit_lightweight_charts_pro.charts.base_chart import BaseChart
    
    class MyCustomChart(BaseChart):
        def to_frontend_config(self):
            return {"type": "custom", "data": self.data}
    ```
"""

from abc import ABC, abstractmethod
from typing import Any, Optional

from ..component import get_component_func


class BaseChart(ABC):
    """
    Abstract base class for all chart types.
    
    This class defines the common interface and functionality that all chart
    classes must implement. It provides the core rendering capabilities and
    configuration methods that are shared across different chart types.
    
    All chart classes should inherit from this base class and implement
    the required abstract methods.
    
    Attributes:
        series: List of series objects to display in the chart
        options: Chart configuration options
        annotation_manager: Manager for chart annotations
        
    Example:
        ```python
        class MyChart(BaseChart):
            def to_frontend_config(self):
                return {"type": "custom", "series": self.series}
        ```
    """

    @abstractmethod
    def to_frontend_config(self) -> Any:
        """
        Convert chart to frontend-compatible configuration.
        
        This method must be implemented by all subclasses to convert the
        chart object into a format that can be consumed by the frontend
        React component.
        
        Returns:
            Any: Frontend-compatible configuration (dict, list, or other format)
                that can be serialized and passed to the React component.
                
        Example:
            ```python
            def to_frontend_config(self):
                return {
                    "chart": self.options.to_dict(),
                    "series": [s.to_dict() for s in self.series]
                }
            ```
        """
        pass

    def render(self, key: Optional[str] = None) -> Any:
        """
        Render the chart using the Streamlit component.
        
        This method converts the chart to frontend configuration and renders
        it using the Streamlit component system. It handles the integration
        between the Python chart objects and the React frontend.
        
        Args:
            key: Optional unique key for the Streamlit component. If not provided,
                a default key will be generated.
                
        Returns:
            Any: The result from the Streamlit component, typically None or
                component-specific return value.
                
        Raises:
            RuntimeError: If the component function is not available or fails
                to render the chart.
                
        Example:
            ```python
            chart = SinglePaneChart(series=line_series)
            chart.render(key="my_chart")
            ```
        """
        # Get the component function for rendering
        component_func = get_component_func()
        if component_func is None:
            raise RuntimeError(
                "Component function not available. "
                "Make sure the frontend is properly built."
            )
        
        # Convert chart to frontend configuration
        config = self.to_frontend_config()
        
        # Render using Streamlit component
        return component_func(config=config, key=key) 