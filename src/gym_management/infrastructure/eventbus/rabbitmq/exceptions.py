from dataclasses import dataclass


class RabbitmqBrokerError(Exception):
    @property
    def detail(self) -> str:
        return "Unknown RabbitMQ broker error has occurred"

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return self.detail


class BrokerConnectionError(RabbitmqBrokerError):
    pass


class QueueError(RabbitmqBrokerError):
    pass


class ExchangeError(RabbitmqBrokerError):
    pass


@dataclass(kw_only=True)
class ExchangeDoesNotExistError(ExchangeError):
    exchange_name: str
    broker_url: str

    @property
    def detail(self) -> str:
        return f"Exchange with name '{self.exchange_name}' does not exist in the broker url: '{self.broker_url}'"


@dataclass(kw_only=True)
class QueueDoesNotExistError(ExchangeError):
    queue_name: str
    broker_url: str

    @property
    def detail(self) -> str:
        return f"Queue with name '{self.queue_name}' does not exist in the broker url: '{self.broker_url}'"


@dataclass(kw_only=True)
class BrokerNotConnectedError(BrokerConnectionError):
    @property
    def detail(self) -> str:
        return "RabbitMQ broker is not connected. Did you forget to call 'connect()'?"


@dataclass(kw_only=True)
class BrokerAlreadyConnectedError(BrokerConnectionError):
    @property
    def detail(self) -> str:
        return "RabbitMQ broker is already connected"
