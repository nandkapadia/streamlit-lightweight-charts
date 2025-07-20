"""
Component initialization for streamlit-lightweight-charts.

This module handles the initialization of the Streamlit component to avoid
circular import issues. It manages the component function that renders
charts in Streamlit applications.

The module supports both development and production modes:
    - Development mode: Uses local development server for hot reloading
    - Production mode: Uses built frontend files for deployment

The component function is initialized once when the module is first imported
and can be retrieved using get_component_func() for use throughout the application.

Example:
    ```python
    from streamlit_lightweight_charts_pro.component import get_component_func

    component_func = get_component_func()
    if component_func:
        component_func(config=chart_config, key="my_chart")
    ```

Raises:
    ImportError: If Streamlit components module cannot be imported
    FileNotFoundError: If frontend build directory is missing in production mode
"""

from pathlib import Path
from typing import Any, Callable, Optional

from streamlit_lightweight_charts_pro.logging_config import get_logger

# Component function for Streamlit integration - initialized once
_component_func: Optional[Callable[..., Any]] = None

# Initialize logger
logger = get_logger("component")

# Determine if we're in a release build or development
# Set to True for production builds, False for development
_RELEASE = True


def get_component_func() -> Optional[Callable[..., Any]]:
    """
    Get the Streamlit component function for rendering charts.

    This function returns the initialized component function that can be used
    to render charts in Streamlit applications. The component function is
    initialized once when the module is first imported.

    The component function takes chart configuration and renders it using
    the React frontend component. It handles the communication between
    Python and the JavaScript frontend.

    Returns:
        Optional[Callable[..., Any]]: The component function if successfully
            initialized, None otherwise. The function signature is:
            component_func(config: Dict[str, Any], key: Optional[str] = None) -> Any

    Raises:
        RuntimeError: If component initialization fails (handled internally)

    Example:
        ```python
        component_func = get_component_func()
        if component_func:
            result = component_func(config=chart_config, key="my_chart")
        else:
            logger.warning("Component function not available")
        ```
    """
    return _component_func


# Initialize component function based on environment
if _RELEASE:
    # Production mode: Use built frontend files from the build directory
    frontend_dir = Path(__file__).parent / "frontend" / "build"
    if frontend_dir.exists():
        try:
            import streamlit.components.v1 as components

            # Declare the component with the built frontend files
            _component_func = components.declare_component(
                "streamlit-lightweight-charts-pro",
                path=str(frontend_dir),
            )
        except Exception as e:
            # Log warning if component initialization fails
            logger.warning(f"Could not load frontend component: {e}")
            _component_func = None
    else:
        # Log warning if build directory is missing
        logger.warning(f"Frontend build directory not found at {frontend_dir}")
        _component_func = None
else:
    # Development mode: Use local development server for hot reloading
    # This allows for real-time development without rebuilding
    try:
        import streamlit.components.v1 as components

        # Declare the component with development server URL
        _component_func = components.declare_component(
            "streamlit-lightweight-charts-pro",
            url="http://localhost:3001",
        )
    except Exception as e:
        # Log warning if development component initialization fails
        logger.warning(f"Could not load development component: {e}")
        _component_func = None
