.PHONY: install
install:
	poetry install --with dev,test,lint


.PHONY: pre-commit-install
pre-commit-install:
	poetry run pre-commit install


.PHONY: pre-commit-uninstall
pre-commit-uninstall:
	poetry run pre-commit install

.PHONY: tests
tests:
	poetry run pytest -v .


.PHONY: unittests
unittests:
	poetry run pytest -v ./tests/unit
