from streamlit_lightweight_charts_pro.charts import Chart
from streamlit_lightweight_charts_pro.charts.series import BarSeries, LineSeries
from streamlit_lightweight_charts_pro.data import SingleValueData


def test_chart_legend_flag():
    """Test that legend flag is set and serialized."""
    series = LineSeries([SingleValueData("2024-01-01", 100)])
    chart = Chart(series)
    chart.options.legend = True
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
    assert chart_obj["chart"]["legend"] is True


def test_chart_legend_multiple_series():
    """Test legend with multiple series types."""
    series1 = LineSeries([SingleValueData("2024-01-01", 100)], color="#ff0000")
    series2 = BarSeries([SingleValueData("2024-01-01", 50)], color="#00ff00")
    chart = Chart([series1, series2])
    chart.options.legend = True
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
    assert chart_obj["chart"]["legend"] is True
    assert len(config["charts"][0]["series"]) == 2


def test_chart_legend_missing_flag():
    """Test chart config with no legend flag set."""
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
    assert config["charts"][0]["chart"].get("legend") in (None, False)


def test_chart_legend_invalid_type():
    """Test legend config with invalid type value."""
    series = LineSeries([SingleValueData("2024-01-01", 100)])
    chart = Chart(series)
    chart.options.legend = "yes"
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
    assert config["charts"][0]["chart"]["legend"] == "yes"


def test_chart_legend_empty_series():
    """Test legend config with empty series list."""
    chart = Chart([])
    chart.options.legend = True
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
    assert config["charts"][0]["chart"]["legend"] is True
    assert config["charts"][0]["series"] == []


def test_chart_legend_extreme_options():
    """Test legend config with extreme options (should not error)."""
    series = LineSeries([SingleValueData("2024-01-01", 100)])
    chart = Chart(series)
    chart.options.legend = True
    # No legend_position tested
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
    assert config["charts"][0]["chart"]["legend"] is True
