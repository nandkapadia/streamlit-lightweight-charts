#!/usr/bin/env python3
"""
Candlestick Chart Example - Demonstrating OHLC Data Visualization.

This example shows how to create candlestick charts using the new fluent API
with method chaining. It demonstrates OHLC data handling, candlestick styling,
and advanced chart features.

The example covers:
    - Candlestick chart creation
    - OHLC data handling
    - Method chaining for configuration
    - Candlestick styling (up/down colors)
    - Annotation system
    - Data handling with pandas DataFrames

Example:
    ```python
    streamlit run examples/candlestick_chart.py
    ```
"""

import streamlit as st

from examples.dataSamples import get_candlestick_data, get_dataframe_candlestick_data
from streamlit_lightweight_charts_pro import CandlestickSeries, SinglePaneChart, create_chart
from streamlit_lightweight_charts_pro.data import create_arrow_annotation, create_text_annotation


def main():
    """
    Main function for the candlestick chart example.

    This function demonstrates different ways to create candlestick charts
    using the new API with method chaining.
    """
    st.set_page_config(page_title="Candlestick Chart Example", page_icon="🕯️", layout="wide")

    st.title("🕯️ Candlestick Chart Example - New API")
    st.markdown(
        """
    This example demonstrates how to create candlestick charts using the new fluent API
    with method chaining. Candlestick charts are essential for technical analysis
    and price action visualization.
    """
    )

    # Create tabs for different examples
    tab1, tab2, tab3 = st.tabs(["Basic Candlestick", "Method Chaining", "DataFrame Example"])

    with tab1:
        basic_candlestick_example()

    with tab2:
        method_chaining_example()

    with tab3:
        dataframe_example()


def basic_candlestick_example():
    """
    Demonstrate basic candlestick chart creation.

    This example shows the traditional way to create a candlestick chart
    with OHLC data and basic styling.
    """
    st.subheader("🕯️ Basic Candlestick Chart")
    st.markdown(
        """
    Create a simple candlestick chart with OHLC data and basic configuration.
    """
    )

    # Get sample data
    candlestick_data = get_candlestick_data()

    # Create candlestick series
    candlestick_series = CandlestickSeries(
        data=candlestick_data,
        up_color="#4CAF50",  # Green for up candles
        down_color="#F44336",  # Red for down candles
        border_visible=False,  # Hide borders for cleaner look
        wick_up_color="#4CAF50",  # Green wicks for up candles
        wick_down_color="#F44336",  # Red wicks for down candles
        price_scale_id="right",
    )

    # Create chart with fitContent enabled
    chart = SinglePaneChart(series=candlestick_series)
    chart.update_options(fit_content_on_load=True)

    # Render chart
    chart.render(key="basic_candlestick_chart")

    st.markdown(
        """
    **Features:**
    - ✅ OHLC candlestick chart
    - ✅ Color-coded up/down candles
    - ✅ Custom wick colors
    - ✅ Right price scale configuration
    - ✅ Responsive design
    - ✅ Auto-fit content on load
    """
    )


def method_chaining_example():
    """
    Demonstrate method chaining for candlestick chart configuration.

    This example shows how to use method chaining to configure
    candlestick charts with advanced features.
    """
    st.subheader("🔗 Method Chaining Example")
    st.markdown(
        """
    Use method chaining to configure candlestick charts with advanced features
    like annotations, watermarks, and custom styling.
    """
    )

    # Get sample data
    candlestick_data = get_candlestick_data()

    # Create chart with method chaining
    chart = (
        create_chart()
        .add_candlestick_series(
            candlestick_data,
            up_color="#4CAF50",
            down_color="#F44336",
            border_visible=False,
            wick_up_color="#4CAF50",
            wick_down_color="#F44336",
        )
        .set_height(500)
        .set_width(800)
        .set_watermark("OHLC Candlestick Data")
        .set_legend(True)
        .add_annotation(
            create_text_annotation(
                "2022-01-19",
                9.78,
                "Support Level",
                color="#4CAF50",
                background_color="rgba(76, 175, 80, 0.1)",
                font_size=12,
            )
        )
        .add_annotation(
            create_text_annotation(
                "2022-01-21",
                10.17,
                "Resistance Level",
                color="#F44336",
                background_color="rgba(244, 67, 54, 0.1)",
                font_size=12,
            )
        )
        .add_annotation(create_arrow_annotation("2022-01-20", 9.51, "Breakout", color="#FF9800"))
        .build()
    )

    # Render chart
    chart.render(key="method_chaining_candlestick_chart")

    st.markdown(
        """
    **Features demonstrated:**
    - ✅ Method chaining for configuration
    - ✅ Chart size and watermark
    - ✅ Legend display
    - ✅ Support and resistance annotations
    - ✅ Arrow annotations for breakouts
    - ✅ Custom styling and colors
    - ✅ Fluent API syntax
    - ✅ Auto-fit content on load
    """
    )

    # Show the method chaining code
    st.subheader("🔍 Method Chaining Code")
    st.code(
        """
# Create chart with method chaining
chart = (SinglePaneChart(series=CandlestickSeries(
    data=candlestick_data,
    up_color="#4CAF50",
    down_color="#F44336",
    border_visible=False,
    wick_up_color="#4CAF50",
    wick_down_color="#F44336"
))
.update_options(height=500, width=800)
.set_watermark("OHLC Candlestick Data")
.set_legend(True)
.add_annotation(
    create_text_annotation(
        "2022-01-19", 9.78, "Support Level",
        color="#4CAF50",
        background_color="rgba(76, 175, 80, 0.1)"
    )
)
.add_annotation(
    create_text_annotation(
        "2022-01-21", 10.17, "Resistance Level",
        color="#F44336",
        background_color="rgba(244, 67, 54, 0.1)"
    )
)
.add_annotation(
    create_arrow_annotation(
        "2022-01-20", 9.51, "Breakout",
        color="#FF9800"
    )
))

# Render the chart
chart.render(key="method_chaining_candlestick_chart")
    """,
        language="python",
    )


def dataframe_example():
    """
    Demonstrate candlestick chart creation from pandas DataFrame.

    This example shows how to create candlestick charts directly from
    pandas DataFrames with OHLC columns.
    """
    st.subheader("📊 DataFrame Example")
    st.markdown(
        """
    Create candlestick charts directly from pandas DataFrames with OHLC columns.
    The library automatically maps the columns to the appropriate data structure.
    """
    )

    # Get sample DataFrame
    df = get_dataframe_candlestick_data()

    st.write("**Sample OHLC DataFrame:**")
    st.dataframe(df)

    # Create chart from DataFrame
    chart = (
        create_chart()
        .add_candlestick_series(
            df,
            up_color="#4CAF50",
            down_color="#F44336",
            border_visible=False,
            wick_up_color="#4CAF50",
            wick_down_color="#F44336",
        )
        .set_height(500)
        .set_width(800)
        .set_watermark("DataFrame OHLC Chart")
        .set_legend(True)
        .add_annotation(
            create_text_annotation(
                "2022-01-19",
                9.78,
                "DataFrame Example",
                color="#9C27B0",
                background_color="rgba(156, 39, 176, 0.1)",
            )
        )
        .build()
    )

    # Render chart
    chart.render(key="dataframe_candlestick_chart")

    st.markdown(
        """
    **Features demonstrated:**
    - ✅ Direct DataFrame input with OHLC columns
    - ✅ Automatic column mapping (open, high, low, close)
    - ✅ Data conversion handling
    - ✅ Chart configuration
    - ✅ Annotations with DataFrame data
    - ✅ Candlestick styling
    """
    )

    # Show the DataFrame code
    st.subheader("🔍 DataFrame Code")
    st.code(
        """
# Get sample DataFrame
df = get_dataframe_candlestick_data()

# Create chart from DataFrame
chart = (SinglePaneChart(series=CandlestickSeries(
    data=df,
    up_color="#4CAF50",
    down_color="#F44336",
    border_visible=False,
    wick_up_color="#4CAF50",
    wick_down_color="#F44336"
))
.update_options(height=500, width=800)
.set_watermark("DataFrame OHLC Chart")
.set_legend(True)
.add_annotation(
    create_text_annotation(
        "2022-01-19", 9.78, "DataFrame Example",
        color="#9C27B0",
        background_color="rgba(156, 39, 176, 0.1)"
    )
))

# Render the chart
chart.render(key="dataframe_candlestick_chart")
    """,
        language="python",
    )

    # Show DataFrame structure
    st.subheader("📋 DataFrame Structure")
    st.markdown(
        """
    The DataFrame should have the following columns:
    - `datetime` or `time`: Time column
    - `open`: Opening price
    - `high`: Highest price
    - `low`: Lowest price
    - `close`: Closing price
    """
    )

    st.code(
        """
# Example DataFrame structure
df = pd.DataFrame({
    "datetime": ["2022-01-17", "2022-01-18", "2022-01-19"],
    "open": [10.0, 9.8, 9.6],
    "high": [10.2, 10.1, 9.8],
    "low": [9.7, 9.5, 9.4],
    "close": [9.8, 9.6, 9.9]
})
    """,
        language="python",
    )


if __name__ == "__main__":
    main()
