"""Localization option classes for streamlit-lightweight-charts."""

from dataclasses import dataclass
from typing import Callable, Optional

from streamlit_lightweight_charts_pro.charts.options.base_options import Options


@dataclass
class LocalizationOptions(Options):
    """Localization configuration for chart."""

    locale: str = "en-US"
    date_format: str = "yyyy-MM-dd"
    time_format: str = "HH:mm:ss"
    price_formatter: Optional[Callable] = None
    percentage_formatter: Optional[Callable] = None
