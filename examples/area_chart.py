#!/usr/bin/env python3
"""
Area Chart Example - Demonstrating Area Chart Visualization.

This example shows how to create area charts using the new fluent API
with method chaining. It demonstrates area chart styling, fill colors,
and gradient effects.

The example covers:
    - Area chart creation
    - Method chaining for configuration
    - Area styling (fill colors, gradients)
    - Data handling with pandas DataFrames
    - Chart customization

Example:
    ```python
    streamlit run examples/area_chart.py
    ```
"""

import streamlit as st

from examples.dataSamples import get_dataframe_line_data, get_line_data
from streamlit_lightweight_charts_pro import AreaSeries, SinglePaneChart, create_chart
from streamlit_lightweight_charts_pro.data import create_text_annotation


def main():
    """
    Main function for the area chart example.

    This function demonstrates different ways to create area charts
    using the new API with method chaining.
    """
    st.set_page_config(page_title="Area Chart Example", page_icon="📊", layout="wide")

    st.title("📊 Area Chart Example - New API")
    st.markdown(
        """
    This example demonstrates how to create area charts using the new fluent API
    with method chaining. Area charts are great for showing volume, trends,
    and filled visualizations.
    """
    )

    # Create tabs for different examples
    tab1, tab2, tab3 = st.tabs(["Basic Area Chart", "Method Chaining", "DataFrame Example"])

    with tab1:
        basic_area_chart_example()

    with tab2:
        method_chaining_example()

    with tab3:
        dataframe_example()


def basic_area_chart_example():
    """
    Demonstrate basic area chart creation.

    This example shows how to create a simple area chart with
    basic styling and configuration.
    """
    st.subheader("📊 Basic Area Chart")
    st.markdown(
        """
    Create a simple area chart with basic configuration and styling.
    """
    )

    # Get sample data
    area_data = get_line_data()

    # Create area series
    area_series = AreaSeries(
        data=area_data,
        line_color="#2196F3",
        top_color="rgba(33, 150, 243, 0.4)",
        bottom_color="rgba(33, 150, 243, 0.0)",
        line_width=2,
        price_scale_id="right",
    )

    # Create chart with fitContent enabled
    chart = SinglePaneChart(series=area_series)
    chart.update_options(fit_content_on_load=True)

    # Render chart
    chart.render(key="basic_area_chart")

    st.markdown(
        """
    **Features:**
    - ✅ Filled area chart
    - ✅ Gradient fill effect
    - ✅ Custom line color and width
    - ✅ Right price scale configuration
    - ✅ Responsive design
    - ✅ Auto-fit content on load
    """
    )


def method_chaining_example():
    """
    Demonstrate method chaining for area chart configuration.

    This example shows how to use method chaining to configure
    area charts with advanced features.
    """
    st.subheader("🔗 Method Chaining Example")
    st.markdown(
        """
    Use method chaining to configure area charts with advanced features
    like annotations, watermarks, and custom styling.
    """
    )

    # Get sample data
    area_data = get_line_data()

    # Create chart with method chaining
    chart = (
        SinglePaneChart(
            series=AreaSeries(
                data=area_data,
                line_color="#4CAF50",
                top_color="rgba(76, 175, 80, 0.6)",
                bottom_color="rgba(76, 175, 80, 0.0)",
                line_width=3,
            )
        )
        .update_options(height=400, width=600, watermark="Sample Area Data", legend=True, fit_content_on_load=True)
        .add_annotation(
            create_text_annotation(
                "2018-12-25",
                27.32,
                "Peak Value",
                color="#4CAF50",
                background_color="rgba(76, 175, 80, 0.1)",
                font_size=12,
            )
        )
        .add_annotation(
            create_text_annotation(
                "2018-12-31",
                22.67,
                "Low Point",
                color="#F44336",
                background_color="rgba(244, 67, 54, 0.1)",
                font_size=12,
            )
        )
    )

    # Render chart
    chart.render(key="method_chaining_area_chart")

    st.markdown(
        """
    **Features demonstrated:**
    - ✅ Method chaining for configuration
    - ✅ Chart size and watermark
    - ✅ Legend display
    - ✅ Peak and low point annotations
    - ✅ Custom area styling with gradients
    - ✅ Fluent API syntax
    - ✅ Auto-fit content on load
    """
    )

    # Show the method chaining code
    st.subheader("🔍 Method Chaining Code")
    st.code(
        """
# Create chart with method chaining
chart = (SinglePaneChart(series=AreaSeries(
    data=area_data,
    line_color="#4CAF50",
    top_color="rgba(76, 175, 80, 0.6)",
    bottom_color="rgba(76, 175, 80, 0.0)",
    line_width=3
))
.update_options(height=400, width=600, watermark="Sample Area Data", legend=True, fit_content_on_load=True)
.add_annotation(
    create_text_annotation(
        "2018-12-25", 27.32, "Peak Value",
        color="#4CAF50",
        background_color="rgba(76, 175, 80, 0.1)"
    )
)
.add_annotation(
    create_text_annotation(
        "2018-12-31", 22.67, "Low Point",
        color="#F44336",
        background_color="rgba(244, 67, 54, 0.1)"
    )
))

# Render the chart
chart.render(key="method_chaining_area_chart")
    """,
        language="python",
    )


def dataframe_example():
    """
    Demonstrate area chart creation from pandas DataFrame.

    This example shows how to create area charts directly from
    pandas DataFrames using the new API.
    """
    st.subheader("📊 DataFrame Example")
    st.markdown(
        """
    Create area charts directly from pandas DataFrames with automatic
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
        .add_area_series(
            df,
            column_mapping={"time": "datetime", "value": "value"},
            line_color="#FF9800",
            top_color="rgba(255, 152, 0, 0.5)",
            bottom_color="rgba(255, 152, 0, 0.0)",
            line_width=2,
        )
        .set_height(400)
        .set_width(600)
        .set_watermark("DataFrame Area Chart")
        .set_fit_content_on_load(True)
        .build()
    )

    # Render chart
    chart.render(key="dataframe_area_chart")

    st.markdown(
        """
    **Features demonstrated:**
    - ✅ DataFrame data handling
    - ✅ Automatic column mapping
    - ✅ create_chart() builder pattern
    - ✅ Custom area styling
    - ✅ Watermark and sizing
    - ✅ Fluent API with builder pattern
    - ✅ Auto-fit content on load
    """
    )


if __name__ == "__main__":
    main()
