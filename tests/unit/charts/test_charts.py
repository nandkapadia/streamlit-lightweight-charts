"""Tests for the ultra-simplified chart API."""

from streamlit_lightweight_charts_pro.charts import Chart, LineSeries
from streamlit_lightweight_charts_pro.data import SingleValueData


def test_single_pane_chart_to_frontend_config():
    data = [SingleValueData("2024-01-01", 100)]
    chart = Chart(series=LineSeries(data))
    config = chart.to_frontend_config()
    assert isinstance(config, dict)
    chart_obj = config["charts"][0]
    assert isinstance(chart_obj["chart"], dict)
    if "timeScale" in chart_obj["chart"]:
        assert isinstance(chart_obj["chart"]["timeScale"], dict)
    if "layout" in chart_obj["chart"]:
        assert isinstance(chart_obj["chart"]["layout"], dict)
    if "PriceScaleOptionss" in chart_obj["chart"]:
        assert isinstance(chart_obj["chart"]["PriceScaleOptionss"], dict)


# Additional merged tests from test_single_pane_chart.py


def test_to_frontend_config_with_annotations():
    data = [SingleValueData("2024-01-01", 100)]
    chart = Chart(series=LineSeries(data))
    # Add a dummy annotation if needed
    config = chart.to_frontend_config()
    assert "annotations" in config["charts"][0]
    assert isinstance(config["charts"][0]["annotations"], dict)
    assert "layers" in config["charts"][0]["annotations"]


def test_to_frontend_config_multiple_series():
    data1 = [SingleValueData("2024-01-01", 100)]
    data2 = [SingleValueData("2024-01-02", 200)]
    chart = Chart(series=[LineSeries(data1), LineSeries(data2)])
    config = chart.to_frontend_config()
    assert "charts" in config
    assert len(config["charts"][0]["series"]) == 2
    assert isinstance(config["charts"][0]["series"][0], dict)
    assert isinstance(config["charts"][0]["series"][1], dict)


def test_to_frontend_config_detailed():
    data = [SingleValueData("2024-01-01", 100)]
    chart = Chart(series=LineSeries(data))
    chart.options.height = 400
    chart.options.width = 600
    config = chart.to_frontend_config()
    chart_config = config["charts"][0]
    assert chart_config["chart"]["height"] == 400
    assert chart_config["chart"]["width"] == 600
    assert isinstance(chart_config["chart"], dict)
    if "timeScale" in chart_config["chart"]:
        assert isinstance(chart_config["chart"]["timeScale"], dict)
    if "layout" in chart_config["chart"]:
        assert isinstance(chart_config["chart"]["layout"], dict)
    if "PriceScaleOptionss" in chart_config["chart"]:
        assert isinstance(chart_config["chart"]["PriceScaleOptionss"], dict)


# ...add any other unique or non-duplicate tests from test_single_pane_chart.py as needed...
