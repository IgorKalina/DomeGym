from src.gym_management.infrastructure.config.api import ApiConfig, UvicornConfig
from src.gym_management.infrastructure.config.base_config import BaseConfig
from src.gym_management.infrastructure.config.database import DatabaseConfig
from src.gym_management.infrastructure.config.enums.environment import Environment
from src.gym_management.infrastructure.config.logger import LoggerConfig
from src.gym_management.infrastructure.config.rabbitmq import RabbitmqConfig


class Config(BaseConfig):
    env: Environment
    api: ApiConfig
    uvicorn: UvicornConfig
    logger: LoggerConfig
    database: DatabaseConfig
    rabbitmq: RabbitmqConfig
