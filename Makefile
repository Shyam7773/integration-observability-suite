include .env
export
export PYTHONPATH:=$(shell pwd)

DC=docker-compose
COMPOSE_FILE=infra/docker-compose.yml

.PHONY: up down ps dbcheck initdb run marts dash

up:
	$(DC) -f $(COMPOSE_FILE) up -d

down:
	$(DC) -f $(COMPOSE_FILE) down

ps:
	$(DC) -f $(COMPOSE_FILE) ps

dbcheck:
	$(DC) -f $(COMPOSE_FILE) exec -T db psql -h 127.0.0.1 -U observability -d observability -c "select now();"

initdb:
	$(DC) -f $(COMPOSE_FILE) exec -T db psql -h 127.0.0.1 -U observability -d observability -f /infra/init.sql

run:
	python -m orchestration.run_once

marts:
	python -m models.run_models

dash:
	streamlit run dashboards/app.py

.PHONY: reset test

reset:
	$(DC) -f $(COMPOSE_FILE) exec -T db psql -h 127.0.0.1 -U observability -d observability -f /infra/reset.sql

test:
	pytest -q
