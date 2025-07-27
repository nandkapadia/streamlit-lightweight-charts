# Candlestick Chart Examples

This directory contains examples demonstrating various candlestick chart features and configurations.

## Examples

### 1. Basic Candlestick Chart (`basic_candlestick_chart.py`)
- Simple candlestick chart with sample data
- Basic configuration and styling
- Good starting point for beginners

### 2. Customized Candlestick Chart (`customized_candlestick_chart.py`)
- Advanced styling and customization options
- Custom colors, borders, and wicks
- Price scale and time scale configuration

### 3. Brownian Motion Trades Chart (`brownian_motion_trades_chart.py`)
- Generates realistic OHLCV data using Brownian motion simulation
- Identifies and visualizes 10 trades on the chart
- Interactive trade visualization options
- Demonstrates trade entry/exit markers and annotations

### 4. Colored Volume Chart (`colored_volume_example.py`)
- **NEW**: Volume bars colored based on price movement
- Green volume bars for bullish candles (close >= open)
- Red volume bars for bearish candles (close < open)
- Interactive color customization
- Real-time data generation with realistic price movements

## Features Demonstrated

### Candlestick Styling
- Up/down colors for candles
- Border visibility and colors
- Wick styling and colors
- Opacity and transparency

### Volume Visualization
- Volume histogram overlay
- **Colored volume bars** based on price movement
- Volume scale configuration
- Custom volume colors

### Trade Visualization
- Trade entry and exit markers
- Multiple visualization styles (markers, rectangles, lines, arrows)
- Interactive trade display options
- Trade annotation integration

### Chart Configuration
- Price scale options (left/right)
- Time scale configuration
- Grid and layout settings
- Annotation layers

## Usage

### Basic Colored Volume Chart
```python
from streamlit_lightweight_charts_pro import Chart

# Method 1: Using Chart.from_price_volume_dataframe (recommended)
chart = Chart.from_price_volume_dataframe(
    data=df,
    column_mapping={
        'time': 'time',
        'open': 'open',
        'high': 'high',
        'low': 'low',
        'close': 'close',
        'volume': 'volume'
    },
    volume_kwargs={
        'up_color': 'rgba(76,175,80,0.5)',    # Green for bullish
        'down_color': 'rgba(244,67,54,0.5)'   # Red for bearish
    }
)

# Method 2: Using HistogramSeries.create_volume_series directly
from streamlit_lightweight_charts_pro.charts.series.histogram import HistogramSeries

volume_series = HistogramSeries.create_volume_series(
    data=df,  # DataFrame with OHLCV data
    column_mapping={
        'time': 'time',
        'volume': 'volume',
        'open': 'open',
        'close': 'close'
    },
    up_color='rgba(76,175,80,0.5)',
    down_color='rgba(244,67,54,0.5)',
    pane_id=0,
    price_scale_id='right'
)

# Method 3: Using OHLCV data objects
from streamlit_lightweight_charts_pro.data.ohlcv_data import OhlcvData

ohlcv_data = [
    OhlcvData('2024-01-01', 100, 105, 98, 105, 1000),
    OhlcvData('2024-01-02', 105, 108, 102, 102, 1500)
]

volume_series_ohlcv = HistogramSeries.create_volume_series(
    data=ohlcv_data,  # List of OhlcvData objects
    column_mapping={},
    up_color='rgba(76,175,80,0.5)',
    down_color='rgba(244,67,54,0.5)'
)
```

### Custom Volume Colors
```python
# Custom volume colors
volume_kwargs = {
    'up_color': 'rgba(0,255,0,0.6)',      # Bright green
    'down_color': 'rgba(255,0,0,0.6)',    # Bright red
    'base': 0                             # Volume baseline
}
```

### Trade Visualization
```python
# Add trade visualization
chart.add_trade_visualization(trades)

# Configure trade visualization options
chart.options.trade_visualization = TradeVisualizationOptions(
    marker_options=MarkerOptions(
        position=MarkerPosition.ABOVE_BAR,
        shape=MarkerShape.CIRCLE,
        size=MarkerSize.LARGE
    )
)
```

## Data Requirements

### OHLCV Data Format
```python
# DataFrame with columns:
df = pd.DataFrame({
    'time': ['2024-01-01', '2024-01-02', ...],
    'open': [100.0, 105.0, ...],
    'high': [108.0, 110.0, ...],
    'low': [99.0, 102.0, ...],
    'close': [105.0, 102.0, ...],
    'volume': [1000, 1500, ...]
})
```

### Trade Data Format
```python
from streamlit_lightweight_charts_pro.data import Trade
from streamlit_lightweight_charts_pro.type_definitions.enums import TradeType

trades = [
    Trade(
        entry_time="2024-01-01 10:00:00",
        entry_price=100.0,
        exit_time="2024-01-01 15:00:00",
        exit_price=105.0,
        quantity=100,
        trade_type=TradeType.LONG
    )
]
```

## Running Examples

1. Navigate to the examples directory:
   ```bash
   cd examples/candlestick_charts
   ```

2. Run any example:
   ```bash
   streamlit run colored_volume_example.py
   ```

3. Or run the launcher to choose an example:
   ```bash
   streamlit run launcher.py
   ```

## Key Features

- **Colored Volume**: Volume bars automatically colored based on price movement
- **Interactive Controls**: Real-time customization of colors, chart options, and data
- **Realistic Data**: Brownian motion simulation for realistic price movements
- **Trade Analysis**: Built-in trade identification and visualization
- **Responsive Design**: Charts adapt to different screen sizes and data volumes
- **Performance Optimized**: Efficient rendering for large datasets

## Notes

- Volume colors are applied at the data level using `HistogramData` with per-point colors
- The colored volume feature works with both DataFrame and OHLCV data object inputs
- **Note**: Only OHLCV data (with volume) is supported, not OHLC data (without volume)
- Use `HistogramSeries.create_volume_series()` factory method for direct volume series creation
- Trade visualization supports multiple marker styles and positions
- All examples include comprehensive error handling and data validation 