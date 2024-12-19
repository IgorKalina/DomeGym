from typing import Literal

from pydantic import BaseModel

UvicornLogLevel = Literal["critical", "error", "warning", "info", "debug", "trace"]


class ApiConfig(BaseModel):
    title: str
    version: str
    debug: bool


class UvicornConfig(BaseModel):
    host: str
    port: int
    log_level: UvicornLogLevel
