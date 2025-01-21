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

# Ubiquitous Language

---

## User

**Definition**: Anyone who uses the system, with roles such as Admin, Trainer, or Participant.

**Usage**: A User registers on the platform.

**Usage**: A User sets their payment method.


## Participant Profile

**Definition**: A User's role enabling them to join and participate in sessions.

**Usage**: A User creates a Participant Profile.

**Usage**: A Participant checks into a session.


## Session

**Definition**: A fitness class held in a gym's room.

**Usage**: A Participant reserves a spot in a Session.

**Usage**: The Session has a capacity limit of 20 participants.


## Room

**Definition**: A designated area within a gym for conducting sessions.

**Usage**: The Room has a capacity limit of 30 participants.

**Usage**: The Room was added to the Gym.


## Gym

**Definition**: A facility offering various fitness sessions.

**Usage**: An Admin creates a Gym within their subscription.

**Usage**: The Gym was deleted.


## Admin Profile

**Definition**: A User's role with privileges to manage gym operations.

**Usage**: An Admin purchased a subscription.

**Usage**: The Admin created a yoga session in Room 3.


## Subscription

**Definition**: A service plan offering Admins different capacities for creating gyms, rooms, and sessions.

**Usage**: An Admin chooses a Subscription type.

**Usage**: An Admin with a Free subscription can create up to 1 gym, 1 room in that gym, and a maximum of 4 sessions in each room, per day.

**Usage**: An Admin with a Starter subscription can create up to 1 gym, 3 rooms in that gym, and an unlimited number of sessions.

**Usage**: An Admin with a Pro subscription can create up to 3 gyms and can create an unlimited number of rooms and sessions.


## Trainer Profile

**Definition**: A User's role qualified to teach sessions.

**Usage**: A Trainer starts their session.

**Usage**: A Trainer received feedback for the session.


## Reserving

**Definition**: The action of securing a spot in a session by a participant.

**Usage**: The Participant reserved a spot in the session.

**Usage**: The reservation was confirmed, and the payment method was charged.


## Subscription Type

**Definition**: The category of a Subscription that determines an Admin's Gym, Room, and Session Capacities.

**Usage**: An Admin upgrades to a higher Subscription Type.

**Usage**: Capacities change based on the Subscription Type.


## Check-In

**Definition**: The action of joining a session.

**Usage**: The Participant checked into the session.

**Usage**: The Trainer started the session; Check-In is now available.


## Cancellation Policy

**Definition**: The rules governing the ability to cancel a reservation.

**Usage**: A Participant reviews the Cancellation Policy before reserving.

**Usage**: The user cannot cancel the session due to the Cancellation Policy.


## Goal Tracking

**Definition**: A feature that records and monitors participant fitness goals.

**Usage**: A Participant sets goals using Goal Tracking.

**Usage**: Goal Tracking alerts a Participant of their progress.
