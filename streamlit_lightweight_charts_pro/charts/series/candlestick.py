"""Candlestick series for streamlit-lightweight-charts."""

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Sequence, Union

import pandas as pd

from streamlit_lightweight_charts_pro.data import OhlcData, OhlcvData, TradeVisualizationOptions
from streamlit_lightweight_charts_pro.type_definitions import ChartType
from streamlit_lightweight_charts_pro.charts.series.base import Series

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
        up_color: str = "#26a69a",
        down_color: str = "#ef5350",
        wick_visible: bool = True,
        border_visible: bool = True,
        border_color: str = "#378658",
        border_up_color: str = "#26a69a",
        border_down_color: str = "#ef5350",
        wick_color: str = "#737375",
        wick_up_color: str = "#26a69a",
        wick_down_color: str = "#ef5350",
        **kwargs
    ):
        """Initialize candlestick series."""
        super().__init__(
            data=data,
            column_mapping=column_mapping,
            markers=markers,
            price_scale=price_scale,
            **kwargs
        )
        
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

    @property
    def chart_type(self) -> ChartType:
        """Get the chart type for this series."""
        return ChartType.CANDLESTICK

    def _convert_dataframe(self, df: pd.DataFrame, column_mapping: Optional[Dict[str, str]] = None) -> Sequence[Union[OhlcData, OhlcvData]]:
        """Convert DataFrame to OHLC/OHLCV data format."""
        return self._convert_ohlc_dataframe(df, column_mapping)

    def _get_options_dict(self) -> Dict[str, Any]:
        """Get options dictionary for candlestick series."""
        options = self._base_dict()
        
        # Add candlestick-specific options
        options.update({
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
        })
        
        return options

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation with trade visualization."""
        result = super().to_dict()
        
        # Add trade visualization if configured
        if self.trades and self.trade_visualization_options:
            result["trades"] = [trade.to_dict() for trade in self.trades]
            result["tradeVisualizationOptions"] = self.trade_visualization_options.to_dict()
            
        return result 