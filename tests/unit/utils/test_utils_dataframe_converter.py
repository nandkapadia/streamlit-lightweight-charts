"""
Comprehensive tests for the dataframe_converter utility module.

This module tests the dataframe conversion utilities that handle conversion
between pandas DataFrames and the library's data models.
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any

from streamlit_lightweight_charts_pro.utils.dataframe_converter import (
    df_to_line_data,
    df_to_ohlc_data,
    df_to_ohlcv_data,
    df_to_histogram_data,
    df_to_baseline_data,
    resample_df_for_charts,
    df_to_data,
)


class TestDataFrameConverter:
    """Test suite for dataframe conversion utilities."""

    def setup_method(self):
        """Set up test data."""
        # Create sample datetime index
        self.dates = pd.date_range('2024-01-01', periods=10, freq='D')
        
        # Create sample OHLC data
        self.ohlc_df = pd.DataFrame({
            'datetime': self.dates,
            'open': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109],
            'high': [105, 106, 107, 108, 109, 110, 111, 112, 113, 114],
            'low': [98, 99, 100, 101, 102, 103, 104, 105, 106, 107],
            'close': [102, 103, 104, 105, 106, 107, 108, 109, 110, 111],
            'volume': [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900]
        })
        
        # Create sample single value data
        self.single_value_df = pd.DataFrame({
            'datetime': self.dates,
            'close': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109]
        })
        
        # Create sample histogram data
        self.histogram_df = pd.DataFrame({
            'datetime': self.dates,
            'volume': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109],
            'color': ['green', 'red', 'green', 'red', 'green', 'red', 'green', 'red', 'green', 'red']
        })
        
        # Create sample baseline data
        self.baseline_df = pd.DataFrame({
            'datetime': self.dates,
            'value': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109]
        })

    def test_df_to_line_data_with_index(self):
        """Test df_to_line_data with DataFrame index as time."""
        df = self.single_value_df.set_index('datetime')
        result = df_to_line_data(df, value_column='close')
        
        assert len(result) == 10
        assert result[0].time == self.dates[0]
        assert result[0].value == 100.0
        assert result[-1].value == 109.0

    def test_df_to_line_data_with_time_column(self):
        """Test df_to_line_data with specific time column."""
        result = df_to_line_data(self.single_value_df, value_column='close', time_column='datetime')
        
        assert len(result) == 10
        assert result[0].time == self.dates[0]
        assert result[0].value == 100.0

    def test_df_to_line_data_with_custom_value_column(self):
        """Test df_to_line_data with custom value column."""
        df = pd.DataFrame({
            'datetime': self.dates[:5],
            'price': [100, 101, 102, 103, 104]
        })
        result = df_to_line_data(df, value_column='price', time_column='datetime')
        
        assert len(result) == 5
        assert result[0].value == 100.0

    def test_df_to_line_data_with_string_dates(self):
        """Test df_to_line_data with string date format."""
        df = pd.DataFrame({
            'date': ['2024-01-01', '2024-01-02'],
            'close': [100, 105]
        })
        result = df_to_line_data(df, value_column='close', time_column='date')
        
        assert len(result) == 2
        assert result[0].time == pd.Timestamp('2024-01-01')
        assert result[0].value == 100.0

    def test_df_to_ohlc_data_with_time_column(self):
        """Test df_to_ohlc_data with time column."""
        result = df_to_ohlc_data(
            self.ohlc_df,
            time_column='datetime',
            open_column='open',
            high_column='high',
            low_column='low',
            close_column='close'
        )
        
        assert len(result) == 10
        assert result[0].open == 100.0
        assert result[0].high == 105.0
        assert result[0].low == 98.0
        assert result[0].close == 102.0

    def test_df_to_ohlc_data_with_index(self):
        """Test df_to_ohlc_data with DataFrame index as time."""
        df = self.ohlc_df.set_index('datetime')
        result = df_to_ohlc_data(df)
        
        assert len(result) == 10
        assert result[0].open == 100.0
        assert result[0].high == 105.0

    def test_df_to_ohlc_data_with_custom_columns(self):
        """Test df_to_ohlc_data with custom column names."""
        df = pd.DataFrame({
            'time': self.dates[:2],
            'o': [100, 101],
            'h': [105, 106],
            'l': [98, 99],
            'c': [102, 103]
        })
        result = df_to_ohlc_data(
            df,
            time_column='time',
            open_column='o',
            high_column='h',
            low_column='l',
            close_column='c'
        )
        
        assert len(result) == 2
        assert result[0].open == 100.0
        assert result[0].close == 102.0

    def test_df_to_ohlcv_data_with_time_column(self):
        """Test df_to_ohlcv_data with time column."""
        result = df_to_ohlcv_data(
            self.ohlc_df,
            time_column='datetime',
            open_column='open',
            high_column='high',
            low_column='low',
            close_column='close',
            volume_column='volume'
        )
        
        assert len(result) == 10
        assert result[0].open == 100.0
        assert result[0].high == 105.0
        assert result[0].low == 98.0
        assert result[0].close == 102.0
        assert result[0].volume == 1000.0

    def test_df_to_ohlcv_data_with_index(self):
        """Test df_to_ohlcv_data with DataFrame index as time."""
        df = self.ohlc_df.set_index('datetime')
        result = df_to_ohlcv_data(df)
        
        assert len(result) == 10
        assert result[0].open == 100.0
        assert result[0].volume == 1000.0

    def test_df_to_histogram_data_with_time_column(self):
        """Test df_to_histogram_data with time column."""
        result = df_to_histogram_data(
            self.histogram_df,
            value_column='volume',
            color_column='color',
            time_column='datetime'
        )
        
        assert len(result) == 10
        assert result[0].value == 100.0
        assert result[0].color == 'green'
        assert result[1].color == 'red'

    def test_df_to_histogram_data_with_index(self):
        """Test df_to_histogram_data with DataFrame index as time."""
        df = self.histogram_df.set_index('datetime')
        result = df_to_histogram_data(df, value_column='volume', color_column='color')
        
        assert len(result) == 10
        assert result[0].value == 100.0
        assert result[0].color == 'green'

    def test_df_to_histogram_data_without_color(self):
        """Test df_to_histogram_data without color column."""
        df = self.histogram_df.drop(columns=['color'])
        result = df_to_histogram_data(df, value_column='volume', time_column='datetime')
        
        assert len(result) == 10
        assert result[0].value == 100.0
        # Should use default color logic based on positive/negative values

    def test_df_to_histogram_data_with_custom_colors(self):
        """Test df_to_histogram_data with custom colors."""
        result = df_to_histogram_data(
            self.histogram_df,
            value_column='volume',
            color_column='color',
            time_column='datetime',
            positive_color='#00ff00',
            negative_color='#ff0000'
        )
        
        assert len(result) == 10
        assert result[0].color == 'green'  # Uses color column, not custom colors

    def test_df_to_baseline_data_with_time_column(self):
        """Test df_to_baseline_data with time column."""
        result = df_to_baseline_data(
            self.baseline_df,
            value_column='value',
            time_column='datetime'
        )
        
        assert len(result) == 10
        assert result[0].value == 100.0

    def test_df_to_baseline_data_with_index(self):
        """Test df_to_baseline_data with DataFrame index as time."""
        df = self.baseline_df.set_index('datetime')
        result = df_to_baseline_data(df, value_column='value')
        
        assert len(result) == 10
        assert result[0].value == 100.0

    def test_df_to_baseline_data_with_custom_value_column(self):
        """Test df_to_baseline_data with custom value column."""
        df = pd.DataFrame({
            'time': self.dates[:5],
            'price': [100, 101, 102, 103, 104]
        })
        result = df_to_baseline_data(df, value_column='price', time_column='time')
        
        assert len(result) == 5
        assert result[0].value == 100.0

    def test_resample_df_for_charts_basic(self):
        """Test resample_df_for_charts with basic functionality."""
        # Create high-frequency data
        high_freq_dates = pd.date_range('2024-01-01', periods=100, freq='h')
        high_freq_df = pd.DataFrame({
            'open': np.random.randn(100).cumsum() + 100,
            'high': np.random.randn(100).cumsum() + 105,
            'low': np.random.randn(100).cumsum() + 95,
            'close': np.random.randn(100).cumsum() + 102,
            'volume': np.random.randint(1000, 10000, 100)
        }, index=high_freq_dates)
        
        # Resample to daily
        result = resample_df_for_charts(high_freq_df, freq='D')
        
        assert len(result) < len(high_freq_df)  # Should have fewer rows
        assert isinstance(result.index, pd.DatetimeIndex)

    def test_resample_df_for_charts_with_custom_agg(self):
        """Test resample_df_for_charts with custom aggregation."""
        high_freq_dates = pd.date_range('2024-01-01', periods=100, freq='h')
        high_freq_df = pd.DataFrame({
            'open': np.random.randn(100).cumsum() + 100,
            'high': np.random.randn(100).cumsum() + 105,
            'low': np.random.randn(100).cumsum() + 95,
            'close': np.random.randn(100).cumsum() + 102,
            'volume': np.random.randint(1000, 10000, 100)
        }, index=high_freq_dates)
        
        agg_dict = {
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last',
            'volume': 'sum'
        }
        
        result = resample_df_for_charts(high_freq_df, freq='D', agg_dict=agg_dict)
        
        assert len(result) < len(high_freq_df)
        assert all(col in result.columns for col in ['open', 'high', 'low', 'close', 'volume'])

    def test_df_to_data_line_chart(self):
        """Test df_to_data for line chart."""
        result = df_to_data(self.single_value_df, 'line', time_column='datetime')
        
        assert len(result) == 10
        assert hasattr(result[0], 'value')
        assert result[0].value == 100.0

    def test_df_to_data_area_chart(self):
        """Test df_to_data for area chart."""
        result = df_to_data(self.single_value_df, 'area', time_column='datetime')
        
        assert len(result) == 10
        assert hasattr(result[0], 'value')
        assert result[0].value == 100.0

    def test_df_to_data_candlestick_chart(self):
        """Test df_to_data for candlestick chart."""
        result = df_to_data(self.ohlc_df, 'candlestick', time_column='datetime')
        
        assert len(result) == 10
        assert hasattr(result[0], 'open')
        assert result[0].open == 100.0

    def test_df_to_data_histogram_chart(self):
        """Test df_to_data for histogram chart."""
        result = df_to_data(self.histogram_df, 'histogram', time_column='datetime', value_column='volume')
        
        assert len(result) == 10
        assert hasattr(result[0], 'value')
        assert result[0].value == 100.0

    def test_df_to_data_baseline_chart(self):
        """Test df_to_data for baseline chart."""
        result = df_to_data(self.baseline_df, 'baseline', time_column='datetime')
        
        assert len(result) == 10
        assert hasattr(result[0], 'value')
        assert result[0].value == 100.0

    def test_df_to_data_invalid_chart_type(self):
        """Test df_to_data with invalid chart type."""
        with pytest.raises(ValueError):
            df_to_data(self.single_value_df, 'invalid_chart_type')

    def test_dataframe_conversion_with_nan_values(self):
        """Test conversion with NaN values."""
        df_with_nan = self.single_value_df.copy()
        df_with_nan.loc[2, 'close'] = np.nan
        
        # The function doesn't handle NaN values gracefully, so we expect an error
        with pytest.raises((TypeError, ValueError)):
            df_to_line_data(df_with_nan, value_column='close', time_column='datetime')

    def test_dataframe_conversion_with_invalid_dtypes(self):
        """Test conversion with invalid data types."""
        df_invalid = self.single_value_df.copy()
        df_invalid['close'] = df_invalid['close'].astype(str)
        
        # Should handle string conversion to float
        result = df_to_line_data(df_invalid, value_column='close', time_column='datetime')
        assert len(result) == 10
        assert result[0].value == 100.0

    def test_dataframe_conversion_with_timezone(self):
        """Test conversion with timezone-aware datetime."""
        tz_dates = pd.date_range('2024-01-01', periods=5, freq='D', tz='UTC')
        tz_df = pd.DataFrame({
            'datetime': tz_dates,
            'close': [100, 101, 102, 103, 104]
        })
        
        result = df_to_line_data(tz_df, value_column='close', time_column='datetime')
        assert len(result) == 5
        assert result[0].time == tz_dates[0]

    def test_dataframe_conversion_performance(self):
        """Test conversion performance with large dataset."""
        large_dates = pd.date_range('2024-01-01', periods=10000, freq='h')
        large_df = pd.DataFrame({
            'datetime': large_dates,
            'close': np.random.randn(10000).cumsum() + 100
        })
        
        import time
        start_time = time.time()
        result = df_to_line_data(large_df, value_column='close', time_column='datetime')
        end_time = time.time()
        
        assert len(result) == 10000
        assert end_time - start_time < 5.0  # Should complete within 5 seconds

    def test_dataframe_conversion_edge_cases(self):
        """Test conversion with edge cases."""
        # Single row dataframe
        single_row = self.single_value_df.iloc[:1]
        result = df_to_line_data(single_row, value_column='close', time_column='datetime')
        assert len(result) == 1
        
        # Empty dataframe
        empty_df = pd.DataFrame(columns=['datetime', 'close'])
        result = df_to_line_data(empty_df, value_column='close', time_column='datetime')
        assert len(result) == 0

    def test_ohlc_conversion_with_missing_columns(self):
        """Test OHLC conversion with missing columns."""
        incomplete_df = self.ohlc_df.drop(columns=['high', 'low'])
        
        with pytest.raises(KeyError):
            df_to_ohlc_data(incomplete_df, time_column='datetime')

    def test_ohlcv_conversion_with_missing_volume(self):
        """Test OHLCV conversion with missing volume column."""
        no_volume_df = self.ohlc_df.drop(columns=['volume'])
        
        with pytest.raises(KeyError):
            df_to_ohlcv_data(no_volume_df, time_column='datetime')

    def test_histogram_conversion_with_positive_negative_values(self):
        """Test histogram conversion with positive/negative values."""
        pos_neg_df = pd.DataFrame({
            'datetime': self.dates[:5],
            'volume': [100, -50, 200, -75, 150]
        })
        
        result = df_to_histogram_data(pos_neg_df, value_column='volume', time_column='datetime')
        assert len(result) == 5
        # Should use default color logic for positive/negative values

    def test_resample_with_different_frequencies(self):
        """Test resampling with different frequencies."""
        high_freq_dates = pd.date_range('2024-01-01', periods=100, freq='h')
        high_freq_df = pd.DataFrame({
            'open': np.random.randn(100).cumsum() + 100,
            'high': np.random.randn(100).cumsum() + 105,
            'low': np.random.randn(100).cumsum() + 95,
            'close': np.random.randn(100).cumsum() + 102,
            'volume': np.random.randint(1000, 10000, 100)
        }, index=high_freq_dates)
        
        # Test different frequencies
        frequencies = ['D', 'W', 'ME']
        for freq in frequencies:
            result = resample_df_for_charts(high_freq_df, freq=freq)
            assert len(result) < len(high_freq_df)
            assert isinstance(result.index, pd.DatetimeIndex) 