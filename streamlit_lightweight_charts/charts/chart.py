"""Chart classes for streamlit-lightweight-charts."""

from typing import List, Optional, Dict, Any, Union
from ..rendering import render_chart
from .options import ChartOptions
from .series import Series


class Chart:
    """Main chart class for creating single-pane charts."""
    
    def __init__(
        self,
        series: Union[Series, List[Series]],
        options: Optional[ChartOptions] = None
    ):
        """
        Initialize a chart.
        
        Args:
            series: Single series or list of series to display
            options: Chart configuration options
        """
        self.series = series if isinstance(series, list) else [series]
        self.options = options or ChartOptions()
    
    def render(self, key: Optional[str] = None) -> Any:
        """
        Render the chart using Streamlit.
        
        Args:
            key: Unique key for the Streamlit component
            
        Returns:
            Rendered chart component
        """
        chart_data = {
            'chart': self.options.to_dict(),
            'series': [s.to_dict() for s in self.series]
        }
        return render_chart([chart_data], key=key)
    
    def add_series(self, series: Series) -> 'Chart':
        """
        Add a series to the chart.
        
        Args:
            series: Series to add
            
        Returns:
            Self for method chaining
        """
        self.series.append(series)
        return self
    
    def update_options(self, **kwargs) -> 'Chart':
        """
        Update chart options.
        
        Args:
            **kwargs: Options to update
            
        Returns:
            Self for method chaining
        """
        for key, value in kwargs.items():
            if hasattr(self.options, key):
                setattr(self.options, key, value)
        return self


class MultiPaneChart:
    """Chart class for creating multi-pane charts."""
    
    def __init__(self, charts: Optional[List[Chart]] = None):
        """
        Initialize a multi-pane chart.
        
        Args:
            charts: List of charts to display in separate panes
        """
        self.charts = charts or []
    
    def add_pane(self, chart: Chart) -> 'MultiPaneChart':
        """
        Add a pane to the multi-pane chart.
        
        Args:
            chart: Chart to add as a new pane
            
        Returns:
            Self for method chaining
        """
        self.charts.append(chart)
        return self
    
    def render(self, key: Optional[str] = None) -> Any:
        """
        Render the multi-pane chart using Streamlit.
        
        Args:
            key: Unique key for the Streamlit component
            
        Returns:
            Rendered chart component
        """
        charts_data = []
        for chart in self.charts:
            charts_data.append({
                'chart': chart.options.to_dict(),
                'series': [s.to_dict() for s in chart.series]
            })
        return render_chart(charts_data, key=key)