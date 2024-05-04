include .env

DOCKER_COMPOSE = docker-compose
PYTHON = poetry run python
UVICORN = poetry run uvicorn

dev:
	$(DOCKER_COMPOSE) up db -d
	$(UVICORN) app.main:app --host 0.0.0.0 --port 8000 --reload

test:
	$(PYTHON) -m pytest -v

docker-up:
	$(DOCKER_COMPOSE) up -d

docker-db:
	$(DOCKER_COMPOSE) up db -d
