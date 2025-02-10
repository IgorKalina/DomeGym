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
	docker-compose --profile api build

.PHONY: build-test
build-test:
	docker build -f Dockerfile.test . -t ${TEST_CONTAINER_NAME}

.PHONY: build-test-dependency
build-test-dependency:
	@${MAKE} stop-test-dependency
	docker-compose -f docker-compose.test.yaml --env-file .env.test --profile dependency up -d --build

.PHONY: stop-test-dependency
stop-test-dependency:
	docker-compose -f docker-compose.test.yaml --profile dependency down -v

.PHONY: run-docker
run-docker: build-app
	docker-compose --profile api up

.PHONY: stop-docker
stop-docker:
	docker-compose --profile api down --remove-orphans

.PHONY: test-docker
test-docker:
	docker-compose -f docker-compose.test.yaml --profile runner down -v
	docker-compose -f docker-compose.test.yaml --env-file .env.test build
	docker-compose -f docker-compose.test.yaml --env-file .env.test run --rm test
	docker-compose -f docker-compose.test.yaml --profile runner down -v


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
