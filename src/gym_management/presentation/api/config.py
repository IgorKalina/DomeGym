from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class APIConfig:
    host: str = "127.0.0.1"
    port: int = 8000
    debug: bool = __debug__


@dataclass
class LoggingConfig:
    render_json_logs: bool = False
    path: Path | None = None
    level: str = "DEBUG"


@dataclass
class Config:
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    api: APIConfig = field(default_factory=APIConfig)
