import asyncio
from dataclasses import dataclass

import orjson
from sqlalchemy.ext.asyncio import create_async_engine

from src.gym_management.common.settings.config import settings


@dataclass
class DBConfig:
    host: str = "localhost"
    port: int = 15432
    database: str = "domegym"
    user: str = "admin"
    password: str = "admin"
    driver: str = "postgresql+asyncpg"
    echo: bool = True

    @property
    def full_url(self) -> str:
        # return "postgresql+asyncpg://{}:{}@{}:{}/{}".format(
        #     self.user,
        #     self.password,
        #     self.host,
        #     self.port,
        #     self.database,
        # )
        return f"{self.driver}://" f"{self.user}:{self.password}" f"@{self.host}:{self.port}" f"/{self.database}"


if __name__ == "__main__":
    db_config = DBConfig()
    print(settings.database)
    engine = create_async_engine(
        settings.database.full_url,
        echo=True,
        echo_pool=db_config.echo,
        json_serializer=lambda data: orjson.dumps(data).decode(),
        json_deserializer=orjson.loads,
        pool_size=50,
    )
    connection = engine.connect()
    asyncio.run(connection.start())
