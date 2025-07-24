"""
Baseline series for streamlit-lightweight-charts.

This module provides the BaselineSeries class for creating baseline charts that display
areas above and below a baseline value with different colors. Baseline series are commonly
used for highlighting positive/negative trends and threshold analysis.

The BaselineSeries class supports various styling options for the baseline, fill colors,
and animation effects. It also supports markers and price line configurations.

Example:
    from streamlit_lightweight_charts_pro.charts.series import BaselineSeries
    from streamlit_lightweight_charts_pro.data import SingleValueData

    # Create baseline data
    data = [
        SingleValueData("2024-01-01", 100),
        SingleValueData("2024-01-02", 105)
    ]

    # Create baseline series with styling
    series = BaselineSeries(
        data=data,
        base_value={"price": 100},
        top_line_color="#26a69a",
        bottom_line_color="#ef5350"
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
)


class BaselineSeries(Series):
    """Baseline series for lightweight charts."""

    def __init__(
        self,
        data,
        column_mapping=None,
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
        **kwargs,
    ):
        # Pop baseline-specific options before calling super().__init__
        base_value = kwargs.pop("base_value", {"price": 0})
        top_line_color = kwargs.pop("top_line_color", "#26a69a")
        top_fill_color1 = kwargs.pop("top_fill_color1", "#b2f2e9")
        top_fill_color2 = kwargs.pop("top_fill_color2", "#e0f7fa")
        bottom_line_color = kwargs.pop("bottom_line_color", "#ef5350")
        bottom_fill_color1 = kwargs.pop("bottom_fill_color1", "#ffcdd2")
        bottom_fill_color2 = kwargs.pop("bottom_fill_color2", "#ffebee")
        line_width = kwargs.pop("line_width", 2)
        line_style = kwargs.pop("line_style", LineStyle.SOLID)
        line_visible = kwargs.pop("line_visible", True)
        point_markers_visible = kwargs.pop("point_markers_visible", False)
        point_markers_radius = kwargs.pop("point_markers_radius", None)
        crosshair_marker_visible = kwargs.pop("crosshair_marker_visible", False)
        crosshair_marker_radius = kwargs.pop("crosshair_marker_radius", 4)
        crosshair_marker_border_color = kwargs.pop("crosshair_marker_border_color", "#2196F3")
        crosshair_marker_background_color = kwargs.pop("crosshair_marker_background_color", "#fff")
        crosshair_marker_border_width = kwargs.pop("crosshair_marker_border_width", 1)
        last_price_animation = kwargs.pop("last_price_animation", LastPriceAnimationMode.DISABLED)
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
        self.base_value = base_value
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

    def _get_columns(self) -> Dict[str, str]:
        """
        Return the column mapping for baseline series, using self.column_mapping if set.
        """
        return self.column_mapping or {
            ColumnNames.TIME: ColumnNames.DATETIME,
            ColumnNames.VALUE: ColumnNames.CLOSE,
        }

    def _process_dataframe(self, df: pd.DataFrame) -> List[SingleValueData]:
        """
        Process pandas DataFrame into SingleValueData format.

        This method converts a pandas DataFrame into a list of SingleValueData
        objects for baseline chart visualization.

        Args:
            df: Pandas DataFrame to process.

        Returns:
            List[SingleValueData]: List of processed data objects.

        Raises:
            ValueError: If required columns are missing from the DataFrame.
        """
        # Use _get_columns for column mapping
        column_mapping = self._get_columns()

        time_col = column_mapping.get(ColumnNames.TIME, ColumnNames.DATETIME)
        value_col = column_mapping.get(ColumnNames.VALUE, ColumnNames.CLOSE)

        if time_col not in df.columns or value_col not in df.columns:
            raise ValueError(f"DataFrame must contain columns: {time_col} and {value_col}")

        # Use vectorized operations for better performance
        times = df[time_col].astype(str).tolist()
        values = df[value_col].astype(float).tolist()

        return [SingleValueData(time=time, value=value) for time, value in zip(times, values)]

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert baseline series to dictionary representation.

        Creates a dictionary representation of the baseline series suitable
        for consumption by the frontend React component.

        Returns:
            Dict[str, Any]: Dictionary representation of the baseline series
                containing series type, data, and styling options.

        Example:
            ```python
            config = series.to_dict()
            # Returns: {
            #     "type": "baseline",
            #     "data": [...],
            #     "options": {...}
            # }
            ```
        """
        # Validate pane configuration
        self._validate_pane_config()

        # Base configuration
        config = {
            "type": "baseline",
            "data": self.data_dict,
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
                # Baseline-specific options
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

    def _get_options_dict(self) -> Dict[str, Any]:
        """Get options dictionary for baseline series."""
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

        # Add baseline-specific options
        options.update(
            {
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
                "lastPriceAnimation": _get_enum_value(
                    self.last_price_animation, LastPriceAnimationMode
                ),
            }
        )

        if self.point_markers_radius is not None:
            options["pointMarkersRadius"] = self.point_markers_radius

        return options
