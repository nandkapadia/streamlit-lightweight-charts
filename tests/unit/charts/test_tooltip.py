from streamlit_lightweight_charts_pro.charts import Chart
from streamlit_lightweight_charts_pro.charts.series import LineSeries
from streamlit_lightweight_charts_pro.data import SingleValueData


def test_chart_tooltip_configuration():
    """Test that tooltip configuration is accepted and serialized."""
    series = LineSeries([SingleValueData("2024-01-01", 100)])
    chart = Chart(series)
    # Simulate tooltip config
    tooltip_config = {
        "enabled": True,
        "type": "ohlc",
        "fields": [
            {"label": "Close", "valueKey": "close"},
        ],
        "position": "cursor",
    }
    chart.options.tooltip = tooltip_config
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
    assert "tooltip" in chart_obj["chart"]
    assert chart_obj["chart"]["tooltip"]["enabled"] is True


def test_chart_tooltip_rendering_structure():
    """Test that tooltip config is correctly structured for frontend."""
    series = LineSeries([SingleValueData("2024-01-01", 100)])
    chart = Chart(series)
    chart.options.tooltip = {
        "enabled": True,
        "type": "single",
        "fields": [
            {"label": "Value", "valueKey": "value"},
        ],
    }
    config = chart.to_frontend_config()
    tooltip = config["charts"][0]["chart"]["tooltip"]
    assert tooltip["type"] == "single"
    assert isinstance(tooltip["fields"], list)


def test_chart_tooltip_interactivity_flag():
    """Test that enabling/disabling tooltip is reflected in config."""
    series = LineSeries([SingleValueData("2024-01-01", 100)])
    chart = Chart(series)
    chart.options.tooltip = {"enabled": False}
    config = chart.to_frontend_config()
    assert config["charts"][0]["chart"]["tooltip"]["enabled"] is False


def test_chart_tooltip_missing_fields():
    """Test tooltip config with missing required fields."""
    series = LineSeries([SingleValueData("2024-01-01", 100)])
    chart = Chart(series)
    # Missing 'fields' and 'type'
    chart.options.tooltip = {"enabled": True}
    config = chart.to_frontend_config()
    assert config["charts"][0]["chart"]["tooltip"]["enabled"] is True
    # Should handle missing fields gracefully


def test_chart_tooltip_invalid_type():
    """Test tooltip config with invalid type value."""
    series = LineSeries([SingleValueData("2024-01-01", 100)])
    chart = Chart(series)
    chart.options.tooltip = {"enabled": True, "type": 123, "fields": []}
    config = chart.to_frontend_config()
    assert config["charts"][0]["chart"]["tooltip"]["type"] == 123


def test_chart_tooltip_empty_config():
    """Test empty tooltip config."""
    series = LineSeries([SingleValueData("2024-01-01", 100)])
    chart = Chart(series)
    chart.options.tooltip = {}
    config = chart.to_frontend_config()
    assert "tooltip" in config["charts"][0]["chart"]


def test_chart_tooltip_extreme_values():
    """Test tooltip config with extreme values."""
    series = LineSeries([SingleValueData("2024-01-01", 100)])
    chart = Chart(series)
    chart.options.tooltip = {
        "enabled": True,
        "type": "ohlc",
        "fields": [{"label": "A" * 1000, "valueKey": "close"}],
        "position": "cursor",
        "offset": {"x": 1e6, "y": -1e6},
    }
    config = chart.to_frontend_config()
    tooltip = config["charts"][0]["chart"]["tooltip"]
    assert tooltip["fields"][0]["label"] == "A" * 1000
    assert tooltip["offset"]["x"] == 1e6
    assert tooltip["offset"]["y"] == -1e6
