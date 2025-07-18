"""Price-Volume composite chart."""

from typing import Any, List, Optional

from streamlit_lightweight_charts.data.models import HistogramData, OhlcData, OhlcvData
from streamlit_lightweight_charts.charts.candlestick_chart import CandlestickChart
from streamlit_lightweight_charts.charts.options import (
    ChartOptions,
    PriceScaleMargins,
    PriceScaleOptions,
)
from streamlit_lightweight_charts.charts.series import HistogramSeries, HistogramSeriesOptions


class PriceVolumeChart(CandlestickChart):
    """
    Candlestick chart with volume overlay.

    Inherits from CandlestickChart and adds volume visualization
    as a histogram overlay on the same chart. The volume is displayed
    using an independent Y-axis and scaled to not exceed 25% of the chart height.

    This provides all the functionality of a CandlestickChart plus
    volume visualization, making it ideal for financial analysis.
    """

    def __init__(
        self,
        data: List[OhlcvData],
        height: int = 500,
        options: Optional[ChartOptions] = None,
        series_options: Optional[Any] = None,
        volume_series_options: Optional[HistogramSeriesOptions] = None,
        **kwargs,
    ):
        """
        Initialize a candlestick chart with volume overlay.

        Args:
            data: List of OhlcvData objects containing OHLC and volume data
            height: Height of the chart
            options: Chart configuration options
            series_options: Candlestick series options (passed to parent)
            volume_series_options: Series options for volume histogram
            **kwargs: Additional arguments passed to CandlestickChart parent
        """
        # Prepare OHLC data for candlestick chart
        ohlc_data = [
            OhlcData(
                time=item.time, open_=item.open, high=item.high, low=item.low, close=item.close
            )
            for item in data
        ]

        # Configure chart options for volume overlay
        chart_options = self._configure_volume_options(options, height)

        # Initialize parent CandlestickChart
        super().__init__(
            data=ohlc_data,
            options=chart_options,
            series_options=series_options,
            **kwargs,
        )

        # Ensure candlestick series uses the right price scale
        if self.candlestick_series:
            self.candlestick_series.options.price_scale_id = "right_ohlcv"

        # Add volume series as overlay
        volume_series = self._create_volume_series(data, volume_series_options)
        self.add_series(volume_series)

        # Store reference for convenience
        self.volume_series = volume_series

    def _configure_volume_options(
        self, options: Optional[ChartOptions], height: int
    ) -> ChartOptions:
        """
        Configure chart options for volume overlay.

        Args:
            options: Original chart options
            height: Chart height

        Returns:
            Configured chart options with volume overlay settings
        """
        chart_options = options or ChartOptions(height=height)
        chart_options.height = height

        # Configure price scale for main candlestick series
        if chart_options.right_price_scale is None:
            chart_options.right_price_scale = PriceScaleOptions()
        
        # Set price scale ID for candlestick series
        chart_options.right_price_scale.price_scale_id = "right_ohlcv"
        
        # Only override scale margins if not already set
        if not hasattr(chart_options.right_price_scale, 'scale_margins') or chart_options.right_price_scale.scale_margins is None:
            chart_options.right_price_scale.scale_margins = PriceScaleMargins(top=0.1, bottom=0.25)
        
        chart_options.right_price_scale.visible = True  # Ensure price scale is visible

        # Configure left price scale for volume (independent Y-axis)
        if chart_options.left_price_scale is None:
            chart_options.left_price_scale = PriceScaleOptions()
        chart_options.left_price_scale.price_scale_id = "left_volume"  # Set price scale ID for volume
        # Scale volume to occupy only the bottom 25% of chart area
        chart_options.left_price_scale.scale_margins = PriceScaleMargins(top=0.75, bottom=0.1)
        chart_options.left_price_scale.visible = False  # Hide volume scale labels

        return chart_options

    def _create_volume_series(
        self,
        data: List[OhlcvData],
        series_options: Optional[HistogramSeriesOptions],
    ) -> HistogramSeries:
        """
        Create volume histogram series as overlay.

        Args:
            data: List of OhlcvData objects containing volume data
            series_options: Options for volume series styling

        Returns:
            HistogramSeries configured for volume overlay
        """
        # Prepare volume data with color based on price movement
        volume_data = self._prepare_volume_data(data)

        # Create volume series options
        if series_options is None:
            options = HistogramSeriesOptions(color="#26a69a")
        else:
            options = series_options
        
        # Always set price scale ID to use left price scale (independent Y-axis)
        # This ensures the volume series uses the left price scale regardless of passed options
        options.price_scale_id = "left_volume"

        return HistogramSeries(data=volume_data, options=options)

    def _prepare_volume_data(self, data: List[OhlcvData]) -> List[HistogramData]:
        """
        Prepare volume data with color based on price movement.

        Args:
            data: List of OhlcvData objects containing volume and OHLC data

        Returns:
            List of HistogramData objects for volume visualization
        """
        volume_data = []

        for item in data:
            # Determine color based on price movement
            color = (
                "rgba(38, 166, 154, 0.4)"  # Green for up
                if item.close >= item.open
                else "rgba(239, 83, 80, 0.4)"  # Red for down
            )

            volume_data.append(
                HistogramData(
                    time=item.time,
                    value=item.volume,
                    color=color,
                )
            )

        return volume_data
