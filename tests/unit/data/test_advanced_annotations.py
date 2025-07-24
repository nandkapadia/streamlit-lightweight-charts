import pytest

from streamlit_lightweight_charts_pro.data.annotation import (
    Annotation,
    AnnotationLayer,
    AnnotationManager,
    create_text_annotation,
)


def test_annotation_layer_filter_by_time_range():
    """Test filtering annotations by time range."""
    ann1 = create_text_annotation("2024-01-01", 100, "A")
    ann2 = create_text_annotation("2024-01-05", 105, "B")
    layer = AnnotationLayer(name="test", annotations=[ann1, ann2])
    filtered = layer.filter_by_time_range("2024-01-02", "2024-01-10")
    assert ann2 in filtered
    assert ann1 not in filtered


def test_annotation_layer_filter_by_price_range():
    """Test filtering annotations by price range."""
    ann1 = create_text_annotation("2024-01-01", 100, "A")
    ann2 = create_text_annotation("2024-01-01", 200, "B")
    layer = AnnotationLayer(name="test", annotations=[ann1, ann2])
    filtered = layer.filter_by_price_range(150, 250)
    assert ann2 in filtered
    assert ann1 not in filtered


def test_annotation_manager_layer_management():
    """Test complex layer management in AnnotationManager."""
    manager = AnnotationManager()
    manager.create_layer("layer1")
    manager.create_layer("layer2")
    ann = create_text_annotation("2024-01-01", 100, "A")
    manager.add_annotation(ann, "layer1")
    assert "layer1" in manager.layers
    assert len(manager.layers["layer1"].annotations) == 1
    manager.hide_layer("layer1")
    assert manager.layers["layer1"].visible is False
    manager.show_layer("layer1")
    assert manager.layers["layer1"].visible is True
    manager.clear_layer("layer1")
    assert len(manager.layers["layer1"].annotations) == 0
    manager.remove_layer("layer1")
    assert "layer1" not in manager.layers


def test_annotation_layer_serialization_edge_case():
    """Test serialization of empty annotation layer."""
    layer = AnnotationLayer(name="empty", annotations=[])
    d = layer.to_dict()
    assert d["name"] == "empty"
    assert d["annotations"] == []


def test_annotation_invalid_data():
    """Test annotation with invalid data types."""
    with pytest.raises(Exception):
        Annotation(None, None, None)


def test_annotation_manager_empty():
    """Test AnnotationManager with no layers."""
    manager = AnnotationManager()
    assert manager.layers == {}
    assert manager.get_all_annotations() == []


def test_annotation_extreme_values():
    """Test annotation with extreme text and price values."""
    ann = create_text_annotation("2024-01-01", 1e12, "A" * 1000)
    layer = AnnotationLayer(name="extreme", annotations=[ann])
    d = layer.to_dict()
    assert d["annotations"][0]["price"] == 1e12
    assert d["annotations"][0]["text"] == "A" * 1000
