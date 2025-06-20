.DEFAULT_GOAL := help

install:  ## Install dependencies from pyproject.toml
	uv sync

lint:  ## Run Ruff to check code
	uv run ruff check --fix .

format:  ## Format code using Ruff
	uv run ruff format .

typecheck: ## Typecheck using basedpyright
	uv run basedpyright

test:  ## Run tests using pytest
	uv run pytest

all-dev: lint format typecheck ## Run lint format and typecheck

clean:  ## Remove __pycache__ and .pyc files
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.py[co]" -delete

help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## ' Makefile | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-18s\033[0m %s\n", $$1, $$2}'

.PHONY: install lint format test all-dev clean help
