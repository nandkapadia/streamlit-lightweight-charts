"""Baseline series for streamlit-lightweight-charts."""

from typing import Any, Dict, List, Optional, Sequence, Union

import pandas as pd

from ...data import BaselineData
from ...type_definitions import ChartType, LastPriceAnimationMode, LineStyle, LineType
from .base import Series, _get_enum_value


class BaselineSeries(Series):
    """Baseline series for lightweight charts."""

    def __init__(
        self,
        data: Union[Sequence[BaselineData], pd.DataFrame],
        column_mapping: Optional[Dict[str, str]] = None,
        markers: Optional[List[Any]] = None,
        price_scale: Optional[Dict[str, Any]] = None,
        # Baseline-specific options
        base_value: Optional[Dict[str, Union[str, float]]] = None,
        top_line_color: str = "rgba(38, 166, 154, 1)",
        top_fill_color1: str = "rgba(38, 166, 154, 0.28)",
        top_fill_color2: str = "rgba(38, 166, 154, 0.05)",
        bottom_line_color: str = "rgba(239, 83, 80, 1)",
        bottom_fill_color1: str = "rgba(239, 83, 80, 0.05)",
        bottom_fill_color2: str = "rgba(239, 83, 80, 0.28)",
        line_width: int = 3,
        line_style: LineStyle = LineStyle.SOLID,
        line_visible: bool = True,
        point_markers_visible: bool = False,
        point_markers_radius: Optional[int] = None,
        crosshair_marker_visible: bool = True,
        crosshair_marker_radius: int = 4,
        crosshair_marker_border_color: str = "",
        crosshair_marker_background_color: str = "",
        crosshair_marker_border_width: int = 2,
        last_price_animation: LastPriceAnimationMode = LastPriceAnimationMode.DISABLED,
        **kwargs
    ):
        """Initialize baseline series."""
        super().__init__(
            data=data,
            column_mapping=column_mapping,
            markers=markers,
            price_scale=price_scale,
            **kwargs
        )
        
        # Baseline-specific styling options
        self.base_value = base_value or {"price": 0}
        self.top_line_color = top_line_color
        self.top_fill_color1 = top_fill_color1
        self.top_fill_color2 = top_fill_color2
        self.bottom_line_color = bottom_line_color
        self.bottom_fill_color1 = bottom_fill_color1
        self.bottom_fill_color2 = bottom_fill_color2
        self.line_width = line_width
        self.line_style = line_style
        self.line_visible = line_visible
        self.point_markers_visible = point_markers_visible
        self.point_markers_radius = point_markers_radius
        self.crosshair_marker_visible = crosshair_marker_visible
        self.crosshair_marker_radius = crosshair_marker_radius
        self.crosshair_marker_border_color = crosshair_marker_border_color
        self.crosshair_marker_background_color = crosshair_marker_background_color
        self.crosshair_marker_border_width = crosshair_marker_border_width
        self.last_price_animation = last_price_animation

    @property
    def chart_type(self) -> ChartType:
        """Get the chart type for this series."""
        return ChartType.BASELINE

    def _convert_dataframe(self, df: pd.DataFrame, column_mapping: Optional[Dict[str, str]] = None) -> List[BaselineData]:
        """Convert DataFrame to BaselineData format."""
        if column_mapping is None:
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
            BaselineData(time=time, value=value)
            for time, value in zip(times, values)
        ]

    def _get_options_dict(self) -> Dict[str, Any]:
        """Get options dictionary for baseline series."""
        options = self._base_dict()
        
        # Add baseline-specific options
        options.update({
            "baseValue": self.base_value,
            "topLineColor": self.top_line_color,
            "topFillColor1": self.top_fill_color1,
            "topFillColor2": self.top_fill_color2,
            "bottomLineColor": self.bottom_line_color,
            "bottomFillColor1": self.bottom_fill_color1,
            "bottomFillColor2": self.bottom_fill_color2,
            "lineWidth": self.line_width,
            "lineStyle": _get_enum_value(self.line_style, LineStyle),
            "lineVisible": self.line_visible,
            "pointMarkersVisible": self.point_markers_visible,
            "crosshairMarkerVisible": self.crosshair_marker_visible,
            "crosshairMarkerRadius": self.crosshair_marker_radius,
            "crosshairMarkerBorderColor": self.crosshair_marker_border_color,
            "crosshairMarkerBackgroundColor": self.crosshair_marker_background_color,
            "crosshairMarkerBorderWidth": self.crosshair_marker_border_width,
            "lastPriceAnimation": _get_enum_value(self.last_price_animation, LastPriceAnimationMode),
        })
        
        if self.point_markers_radius is not None:
            options["pointMarkersRadius"] = self.point_markers_radius
            
        return options 