from streamlit_lightweight_charts.charts import Chart
from streamlit_lightweight_charts.charts.series import LineSeries
from streamlit_lightweight_charts.data.annotation import (
    Annotation,
    AnnotationPosition,
    AnnotationType,
)
from streamlit_lightweight_charts.data.models import SingleValueData


def test_chart_with_annotations():
    series = LineSeries([SingleValueData("2023-01-01", 1.0)])
    ann = Annotation("2023-01-01", 1.0, "Test", AnnotationType.TEXT, AnnotationPosition.ABOVE)
    chart = Chart(series, annotations=[ann])
    config = chart.to_frontend_config()
    assert "annotations" in config
    assert isinstance(config["annotations"], list)
    assert config["annotations"][0]["text"] == "Test"
    assert "annotationLayers" in config
    assert isinstance(config["annotationLayers"], list)
