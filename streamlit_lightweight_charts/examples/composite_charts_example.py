"""Example demonstrating composite charts."""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from streamlit_lightweight_charts import (
    PriceVolumeChart, ComparisonChart,
    ChartOptions, LayoutOptions, Background,
    CandlestickSeriesOptions, LineSeriesOptions
)


@st.cache_data
def generate_stock_data(symbol: str = 'STOCK', days: int = 100, start_price: float = 100):
    """Generate sample stock data."""
    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
    
    # Generate price data with trend and volatility
    trend = np.random.choice([1, -1]) * np.random.uniform(0, 0.2)
    volatility = np.random.uniform(0.01, 0.03)
    
    prices = [start_price]
    for i in range(1, days):
        change = np.random.randn() * volatility + trend / days
        prices.append(prices[-1] * (1 + change))
    
    df = pd.DataFrame(index=dates)
    df['close'] = prices
    
    # Generate OHLC from close
    df['open'] = df['close'].shift(1).fillna(df['close'].iloc[0])
    df['high'] = df[['open', 'close']].max(axis=1) * (1 + np.abs(np.random.randn(days) * 0.005))
    df['low'] = df[['open', 'close']].min(axis=1) * (1 - np.abs(np.random.randn(days) * 0.005))
    
    # Generate volume (higher volume on larger price moves)
    price_change = df['close'].pct_change().fillna(0).abs()
    base_volume = np.random.randint(1000000, 2000000)
    df['volume'] = base_volume * (1 + price_change * 10) * (1 + np.random.randn(days) * 0.3)
    df['volume'] = df['volume'].astype(int)
    
    return df


def main():
    st.title("Composite Charts Example")
    st.markdown("This example demonstrates pre-built composite chart types.")
    
    # Generate sample data
    stock_data = generate_stock_data(days=90)
    
    # Create chart options
    chart_options = ChartOptions(
        layout=LayoutOptions(
            background=Background.solid('#f5f5f5'),
            text_color='#333'
        )
    )
    
    # Example 1: PriceVolumeChart
    st.header("1. Price-Volume Chart")
    st.markdown("The most common financial chart - candlesticks with volume below.")
    
    price_volume_chart = PriceVolumeChart(
        df=stock_data,
        price_type='candlestick',
        price_height=400,
        volume_height=100,
        price_options=chart_options
    )
    price_volume_chart.render(key='price_volume')
    
    st.code("""
# Create a price-volume chart with one line of code
chart = PriceVolumeChart(
    df=stock_data,
    price_type='candlestick',  # or 'line', 'area', 'bar'
    price_height=400,
    volume_height=100
)
chart.render()
    """)
    
    # Example 2: Comparison Chart
    st.header("2. Comparison Chart")
    st.markdown("Compare multiple instruments with automatic normalization.")
    
    # Generate data for multiple stocks
    stocks_data = [
        ('TECH', generate_stock_data('TECH', 90, 150)),
        ('RETAIL', generate_stock_data('RETAIL', 90, 80)),
        ('ENERGY', generate_stock_data('ENERGY', 90, 120))
    ]
    
    comparison_chart = ComparisonChart(
        dataframes=stocks_data,
        normalize=True,  # Show as percentage change
        chart_options=chart_options
    )
    comparison_chart.render(key='comparison')
    
    st.code("""
# Compare multiple instruments
chart = ComparisonChart(
    dataframes=[
        ('TECH', tech_df),
        ('RETAIL', retail_df),
        ('ENERGY', energy_df)
    ],
    normalize=True  # Shows percentage change from start
)
    """)
    
    # Example 3: Advanced Price-Volume with Indicators
    st.header("3. Advanced Price-Volume Chart")
    st.markdown("Price-Volume chart with added indicators.")
    
    # Calculate additional indicators
    stock_data['SMA_20'] = stock_data['close'].rolling(window=20).mean()
    
    # Create price-volume chart
    adv_chart = PriceVolumeChart(
        df=stock_data,
        price_type='candlestick',
        price_series_options=CandlestickSeriesOptions(
            up_color='#26a69a',
            down_color='#ef5350',
            border_visible=False
        )
    )
    
    # Add SMA as indicator
    from streamlit_lightweight_charts.utils import df_to_line_data
    sma_data = df_to_line_data(stock_data.dropna(), value_column='SMA_20')
    adv_chart.add_price_indicator(
        indicator_data=sma_data,
        options=LineSeriesOptions(
            color='#FF6B6B',
            line_width=2
        )
    )
    
    adv_chart.render(key='advanced_pv')
    
    st.code("""
# Create base chart
chart = PriceVolumeChart(df=stock_data)

# Add indicators
sma_data = df_to_line_data(df, value_column='SMA_20')
chart.add_price_indicator(
    indicator_data=sma_data,
    options=LineSeriesOptions(color='#FF6B6B')
)
    """)
    
    # Example 4: Different Price Types
    st.header("4. Different Price Display Types")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Area Chart with Volume")
        area_pv = PriceVolumeChart(
            df=stock_data,
            price_type='area',
            price_height=250,
            volume_height=80
        )
        area_pv.render(key='area_pv')
    
    with col2:
        st.subheader("Line Chart with Volume")
        line_pv = PriceVolumeChart(
            df=stock_data,
            price_type='line',
            price_height=250,
            volume_height=80
        )
        line_pv.render(key='line_pv')
    
    # Benefits summary
    st.header("Benefits of Composite Charts")
    
    st.markdown("""
    ### 🚀 Rapid Development
    - Create complex charts with one line of code
    - Common patterns are pre-built and tested
    - Sensible defaults for financial data
    
    ### 📊 Common Use Cases
    - **PriceVolumeChart**: Standard financial chart
    - **ComparisonChart**: Multi-instrument analysis
    
    ### 🎨 Customizable
    - All options from base charts are available
    - Add custom indicators and overlays
    - Full control over appearance
    
    ### 🔧 Extensible
    ```python
    # Easy to create your own composite charts
    class RSIWithPriceChart(MultiPaneChart):
        def __init__(self, df, rsi_period=14):
            price_chart = CandlestickChart(...)
            rsi_chart = self._calculate_rsi_chart(df, rsi_period)
            super().__init__([price_chart, rsi_chart])
    ```
    """)


if __name__ == "__main__":
    main()