from streamlit_lightweight_charts.charts import (
    AreaChart,
    BarChart,
    BaselineChart,
    CandlestickChart,
    Chart,
    HistogramChart,
    LineChart,
    MultiPaneChart,
)
from streamlit_lightweight_charts.charts.series import AreaSeries, LineSeries
from streamlit_lightweight_charts.data.models import (
    BaselineData,
    HistogramData,
    OhlcData,
    SingleValueData,
)


def test_chart_to_frontend_config():
    series = LineSeries([SingleValueData("2023-01-01", 1.0)])
    chart = Chart(series)
    config = chart.to_frontend_config()
    assert "chart" in config
    assert "series" in config
    assert isinstance(config["series"], list)


def test_multipane_chart():
    s1 = LineSeries([SingleValueData("2023-01-01", 1.0)])
    s2 = AreaSeries([SingleValueData("2023-01-01", 2.0)])
    c1 = Chart(s1)
    c2 = Chart(s2)
    mp = MultiPaneChart([c1, c2])
    config = mp.to_frontend_config()
    assert isinstance(config, list)
    assert len(config) == 2


def test_specialized_charts():
    line = LineChart([SingleValueData("2023-01-01", 1.0)])
    area = AreaChart([SingleValueData("2023-01-01", 2.0)])
    bar = BarChart([OhlcData("2023-01-01", 1, 2, 0, 1.5)])
    candle = CandlestickChart([OhlcData("2023-01-01", 1, 2, 0, 1.5)])
    hist = HistogramChart([HistogramData("2023-01-01", 42.0)])
    base = BaselineChart([BaselineData("2023-01-01", 123.4)])
    for chart in [line, area, bar, candle, hist, base]:
        config = chart.to_frontend_config()
        assert "chart" in config
        assert "series" in config
