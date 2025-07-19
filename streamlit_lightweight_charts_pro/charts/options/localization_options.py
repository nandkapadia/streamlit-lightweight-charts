"""Localization option classes for streamlit-lightweight-charts."""

from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional


@dataclass
class LocalizationOptions:
    """Localization configuration for chart."""

    locale: str = "en-US"
    date_format: str = "yyyy-MM-dd"
    time_format: str = "HH:mm:ss"
    price_formatter: Optional[Callable] = None
    percentage_formatter: Optional[Callable] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        result = {
            "locale": self.locale,
            "dateFormat": self.date_format,
            "timeFormat": self.time_format,
        }

        if self.price_formatter is not None:
            result["priceFormatter"] = self.price_formatter

        if self.percentage_formatter is not None:
            result["percentageFormatter"] = self.percentage_formatter

        return result
