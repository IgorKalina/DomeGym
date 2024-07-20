import os

from dynaconf import Dynaconf

current_directory = os.path.dirname(os.path.realpath(__file__))

settings = Dynaconf(
    root_path=current_directory,
    settings_files=["configs/*.toml", "configs/.secrets.toml"],
    environments=True,
    env_switcher="ENV",
    env="local",
    merge_enabled=True,
)
