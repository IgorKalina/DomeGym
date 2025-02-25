from aio_pika import ExchangeType
from pydantic import BaseModel, SecretStr

from src.shared_kernel.infrastructure.interfaces.eventbus.options import (
    BrokerOptions,
    PublishOptions,
    SubscribeOptions,
    TopicOptions,
)


class RabbitmqBrokerOptions(BrokerOptions):
    user: str = "guest"
    password: SecretStr = SecretStr("guest")
    host: str = "localhost"
    port: int = 5672

    def get_url(self, safe: bool = True) -> str:
        password = self.password if safe else self.password.get_secret_value()
        return f"amqp://{self.user}:{password}@{self.host}:{self.port}/"


class RabbitmqSubscribeOptions(SubscribeOptions):
    queue_name: str
    exchange_name: str
    routing_key: str


class RabbitmqPublishOptions(PublishOptions):
    exchange_name: str
    routing_key: str


class RabbitmqExchangeOptions(BaseModel):
    name: str
    type: ExchangeType = ExchangeType.DIRECT
    durable: bool = True


class RabbitmqQueueOptions(BaseModel):
    name: str
    exchange_name: str
    routing_key: str
    durable: bool = True


class RabbitmqTopicOptions(TopicOptions):
    exchange: RabbitmqExchangeOptions
    queue: RabbitmqQueueOptions
