# setup.py
from setuptools import setup, find_packages

setup(
    name="stock_screener",
    version="0.1.0",
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=[
        "requests>=2.28",
        "beautifulsoup4>=4.11",
        "pandas>=1.5",
        "openpyxl>=3.1",
        "plotly>=5.13"
        "python-dateutil>=2.8"
    ],
    entry_points={
        "console_scripts": [
            "stock-screener=stock_screener.main:main"
        ]
    }
)
