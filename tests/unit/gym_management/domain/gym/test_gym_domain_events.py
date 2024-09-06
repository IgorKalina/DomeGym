from src.gym_management.domain.gym.events.room_added_event import RoomAddedEvent
from tests.common.gym.factories.gym_factory import GymFactory
from tests.common.room.factories.room_factory import RoomFactory
from tests.common.subscription.factories.subscription_factory import SubscriptionFactory


class TestGymDomainEvents:
    def test_gym_add_room_when_added_should_create_domain_event(self) -> None:
        subscription = SubscriptionFactory.create_subscription()
        gym = GymFactory.create_gym(max_rooms=subscription.max_rooms)
        rooms = [RoomFactory.create_room() for _ in range(subscription.max_rooms)]

        for room in rooms:
            gym.add_room(room)

        expected_domain_events = [
            RoomAddedEvent(
                room=room,
                gym=gym,
            )
            for room in rooms
        ]

        assert gym.pop_domain_events() == expected_domain_events

    def test_gym_add_rom_when_error_should_not_create_domain_event(self) -> None:
        subscription = SubscriptionFactory.create_subscription()
        gym = GymFactory.create_gym(max_rooms=subscription.max_rooms)
        rooms = [RoomFactory.create_room() for _ in range(subscription.max_rooms)]

        for room in rooms:
            gym.add_room(room)
        # flush domain events created for valid number of rooms
        gym.pop_domain_events()

        gym.add_room(RoomFactory.create_room())

        assert subscription.pop_domain_events() == []
