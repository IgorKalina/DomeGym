import uuid
from typing import Self

import aio_pika
import orjson
from pydantic import Field

from src.shared_kernel.infrastructure.eventbus.interfaces.event import Event


class RabbitmqEvent(Event):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    data: dict
    event_type: str

    @classmethod
    def from_pika_message(cls, message: aio_pika.IncomingMessage) -> Self:
        data = orjson.loads(message.body.decode())
        return cls(**data)

    def to_pika_message(self, delivery_mode: int = aio_pika.DeliveryMode.PERSISTENT) -> aio_pika.Message:
        return aio_pika.Message(
            body=orjson.dumps({"event_type": self.event_type, "data": self.data}),
            message_id=str(self.id),
            content_type="application/json",
            delivery_mode=delivery_mode,
            headers={},
        )
