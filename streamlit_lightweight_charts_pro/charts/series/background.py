"""
Background series for streamlit-lightweight-charts.

This module provides the BackgroundSeries class for creating background shading
that changes color based on indicator values. The background is rendered behind
all other chart elements and can be used to highlight market conditions,
overbought/oversold zones, or other technical indicators.

Example:
    ```python
    from streamlit_lightweight_charts_pro.charts.series import BackgroundSeries
    from streamlit_lightweight_charts_pro.data import BackgroundData
    
    # Create background data for market conditions
    data = [
        BackgroundData("2024-01-01", 0.2, "#FFE5E5", "#E5FFE5"),  # Bearish
        BackgroundData("2024-01-02", 0.8, "#FFE5E5", "#E5FFE5"),  # Bullish
    ]
    
    # Create background series
    series = BackgroundSeries(data=data)
    ```
"""

from typing import List, Optional, Union

import pandas as pd

from streamlit_lightweight_charts_pro.charts.series.base import Series
from streamlit_lightweight_charts_pro.data.background_data import BackgroundData
from streamlit_lightweight_charts_pro.type_definitions import ChartType


class BackgroundSeries(Series):
    """
    Background series for indicator-based background shading.
    
    This series creates a background layer that changes color based on indicator
    values. The color is interpolated between minColor and maxColor based on
    the data value, making it ideal for visualizing market conditions,
    sentiment indicators, or technical analysis zones.
    
    The background is rendered behind all other chart elements and spans the
    full height of the chart pane.
    
    Attributes:
        data: List of BackgroundData points with time, value, and color settings
        visible: Whether the series is visible (default: True)
        price_scale_id: Price scale to use (default: "right")
        pane_id: Pane to render in (default: 0)
        overlay: Whether to overlay on price (default: True)
        
    Example:
        ```python
        # Create RSI-based background shading
        rsi_data = [
            BackgroundData(
                time="2024-01-01",
                value=0.3,  # RSI 30 - oversold
                minColor="#FFE5E5",  # Light red
                maxColor="#E5FFE5"   # Light green
            ),
            BackgroundData(
                time="2024-01-02", 
                value=0.7,  # RSI 70 - overbought
                minColor="#FFE5E5",
                maxColor="#E5FFE5"
            )
        ]
        
        background_series = BackgroundSeries(data=rsi_data)
        ```
    """
    
    DATA_CLASS = BackgroundData
    
    @property
    def chart_type(self) -> ChartType:
        """Get the chart type for this series."""
        return ChartType.BACKGROUND
    
    def __init__(
        self,
        data: Union[List[BackgroundData], pd.DataFrame, pd.Series],
        column_mapping: Optional[dict] = None,
        visible: bool = True,
        price_scale_id: str = "right",
        pane_id: Optional[int] = 0,
        overlay: Optional[bool] = True,
    ):
        """
        Initialize background series.
        
        Args:
            data: List of BackgroundData or DataFrame with background data
            column_mapping: Column mapping for DataFrame input
            visible: Whether the series is visible
            price_scale_id: Price scale to use
            pane_id: Pane to render in
            overlay: Whether to overlay on price
        """
        super().__init__(
            data=data,
            column_mapping=column_mapping,
            visible=visible,
            price_scale_id=price_scale_id,
            pane_id=pane_id,
            overlay=overlay,
        )
    
    def to_dict(self) -> dict:
        """
        Convert series to dictionary for frontend.
        
        Returns:
            dict: Series configuration for frontend
            
        Example:
            ```python
            series = BackgroundSeries(data=[...])
            config = series.to_dict()
            # {
            #     'type': 'Background',
            #     'data': [...],
            #     'options': {...}
            # }
            ```
        """
        config = {
            "type": "Background",
            "data": self.data_dict,
            "options": {
                "visible": self.visible,
                "priceScaleId": self.price_scale_id,
            },
        }
        
        # Add optional configurations
        if self.pane_id is not None:
            config["options"]["paneId"] = self.pane_id
            
        if self.overlay is not None:
            config["options"]["overlay"] = self.overlay
            
        if self._price_format:
            config["options"]["priceFormat"] = self._price_format.to_dict()
            
        return config