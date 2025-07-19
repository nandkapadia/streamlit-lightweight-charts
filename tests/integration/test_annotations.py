from streamlit_lightweight_charts_pro.charts import SinglePaneChart
from streamlit_lightweight_charts_pro.charts.series import LineSeries
from streamlit_lightweight_charts_pro.data.annotation import (
    Annotation,
    AnnotationPosition,
    AnnotationType,
)
from streamlit_lightweight_charts_pro.data.models import SingleValueData


def test_chart_with_annotations():
    """Test chart with annotations using ultra-simplified API."""
    series = LineSeries([SingleValueData("2023-01-01", 1.0)], color="#ff0000")
    ann = Annotation("2023-01-01", 1.0, "Test", AnnotationType.TEXT, AnnotationPosition.ABOVE)
    chart = SinglePaneChart(series, annotations=[ann])
    config = chart.to_frontend_config()
    assert "annotations" in config
    assert isinstance(config["annotations"], list)
    assert config["annotations"][0]["text"] == "Test"
    assert "annotationLayers" in config
    assert isinstance(config["annotationLayers"], list)
