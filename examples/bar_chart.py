#!/usr/bin/env python3
"""
Bar Chart Example - Demonstrating Bar Chart Visualization.

This example shows how to create bar charts using the new fluent API
with method chaining. It demonstrates bar chart styling, base lines,
and data visualization.

The example covers:
    - Bar chart creation
    - Method chaining for configuration
    - Bar styling (colors, base lines)
    - Data handling with pandas DataFrames
    - Chart customization

Example:
    ```python
    streamlit run examples/bar_chart.py
    ```
"""

import streamlit as st

from examples.dataSamples import get_dataframe_line_data, get_line_data
from streamlit_lightweight_charts_pro import BarSeries, SinglePaneChart, create_chart
from streamlit_lightweight_charts_pro.data import create_text_annotation


def main():
    """
    Main function for the bar chart example.

    This function demonstrates different ways to create bar charts
    using the new API with method chaining.
    """
    st.set_page_config(page_title="Bar Chart Example", page_icon="📊", layout="wide")

    st.title("📊 Bar Chart Example - New API")
    st.markdown(
        """
    This example demonstrates how to create bar charts using the new fluent API
    with method chaining. Bar charts are great for showing discrete values,
    volumes, and comparisons.
    """
    )

    # Create tabs for different examples
    tab1, tab2, tab3 = st.tabs(["Basic Bar Chart", "Method Chaining", "DataFrame Example"])

    with tab1:
        basic_bar_chart_example()

    with tab2:
        method_chaining_example()

    with tab3:
        dataframe_example()


def basic_bar_chart_example():
    """
    Demonstrate basic bar chart creation.

    This example shows how to create a simple bar chart with
    basic styling and configuration.
    """
    st.subheader("📊 Basic Bar Chart")
    st.markdown(
        """
    Create a simple bar chart with basic configuration and styling.
    """
    )

    # Get sample data
    bar_data = get_line_data()

    # Create bar series
    bar_series = BarSeries(data=bar_data, color="#26a69a", base=0, price_scale_id="right")

    # Create chart with fitContent enabled
    chart = SinglePaneChart(series=bar_series)
    chart.update_options(fit_content_on_load=True)

    # Render chart
    chart.render(key="basic_bar_chart")

    st.markdown(
        """
    **Features:**
    - ✅ Vertical bar chart
    - ✅ Custom bar color
    - ✅ Base line at zero
    - ✅ Right price scale configuration
    - ✅ Responsive design
    - ✅ Auto-fit content on load
    """
    )


def method_chaining_example():
    """
    Demonstrate method chaining for bar chart configuration.

    This example shows how to use method chaining to configure
    bar charts with advanced features.
    """
    st.subheader("🔗 Method Chaining Example")
    st.markdown(
        """
    Use method chaining to configure bar charts with advanced features
    like annotations, watermarks, and custom styling.
    """
    )

    # Get sample data
    bar_data = get_line_data()

    # Create chart with method chaining
    chart = (
        SinglePaneChart(
            series=BarSeries(
                data=bar_data,
                color="#4CAF50",
                base=20,  # Set base line at 20
                border_color="#2E7D32",
            )
        )
        .update_options(height=400, width=600, watermark="Sample Bar Data", legend=True, fit_content_on_load=True)
        .add_annotation(
            create_text_annotation(
                "2018-12-25",
                27.32,
                "Peak Bar",
                color="#4CAF50",
                background_color="rgba(76, 175, 80, 0.1)",
                font_size=12,
            )
        )
        .add_annotation(
            create_text_annotation(
                "2018-12-31",
                22.67,
                "Low Bar",
                color="#F44336",
                background_color="rgba(244, 67, 54, 0.1)",
                font_size=12,
            )
        )
    )

    # Render chart
    chart.render(key="method_chaining_bar_chart")

    st.markdown(
        """
    **Features demonstrated:**
    - ✅ Method chaining for configuration
    - ✅ Chart size and watermark
    - ✅ Legend display
    - ✅ Peak and low bar annotations
    - ✅ Custom base line (20 instead of 0)
    - ✅ Border color styling
    - ✅ Fluent API syntax
    - ✅ Auto-fit content on load
    """
    )

    # Show the method chaining code
    st.subheader("🔍 Method Chaining Code")
    st.code(
        """
# Create chart with method chaining
chart = (SinglePaneChart(series=BarSeries(
    data=bar_data,
    color="#4CAF50",
    base=20,  # Set base line at 20
    border_color="#2E7D32"
))
.update_options(height=400, width=600, watermark="Sample Bar Data", legend=True)
.add_annotation(
    create_text_annotation(
        "2018-12-25", 27.32, "Peak Bar",
        color="#4CAF50",
        background_color="rgba(76, 175, 80, 0.1)"
    )
)
.add_annotation(
    create_text_annotation(
        "2018-12-31", 22.67, "Low Bar",
        color="#F44336",
        background_color="rgba(244, 67, 54, 0.1)"
    )
))

# Render the chart
chart.render(key="method_chaining_bar_chart")
    """,
        language="python",
    )


def dataframe_example():
    """
    Demonstrate bar chart creation from pandas DataFrame.

    This example shows how to create bar charts directly from
    pandas DataFrames using the new API.
    """
    st.subheader("📊 DataFrame Example")
    st.markdown(
        """
    Create bar charts directly from pandas DataFrames with automatic
    column mapping and data conversion.
    """
    )

    # Get sample DataFrame
    df = get_dataframe_line_data()

    st.write("**Sample DataFrame:**")
    st.dataframe(df)

    # Create chart using create_chart() function
    chart = (
        create_chart()
        .add_bar_series(df, column_mapping={"time": "datetime", "value": "value"}, color="#FF9800")
        .set_height(400)
        .set_width(600)
        .set_watermark("DataFrame Bar Chart")
        .set_fit_content_on_load(True)
        .build()
    )

    # Render chart
    chart.render(key="dataframe_bar_chart")

    st.markdown(
        """
    **Features demonstrated:**
    - ✅ DataFrame data handling
    - ✅ Automatic column mapping
    - ✅ create_chart() builder pattern
    - ✅ Custom bar styling
    - ✅ Watermark and sizing
    - ✅ Fluent API with builder pattern
    - ✅ Auto-fit content on load
    """
    )

    # Show different base line examples
    st.subheader("🎯 Different Base Line Examples")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Base at 0:**")
        chart1 = create_chart().add_bar_series(df, color="#2196F3", base=0).set_height(200).set_fit_content_on_load(True).build()
        chart1.render(key="bar_base_0")

    with col2:
        st.write("**Base at 25:**")
        chart2 = create_chart().add_bar_series(df, color="#9C27B0", base=25).set_height(200).set_fit_content_on_load(True).build()
        chart2.render(key="bar_base_25")


if __name__ == "__main__":
    main()
