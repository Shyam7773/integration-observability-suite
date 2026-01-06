include .env
export

up:
	docker compose -f infra/docker-compose.yml up -d

down:
	docker compose -f infra/docker-compose.yml down

ps:
	docker compose -f infra/docker-compose.yml ps

logs:
	docker compose -f infra/docker-compose.yml logs -f --tail=200

initdb:
	docker compose -f infra/docker-compose.yml exec -T db psql -U observability -d observability -f /infra/init.sql

dbcheck:
	docker compose -f infra/docker-compose.yml exec -T db psql -U observability -d observability -c "select now();"
