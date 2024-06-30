.PHONY: install
install:
	poetry install --with dev,test,lint


.PHONY: pre-commit-install
pre-commit-install:
	poetry run pre-commit install


.PHONY: pre-commit-uninstall
pre-commit-uninstall:
	poetry run pre-commit install

.PHONY: run-all-tests
run-all-tests:
	poetry run pytest -v .


.PHONY: run-unittests
run-unittests:
	poetry run pytest -v ./tests/unit
