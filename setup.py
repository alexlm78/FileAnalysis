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
        "xlrd>=2.0.1",
        "argparse>=1.4.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.10.0",
            "pytest-xdist>=3.3.0",
            "black>=23.0.0",
            "ruff>=0.1.0",
            "coverage>=7.0.0",
            "twine>=4.0.0",
            "sphinx>=7.0.0",
            "sphinx_rtd_theme>=1.0.0",
            "build>=0.10.0",
            "wheel>=0.40.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "analyze=analysis.cli:main",
        ],
    },
    # Metadatos
    author="Alejandro Lopez Monzon",
    author_email="alejandro@kreaker.dev",
    description="Data filling from generated files (databases dumps)",
    keywords="analysis datafill data skus",
    url="https://github.com/alexlm78/FileAnalysis",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
