.PHONY: clean clean-test clean-pyc clean-build docs help install dev test lint dist venv
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"
PYTHON := python3
PIP := uv pip

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, Python, and test artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -fr {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -fr .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache
	rm -fr .ruff_cache/

lint: ## check code style with ruff
	ruff check analysis tests

format: ## format code with black and ruff
	ruff format analysis tests
	black analysis tests

test: ## run tests
	pytest --verbose

coverage: ## check code coverage
	pytest --cov=analysis --cov-report=term --cov-report=html
	$(BROWSER) htmlcov/index.html

docs: ## generate Sphinx documentation
	rm -f docs/analysis.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ analysis
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

install: clean ## install the package
	$(PIP) install -e .

dev: clean ## install the package for development
	$(PIP) install -e ".[dev]"
	$(PIP) install -r requirements_dev.txt

dist: clean ## build distribution packages
	$(PYTHON) setup.py sdist
	$(PYTHON) setup.py bdist_wheel
	ls -l dist

release: dist ## package and upload a release to PyPI
	twine upload dist/*

venv: ## create a virtual environment using uv
	uv venv
	@echo "Run 'source .venv/bin/activate' to activate the virtual environment"

run-file: ## run analysis on a specific file (use FILE=path/to/file OUTPUT=path/to/results)
	analyze --file $(FILE) --output $(OUTPUT)

run-dir: ## run analysis on a directory (use DIR=path/to/directory OUTPUT=path/to/results)
	analyze --directory $(DIR) --output $(OUTPUT)

test-unit: ## run only unit tests
	pytest -v -m unit

test-integration: ## run only integration tests
	pytest -v -m integration

test-quick: ## run tests without slow ones
	pytest -v -k "not slow"

test-file: ## run tests in a specific file (use FILE=path/to/test_file.py)
	pytest -v $(FILE)
