import uuid

from src.common.error_or import Result
from src.gym_management.domain.gym.errors import GymCannotHaveMoreRoomsThanSubscriptionAllows, RoomDoesNotExist
from src.gym_management.domain.gym.events.room_added_event import RoomAddedEvent
from src.gym_management.domain.gym.events.room_removed_event import RoomRemovedEvent
from tests.unit.utils.gym.gym_factory import GymFactory
from tests.unit.utils.room.room_factory import RoomFactory


class TestGymAggregate:
    def test_add_room_when_subscription_allows_should_succeed(self) -> None:
        gym = GymFactory.create_gym(max_rooms=1)
        room1 = RoomFactory.create_room()

        add_room1_result = gym.add_room(room1)

        assert add_room1_result.is_ok()
        assert add_room1_result.value == Result.created()
        assert gym.has_room(room1.id)
        expected_domain_events = [
            RoomAddedEvent(
                gym=gym,
                room=room1,
            )
        ]

        actual_domain_events = gym.pop_domain_events()
        assert actual_domain_events == expected_domain_events

    def test_add_room_when_more_than_subscription_allows_should_fail(self) -> None:
        gym = GymFactory.create_gym(max_rooms=1)
        room1 = RoomFactory.create_room()
        room2 = RoomFactory.create_room()

        add_room1_result = gym.add_room(room1)
        add_room2_result = gym.add_room(room2)

        assert add_room1_result.is_ok()
        assert add_room2_result.is_error()
        assert add_room2_result.first_error == GymCannotHaveMoreRoomsThanSubscriptionAllows()
        assert gym.has_room(room2.id) is False
        expected_domain_events = [
            RoomAddedEvent(
                gym=gym,
                room=room1,
            )
        ]

        actual_domain_events = gym.pop_domain_events()
        assert actual_domain_events == expected_domain_events

    def test_remove_room_when_exists_should_succeed(self) -> None:
        gym = GymFactory.create_gym()
        room1 = RoomFactory.create_room()
        gym.add_room(room1)

        remove_group_result = gym.remove_room(room1)

        assert remove_group_result.is_ok()
        assert remove_group_result.value == Result.deleted()
        assert gym.has_room(room1.id) is False
        expected_domain_events = [
            RoomAddedEvent(
                gym=gym,
                room=room1,
            ),
            RoomRemovedEvent(
                gym=gym,
                room_id=room1.id,
            ),
        ]

        actual_domain_events = gym.pop_domain_events()
        assert actual_domain_events == expected_domain_events

    def test_remove_room_when_not_exists_should_fail(self) -> None:
        gym = GymFactory.create_gym()
        room1 = RoomFactory.create_room()

        remove_group_result = gym.remove_room(room1)

        assert remove_group_result.is_error()
        assert remove_group_result.first_error == RoomDoesNotExist()
        assert gym.pop_domain_events() == []

    def test_add_trainer_should_succeed(self) -> None:
        gym = GymFactory.create_gym()
        trainer_id = uuid.uuid4()

        add_trainer_result = gym.add_trainer(trainer_id)

        assert add_trainer_result == Result.created()
        assert gym.has_trainer(trainer_id)
        assert gym.pop_domain_events() == []

    def test_has_trainer_when_not_exists_should_return_false(self) -> None:
        gym = GymFactory.create_gym()
        trainer_id = uuid.uuid4()

        assert gym.has_trainer(trainer_id) is False
        assert gym.pop_domain_events() == []
