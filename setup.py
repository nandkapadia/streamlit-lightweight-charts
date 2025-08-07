import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="streamlit_lightweight_charts_pro",
    version="0.1.0",
    author="Nand Kapadia",
    author_email="nand.kapadia@gmail.com",
    description="Enhanced Streamlit component for TradingView's lightweight-charts with ultra-simplified API and performance optimizations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nandkapadia/streamlit_lightweight_charts_pro",
    packages=setuptools.find_packages(include=["streamlit_lightweight_charts_pro*"]),
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
        "Topic :: Office/Business :: Financial :: Investment",
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
        "visualization",
        "pro",
        "enhanced",
    ],
    python_requires=">=3.7",
    install_requires=[
        "streamlit>=1.0",
        "pandas>=1.0",
        "numpy>=1.19",
    ],
    extras_require={
        "dev": [
            "pandas>=1.0",
            "numpy>=1.19",
        ],
        "examples": [
            "pandas>=1.0",
            "numpy>=1.19",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/nandkapadia/streamlit_lightweight_charts_pro/issues",
        "Source": "https://github.com/nandkapadia/streamlit_lightweight_charts_pro",
        "Documentation": "https://github.com/nandkapadia/streamlit_lightweight_charts_pro/blob/main/README.md",
    },
)
