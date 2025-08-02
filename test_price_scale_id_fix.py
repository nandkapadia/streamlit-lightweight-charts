#!/usr/bin/env python3
"""
Test script to verify that the priceScaleId fix works correctly.
"""

import pandas as pd
from streamlit_lightweight_charts_pro.charts.series import BandSeries
from streamlit_lightweight_charts_pro.data import BandData

# Create test data
data = [
    BandData("2024-01-01", upper=110, middle=105, lower=100),
    BandData("2024-01-02", upper=112, middle=107, lower=102),
]

# Create band series
series = BandSeries(data=data)

# Test configuration with priceScaleId
config = {
    "seriesType": "band",
    "propertyName": ["upper", "middle", "lower"],
    "columnMapping": {
        "time": "datetime",
        "upper": "upper",
        "lower": "lower",
        "middle": "middle",
    },
    "paneId": 0,
    "priceScaleId": "right",  # This should be at top level
    "lastValueVisible": False,
    "priceLineVisible": False,
    # Line styling using new LineOptions format
    "upperLine": {
        "color": "#4CAF50",  # Green for upper band
        "lineWidth": 1,
        "lineStyle": "solid",
        "lineVisible": True,
    },
    "middleLine": {
        "color": "#2196F3",  # Blue for middle band
        "lineWidth": 1,
        "lineStyle": "dotted",
        "lineVisible": True,
    },
    "lowerLine": {
        "color": "#F44336",  # Red for lower band
        "lineWidth": 1,
        "lineStyle": "solid",
        "lineVisible": True,
    },
    # Fill colors
    "upperFillColor": "rgba(76, 175, 80, 0.1)",  # Light green fill
    "lowerFillColor": "rgba(244, 67, 54, 0.1)",  # Light red fill
}

print("Before update:")
print(f"Price scale ID: {series.price_scale_id}")

# Apply configuration
series.update(config)

print("\nAfter update:")
print(f"Price scale ID: {series.price_scale_id}")

# Check the asdict output
result = series.asdict()
print("\nAsdict result:")
import json
print(json.dumps(result, indent=2))

# Verify that priceScaleId is at the top level
if "priceScaleId" in result:
    print(f"\n✅ priceScaleId found at top level: {result['priceScaleId']}")
else:
    print("\n❌ priceScaleId not found at top level")
    if "options" in result and "priceScaleId" in result["options"]:
        print(f"⚠️  priceScaleId found in options: {result['options']['priceScaleId']}")
    else:
        print("❌ priceScaleId not found anywhere") 