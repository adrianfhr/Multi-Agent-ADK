.PHONY: install lint test test-unit test-integration eval run

install:
	pip install -e .[dev]

lint:
	ruff check src/ tests/ main.py
	ruff format --check src/ tests/ main.py

format:
	ruff check --fix src/ tests/ main.py
	ruff format src/ tests/ main.py

test-unit:
	pytest tests/unit/ -v

test-integration:
	pytest tests/integration/ -v

test:
	pytest tests/ -v

eval:
	python evaluations/eval_smart_info.py

run:
	python main.py
