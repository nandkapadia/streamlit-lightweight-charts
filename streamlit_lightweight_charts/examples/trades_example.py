"""Example demonstrating trade visualization on candlestick charts."""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from streamlit_lightweight_charts import (
    CandlestickChart, ChartOptions, LayoutOptions, Background,
    CandlestickSeriesOptions, Trade, TradeType, TradeVisualization,
    TradeVisualizationOptions
)


@st.cache_data
def generate_stock_data(days: int = 60) -> pd.DataFrame:
    """Generate sample OHLC data."""
    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
    
    # Generate realistic price movement
    prices = [100]
    for i in range(1, days):
        change = np.random.randn() * 2
        prices.append(max(prices[-1] + change, 50))
    
    df = pd.DataFrame(index=dates)
    df['close'] = prices
    df['open'] = df['close'].shift(1).fillna(df['close'].iloc[0]) * (1 + np.random.randn(days) * 0.002)
    df['high'] = df[['open', 'close']].max(axis=1) * (1 + np.abs(np.random.randn(days) * 0.01))
    df['low'] = df[['open', 'close']].min(axis=1) * (1 - np.abs(np.random.randn(days) * 0.01))
    
    return df


def generate_sample_trades(df: pd.DataFrame) -> list:
    """Generate sample trades based on the data."""
    trades = []
    
    # Trade 1: Profitable long trade
    trades.append(Trade(
        entry_time=df.index[10],
        entry_price=df['close'].iloc[10],
        exit_time=df.index[15],
        exit_price=df['close'].iloc[15] * 1.05,  # 5% profit
        quantity=100,
        trade_type=TradeType.LONG,
        id="T001",
        notes="Trend following trade"
    ))
    
    # Trade 2: Loss-making short trade
    trades.append(Trade(
        entry_time=df.index[20],
        entry_price=df['high'].iloc[20],
        exit_time=df.index[23],
        exit_price=df['high'].iloc[23] * 1.02,  # 2% loss on short
        quantity=50,
        trade_type=TradeType.SHORT,
        id="T002",
        notes="Failed breakdown"
    ))
    
    # Trade 3: Profitable short trade
    trades.append(Trade(
        entry_time=df.index[30],
        entry_price=df['high'].iloc[30],
        exit_time=df.index[35],
        exit_price=df['low'].iloc[35],  # Profitable short
        quantity=75,
        trade_type=TradeType.SHORT,
        id="T003"
    ))
    
    # Trade 4: Small profit long trade
    trades.append(Trade(
        entry_time=df.index[40],
        entry_price=df['low'].iloc[40],
        exit_time=df.index[45],
        exit_price=df['close'].iloc[45] * 1.02,  # 2% profit
        quantity=200,
        trade_type=TradeType.LONG,
        id="T004"
    ))
    
    return trades


def main():
    st.title("Trade Visualization Example")
    st.markdown("This example demonstrates different ways to visualize trades on candlestick charts.")
    
    # Generate data and trades
    df = generate_stock_data()
    trades = generate_sample_trades(df)
    
    # Chart options
    chart_options = ChartOptions(
        height=500,
        layout=LayoutOptions(
            background=Background.solid('#ffffff'),
            text_color='#333'
        )
    )
    
    # Visualization style selector
    st.sidebar.header("Trade Visualization Options")
    
    viz_style = st.sidebar.selectbox(
        "Visualization Style",
        [
            TradeVisualization.MARKERS,
            TradeVisualization.RECTANGLES,
            TradeVisualization.BOTH,
            TradeVisualization.LINES,
            TradeVisualization.ARROWS,
            TradeVisualization.ZONES
        ],
        index=2,  # Default to BOTH
        format_func=lambda x: x.value.title()
    )
    
    # Create trade visualization options
    trade_options = TradeVisualizationOptions(style=viz_style)
    
    # Additional options based on style
    if viz_style in [TradeVisualization.MARKERS, TradeVisualization.BOTH]:
        st.sidebar.subheader("Marker Options")
        trade_options.show_pnl_in_markers = st.sidebar.checkbox("Show P&L in markers", True)
        trade_options.marker_size = st.sidebar.slider("Marker size", 10, 30, 20)
    
    if viz_style in [TradeVisualization.RECTANGLES, TradeVisualization.BOTH]:
        st.sidebar.subheader("Rectangle Options")
        trade_options.rectangle_fill_opacity = st.sidebar.slider(
            "Rectangle opacity", 0.0, 0.5, 0.2
        )
        trade_options.rectangle_border_width = st.sidebar.slider(
            "Border width", 1, 5, 1
        )
    
    if viz_style == TradeVisualization.ZONES:
        st.sidebar.subheader("Zone Options")
        trade_options.zone_opacity = st.sidebar.slider(
            "Zone opacity", 0.0, 0.3, 0.1
        )
        trade_options.zone_extend_bars = st.sidebar.slider(
            "Extend bars", 0, 5, 2
        )
    
    # Annotation options
    st.sidebar.subheader("Annotation Options")
    trade_options.show_trade_id = st.sidebar.checkbox("Show Trade ID", True)
    trade_options.show_quantity = st.sidebar.checkbox("Show Quantity", True)
    trade_options.show_trade_type = st.sidebar.checkbox("Show Trade Type", False)
    
    # Create candlestick chart with trades
    from streamlit_lightweight_charts.utils import df_to_ohlc_data
    ohlc_data = df_to_ohlc_data(df)
    
    chart = CandlestickChart(
        data=ohlc_data,
        options=chart_options,
        series_options=CandlestickSeriesOptions(
            up_color='#26a69a',
            down_color='#ef5350'
        ),
        trades=trades,
        trade_visualization_options=trade_options
    )
    
    # Display chart
    st.subheader(f"Trade Visualization: {viz_style.value.title()}")
    chart.render(key=f'trades_{viz_style.value}')
    
    # Show trade summary
    st.subheader("Trade Summary")
    
    # Create summary DataFrame
    trade_summary = []
    for trade in trades:
        trade_summary.append({
            'ID': trade.id,
            'Type': trade.trade_type.value.upper(),
            'Entry Time': pd.Timestamp(trade.entry_time).strftime('%Y-%m-%d'),
            'Entry Price': f"${trade.entry_price:.2f}",
            'Exit Time': pd.Timestamp(trade.exit_time).strftime('%Y-%m-%d'),
            'Exit Price': f"${trade.exit_price:.2f}",
            'Quantity': trade.quantity,
            'P&L': f"${trade.pnl:.2f}",
            'P&L %': f"{trade.pnl_percentage:+.1f}%",
            'Result': '✅ Profit' if trade.is_profitable else '❌ Loss'
        })
    
    summary_df = pd.DataFrame(trade_summary)
    st.dataframe(summary_df, use_container_width=True)
    
    # Calculate overall statistics
    total_trades = len(trades)
    profitable_trades = sum(1 for t in trades if t.is_profitable)
    total_pnl = sum(t.pnl for t in trades)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Trades", total_trades)
    with col2:
        st.metric("Win Rate", f"{(profitable_trades/total_trades)*100:.1f}%")
    with col3:
        st.metric("Total P&L", f"${total_pnl:.2f}")
    with col4:
        st.metric("Avg P&L per Trade", f"${total_pnl/total_trades:.2f}")
    
    # Code example
    st.subheader("Code Example")
    
    st.code("""
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
    ),
    # ... more trades
]

# Create visualization options
trade_options = TradeVisualizationOptions(
    style=TradeVisualization.BOTH,  # or MARKERS, RECTANGLES, LINES, ARROWS, ZONES
    show_pnl_in_markers=True,
    rectangle_fill_opacity=0.2
)

# Create chart with trades
chart = CandlestickChart(
    data=ohlc_data,
    trades=trades,
    trade_visualization_options=trade_options
)

# Or add trades later
chart.add_trades(trades, trade_options)
    """)
    
    # Different visualization styles explanation
    st.subheader("Visualization Styles")
    
    st.markdown("""
    ### Available Styles:
    
    1. **Markers**: Entry/exit points with arrows
       - Up arrows for long entries, down for shorts
       - Colors indicate profit/loss
       - Optional P&L display
    
    2. **Rectangles**: Box from entry to exit
       - Height shows price range
       - Width shows time duration
       - Color indicates profit/loss
    
    3. **Both**: Combines markers and rectangles
       - Best for detailed analysis
       - Shows all trade information
    
    4. **Lines**: Simple lines connecting entry/exit
       - Clean, minimal visualization
       - Good for many trades
    
    5. **Arrows**: Directional arrows
       - Shows trade direction clearly
       - P&L percentage on arrow
    
    6. **Zones**: Colored background zones
       - Emphasizes trade periods
       - Can extend beyond trade duration
       - Different colors for long/short
    """)


if __name__ == "__main__":
    main()