[private]
default:
  @just --list --unsorted

[group('lifecycle')]
install:
  uv sync

[group('lifecycle')]
update:
  uv sync --upgrade

[group('lifecycle')]
clean:
    rm -rf .venv .pytest_cache .mypy_cache .ruff_cache .coverage htmlcov
    find . -type d -name "__pycache__" -exec rm -r {} +

[group('lifecycle')]
fresh: clean install

[group('check')] 
lint:
	uv run ruff check --fix .

[group('check')] 
format: 
	uv run ruff format .

[group('check')] 
typing:
	uv run basedpyright

[group('check')] 
test: 
	uv run pytest

[group('check')] 
all-dev: lint format typing

[group('git')]
pre-commit:
  uv run pre-commit

