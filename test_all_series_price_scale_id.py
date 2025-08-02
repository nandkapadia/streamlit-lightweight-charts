#!/usr/bin/env python3
"""
Comprehensive test script to verify that all series types work correctly with the priceScaleId fix.
"""

import pandas as pd
from streamlit_lightweight_charts_pro.charts.series import (
    BandSeries, AreaSeries, LineSeries, BarSeries, CandlestickSeries, HistogramSeries, BaselineSeries
)
from streamlit_lightweight_charts_pro.data import (
    BandData, AreaData, LineData, BarData, CandlestickData, HistogramData, BaselineData
)

def test_series_price_scale_id(series_class, data_class, test_data, series_name):
    """Test that a series type correctly handles priceScaleId."""
    print(f"\n=== Testing {series_name} ===")
    
    # Create series
    series = series_class(data=test_data)
    
    # Test configuration with priceScaleId
    config = {
        "seriesType": series_name.lower(),
        "priceScaleId": "right",
        "lastValueVisible": False,
        "priceLineVisible": False,
    }
    
    print(f"Before update - Price scale ID: {series.price_scale_id}")
    
    # Apply configuration
    series.update(config)
    
    print(f"After update - Price scale ID: {series.price_scale_id}")
    
    # Check the asdict output
    result = series.asdict()
    
    # Verify that priceScaleId is at the top level
    if "priceScaleId" in result:
        print(f"✅ {series_name}: priceScaleId found at top level: {result['priceScaleId']}")
        return True
    else:
        print(f"❌ {series_name}: priceScaleId not found at top level")
        if "options" in result and "priceScaleId" in result["options"]:
            print(f"⚠️  {series_name}: priceScaleId found in options: {result['options']['priceScaleId']}")
        else:
            print(f"❌ {series_name}: priceScaleId not found anywhere")
        return False

# Test data for different series types
band_data = [
    BandData("2024-01-01", upper=110, middle=105, lower=100),
    BandData("2024-01-02", upper=112, middle=107, lower=102),
]

area_data = [
    AreaData("2024-01-01", value=100),
    AreaData("2024-01-02", value=102),
]

line_data = [
    LineData("2024-01-01", value=100),
    LineData("2024-01-02", value=102),
]

bar_data = [
    BarData("2024-01-01", open=100, high=105, low=98, close=102),
    BarData("2024-01-02", open=102, high=108, low=100, close=106),
]

candlestick_data = [
    CandlestickData("2024-01-01", open=100, high=105, low=98, close=102),
    CandlestickData("2024-01-02", open=102, high=108, low=100, close=106),
]

histogram_data = [
    HistogramData("2024-01-01", value=100),
    HistogramData("2024-01-02", value=102),
]

baseline_data = [
    BaselineData("2024-01-01", value=100),
    BaselineData("2024-01-02", value=102),
]

# Test all series types
test_results = []

test_results.append(test_series_price_scale_id(BandSeries, BandData, band_data, "Band"))
test_results.append(test_series_price_scale_id(AreaSeries, AreaData, area_data, "Area"))
test_results.append(test_series_price_scale_id(LineSeries, LineData, line_data, "Line"))
test_results.append(test_series_price_scale_id(BarSeries, BarData, bar_data, "Bar"))
test_results.append(test_series_price_scale_id(CandlestickSeries, CandlestickData, candlestick_data, "Candlestick"))
test_results.append(test_series_price_scale_id(HistogramSeries, HistogramData, histogram_data, "Histogram"))
test_results.append(test_series_price_scale_id(BaselineSeries, BaselineData, baseline_data, "Baseline"))

# Summary
print(f"\n=== SUMMARY ===")
passed = sum(test_results)
total = len(test_results)
print(f"Passed: {passed}/{total} series types")

if passed == total:
    print("✅ All series types correctly handle priceScaleId!")
else:
    print("❌ Some series types have issues with priceScaleId") 