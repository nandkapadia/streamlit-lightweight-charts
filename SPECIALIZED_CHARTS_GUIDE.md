# Specialized Charts Guide

The streamlit-lightweight-charts library provides specialized chart classes that offer type safety, automatic data validation, and chart-specific methods. These classes make it easier to create specific chart types while ensuring data correctness.

## Available Specialized Charts

### 1. CandlestickChart

The most comprehensive chart type, now with built-in trade visualization support.

#### Basic Usage
```python
from streamlit_lightweight_charts import CandlestickChart, OhlcData

# Create OHLC data
data = [
    OhlcData(time=pd.Timestamp('2024-01-01'), open=100, high=105, low=98, close=102),
    OhlcData(time=pd.Timestamp('2024-01-02'), open=102, high=108, low=101, close=106),
    # ... more data
]

# Create chart
chart = CandlestickChart(
    data=data,
    options=ChartOptions(height=500)
)
chart.render(key='candlestick')
```

#### Trade Visualization

CandlestickChart now supports advanced trade visualization with multiple styles:

```python
from streamlit_lightweight_charts import Trade, TradeType, TradeVisualization, TradeVisualizationOptions

# Create trades
trades = [
    Trade(
        entry_time=pd.Timestamp('2024-01-01'),
        entry_price=100,
        exit_time=pd.Timestamp('2024-01-05'),
        exit_price=105,
        quantity=100,
        trade_type=TradeType.LONG,
        id="T001"
    )
]

# Visualization options
trade_options = TradeVisualizationOptions(
    style=TradeVisualization.BOTH,  # Shows both markers and rectangles
    show_pnl_in_markers=True,
    rectangle_fill_opacity=0.2
)

# Create chart with trades
chart = CandlestickChart(
    data=ohlc_data,
    trades=trades,
    trade_visualization_options=trade_options
)
```

##### Visualization Styles

1. **MARKERS** - Entry/exit points with arrows
   ```python
   TradeVisualizationOptions(style=TradeVisualization.MARKERS)
   ```

2. **RECTANGLES** - Boxes from entry to exit
   ```python
   TradeVisualizationOptions(
       style=TradeVisualization.RECTANGLES,
       rectangle_fill_opacity=0.2,
       rectangle_color_profit='#4CAF50',
       rectangle_color_loss='#F44336'
   )
   ```

3. **BOTH** - Combines markers and rectangles
   ```python
   TradeVisualizationOptions(style=TradeVisualization.BOTH)
   ```

4. **LINES** - Simple lines connecting entry/exit
   ```python
   TradeVisualizationOptions(
       style=TradeVisualization.LINES,
       line_style='dashed',
       line_width=2
   )
   ```

5. **ARROWS** - Directional arrows with P&L
   ```python
   TradeVisualizationOptions(
       style=TradeVisualization.ARROWS,
       arrow_size=10
   )
   ```

6. **ZONES** - Colored background zones
   ```python
   TradeVisualizationOptions(
       style=TradeVisualization.ZONES,
       zone_opacity=0.1,
       zone_extend_bars=2  # Extend zone by 2 bars
   )
   ```

#### Trade Management Methods

```python
# Add trades after creation
chart.add_trades([trade1, trade2])

# Add single trade
chart.add_trade(trade3)

# Clear all trades
chart.clear_trades()

# Update visualization style
chart.set_trade_visualization(
    TradeVisualizationOptions(style=TradeVisualization.RECTANGLES)
)

# Add technical indicator
chart.add_indicator(
    data=sma_data,
    options=LineSeriesOptions(color='#FF6B6B')
)
```

### 2. LineChart

For simple time series data visualization.

```python
from streamlit_lightweight_charts import LineChart, SingleValueData

# Create data
data = [
    SingleValueData(time=pd.Timestamp('2024-01-01'), value=100),
    SingleValueData(time=pd.Timestamp('2024-01-02'), value=102),
    # ... more data
]

# Create chart
chart = LineChart(
    data=data,
    options=ChartOptions(height=400),
    series_options=LineSeriesOptions(
        color='#2196F3',
        line_width=2
    )
)

# Add another line
chart.add_line(
    data=another_data,
    options=LineSeriesOptions(color='#FF9800')
)
```

### 3. AreaChart

Similar to LineChart but with filled area below.

```python
from streamlit_lightweight_charts import AreaChart

chart = AreaChart(
    data=data,
    series_options=AreaSeriesOptions(
        top_color='rgba(33, 150, 243, 0.56)',
        bottom_color='rgba(33, 150, 243, 0.04)',
        line_color='#2196F3'
    )
)
```

### 4. BarChart

For OHLC data displayed as bars instead of candlesticks.

```python
from streamlit_lightweight_charts import BarChart

chart = BarChart(
    data=ohlc_data,
    series_options=BarSeriesOptions(
        up_color='#26a69a',
        down_color='#ef5350'
    )
)
```

### 5. HistogramChart

For volume or distribution data.

```python
from streamlit_lightweight_charts import HistogramChart, HistogramData

data = [
    HistogramData(time=pd.Timestamp('2024-01-01'), value=1000000, color='#26a69a'),
    HistogramData(time=pd.Timestamp('2024-01-02'), value=1500000, color='#ef5350'),
    # ... more data
]

chart = HistogramChart(
    data=data,
    series_options=HistogramSeriesOptions()
)
```

### 6. BaselineChart

For data with a baseline reference value.

```python
from streamlit_lightweight_charts import BaselineChart, BaselineData

data = [
    BaselineData(time=pd.Timestamp('2024-01-01'), value=50),
    BaselineData(time=pd.Timestamp('2024-01-02'), value=55),
    # ... more data
]

chart = BaselineChart(
    data=data,
    series_options=BaselineSeriesOptions(
        base_value={'type': 'price', 'price': 52},
        top_line_color='rgba(38, 166, 154, 1)',
        bottom_line_color='rgba(239, 83, 80, 1)'
    )
)
```

## Trade Object Details

The `Trade` class represents a complete trading position:

```python
trade = Trade(
    # Required fields
    entry_time=pd.Timestamp('2024-01-01 10:30:00'),  # Accepts datetime, pd.Timestamp, string
    entry_price=100.50,
    exit_time=pd.Timestamp('2024-01-05 14:45:00'),
    exit_price=105.75,
    quantity=100,
    
    # Optional fields
    trade_type=TradeType.LONG,  # or TradeType.SHORT, default is LONG
    id="T001",                  # Trade identifier
    notes="Breakout trade"      # Additional notes
)

# Calculated properties
print(f"P&L: ${trade.pnl:.2f}")                    # Profit/Loss
print(f"P&L %: {trade.pnl_percentage:.1f}%")      # Percentage gain/loss
print(f"Profitable: {trade.is_profitable}")        # True/False
```

## Working with DataFrames

All specialized charts work seamlessly with pandas DataFrames:

```python
import pandas as pd
from streamlit_lightweight_charts.utils import df_to_ohlc_data, df_to_line_data

# Load your data
df = pd.read_csv('stock_data.csv', index_col='date', parse_dates=True)

# Convert to appropriate format
ohlc_data = df_to_ohlc_data(df)
chart = CandlestickChart(data=ohlc_data)

# For line data
line_data = df_to_line_data(df, value_column='close')
line_chart = LineChart(data=line_data)
```

## Benefits of Specialized Charts

### 1. Type Safety
```python
# This will raise a TypeError
try:
    chart = CandlestickChart(data=[{'time': '2024-01-01', 'value': 100}])
except TypeError as e:
    print(e)  # "CandlestickChart requires List[OhlcData]"
```

### 2. Automatic Validation
- Ensures data is in correct format
- Validates required fields
- Provides clear error messages

### 3. Chart-Specific Methods
Each chart type has methods relevant to its use case:
- `CandlestickChart`: `add_trades()`, `add_indicator()`
- `LineChart`: `add_line()`
- All charts: `add_series()`, `render()`

### 4. Cleaner Code
```python
# Instead of generic Chart with type checking
chart = Chart(series=CandlestickSeries(data=data))

# Use specialized chart
chart = CandlestickChart(data=data)
```

## Best Practices

### 1. Use DataFrame Converters
```python
# Good
data = df_to_ohlc_data(df)
chart = CandlestickChart(data=data)

# Avoid manual conversion
data = [OhlcData(...) for _, row in df.iterrows()]  # Slower
```

### 2. Handle Timezone Properly
```python
# Data will be automatically converted to UTC
df.index = pd.to_datetime(df.index).tz_localize('US/Eastern')
data = df_to_ohlc_data(df)
```

### 3. Validate Data Before Charting
```python
# Check for required columns
required_cols = ['open', 'high', 'low', 'close']
if not all(col in df.columns for col in required_cols):
    raise ValueError("Missing required OHLC columns")

# Remove invalid data
df = df.dropna()
df = df[df['high'] >= df['low']]  # Ensure high >= low
```

### 4. Use Type Hints
```python
def create_chart(data: List[OhlcData]) -> CandlestickChart:
    return CandlestickChart(
        data=data,
        options=ChartOptions(height=500)
    )
```

## Advanced Trade Visualization

### Custom Trade Colors
```python
trade_options = TradeVisualizationOptions(
    # Entry markers
    entry_marker_color_long='#2196F3',   # Blue for long entries
    entry_marker_color_short='#FF9800',  # Orange for short entries
    
    # Exit markers
    exit_marker_color_profit='#4CAF50',  # Green for profitable exits
    exit_marker_color_loss='#F44336',    # Red for losing exits
    
    # Rectangle colors
    rectangle_color_profit='#4CAF50',
    rectangle_color_loss='#F44336'
)
```

### Trade Annotations
```python
trade_options = TradeVisualizationOptions(
    show_trade_id=True,      # Show trade ID
    show_quantity=True,      # Show position size
    show_trade_type=True,    # Show LONG/SHORT
    annotation_font_size=12,
    annotation_background='rgba(255, 255, 255, 0.8)'
)
```

### Performance Tracking
```python
# Create trades from trading log
trades = []
for _, row in trading_log.iterrows():
    trades.append(Trade(
        entry_time=row['entry_date'],
        entry_price=row['entry_price'],
        exit_time=row['exit_date'],
        exit_price=row['exit_price'],
        quantity=row['shares'],
        trade_type=TradeType.LONG if row['side'] == 'buy' else TradeType.SHORT,
        id=row['trade_id']
    ))

# Visualize all trades
chart = CandlestickChart(
    data=ohlc_data,
    trades=trades,
    trade_visualization_options=TradeVisualizationOptions(
        style=TradeVisualization.ZONES,  # Show as colored zones
        zone_opacity=0.1
    )
)

# Calculate statistics
total_pnl = sum(t.pnl for t in trades)
win_rate = sum(1 for t in trades if t.is_profitable) / len(trades)
```

## Common Patterns

### Multi-Timeframe Analysis
```python
# Daily chart with trades
daily_chart = CandlestickChart(
    data=daily_data,
    trades=trades,
    trade_visualization_options=TradeVisualizationOptions(
        style=TradeVisualization.RECTANGLES
    )
)

# Hourly chart for detailed view
hourly_chart = CandlestickChart(
    data=hourly_data,
    trades=trades,  # Same trades on different timeframe
    trade_visualization_options=TradeVisualizationOptions(
        style=TradeVisualization.MARKERS  # Different style
    )
)
```

### Strategy Backtesting Display
```python
def display_backtest_results(df: pd.DataFrame, trades: List[Trade]):
    # Create chart with all trades
    chart = CandlestickChart(
        data=df_to_ohlc_data(df),
        trades=trades,
        trade_visualization_options=TradeVisualizationOptions(
            style=TradeVisualization.BOTH,
            show_pnl_in_markers=True
        )
    )
    
    # Add equity curve
    equity_data = calculate_equity_curve(trades)
    chart.add_indicator(
        data=equity_data,
        options=LineSeriesOptions(
            color='#9C27B0',
            line_width=2
        )
    )
    
    chart.render()
```

## Summary

Specialized charts provide:
- **Type safety** with proper data validation
- **Cleaner API** with chart-specific methods  
- **Better errors** with helpful messages
- **Trade visualization** with multiple styles
- **Seamless pandas integration**
- **Automatic timezone handling**

Choose the right chart type for your data and let the library handle the validation and rendering details.