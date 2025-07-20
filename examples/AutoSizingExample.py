#!/usr/bin/env python3
"""
Auto-Sizing Charts Example

This example demonstrates the new auto-sizing functionality that allows charts
to automatically resize based on their container dimensions.
"""

from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import streamlit as st



# Page configuration
st.set_page_config(page_title="Auto-Sizing Charts Example", page_icon="📊", layout="wide")

st.title("📊 Auto-Sizing Charts Example")
st.markdown(
    """
This example demonstrates the new auto-sizing functionality. Try resizing your browser window 
to see the charts adapt to their container dimensions!
"""
)


# Generate sample data
def generate_sample_data(days=50, base_price=100):
    """Generate sample OHLCV data."""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    date_range = pd.date_range(start=start_date, end=end_date, freq="D")

    data = []
    current_price = base_price

    for date in date_range:
        # Generate realistic price movements
        change = np.random.normal(0, 0.02)
        current_price *= 1 + change

        # Generate OHLC from current price
        high = current_price * (1 + abs(np.random.normal(0, 0.01)))
        low = current_price * (1 - abs(np.random.normal(0, 0.01)))
        open_price = current_price * (1 + np.random.normal(0, 0.005))
        close_price = current_price

        # Ensure OHLC relationships
        high = max(high, open_price, close_price)
        low = min(low, open_price, close_price)

        data.append(
            {
                "time": date.strftime("%Y-%m-%d"),
                "open": round(open_price, 2),
                "high": round(high, 2),
                "low": round(low, 2),
                "close": round(close_price, 2),
            }
        )

        current_price = close_price

    return data


# Generate data
data = generate_sample_data(50, 100)

# Example 1: Full Auto-Size Chart
st.header("1️⃣ Full Auto-Size Chart")
st.markdown("This chart automatically sizes both width and height to fit its container.")

chart_options_1 = {
    "autoSize": True,
    "minWidth": 300,
    "maxWidth": 1200,
    "minHeight": 200,
    "maxHeight": 600,
    "layout": {
        "background": {"type": "solid", "color": "white"},
        "textColor": "black",
    },
    "grid": {
        "vertLines": {"color": "rgba(197, 203, 206, 0.5)"},
        "horzLines": {"color": "rgba(197, 203, 206, 0.5)"},
    },
    "crosshair": {
        "mode": 1,
    },
    "legend": {
        "visible": True,
        "type": "simple",
        "position": "top-left",
        "symbolName": "AAPL",
        "showLastValue": True,
    },
}

candlestick_series_1 = [
    {
        "type": "Candlestick",
        "data": data,
        "options": {
            "upColor": "#26a69a",
            "downColor": "#ef5350",
            "borderVisible": False,
            "wickUpColor": "#26a69a",
            "wickDownColor": "#ef5350",
        },
    }
]

chart_1 = [
    {
        "chart": chart_options_1,
        "series": candlestick_series_1,
    }
]

chart_1.render(key="auto_size_chart_1")

# Example 2: Responsive Columns
st.header("2️⃣ Responsive Column Layout")
st.markdown("Charts in different column widths automatically adapt their size.")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("**Wide Column (2/3 width):**")
    chart_options_2 = {
        "autoSize": True,
        "minWidth": 200,
        "maxWidth": 800,
        "minHeight": 200,
        "maxHeight": 400,
        "layout": {
            "background": {"type": "solid", "color": "#f8f9fa"},
            "textColor": "black",
        },
        "grid": {
            "vertLines": {"color": "rgba(197, 203, 206, 0.3)"},
            "horzLines": {"color": "rgba(197, 203, 206, 0.3)"},
        },
        "crosshair": {
            "mode": 1,
        },
        "legend": {
            "visible": True,
            "type": "3line",
            "position": "top-right",
            "symbolName": "AAPL",
            "showLastValue": True,
            "showTime": True,
        },
    }

    line_series_2 = [
        {
            "type": "Line",
            "data": [{"time": item["time"], "value": item["close"]} for item in data],
            "options": {
                "color": "#2962ff",
                "lineWidth": 2,
            },
        }
    ]

    chart_2 = [
        {
            "chart": chart_options_2,
            "series": line_series_2,
        }
    ]

    chart_2.render(key="auto_size_chart_2")

with col2:
    st.markdown("**Narrow Column (1/3 width):**")
    chart_options_3 = {
        "autoSize": True,
        "minWidth": 150,
        "maxWidth": 400,
        "minHeight": 200,
        "maxHeight": 400,
        "layout": {
            "background": {"type": "solid", "color": "#e3f2fd"},
            "textColor": "black",
        },
        "grid": {
            "vertLines": {"visible": False},
            "horzLines": {"color": "rgba(197, 203, 206, 0.2)"},
        },
        "crosshair": {
            "mode": 1,
        },
        "legend": {
            "visible": True,
            "type": "simple",
            "position": "bottom-left",
            "symbolName": "Price",
            "showLastValue": True,
        },
    }

    area_series_3 = [
        {
            "type": "Area",
            "data": [{"time": item["time"], "value": item["close"]} for item in data],
            "options": {
                "topColor": "rgba(76, 175, 80, 0.4)",
                "bottomColor": "rgba(76, 175, 80, 0.0)",
                "lineColor": "#4caf50",
                "lineWidth": 2,
            },
        }
    ]

    chart_3 = [
        {
            "chart": chart_options_3,
            "series": area_series_3,
        }
    ]

    chart_3.render(key="auto_size_chart_3")

# Example 3: Auto-Width vs Auto-Height
st.header("3️⃣ Auto-Width vs Auto-Height")
st.markdown("Compare different auto-sizing modes.")

col3, col4 = st.columns(2)

with col3:
    st.markdown("**Auto-Width Only (Fixed Height):**")
    chart_options_width = {
        "autoWidth": True,
        "height": 300,  # Fixed height
        "minWidth": 200,
        "maxWidth": 600,
        "layout": {
            "background": {"type": "solid", "color": "white"},
            "textColor": "black",
        },
        "grid": {
            "vertLines": {"color": "rgba(197, 203, 206, 0.5)"},
            "horzLines": {"color": "rgba(197, 203, 206, 0.5)"},
        },
        "crosshair": {
            "mode": 1,
        },
    }

    bar_series_width = [
        {
            "type": "Bar",
            "data": [{"time": item["time"], "value": item["close"]} for item in data],
            "options": {
                "upColor": "#26a69a",
                "downColor": "#ef5350",
            },
        }
    ]

    chart_width = [
        {
            "chart": chart_options_width,
            "series": bar_series_width,
        }
    ]

    chart_width.render(key="auto_width_chart")

with col4:
    st.markdown("**Auto-Height Only (Fixed Width):**")
    chart_options_height = {
        "autoHeight": True,
        "width": 400,  # Fixed width
        "minHeight": 200,
        "maxHeight": 500,
        "layout": {
            "background": {"type": "solid", "color": "white"},
            "textColor": "black",
        },
        "grid": {
            "vertLines": {"color": "rgba(197, 203, 206, 0.5)"},
            "horzLines": {"color": "rgba(197, 203, 206, 0.5)"},
        },
        "crosshair": {
            "mode": 1,
        },
    }

    line_series_height = [
        {
            "type": "Line",
            "data": [{"time": item["time"], "value": item["close"]} for item in data],
            "options": {
                "color": "#ff9800",
                "lineWidth": 3,
            },
        }
    ]

    chart_height = [
        {
            "chart": chart_options_height,
            "series": line_series_height,
        }
    ]

    chart_height.render(key="auto_height_chart")

# Usage Instructions
st.header("📖 How to Use Auto-Sizing")

st.markdown(
    """
### Basic Usage

```python
# Full auto-sizing
chart_options = {
    "autoSize": True,
    "minWidth": 300,
    "maxWidth": 1200,
    "minHeight": 200,
    "maxHeight": 800,
}

# Auto-width only
chart_options = {
    "autoWidth": True,
    "height": 400,  # Fixed height
    "minWidth": 300,
    "maxWidth": 1200,
}

# Auto-height only
chart_options = {
    "autoHeight": True,
    "width": 600,  # Fixed width
    "minHeight": 200,
    "maxHeight": 800,
}
```

### Features

✅ **Responsive Design**: Charts automatically resize when container changes  
✅ **Size Constraints**: Set minimum and maximum dimensions  
✅ **Flexible Options**: Auto-size width, height, or both  
✅ **Performance**: Uses ResizeObserver for efficient updates  
✅ **Streamlit Integration**: Works seamlessly with Streamlit's responsive layout  

### Try It Out

1. **Resize your browser window** to see the charts adapt
2. **Test different column layouts** to see responsive behavior
3. **Compare fixed vs auto-sizing** charts in the examples above
"""
)

# Data info
st.header("📊 Data Information")
col_info1, col_info2, col_info3 = st.columns(3)

with col_info1:
    st.metric("Data Points", len(data))
    st.metric("Date Range", f"{data[0]['time']} to {data[-1]['time']}")

with col_info2:
    latest_price = data[-1]["close"]
    prev_price = data[-2]["close"] if len(data) > 1 else latest_price
    change = latest_price - prev_price
    change_pct = (change / prev_price) * 100 if prev_price > 0 else 0
    st.metric("Latest Price", f"${latest_price:.2f}", f"{change:+.2f} ({change_pct:+.2f}%)")

with col_info3:
    st.metric("Auto-Size Mode", "Full Auto-Size")
    st.metric("Container Size", "Responsive")
