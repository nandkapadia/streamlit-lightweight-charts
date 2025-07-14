# Enhanced Streamlit Lightweight Charts

A significantly enhanced version of streamlit-lightweight-charts that brings the full power of TradingView's lightweight-charts library to Streamlit applications.

## 🚀 New Features

### 1. **Full Multi-Pane Support**
- Create multiple chart panes stacked vertically
- Each pane can have its own configuration and series
- Shared time axis across all panes

### 2. **Advanced Synchronization**
- **Time Range Sync**: Scroll and zoom are synchronized across all charts
- **Crosshair Sync**: Crosshair position is synchronized in real-time
- **Configurable**: Enable/disable sync features as needed

### 3. **Complete API Coverage**
- Support for all series types: Line, Area, Histogram, Bar, Candlestick, Baseline
- Full access to all chart options and series options
- Price scale configuration per series
- Custom markers and price lines

### 4. **Interactive Features**
- Click event callbacks
- Crosshair move callbacks
- Visible time range change callbacks
- Dynamic chart updates without re-rendering

### 5. **Trade Drawing**
- Add buy/sell markers with customizable shapes and colors
- Draw trade rectangles showing entry/exit periods
- Support for both individual markers and complete trades
- Trade click events and callbacks
- Automatic color coding for buy/sell trades

### 6. **Enhanced Styling**
- Multiple built-in themes (Light, Dark, Trading View)
- Watermarks and custom backgrounds
- Grid and axis customization
- Price line styling with multiple line styles
- Range switcher for quick time range selection

## 📦 Installation

```bash
pip install streamlit-lightweight-charts
```

## 🎯 Quick Start

### Basic Example

```python
import streamlit as st
from streamlit_lightweight_charts import Chart, ChartGroup, SeriesType

# Create a chart group
chart_group = ChartGroup()

# Create main price chart
price_chart = Chart(height=400)
price_chart.add_series(
    SeriesType.CANDLESTICK,
    data=[
        {'time': '2023-01-01', 'open': 100, 'high': 105, 'low': 98, 'close': 102},
        {'time': '2023-01-02', 'open': 102, 'high': 107, 'low': 101, 'close': 105},
        # ... more data
    ]
)

# Create volume chart
volume_chart = Chart(height=100)
volume_chart.add_series(
    SeriesType.HISTOGRAM,
    data=[
        {'time': '2023-01-01', 'value': 1000000},
        {'time': '2023-01-02', 'value': 1500000},
        # ... more data
    ]
)

# Add charts to group and render
chart_group.add_chart(price_chart)
chart_group.add_chart(volume_chart)
chart_group.render(key="my_charts")
```

### Advanced Example with Synchronization

```python
from streamlit_lightweight_charts import Chart, ChartGroup, SeriesType, LineStyle

# Create synchronized chart group
chart_group = ChartGroup(
    sync_enabled=True,
    sync_crosshair=True,
    sync_time_range=True
)

# Main chart with multiple indicators
main_chart = Chart(
    height=400,
    layout={'background': {'type': 'solid', 'color': '#1e222d'}},
    grid={'vertLines': {'color': 'rgba(42, 46, 57, 0)'}},
    crosshair={'mode': 0}
)

# Add candlestick series
main_chart.add_series(
    SeriesType.CANDLESTICK,
    data=candlestick_data,
    name="BTC/USD"
)

# Add SMA overlay
main_chart.add_series(
    SeriesType.LINE,
    data=sma_data,
    name="SMA 20",
    options={'color': '#2962FF', 'lineWidth': 2}
)

# Add price line
main_chart.add_price_line(
    price=45000,
    color='#4CAF50',
    line_style=LineStyle.DASHED,
    title='Support'
)

# Add range switcher
main_chart.add_range_switcher(
    position="top-right",
    default_range="1M"
)

# Add RSI indicator pane
rsi_chart = Chart(height=150)
rsi_chart.add_series(
    SeriesType.LINE,
    data=rsi_data,
    name="RSI",
    options={'color': '#9C27B0'}
)

# Add to group
chart_group.add_chart(main_chart)
chart_group.add_chart(rsi_chart)

# Add event callbacks
def on_click(event_data):
    st.write(f"Clicked at {event_data['time']}")

chart_group.on_click(on_click)

# Render
chart_group.render(key="advanced_chart")
```

## 📊 Series Types

All TradingView lightweight-charts series types are supported:

- **Line**: `SeriesType.LINE`
- **Area**: `SeriesType.AREA`
- **Histogram**: `SeriesType.HISTOGRAM`
- **Bar**: `SeriesType.BAR`
- **Candlestick**: `SeriesType.CANDLESTICK`
- **Baseline**: `SeriesType.BASELINE`

## 🎯 Trade Drawing

### Adding Complete Trades

```python
from streamlit_lightweight_charts import Chart, TradeType, MarkerShape

# Add a complete trade with markers and rectangle
chart.add_trade(
    trade_type=TradeType.BUY,
    entry_time="2024-01-15",
    entry_price=95.50,
    exit_time="2024-01-25",
    exit_price=102.30,
    quantity=100,
    symbol="AAPL",
    show_markers=True,
    show_rectangle=True,
    marker_color="#26a69a",
    rectangle_color="rgba(38, 166, 154, 0.2)"
)
```

### Adding Individual Markers

```python
# Add buy marker
chart.add_trade_marker(
    time="2024-01-10",
    price=94.50,
    trade_type=TradeType.BUY,
    shape=MarkerShape.CIRCLE,
    text="BUY SIGNAL",
    color="#4CAF50",
    size=2
)

# Add sell marker
chart.add_trade_marker(
    time="2024-01-20",
    price=105.80,
    trade_type=TradeType.SELL,
    shape=MarkerShape.TRIANGLE_DOWN,
    text="SELL SIGNAL",
    color="#FF5722"
)
```

### Trade Types and Shapes

```python
# Trade Types
TradeType.BUY      # Buy trade
TradeType.SELL     # Sell trade
TradeType.LONG     # Long position
TradeType.SHORT    # Short position

# Marker Shapes
MarkerShape.ARROW_UP        # Up arrow
MarkerShape.ARROW_DOWN      # Down arrow
MarkerShape.CIRCLE          # Circle
MarkerShape.SQUARE          # Square
MarkerShape.TRIANGLE_UP     # Up triangle
MarkerShape.TRIANGLE_DOWN   # Down triangle
MarkerShape.FLAG            # Flag
```

### Trade Click Events

```python
def on_trade_click(event_data):
    trade = event_data['trade']
    st.write(f"Trade clicked: {trade['type']} {trade['quantity']} @ {trade['entry_price']}")

chart_group.on_trade_click(on_trade_click)
```

### Quick Trade Chart Creation

```python
from streamlit_lightweight_charts import create_trade_chart

# Create chart with trades
chart = create_trade_chart(
    chart_data=ohlcv_data,
    trades=trades_list,
    height=400,
    show_trade_markers=True,
    show_trade_rectangles=True
)
```

## 🎨 Themes and Styling

### Built-in Themes

```python
# Light theme
chart = Chart(
    layout={'background': {'type': 'solid', 'color': 'white'}, 'textColor': 'black'},
    grid={'vertLines': {'color': 'rgba(197, 203, 206, 0.5)'}}
)

# Dark theme
chart = Chart(
    layout={'background': {'type': 'solid', 'color': '#131722'}, 'textColor': '#d1d4dc'},
    grid={'vertLines': {'color': 'rgba(42, 46, 57, 0.6)'}}
)

# Trading View theme
chart = Chart(
    layout={'background': {'type': 'solid', 'color': '#1e222d'}, 'textColor': '#9598a1'},
    grid={'vertLines': {'color': 'rgba(42, 46, 57, 0)'}}
)
```

### Watermarks

```python
chart = Chart(
    watermark={
        'visible': True,
        'fontSize': 48,
        'horzAlign': 'center',
        'vertAlign': 'center',
        'color': 'rgba(171, 71, 188, 0.3)',
        'text': 'CONFIDENTIAL'
    }
)
```

## 🔄 Dynamic Updates

The enhanced library supports dynamic updates through Streamlit's session state:

```python
# Initial render
if 'chart_data' not in st.session_state:
    st.session_state.chart_data = initial_data

chart = Chart()
chart.add_series(SeriesType.LINE, st.session_state.chart_data)
chart.render(key="dynamic_chart")

# Update data
if st.button("Update Data"):
    st.session_state.chart_data = new_data
    st.rerun()
```

## 🎯 Event Callbacks

Handle user interactions with event callbacks:

```python
chart_group = ChartGroup()

# Click events
def handle_click(event):
    chart_id = event['chartId']
    time = event['time']
    price = event['seriesPrices']
    st.write(f"Clicked on {chart_id} at {time}")

# Crosshair move events
def handle_crosshair(event):
    st.session_state.crosshair_pos = event

# Time range changes
def handle_range_change(event):
    st.write(f"Visible range: {event['timeRange']}")

# Range switcher changes
def handle_range_switcher(event):
    st.write(f"Range changed to: {event['range']['label']}")

chart_group.on_click(handle_click)
chart_group.on_crosshair_move(handle_crosshair)
chart_group.on_visible_time_range_change(handle_range_change)
chart_group.on_range_switcher_change(handle_range_switcher)
```

## 📈 Price Scales

Configure multiple price scales:

```python
# Right price scale (default)
chart.add_series(
    SeriesType.LINE,
    data=price_data,
    price_scale_id="right"
)

# Left price scale
chart.add_series(
    SeriesType.LINE,
    data=volume_data,
    price_scale_id="left",
    price_scale={'scaleMargins': {'top': 0.8, 'bottom': 0}}
)

# Overlay scale
chart.add_series(
    SeriesType.HISTOGRAM,
    data=volume_data,
    price_scale_id="",
    price_scale={'scaleMargins': {'top': 0.7, 'bottom': 0}}
)
```

## ⏰ Range Switcher

Add quick time range selection buttons:

```python
# Default ranges (1D, 1W, 1M, 3M, 6M, 1Y, ALL)
chart.add_range_switcher(
    position="top-right",
    default_range="1M"
)

# Custom ranges
custom_ranges = [
    {"label": "1H", "seconds": 3600},
    {"label": "4H", "seconds": 14400},
    {"label": "1D", "seconds": 86400},
    {"label": "1W", "seconds": 604800}
]

chart.add_range_switcher(
    ranges=custom_ranges,
    position="bottom-left",
    default_range="1D"
)

# Handle range changes
def on_range_change(event):
    print(f"Range changed to: {event['range']['label']}")

chart_group.on_range_switcher_change(on_range_change)
```

## 🏗️ Architecture

The enhanced library consists of:

1. **Python API** (`streamlit_lightweight_charts/__init__.py`):
   - `Chart` class for individual chart configuration
   - `ChartGroup` class for managing multiple synchronized charts
   - Comprehensive type hints and enums
   - Backward compatibility with the original API

2. **TypeScript Frontend** (`frontend/src/LightweightCharts.tsx`):
   - `ChartManager` class for managing chart instances
   - Full synchronization implementation
   - Event handling and callbacks
   - Dynamic updates support

3. **Enhanced Features**:
   - Bi-directional communication between Python and JavaScript
   - Efficient chart synchronization without performance degradation
   - Support for all lightweight-charts features

## 🔧 Development

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/streamlit-lightweight-charts
cd streamlit-lightweight-charts

# Install dependencies
pip install -e .
cd streamlit_lightweight_charts/frontend
npm install
```

### Development Mode

```bash
# Terminal 1: Run the frontend dev server
cd streamlit_lightweight_charts/frontend
npm start

# Terminal 2: Run Streamlit with the example
streamlit run examples/AdvancedMultiPaneSync.py
```

### Building

```bash
cd streamlit_lightweight_charts/frontend
npm run build
```

## 📝 Migration Guide

If you're upgrading from the original streamlit-lightweight-charts:

1. **Backward Compatibility**: The original `renderLightweightCharts()` function still works
2. **New API**: For new features, use the `Chart` and `ChartGroup` classes
3. **Data Format**: The data format remains the same
4. **Options**: All original options are supported, plus many new ones

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built on top of [TradingView's lightweight-charts](https://github.com/tradingview/lightweight-charts)
- Inspired by [lightweight-charts-python](https://github.com/louisnw01/lightweight-charts-python)
- Original [streamlit-lightweight-charts](https://github.com/freyastreamlit/streamlit-lightweight-charts)