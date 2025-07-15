from streamlit_lightweight_charts.charts import Chart
from streamlit_lightweight_charts.charts.series import LineSeries
from streamlit_lightweight_charts.data.models import SingleValueData
from streamlit_lightweight_charts.rendering import render_chart


def test_render_chart_serialization(monkeypatch):
    # Patch the Streamlit component to just return the config
    monkeypatch.setattr(
        "streamlit_lightweight_charts._component_func",
        lambda **kwargs: kwargs,
    )
    series = LineSeries([SingleValueData("2023-01-01", 1.0)])
    chart = Chart(series)
    result = render_chart(chart)
    assert "config" in result
    assert "charts" in result["config"]
    assert isinstance(result["config"]["charts"], list)
    assert result["config"]["charts"][0]["series"][0]["type"] == "Line"
