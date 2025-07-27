"""
Shared test configuration and fixtures for Streamlit Lightweight Charts Pro.

This module provides common fixtures, utilities, and configuration that can be
used across all test modules.
"""

from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import pytest

# Import modules only when needed to avoid import errors during test discovery
try:
    from streamlit_lightweight_charts_pro.charts.options import (
        ChartOptions,
        InteractionOptions,
        LayoutOptions,
    )
    from streamlit_lightweight_charts_pro.data import (
        AreaData,
        BandData,
        BarData,
        BaselineData,
        CandlestickData,
        HistogramData,
        LineData,
        Marker,
    )
    from streamlit_lightweight_charts_pro.series import (
        AreaSeries,
        BandSeries,
        BarSeries,
        BaselineSeries,
        CandlestickSeries,
        HistogramSeries,
        LineSeries,
    )

    IMPORTS_AVAILABLE = True
except ImportError:
    IMPORTS_AVAILABLE = False


@pytest.fixture
def sample_timestamps():
    """Generate sample timestamps for testing."""
    base_time = datetime(2023, 1, 1)
    return [base_time + timedelta(hours=i) for i in range(10)]


@pytest.fixture
def sample_values():
    """Generate sample numeric values for testing."""
    return [100 + i * 10 + np.random.randint(-5, 5) for i in range(10)]


@pytest.fixture
def sample_ohlc_data():
    """Generate sample OHLC data for testing."""
    base_price = 100.0
    data = []
    for i in range(10):
        open_price = base_price + i * 2 + np.random.randint(-5, 5)
        high_price = open_price + np.random.randint(1, 10)
        low_price = open_price - np.random.randint(1, 10)
        close_price = open_price + np.random.randint(-5, 5)
        volume = np.random.randint(100, 1000)

        data.append(
            {
                "open": open_price,
                "high": high_price,
                "low": low_price,
                "close": close_price,
                "volume": volume,
            }
        )
    return data


@pytest.fixture
def sample_dataframe():
    """Generate sample DataFrame for testing."""
    dates = pd.date_range("2023-01-01", periods=10, freq="H")
    data = {
        "time": dates,
        "value": [100 + i * 10 + np.random.randint(-5, 5) for i in range(10)],
        "open": [100 + i * 2 + np.random.randint(-5, 5) for i in range(10)],
        "high": [110 + i * 2 + np.random.randint(1, 10) for i in range(10)],
        "low": [90 + i * 2 - np.random.randint(1, 10) for i in range(10)],
        "close": [105 + i * 2 + np.random.randint(-5, 5) for i in range(10)],
        "volume": [np.random.randint(100, 1000) for _ in range(10)],
    }
    return pd.DataFrame(data)


@pytest.fixture
def sample_line_data(sample_timestamps, sample_values):
    """Generate sample LineData for testing."""
    if not IMPORTS_AVAILABLE:
        pytest.skip("Required imports not available")
    return LineData(time=sample_timestamps, value=sample_values)


@pytest.fixture
def sample_area_data(sample_timestamps, sample_values):
    """Generate sample AreaData for testing."""
    if not IMPORTS_AVAILABLE:
        pytest.skip("Required imports not available")
    return AreaData(
        time=sample_timestamps,
        value=sample_values,
        lineColor="#ff0000",
        topColor="rgba(255, 0, 0, 0.3)",
        bottomColor="rgba(255, 0, 0, 0.1)",
    )


@pytest.fixture
def sample_candlestick_data(sample_timestamps, sample_ohlc_data):
    """Generate sample CandlestickData for testing."""
    if not IMPORTS_AVAILABLE:
        pytest.skip("Required imports not available")
    return CandlestickData(
        time=sample_timestamps,
        open=[d["open"] for d in sample_ohlc_data],
        high=[d["high"] for d in sample_ohlc_data],
        low=[d["low"] for d in sample_ohlc_data],
        close=[d["close"] for d in sample_ohlc_data],
    )


@pytest.fixture
def sample_bar_data(sample_timestamps, sample_ohlc_data):
    """Generate sample BarData for testing."""
    if not IMPORTS_AVAILABLE:
        pytest.skip("Required imports not available")
    return BarData(
        time=sample_timestamps,
        open=[d["open"] for d in sample_ohlc_data],
        high=[d["high"] for d in sample_ohlc_data],
        low=[d["low"] for d in sample_ohlc_data],
        close=[d["close"] for d in sample_ohlc_data],
    )


@pytest.fixture
def sample_histogram_data(sample_timestamps, sample_values):
    """Generate sample HistogramData for testing."""
    if not IMPORTS_AVAILABLE:
        pytest.skip("Required imports not available")
    return HistogramData(time=sample_timestamps, value=sample_values, color="#00ff00")


@pytest.fixture
def sample_baseline_data(sample_timestamps, sample_values):
    """Generate sample BaselineData for testing."""
    if not IMPORTS_AVAILABLE:
        pytest.skip("Required imports not available")
    return BaselineData(
        time=sample_timestamps,
        value=sample_values,
        topFillColor="rgba(0, 255, 0, 0.3)",
        bottomFillColor="rgba(255, 0, 0, 0.3)",
        topLineColor="#00ff00",
        bottomLineColor="#ff0000",
    )


@pytest.fixture
def sample_band_data(sample_timestamps, sample_values):
    """Generate sample BandData for testing."""
    if not IMPORTS_AVAILABLE:
        pytest.skip("Required imports not available")
    upper_values = [v + 10 for v in sample_values]
    lower_values = [v - 10 for v in sample_values]
    return BandData(
        time=sample_timestamps,
        upperValue=upper_values,
        lowerValue=lower_values,
        lineColor="#0000ff",
        topFillColor="rgba(0, 0, 255, 0.3)",
        bottomFillColor="rgba(0, 0, 255, 0.1)",
    )


@pytest.fixture
def sample_marker():
    """Generate sample Marker for testing."""
    if not IMPORTS_AVAILABLE:
        pytest.skip("Required imports not available")
    return Marker(
        time=datetime(2023, 1, 1, 12, 0),
        position="aboveBar",
        color="#ff0000",
        shape="circle",
        text="Test Marker",
    )


@pytest.fixture
def sample_line_series(sample_line_data):
    """Generate sample LineSeries for testing."""
    if not IMPORTS_AVAILABLE:
        pytest.skip("Required imports not available")
    return LineSeries(data=sample_line_data)


@pytest.fixture
def sample_area_series(sample_area_data):
    """Generate sample AreaSeries for testing."""
    if not IMPORTS_AVAILABLE:
        pytest.skip("Required imports not available")
    return AreaSeries(data=sample_area_data)


@pytest.fixture
def sample_candlestick_series(sample_candlestick_data):
    """Generate sample CandlestickSeries for testing."""
    if not IMPORTS_AVAILABLE:
        pytest.skip("Required imports not available")
    return CandlestickSeries(data=sample_candlestick_data)


@pytest.fixture
def sample_bar_series(sample_bar_data):
    """Generate sample BarSeries for testing."""
    if not IMPORTS_AVAILABLE:
        pytest.skip("Required imports not available")
    return BarSeries(data=sample_bar_data)


@pytest.fixture
def sample_histogram_series(sample_histogram_data):
    """Generate sample HistogramSeries for testing."""
    if not IMPORTS_AVAILABLE:
        pytest.skip("Required imports not available")
    return HistogramSeries(data=sample_histogram_data)


@pytest.fixture
def sample_baseline_series(sample_baseline_data):
    """Generate sample BaselineSeries for testing."""
    if not IMPORTS_AVAILABLE:
        pytest.skip("Required imports not available")
    return BaselineSeries(data=sample_baseline_data)


@pytest.fixture
def sample_band_series(sample_band_data):
    """Generate sample BandSeries for testing."""
    if not IMPORTS_AVAILABLE:
        pytest.skip("Required imports not available")
    return BandSeries(data=sample_band_data)


@pytest.fixture
def sample_chart_options():
    """Generate sample ChartOptions for testing."""
    if not IMPORTS_AVAILABLE:
        pytest.skip("Required imports not available")
    return ChartOptions(
        width=800,
        height=400,
        layout=LayoutOptions(background=dict(color="#ffffff"), textColor="#000000"),
        interaction=InteractionOptions(hoverMode="greedy", crosshairMode="normal"),
    )


@pytest.fixture
def sample_invalid_data():
    """Generate sample invalid data for testing error handling."""
    return {
        "time": [1, 2, 3],  # Invalid time format
        "value": ["a", "b", "c"],  # Invalid numeric values
        "open": [None, None, None],  # None values
        "high": [],  # Empty list
        "low": [1, 2],  # Mismatched lengths
        "close": [1.0, 2.0, 3.0],  # Valid data
    }


@pytest.fixture
def sample_large_dataset():
    """Generate large dataset for performance testing."""
    dates = pd.date_range("2023-01-01", periods=10000, freq="1min")
    data = {
        "time": dates,
        "value": np.random.randn(10000).cumsum() + 100,
        "volume": np.random.randint(100, 10000, 10000),
    }
    return pd.DataFrame(data)


class TestDataFactory:
    """Factory class for creating test data."""

    @staticmethod
    def create_line_data(count: int = 10, start_date: str = "2023-01-01"):
        """Create LineData with specified parameters."""
        if not IMPORTS_AVAILABLE:
            pytest.skip("Required imports not available")
        dates = pd.date_range(start_date, periods=count, freq="H")
        values = [100 + i * 10 + np.random.randint(-5, 5) for i in range(count)]
        return LineData(time=dates, value=values)

    @staticmethod
    def create_candlestick_data(count: int = 10, start_date: str = "2023-01-01"):
        """Create CandlestickData with specified parameters."""
        if not IMPORTS_AVAILABLE:
            pytest.skip("Required imports not available")
        dates = pd.date_range(start_date, periods=count, freq="H")
        data = []
        base_price = 100.0

        for i in range(count):
            open_price = base_price + i * 2 + np.random.randint(-5, 5)
            high_price = open_price + np.random.randint(1, 10)
            low_price = open_price - np.random.randint(1, 10)
            close_price = open_price + np.random.randint(-5, 5)

            data.append(
                {"open": open_price, "high": high_price, "low": low_price, "close": close_price}
            )

        return CandlestickData(
            time=dates,
            open=[d["open"] for d in data],
            high=[d["high"] for d in data],
            low=[d["low"] for d in data],
            close=[d["close"] for d in data],
        )


@pytest.fixture
def data_factory():
    """Provide access to TestDataFactory."""
    return TestDataFactory


# Performance testing utilities
@pytest.fixture
def performance_threshold():
    """Define performance thresholds for tests."""
    return {
        "data_creation": 0.1,  # seconds
        "serialization": 0.05,  # seconds
        "validation": 0.01,  # seconds
        "memory_usage": 100,  # MB
    }


# Integration testing utilities
@pytest.fixture
def mock_streamlit():
    """Mock Streamlit components for integration testing."""

    class MockStreamlit:
        def __init__(self):
            self.components = []
            self.calls = []

        def components_v1_html(self, html, **kwargs):
            self.components.append(html)
            self.calls.append(("components_v1_html", kwargs))
            return None

        def write(self, data):
            self.calls.append(("write", data))
            return None

    return MockStreamlit()


# E2E testing utilities
@pytest.fixture
def sample_chart_config():
    """Generate sample chart configuration for E2E testing."""
    return {
        "chart_type": "line",
        "data": {"time": ["2023-01-01", "2023-01-02", "2023-01-03"], "value": [100, 110, 120]},
        "options": {
            "width": 800,
            "height": 400,
            "layout": {"background": {"color": "#ffffff"}, "textColor": "#000000"},
        },
    }
