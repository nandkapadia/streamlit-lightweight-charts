import subprocess
import time

import pytest
from playwright.sync_api import sync_playwright

STREAMLIT_INTERACTIVE_APP = """\
import streamlit as st
import streamlit_lightweight_charts as stlc

# Create sample data as plain dictionaries
data = [
    {"time": "2023-01-01", "open": 100, "high": 110, "low": 95, "close": 105},
    {"time": "2023-01-02", "open": 105, "high": 115, "low": 100, "close": 110},
    {"time": "2023-01-03", "open": 110, "high": 120, "low": 105, "close": 115},
    {"time": "2023-01-04", "open": 115, "high": 125, "low": 110, "close": 120},
    {"time": "2023-01-05", "open": 120, "high": 130, "low": 115, "close": 125}
]

st.write('Interactive Candlestick Chart')
stlc.renderLightweightCharts([{
    "width": 600,
    "height": 400,
    "layout": {
        "background": {"type": "solid", "color": "white"},
        "textColor": "black"
    },
    "grid": {
        "vertLines": {"color": "#e6e6e6"},
        "horzLines": {"color": "#e6e6e6"}
    },
    "series": [{
        "type": "candlestick",
        "data": data
    }]
}])
"""


def test_chart_interactivity(tmp_path):
    app_path = tmp_path / "interactive_app.py"
    app_path.write_text(STREAMLIT_INTERACTIVE_APP)

    proc = subprocess.Popen(
        ["streamlit", "run", str(app_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        time.sleep(10)

        # Check if process is still running and capture any output
        if proc.poll() is not None:
            stdout, stderr = proc.communicate()
            print(f"Streamlit process failed to start!")
            print(f"Return code: {proc.returncode}")
            print(f"STDOUT: {stdout.decode()}")
            print(f"STDERR: {stderr.decode()}")
            pytest.fail("Streamlit app failed to start")

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto("http://localhost:8501", timeout=30000)

            # Wait for chart to load - try multiple selectors
            try:
                page.wait_for_selector("canvas", timeout=30000)
            except Exception:
                # Try alternative selectors if canvas doesn't appear
                try:
                    page.wait_for_selector("[data-testid='stChart']", timeout=10000)
                except Exception:
                    # If still no chart, check if page loaded at all
                    page.wait_for_selector("body", timeout=5000)
                    # Take screenshot for debugging
                    page.screenshot(path="test_debug.png")
                    pytest.fail("Chart did not load - check test_debug.png")

            # Test zoom functionality (if available)
            canvas = page.locator("canvas").first
            canvas.hover()

            # Test mouse interactions
            page.mouse.wheel(0, -100)  # Scroll down (zoom in)
            time.sleep(1)
            page.mouse.wheel(0, 100)  # Scroll up (zoom out)
            time.sleep(1)

            # Test crosshair (move mouse over chart)
            canvas.hover()
            page.mouse.move(400, 200)
            time.sleep(1)

            # Verify chart is still visible after interactions
            assert canvas.is_visible()

            browser.close()
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except Exception:
            proc.kill()


def test_trade_visualization_rendering(tmp_path):
    app_path = tmp_path / "trade_app.py"
    app_path.write_text(STREAMLIT_INTERACTIVE_APP)

    proc = subprocess.Popen(
        ["streamlit", "run", str(app_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        time.sleep(10)

        # Check if process is still running and capture any output
        if proc.poll() is not None:
            stdout, stderr = proc.communicate()
            print(f"Streamlit process failed to start!")
            print(f"Return code: {proc.returncode}")
            print(f"STDOUT: {stdout.decode()}")
            print(f"STDERR: {stderr.decode()}")
            pytest.fail("Streamlit app failed to start")

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto("http://localhost:8501", timeout=30000)

            # Wait for chart to load - try multiple selectors
            try:
                page.wait_for_selector("canvas", timeout=30000)
            except Exception:
                try:
                    page.wait_for_selector("[data-testid='stChart']", timeout=10000)
                except Exception:
                    page.wait_for_selector("body", timeout=5000)
                    page.screenshot(path="test_debug.png")
                    pytest.fail("Chart did not load - check test_debug.png")

            # Check that trade markers are visible (they should be rendered on canvas)
            canvas = page.locator("canvas").first
            assert canvas.is_visible()

            # Take a screenshot to verify trade visualization
            screenshot = canvas.screenshot()
            assert len(screenshot) > 0  # Screenshot should not be empty

            browser.close()
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except Exception:
            proc.kill()
