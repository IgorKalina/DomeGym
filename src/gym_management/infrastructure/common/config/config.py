from src.gym_management.infrastructure.common.config.api import ApiConfig, UvicornConfig
from src.gym_management.infrastructure.common.config.base_config import BaseConfig
from src.gym_management.infrastructure.common.config.database import DatabaseConfig
from src.gym_management.infrastructure.common.config.enums.environment import Environment
from src.gym_management.infrastructure.common.config.logger import LoggerConfig


class Config(BaseConfig):
    env: Environment
    api: ApiConfig
    uvicorn: UvicornConfig
    logger: LoggerConfig
    database: DatabaseConfig
