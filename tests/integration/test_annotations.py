from streamlit_lightweight_charts_pro.charts import Chart
from streamlit_lightweight_charts_pro.charts.series import LineSeries
from streamlit_lightweight_charts_pro.data import SingleValueData
from streamlit_lightweight_charts_pro.data.annotation import (
    Annotation,
    AnnotationPosition,
    AnnotationType,
)


def test_chart_with_annotations():
    """Test chart with annotations using ultra-simplified API."""
    series = LineSeries([SingleValueData("2023-01-01", 1.0)], color="#ff0000")
    ann = Annotation("2023-01-01", 1.0, "Test", AnnotationType.TEXT, AnnotationPosition.ABOVE)
    chart = Chart(series, annotations=[ann])
    config = chart.to_frontend_config()

    # The Chart returns a structure with "charts" array containing the chart config
    assert "charts" in config
    assert len(config["charts"]) == 1

    chart_config = config["charts"][0]
    assert "annotations" in chart_config
    assert "layers" in chart_config["annotations"]
    assert "default" in chart_config["annotations"]["layers"]

    # Check that the annotation layer contains the expected annotation
    annotation_layer = chart_config["annotations"]["layers"]["default"]
    assert annotation_layer["name"] == "default"
    assert annotation_layer["visible"] is True
    assert annotation_layer["opacity"] == 1.0

    # Check the actual annotation data
    annotation_data = annotation_layer["annotations"][0]
    assert annotation_data["text"] == "Test"
    assert annotation_data["type"] == "text"
    assert annotation_data["position"] == "above"
