from unittest.mock import Mock

import aio_pika
import pytest

from src.gym_management.infrastructure.background_services.domain_events.mappers import (
    domain_event_to_rabbitmq_event,
    rabbitmq_event_to_domain_event,
)
from src.gym_management.infrastructure.eventbus.rabbitmq.broker import RabbitmqEventBroker
from src.gym_management.infrastructure.eventbus.rabbitmq.dto.event import RabbitmqEvent
from src.gym_management.infrastructure.eventbus.rabbitmq.options import RabbitmqPublishOptions, RabbitmqSubscribeOptions
from tests.common.gym_management.gym.factory.gym_domain_event_factory import GymDomainEventFactory


@pytest.mark.asyncio
class TestRabbitmqEventBroker:
    @pytest.fixture(autouse=True)
    def setup_method(self, broker: RabbitmqEventBroker) -> None:
        self._broker = broker

        self._publish_options = RabbitmqPublishOptions(exchange_name="domain_events", routing_key="domain_events")
        self._subscribe_options = RabbitmqSubscribeOptions(
            queue_name="domain_events", exchange_name="domain_events", routing_key="domain_events"
        )

    async def test_when_message_published_should_be_consumed_by_subscriber(self) -> None:
        mock = Mock()

        async def simple_handler(message: aio_pika.IncomingMessage) -> None:
            # async with message.process():
            event = RabbitmqEvent.from_pika_message(message)
            rabbitmq_event_to_domain_event(event)
            mock()

        await self._broker.subscribe(simple_handler, options=self._subscribe_options)
        event = domain_event_to_rabbitmq_event(GymDomainEventFactory.create_gym_removed_event())

        await self._broker.publish(event=event, options=self._publish_options)

        mock.assert_called_once()

    async def test_when_no_messages_published_should_not_execute_handler(self) -> None:
        mock = Mock()

        async def simple_handler(message: aio_pika.IncomingMessage) -> None:
            # async with message.process():
            event = RabbitmqEvent.from_pika_message(message)
            rabbitmq_event_to_domain_event(event)
            mock()

        await self._broker.subscribe(simple_handler, options=self._subscribe_options)

        mock.assert_not_called()
