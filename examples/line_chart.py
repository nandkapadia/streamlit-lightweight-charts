#!/usr/bin/env python3
"""
Line Chart Example - Demonstrating the New API with Method Chaining.

This example shows how to create a simple line chart using the new fluent API
with method chaining. It demonstrates basic chart creation, configuration,
and annotation features.

The example covers:
    - Basic line chart creation
    - Method chaining for configuration
    - Annotation system
    - Data handling with pandas DataFrames
    - Chart styling and customization

Example:
    ```python
    streamlit run examples/line_chart.py
    ```
"""

import streamlit as st

from examples.dataSamples import get_dataframe_line_data, get_line_data
from streamlit_lightweight_charts_pro import LineSeries, SinglePaneChart
from streamlit_lightweight_charts_pro.data import create_text_annotation


def main():
    """
    Main function for the line chart example.

    This function demonstrates different ways to create line charts
    using the new API with method chaining.
    """
    st.set_page_config(page_title="Line Chart Example", page_icon="📈", layout="wide")

    st.title("📈 Line Chart Example - New API")
    st.markdown(
        """
    This example demonstrates how to create line charts using the new fluent API
    with method chaining. The new API provides a more intuitive and readable
    way to build charts.
    """
    )

    # Create tabs for different examples
    tab1, tab2, tab3 = st.tabs(["Basic Line Chart", "Method Chaining", "DataFrame Example"])

    with tab1:
        basic_line_chart_example()

    with tab2:
        method_chaining_example()

    with tab3:
        dataframe_example()


def basic_line_chart_example():
    """
    Demonstrate basic line chart creation.

    This example shows the traditional way to create a line chart
    and then compares it with the new method chaining approach.
    """
    st.subheader("🔄 Basic Line Chart")
    st.markdown(
        """
    Create a simple line chart with basic configuration.
    """
    )

    # Get sample data
    line_data = get_line_data()

    # Create line series
    line_series = LineSeries(data=line_data, color="#2196F3", line_width=2, price_scale_id="right")

    # Create chart
    chart = SinglePaneChart(series=line_series)

    # Render chart
    chart.render(key="basic_line_chart")

    st.markdown(
        """
    **Features:**
    - ✅ Simple line chart creation
    - ✅ Custom line color and width
    - ✅ Right price scale configuration
    - ✅ Responsive design
    """
    )


def method_chaining_example():
    """
    Demonstrate method chaining for line chart configuration.

    This example shows how to use method chaining to configure
    charts in a fluent, readable way.
    """
    st.subheader("🔗 Method Chaining Example")
    st.markdown(
        """
    Use method chaining to configure charts in a more intuitive way.
    Each method returns the chart object, enabling fluent configuration.
    """
    )

    # Get sample data
    line_data = get_line_data()

    # Create chart with method chaining
    chart = (
        SinglePaneChart(series=LineSeries(data=line_data))
        .update_options(height=400, width=600, watermark="Sample Line Data", legend=True)
        .add_annotation(
            create_text_annotation(
                "2018-12-25",
                27.32,
                "Christmas Day",
                color="#ff0000",
                background_color="rgba(255, 0, 0, 0.1)",
                font_size=12,
            )
        )
        .add_annotation(
            create_text_annotation(
                "2018-12-31",
                22.67,
                "Year End",
                color="#00ff00",
                background_color="rgba(0, 255, 0, 0.1)",
                font_size=12,
            )
        )
    )

    # Render chart
    chart.render(key="method_chaining_line_chart")

    st.markdown(
        """
    **Features demonstrated:**
    - ✅ Method chaining for configuration
    - ✅ Chart size and watermark
    - ✅ Legend display
    - ✅ Multiple annotations
    - ✅ Custom styling and colors
    - ✅ Fluent API syntax
    """
    )

    # Show the method chaining code
    st.subheader("🔍 Method Chaining Code")
    st.code(
        """
# Create chart with method chaining
chart = (SinglePaneChart(series=LineSeries(data=line_data))
        .update_options(height=400, width=600)
        .set_watermark("Sample Line Data")
        .set_legend(True)
        .add_annotation(
            create_text_annotation(
                "2018-12-25", 27.32, "Christmas Day",
                color="#ff0000",
                background_color="rgba(255, 0, 0, 0.1)"
            )
        )
        .add_annotation(
            create_text_annotation(
                "2018-12-31", 22.67, "Year End",
                color="#00ff00",
                background_color="rgba(0, 255, 0, 0.1)"
            )
        ))

# Render the chart
chart.render(key="method_chaining_line_chart")
    """,
        language="python",
    )


def dataframe_example():
    """
    Demonstrate line chart creation from pandas DataFrame.

    This example shows how to create line charts directly from
    pandas DataFrames using the new API.
    """
    st.subheader("📊 DataFrame Example")
    st.markdown(
        """
    Create line charts directly from pandas DataFrames with automatic
    column mapping and data conversion.
    """
    )

    # Get sample DataFrame
    df = get_dataframe_line_data()

    st.write("**Sample DataFrame:**")
    st.dataframe(df)

    # Create chart from DataFrame
    chart = (
        SinglePaneChart(series=LineSeries(data=df))
        .update_options(height=400, width=600)
        .set_watermark("DataFrame Line Chart")
        .set_legend(True)
        .add_annotation(
            create_text_annotation(
                "2018-12-25",
                27.32,
                "DataFrame Example",
                color="#9C27B0",
                background_color="rgba(156, 39, 176, 0.1)",
            )
        )
    )

    # Render chart
    chart.render(key="dataframe_line_chart")

    st.markdown(
        """
    **Features demonstrated:**
    - ✅ Direct DataFrame input
    - ✅ Automatic column mapping
    - ✅ Data conversion handling
    - ✅ Chart configuration
    - ✅ Annotations with DataFrame data
    """
    )

    # Show the DataFrame code
    st.subheader("🔍 DataFrame Code")
    st.code(
        """
# Get sample DataFrame
df = get_dataframe_line_data()

# Create chart from DataFrame
chart = (SinglePaneChart(series=LineSeries(data=df))
        .update_options(height=400, width=600)
        .set_watermark("DataFrame Line Chart")
        .set_legend(True)
        .add_annotation(
            create_text_annotation(
                "2018-12-25", 27.32, "DataFrame Example",
                color="#9C27B0",
                background_color="rgba(156, 39, 176, 0.1)"
            )
        ))

# Render the chart
chart.render(key="dataframe_line_chart")
    """,
        language="python",
    )


if __name__ == "__main__":
    main()
