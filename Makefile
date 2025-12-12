.PHONY = python3

.PHONY: lint
lint:
	ruff format .
	ruff check --fix
	ruff check .
	mypy .

.PHONY: testcover
testcover:
	pytest --cov --cov-report=term-missing

.PHONY: setup
setup:
	curl -LsSf https://astral.sh/uv/install.sh | sh
	uv sync
