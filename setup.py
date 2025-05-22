# setup.py
from setuptools import setup, find_packages

setup(
    name="stock_screener",
    version="0.1.0",
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=[
        "aiohappyeyeballs==2.6.1"
        "aiohttp==3.11.18"
        "aiosignal==1.3.2"
        "async-timeout==5.0.1"
        "asyncio==3.4.3"
        "attrs==25.3.0"
        "beautifulsoup4==4.13.4"
        "certifi==2025.4.26"
        "charset-normalizer==3.4.2"
        "CurrencyConverter==0.18.5"
        "et_xmlfile==2.0.0"
        "exceptiongroup==1.2.2"
        "frozenlist==1.6.0"
        "idna==3.10"
        "iniconfig==2.1.0"
        "kaleido==0.2.1"
        "multidict==6.4.3"
        "narwhals==1.38.1"
        "numpy==2.2.5"
        "openpyxl==3.1.5"
        "packaging==25.0"
        "pandas==2.2.3"
        "plotly==6.0.1"
        "pluggy==1.5.0"
        "propcache==0.3.1"
        "pytest==8.3.5"
        "pytest-asyncio==0.26.0"
        "python-dateutil==2.9.0.post0"
        "pytz==2025.2"
        "requests==2.32.3"
        "six==1.17.0"
        "soupsieve==2.7"
        "tomli==2.2.1"
        "typing_extensions==4.13.2"
        "tzdata==2025.2"
        "urllib3==2.4.0"
        "yarl==1.20.0"
    ],
    entry_points={
        "console_scripts": [
            "stock-screener=stock_screener.main:main"
        ]
    }
)
