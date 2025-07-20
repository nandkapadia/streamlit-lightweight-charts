#!/usr/bin/env python3
"""
Histogram Chart Example - Demonstrating Histogram Visualization.

This example shows how to create histogram charts using the new fluent API
with method chaining. It demonstrates histogram styling, base lines,
and volume data visualization.

The example covers:
    - Histogram chart creation
    - Method chaining for configuration
    - Histogram styling (colors, base lines)
    - Data handling with pandas DataFrames
    - Chart customization

Example:
    ```python
    streamlit run examples/histogram_chart.py
    ```
"""

import streamlit as st

from examples.dataSamples import get_dataframe_volume_data, get_volume_data
from streamlit_lightweight_charts_pro import HistogramSeries, SinglePaneChart, create_chart
from streamlit_lightweight_charts_pro.data import create_text_annotation


def main():
    """
    Main function for the histogram chart example.

    This function demonstrates different ways to create histogram charts
    using the new API with method chaining.
    """
    st.set_page_config(page_title="Histogram Chart Example", page_icon="📊", layout="wide")

    st.title("📊 Histogram Chart Example - New API")
    st.markdown(
        """
    This example demonstrates how to create histogram charts using the new fluent API
    with method chaining. Histogram charts are great for showing volume data,
    distributions, and frequency counts.
    """
    )

    # Create tabs for different examples
    tab1, tab2, tab3 = st.tabs(["Basic Histogram", "Method Chaining", "DataFrame Example"])

    with tab1:
        basic_histogram_example()

    with tab2:
        method_chaining_example()

    with tab3:
        dataframe_example()


def basic_histogram_example():
    """
    Demonstrate basic histogram chart creation.

    This example shows how to create a simple histogram chart with
    basic styling and configuration.
    """
    st.subheader("📊 Basic Histogram Chart")
    st.markdown(
        """
    Create a simple histogram chart with basic configuration and styling.
    """
    )

    # Get sample data
    histogram_data = get_volume_data()

    # Create histogram series
    histogram_series = HistogramSeries(
        data=histogram_data, color="#2196F3", base=0, price_scale_id="right"
    )

    # Create chart with fitContent enabled
    chart = SinglePaneChart(series=histogram_series)
    chart.update_options(fit_content_on_load=True)

    # Render chart
    chart.render(key="basic_histogram_chart")

    st.markdown(
        """
    **Features:**
    - ✅ Volume histogram chart
    - ✅ Custom bar color
    - ✅ Base line at zero
    - ✅ Right price scale configuration
    - ✅ Responsive design
    - ✅ Auto-fit content on load
    """
    )


def method_chaining_example():
    """
    Demonstrate method chaining for histogram chart configuration.

    This example shows how to use method chaining to configure
    histogram charts with advanced features.
    """
    st.subheader("🔗 Method Chaining Example")
    st.markdown(
        """
    Use method chaining to configure histogram charts with advanced features
    like annotations, watermarks, and custom styling.
    """
    )

    # Get sample data
    histogram_data = get_volume_data()

    # Create chart with method chaining
    chart = (
        SinglePaneChart(
            series=HistogramSeries(
                data=histogram_data,
                color="#4CAF50",
                base=5,  # Set base line at 5
            )
        )
        .update_options(height=400, width=600, watermark="Sample Volume Data", legend=True, fit_content_on_load=True)
        .add_annotation(
            create_text_annotation(
                "2022-01-19",
                20,
                "High Volume",
                color="#4CAF50",
                background_color="rgba(76, 175, 80, 0.1)",
                font_size=12,
            )
        )
        .add_annotation(
            create_text_annotation(
                "2022-01-21",
                3,
                "Low Volume",
                color="#F44336",
                background_color="rgba(244, 67, 54, 0.1)",
                font_size=12,
            )
        )
    )

    # Render chart
    chart.render(key="method_chaining_histogram_chart")

    st.markdown(
        """
    **Features demonstrated:**
    - ✅ Method chaining for configuration
    - ✅ Chart size and watermark
    - ✅ Legend display
    - ✅ High and low volume annotations
    - ✅ Custom base line (5 instead of 0)
    - ✅ Fluent API syntax
    - ✅ Auto-fit content on load
    """
    )

    # Show the method chaining code
    st.subheader("🔍 Method Chaining Code")
    st.code(
        """
# Create chart with method chaining
chart = (SinglePaneChart(series=HistogramSeries(
    data=histogram_data,
    color="#4CAF50",
    base=5,  # Set base line at 5
))
.update_options(height=400, width=600, watermark="Sample Volume Data", legend=True)
.add_annotation(
    create_text_annotation(
        "2022-01-19", 20, "High Volume",
        color="#4CAF50",
        background_color="rgba(76, 175, 80, 0.1)"
    )
)
.add_annotation(
    create_text_annotation(
        "2022-01-21", 3, "Low Volume",
        color="#F44336",
        background_color="rgba(244, 67, 54, 0.1)"
    )
))

# Render the chart
chart.render(key="method_chaining_histogram_chart")
    """,
        language="python",
    )


def dataframe_example():
    """
    Demonstrate histogram chart creation from pandas DataFrame.

    This example shows how to create histogram charts directly from
    pandas DataFrames using the new API.
    """
    st.subheader("📊 DataFrame Example")
    st.markdown(
        """
    Create histogram charts directly from pandas DataFrames with automatic
    column mapping and data conversion.
    """
    )

    # Get sample DataFrame
    df = get_dataframe_volume_data()

    st.write("**Sample DataFrame:**")
    st.dataframe(df)

    # Create chart using create_chart() function
    chart = (
        create_chart()
        .add_histogram_series(
            df, column_mapping={"time": "datetime", "value": "value"}, color="#9C27B0"
        )
        .set_height(400)
        .set_width(600)
        .set_watermark("DataFrame Histogram Chart")
        .set_fit_content_on_load(True)
        .build()
    )

    # Render chart
    chart.render(key="dataframe_histogram_chart")

    st.markdown(
        """
    **Features demonstrated:**
    - ✅ DataFrame data handling
    - ✅ Automatic column mapping
    - ✅ create_chart() builder pattern
    - ✅ Custom histogram styling
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
        chart1 = (
            create_chart().add_histogram_series(df, color="#2196F3", base=0).set_height(200).set_fit_content_on_load(True).build()
        )
        chart1.render(key="histogram_base_0")

    with col2:
        st.write("**Base at 10:**")
        chart2 = (
            create_chart()
            .add_histogram_series(df, color="#9C27B0", base=10)
            .set_height(200)
            .set_fit_content_on_load(True)
            .build()
        )
        chart2.render(key="histogram_base_10")


if __name__ == "__main__":
    main()
