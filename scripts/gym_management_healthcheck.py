import sys
from http import HTTPStatus

import requests


def make_healthcheck() -> None:
    try:
        response = requests.get("http://localhost:8000/healthcheck", timeout=10)  # type: ignore
        if response.status_code == HTTPStatus.OK:
            sys.exit(0)
        else:
            sys.exit(1)
    except Exception:
        sys.exit(1)


if __name__ == "__main__":
    make_healthcheck()
