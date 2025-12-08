.PHONY = python3

.PHONY: lint
lint:
	ruff format .
	ruff check --fix
	ruff check .
	mypy .