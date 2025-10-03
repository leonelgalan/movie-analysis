.PHONY: help init lint test refresh_data clean all

# Default target
all: lint test

# Show available targets
help:
	@echo "Available targets:"
	@echo "  make init         - Initialize project dependencies with uv sync"
	@echo "  make lint         - Run ruff linter and ty type checker"
	@echo "  make test         - Run pytest test suite"
	@echo "  make refresh_data - Refresh raw movie data"
	@echo "  make clean        - Remove generated files and caches"
	@echo "  make all          - Run lint and test (default)"

# Initialize project dependencies
init:
	uv sync

# Run linters and type checks
lint:
	uv run ruff check scripts/ tests/
	uv run ruff format --check scripts/ tests/
	uv run ty check scripts/ tests/

# Run tests
test:
	uv run pytest tests/ -v

# Refresh raw data
refresh_data:
	uv run python scripts/00_refresh_raw.py

# Clean generated files
clean:
	rm -rf results/* outputs/*
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
