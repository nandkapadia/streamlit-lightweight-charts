"""
Examples package for streamlit-lightweight-charts-pro.

This package contains example applications demonstrating various chart types
and features of the streamlit-lightweight-charts-pro library.
"""

import sys
from pathlib import Path


def _setup_examples_path():
    """Add the project root to Python path for examples to work from any directory."""
    # Get the project root (two levels up from this file)
    project_root = Path(__file__).parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))


# Setup path when package is imported
_setup_examples_path()


__all__ = [
    # Example files
    "legend_example",
    "tooltip_examples", 
    "pane_heights_example",
    "signal_series_example",
    "tooltip_demo",
    "signal_example",
]
