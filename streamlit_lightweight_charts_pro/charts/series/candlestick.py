"""
Candlestick series for streamlit-lightweight-charts.

This module provides the CandlestickSeries class for creating candlestick charts that display
OHLC or OHLCV data. Candlestick series are commonly used for price charts and technical analysis.

The CandlestickSeries class supports various styling options for up/down colors, wicks, borders,
and animation effects. It also supports markers, price line configurations, and trade 
visualizations.

Example:
    from streamlit_lightweight_charts_pro.charts.series import CandlestickSeries
    from streamlit_lightweight_charts_pro.data import OhlcData

    # Create candlestick data
    data = [
        OhlcData("2024-01-01", 100, 105, 98, 103),
        OhlcData("2024-01-02", 103, 108, 102, 106)
    ]

    # Create candlestick series with styling
    series = CandlestickSeries(
        data=data,
        up_color="#4CAF50",
        down_color="#F44336"
    )
"""

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Sequence, Union

import pandas as pd

from streamlit_lightweight_charts_pro.charts.series.base import Series
from streamlit_lightweight_charts_pro.data import OhlcData, OhlcvData, TradeVisualizationOptions
from streamlit_lightweight_charts_pro.type_definitions import ChartType, ColumnNames
from streamlit_lightweight_charts_pro.utils import add_trades_to_series

if TYPE_CHECKING:
    from streamlit_lightweight_charts_pro.data.trade import Trade


class CandlestickSeries(Series):
    """Candlestick series for lightweight charts."""

    def __init__(
        self,
        data: Union[Sequence[Union[OhlcData, OhlcvData]], pd.DataFrame],
        column_mapping: Optional[Dict[str, str]] = None,
        markers: Optional[List[Any]] = None,
        trades: Optional[List["Trade"]] = None,
        trade_visualization_options: Optional["TradeVisualizationOptions"] = None,
        up_color: str = "#4CAF50",
        down_color: str = "#F44336",
        wick_visible: bool = True,
        border_visible: bool = True,
        border_color: str = "#378658",
        border_up_color: str = "#4CAF50",
        border_down_color: str = "#F44336",
        wick_color: str = "#737375",
        wick_up_color: str = "#4CAF50",
        wick_down_color: str = "#F44336",
        pane_id: int = 0,
        **kwargs,
    ):
        super().__init__(
            data=data,
            column_mapping=column_mapping,
            markers=markers,
            pane_id=pane_id,
            **kwargs,
        )
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
        self.trades = trades or []
        self.trade_visualization_options = trade_visualization_options

    @property
    def chart_type(self) -> ChartType:
        """Get the chart type for this series."""
        return ChartType.CANDLESTICK

    def _get_columns(self) -> Dict[str, str]:
        """
        Return the column mapping for candlestick series, using self.column_mapping if set.
        """
        return self.column_mapping or {
            ColumnNames.TIME: ColumnNames.DATETIME,
            ColumnNames.OPEN: ColumnNames.OPEN,
            ColumnNames.HIGH: ColumnNames.HIGH,
            ColumnNames.LOW: ColumnNames.LOW,
            ColumnNames.CLOSE: ColumnNames.CLOSE,
        }

    def _normalize_input_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Normalize input data to ensure consistent format for candlestick series.

        This method overrides the base class method to handle volume as optional.
        Only OHLC columns are required; volume is optional.

        Args:
            data: Pandas DataFrame to normalize.

        Returns:
            pd.DataFrame: Normalized pandas DataFrame.

        Raises:
            ValueError: If required OHLC columns are missing from the DataFrame.
        """
        if isinstance(data, pd.Series):
            data = data.to_frame()

        columns_mapping = self._get_columns()

        # Only require OHLC columns, volume is optional
        required_columns = [
            ColumnNames.TIME,
            ColumnNames.OPEN,
            ColumnNames.HIGH,
            ColumnNames.LOW,
            ColumnNames.CLOSE,
        ]
        required_col_names = [columns_mapping.get(col, col) for col in required_columns]

        data = self._process_index_columns(data, required_col_names)
        if not all(col in data.columns for col in required_col_names):
            missing = [col for col in required_col_names if col not in data.columns]
            raise ValueError(f"Columns {missing} are missing in the data")

        data = self._process_dataframe(data)

        return data

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
        # Use _get_columns for column mapping
        column_mapping = self._get_columns()

        time_col = column_mapping.get(ColumnNames.TIME, ColumnNames.DATETIME)
        open_col = column_mapping.get(ColumnNames.OPEN, ColumnNames.OPEN)
        high_col = column_mapping.get(ColumnNames.HIGH, ColumnNames.HIGH)
        low_col = column_mapping.get(ColumnNames.LOW, ColumnNames.LOW)
        close_col = column_mapping.get(ColumnNames.CLOSE, ColumnNames.CLOSE)

        # Check for required OHLC columns
        required_cols = [time_col, open_col, high_col, low_col, close_col]
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise ValueError(f"DataFrame must contain columns: {', '.join(missing_cols)}")

        # Use vectorized operations for better performance
        times = df[time_col].astype(str).tolist()
        opens = df[open_col].astype(float).tolist()
        highs = df[high_col].astype(float).tolist()
        lows = df[low_col].astype(float).tolist()
        closes = df[close_col].astype(float).tolist()

        return [
            OhlcData(time=time, open_=open_val, high=high_val, low=low_val, close=close_val)
            for time, open_val, high_val, low_val, close_val in zip(
                times, opens, highs, lows, closes
            )
        ]

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert candlestick series to dictionary representation.

        Creates a dictionary representation of the candlestick series suitable
        for consumption by the frontend React component.

        Returns:
            Dict[str, Any]: Dictionary representation of the candlestick series
                containing series type, data, and styling options.

        Example:
            ```python
            config = series.to_dict()
            # Returns: {
            #     "type": "candlestick",
            #     "data": [...],
            #     "options": {...}
            # }
            ```
        """
        # Validate pane configuration
        self._validate_pane_config()

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

        # Remove priceScale from series config
        # if self.price_scale_config:
        #     config["priceScale"] = self.price_scale_config.to_dict()

        # Add trade visualizations if trades are provided
        if self.trades and self.trade_visualization_options:
            config = add_trades_to_series(config, self.trades, self.trade_visualization_options)

        # Add height and pane_id
        if self.height is not None:
            config["height"] = self.height
        config["pane_id"] = self.pane_id
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
