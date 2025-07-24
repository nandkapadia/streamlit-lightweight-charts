import streamlit as st

from streamlit_lightweight_charts_pro import AreaSeries, Chart
from streamlit_lightweight_charts_pro.data import SingleValueData

st.title("FitContent Debug Test")

# Create sample data
data = [
    SingleValueData("2024-01-01", 100),
    SingleValueData("2024-01-02", 105),
    SingleValueData("2024-01-03", 103),
    SingleValueData("2024-01-04", 108),
    SingleValueData("2024-01-05", 110),
    SingleValueData("2024-01-06", 107),
    SingleValueData("2024-01-07", 112),
]

# Test different configurations
st.subheader("Test 1: Default fitContent (should work)")
chart1 = Chart()
chart1.add_series(AreaSeries(data))
chart1.update_options(fit_content_on_load=True, height=400, auto_size=True)
st.plotly_chart(chart1.to_frontend_config(), use_container_width=True)

st.subheader("Test 2: Explicit fitContent with longer delay")
chart2 = Chart()
chart2.add_series(AreaSeries(data))
chart2.update_options(fit_content_on_load=True, height=400, auto_size=True)
st.plotly_chart(chart2.to_frontend_config(), use_container_width=True)

st.subheader("Test 3: No fitContent (for comparison)")
chart3 = Chart()
chart3.add_series(AreaSeries(data))
chart3.update_options(fit_content_on_load=False, height=400, auto_size=True)
st.plotly_chart(chart3.to_frontend_config(), use_container_width=True)

# Show the configuration being sent
st.subheader("Configuration Debug")
st.json(chart1.to_frontend_config())
