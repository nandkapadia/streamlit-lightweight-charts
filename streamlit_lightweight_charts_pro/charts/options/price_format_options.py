from dataclasses import dataclass
from typing import Optional

from streamlit_lightweight_charts_pro.charts.options.base_options import Options


@dataclass
class PriceFormatOptions(Options):
    """
    Encapsulates price formatting options for a series, matching TradingView's API.

    Attributes:
        type (str): Format type ("price", "volume", "percent", "custom").
        precision (int): Number of decimal places.
        min_move (float): Minimum price movement.
        formatter (Optional[str]): Optional custom formatter (string name or function reference).
    """

    type: str = "price"
    precision: int = 2
    min_move: float = 0.01
    formatter: Optional[str] = None

    def __post_init__(self):
        """Post-initialization validation."""
        super().__post_init__()

        if self.type not in {"price", "volume", "percent", "custom"}:
            raise ValueError(
                f"Invalid type: {self.type!r}. Must be one of 'price', 'volume', "
                f"'percent', 'custom'."
            )
        if not isinstance(self.precision, int) or self.precision < 0:
            raise ValueError(f"precision must be a non-negative integer, got {self.precision}")
        if not isinstance(self.min_move, (int, float)) or self.min_move <= 0:
            raise ValueError(f"min_move must be a positive number, got {self.min_move}")
