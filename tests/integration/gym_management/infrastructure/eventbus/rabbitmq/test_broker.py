import asyncio
import uuid
from unittest.mock import Mock

import aio_pika
import pytest

from src.gym_management.infrastructure.common.eventbus.rabbitmq.broker import RabbitmqEventBroker
from src.gym_management.infrastructure.common.eventbus.rabbitmq.dto.event import RabbitmqEvent
from src.gym_management.infrastructure.common.eventbus.rabbitmq.exceptions import (
    BrokerNotConnectedError,
    ExchangeDoesNotExistError,
    QueueDoesNotExistError,
)
from src.gym_management.infrastructure.common.eventbus.rabbitmq.options import (
    RabbitmqPublishOptions,
    RabbitmqSubscribeOptions,
)


@pytest.mark.asyncio
class TestRabbitmqEventBroker:
    @pytest.fixture(autouse=True)
    def setup_method(self, broker: RabbitmqEventBroker) -> None:
        self._broker = broker

        self._publish_options = RabbitmqPublishOptions(exchange_name="domain_events", routing_key="domain_events")
        self._subscribe_options = RabbitmqSubscribeOptions(
            queue_name="domain_events", exchange_name="domain_events", routing_key="domain_events"
        )
        self._event = RabbitmqEvent(id=uuid.uuid4(), data={"dummy_data": "dummy_data"}, event_type="dummy_event")

    async def test_when_message_published_should_be_consumed_by_subscriber(self) -> None:
        # Arrange
        mock = Mock()

        async def simple_handler(event: RabbitmqEvent) -> None:  # noqa: ARG001
            mock()

        await self._broker.subscribe(simple_handler, options=self._subscribe_options)

        # Act
        await self._broker.publish(event=self._event, options=self._publish_options)

        # Assert
        await asyncio.sleep(0.4)
        mock.assert_called_once()

    async def test_when_no_messages_published_should_not_execute_handler(self) -> None:
        # Arrange
        mock = Mock()

        async def simple_handler(event: RabbitmqEvent) -> None:  # noqa: ARG001
            mock()

        # Act
        await self._broker.subscribe(simple_handler, options=self._subscribe_options)

        # Assert
        mock.assert_not_called()

    async def test_when_publishing_event_but_broker_disconnected_should_fail(self) -> None:
        # Arrange
        # broker is connected by default
        await self._broker.disconnect()

        # Act
        with pytest.raises(BrokerNotConnectedError) as err:
            await self._broker.publish(event=self._event, options=self._publish_options)

        # Assert
        assert err.value.detail == "RabbitMQ broker is not connected. Did you forget to call 'connect()'?"

    async def test_when_subscribing_but_broker_disconnected_should_fail(self) -> None:
        # Arrange
        # broker is connected by default
        await self._broker.disconnect()

        async def simple_handler(message: aio_pika.IncomingMessage) -> None:
            # async with message.process():
            RabbitmqEvent.from_pika_message(message)

        # Act
        with pytest.raises(BrokerNotConnectedError) as err:
            await self._broker.subscribe(handler=simple_handler, options=self._subscribe_options)

        # Assert
        assert err.value.detail == "RabbitMQ broker is not connected. Did you forget to call 'connect()'?"

    async def test_when_publishing_event_to_non_existing_exchange_should_fail(self) -> None:
        # Arrange
        publish_options = RabbitmqPublishOptions(
            **self._publish_options.model_dump(exclude={"exchange_name"}),
            exchange_name="non_existing_exchange",
        )

        # Act
        with pytest.raises(ExchangeDoesNotExistError) as err:
            await self._broker.publish(event=self._event, options=publish_options)

        # Assert
        assert err.value.detail == (
            f"Exchange with name '{publish_options.exchange_name}' does not exist in the broker url: "
            f"'{self._broker.options.get_url()}'"
        )

    async def test_when_subscribing_to_non_existing_queue_should_fail(self) -> None:
        # Arrange
        subscribe_options = RabbitmqSubscribeOptions(
            **self._subscribe_options.model_dump(exclude={"queue_name"}),
            queue_name="non_existing_queue",
        )

        async def simple_handler(message: aio_pika.IncomingMessage) -> None:
            RabbitmqEvent.from_pika_message(message)

        # Act
        with pytest.raises(QueueDoesNotExistError) as err:
            await self._broker.subscribe(simple_handler, options=subscribe_options)

        # Assert
        assert err.value.detail == (
            f"Queue with name '{subscribe_options.queue_name}' does not exist in the broker url: "
            f"'{self._broker.options.get_url()}'"
        )
