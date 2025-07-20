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
    """Generate sample OHLCV data with trade opportunities"""
    data = []
    base_date = datetime.now() - timedelta(days=days)
    base_price = 100

    for i in range(days):
        date = base_date + timedelta(days=i)
        # Create some obvious trade opportunities
        if i % 20 == 0:  # Every 20 days, create a dip
            base_price -= 5
        elif i % 15 == 0:  # Every 15 days, create a peak
            base_price += 8

        open_price = base_price + (i % 3) * 0.5
        close_price = open_price + (1 if i % 2 == 0 else -1) * 1.2
        high_price = max(open_price, close_price) + 0.8
        low_price = min(open_price, close_price) - 0.8

        data.append(
            OhlcData(date.strftime("%Y-%m-%d"), open_price, high_price, low_price, close_price)
        )

        base_price = close_price

    return data


# Generate sample trades
def generate_sample_trades():
    """Generate sample trades for demonstration"""
    # Calculate dates that exist in the generated data
    base_date = datetime.now() - timedelta(days=180)

    # Create trades at specific intervals that match the data generation pattern
    trades = [
        Trade(
            entry_time=(base_date + timedelta(days=20)).strftime("%Y-%m-%d"),  # Day 20 (dip)
            entry_price=95.50,
            exit_time=(base_date + timedelta(days=30)).strftime("%Y-%m-%d"),  # Day 30
            exit_price=102.30,
            quantity=100,
            trade_type="long",
        ),
        Trade(
            entry_time=(base_date + timedelta(days=40)).strftime("%Y-%m-%d"),  # Day 40 (peak)
            entry_price=105.20,
            exit_time=(base_date + timedelta(days=50)).strftime("%Y-%m-%d"),  # Day 50
            exit_price=98.80,
            quantity=50,
            trade_type="short",
        ),
        Trade(
            entry_time=(base_date + timedelta(days=60)).strftime("%Y-%m-%d"),  # Day 60 (dip)
            entry_price=92.10,
            exit_time=(base_date + timedelta(days=75)).strftime("%Y-%m-%d"),  # Day 75 (peak)
            exit_price=108.50,
            quantity=200,
            trade_type="long",
        ),
        Trade(
            entry_time=(base_date + timedelta(days=90)).strftime("%Y-%m-%d"),  # Day 90 (peak)
            entry_price=110.30,
            exit_time=(base_date + timedelta(days=105)).strftime("%Y-%m-%d"),  # Day 105 (dip)
            exit_price=95.20,
            quantity=75,
            trade_type="short",
        ),
    ]
    return trades


# Generate data
ohlcv_data = generate_trade_data()
sample_trades = generate_sample_trades()

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
    trade_style = None

# Create candlestick series with trades and markers
candlestick_series = CandlestickSeries(
    data=ohlcv_data,
    up_color="#4CAF50",
    down_color="#F44336",
    markers=markers if show_markers else None,
    trades=sample_trades if (show_markers or show_rectangles) else None,
    trade_visualization_options=(
        TradeVisualizationOptions(
            style=trade_style,
            entry_marker_color_long="#4CAF50",
            entry_marker_color_short="#FF5722",
            exit_marker_color_profit="#4CAF50",
            exit_marker_color_loss="#F44336",
        )
        if trade_style
        else None
    ),
)

# Create chart
chart = SinglePaneChart(series=candlestick_series)

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
