"""Chart rendering functionality for streamlit-lightweight-charts."""

import os
from typing import List, Dict, Any, Optional
import streamlit.components.v1 as components

_COMPONENT_NAME = "streamlit_lightweight_charts"
_RELEASE = True

# Get the absolute path to the component's build directory
parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "frontend", "build")

if not _RELEASE:
    _component_func = components.declare_component(
        _COMPONENT_NAME,
        url="http://localhost:3001",
    )
else:
    _component_func = components.declare_component(
        _COMPONENT_NAME,
        path=build_dir
    )


def render_chart(charts: List[Dict[str, Any]], key: Optional[str] = None) -> Any:
    """
    Render lightweight charts using Streamlit component.
    
    Args:
        charts: List of chart configurations
        key: Unique key for the Streamlit component
        
    Returns:
        Component render result
    """
    return _component_func(
        charts=charts,
        key=key
    )