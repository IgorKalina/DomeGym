from pydantic import SecretStr
from sqlalchemy import make_url

from src.gym_management.infrastructure.common.config.database import DatabaseConfig, DatabaseUser


def map_database_full_url_to_config(full_url: str) -> DatabaseConfig:
    try:
        parsed_url = make_url(full_url)

        return DatabaseConfig(
            user=DatabaseUser(name=parsed_url.username, password=SecretStr(parsed_url.password)),
            host=parsed_url.host,
            port=parsed_url.port,
            name=parsed_url.database,
            driver=parsed_url.drivername,
        )
    except Exception as e:
        raise ValueError(f"Failed to parse URL: {e}") from e
