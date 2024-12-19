import logging

from src.gym_management.infrastructure.config.config import Config

logger = logging.getLogger(__name__)


def load_config() -> Config:
    # todo: add loading of some configs from AWS Secrets Manager
    return Config()
