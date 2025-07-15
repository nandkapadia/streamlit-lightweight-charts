import subprocess
import time

from playwright.sync_api import sync_playwright

STREAMLIT_APP_CODE = """\
import streamlit as st
from streamlit_lightweight_charts.charts import LineChart
from streamlit_lightweight_charts.data.models import SingleValueData
chart = LineChart([SingleValueData('2023-01-01', 1.0), SingleValueData('2023-01-02', 2.0)])
st.write('Test Chart')
chart.render()
"""


def test_streamlit_chart_renders(tmp_path):
    # Write a temporary Streamlit app
    app_path = tmp_path / "app.py"
    app_path.write_text(STREAMLIT_APP_CODE)
    # Launch Streamlit
    proc = subprocess.Popen(
        ["streamlit", "run", str(app_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        # Wait for server to start
        time.sleep(10)
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto("http://localhost:8501", timeout=30000)
            # Wait for chart to render
            page.wait_for_selector("canvas", timeout=20000)
            assert page.locator("text=Test Chart").is_visible()
            assert page.locator("canvas").is_visible()
            browser.close()
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except Exception:
            proc.kill()
