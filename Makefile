COMPOSE=docker compose
API_CONTAINER=api

.PHONY: up down build restart migrate reset logs bash

up:
	$(COMPOSE) up -d

down:
	$(COMPOSE) down

build:
	$(COMPOSE) up -d --build

restart: down build

logs:
	$(COMPOSE) logs -f

bash:
	$(COMPOSE) exec $(API_CONTAINER) bash

migrate:
	${COMPOSE} exec $(API_CONTAINER) bash -c "/app/.venv/bin/alembic upgrade head"
reset:
	$(COMPOSE) down -v
	$(COMPOSE) up -d --build
	sleep 5
	$(COMPOSE) exec $(API_CONTAINER) sh -c  "/app/.venv/bin/alembic upgrade head"