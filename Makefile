DOCKER_COMPOSE_TEST := docker-compose -f docker-compose.test.yaml

.PHONY: install
install:
	poetry install --with dev,test

.PHONY: pre-commit-install
pre-commit-install:
	poetry run pre-commit install

.PHONY: pre-commit-uninstall
pre-commit-uninstall:
	poetry run pre-commit uninstall

.PHONY: run
run:
	poetry run python src/gym_management/presentation/api/main.py

.PHONY: lint
lint:
	SKIP=${SKIP} poetry run pre-commit run --all-file

# Docker-specific commands
.PHONY: build
build-app:
	docker-compose --profile api build

.PHONY: build-test
build-test:
	${DOCKER_COMPOSE_TEST} build

.PHONY: run-docker
run-docker: build-app
	docker-compose --profile api up

.PHONY: stop-docker
stop-docker:
	docker-compose --profile api down

.PHONY: test-docker
test-docker: build-test
	${DOCKER_COMPOSE_TEST} run --rm gym_management_test make test

.PHONY: lint-docker
lint-docker: build-test
	${DOCKER_COMPOSE_TEST} run --rm gym_management_test make lint

.PHONY: test
test:
	poetry run pytest --cov src --cov-report xml:coverage/coverage.xml -v ./tests

.PHONY: test-unit
test-unit:
	poetry run pytest -v ./tests/unit

.PHONY: test-subcutaneous
test-subcutaneous:
	poetry run pytest -v ./tests/subcutaneous

.PHONY: test-integration
test-integration:
	poetry run pytest -v ./tests/integration

.PHONY: create-migrations
create-migrations:
	alembic revision --autogenerate


.PHONY: migrate
migrate:
	alembic upgrade head
