.DEFAULT_GOAL := build_and_restart
COMPOSE := docker compose -f build/docker-compose.yml
CURRENT_VERSION_TAG := v0.1
BUILDX := docker buildx build -f build/Dockerfile --platform linux/amd64,linux/arm64
EXEC := docker exec -it build-base_img-1


build_and_restart: build_local restart

build_local:
	docker build -f build/Dockerfile -t ilyatbn/base_img-dev:latest .

build_dev:
	$(BUILDX) -t ilyatbn/base_img-dev:$(CURRENT_VERSION_TAG) -t ilyatbn/base_img-dev:latest --push .

build_prod:
	$(BUILDX) -t ilyatbn/base_img:$(CURRENT_VERSION_TAG) -t ilyatbn/base_img:latest --push .

start:
	$(COMPOSE) up -d --remove-orphans


stop:
	$(COMPOSE) stop

restart: stop start

remove:
	$(COMPOSE) down
	$(COMPOSE) rm -v

shell:
	$(EXEC) ipython

bash:
	$(EXEC) bash

logs:
	docker logs -f build-base_img-1
