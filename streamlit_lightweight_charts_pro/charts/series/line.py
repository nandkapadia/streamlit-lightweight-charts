"""
Line series for streamlit-lightweight-charts.

This module provides the LineSeries class for creating line charts that display
continuous data points connected by lines. Line series are commonly used for
price charts, indicators, and trend analysis.

The LineSeries class supports various styling options including line color,
width, style, and animation effects. It also supports markers and price
line configurations.

Example:
    ```python
    from streamlit_lightweight_charts_pro.charts.series import LineSeries
    from streamlit_lightweight_charts_pro.data import SingleValueData
    
    # Create line data
    data = [
        SingleValueData("2024-01-01", 100),
        SingleValueData("2024-01-02", 105),
        SingleValueData("2024-01-03", 102)
    ]
    
    # Create line series with styling
    series = LineSeries(
        data=data,
        color="#2196F3",
        line_width=2,
        line_style=LineStyle.SOLID
    )
    ```
"""

from typing import Any, Dict, List, Optional, Union

import pandas as pd

from ...data import SingleValueData
from ...type_definitions import LastPriceAnimationMode, LineStyle, LineType
from .base import Series, _get_enum_value


class LineSeries(Series):
    """
    Line series for lightweight charts.
    
    This class represents a line series that displays continuous data points
    connected by lines. It's commonly used for price charts, technical
    indicators, and trend analysis.
    
    The LineSeries supports various styling options including line color,
    width, style, and animation effects. It also supports markers and
    price line configurations.
    
    Attributes:
        color: Color of the line
        line_style: Style of the line (solid, dashed, dotted)
        line_width: Width of the line in pixels
        line_type: Type of line (simple, curved, stepped)
        line_visible: Whether the line is visible
        point_markers_visible: Whether to show point markers
        point_markers_radius: Radius of point markers in pixels
        crosshair_marker_visible: Whether to show crosshair markers
        crosshair_marker_radius: Radius of crosshair markers
        crosshair_marker_border_color: Border color of crosshair markers
        crosshair_marker_background_color: Background color of crosshair markers
        crosshair_marker_border_width: Border width of crosshair markers
        last_price_animation: Animation mode for the last price
    """

    def __init__(
        self,
        data: Union[List[SingleValueData], pd.DataFrame],
        color: str = "#2196F3",
        line_style: Union[LineStyle, str] = LineStyle.SOLID,
        line_width: int = 3,
        line_type: Union[LineType, str] = LineType.SIMPLE,
        line_visible: bool = True,
        point_markers_visible: bool = False,
        point_markers_radius: Optional[int] = None,
        crosshair_marker_visible: bool = True,
        crosshair_marker_radius: int = 4,
        crosshair_marker_border_color: str = "",
        crosshair_marker_background_color: str = "",
        crosshair_marker_border_width: int = 2,
        last_price_animation: Union[LastPriceAnimationMode, str] = LastPriceAnimationMode.DISABLED,
        **kwargs
    ):
        """
        Initialize line series with data and styling options.
        
        Args:
            data: Series data as a list of SingleValueData objects or pandas DataFrame.
            color: Color of the line. Defaults to "#2196F3".
            line_style: Style of the line. Defaults to LineStyle.SOLID.
            line_width: Width of the line in pixels. Defaults to 3.
            line_type: Type of line. Defaults to LineType.SIMPLE.
            line_visible: Whether the line is visible. Defaults to True.
            point_markers_visible: Whether to show point markers. Defaults to False.
            point_markers_radius: Radius of point markers in pixels. Defaults to None.
            crosshair_marker_visible: Whether to show crosshair markers. Defaults to True.
            crosshair_marker_radius: Radius of crosshair markers. Defaults to 4.
            crosshair_marker_border_color: Border color of crosshair markers. Defaults to "".
            crosshair_marker_background_color: Background color of crosshair markers. Defaults to "".
            crosshair_marker_border_width: Border width of crosshair markers. Defaults to 2.
            last_price_animation: Animation mode for the last price. Defaults to DISABLED.
            **kwargs: Additional series configuration options.
            
        Example:
            ```python
            # Basic line series
            series = LineSeries(data=line_data)
            
            # With custom styling
            series = LineSeries(
                data=line_data,
                color="#ff0000",
                line_width=2,
                line_style=LineStyle.DASHED
            )
            ```
        """
        # Initialize base class
        super().__init__(data=data, **kwargs)
        
        # Line-specific styling options
        self.color = color
        self.line_style = line_style
        self.line_width = line_width
        self.line_type = line_type
        self.line_visible = line_visible
        self.point_markers_visible = point_markers_visible
        self.point_markers_radius = point_markers_radius
        self.crosshair_marker_visible = crosshair_marker_visible
        self.crosshair_marker_radius = crosshair_marker_radius
        self.crosshair_marker_border_color = crosshair_marker_border_color
        self.crosshair_marker_background_color = crosshair_marker_background_color
        self.crosshair_marker_border_width = crosshair_marker_border_width
        self.last_price_animation = last_price_animation

    def _process_dataframe(self, df: pd.DataFrame) -> List[SingleValueData]:
        """
        Process pandas DataFrame into SingleValueData format.
        
        Converts a pandas DataFrame with time and value columns into
        a list of SingleValueData objects for the line series.
        
        Args:
            df: Pandas DataFrame with time and value columns.
                
        Returns:
            List[SingleValueData]: List of processed data objects.
            
        Raises:
            ValueError: If required columns are missing from the DataFrame.
            
        Example:
            ```python
            # DataFrame with 'datetime' and 'close' columns
            df = pd.DataFrame({
                'datetime': ['2024-01-01', '2024-01-02'],
                'close': [100, 105]
            })
            series = LineSeries(data=df)
            ```
        """
        # Default column mapping
        column_mapping = {
            'time': 'datetime',
            'value': 'close'
        }
        
        time_col = column_mapping.get('time', 'datetime')
        value_col = column_mapping.get('value', 'close')
        
        if time_col not in df.columns or value_col not in df.columns:
            raise ValueError(f"DataFrame must contain columns: {time_col} and {value_col}")
        
        # Use vectorized operations for better performance
        times = df[time_col].astype(str).tolist()
        values = df[value_col].astype(float).tolist()
        
        return [
            SingleValueData(time=time, value=value)
            for time, value in zip(times, values)
        ]

    def to_frontend_config(self) -> Dict[str, Any]:
        """
        Convert line series to frontend-compatible configuration.
        
        Creates a dictionary representation of the line series suitable
        for consumption by the frontend React component.
        
        Returns:
            Dict[str, Any]: Frontend-compatible configuration dictionary
                containing series type, data, and styling options.
                
        Example:
            ```python
            config = series.to_frontend_config()
            # Returns: {
            #     "type": "line",
            #     "data": [...],
            #     "options": {...}
            # }
            ```
        """
        # Base configuration
        config = {
            "type": "line",
            "data": [item.to_dict() for item in self.data],
            "options": {
                "priceScaleId": self.price_scale_id,
                "visible": self.visible,
                "priceLineVisible": self.price_line_visible,
                "priceLineWidth": self.price_line_width,
                "priceLineColor": self.price_line_color,
                "priceLineStyle": self.price_line_style,
                "baseLineVisible": self.base_line_visible,
                "baseLineWidth": self.base_line_width,
                "baseLineColor": self.base_line_color,
                "baseLineStyle": self.base_line_style,
                "priceFormat": self.price_format,
                # Line-specific options
                "color": self.color,
                "lineStyle": _get_enum_value(self.line_style, LineStyle),
                "lineWidth": self.line_width,
                "lineType": _get_enum_value(self.line_type, LineType),
                "lineVisible": self.line_visible,
                "pointMarkersVisible": self.point_markers_visible,
                "crosshairMarkerVisible": self.crosshair_marker_visible,
                "crosshairMarkerRadius": self.crosshair_marker_radius,
                "crosshairMarkerBorderColor": self.crosshair_marker_border_color,
                "crosshairMarkerBackgroundColor": self.crosshair_marker_background_color,
                "crosshairMarkerBorderWidth": self.crosshair_marker_border_width,
                "lastPriceAnimation": _get_enum_value(self.last_price_animation, LastPriceAnimationMode),
            }
        }
        
        # Add optional fields only if they are set
        if self.point_markers_radius is not None:
            config["options"]["pointMarkersRadius"] = self.point_markers_radius
            
        if self.markers:
            config["markers"] = [marker.to_dict() for marker in self.markers]
            
        if self.price_scale_config:
            config["priceScale"] = self.price_scale_config
            
        return config 