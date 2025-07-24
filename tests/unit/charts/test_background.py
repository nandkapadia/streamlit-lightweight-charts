from streamlit_lightweight_charts_pro.charts import Chart
from streamlit_lightweight_charts_pro.charts.series import LineSeries
from streamlit_lightweight_charts_pro.data import SingleValueData


def test_chart_background_color():
    """Test that background color is set and serialized."""
    series = LineSeries([SingleValueData("2024-01-01", 100)])
    chart = Chart(series)
    chart.options.layout.background = {"color": "#f0f0f0"}
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
    assert chart_obj["layout"]["background"]["color"] == "#f0f0f0"


def test_chart_background_pattern():
    """Test that background pattern option is ignored and color is serialized."""
    series = LineSeries([SingleValueData("2024-01-01", 100)])
    chart = Chart(series)
    chart.options.layout.background = {"pattern": "diagonal-stripes"}
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
    # Only color is supported
    assert chart_obj["layout"]["background"]["color"] == "#FFFFFF"


def test_chart_background_missing():
    """Test chart config with no background set."""
    series = LineSeries([SingleValueData("2024-01-01", 100)])
    chart = Chart(series)
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
    assert "background" in chart_obj["layout"]


def test_chart_background_invalid_color():
    """Test chart config with invalid background color."""
    series = LineSeries([SingleValueData("2024-01-01", 100)])
    chart = Chart(series)
    chart.options.layout.background = {"color": "not-a-color"}
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
    assert chart_obj["layout"]["background"]["color"] == "not-a-color"


def test_chart_background_extreme_pattern():
    """Test chart config with extreme pattern value is ignored and color is serialized."""
    series = LineSeries([SingleValueData("2024-01-01", 100)])
    chart = Chart(series)
    chart.options.layout.background = {"pattern": "X" * 1000}
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
    assert chart_obj["layout"]["background"]["color"] == "#FFFFFF"
