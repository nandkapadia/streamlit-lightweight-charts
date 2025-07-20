"""Tests for the ultra-simplified chart API."""

from streamlit_lightweight_charts_pro.charts import (
    MultiPaneChart,
    SinglePaneChart,
)
from streamlit_lightweight_charts_pro.charts.series import (
    AreaSeries,
    BarSeries,
    BaselineSeries,
    CandlestickSeries,
    HistogramSeries,
    LineSeries,
)
from streamlit_lightweight_charts_pro.data.models import (
    BaselineData,
    HistogramData,
    OhlcData,
    SingleValueData,
)


def test_single_pane_chart_to_frontend_config():
    """Test SinglePaneChart with ultra-simplified API."""
    series = LineSeries([SingleValueData("2023-01-01", 1.0)])
    chart = SinglePaneChart(series)
    config = chart.to_frontend_config()
    assert "charts" in config
    assert len(config["charts"]) == 1
    assert "chart" in config["charts"][0]
    assert "series" in config["charts"][0]
    assert isinstance(config["charts"][0]["series"], list)


def test_multipane_chart():
    """Test MultiPaneChart with ultra-simplified API."""
    s1 = LineSeries([SingleValueData("2023-01-01", 1.0)])
    s2 = AreaSeries([SingleValueData("2023-01-01", 2.0)])
    c1 = SinglePaneChart(s1)
    c2 = SinglePaneChart(s2)
    mp = MultiPaneChart([c1, c2])
    config = mp.to_frontend_config()
    assert isinstance(config, dict)
    assert "charts" in config
    assert len(config["charts"]) == 2


def test_ultra_simplified_series_charts():
    """Test all series types with ultra-simplified API."""
    # Test each series type with SinglePaneChart
    line_series = LineSeries([SingleValueData("2023-01-01", 1.0)])
    line_chart = SinglePaneChart(line_series)

    area_series = AreaSeries([SingleValueData("2023-01-01", 2.0)])
    area_chart = SinglePaneChart(area_series)

    bar_series = BarSeries([OhlcData("2023-01-01", 1, 2, 0, 1.5)])
    bar_chart = SinglePaneChart(bar_series)

    candle_series = CandlestickSeries([OhlcData("2023-01-01", 1, 2, 0, 1.5)])
    candle_chart = SinglePaneChart(candle_series)

    hist_series = HistogramSeries([HistogramData("2023-01-01", 42.0)])
    hist_chart = SinglePaneChart(hist_series)

    base_series = BaselineSeries([BaselineData("2023-01-01", 123.4)])
    base_chart = SinglePaneChart(base_series)

    # Test that all charts generate valid frontend config
    for chart in [line_chart, area_chart, bar_chart, candle_chart, hist_chart, base_chart]:
        config = chart.to_frontend_config()
        assert "charts" in config
        assert len(config["charts"]) == 1
        assert "chart" in config["charts"][0]
        assert "series" in config["charts"][0]


def test_series_with_styling():
    """Test series with direct styling parameters."""
    from streamlit_lightweight_charts_pro.type_definitions.enums import LineStyle

    # Test LineSeries with styling
    line_series = LineSeries(
        [SingleValueData("2023-01-01", 1.0)],
        color="#ff0000",
        line_width=3,
        line_style=LineStyle.DASHED,
    )
    line_chart = SinglePaneChart(line_series)
    config = line_chart.to_frontend_config()

    # Test that styling is included in the config
    series_config = config["charts"][0]["series"][0]
    assert series_config["options"]["color"] == "#ff0000"
    assert series_config["options"]["lineWidth"] == 3


def test_multiple_series_in_chart():
    """Test SinglePaneChart with multiple series."""
    line_series = LineSeries([SingleValueData("2023-01-01", 1.0)], color="#ff0000")
    area_series = AreaSeries([SingleValueData("2023-01-01", 2.0)], top_color="rgba(0,255,0,0.5)")

    chart = SinglePaneChart([line_series, area_series])
    config = chart.to_frontend_config()

    # Test that both series are included
    assert len(config["charts"][0]["series"]) == 2
    assert config["charts"][0]["series"][0]["options"]["color"] == "#ff0000"
    assert config["charts"][0]["series"][1]["options"]["topColor"] == "rgba(0,255,0,0.5)"


def test_chart_with_dataframe():
    """Test chart creation with DataFrame data."""
    import pandas as pd

    # Create test DataFrame
    df = pd.DataFrame({"datetime": ["2023-01-01", "2023-01-02"], "close": [100.0, 105.0]})

    # Create series with DataFrame
    series = LineSeries(df, color="#ff0000")
    chart = SinglePaneChart(series)
    config = chart.to_frontend_config()

    # Test that data was converted correctly
    assert len(config["charts"][0]["series"][0]["data"]) == 2
    assert config["charts"][0]["series"][0]["data"][0]["value"] == 100.0
    assert config["charts"][0]["series"][0]["data"][1]["value"] == 105.0
