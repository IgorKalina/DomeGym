from typing import Self

import aio_pika
import orjson

from src.gym_management.presentation.api.controllers.common.responses.orjson import additionally_serialize
from src.shared_kernel.infrastructure.interfaces.eventbus.event import Event


class RabbitmqEvent(Event):
    @classmethod
    def from_pika_message(cls, message: aio_pika.IncomingMessage) -> Self:
        data = orjson.loads(message.body.decode())
        return cls(**data)

    def to_pika_message(self, delivery_mode: int = aio_pika.DeliveryMode.PERSISTENT) -> aio_pika.Message:
        return aio_pika.Message(
            body=orjson.dumps(self.model_dump(), default=additionally_serialize),
            message_id=str(self.id),
            content_type="application/json",
            delivery_mode=delivery_mode,
            headers={},
        )
