import logging

from src.gym_management.infrastructure.common.config.config import Config

logger = logging.getLogger(__name__)

__all__ = ["load_config"]


def load_config() -> Config:
    # todo: add loading of some configs from AWS Secrets Manager
    return Config()
