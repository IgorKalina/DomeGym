from typing import Literal

from pydantic import BaseModel

LogLevel = Literal["CRITICAL", "FATAL", "ERROR", "WARN", "WARNING", "INFO", "DEBUG", "NOTSET"]


class LoggerConfig(BaseModel):
    level: LogLevel
