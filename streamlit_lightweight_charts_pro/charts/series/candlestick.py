"""Candlestick series for streamlit-lightweight-charts."""

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Sequence, Union

import pandas as pd

from streamlit_lightweight_charts_pro.charts.series.base import Series
from streamlit_lightweight_charts_pro.data import OhlcData, OhlcvData, TradeVisualizationOptions
from streamlit_lightweight_charts_pro.type_definitions import ChartType

if TYPE_CHECKING:
    from streamlit_lightweight_charts_pro.data.trade import Trade


class CandlestickSeries(Series):
    """Candlestick series for lightweight charts."""

    def __init__(
        self,
        data: Union[Sequence[Union[OhlcData, OhlcvData]], pd.DataFrame],
        column_mapping: Optional[Dict[str, str]] = None,
        markers: Optional[List[Any]] = None,
        price_scale: Optional[Dict[str, Any]] = None,
        trades: Optional[List["Trade"]] = None,
        trade_visualization_options: Optional["TradeVisualizationOptions"] = None,
        # Candlestick-specific options
        up_color: str = "#4CAF50",  # TradingView vibrant green
        down_color: str = "#F44336",  # TradingView vibrant red
        wick_visible: bool = True,
        border_visible: bool = True,
        border_color: str = "#378658",
        border_up_color: str = "#4CAF50",  # TradingView vibrant green
        border_down_color: str = "#F44336",  # TradingView vibrant red
        wick_color: str = "#737375",
        wick_up_color: str = "#4CAF50",  # TradingView vibrant green
        wick_down_color: str = "#F44336",  # TradingView vibrant red
        **kwargs,
    ):
        """Initialize candlestick series."""
        # Store column mapping first
        self.column_mapping = column_mapping

        # Candlestick-specific styling options
        self.up_color = up_color
        self.down_color = down_color
        self.wick_visible = wick_visible
        self.border_visible = border_visible
        self.border_color = border_color
        self.border_up_color = border_up_color
        self.border_down_color = border_down_color
        self.wick_color = wick_color
        self.wick_up_color = wick_up_color
        self.wick_down_color = wick_down_color

        # Trade visualization
        self.trades = trades or []
        self.trade_visualization_options = trade_visualization_options

        # Call parent constructor after setting column_mapping
        super().__init__(
            data=data,
            markers=markers,
            price_scale_config=price_scale,
            **kwargs,
        )

    @property
    def chart_type(self) -> ChartType:
        """Get the chart type for this series."""
        return ChartType.CANDLESTICK

    def _process_dataframe(self, df: pd.DataFrame) -> List[Union[OhlcData, OhlcvData]]:
        """
        Process pandas DataFrame into OHLC/OHLCV data format.

        This method converts a pandas DataFrame into a list of OhlcData or OhlcvData
        objects for candlestick chart visualization.

        Args:
            df: Pandas DataFrame to process.

        Returns:
            List[Union[OhlcData, OhlcvData]]: List of processed data objects.

        Raises:
            ValueError: If required columns are missing from the DataFrame.
        """
        # Use default column mapping if none provided
        column_mapping = self.column_mapping or {
            "time": "datetime",
            "open": "open",
            "high": "high",
            "low": "low",
            "close": "close",
            "volume": "volume",
        }

        time_col = column_mapping.get("time", "datetime")
        open_col = column_mapping.get("open", "open")
        high_col = column_mapping.get("high", "high")
        low_col = column_mapping.get("low", "low")
        close_col = column_mapping.get("close", "close")
        volume_col = column_mapping.get("volume", "volume")

        # Check for required OHLC columns
        required_cols = [time_col, open_col, high_col, low_col, close_col]
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise ValueError(f"DataFrame must contain columns: {', '.join(missing_cols)}")

        # Check if volume column exists
        has_volume = volume_col in df.columns

        # Use vectorized operations for better performance
        times = df[time_col].astype(str).tolist()
        opens = df[open_col].astype(float).tolist()
        highs = df[high_col].astype(float).tolist()
        lows = df[low_col].astype(float).tolist()
        closes = df[close_col].astype(float).tolist()

        if has_volume:
            volumes = df[volume_col].astype(float).tolist()
            return [
                OhlcvData(
                    time=time,
                    open_=open_val,
                    high=high_val,
                    low=low_val,
                    close=close_val,
                    volume=volume_val,
                )
                for time, open_val, high_val, low_val, close_val, volume_val in zip(
                    times, opens, highs, lows, closes, volumes
                )
            ]
        else:
            return [
                OhlcData(time=time, open_=open_val, high=high_val, low=low_val, close=close_val)
                for time, open_val, high_val, low_val, close_val in zip(
                    times, opens, highs, lows, closes
                )
            ]

    def to_frontend_config(self) -> Dict[str, Any]:
        """
        Convert candlestick series to frontend-compatible configuration.

        Creates a dictionary representation of the candlestick series suitable
        for consumption by the frontend React component.

        Returns:
            Dict[str, Any]: Frontend-compatible configuration dictionary
                containing series type, data, and styling options.

        Example:
            ```python
            config = series.to_frontend_config()
            # Returns: {
            #     "type": "candlestick",
            #     "data": [...],
            #     "options": {...}
            # }
            ```
        """
        # Base configuration
        config = {
            "type": "candlestick",
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
                # Candlestick-specific options
                "upColor": self.up_color,
                "downColor": self.down_color,
                "wickVisible": self.wick_visible,
                "borderVisible": self.border_visible,
                "borderColor": self.border_color,
                "borderUpColor": self.border_up_color,
                "borderDownColor": self.border_down_color,
                "wickColor": self.wick_color,
                "wickUpColor": self.wick_up_color,
                "wickDownColor": self.wick_down_color,
            },
        }

        # Add optional fields only if they are set
        if self.markers:
            config["markers"] = [marker.to_dict() for marker in self.markers]

        if self.price_scale_config:
            config["priceScale"] = self.price_scale_config

        # Add trade visualization if configured
        if self.trades and self.trade_visualization_options:
            config["trades"] = [trade.to_dict() for trade in self.trades]
            config["tradeVisualizationOptions"] = self.trade_visualization_options.to_dict()

        return config

    def _get_options_dict(self) -> Dict[str, Any]:
        """Get options dictionary for candlestick series."""
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

        # Add candlestick-specific options
        options.update(
            {
                "upColor": self.up_color,
                "downColor": self.down_color,
                "wickVisible": self.wick_visible,
                "borderVisible": self.border_visible,
                "borderColor": self.border_color,
                "borderUpColor": self.border_up_color,
                "borderDownColor": self.border_down_color,
                "wickColor": self.wick_color,
                "wickUpColor": self.wick_up_color,
                "wickDownColor": self.wick_down_color,
            }
        )

        return options
