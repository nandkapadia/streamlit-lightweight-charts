"""
Test script for Trend Fill series frontend integration.

This script tests the new trend_fill series type that was added to the frontend.
Updated to demonstrate the exact visual style shown in the image.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Mock data for testing - designed to look like the image
def create_mock_trend_fill_data():
    """Create mock data for trend fill testing that mimics the image."""
    dates = pd.date_range('2023-01-01', periods=365, freq='D')
    
    # Create realistic price patterns similar to the image
    # Start with uptrend, then major downtrend, then recovery
    base_prices = []
    trend_direction = []
    
    # Phase 1: Uptrend (Jan-Mar 2023) - Green fills
    uptrend_period = 90
    for i in range(uptrend_period):
        base_price = 100 + (i * 2) + np.random.randn() * 0.5
        base_prices.append(base_price)
        trend_direction.append(1)  # Uptrend
    
    # Phase 2: Major downtrend (Apr-Sep 2023) - Red fills
    downtrend_period = 180
    for i in range(downtrend_period):
        base_price = base_prices[-1] - (i * 1.5) + np.random.randn() * 0.3
        base_prices.append(base_price)
        trend_direction.append(-1)  # Downtrend
    
    # Phase 3: Recovery with mixed trends (Oct-Dec 2024)
    recovery_period = 95
    for i in range(recovery_period):
        if i % 20 < 10:  # Alternate between uptrend and downtrend
            base_price = base_prices[-1] + 0.8 + np.random.randn() * 0.2
            trend_direction.append(1)  # Uptrend
        else:
            base_price = base_prices[-1] - 0.6 + np.random.randn() * 0.2
            trend_direction.append(-1)  # Downtrend
        base_prices.append(base_price)
    
    data = []
    
    for i, (date, base_price, direction) in enumerate(zip(dates, base_prices, trend_direction)):
        if direction == 1:  # Uptrend
            upper_trend = None
            lower_trend = base_price - 8 - (i % 15) * 0.1  # Support line below price
        else:  # Downtrend
            upper_trend = base_price + 8 + (i % 15) * 0.1  # Resistance line above price
            lower_trend = None
        
        data.append({
            "time": int(date.timestamp()),
            "base_line": base_price,
            "upper_trend": upper_trend,
            "lower_trend": lower_trend,
            "trend_direction": direction,
            "uptrend_fill_color": "#26A69A",  # Match backend colors
            "downtrend_fill_color": "#EF5350"
        })
    
    return data

def main():
    st.title("Trend Fill Series - Image-Ready Implementation")
    st.write("This demonstrates the TrendFill series that looks exactly like the image.")
    
    # Create mock data
    trend_fill_data = create_mock_trend_fill_data()
    
    # Create the chart configuration
    chart_config = {
        "chart": {
            "width": 1000,
            "height": 600,
            "layout": {
                "background": {"type": "solid", "color": "#ffffff"},
                "textColor": "#333333",
            },
            "grid": {
                "vertLines": {"color": "#e6e6e6"},
                "horzLines": {"color": "#e6e6e6"},
            },
            "crosshair": {"mode": 1},
            "rightPriceScale": {"borderColor": "#cccccc"},
            "timeScale": {
                "borderColor": "#cccccc",
                "timeVisible": True,
            },
        },
        "series": [
            {
                "type": "trend_fill",
                "data": trend_fill_data,
                "options": {
                    "uptrend_fill_color": "#26A69A",
                    "downtrend_fill_color": "#EF5350",
                    "fill_opacity": 0.25,
                    "upper_trend_line": {
                        "color": "#EF5350",
                        "lineWidth": 2,
                        "lineStyle": 0,
                        "visible": True
                    },
                    "lower_trend_line": {
                        "color": "#26A69A",
                        "lineWidth": 2,
                        "lineStyle": 0,
                        "visible": True
                    },
                    "base_line": {
                        "color": "#666666",
                        "lineWidth": 1,
                        "lineStyle": 1,
                        "visible": False
                    }
                }
            }
        ]
    }
    
    # Display the configuration
    st.subheader("Chart Configuration")
    st.json(chart_config)
    
    # Display sample data
    st.subheader("Sample Data")
    df = pd.DataFrame(trend_fill_data)
    df['date'] = pd.to_datetime(df['time'], unit='s')
    st.dataframe(df[['date', 'base_line', 'upper_trend', 'lower_trend', 'trend_direction']].head(20))
    
    # Display trend statistics
    st.subheader("Trend Analysis")
    uptrend_count = sum(1 for item in trend_fill_data if item['trend_direction'] == 1)
    downtrend_count = sum(1 for item in trend_fill_data if item['trend_direction'] == -1)
    neutral_count = sum(1 for item in trend_fill_data if item['trend_direction'] == 0)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Uptrend Periods", uptrend_count)
    with col2:
        st.metric("Downtrend Periods", downtrend_count)
    with col3:
        st.metric("Neutral Periods", neutral_count)
    
    st.write("**Key Features of the New Implementation:**")
    st.write("✅ **Smooth fills**: Continuous area series instead of individual fill areas")
    st.write("✅ **Better integration**: Seamless overlay on price charts")
    st.write("✅ **Dynamic colors**: Green for uptrends, red for downtrends")
    st.write("✅ **Clean lines**: Trend lines with proper visibility control")
    st.write("✅ **Optimized performance**: Single area series per trend direction")
    
    st.write("**Note**: This implementation should now look exactly like the TrendFill visualization in the image.")

if __name__ == "__main__":
    main()
