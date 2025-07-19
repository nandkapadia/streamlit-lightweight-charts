"""Area series for streamlit-lightweight-charts."""

from typing import Any, Dict, List, Optional, Sequence, Union

import pandas as pd

from streamlit_lightweight_charts_pro.charts.series.base import Series, _get_enum_value
from streamlit_lightweight_charts_pro.data import SingleValueData
from streamlit_lightweight_charts_pro.type_definitions import (
    ChartType,
    LastPriceAnimationMode,
    LineStyle,
    LineType,
)


class AreaSeries(Series):
    """Area series for lightweight charts."""

    def __init__(
        self,
        data: Union[Sequence[SingleValueData], pd.DataFrame],
        column_mapping: Optional[Dict[str, str]] = None,
        markers: Optional[List[Any]] = None,
        price_scale: Optional[Dict[str, Any]] = None,
        # Area-specific options
        top_color: str = "rgba(46, 220, 135, 0.4)",
        bottom_color: str = "rgba(40, 221, 100, 0)",
        line_color: str = "#33D778",
        line_style: LineStyle = LineStyle.SOLID,
        line_width: int = 3,
        line_type: LineType = LineType.SIMPLE,
        line_visible: bool = True,
        point_markers_visible: bool = False,
        point_markers_radius: Optional[int] = None,
        crosshair_marker_visible: bool = True,
        crosshair_marker_radius: int = 4,
        crosshair_marker_border_color: str = "",
        crosshair_marker_background_color: str = "",
        crosshair_marker_border_width: int = 2,
        last_price_animation: LastPriceAnimationMode = LastPriceAnimationMode.DISABLED,
        **kwargs,
    ):
        """Initialize area series."""
        super().__init__(
            data=data,
            column_mapping=column_mapping,
            markers=markers,
            price_scale=price_scale,
            **kwargs,
        )

        # Area-specific styling options
        self.top_color = top_color
        self.bottom_color = bottom_color
        self.line_color = line_color
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

    @property
    def chart_type(self) -> ChartType:
        """Get the chart type for this series."""
        return ChartType.AREA

    def _convert_dataframe(
        self, df: pd.DataFrame, column_mapping: Optional[Dict[str, str]] = None
    ) -> List[SingleValueData]:
        """Convert DataFrame to SingleValueData format."""
        if column_mapping is None:
            column_mapping = {"time": "datetime", "value": "close"}

        time_col = column_mapping.get("time", "datetime")
        value_col = column_mapping.get("value", "close")

        if time_col not in df.columns or value_col not in df.columns:
            raise ValueError(f"DataFrame must contain columns: {time_col} and {value_col}")

        # Use vectorized operations for better performance
        times = df[time_col].astype(str).tolist()
        values = df[value_col].astype(float).tolist()

        return [SingleValueData(time=time, value=value) for time, value in zip(times, values)]

    def _get_options_dict(self) -> Dict[str, Any]:
        """Get options dictionary for area series."""
        options = self._base_dict()

        # Add area-specific options
        options.update(
            {
                "topColor": self.top_color,
                "bottomColor": self.bottom_color,
                "lineColor": self.line_color,
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
                "lastPriceAnimation": _get_enum_value(
                    self.last_price_animation, LastPriceAnimationMode
                ),
            }
        )

        if self.point_markers_radius is not None:
            options["pointMarkersRadius"] = self.point_markers_radius

        return options
