#!/usr/bin/env python3
"""
Method Chaining Demo - Comprehensive Example of New API.

This example demonstrates the new fluent API with method chaining for creating
interactive financial charts. It showcases various chart types, configurations,
and the builder pattern for intuitive chart creation.

The example covers:
    - Basic chart creation with method chaining
    - Multiple series types (line, candlestick, area, volume)
    - Chart configuration and styling
    - Annotation system with layers
    - Trade visualization
    - Multi-pane charts
    - Data processing and conversion

Example:
    ```python
    streamlit run examples/method_chaining_demo.py
    ```
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

from streamlit_lightweight_charts_pro import (
    SinglePaneChart, MultiPaneChart, PriceVolumeChart,
    LineSeries, CandlestickSeries, AreaSeries, HistogramSeries,
    create_chart, ChartBuilder
)
from streamlit_lightweight_charts_pro.data import (
    SingleValueData, OhlcData, HistogramData,
    create_text_annotation, create_arrow_annotation
)
from streamlit_lightweight_charts_pro.data.trade import Trade, TradeType
from examples.dataSamples import (
    get_line_data, get_candlestick_data, get_volume_data,
    get_baseline_data, get_multi_area_data_1, get_multi_area_data_2
)


def main():
    """
    Main function for the method chaining demo application.
    
    This function sets up the Streamlit interface and demonstrates
    various chart creation patterns using the new fluent API.
    """
    st.set_page_config(
        page_title="Method Chaining Demo",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("📊 Method Chaining Demo - New API")
    st.markdown("""
    This demo showcases the new fluent API with method chaining for creating
    interactive financial charts. The new API provides a more intuitive and
    readable way to build complex charts.
    """)
    
    # Sidebar for navigation
    demo_type = st.sidebar.selectbox(
        "Choose Demo Type",
        [
            "Basic Method Chaining",
            "Chart Builder Pattern",
            "Multi-Series Charts",
            "Annotations & Layers",
            "Trade Visualization",
            "Multi-Pane Charts",
            "Data Processing"
        ]
    )
    
    # Display the selected demo
    if demo_type == "Basic Method Chaining":
        basic_method_chaining_demo()
    elif demo_type == "Chart Builder Pattern":
        chart_builder_pattern_demo()
    elif demo_type == "Multi-Series Charts":
        multi_series_charts_demo()
    elif demo_type == "Annotations & Layers":
        annotations_layers_demo()
    elif demo_type == "Trade Visualization":
        trade_visualization_demo()
    elif demo_type == "Multi-Pane Charts":
        multi_pane_charts_demo()
    elif demo_type == "Data Processing":
        data_processing_demo()


def basic_method_chaining_demo():
    """
    Demonstrate basic method chaining with single series charts.
    
    This demo shows how to use method chaining for basic chart creation,
    including line charts, candlestick charts, and area charts.
    """
    st.header("🔄 Basic Method Chaining")
    st.markdown("""
    Method chaining allows you to configure charts in a fluent, readable way.
    Each method returns the chart object, enabling you to chain multiple
    configuration calls together.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Line Chart with Method Chaining")
        
        # Get sample data
        line_data = get_line_data()
        
        # Create chart with method chaining
        chart = (SinglePaneChart(series=LineSeries(data=line_data))
                .update_options(height=400, width=600)
                .add_annotation(
                    create_text_annotation(
                        "2018-12-25", 27.32, "Christmas Day",
                        color="#ff0000", background_color="rgba(255, 0, 0, 0.1)"
                    )
                )
                .add_annotation(
                    create_arrow_annotation(
                        "2018-12-31", 22.67, "Year End",
                        color="#00ff00"
                    )
                ))
        
        # Render the chart
        chart.render(key="basic_line_chart")
        
        st.markdown("""
        **Features demonstrated:**
        - Chart creation with series
        - Options configuration
        - Text and arrow annotations
        - Method chaining syntax
        """)
    
    with col2:
        st.subheader("Candlestick Chart with Method Chaining")
        
        # Get sample data
        candlestick_data = get_candlestick_data()
        
        # Create chart with method chaining
        chart = (SinglePaneChart(series=CandlestickSeries(data=candlestick_data))
                .update_options(height=400, width=600)
                .set_watermark("Sample OHLC Data")
                .set_legend(True)
                .add_annotation(
                    create_text_annotation(
                        "2022-01-19", 9.78, "Support Level",
                        color="#2196F3", background_color="rgba(33, 150, 243, 0.1)"
                    )
                ))
        
        # Render the chart
        chart.render(key="basic_candlestick_chart")
        
        st.markdown("""
        **Features demonstrated:**
        - OHLC data handling
        - Watermark and legend
        - Price level annotations
        - Candlestick styling
        """)


def chart_builder_pattern_demo():
    """
    Demonstrate the ChartBuilder pattern for fluent chart creation.
    
    This demo shows how to use the ChartBuilder class to create charts
    with an even more intuitive fluent API.
    """
    st.header("🏗️ Chart Builder Pattern")
    st.markdown("""
    The ChartBuilder pattern provides the most intuitive way to create charts.
    It uses a builder pattern where you chain method calls to configure
    the chart step by step.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Using create_chart() Function")
        
        # Get sample data
        line_data = get_line_data()
        volume_data = get_volume_data()
        
        # Create chart using the builder pattern
        chart = (create_chart()
                .add_line_series(line_data, color="#2196F3", line_width=2)
                .add_histogram_series(volume_data, color="#FF9800")
                .set_size(width=600, height=400)
                .set_auto_size(True)
                .set_watermark("Price & Volume")
                .set_legend(True)
                .add_annotation(
                    create_text_annotation(
                        "2018-12-25", 27.32, "Peak Volume",
                        color="#ff0000"
                    )
                )
                .build())
        
        # Render the chart
        chart.render(key="builder_pattern_chart")
        
        st.markdown("""
        **Features demonstrated:**
        - Multiple series (line + volume)
        - Size and auto-sizing configuration
        - Watermark and legend
        - Annotations
        - Builder pattern syntax
        """)
    
    with col2:
        st.subheader("Using ChartBuilder Class Directly")
        
        # Get sample data
        area_data = get_multi_area_data_1()
        
        # Create chart using ChartBuilder class
        builder = ChartBuilder()
        chart = (builder
                .add_area_series(area_data, color="#4CAF50", fill_color="rgba(76, 175, 80, 0.3)")
                .set_height(400)
                .set_width(600)
                .set_watermark("Area Chart")
                .add_annotation(
                    create_arrow_annotation(
                        "2019-04-08", 45.23, "Breakout",
                        color="#FF5722"
                    )
                )
                .build())
        
        # Render the chart
        chart.render(key="chart_builder_class_chart")
        
        st.markdown("""
        **Features demonstrated:**
        - Area series with fill color
        - Direct ChartBuilder usage
        - Arrow annotations
        - Custom styling
        """)


def multi_series_charts_demo():
    """
    Demonstrate multi-series charts with different chart types.
    
    This demo shows how to create charts with multiple series of
    different types, including line, area, and histogram series.
    """
    st.header("📈 Multi-Series Charts")
    st.markdown("""
    Multi-series charts allow you to display multiple data series
    on the same chart for comparison and analysis.
    """)
    
    st.subheader("Price and Volume Chart")
    
    # Get sample data
    candlestick_data = get_candlestick_data()
    volume_data = get_volume_data()
    
    # Create multi-series chart
    chart = (SinglePaneChart(series=[
        CandlestickSeries(
            data=candlestick_data,
            up_color="#4CAF50",
            down_color="#F44336",
            price_scale_id="right"
        ),
        HistogramSeries(
            data=volume_data,
            color="#FF9800",
            price_scale_id="left"
        )
    ])
    .update_options(height=500, width=800)
    .set_watermark("Price & Volume Analysis")
    .set_legend(True)
    .add_annotation(
        create_text_annotation(
            "2022-01-19", 9.78, "High Volume",
            color="#FF9800", background_color="rgba(255, 152, 0, 0.1)"
        )
    ))
    
    # Render the chart
    chart.render(key="multi_series_price_volume")
    
    st.markdown("""
    **Features demonstrated:**
    - Candlestick + Volume histogram
    - Dual price scales (left/right)
    - Color-coded up/down candles
    - Volume analysis
    """)
    
    # Second example: Multiple area series
    st.subheader("Multiple Area Series Comparison")
    
    # Get sample data
    area_data_1 = get_multi_area_data_1()
    area_data_2 = get_multi_area_data_2()
    
    # Create multi-area chart
    chart = (SinglePaneChart(series=[
        AreaSeries(
            data=area_data_1,
            color="#2196F3",
            fill_color="rgba(33, 150, 243, 0.3)",
            price_scale_id="right"
        ),
        AreaSeries(
            data=area_data_2,
            color="#FF5722",
            fill_color="rgba(255, 87, 34, 0.3)",
            price_scale_id="left"
        )
    ])
    .update_options(height=500, width=800)
    .set_watermark("Multi-Asset Comparison")
    .set_legend(True)
    .add_annotation(
        create_text_annotation(
            "2019-04-08", 45.23, "Correlation",
            color="#9C27B0", background_color="rgba(156, 39, 176, 0.1)"
        )
    ))
    
    # Render the chart
    chart.render(key="multi_series_area_comparison")
    
    st.markdown("""
    **Features demonstrated:**
    - Multiple area series
    - Dual price scales for comparison
    - Correlation analysis
    - Legend and annotations
    """)


def annotations_layers_demo():
    """
    Demonstrate the annotation system with layers and management.
    
    This demo shows how to use the annotation system to add text,
    arrows, and shapes to charts, organized in layers.
    """
    st.header("📝 Annotations & Layers")
    st.markdown("""
    The annotation system allows you to add contextual information
    to charts, organized in layers for better management.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Basic Annotations")
        
        # Get sample data
        line_data = get_line_data()
        
        # Create chart with multiple annotations
        chart = (SinglePaneChart(series=LineSeries(data=line_data))
                .update_options(height=400, width=600)
                .create_annotation_layer("events")
                .add_annotation(
                    create_text_annotation(
                        "2018-12-25", 27.32, "Christmas",
                        color="#ff0000", background_color="rgba(255, 0, 0, 0.1)"
                    ),
                    "events"
                )
                .add_annotation(
                    create_arrow_annotation(
                        "2018-12-31", 22.67, "Year End",
                        color="#00ff00"
                    ),
                    "events"
                )
                .create_annotation_layer("analysis")
                .add_annotation(
                    create_text_annotation(
                        "2018-12-27", 28.89, "Support",
                        color="#2196F3", background_color="rgba(33, 150, 243, 0.1)"
                    ),
                    "analysis"
                ))
        
        # Render the chart
        chart.render(key="annotations_basic")
        
        st.markdown("""
        **Features demonstrated:**
        - Multiple annotation layers
        - Text and arrow annotations
        - Layer organization
        - Color-coded annotations
        """)
    
    with col2:
        st.subheader("Layer Management")
        
        # Get sample data
        candlestick_data = get_candlestick_data()
        
        # Create chart with layer management
        chart = (SinglePaneChart(series=CandlestickSeries(data=candlestick_data))
                .update_options(height=400, width=600)
                .create_annotation_layer("technical")
                .create_annotation_layer("fundamental")
                .add_annotation(
                    create_text_annotation(
                        "2022-01-19", 9.78, "Support Level",
                        color="#4CAF50", background_color="rgba(76, 175, 80, 0.1)"
                    ),
                    "technical"
                )
                .add_annotation(
                    create_text_annotation(
                        "2022-01-21", 10.17, "Resistance",
                        color="#F44336", background_color="rgba(244, 67, 54, 0.1)"
                    ),
                    "technical"
                )
                .add_annotation(
                    create_arrow_annotation(
                        "2022-01-20", 9.51, "Earnings",
                        color="#FF9800"
                    ),
                    "fundamental"
                ))
        
        # Render the chart
        chart.render(key="annotations_layers")
        
        # Layer controls
        st.markdown("**Layer Controls:**")
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            if st.button("Hide Technical"):
                chart.hide_annotation_layer("technical")
        
        with col_b:
            if st.button("Hide Fundamental"):
                chart.hide_annotation_layer("fundamental")
        
        with col_c:
            if st.button("Show All"):
                chart.show_annotation_layer("technical")
                chart.show_annotation_layer("fundamental")
        
        st.markdown("""
        **Features demonstrated:**
        - Layer creation and management
        - Layer visibility controls
        - Technical vs fundamental analysis
        - Interactive layer toggling
        """)


def trade_visualization_demo():
    """
    Demonstrate trade visualization with buy/sell markers.
    
    This demo shows how to visualize trading activity with
    buy/sell markers and trade annotations.
    """
    st.header("💰 Trade Visualization")
    st.markdown("""
    Trade visualization allows you to display buy/sell signals
    and trading activity on charts for backtesting and analysis.
    """)
    
    # Get sample data
    candlestick_data = get_candlestick_data()
    
    # Create sample trades
    trades = [
        Trade(
            time="2022-01-17",
            price=10.0,
            type=TradeType.BUY,
            size=100,
            description="Entry"
        ),
        Trade(
            time="2022-01-19",
            price=9.78,
            type=TradeType.SELL,
            size=100,
            description="Exit"
        ),
        Trade(
            time="2022-01-20",
            price=9.51,
            type=TradeType.BUY,
            size=150,
            description="Re-entry"
        ),
        Trade(
            time="2022-01-21",
            price=10.17,
            type=TradeType.SELL,
            size=150,
            description="Take profit"
        )
    ]
    
    # Create chart with trade visualization
    chart = (SinglePaneChart(series=CandlestickSeries(data=candlestick_data))
            .update_options(height=500, width=800)
            .set_watermark("Trade Analysis")
            .set_legend(True)
            .add_annotation(
                create_text_annotation(
                    "2022-01-17", 10.0, "BUY 100 shares",
                    color="#4CAF50", background_color="rgba(76, 175, 80, 0.2)"
                )
            )
            .add_annotation(
                create_text_annotation(
                    "2022-01-19", 9.78, "SELL 100 shares",
                    color="#F44336", background_color="rgba(244, 67, 54, 0.2)"
                )
            )
            .add_annotation(
                create_text_annotation(
                    "2022-01-20", 9.51, "BUY 150 shares",
                    color="#4CAF50", background_color="rgba(76, 175, 80, 0.2)"
                )
            )
            .add_annotation(
                create_text_annotation(
                    "2022-01-21", 10.17, "SELL 150 shares",
                    color="#F44336", background_color="rgba(244, 67, 54, 0.2)"
                )
            ))
    
    # Render the chart
    chart.render(key="trade_visualization")
    
    # Display trade summary
    st.subheader("Trade Summary")
    trade_df = pd.DataFrame([
        {
            "Date": trade.time,
            "Type": trade.type.value,
            "Price": trade.price,
            "Size": trade.size,
            "Description": trade.description
        }
        for trade in trades
    ])
    
    st.dataframe(trade_df, use_container_width=True)
    
    # Calculate P&L
    total_pnl = 0
    for i in range(0, len(trades), 2):
        if i + 1 < len(trades):
            buy_trade = trades[i]
            sell_trade = trades[i + 1]
            pnl = (sell_trade.price - buy_trade.price) * buy_trade.size
            total_pnl += pnl
    
    st.metric("Total P&L", f"${total_pnl:.2f}")
    
    st.markdown("""
    **Features demonstrated:**
    - Trade visualization with markers
    - Buy/sell annotations
    - Trade summary table
    - P&L calculation
    - Color-coded trade types
    """)


def multi_pane_charts_demo():
    """
    Demonstrate multi-pane charts for complex analysis.
    
    This demo shows how to create multi-pane charts for
    displaying different aspects of financial data.
    """
    st.header("📊 Multi-Pane Charts")
    st.markdown("""
    Multi-pane charts allow you to display different data series
    in separate panes for detailed analysis and comparison.
    """)
    
    st.subheader("Price and Volume Multi-Pane Chart")
    
    # Get sample data
    candlestick_data = get_candlestick_data()
    volume_data = get_volume_data()
    
    # Create multi-pane chart
    chart = MultiPaneChart([
        SinglePaneChart(series=CandlestickSeries(data=candlestick_data))
        .update_options(height=300)
        .set_watermark("Price Chart"),
        
        SinglePaneChart(series=HistogramSeries(data=volume_data))
        .update_options(height=200)
        .set_watermark("Volume Chart")
    ])
    
    # Render the chart
    chart.render(key="multi_pane_price_volume")
    
    st.markdown("""
    **Features demonstrated:**
    - Multi-pane layout
    - Synchronized time scales
    - Separate price and volume analysis
    - Independent pane configuration
    """)
    
    # Second example: Multiple indicators
    st.subheader("Technical Analysis Multi-Pane Chart")
    
    # Create sample indicator data (simplified)
    indicator_data = [
        SingleValueData("2022-01-17", 50),
        SingleValueData("2022-01-18", 55),
        SingleValueData("2022-01-19", 45),
        SingleValueData("2022-01-20", 60),
        SingleValueData("2022-01-21", 65)
    ]
    
    # Create multi-pane chart with indicators
    chart = MultiPaneChart([
        SinglePaneChart(series=CandlestickSeries(data=candlestick_data))
        .update_options(height=300)
        .set_watermark("Price Chart"),
        
        SinglePaneChart(series=LineSeries(data=indicator_data))
        .update_options(height=200)
        .set_watermark("RSI Indicator")
    ])
    
    # Render the chart
    chart.render(key="multi_pane_indicators")
    
    st.markdown("""
    **Features demonstrated:**
    - Price chart with technical indicators
    - RSI indicator in separate pane
    - Synchronized navigation
    - Independent indicator scaling
    """)


def data_processing_demo():
    """
    Demonstrate data processing and conversion features.
    
    This demo shows how to work with different data formats
    and convert between them for chart creation.
    """
    st.header("🔄 Data Processing")
    st.markdown("""
    The library supports various data formats and provides
    tools for data processing and conversion.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("DataFrame to Chart")
        
        # Create sample DataFrame
        df = pd.DataFrame({
            "datetime": ["2022-01-17", "2022-01-18", "2022-01-19", "2022-01-20", "2022-01-21"],
            "open": [10.0, 9.8, 9.6, 9.9, 9.7],
            "high": [10.2, 10.1, 9.8, 10.0, 9.9],
            "low": [9.7, 9.5, 9.4, 9.6, 9.5],
            "close": [9.8, 9.6, 9.9, 9.7, 9.8],
            "volume": [1000000, 1200000, 800000, 1500000, 900000]
        })
        
        st.write("**Sample DataFrame:**")
        st.dataframe(df)
        
        # Create chart from DataFrame
        chart = (create_chart()
                .add_candlestick_series(df, up_color="#4CAF50", down_color="#F44336")
                .add_histogram_series(df, color="#FF9800")
                .set_size(width=600, height=400)
                .set_watermark("DataFrame Example")
                .build())
        
        # Render the chart
        chart.render(key="dataframe_chart")
        
        st.markdown("""
        **Features demonstrated:**
        - DataFrame input support
        - Automatic column mapping
        - Multiple series from single DataFrame
        - OHLC + Volume data
        """)
    
    with col2:
        st.subheader("Data Model Conversion")
        
        # Show data model conversion
        st.write("**Converting to Data Models:**")
        
        # Convert DataFrame to data models
        ohlc_data = [
            OhlcData(
                time=row["datetime"],
                open_=row["open"],
                high=row["high"],
                low=row["low"],
                close=row["close"]
            )
            for _, row in df.iterrows()
        ]
        
        volume_data = [
            HistogramData(
                time=row["datetime"],
                value=row["volume"]
            )
            for _, row in df.iterrows()
        ]
        
        st.write(f"Created {len(ohlc_data)} OHLC data points")
        st.write(f"Created {len(volume_data)} volume data points")
        
        # Create chart from data models
        chart = (SinglePaneChart(series=[
            CandlestickSeries(data=ohlc_data, up_color="#4CAF50", down_color="#F44336"),
            HistogramSeries(data=volume_data, color="#FF9800")
        ])
        .update_options(height=400, width=600)
        .set_watermark("Data Models Example")
        .set_legend(True))
        
        # Render the chart
        chart.render(key="data_models_chart")
        
        st.markdown("""
        **Features demonstrated:**
        - Manual data model creation
        - Type-safe data handling
        - Explicit data conversion
        - Performance optimization
        """)


if __name__ == "__main__":
    main() 