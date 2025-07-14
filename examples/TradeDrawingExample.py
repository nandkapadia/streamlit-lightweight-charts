"""
Trade Drawing Example

This example demonstrates the new trade drawing functionality that allows users to:
1. Add buy/sell markers on candlestick charts
2. Draw trade rectangles showing trade duration
3. Combine both markers and rectangles
4. Handle trade click events
"""

import streamlit as st
from datetime import datetime, timedelta
from streamlit_lightweight_charts import (
    Chart, ChartGroup, SeriesType, TradeType, MarkerShape, Themes,
    create_trade_chart
)

st.set_page_config(page_title="Trade Drawing Demo", layout="wide")

st.title("Trade Drawing Demo")
st.markdown("""
This example shows the new trade drawing functionality that allows you to:
- **Markers**: Add buy/sell markers with different shapes and colors
- **Rectangles**: Draw trade rectangles showing entry/exit periods
- **Combined**: Use both markers and rectangles together
- **Interactive**: Click on trades to see trade details
""")

# Generate sample data
def generate_trade_data(days=100):
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
        volume = 1000000 + abs(close_price - open_price) * 100000
        
        data.append({
            'time': date.strftime('%Y-%m-%d'),
            'open': open_price,
            'high': high_price,
            'low': low_price,
            'close': close_price,
            'volume': volume
        })
        
        base_price = close_price
    
    return data

# Generate sample trades
def generate_sample_trades():
    """Generate sample trades for demonstration"""
    trades = [
        {
            "type": TradeType.BUY,
            "entry_time": "2024-01-15",
            "entry_price": 95.50,
            "exit_time": "2024-01-25",
            "exit_price": 102.30,
            "quantity": 100,
            "symbol": "AAPL",
            "marker_color": "#26a69a",
            "rectangle_color": "rgba(38, 166, 154, 0.2)"
        },
        {
            "type": TradeType.SELL,
            "entry_time": "2024-02-10",
            "entry_price": 105.20,
            "exit_time": "2024-02-20",
            "exit_price": 98.80,
            "quantity": 50,
            "symbol": "AAPL",
            "marker_color": "#ef5350",
            "rectangle_color": "rgba(239, 83, 80, 0.2)"
        },
        {
            "type": TradeType.LONG,
            "entry_time": "2024-03-05",
            "entry_price": 92.10,
            "exit_time": "2024-03-15",
            "exit_price": 108.50,
            "quantity": 200,
            "symbol": "AAPL",
            "marker_color": "#4CAF50",
            "rectangle_color": "rgba(76, 175, 80, 0.2)"
        },
        {
            "type": TradeType.SHORT,
            "entry_time": "2024-03-25",
            "entry_price": 110.30,
            "exit_time": "2024-04-05",
            "exit_price": 95.20,
            "quantity": 75,
            "symbol": "AAPL",
            "marker_color": "#FF9800",
            "rectangle_color": "rgba(255, 152, 0, 0.2)"
        }
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
        ["arrowUp", "arrowDown", "circle", "square", "triangleUp", "triangleDown", "flag"],
        index=0
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
            new_trade = {
                "type": trade_type,
                "entry_time": entry_time.strftime('%Y-%m-%d'),
                "entry_price": entry_price,
                "exit_time": exit_time.strftime('%Y-%m-%d'),
                "exit_price": exit_price,
                "quantity": quantity,
                "symbol": "AAPL"
            }
            sample_trades.append(new_trade)
            st.success("Trade added!")

# Create chart group
chart_group = ChartGroup(
    sync_enabled=True,
    sync_crosshair=True,
    sync_time_range=True
)

# Main trade chart
trade_chart = Chart(
    height=500,
    **Themes.TRADING_VIEW,
    watermark={
        'visible': True,
        'text': 'TRADE ANALYSIS',
        'fontSize': 20,
        'color': 'rgba(255, 255, 255, 0.1)'
    }
)

# Add candlestick series
trade_chart.add_series(
    SeriesType.CANDLESTICK,
    ohlcv_data,
    name="Price",
    options={
        'upColor': '#26a69a',
        'downColor': '#ef5350',
        'borderVisible': False,
        'wickUpColor': '#26a69a',
        'wickDownColor': '#ef5350'
    }
)

# Add trades
for trade in sample_trades:
    trade_chart.add_trade(
        trade_type=trade["type"],
        entry_time=trade["entry_time"],
        entry_price=trade["entry_price"],
        exit_time=trade["exit_time"],
        exit_price=trade["exit_price"],
        quantity=trade["quantity"],
        symbol=trade["symbol"],
        show_markers=show_markers,
        show_rectangle=show_rectangles,
        marker_color=trade.get("marker_color"),
        rectangle_color=trade.get("rectangle_color")
    )

# Add individual markers for demonstration
trade_chart.add_trade_marker(
    time="2024-01-10",
    price=94.50,
    trade_type=TradeType.BUY,
    shape=MarkerShape.CIRCLE,
    text="BUY SIGNAL",
    color="#4CAF50",
    size=marker_size
)

trade_chart.add_trade_marker(
    time="2024-02-05",
    price=107.80,
    trade_type=TradeType.SELL,
    shape=MarkerShape.TRIANGLE_DOWN,
    text="SELL SIGNAL",
    color="#FF5722",
    size=marker_size
)

# Add range switcher
trade_chart.add_range_switcher(
    position="top-right",
    default_range="3M"
)

# Volume chart
volume_chart = Chart(
    height=150,
    **Themes.TRADING_VIEW,
    time_scale={'visible': True}
)

volume_data = [
    {'time': item['time'], 'value': item['volume']} 
    for item in ohlcv_data
]

volume_chart.add_series(
    SeriesType.HISTOGRAM,
    volume_data,
    name="Volume",
    options={
        'color': '#26a69a',
        'priceFormat': {'type': 'volume'}
    }
)

# Add charts to group
chart_group.add_chart(trade_chart)
chart_group.add_chart(volume_chart)

# Event callbacks
def on_trade_click(event_data):
    st.session_state['last_trade_click'] = event_data
    trade = event_data['trade']
    st.info(f"Trade clicked: {trade['type'].upper()} {trade['quantity']} @ {trade['entry_price']}")

def on_crosshair_move(event_data):
    if 'crosshair_data' not in st.session_state:
        st.session_state.crosshair_data = {}
    st.session_state.crosshair_data = event_data

# Register callbacks
chart_group.on_trade_click(on_trade_click)
chart_group.on_crosshair_move(on_crosshair_move)

# Render the chart group
chart_group.render(key="trade_drawing_demo")

# Display event information
col1, col2 = st.columns(2)

with col1:
    st.subheader("Last Trade Click")
    if 'last_trade_click' in st.session_state:
        st.json(st.session_state['last_trade_click'])
    else:
        st.info("Click on trade markers to see trade details")

with col2:
    st.subheader("Current Crosshair Position")
    if 'crosshair_data' in st.session_state:
        st.json(st.session_state['crosshair_data'])
    else:
        st.info("Move crosshair to see position data")

# Trade summary
st.subheader("Trade Summary")
trade_df = st.dataframe(
    [
        {
            "Type": trade["type"].upper(),
            "Entry Date": trade["entry_time"],
            "Entry Price": f"${trade['entry_price']:.2f}",
            "Exit Date": trade["exit_time"],
            "Exit Price": f"${trade['exit_price']:.2f}",
            "Quantity": trade["quantity"],
            "P&L": f"${(trade['exit_price'] - trade['entry_price']) * trade['quantity']:.2f}",
            "Return %": f"{((trade['exit_price'] / trade['entry_price']) - 1) * 100:.1f}%"
        }
        for trade in sample_trades
    ],
    use_container_width=True
)

# Usage instructions
with st.expander("How to Use Trade Drawing"):
    st.markdown("""
    ### Trade Drawing Features
    
    1. **Trade Markers**: 
       - Buy markers: Green arrows pointing up
       - Sell markers: Red arrows pointing down
       - Customizable shapes and colors
    
    2. **Trade Rectangles**: 
       - Show trade duration with colored overlays
       - Entry and exit price lines
       - Customizable opacity and colors
    
    3. **Trade Management**:
       - Add trades programmatically
       - Click on trades for details
       - Event callbacks for trade interactions
    
    ### Code Examples
    
    ```python
    # Add a complete trade
    chart.add_trade(
        trade_type=TradeType.BUY,
        entry_time="2024-01-15",
        entry_price=95.50,
        exit_time="2024-01-25",
        exit_price=102.30,
        quantity=100,
        show_markers=True,
        show_rectangle=True
    )
    
    # Add individual markers
    chart.add_trade_marker(
        time="2024-01-10",
        price=94.50,
        trade_type=TradeType.BUY,
        shape=MarkerShape.CIRCLE,
        text="BUY SIGNAL"
    )
    
    # Handle trade clicks
    def on_trade_click(event):
        print(f"Trade clicked: {event['trade']}")
    
    chart_group.on_trade_click(on_trade_click)
    ```
    """)

# Performance metrics
st.subheader("Trading Performance")
total_pnl = sum((trade['exit_price'] - trade['entry_price']) * trade['quantity'] for trade in sample_trades)
winning_trades = sum(1 for trade in sample_trades if trade['exit_price'] > trade['entry_price'])
total_trades = len(sample_trades)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total P&L", f"${total_pnl:.2f}", f"{'📈' if total_pnl > 0 else '📉'}")

with col2:
    win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
    st.metric("Win Rate", f"{win_rate:.1f}%", f"{winning_trades}/{total_trades}")

with col3:
    avg_return = sum(((trade['exit_price'] / trade['entry_price']) - 1) * 100 for trade in sample_trades) / total_trades if total_trades > 0 else 0
    st.metric("Avg Return", f"{avg_return:.1f}%")

with col4:
    total_volume = sum(trade['quantity'] for trade in sample_trades)
    st.metric("Total Volume", f"{total_volume:,}") 