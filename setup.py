# setup.py
from setuptools import setup, find_packages

setup(
    name="stock_screener",
    version="0.1.0",
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=[
        "aiohttp==3.11.18",
        "async-timeout==5.0.1",
        "asyncio==3.4.3",
        "attrs==25.3.0",
        "beautifulsoup4==4.13.4",
        "CurrencyConverter==0.18.5",
        "numpy==2.2.5",
        "openpyxl==3.1.5",
        "pandas==2.2.3",
        "plotly==6.0.1",
        "pytest==8.3.5",
        "pytest-asyncio==0.26.0",
        "requests==2.32.3"
    ],
    entry_points={
        "console_scripts": [
            "stock-screener=stock_screener.main:main"
        ]
    }
)
