"""
Candlestick series for streamlit-lightweight-charts.

This module provides the CandlestickSeries class for creating candlestick charts that display
OHLC or OHLCV data. Candlestick series are commonly used for price charts and technical analysis.

The CandlestickSeries class supports various styling options for up/down colors, wicks, borders,
and animation effects. It also supports markers, price line configurations, and trade
visualizations.

Example:
    from streamlit_lightweight_charts_pro.charts.series import CandlestickSeries
    from streamlit_lightweight_charts_pro.data.ohlc_data import OhlcData

    # Create candlestick data
    data = [
        OhlcData("2024-01-01", 100, 105, 98, 103),
        OhlcData("2024-01-02", 103, 108, 102, 106)
    ]

    # Create candlestick series with styling
    series = CandlestickSeries(data=data)
    series.up_color = "#4CAF50"
    series.down_color = "#F44336"
"""

from typing import List, Optional, Union

import pandas as pd

from streamlit_lightweight_charts_pro.charts.series.base import Series
from streamlit_lightweight_charts_pro.data.candlestick_data import CandlestickData
from streamlit_lightweight_charts_pro.type_definitions import ChartType
from streamlit_lightweight_charts_pro.utils.data_utils import is_valid_color


class CandlestickSeries(Series):
    """Candlestick series for lightweight charts."""

    DATA_CLASS = CandlestickData

    def __init__(
        self,
        data: Union[List[CandlestickData], pd.DataFrame, pd.Series],
        column_mapping: Optional[dict] = None,
        visible: bool = True,
        price_scale_id: str = "right",
        pane_id: Optional[int] = 0,
        overlay: Optional[bool] = True,
    ):
        super().__init__(
            data=data,
            column_mapping=column_mapping,
            visible=visible,
            price_scale_id=price_scale_id,
            pane_id=pane_id,
            overlay=overlay,
        )

        # Initialize candlestick-specific properties with default values
        self._up_color = "#26a69a"
        self._down_color = "#ef5350"
        self._wick_visible = True
        self._border_visible = True
        self._border_color = "#378658"
        self._border_up_color = "#26a69a"
        self._border_down_color = "#ef5350"
        self._wick_color = "#737375"
        self._wick_up_color = "#26a69a"
        self._wick_down_color = "#ef5350"

    def _validate_color(self, color: str, property_name: str) -> str:
        """Validate color format."""
        if not is_valid_color(color):
            raise ValueError(
                f"Invalid color format for {property_name}: {color!r}. Must be hex or rgba."
            )
        return color

    @property
    def up_color(self) -> str:
        """Get the color of rising candles."""
        return self._up_color

    @up_color.setter
    def up_color(self, value: str):
        """Set the color of rising candles."""
        self._up_color = self._validate_color(value, "up_color")

    @property
    def down_color(self) -> str:
        """Get the color of falling candles."""
        return self._down_color

    @down_color.setter
    def down_color(self, value: str):
        """Set the color of falling candles."""
        self._down_color = self._validate_color(value, "down_color")

    @property
    def wick_visible(self) -> bool:
        """Get whether high and low prices candle wicks are enabled."""
        return self._wick_visible

    @wick_visible.setter
    def wick_visible(self, value: bool):
        """Set whether high and low prices candle wicks are enabled."""
        self._wick_visible = bool(value)

    @property
    def border_visible(self) -> bool:
        """Get whether candle borders are enabled."""
        return self._border_visible

    @border_visible.setter
    def border_visible(self, value: bool):
        """Set whether candle borders are enabled."""
        self._border_visible = bool(value)

    @property
    def border_color(self) -> str:
        """Get the border color."""
        return self._border_color

    @border_color.setter
    def border_color(self, value: str):
        """Set the border color."""
        self._border_color = self._validate_color(value, "border_color")

    @property
    def border_up_color(self) -> str:
        """Get the border color of rising candles."""
        return self._border_up_color

    @border_up_color.setter
    def border_up_color(self, value: str):
        """Set the border color of rising candles."""
        self._border_up_color = self._validate_color(value, "border_up_color")

    @property
    def border_down_color(self) -> str:
        """Get the border color of falling candles."""
        return self._border_down_color

    @border_down_color.setter
    def border_down_color(self, value: str):
        """Set the border color of falling candles."""
        self._border_down_color = self._validate_color(value, "border_down_color")

    @property
    def wick_color(self) -> str:
        """Get the wick color."""
        return self._wick_color

    @wick_color.setter
    def wick_color(self, value: str):
        """Set the wick color."""
        self._wick_color = self._validate_color(value, "wick_color")

    @property
    def wick_up_color(self) -> str:
        """Get the wick color of rising candles."""
        return self._wick_up_color

    @wick_up_color.setter
    def wick_up_color(self, value: str):
        """Set the wick color of rising candles."""
        self._wick_up_color = self._validate_color(value, "wick_up_color")

    @property
    def wick_down_color(self) -> str:
        """Get the wick color of falling candles."""
        return self._wick_down_color

    @wick_down_color.setter
    def wick_down_color(self, value: str):
        """Set the wick color of falling candles."""
        self._wick_down_color = self._validate_color(value, "wick_down_color")

    @property
    def chart_type(self) -> ChartType:
        """Get the chart type for this series."""
        return ChartType.CANDLESTICK
