# setup.py
#pip install . install the required packages to run the code
# pip install .[dev] install the extra packages, here to run the tests
# the classifiers are used to describe the package, they are not used by pip, but by PyPI
# the entry_points are used to define the command line interface of the package
from setuptools import setup, find_packages

setup(
    name="stock_screener",
    version="1.0.0",
    packages=find_packages(exclude=["tests", "tests.*"]),
    python_requires=">=3.9",
    install_requires=[
        "aiohttp>=3.12",
        "attrs>=25.0",
        "beautifulsoup4>=4.13",
        "CurrencyConverter>=0.18",
        "numpy>=2.2",
        "openpyxl>=3.1",
        "pandas>=2.2",
        "plotly>=6.0",
        "requests>=2.32"
    ],
    extras_require={
        "dev": [
            "pytest>=8.3",
            "pytest-asyncio>=0.26"
        ]
    },
    classifiers=[
        "Intended Audience :: Personal",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Financial Analysis",
    ],
    entry_points={
        "console_scripts": [
            "stock-screener=stock_screener.main:main"
        ]
    }
)
