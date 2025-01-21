# DomeGym

A streamlined gym management and workout scheduling platform connecting trainers, gym owners, and clients. Manage memberships, book sessions, and enhance fitness experiences—all in one place.


---
## Getting started 🔨
### Local Setup
- Python 3.11.10
- Poetry
- docker
- linters: ruff, mypy

> [!TIP]
> Use `pyenv` to easily manage multiple versions of your python environment

### Start in local
1. Install poetry: [guide](https://python-poetry.org/docs/#installation)
2. Install all project dependencies: `make install`
3. Install pre-commit: `make pre-commit-install`
4. Copy and paste `.env.example` as `.env` in the project root and adjust environment variables if needed
5. Run application: `make run`
6. Run tests: `make test`
7. Run linter: `make lint`

### Start in docker
1. Run application: `make run-docker`
2. Stop application: `make stop-docker`
3. Run tests: `make test-docker`
4. Run linter: `make lint-docker`


### Pre-commit
Run `make pre-commit-install` at the root of the repository.
It will install all the linters defined in the `pre-commit-config.yaml`

## Configuration ⚙️

### Files
- `src/gym_management/infrastructure/common/config/config.py` - contains config required for running the application.

### Loading priority

The configuration is loaded in the following order:
- default values provided in the config
- environment variables: to set value specific to an environment (local, dev, prod)
- aws secrets manager: to set secrets

The `config.py` file provides the default values for configuration attributes. These values are then overridden by environment variables and by secrets fetched from AWS Secrets Manager (if configured). Environment variables are set during the application's deployment to development (dev) and production (prod) environments.

## CI/CD pipelines

Pipelines are built following standard [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow)


## Tech stack

### Application:
- **Language**: [Python](https://docs.python.org/3.11/)
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Data validation**: [Pydantic](https://docs.pydantic.dev/latest/)
- **Database**: [PostgreSQL](https://www.postgresql.org/)
- **Tests**: [Pytest](https://docs.pytest.org/en/stable/)

---
## Documentation and good practices:
Highly recommended for starters 🎓:
- [Python official tutorial](https://docs.python.org/3.11/tutorial/index.html)
- [Python guide](https://docs.python-guide.org/)

For inspiration 💡:
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
