from importlib.metadata import entry_points
from setuptools import setup, find_packages

setup (
    name="FileAnalysis",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pandas>=1.3.0",
        "numpy>=1.20.0",
        "openpyxl>=3.0.7",
        "xlrd>=2.0.1"
        "argparse>=1.4.0",
    ],
    entry_points={
        "console_scripts": [
            "commando=analysis.cli:main",
        ],
    },
    # Metadatos
    author="Alejandro Lopez Monzon",
    author_email="alejandro@kreaker.dev",
    description="File Analysis for DataFill on SKU tables",
    keywords="analysis datafill data skus",
    url="https://github.com/alexlm78/FileAnalysis",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
