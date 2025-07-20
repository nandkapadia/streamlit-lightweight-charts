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
        visible: bool = True,
        price_scale_id: str = "right",
        price_line_visible: bool = False,
        base_line_visible: bool = False,
        price_line_width: int = 1,
        price_line_color: str = "#2196F3",
        price_line_style: str = "solid",
        base_line_width: int = 1,
        base_line_color: str = "#FF9800",
        base_line_style: str = "solid",
        price_format: Optional[Dict[str, Any]] = None,
        markers: Optional[List[Any]] = None,
        price_scale_config: Optional[Dict[str, Any]] = None,
        # Area-specific options
        column_mapping: Optional[Dict[str, str]] = None,
        top_color: str = "rgba(33, 150, 243, 0.4)",  # TradingView blue with transparency
        bottom_color: str = "rgba(33, 150, 243, 0.0)",  # TradingView blue transparent
        line_color: str = "#2196F3",  # TradingView blue
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
    ):
        """Initialize area series."""
        # Store column mapping first
        self.column_mapping = column_mapping

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

        # Call parent constructor after setting column_mapping
        super().__init__(
            data=data,
            visible=visible,
            price_scale_id=price_scale_id,
            price_line_visible=price_line_visible,
            base_line_visible=base_line_visible,
            price_line_width=price_line_width,
            price_line_color=price_line_color,
            price_line_style=price_line_style,
            base_line_width=base_line_width,
            base_line_color=base_line_color,
            base_line_style=base_line_style,
            price_format=price_format,
            markers=markers,
            price_scale_config=price_scale_config,
        )

    @property
    def chart_type(self) -> ChartType:
        """Get the chart type for this series."""
        return ChartType.AREA

    def _process_dataframe(self, df: pd.DataFrame) -> List[SingleValueData]:
        """
        Process pandas DataFrame into SingleValueData format.

        This method converts a pandas DataFrame into a list of SingleValueData
        objects for area chart visualization.

        Args:
            df: Pandas DataFrame to process.

        Returns:
            List[SingleValueData]: List of processed data objects.

        Raises:
            ValueError: If required columns are missing from the DataFrame.
        """
        # Use default column mapping if none provided
        column_mapping = self.column_mapping or {"time": "datetime", "value": "close"}

        time_col = column_mapping.get("time", "datetime")
        value_col = column_mapping.get("value", "close")

        if time_col not in df.columns or value_col not in df.columns:
            raise ValueError(f"DataFrame must contain columns: {time_col} and {value_col}")

        # Use vectorized operations for better performance
        times = df[time_col].astype(str).tolist()
        values = df[value_col].astype(float).tolist()

        return [SingleValueData(time=time, value=value) for time, value in zip(times, values)]

    def to_frontend_config(self) -> Dict[str, Any]:
        """
        Convert series to frontend-compatible configuration.

        This method creates a dictionary representation of the area series
        that can be consumed by the frontend React component.

        Returns:
            Dict[str, Any]: Dictionary containing series configuration for the frontend.
        """
        # Get base configuration
        config = {
            "type": "area",
            "data": [item.to_dict() for item in self.data],
            "options": self._get_options_dict(),
        }

        # Add markers if present
        if self.markers:
            config["markers"] = [marker.to_dict() for marker in self.markers]

        return config

    def _get_options_dict(self) -> Dict[str, Any]:
        """Get options dictionary for area series."""
        options = {
            "visible": self.visible,
            "priceScaleId": self.price_scale_id,
            "priceLineVisible": self.price_line_visible,
            "priceLineWidth": self.price_line_width,
            "priceLineColor": self.price_line_color,
            "priceLineStyle": self.price_line_style,
            "baseLineVisible": self.base_line_visible,
            "baseLineWidth": self.base_line_width,
            "baseLineColor": self.base_line_color,
            "baseLineStyle": self.base_line_style,
            "priceFormat": self.price_format,
        }

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
