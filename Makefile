APP_CONTAINER_NAME := gym-management
TEST_CONTAINER_NAME := gym-management-test

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
	docker build . -t ${APP_CONTAINER_NAME}

.PHONY: build-test
build-test:
	docker build -f Dockerfile.test . -t ${TEST_CONTAINER_NAME}

.PHONY: run-docker
run-docker: build-app
	@echo "Stopping and removing existing container if it exists"
	@docker ps -q -f name=${APP_CONTAINER_NAME} && docker rm -f ${APP_CONTAINER_NAME} || true
	docker run -v ./.env:/app/.env:ro -p 8000:8000 -d --name ${APP_CONTAINER_NAME} ${APP_CONTAINER_NAME}

.PHONY: stop-docker
stop-docker:
	docker stop ${APP_CONTAINER_NAME}

.PHONY: test-docker
test-docker: build-test
	docker run ${TEST_CONTAINER_NAME} make test

.PHONY: lint-docker
lint-docker: build-test
	docker run ${TEST_CONTAINER_NAME} make lint

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
