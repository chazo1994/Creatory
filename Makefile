PYTHON ?= python3

install:
	$(PYTHON) -m pip install -e .[dev]

run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

migrate:
	alembic upgrade head

downgrade:
	alembic downgrade -1

lint:
	ruff check app tests
	black --check app tests

format:
	ruff check --fix app tests
	black app tests

test:
	pytest

precommit-install:
	pre-commit install

compose-up:
	docker compose up --build

compose-up-dev:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build

compose-down:
	docker compose down
