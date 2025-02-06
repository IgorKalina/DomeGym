from typing import List

from pydantic import BaseModel, SecretStr


class RabbitmqUser(BaseModel):
    name: str
    password: SecretStr


class RabbitmqQueue(BaseModel):
    queue_name: str
    exchange_name: str
    routing_key: str


class RabbitmqConfig(BaseModel):
    user: RabbitmqUser
    host: str
    port: int
    queues: List[RabbitmqQueue]

    @property
    def full_url(self) -> str:
        return f"amqp://{self.user.name}:{self.user.password.get_secret_value()}@{self.host}:{self.port}/"
