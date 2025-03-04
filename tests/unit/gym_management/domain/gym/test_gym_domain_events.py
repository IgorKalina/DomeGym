import pytest
from freezegun import freeze_time

from src.gym_management.domain.gym.events.room_added_event import RoomAddedEvent
from src.gym_management.domain.gym.exceptions import GymCannotHaveMoreRoomsThanSubscriptionAllowsError
from tests.common.gym_management.common import constants
from tests.common.gym_management.gym.factory.gym_factory import GymFactory
from tests.common.gym_management.room.factory.room_factory import RoomFactory
from tests.common.gym_management.subscription.factory.subscription_factory import SubscriptionFactory


@freeze_time(constants.common.DEFAULT_DATETIME)
class TestGymDomainEvents:
    def test_add_room_when_added_should_create_domain_event(self) -> None:
        # Arrange
        subscription = SubscriptionFactory.create_subscription()
        gym = GymFactory.create_gym(max_rooms=subscription.max_rooms)
        rooms = [RoomFactory.create_room() for _ in range(subscription.max_rooms)]
        expected_domain_events = [
            RoomAddedEvent(
                room=room,
                gym=gym,
            )
            for room in rooms
        ]

        # Act
        for room in rooms:
            gym.add_room(room)

        # Assert
        assert gym.pop_domain_events() == expected_domain_events

    def test_add_room_when_error_should_not_create_domain_event(self) -> None:
        # Arrange
        subscription = SubscriptionFactory.create_subscription()
        gym = GymFactory.create_gym(max_rooms=subscription.max_rooms)
        rooms = [RoomFactory.create_room() for _ in range(subscription.max_rooms)]
        for room in rooms:
            gym.add_room(room)
        # flush domain events created for valid number of rooms
        gym.pop_domain_events()

        # Act
        with pytest.raises(GymCannotHaveMoreRoomsThanSubscriptionAllowsError):
            gym.add_room(RoomFactory.create_room())

        # Assert
        assert subscription.pop_domain_events() == []
