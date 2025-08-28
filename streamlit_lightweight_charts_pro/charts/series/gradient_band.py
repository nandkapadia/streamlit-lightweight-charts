"""
Gradient band series for streamlit-lightweight-charts.

This module provides the GradientBandSeries class for creating band charts
that display upper, middle, and lower bands with gradient fill areas based on gradient values.
"""

import logging
import math
from typing import List, Optional, Union

import pandas as pd

from streamlit_lightweight_charts_pro.charts.series.band import BandSeries
from streamlit_lightweight_charts_pro.data.gradient_band import GradientBandData
from streamlit_lightweight_charts_pro.type_definitions import ChartType
from streamlit_lightweight_charts_pro.utils import chainable_property

logger = logging.getLogger(__name__)


@chainable_property("gradient_start_color", str, validator="color")
@chainable_property("gradient_end_color", str, validator="color")
@chainable_property("gradient_type", str)
@chainable_property("normalize_gradients", bool)
class GradientBandSeries(BandSeries):
    """
    Gradient band series for lightweight charts.

    This class represents a band series that displays upper, middle, and lower bands
    with gradient fill areas based on gradient values. It extends BandSeries
    with gradient fill capabilities, allowing for dynamic color transitions
    based on data values.

    The GradientBandSeries supports various styling options including separate
    line styling for each band via LineOptions, fill colors, and gradient effects.

    Attributes:
        upper_line: LineOptions instance for upper band styling.
        middle_line: LineOptions instance for middle band styling.
        lower_line: LineOptions instance for lower band styling.
        fill: Default fill color for the area between upper and lower bands.
        fill_visible: Whether to display the fill area.
        gradient_start_color: Starting color for gradient fills.
        gradient_end_color: Ending color for gradient fills.
        gradient_type: Type of gradient ('linear' or 'radial').
        normalize_gradients: Whether to normalize gradient values to 0-1 range.
        price_lines: List of PriceLineOptions for price lines (set after construction)
        price_format: PriceFormatOptions for price formatting (set after construction)
        markers: List of markers to display on this series (set after construction)
    """

    DATA_CLASS = GradientBandData

    def __init__(
        self,
        data: Union[List[GradientBandData], pd.DataFrame, pd.Series],
        column_mapping: Optional[dict] = None,
        visible: bool = True,
        price_scale_id: str = "",
        pane_id: Optional[int] = 0,
        gradient_start_color: str = "#4CAF50",
        gradient_end_color: str = "#F44336",
        gradient_type: str = "linear",
        normalize_gradients: bool = False,
    ):
        """
        Initialize GradientBandSeries.

        Args:
            data: List of data points or DataFrame
            column_mapping: Column mapping for DataFrame conversion
            visible: Whether the series is visible
            price_scale_id: ID of the price scale
            pane_id: The pane index this series belongs to
            gradient_start_color: Starting color for gradient fills
            gradient_end_color: Ending color for gradient fills
            gradient_type: Type of gradient ('linear' or 'radial')
            normalize_gradients: Whether to normalize gradient values to 0-1 range
        """
        super().__init__(
            data=data,
            column_mapping=column_mapping,
            visible=visible,
            price_scale_id=price_scale_id,
            pane_id=pane_id,
        )

        # Initialize gradient-specific properties
        self._gradient_start_color = gradient_start_color
        self._gradient_end_color = gradient_end_color
        self._gradient_type = gradient_type
        self._normalize_gradients = normalize_gradients
        self._gradient_bounds = None

    @property
    def chart_type(self) -> ChartType:
        """Get the chart type for this series."""
        return ChartType.GRADIENT_BAND

    def _calculate_gradient_bounds(self) -> None:
        """Calculate min/max gradient values for normalization."""
        valid_gradients = []
        invalid_count = 0

        for i, data_point in enumerate(self.data):
            if data_point.gradient is not None:
                gradient = data_point.gradient

                # Check for invalid values
                if (
                    math.isnan(gradient)
                    or math.isinf(gradient)
                    or not isinstance(gradient, (int, float))
                ):

                    invalid_count += 1
                    logger.warning(
                        "Invalid gradient value at index %d: %s. Data point:"
                        " upper=%s, middle=%s,"
                        " lower=%s",
                        i, gradient, data_point.upper, data_point.middle,
                        data_point.lower
                    )
                    continue

                valid_gradients.append(gradient)

        # Log summary of invalid values
        if invalid_count > 0:
            logger.warning(
                "Found %d invalid gradient values out of %d "
                "data points. These will use series default fill color.",
                invalid_count, len(self.data)
            )

        # Set bounds only if we have valid gradients
        if valid_gradients:
            self._gradient_bounds = (min(valid_gradients), max(valid_gradients))
            logger.debug(
                "Gradient bounds calculated: %s "
                "from %d valid values",
                self._gradient_bounds, len(valid_gradients)
            )
        else:
            self._gradient_bounds = None
            logger.warning("No valid gradient values found. Gradient fills will be disabled.")

    def asdict(self):
        """Override to include normalized gradients if requested."""
        data_dict = super().asdict()

        if self._normalize_gradients:
            # Calculate bounds if not already calculated
            if self._gradient_bounds is None:
                self._calculate_gradient_bounds()

            if self._gradient_bounds:
                min_grad, max_grad = self._gradient_bounds
                range_grad = max_grad - min_grad

                if range_grad > 0:  # Avoid division by zero
                    # Normalize gradients in the output
                    for i, item in enumerate(data_dict["data"]):
                        if item.get("gradient") is not None:
                            gradient = item["gradient"]

                            # Double-check for invalid values (defensive programming)
                            if (
                                math.isnan(gradient)
                                or math.isinf(gradient)
                                or not isinstance(gradient, (int, float))
                            ):

                                # Remove invalid gradient, fall back to series fill
                                item.pop("gradient", None)
                                logger.debug("Removed invalid gradient at index %d: %s", i, gradient)
                                continue

                            # Normalize valid gradient
                            try:
                                normalized = (gradient - min_grad) / range_grad
                                # Clamp to [0, 1] range for safety
                                item["gradient"] = max(0.0, min(1.0, normalized))
                            except (TypeError, ValueError) as e:
                                logger.error(
                                    "Error normalizing gradient %s at index %d: %s",
                                    gradient, i, e
                                )
                                item.pop("gradient", None)

        return data_dict
