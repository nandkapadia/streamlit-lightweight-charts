import setuptools

with open("README_ENHANCED.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="streamlit-lightweight-charts-enhanced",
    version="2.0.0",
    author="Enhanced by AI Assistant",
    author_email="",
    description="Enhanced Streamlit component for TradingView's lightweight-charts with full features",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/streamlit-lightweight-charts",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Streamlit",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Office/Business :: Financial :: Investment"
    ],
    keywords=[
        "streamlit",
        "lightweight-charts",
        "tradingview",
        "charts",
        "financial",
        "trading",
        "candlestick",
        "technical-analysis",
        "visualization"
    ],
    python_requires=">=3.7",
    install_requires=[
        "streamlit>=1.0",
    ],
    extras_require={
        "dev": [
            "pandas>=1.0",
            "numpy>=1.19",
        ],
        "examples": [
            "pandas>=1.0",
            "numpy>=1.19",
        ]
    },
    project_urls={
        "Bug Reports": "https://github.com/yourusername/streamlit-lightweight-charts/issues",
        "Source": "https://github.com/yourusername/streamlit-lightweight-charts",
        "Documentation": "https://github.com/yourusername/streamlit-lightweight-charts/blob/main/README_ENHANCED.md",
    },
)
