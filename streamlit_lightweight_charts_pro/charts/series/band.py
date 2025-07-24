"""
Band series for streamlit-lightweight-charts.

This module provides the BandSeries class for creating band charts (e.g., Bollinger Bands)
that display upper, middle, and lower bands. Band series are commonly used for technical
indicators and volatility analysis.

The BandSeries class supports various styling options for each band, fill colors, and
animation effects. It also supports markers and price line configurations.

Example:
    from streamlit_lightweight_charts_pro.charts.series import BandSeries
    from streamlit_lightweight_charts_pro.data import BandData

    # Create band data
    data = [
        BandData("2024-01-01", upper=110, middle=105, lower=100),
        BandData("2024-01-02", upper=112, middle=107, lower=102)
    ]

    # Create band series with styling
    series = BandSeries(
        data=data,
        upper_line_color="#4CAF50",
        lower_line_color="#F44336",
        upper_fill_color="rgba(76, 175, 80, 0.1)",
        lower_fill_color="rgba(244, 67, 54, 0.1)"
    )
"""

from typing import Any, Dict, List, Optional, Union

import pandas as pd

from streamlit_lightweight_charts_pro.charts.series.base import Series, _get_enum_value
from streamlit_lightweight_charts_pro.data import BandData
from streamlit_lightweight_charts_pro.type_definitions import (
    ChartType,
    ColumnNames,
    LastPriceAnimationMode,
    LineStyle,
    LineType,
)


class BandSeries(Series):
    """Band series for lightweight charts (e.g., Bollinger Bands)."""

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
        # Pop band-specific options before calling super().__init__
        band_kwargs = {}
        band_kwargs["upper_line_color"] = kwargs.pop("upper_line_color", "#4CAF50")
        band_kwargs["middle_line_color"] = kwargs.pop("middle_line_color", "#2196F3")
        band_kwargs["lower_line_color"] = kwargs.pop("lower_line_color", "#F44336")
        band_kwargs["upper_line_width"] = kwargs.pop("upper_line_width", 2)
        band_kwargs["middle_line_width"] = kwargs.pop("middle_line_width", 2)
        band_kwargs["lower_line_width"] = kwargs.pop("lower_line_width", 2)
        band_kwargs["upper_line_style"] = kwargs.pop("upper_line_style", LineStyle.SOLID)
        band_kwargs["middle_line_style"] = kwargs.pop("middle_line_style", LineStyle.SOLID)
        band_kwargs["lower_line_style"] = kwargs.pop("lower_line_style", LineStyle.SOLID)
        band_kwargs["upper_line_visible"] = kwargs.pop("upper_line_visible", True)
        band_kwargs["middle_line_visible"] = kwargs.pop("middle_line_visible", True)
        band_kwargs["lower_line_visible"] = kwargs.pop("lower_line_visible", True)
        band_kwargs["upper_fill_color"] = kwargs.pop("upper_fill_color", "rgba(76, 175, 80, 0.1)")
        band_kwargs["lower_fill_color"] = kwargs.pop("lower_fill_color", "rgba(244, 67, 54, 0.1)")
        band_kwargs["line_type"] = kwargs.pop("line_type", LineType.SIMPLE)
        band_kwargs["crosshair_marker_visible"] = kwargs.pop("crosshair_marker_visible", False)
        band_kwargs["crosshair_marker_radius"] = kwargs.pop("crosshair_marker_radius", 4)
        band_kwargs["crosshair_marker_border_color"] = kwargs.pop(
            "crosshair_marker_border_color", "#2196F3"
        )
        band_kwargs["crosshair_marker_background_color"] = kwargs.pop(
            "crosshair_marker_background_color", "#fff"
        )
        band_kwargs["crosshair_marker_border_width"] = kwargs.pop(
            "crosshair_marker_border_width", 1
        )
        band_kwargs["last_price_animation"] = kwargs.pop(
            "last_price_animation", LastPriceAnimationMode.DISABLED
        )
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
        self.upper_line_color = band_kwargs["upper_line_color"]
        self.middle_line_color = band_kwargs["middle_line_color"]
        self.lower_line_color = band_kwargs["lower_line_color"]
        self.upper_line_width = band_kwargs["upper_line_width"]
        self.middle_line_width = band_kwargs["middle_line_width"]
        self.lower_line_width = band_kwargs["lower_line_width"]
        self.upper_line_style = band_kwargs["upper_line_style"]
        self.middle_line_style = band_kwargs["middle_line_style"]
        self.lower_line_style = band_kwargs["lower_line_style"]
        self.upper_line_visible = band_kwargs["upper_line_visible"]
        self.middle_line_visible = band_kwargs["middle_line_visible"]
        self.lower_line_visible = band_kwargs["lower_line_visible"]
        self.upper_fill_color = band_kwargs["upper_fill_color"]
        self.lower_fill_color = band_kwargs["lower_fill_color"]
        self.line_type = band_kwargs["line_type"]
        self.crosshair_marker_visible = band_kwargs["crosshair_marker_visible"]
        self.crosshair_marker_radius = band_kwargs["crosshair_marker_radius"]
        self.crosshair_marker_border_color = band_kwargs["crosshair_marker_border_color"]
        self.crosshair_marker_background_color = band_kwargs["crosshair_marker_background_color"]
        self.crosshair_marker_border_width = band_kwargs["crosshair_marker_border_width"]
        self.last_price_animation = band_kwargs["last_price_animation"]

    @property
    def chart_type(self) -> ChartType:
        """Get the chart type for this series."""
        return ChartType.BAND

    def _get_columns(self) -> Dict[str, str]:
        """
        Return the column mapping for band series, using self.column_mapping if set.
        """
        return self.column_mapping or {
            ColumnNames.TIME: ColumnNames.DATETIME,
            "upper": "upper",
            "middle": "middle",
            "lower": "lower",
        }

    def _process_dataframe(self, df: pd.DataFrame) -> List[BandData]:
        """
        Process pandas DataFrame into BandData format.

        This method converts a pandas DataFrame into a list of BandData
        objects for band chart visualization using vectorized operations
        for better performance.

        Args:
            df: Pandas DataFrame to process.

        Returns:
            List[BandData]: List of processed data objects.

        Raises:
            ValueError: If required columns are missing from the DataFrame.
        """
        # Use _get_columns for column mapping
        column_mapping = self._get_columns()

        time_col = column_mapping.get(ColumnNames.TIME, ColumnNames.DATETIME)
        upper_col = column_mapping.get("upper", "upper")
        middle_col = column_mapping.get("middle", "middle")
        lower_col = column_mapping.get("lower", "lower")

        required_cols = [time_col, upper_col, middle_col, lower_col]
        missing_cols = [col for col in required_cols if col not in df.columns]

        if missing_cols:
            raise ValueError(f"DataFrame must contain columns: {missing_cols}")

        # Create a working copy with only the required columns
        working_df = df[[time_col, upper_col, middle_col, lower_col]].copy()

        # Rename columns for easier processing
        working_df.columns = ["time", "upper", "middle", "lower"]

        # Remove rows with any NaN values using vectorized operations
        working_df = working_df.dropna()

        # Convert time column to string format
        working_df["time"] = working_df["time"].astype(str)

        # Convert numeric columns to float
        working_df[["upper", "middle", "lower"]] = working_df[["upper", "middle", "lower"]].astype(
            float
        )

        # Create BandData objects using vectorized operations
        # Use apply() for better performance than list comprehension with zip
        valid_data = working_df.apply(
            lambda row: BandData(
                time=row["time"], upper=row["upper"], middle=row["middle"], lower=row["lower"]
            ),
            axis=1,
        ).tolist()

        return valid_data

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert series to dictionary representation.

        This method creates a dictionary representation of the band series
        that can be consumed by the frontend React component.

        Returns:
            Dict[str, Any]: Dictionary containing series configuration for the frontend.
        """
        # Validate pane configuration
        self._validate_pane_config()

        # Get base configuration
        config = {
            "type": "band",
            "data": self.data_dict,
            "options": self._get_options_dict(),
        }

        # Add markers if present
        if self.markers:
            config["markers"] = [marker.to_dict() for marker in self.markers]

        # Add height and pane_id
        if self.height is not None:
            config["height"] = self.height
        config["pane_id"] = self.pane_id
        return config

    def _get_options_dict(self) -> Dict[str, Any]:
        """Get options dictionary for band series."""
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

        # Add band-specific options
        options.update(
            {
                # Upper band
                "upperLineColor": self.upper_line_color,
                "upperLineStyle": _get_enum_value(self.upper_line_style, LineStyle),
                "upperLineWidth": self.upper_line_width,
                "upperLineVisible": self.upper_line_visible,
                # Middle band
                "middleLineColor": self.middle_line_color,
                "middleLineStyle": _get_enum_value(self.middle_line_style, LineStyle),
                "middleLineWidth": self.middle_line_width,
                "middleLineVisible": self.middle_line_visible,
                # Lower band
                "lowerLineColor": self.lower_line_color,
                "lowerLineStyle": _get_enum_value(self.lower_line_style, LineStyle),
                "lowerLineWidth": self.lower_line_width,
                "lowerLineVisible": self.lower_line_visible,
                # Fill colors
                "upperFillColor": self.upper_fill_color,
                "lowerFillColor": self.lower_fill_color,
                # Line type
                "lineType": _get_enum_value(self.line_type, LineType),
                # Crosshair markers
                "crosshairMarkerVisible": self.crosshair_marker_visible,
                "crosshairMarkerRadius": self.crosshair_marker_radius,
                "crosshairMarkerBorderColor": self.crosshair_marker_border_color,
                "crosshairMarkerBackgroundColor": self.crosshair_marker_background_color,
                "crosshairMarkerBorderWidth": self.crosshair_marker_border_width,
                # Animation
                "lastPriceAnimation": _get_enum_value(
                    self.last_price_animation, LastPriceAnimationMode
                ),
            }
        )

        return options

    def get_data_range(self) -> Optional[Dict[str, Union[float, str]]]:
        """
        Get the data range for band series.

        Returns the minimum and maximum values and times for the band series data.
        For band series, this includes all upper, middle, and lower values.

        Returns:
            Optional[Dict[str, Union[float, str]]]: Dictionary containing
                min_value, max_value, min_time, max_time, or None if no data.

        Example:
            ```python
            range_info = series.get_data_range()
            if range_info:
                logger.info(f"Value range: {range_info['min_value']} - {range_info['max_value']}")
            ```
        """
        if not self.data:
            return None

        # Extract all values from band data (upper, middle, lower)
        values = []
        times = []

        for item in self.data:
            if hasattr(item, "upper") and hasattr(item, "middle") and hasattr(item, "lower"):
                if item.upper is not None and not pd.isna(item.upper):
                    values.append(item.upper)
                if item.middle is not None and not pd.isna(item.middle):
                    values.append(item.middle)
                if item.lower is not None and not pd.isna(item.lower):
                    values.append(item.lower)

            times.append(item._time)

        if not values:
            return {
                "min_value": None,
                "max_value": None,
                "min_time": min(times),
                "max_time": max(times),
            }

        return {
            "min_value": min(values),
            "max_value": max(values),
            "min_time": min(times),
            "max_time": max(times),
        }
