install:
	poetry install --with dev,test,lint


pre-commit-install:
	poetry run pre-commit install


pre-commit-uninstall:
	poetry run pre-commit install

test:
	poetry run pytest -v .
