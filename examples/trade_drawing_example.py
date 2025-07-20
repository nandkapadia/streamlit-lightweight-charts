"""
Trade Drawing Example

This example demonstrates advanced trade drawing and visualization using the new OOP architecture.
"""

from datetime import datetime, timedelta

import streamlit as st

from streamlit_lightweight_charts_pro import SinglePaneChart
from streamlit_lightweight_charts_pro.charts.series import CandlestickSeries
from streamlit_lightweight_charts_pro.data import (
    Marker,
    MarkerPosition,
    MarkerShape,
    OhlcData,
    Trade,
    TradeVisualizationOptions,
    TradeVisualization,
)

st.set_page_config(page_title="Trade Drawing Demo", layout="wide")

st.title("Trade Drawing Demo")
st.markdown(
    """
This example shows the new trade drawing functionality that allows you to:
- **Markers**: Add buy/sell markers with different shapes and colors
- **Rectangles**: Draw trade rectangles showing entry/exit periods
- **Combined**: Use both markers and rectangles together
- **Interactive**: Click on trades to see trade details
"""
)


# Generate sample data
def generate_trade_data(days=180):
    """Generate realistic OHLCV data using Geometric Brownian Motion"""
    import numpy as np
    
    data = []
    base_date = datetime.now() - timedelta(days=days)
    base_price = 100.0
    volume_base = 1000000
    
    # GBM parameters
    mu = 0.0001  # Daily drift (annualized ~2.5%)
    sigma = 0.02  # Daily volatility (annualized ~32%)
    dt = 1.0  # Daily time step
    
    # Generate price path using GBM
    np.random.seed(42)  # For reproducible results
    price_path = [base_price]
    
    for i in range(days - 1):
        # GBM formula: S(t+1) = S(t) * exp((mu - 0.5*sigma^2)*dt + sigma*sqrt(dt)*Z)
        drift = (mu - 0.5 * sigma**2) * dt
        diffusion = sigma * np.sqrt(dt) * np.random.normal(0, 1)
        new_price = price_path[-1] * np.exp(drift + diffusion)
        price_path.append(new_price)
    
    # Create OHLC data from price path
    for i, close_price in enumerate(price_path):
        date = base_date + timedelta(days=i)
        
        # Generate realistic OHLC from close price
        # Add some intraday volatility
        intraday_vol = sigma * 0.3  # 30% of daily volatility for intraday
        
        # Generate open, high, low from close
        open_price = close_price * (1 + np.random.normal(0, intraday_vol * 0.5))
        
        # High and low with realistic ranges
        price_range = close_price * intraday_vol
        high_price = max(open_price, close_price) + np.random.uniform(0, price_range * 0.5)
        low_price = min(open_price, close_price) - np.random.uniform(0, price_range * 0.5)
        
        # Ensure realistic OHLC relationships
        high_price = max(high_price, open_price, close_price)
        low_price = min(low_price, open_price, close_price)
        
        # Volume with some correlation to price movement
        price_change = abs(close_price - open_price) / open_price
        volume_factor = 1 + price_change * 5 + np.random.uniform(-0.3, 0.3)
        volume = max(volume_base * volume_factor, volume_base * 0.5)
        
        data.append(
            OhlcData(
                time=date.strftime("%Y-%m-%d"),
                open_=round(open_price, 2),
                high=round(high_price, 2),
                low=round(low_price, 2),
                close=round(close_price, 2)
            )
        )
    
    return data


# Generate sample trades
def generate_sample_trades(ohlcv_data):
    """Generate sample trades using actual OHLCV data prices with intraday times"""
    # Create a dictionary for quick lookup
    ohlcv_dict = {ohlc.time: ohlc for ohlc in ohlcv_data}
    
    # Get available dates from OHLC data
    available_dates = list(ohlcv_dict.keys())
    st.write(f"**Available dates in OHLC data: {len(available_dates)}**")
    st.write(f"**Date range: {available_dates[0]} to {available_dates[-1]}**")
    
    trades = []
    
    # Trade 1: Long trade with intraday entry time
    if len(available_dates) >= 20:
        entry_date = available_dates[10]  # Use actual date from data
        exit_date = available_dates[20]   # Use actual date from data
        
        if entry_date in ohlcv_dict and exit_date in ohlcv_dict:
            entry_price = ohlcv_dict[entry_date].close
            exit_price = ohlcv_dict[exit_date].close
            
            # Add intraday time to entry (09:30 AM)
            entry_time_with_intraday = f"{entry_date} 09:30:00"
            
            trades.append(Trade(
                entry_time=entry_time_with_intraday,
                entry_price=entry_price,
                exit_time=exit_date,
                exit_price=exit_price,
                quantity=100,
                trade_type="long",
            ))
    
    # Trade 2: Short trade with intraday exit time
    if len(available_dates) >= 40:
        entry_date = available_dates[25]  # Use actual date from data
        exit_date = available_dates[35]   # Use actual date from data
        
        if entry_date in ohlcv_dict and exit_date in ohlcv_dict:
            entry_price = ohlcv_dict[entry_date].close
            exit_price = ohlcv_dict[exit_date].close
            
            # Add intraday time to exit (14:45 PM)
            exit_time_with_intraday = f"{exit_date} 14:45:00"
            
            trades.append(Trade(
                entry_time=entry_date,
                entry_price=entry_price,
                exit_time=exit_time_with_intraday,
                exit_price=exit_price,
                quantity=50,
                trade_type="short",
            ))
    
    # Trade 3: Long trade with both intraday times
    if len(available_dates) >= 60:
        entry_date = available_dates[40]  # Use actual date from data
        exit_date = available_dates[55]   # Use actual date from data
        
        if entry_date in ohlcv_dict and exit_date in ohlcv_dict:
            entry_price = ohlcv_dict[entry_date].close
            exit_price = ohlcv_dict[exit_date].close
            
            # Add intraday times to both entry and exit
            entry_time_with_intraday = f"{entry_date} 10:15:00"
            exit_time_with_intraday = f"{exit_date} 15:20:00"
            
            trades.append(Trade(
                entry_time=entry_time_with_intraday,
                entry_price=entry_price,
                exit_time=exit_time_with_intraday,
                exit_price=exit_price,
                quantity=200,
                trade_type="long",
            ))
    
    # Trade 4: Short trade with intraday entry time
    if len(available_dates) >= 80:
        entry_date = available_dates[60]  # Use actual date from data
        exit_date = available_dates[75]   # Use actual date from data
        
        if entry_date in ohlcv_dict and exit_date in ohlcv_dict:
            entry_price = ohlcv_dict[entry_date].close
            exit_price = ohlcv_dict[exit_date].close
            
            # Add intraday time to entry (11:30 AM)
            entry_time_with_intraday = f"{entry_date} 11:30:00"
            
            trades.append(Trade(
                entry_time=entry_time_with_intraday,
                entry_price=entry_price,
                exit_time=exit_date,
                exit_price=exit_price,
                quantity=75,
                trade_type="short",
            ))
    
    # Trade 5: Test trade with time between market hours (12:30 PM)
    if len(available_dates) >= 100:
        entry_date = available_dates[80]  # Use actual date from data
        exit_date = available_dates[90]   # Use actual date from data
        
        if entry_date in ohlcv_dict and exit_date in ohlcv_dict:
            entry_price = ohlcv_dict[entry_date].close
            exit_price = ohlcv_dict[exit_date].close
            
            # Add intraday time between market hours
            entry_time_with_intraday = f"{entry_date} 12:30:00"
            exit_time_with_intraday = f"{exit_date} 13:45:00"
            
            trades.append(Trade(
                entry_time=entry_time_with_intraday,
                entry_price=entry_price,
                exit_time=exit_time_with_intraday,
                exit_price=exit_price,
                quantity=150,
                trade_type="long",
            ))
    
    st.write(f"**Generated {len(trades)} trades using actual OHLC data with intraday times**")
    return trades


# Generate data
ohlcv_data = generate_trade_data()
sample_trades = generate_sample_trades(ohlcv_data)

# Debug: Show trade information
st.subheader("🔍 Debug: Trade Information")
st.write(f"Generated {len(sample_trades)} trades:")
for i, trade in enumerate(sample_trades):
    st.write(f"**Trade {i+1}:** {trade.trade_type.upper()}")
    st.write(f"  Entry: {trade.entry_time} @ ${trade.entry_price:.2f}")
    st.write(f"  Exit: {trade.exit_time} @ ${trade.exit_price:.2f}")
    st.write(f"  P&L: ${trade.pnl:.2f} ({trade.pnl_percentage:.1f}%)")
    st.write(f"  Entry Timestamp: {trade.entry_timestamp}")
    st.write(f"  Exit Timestamp: {trade.exit_timestamp}")
    st.write(f"  Trade Dict: {trade.to_dict()}")
    st.write("---")

# Debug: Show OHLC data sample
st.write("**OHLC Data Sample (first 5 points):**")
for i, ohlc in enumerate(ohlcv_data[:5]):
    st.write(f"  {i+1}. {ohlc.time}: O={ohlc.open:.2f}, H={ohlc.high:.2f}, L={ohlc.low:.2f}, C={ohlc.close:.2f}")

# Sidebar controls
with st.sidebar:
    st.header("Trade Drawing Controls")

    # Display options
    st.subheader("Display Options")
    show_markers = st.checkbox("Show Trade Markers", True)
    show_rectangles = st.checkbox("Show Trade Rectangles", True)

    # Marker customization
    st.subheader("Marker Customization")
    marker_shape = st.selectbox(
        "Default Marker Shape",
        [
            "arrowUp",
            "arrowDown",
            "circle",
            "square",
            "triangleUp",
            "triangleDown",
            "flag",
        ],
        index=0,
    )

    marker_size = st.slider("Marker Size", 1, 5, 2)

    # Rectangle customization
    st.subheader("Rectangle Customization")
    rectangle_opacity = st.slider("Rectangle Opacity", 0.1, 1.0, 0.2)

    # Add new trade
    st.subheader("Add New Trade")
    with st.form("add_trade"):
        trade_type = st.selectbox("Trade Type", ["buy", "sell", "long", "short"])
        entry_time = st.date_input("Entry Date", datetime.now() - timedelta(days=30))
        entry_price = st.number_input("Entry Price", min_value=50.0, max_value=200.0, value=100.0)
        exit_time = st.date_input("Exit Date", datetime.now() - timedelta(days=10))
        exit_price = st.number_input("Exit Price", min_value=50.0, max_value=200.0, value=105.0)
        quantity = st.number_input("Quantity", min_value=1, value=100)

        if st.form_submit_button("Add Trade"):
            new_trade = Trade(
                entry_time=entry_time.strftime("%Y-%m-%d"),
                entry_price=entry_price,
                exit_time=exit_time.strftime("%Y-%m-%d"),
                exit_price=exit_price,
                quantity=quantity,
                trade_type=trade_type,
            )
            sample_trades.append(new_trade)
            st.success("Trade added!")

# Create markers for demonstration
base_date = datetime.now() - timedelta(days=180)
markers = [
    Marker(
        time=(base_date + timedelta(days=15)).strftime("%Y-%m-%d"),  # Day 15
        position=MarkerPosition.BELOW_BAR,
        color="#4CAF50",
        shape=MarkerShape.CIRCLE,
        text="BUY SIGNAL",
        size=marker_size,
    ),
    Marker(
        time=(base_date + timedelta(days=35)).strftime("%Y-%m-%d"),  # Day 35
        position=MarkerPosition.ABOVE_BAR,
        color="#FF5722",
        shape=MarkerShape.ARROW_DOWN,
        text="SELL SIGNAL",
        size=marker_size,
    ),
]

# Determine trade visualization style based on user selections
if show_markers and show_rectangles:
    trade_style = TradeVisualization.BOTH
elif show_markers:
    trade_style = TradeVisualization.MARKERS
elif show_rectangles:
    trade_style = TradeVisualization.RECTANGLES
else:
    trade_style = TradeVisualization.BOTH  # Default to both if nothing selected

# Debug: Show trade visualization options
st.write(f"**Trade Visualization Style:** {trade_style}")
st.write(f"**Show Markers:** {show_markers}")
st.write(f"**Show Rectangles:** {show_rectangles}")
st.write(f"**Rectangle Opacity:** {rectangle_opacity}")

# Create candlestick series with trades and markers
candlestick_series = CandlestickSeries(
    data=ohlcv_data,
    up_color="#4CAF50",
    down_color="#F44336",
    markers=markers if show_markers else None,
    trades=sample_trades,  # Always pass trades
    trade_visualization_options=TradeVisualizationOptions(
        style=trade_style,
        entry_marker_color_long="#4CAF50",
        entry_marker_color_short="#FF5722",
        exit_marker_color_profit="#4CAF50",
        exit_marker_color_loss="#F44336",
        rectangle_fill_opacity=rectangle_opacity,
        rectangle_border_width=2,
        show_trade_id=True,
        show_quantity=True,
        show_pnl_in_markers=True
    )
)

# Create chart
chart = SinglePaneChart(series=candlestick_series)

# Debug: Show chart configuration
st.write("**Chart Configuration:**")
chart_config = chart.to_frontend_config()
st.write(f"  Number of charts: {len(chart_config['charts'])}")
if chart_config['charts']:
    first_chart = chart_config['charts'][0]
    st.write(f"  Number of series: {len(first_chart['series'])}")
    st.write(f"  Has trades: {'trades' in first_chart}")
    if 'trades' in first_chart:
        st.write(f"  Number of trades: {len(first_chart['trades'])}")
        st.write(f"  Has trade options: {'tradeVisualizationOptions' in first_chart}")
    st.write(f"  Chart config keys: {list(first_chart.keys())}")

# Render the chart
chart.render(key="trade_drawing_demo")

# Display trade information
st.subheader("Trade Summary")
for trade_idx, trade in enumerate(sample_trades, 1):
    pnl = trade.pnl
    return_pct = trade.pnl_percentage

    st.write(f"**Trade {trade_idx}**: {trade.trade_type.upper()} {trade.quantity} shares")
    st.write(f"Entry: {trade.entry_time} @ ${trade.entry_price}")
    st.write(f"Exit: {trade.exit_time} @ ${trade.exit_price}")
    st.write(f"P&L: ${pnl:.2f} ({return_pct:.1f}%)")
    st.write("---")

# Performance metrics
st.subheader("Performance Metrics")
col1, col2, col3, col4 = st.columns(4)

total_pnl = sum(trade.pnl for trade in sample_trades)
total_return = sum(trade.pnl_percentage for trade in sample_trades)
winning_trades = sum(1 for trade in sample_trades if trade.pnl > 0)
num_trades = len(sample_trades)

with col1:
    st.metric("Total P&L", f"${total_pnl:.2f}", f"{total_return:.1f}%")

with col2:
    win_rate = (winning_trades / num_trades) * 100 if num_trades > 0 else 0
    st.metric("Win Rate", f"{win_rate:.1f}%", f"{winning_trades}/{num_trades}")

with col3:
    avg_pnl = total_pnl / num_trades if num_trades > 0 else 0
    st.metric("Avg P&L per Trade", f"${avg_pnl:.2f}")

with col4:
    st.metric("Total Trades", f"{num_trades}")

# Usage instructions
with st.expander("How to Use Trade Drawing"):
    st.markdown(
        """
    ### Trade Drawing Features
    
    1. **Trade Markers**: Visual indicators for entry/exit points
    2. **Trade Rectangles**: Show trade duration and price range
    3. **P&L Calculation**: Automatic profit/loss calculation
    4. **Interactive Controls**: Add new trades dynamically
    5. **Customization**: Customize markers and rectangles
    
    ### Code Example
    ```python
    # Create trades
    trades = [
        Trade(
            trade_type=TradeType.BUY,
            entry_time="2024-01-15",
            entry_price=95.50,
            exit_time="2024-01-25",
            exit_price=102.30,
            quantity=100,
            symbol="AAPL"
        )
    ]
    
    # Create markers
    markers = [
        Marker(
            time="2024-01-10",
            position=MarkerPosition.BELOW_BAR,
            color="#4CAF50",
            shape=MarkerShape.CIRCLE,
            text="BUY SIGNAL"
        )
    ]
    
    # Create candlestick chart with trades and markers
    chart = CandlestickChart(
        data=ohlcv_data,
        trades=trades,
        markers=markers
    )
    
    # Render the chart
    render_chart(chart, key="trade_demo")
    ```
    """
    )
