# Composite Charts Guide

Composite charts are pre-built combinations of common chart patterns that make it easy to create complex financial visualizations with minimal code.

## Available Composite Charts

### 1. PriceVolumeChart

The most common financial chart combining price (candlestick, line, area, or bar) with volume histogram below.

```python
from streamlit_lightweight_charts import PriceVolumeChart

# Basic usage
chart = PriceVolumeChart(
    df=stock_data,
    price_type='candlestick',  # 'candlestick', 'line', 'area', or 'bar'
    price_height=400,
    volume_height=100
)
chart.render()

# With custom options
chart = PriceVolumeChart(
    df=stock_data,
    price_type='candlestick',
    price_options=ChartOptions(
        layout=LayoutOptions(background=Background.solid('#1e1e1e'))
    ),
    price_series_options=CandlestickSeriesOptions(
        up_color='#26a69a',
        down_color='#ef5350'
    )
)

# Add indicators
sma_data = df_to_line_data(df, value_column='SMA_20')
chart.add_price_indicator(
    indicator_data=sma_data,
    options=LineSeriesOptions(color='#FF6B6B')
)
```

**Features:**
- Automatic volume coloring based on price movement
- Synchronized crosshairs between price and volume
- Easy indicator overlay with `add_price_indicator()`
- Customizable heights for each pane

### 2. PriceWithMAChart

Price chart with automatic moving average calculations.

```python
from streamlit_lightweight_charts import PriceWithMAChart

# Create chart with multiple MAs
chart = PriceWithMAChart(
    df=stock_data,
    ma_periods=[10, 20, 50, 200],  # Calculate these MAs
    price_type='candlestick',      # or 'line'
    ma_colors=['#2196F3', '#FF9800', '#4CAF50', '#F44336']
)
chart.render()

# Access individual series
chart.price_series  # The main price series
chart.ma_series     # List of MA series
```

**Features:**
- Automatic MA calculation from DataFrame
- Customizable periods and colors
- Handles NaN values appropriately
- Supports both candlestick and line price display

### 3. ComparisonChart

Compare multiple instruments with automatic normalization.

```python
from streamlit_lightweight_charts import ComparisonChart

# Compare multiple stocks
chart = ComparisonChart(
    dataframes=[
        ('AAPL', apple_df),
        ('GOOGL', google_df),
        ('MSFT', microsoft_df)
    ],
    normalize=True,  # Show as percentage change
    value_column='close'
)
chart.render()

# Access metadata
print(chart.series_names)  # ['AAPL', 'GOOGL', 'MSFT']
print(chart.normalized)    # True
```

**Features:**
- Automatic percentage normalization
- Multiple instrument comparison
- Customizable colors
- Percentage scale display when normalized

### 4. BollingerBandsChart

Price with Bollinger Bands for volatility analysis.

```python
from streamlit_lightweight_charts import BollingerBandsChart

# Create Bollinger Bands chart
chart = BollingerBandsChart(
    df=stock_data,
    period=20,           # MA period
    std_dev=2.0,        # Standard deviations
    price_type='line',  # or 'candlestick'
    band_color='#9E9E9E'
)
chart.render()
```

**Features:**
- Automatic band calculation
- Customizable period and standard deviation
- Support for both line and candlestick price display
- Clean visualization with proper styling

## Creating Custom Composite Charts

You can easily create your own composite charts by extending the base classes:

### Example: RSI with Price Chart

```python
from streamlit_lightweight_charts import MultiPaneChart, CandlestickChart, LineChart
from streamlit_lightweight_charts.utils import df_to_line_data
import pandas as pd

class RSIWithPriceChart(MultiPaneChart):
    def __init__(self, df: pd.DataFrame, rsi_period: int = 14):
        # Calculate RSI
        df['RSI'] = self._calculate_rsi(df['close'], rsi_period)
        
        # Create price chart
        price_chart = CandlestickChart(
            data=df_to_ohlc_data(df),
            options=ChartOptions(height=400)
        )
        
        # Create RSI chart
        rsi_data = df_to_line_data(df.dropna(), value_column='RSI')
        rsi_chart = LineChart(
            data=rsi_data,
            options=ChartOptions(height=150)
        )
        
        # Add overbought/oversold lines
        rsi_chart.add_line(
            data=[{'time': d['time'], 'value': 70} for d in rsi_data],
            options=LineSeriesOptions(color='#ff0000', line_width=1)
        )
        rsi_chart.add_line(
            data=[{'time': d['time'], 'value': 30} for d in rsi_data],
            options=LineSeriesOptions(color='#00ff00', line_width=1)
        )
        
        super().__init__([price_chart, rsi_chart])
    
    def _calculate_rsi(self, prices: pd.Series, period: int) -> pd.Series:
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
```

### Example: MACD Chart

```python
class MACDChart(MultiPaneChart):
    def __init__(
        self,
        df: pd.DataFrame,
        fast_period: int = 12,
        slow_period: int = 26,
        signal_period: int = 9
    ):
        # Calculate MACD
        exp1 = df['close'].ewm(span=fast_period, adjust=False).mean()
        exp2 = df['close'].ewm(span=slow_period, adjust=False).mean()
        df['MACD'] = exp1 - exp2
        df['Signal'] = df['MACD'].ewm(span=signal_period, adjust=False).mean()
        df['Histogram'] = df['MACD'] - df['Signal']
        
        # Create price chart
        price_chart = CandlestickChart(
            data=df_to_ohlc_data(df),
            options=ChartOptions(height=400)
        )
        
        # Create MACD chart
        macd_chart = Chart(options=ChartOptions(height=200))
        
        # Add MACD line
        macd_data = df_to_line_data(df.dropna(), value_column='MACD')
        macd_chart.add_series(LineSeries(
            data=macd_data,
            options=LineSeriesOptions(color='#2196F3')
        ))
        
        # Add Signal line
        signal_data = df_to_line_data(df.dropna(), value_column='Signal')
        macd_chart.add_series(LineSeries(
            data=signal_data,
            options=LineSeriesOptions(color='#FF6B6B')
        ))
        
        # Add Histogram
        hist_data = df_to_histogram_data(df.dropna(), value_column='Histogram')
        macd_chart.add_series(HistogramSeries(
            data=hist_data,
            options=HistogramSeriesOptions()
        ))
        
        super().__init__([price_chart, macd_chart])
```

## Best Practices

### 1. Data Preparation
```python
# Ensure your DataFrame has proper datetime index
df.index = pd.to_datetime(df.index)

# Handle missing data appropriately
df = df.fillna(method='ffill')  # or df.dropna()

# Sort by time
df = df.sort_index()
```

### 2. Performance Optimization
```python
# Resample large datasets
from streamlit_lightweight_charts.utils import resample_df_for_charts
df_resampled = resample_df_for_charts(df, max_bars=1000)

# Use the resampled data
chart = PriceVolumeChart(df=df_resampled)
```

### 3. Styling Consistency
```python
# Create a theme
dark_theme = ChartOptions(
    layout=LayoutOptions(
        background=Background.solid('#1e1e1e'),
        text_color='#d1d4dc'
    ),
    grid=GridOptions(
        vert_lines=GridLineOptions(color='#2B2B43'),
        horz_lines=GridLineOptions(color='#2B2B43')
    )
)

# Apply to all charts
chart1 = PriceVolumeChart(df=data1, price_options=dark_theme)
chart2 = BollingerBandsChart(df=data2, chart_options=dark_theme)
```

### 4. Interactive Features
```python
# Add markers to highlight events
markers = [
    Marker(
        time=pd.Timestamp('2024-01-15'),
        position='belowBar',
        shape='arrowUp',
        color='#26a69a',
        text='Buy Signal'
    )
]

# For PriceVolumeChart
chart = PriceVolumeChart(df=stock_data)
chart.price_chart.series[0].markers = markers
```

## Common Patterns

### Financial Dashboard
```python
import streamlit as st

# Layout with multiple charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("AAPL")
    PriceVolumeChart(df=apple_data).render(key='aapl')

with col2:
    st.subheader("Market Comparison")
    ComparisonChart(
        dataframes=[
            ('AAPL', apple_data),
            ('SPY', spy_data),
            ('QQQ', qqq_data)
        ]
    ).render(key='comparison')

# Technical analysis section
st.subheader("Technical Analysis")
PriceWithMAChart(
    df=apple_data,
    ma_periods=[20, 50, 200]
).render(key='technical')
```

### Real-time Updates
```python
# Use st.empty() for updates
chart_placeholder = st.empty()

while True:
    # Get latest data
    df = fetch_latest_data()
    
    # Update chart
    with chart_placeholder.container():
        PriceVolumeChart(df=df).render(key='realtime')
    
    time.sleep(1)
```

## Extending Composite Charts

### Adding Methods
```python
class EnhancedPriceVolumeChart(PriceVolumeChart):
    def add_support_resistance(self, levels: List[float]):
        """Add horizontal lines for support/resistance."""
        for level in levels:
            line_data = [
                {'time': d['time'], 'value': level}
                for d in self.price_chart.series[0].data
            ]
            self.price_chart.add_series(LineSeries(
                data=line_data,
                options=LineSeriesOptions(
                    color='#9C27B0',
                    line_width=1,
                    line_style=LineStyle.DASHED
                )
            ))
    
    def highlight_volume_spikes(self, threshold: float = 2.0):
        """Highlight volume bars above threshold."""
        # Implementation here
        pass
```

### Custom Indicators
```python
def create_pivot_points_chart(df: pd.DataFrame) -> MultiPaneChart:
    """Create chart with pivot points."""
    # Calculate pivot points
    df['Pivot'] = (df['high'] + df['low'] + df['close']) / 3
    df['R1'] = 2 * df['Pivot'] - df['low']
    df['S1'] = 2 * df['Pivot'] - df['high']
    
    # Create base chart
    chart = PriceWithMAChart(df=df, ma_periods=[])
    
    # Add pivot lines
    for col, color in [('Pivot', '#FFD700'), ('R1', '#FF0000'), ('S1', '#00FF00')]:
        data = df_to_line_data(df, value_column=col)
        chart.add_series(LineSeries(
            data=data,
            options=LineSeriesOptions(color=color, line_width=1)
        ))
    
    return chart
```

## Performance Tips

1. **Large Datasets**: Always resample data before charting
2. **Multiple Charts**: Use unique keys for each render
3. **Updates**: Cache data transformations with `@st.cache_data`
4. **Memory**: Clean up DataFrames after calculations

## Troubleshooting

### Common Issues

1. **Empty Charts**: Check DataFrame has valid datetime index
2. **Missing Indicators**: Ensure calculations don't produce all NaN
3. **Performance**: Reduce data points or use resampling
4. **Styling**: Verify color formats ('#RRGGBB' or 'rgba()')

### Debug Helper
```python
def debug_chart_data(df: pd.DataFrame):
    """Print debug info for chart data."""
    print(f"Shape: {df.shape}")
    print(f"Index type: {type(df.index)}")
    print(f"Columns: {df.columns.tolist()}")
    print(f"Missing values: {df.isnull().sum()}")
    print(f"Date range: {df.index.min()} to {df.index.max()}")
```