NAME := haystack

PORT := 8000

.PHONY: build
build:
	docker compose -p ${NAME} --verbose build

.PHONY: up
up:
	docker compose -p ${NAME} up -d

.PHONY: down
down:
	docker compose -p ${NAME} down

.PHONY: serve
serve:
	docker exec -it ${NAME}_django uv run manage.py runserver 0.0.0.0:${PORT}

.PHONY: migrations
migrations:
	docker exec -it ${NAME}_django uv run manage.py makemigrations

.PHONY: migrate
migrate:
	docker exec -it ${NAME}_django uv run manage.py migrate

.PHONY: shell
shell:
	docker exec -it ${NAME}_django /bin/bash
