PYTHON ?= python3

install:
	$(PYTHON) -m pip install -e .[dev]

run:
	uvicorn creatory_core.main:app --host 0.0.0.0 --port 8000 --reload

run-worker:
	python -m creatory_core.worker

migrate:
	alembic upgrade head

downgrade:
	alembic downgrade -1

lint:
	ruff check creatory_core tests
	black --check creatory_core tests
	cd creatory_studio && npm run lint

format:
	ruff check --fix creatory_core tests
	black creatory_core tests

test:
	$(PYTHON) -m pytest

precommit-install:
	pre-commit install

compose-up:
	docker compose -f infra/docker-compose.yml up --build

compose-up-dev:
	docker compose -f infra/docker-compose.yml -f infra/docker-compose.dev.yml up --build

compose-down:
	docker compose -f infra/docker-compose.yml down

frontend-install:
	cd creatory_studio && npm install

frontend-dev:
	cd creatory_studio && npm run dev

frontend-build:
	cd creatory_studio && npm run build
