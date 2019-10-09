.PHONY: lock install build test lint format
.DEFAULT_GOAL := help

lock:
	poetry lock

install:
	poetry install

build:
	poetry build

test:
	pytest

lint:
	flake8 src tests
	isort --check-only --recursive src tests
	pydocstyle src tests
	mypy src tests
	black --check src tests

format:
	isort src tests
	black src tests
