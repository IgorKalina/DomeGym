import os
from typing import List, Tuple, Type

from dotenv import find_dotenv
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
)

from src.gym_management.infrastructure.config.api import ApiConfig, UvicornConfig
from src.gym_management.infrastructure.config.enums.environment import Environment
from src.gym_management.infrastructure.config.logger import LoggerConfig

ENV_PREFIX = "GYM_MANAGEMENT_"
ENV_NESTED_DELIMITED = "__"


def _find_yaml_configs(folder: str) -> List[str]:
    return [
        os.path.join(folder, config) for config in os.listdir(folder) if os.path.isfile(os.path.join(folder, config))
    ]


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(find_dotenv(".env"),),
        env_prefix=ENV_PREFIX,
        env_nested_delimiter=ENV_NESTED_DELIMITED,
        yaml_file=_find_yaml_configs("configs"),
    )

    env: Environment
    api: ApiConfig
    uvicorn: UvicornConfig
    logger: LoggerConfig

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,  # environment variables takes precedence over yaml configs
            dotenv_settings,
            YamlConfigSettingsSource(settings_cls),
            file_secret_settings,
        )