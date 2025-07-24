"""
Line series for streamlit-lightweight-charts.

This module provides the LineSeries class for creating line charts that display
continuous data points connected by lines. Line series are commonly used for
price charts, indicators, and trend analysis.

The LineSeries class supports various styling options including line color,
width, style, and animation effects. It also supports markers and price
line configurations.

Example:
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
"""

from typing import Any, Dict, List

import pandas as pd

from streamlit_lightweight_charts_pro.charts.series.base import Series, _get_enum_value
from streamlit_lightweight_charts_pro.data import SingleValueData
from streamlit_lightweight_charts_pro.type_definitions import (
    ChartType,
    ColumnNames,
    LastPriceAnimationMode,
    LineStyle,
    LineType,
)


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
        data,
        column_mapping=None,
        color="#2196F3",
        visible=True,
        price_scale_id="right",
        price_line_visible=False,
        base_line_visible=False,
        price_line_width=1,
        price_line_color="#2196F3",
        price_line_style="solid",
        base_line_width=1,
        base_line_color="#FF9800",
        base_line_style="solid",
        price_format=None,
        markers=None,
        pane_id=0,
        height=None,
        overlay=True,
        line_style=LineStyle.SOLID,
        line_width=2,
        line_type=LineType.SIMPLE,
        line_visible=True,
        point_markers_visible=False,
        point_markers_radius=None,
        crosshair_marker_visible=False,
        crosshair_marker_radius=4,
        crosshair_marker_border_color="#2196F3",
        crosshair_marker_background_color="#fff",
        crosshair_marker_border_width=1,
        last_price_animation=LastPriceAnimationMode.DISABLED,
        **kwargs,
    ):
        super().__init__(
            data=data,
            column_mapping=column_mapping,
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
            pane_id=pane_id,
            height=height,
            overlay=overlay,
            **kwargs,
        )
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

    @property
    def chart_type(self) -> ChartType:
        """Get the chart type for this series."""
        return ChartType.LINE

    def _get_columns(self) -> Dict[str, str]:
        """
        Return the column mapping for line series, using self.column_mapping if set.
        """
        return self.column_mapping or {
            ColumnNames.TIME: ColumnNames.DATETIME,
            ColumnNames.VALUE: ColumnNames.CLOSE,
        }

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
        # Use _get_columns for column mapping
        mapping = self._get_columns()
        time_col = mapping.get(ColumnNames.TIME, ColumnNames.DATETIME)
        value_col = mapping.get(ColumnNames.VALUE, ColumnNames.CLOSE)

        if time_col not in df.columns or value_col not in df.columns:
            raise ValueError(f"DataFrame must contain columns: {time_col} and {value_col}")

        # Use vectorized operations for better performance
        times = df[time_col].astype(str).tolist()
        values = df[value_col].astype(float).tolist()

        return [SingleValueData(time=time, value=value) for time, value in zip(times, values)]

    def _get_options_dict(self) -> Dict[str, Any]:
        """Get options dictionary for line series."""
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
            "color": self.color,
        }

        # Add line-specific options
        options.update(
            {
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

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert line series to dictionary representation.

        Creates a dictionary representation of the line series suitable
        for consumption by the frontend React component.

        Returns:
            Dict[str, Any]: Dictionary representation of the line series
                containing series type, data, and styling options.

        Example:
            ```python
            config = series.to_dict()
            # Returns: {
            #     "type": "line",
            #     "data": [...],
            #     "options": {...}
            # }
            ```
        """
        # Validate pane configuration
        self._validate_pane_config()

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
                "lastPriceAnimation": _get_enum_value(
                    self.last_price_animation, LastPriceAnimationMode
                ),
            },
        }

        # Add optional fields only if they are set
        if self.point_markers_radius is not None:
            config["options"]["pointMarkersRadius"] = self.point_markers_radius

        if self.markers:
            config["markers"] = [marker.to_dict() for marker in self.markers]

        # Remove price_scale_config from to_dict

        # Add height and pane_id
        if self.height is not None:
            config["height"] = self.height
        config["pane_id"] = self.pane_id
        return config
