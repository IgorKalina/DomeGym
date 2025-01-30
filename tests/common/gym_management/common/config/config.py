from dotenv import find_dotenv
from pydantic_settings import SettingsConfigDict

from src.gym_management.infrastructure.config import Config
from src.gym_management.infrastructure.config.base_config import (
    ENV_NESTED_DELIMITED,
    ENV_PREFIX,
    find_yaml_configs,
)


class ConfigTest(Config):
    model_config = SettingsConfigDict(
        env_file=(find_dotenv(".env.test"),),
        env_prefix=ENV_PREFIX,
        env_nested_delimiter=ENV_NESTED_DELIMITED,
        yaml_file=find_yaml_configs("configs"),
    )
