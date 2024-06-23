install:
	poetry install --with dev,test,lint


precommit_install:
	poetry run pre-commit install


precommit_uninstall:
	poetry run pre-commit install

test:
	poetry run pytest -v .
