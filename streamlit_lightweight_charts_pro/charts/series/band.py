"""Band series for streamlit-lightweight-charts."""

from typing import Any, Dict, List, Optional, Sequence, Union

import pandas as pd

from streamlit_lightweight_charts_pro.charts.series.base import Series, _get_enum_value
from streamlit_lightweight_charts_pro.data import BandData
from streamlit_lightweight_charts_pro.type_definitions import (
    ChartType,
    LastPriceAnimationMode,
    LineStyle,
    LineType,
)


class BandSeries(Series):
    """Band series for lightweight charts (e.g., Bollinger Bands)."""

    def __init__(
        self,
        data: Union[Sequence[BandData], pd.DataFrame],
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
        # Band-specific options
        column_mapping: Optional[Dict[str, str]] = None,
        # Upper band styling
        upper_line_color: str = "#4CAF50",  # TradingView green
        upper_line_style: LineStyle = LineStyle.SOLID,
        upper_line_width: int = 2,
        upper_line_visible: bool = True,
        # Middle band styling
        middle_line_color: str = "#2196F3",  # TradingView blue
        middle_line_style: LineStyle = LineStyle.SOLID,
        middle_line_width: int = 2,
        middle_line_visible: bool = True,
        # Lower band styling
        lower_line_color: str = "#F44336",  # TradingView red
        lower_line_style: LineStyle = LineStyle.SOLID,
        lower_line_width: int = 2,
        lower_line_visible: bool = True,
        # Fill colors
        upper_fill_color: str = "rgba(76, 175, 80, 0.1)",  # Green with transparency
        lower_fill_color: str = "rgba(244, 67, 54, 0.1)",  # Red with transparency
        # Line type
        line_type: LineType = LineType.SIMPLE,
        # Crosshair markers
        crosshair_marker_visible: bool = True,
        crosshair_marker_radius: int = 4,
        crosshair_marker_border_color: str = "",
        crosshair_marker_background_color: str = "",
        crosshair_marker_border_width: int = 2,
        # Animation
        last_price_animation: LastPriceAnimationMode = LastPriceAnimationMode.DISABLED,
    ):
        """Initialize band series."""
        # Store column mapping first
        self.column_mapping = column_mapping

        # Band-specific styling options
        # Upper band
        self.upper_line_color = upper_line_color
        self.upper_line_style = upper_line_style
        self.upper_line_width = upper_line_width
        self.upper_line_visible = upper_line_visible

        # Middle band
        self.middle_line_color = middle_line_color
        self.middle_line_style = middle_line_style
        self.middle_line_width = middle_line_width
        self.middle_line_visible = middle_line_visible

        # Lower band
        self.lower_line_color = lower_line_color
        self.lower_line_style = lower_line_style
        self.lower_line_width = lower_line_width
        self.lower_line_visible = lower_line_visible

        # Fill colors
        self.upper_fill_color = upper_fill_color
        self.lower_fill_color = lower_fill_color

        # Line type
        self.line_type = line_type

        # Crosshair markers
        self.crosshair_marker_visible = crosshair_marker_visible
        self.crosshair_marker_radius = crosshair_marker_radius
        self.crosshair_marker_border_color = crosshair_marker_border_color
        self.crosshair_marker_background_color = crosshair_marker_background_color
        self.crosshair_marker_border_width = crosshair_marker_border_width

        # Animation
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
        return ChartType.BAND

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
        # Use default column mapping if none provided
        column_mapping = self.column_mapping or {
            "time": "datetime",
            "upper": "upper",
            "middle": "middle",
            "lower": "lower",
        }

        time_col = column_mapping.get("time", "datetime")
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
        working_df.columns = ['time', 'upper', 'middle', 'lower']
        
        # Remove rows with any NaN values using vectorized operations
        working_df = working_df.dropna()
        
        # Convert time column to string format
        working_df['time'] = working_df['time'].astype(str)
        
        # Convert numeric columns to float
        working_df[['upper', 'middle', 'lower']] = working_df[['upper', 'middle', 'lower']].astype(float)
        
        # Create BandData objects using vectorized operations
        # Use apply() for better performance than list comprehension with zip
        valid_data = working_df.apply(
            lambda row: BandData(
                time=row['time'],
                upper=row['upper'],
                middle=row['middle'],
                lower=row['lower']
            ),
            axis=1
        ).tolist()

        return valid_data

    def to_frontend_config(self) -> Dict[str, Any]:
        """
        Convert series to frontend-compatible configuration.

        This method creates a dictionary representation of the band series
        that can be consumed by the frontend React component.

        Returns:
            Dict[str, Any]: Dictionary containing series configuration for the frontend.
        """
        # Get base configuration
        config = {
            "type": "band",
            "data": [item.to_dict() for item in self.data],
            "options": self._get_options_dict(),
        }

        # Add markers if present
        if self.markers:
            config["markers"] = [marker.to_dict() for marker in self.markers]

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