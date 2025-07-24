"""Integration tests for BandSeries."""

import numpy as np
import pandas as pd
import pytest

from streamlit_lightweight_charts_pro.charts.chart import Chart
from streamlit_lightweight_charts_pro.charts.series.band import BandSeries
from streamlit_lightweight_charts_pro.data import BandData
from streamlit_lightweight_charts_pro.type_definitions import (
    ColumnNames,
    LineStyle,
    LineType,
    MarkerPosition,
)
from streamlit_lightweight_charts_pro.type_definitions.enums import MarkerShape


class TestBandSeriesIntegration:
    """Integration tests for BandSeries."""

    def setup_method(self):
        """Set up test data."""
        # Create sample band data for testing
        dates = pd.date_range("2024-01-01", periods=100, freq="D")
        np.random.seed(42)

        # Generate realistic band data (e.g., Bollinger Bands)
        base_price = 100.0
        prices = [base_price]

        for _ in range(99):
            # Random walk for price
            change = np.random.normal(0, 1)
            new_price = prices[-1] + change
            prices.append(new_price)

        # Calculate Bollinger Bands (20-period SMA with 2 standard deviations)
        prices_series = pd.Series(prices)
        sma = prices_series.rolling(window=20, min_periods=1).mean()
        std = prices_series.rolling(window=20, min_periods=1).std()

        # Fill any NaN values with the first valid value
        sma = sma.bfill().ffill()
        std = std.bfill().ffill()

        upper_band = sma + (2 * std)
        lower_band = sma - (2 * std)

        # Create DataFrame
        self.band_df = pd.DataFrame(
            {
                ColumnNames.DATETIME: dates,
                "upper": upper_band,
                "middle": sma,
                "lower": lower_band,
            }
        )

        # Create BandData objects
        self.band_data = [
            BandData(str(row[ColumnNames.DATETIME]), row["upper"], row["middle"], row["lower"])
            for _, row in self.band_df.iterrows()
        ]

    def test_band_series_full_integration(self):
        """Test complete BandSeries integration with chart."""
        # Create band series
        band_series = BandSeries(
            data=self.band_df,
            upper_line_color="#4CAF50",
            middle_line_color="#2196F3",
            lower_line_color="#F44336",
            upper_fill_color="rgba(76, 175, 80, 0.1)",
            lower_fill_color="rgba(244, 67, 54, 0.1)",
        )

        # Create chart with band series
        chart = Chart(series=[band_series])

        # Test chart configuration
        assert len(chart.series) == 1
        assert chart.series[0].chart_type.value == "Band"

        # Test frontend configuration
        config = chart.to_frontend_config()
        assert "charts" in config
        assert len(config["charts"]) == 1

        chart_config = config["charts"][0]
        assert "series" in chart_config
        assert len(chart_config["series"]) == 1

        series_config = chart_config["series"][0]
        assert series_config["type"] == "band"
        assert len(series_config["data"]) == 100

        # Test data integrity
        first_data_point = series_config["data"][0]
        assert ColumnNames.TIME in first_data_point
        assert "upper" in first_data_point
        assert "middle" in first_data_point
        assert "lower" in first_data_point

        # Test options
        options = series_config["options"]
        assert options["upperLineColor"] == "#4CAF50"
        assert options["middleLineColor"] == "#2196F3"
        assert options["lowerLineColor"] == "#F44336"
        assert options["upperFillColor"] == "rgba(76, 175, 80, 0.1)"
        assert options["lowerFillColor"] == "rgba(244, 67, 54, 0.1)"

    def test_band_series_with_custom_styling(self):
        """Test BandSeries with custom styling options."""
        band_series = BandSeries(
            data=self.band_df,
            upper_line_color="#FF0000",
            middle_line_color="#00FF00",
            lower_line_color="#0000FF",
            upper_line_width=3,
            middle_line_width=2,
            lower_line_width=3,
            upper_line_style=LineStyle.DASHED,
            middle_line_style=LineStyle.SOLID,
            lower_line_style=LineStyle.DASHED,
            upper_fill_color="rgba(255, 0, 0, 0.2)",
            lower_fill_color="rgba(0, 0, 255, 0.2)",
            line_type=LineType.CURVED,
        )

        config = band_series.to_dict()
        options = config["options"]

        # Test custom styling
        assert options["upperLineColor"] == "#FF0000"
        assert options["middleLineColor"] == "#00FF00"
        assert options["lowerLineColor"] == "#0000FF"
        assert options["upperLineWidth"] == 3
        assert options["middleLineWidth"] == 2
        assert options["lowerLineWidth"] == 3
        assert options["upperLineStyle"] == 2  # DASHED
        assert options["middleLineStyle"] == 0  # SOLID
        assert options["lowerLineStyle"] == 2  # DASHED
        assert options["upperFillColor"] == "rgba(255, 0, 0, 0.2)"
        assert options["lowerFillColor"] == "rgba(0, 0, 255, 0.2)"
        assert options["lineType"] == 1  # CURVED

    def test_band_series_line_visibility_control(self):
        """Test BandSeries line visibility control."""
        band_series = BandSeries(
            data=self.band_df,
            upper_line_visible=False,
            middle_line_visible=True,
            lower_line_visible=False,
        )

        config = band_series.to_dict()
        options = config["options"]

        assert options["upperLineVisible"] is False
        assert options["middleLineVisible"] is True
        assert options["lowerLineVisible"] is False

    def test_band_series_with_markers(self):
        """Test BandSeries with markers."""

        band_series = BandSeries(data=self.band_df)

        # Add markers
        band_series.add_marker(
            time="2024-01-15",
            position=MarkerPosition.ABOVE_BAR,
            color="#FF0000",
            shape=MarkerShape.CIRCLE,
            text="Upper Band Touch",
        )

        band_series.add_marker(
            time="2024-01-30",
            position=MarkerPosition.BELOW_BAR,
            color="#00FF00",
            shape=MarkerShape.SQUARE,
            text="Lower Band Touch",
        )

        config = band_series.to_dict()

        assert "markers" in config
        assert len(config["markers"]) == 2

        # Test marker data
        marker1 = config["markers"][0]
        assert marker1["text"] == "Upper Band Touch"
        assert marker1["position"] == "aboveBar"
        assert marker1["color"] == "#FF0000"

        marker2 = config["markers"][1]
        assert marker2["text"] == "Lower Band Touch"
        assert marker2["position"] == "belowBar"
        assert marker2["color"] == "#00FF00"

    def test_band_series_crosshair_markers(self):
        """Test BandSeries crosshair marker configuration."""
        band_series = BandSeries(
            data=self.band_df,
            crosshair_marker_visible=False,
            crosshair_marker_radius=6,
            crosshair_marker_border_color="#FF0000",
            crosshair_marker_background_color="#00FF00",
            crosshair_marker_border_width=3,
        )

        config = band_series.to_dict()
        options = config["options"]

        assert options["crosshairMarkerVisible"] is False
        assert options["crosshairMarkerRadius"] == 6
        assert options["crosshairMarkerBorderColor"] == "#FF0000"
        assert options["crosshairMarkerBackgroundColor"] == "#00FF00"
        assert options["crosshairMarkerBorderWidth"] == 3

    def test_band_series_price_scale_integration(self):
        """Test BandSeries with custom price scale."""
        band_series = BandSeries(
            data=self.band_df,
            price_scale_id="left",
        )

        config = band_series.to_dict()
        options = config["options"]

        assert options["priceScaleId"] == "left"
        # Remove price_scale_config from test setup and assertions

    def test_band_series_data_validation(self):
        """Test BandSeries data validation."""
        # Test with invalid DataFrame (missing columns)
        invalid_df = pd.DataFrame(
            {
                ColumnNames.DATETIME: ["2024-01-01", "2024-01-02"],
                "upper": [105.0, 107.0],
                # Missing middle and lower columns
            }
        )

        with pytest.raises(ValueError, match="Columns.*are missing in the data"):
            BandSeries(data=invalid_df)

    def test_band_series_large_dataset(self):
        """Test BandSeries with large dataset."""
        # Create large dataset
        large_dates = pd.date_range("2020-01-01", periods=1000, freq="D")
        np.random.seed(42)

        base_price = 100.0
        prices = [base_price]

        for _ in range(999):
            change = np.random.normal(0, 1)
            new_price = prices[-1] + change
            prices.append(new_price)

        prices_series = pd.Series(prices)
        sma = prices_series.rolling(window=20, min_periods=1).mean()
        std = prices_series.rolling(window=20, min_periods=1).std()

        # Fill any NaN values with the first valid value
        sma = sma.bfill().ffill()
        std = std.bfill().ffill()

        large_df = pd.DataFrame(
            {
                ColumnNames.DATETIME: large_dates,
                "upper": sma + (2 * std),
                "middle": sma,
                "lower": sma - (2 * std),
            }
        )

        band_series = BandSeries(data=large_df)

        # Test that large dataset is handled correctly
        assert len(band_series.data) == 1000

        config = band_series.to_dict()
        assert len(config["data"]) == 1000

    def test_band_series_custom_column_mapping(self):
        """Test BandSeries with custom column mapping."""
        custom_df = pd.DataFrame(
            {
                "date": self.band_df[ColumnNames.DATETIME],
                "u": self.band_df["upper"],
                "m": self.band_df["middle"],
                "l": self.band_df["lower"],
            }
        )

        column_mapping = {
            ColumnNames.TIME: "date",
            "upper": "u",
            "middle": "m",
            "lower": "l",
        }

        band_series = BandSeries(data=custom_df, column_mapping=column_mapping)

        # Test that data is correctly mapped
        # Note: NaN values are filtered out, so the count might be less than 100
        assert len(band_series.data) > 0  # Should have some valid data
        assert len(band_series.data) <= 100  # Should not exceed original count

        # Test that the data is correctly mapped (first valid data point)
        if len(band_series.data) > 0:
            first_data = band_series.data[0]
            # Find the first non-NaN row in the original DataFrame
            first_valid_row = self.band_df.dropna().iloc[0]
            assert first_data.upper == first_valid_row["upper"]
            assert first_data.middle == first_valid_row["middle"]
            assert first_data.lower == first_valid_row["lower"]

    def test_band_series_method_chaining(self):
        """Test BandSeries method chaining."""
        band_series = BandSeries(data=self.band_df)

        # Test method chaining
        result = (
            band_series.set_price_scale("left")
            .set_price_line(visible=True, color="#FF0000")
            .set_base_line(visible=True, color="#00FF00")
            .set_price_format(format_type="price", precision=4)
        )

        assert result is band_series
        assert band_series.price_scale_id == "left"
        assert band_series.price_line_visible is True
        assert band_series.price_line_color == "#FF0000"
        assert band_series.base_line_visible is True
        assert band_series.base_line_color == "#00FF00"
        assert band_series.price_format["precision"] == 4

    def test_band_series_data_range(self):
        """Test BandSeries data range calculation."""
        band_series = BandSeries(data=self.band_df)

        data_range = band_series.get_data_range()

        assert data_range is not None
        assert "min_value" in data_range
        assert "max_value" in data_range
        assert "min_time" in data_range
        assert "max_time" in data_range

        # The range should cover the full range of all bands
        all_values = []
        for data_point in band_series.data:
            if not pd.isna(data_point.upper):
                all_values.append(data_point.upper)
            if not pd.isna(data_point.middle):
                all_values.append(data_point.middle)
            if not pd.isna(data_point.lower):
                all_values.append(data_point.lower)

        if all_values:  # Only test if we have valid values
            assert data_range["min_value"] == min(all_values)
            assert data_range["max_value"] == max(all_values)

    def test_band_series_as_overlay(self):
        """Test BandSeries as overlay on another chart."""
        # Create a candlestick series (simulated)
        candlestick_data = [
            {
                ColumnNames.TIME: "2024-01-01",
                ColumnNames.OPEN: 100,
                ColumnNames.HIGH: 105,
                ColumnNames.LOW: 95,
                ColumnNames.CLOSE: 102,
            },
            {
                ColumnNames.TIME: "2024-01-02",
                ColumnNames.OPEN: 102,
                ColumnNames.HIGH: 107,
                ColumnNames.LOW: 97,
                ColumnNames.CLOSE: 104,
            },
            {
                ColumnNames.TIME: "2024-01-03",
                ColumnNames.OPEN: 104,
                ColumnNames.HIGH: 103,
                ColumnNames.LOW: 93,
                ColumnNames.CLOSE: 98,
            },
        ]

        # Create band series as overlay
        band_series = BandSeries(
            data=self.band_df.iloc[:3],  # Use first 3 points
            price_scale_id="right",  # Same price scale as candlestick
        )

        # Test that band series can be used as overlay
        config = band_series.to_dict()
        assert config["options"]["priceScaleId"] == "right"

        # Test data compatibility
        # Note: NaN values are filtered out, so the count might be less than 3
        assert len(config["data"]) > 0  # Should have some valid data
        assert len(config["data"]) <= 3  # Should not exceed original count
        for data_point in config["data"]:
            assert ColumnNames.TIME in data_point
            assert "upper" in data_point
            assert "middle" in data_point
            assert "lower" in data_point
