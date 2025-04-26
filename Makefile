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
	$(COMPOSE) exec $(APP_CONTAINER) bash

migrate:
	$(COMPOSE) exec $(APP_CONTAINER) alembic upgrade head

reset:
	$(COMPOSE) down -v
	$(COMPOSE) up -d --build
	sleep 5
	$(COMPOSE) exec $(APP_CONTAINER) alembic upgrade head