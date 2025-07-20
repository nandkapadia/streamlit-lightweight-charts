"""Price Volume Chart for streamlit-lightweight-charts."""

from typing import Dict, List, Optional, Union

import pandas as pd

from streamlit_lightweight_charts_pro.charts.options import (
    ChartOptions,
    OverlayPriceScale,
    PriceScaleMargins,
)
from streamlit_lightweight_charts_pro.charts.series import CandlestickSeries, HistogramSeries
from streamlit_lightweight_charts_pro.charts.single_pane_chart import SinglePaneChart
from streamlit_lightweight_charts_pro.data import OhlcData, OhlcvData


class PriceVolumeChart(SinglePaneChart):
    """
    Price Volume Chart combining candlestick and volume series.

    This chart displays candlestick data in the main area (75% of chart height)
    and volume as a histogram in the bottom area (25% of chart height).
    """

    def __init__(
        self,
        data: Union[pd.DataFrame, List[Union[OhlcData, OhlcvData]]],
        column_mapping: Optional[Dict[str, str]] = None,
        # Candlestick options
        up_color: str = "#4CAF50",  # TradingView vibrant green
        down_color: str = "#F44336",  # TradingView vibrant red
        border_visible: bool = True,  # TradingView shows borders
        wick_up_color: str = "#4CAF50",  # TradingView vibrant green
        wick_down_color: str = "#F44336",  # TradingView vibrant red
        # Volume options
        volume_color: str = "#2196F3",  # TradingView light blue/teal
        volume_alpha: float = 0.8,
        # Chart options
        height: int = 400,
        **kwargs,
    ):
        """
        Initialize Price Volume Chart.

        Args:
            data: OHLC/OHLCV data as DataFrame or list of data objects
            column_mapping: Optional column mapping for DataFrame
            up_color: Color for up candles
            down_color: Color for down candles
            border_visible: Whether candle borders are visible
            wick_up_color: Color for up candle wicks
            wick_down_color: Color for down candle wicks
            volume_color: Color for volume histogram
            volume_alpha: Transparency for volume (0.0 to 1.0)
            height: Chart height in pixels
            **kwargs: Additional chart options
        """
        # Extract volume data if available
        volume_data = None
        if isinstance(data, pd.DataFrame):
            # Check if volume column exists
            if column_mapping is None:
                column_mapping = {
                    "time": "datetime",
                    "open": "open",
                    "high": "high",
                    "low": "low",
                    "close": "close",
                    "volume": "volume",
                }

            volume_col = column_mapping.get("volume", "volume")
            if volume_col in data.columns:
                volume_data = data[[column_mapping.get("time", "datetime"), volume_col]].copy()
                volume_data.columns = ["datetime", "volume"]

        # Create candlestick series
        candlestick_series = CandlestickSeries(
            data=data,
            column_mapping=column_mapping,
            up_color=up_color,
            down_color=down_color,
            border_visible=border_visible,
            wick_up_color=wick_up_color,
            wick_down_color=wick_down_color,
            price_scale_id="right",
            price_format={"type": "price", "precision": 2, "minMove": 0.01},
        )

        # Create series list starting with candlestick
        series_list = [candlestick_series]

        # Add volume series if volume data is available
        if volume_data is not None:
            # Create volume series with volume-specific price scale configuration
            volume_series = HistogramSeries(
                data=volume_data,
                column_mapping={"time": "datetime", "value": "volume"},
                color=f"{volume_color}{int(volume_alpha * 255):02x}",  # Add alpha to color
                base=0,
                price_scale_id="volume",  # Use volume-specific price scale
                price_format={"type": "volume", "precision": 0},
                price_scale_config={
                    "visible": False,  # Hide volume price scale - we don't want volume values on right side
                    "autoScale": True,
                    "mode": 0,  # Normal mode
                    "invertScale": False,
                    "borderVisible": False,
                    "textColor": "#131722",
                    "fontSize": 11,
                    "fontWeight": "400",
                    "ticksVisible": False,  # Hide volume ticks
                    "drawTicks": True,
                    "ensureEdgeTickMarksVisible": False,
                    "alignLabels": False,
                    "entireTextOnly": False,
                    "minimumWidth": 72,
                    "scaleMargins": {"top": 0.75, "bottom": 0},  # Occupy bottom 25%
                    "handleScale": False,
                    "handleSize": 20,
                    "priceScaleId": "volume",
                    "overlay": True  # Mark as overlay price scale
                },
            )

            series_list.append(volume_series)

        # Create chart options with overlay price scale for volume
        chart_options = ChartOptions(
            height=height,
            right_price_scale={
                "visible": True,
                "ticksVisible": True,
                "borderVisible": True,
                "textColor": "#131722",  # TradingView dark gray
                "fontSize": 11,
                "minimumWidth": 80,
                "drawTicks": True,
                "ensureEdgeTickMarksVisible": True,
                "alignLabels": True,
            },
            **kwargs,
        )
        
        # Add volume-specific price scale configuration if volume data exists
        if volume_data is not None:
            chart_options.overlay_price_scales = {
                "volume": {
                    "visible": False,  # Hide volume price scale - we don't want volume values on right side
                    "autoScale": True,
                    "mode": 0,
                    "invertScale": False,
                    "borderVisible": False,
                    "textColor": "#131722",
                    "fontSize": 11,
                    "fontWeight": "400",
                    "ticksVisible": False,
                    "drawTicks": True,
                    "ensureEdgeTickMarksVisible": False,
                    "alignLabels": False,
                    "entireTextOnly": False,
                    "minimumWidth": 72,
                    "scaleMargins": {"top": 0.75, "bottom": 0},
                    "handleScale": False,
                    "handleSize": 20,
                    "priceScaleId": "volume"
                }
            }

        # Initialize parent class
        super().__init__(series=series_list, options=chart_options)

        # Store references for easy access
        self.candlestick_series = candlestick_series
        self.volume_series = volume_series if volume_data is not None else None
        self.volume_data = volume_data

    def get_candlestick_series(self) -> CandlestickSeries:
        """Get the candlestick series."""
        return self.candlestick_series

    def get_volume_series(self) -> Optional[HistogramSeries]:
        """Get the volume series if it exists."""
        return self.volume_series

    def has_volume(self) -> bool:
        """Check if the chart has volume data."""
        return self.volume_series is not None

    def update_volume_alpha(self, alpha: float) -> "PriceVolumeChart":
        """
        Update the volume transparency.

        Args:
            alpha: Transparency value (0.0 to 1.0)

        Returns:
            self: For method chaining.
        """
        if self.volume_series is not None:
            # Extract base color without alpha
            base_color = (
                self.volume_series.color[:-2]
                if len(self.volume_series.color) == 9
                else self.volume_series.color
            )
            self.volume_series.color = f"{base_color}{int(alpha * 255):02x}"
        return self

    def update_volume_color(self, color: str, alpha: Optional[float] = None) -> "PriceVolumeChart":
        """
        Update the volume color.

        Args:
            color: New color (hex format)
            alpha: Optional transparency value (0.0 to 1.0)

        Returns:
            self: For method chaining.
        """
        if self.volume_series is not None:
            if alpha is not None:
                self.volume_series.color = f"{color}{int(alpha * 255):02x}"
            else:
                # Keep existing alpha
                current_alpha = (
                    self.volume_series.color[-2:] if len(self.volume_series.color) == 9 else "ff"
                )
                self.volume_series.color = f"{color}{current_alpha}"
        return self
