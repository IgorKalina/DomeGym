import uuid

import pytest

from src.gym_management.domain.gym.exceptions import GymCannotHaveMoreRoomsThanSubscriptionAllowsError
from src.gym_management.domain.room.exceptions import RoomDoesNotExistError
from src.shared_kernel.application.error_or import ErrorType
from tests.common.gym_management.gym.factory.gym_factory import GymFactory
from tests.common.gym_management.room.room_factory import RoomFactory


class TestGymAggregate:
    def test_add_room_when_subscription_allows_should_succeed(self) -> None:
        # Arrange
        gym = GymFactory.create_gym(max_rooms=1)
        room = RoomFactory.create_room()

        # Act
        gym.add_room(room)

        # Assert
        assert gym.has_room(room.id)

    def test_add_room_when_more_than_subscription_allows_should_fail(self) -> None:
        # Arrange
        gym = GymFactory.create_gym(max_rooms=1)
        room1 = RoomFactory.create_room()
        room2 = RoomFactory.create_room()
        gym.add_room(room1)

        # Act
        with pytest.raises(GymCannotHaveMoreRoomsThanSubscriptionAllowsError) as err:
            gym.add_room(room2)

        # Assert
        assert err.value.max_rooms == 1
        assert err.value.title == "Gym.Validation"
        assert err.value.detail == "A gym cannot have more rooms than the subscription allows. Max rooms allowed: 1"
        assert err.value.error_type == ErrorType.VALIDATION
        assert gym.has_room(room2.id) is False

    def test_remove_room_when_exists_should_succeed(self) -> None:
        # Arrange
        gym = GymFactory.create_gym()
        room1 = RoomFactory.create_room()
        gym.add_room(room1)

        # Act
        gym.remove_room(room1)

        # Assert
        assert gym.has_room(room1.id) is False

    def test_remove_room_when_not_exists_should_fail(self) -> None:
        # Arrange
        gym = GymFactory.create_gym()
        room1 = RoomFactory.create_room()

        # Act
        with pytest.raises(RoomDoesNotExistError) as err:
            gym.remove_room(room1)

        # Assert
        assert err.value.title == "Room.Not_found"
        assert err.value.detail == "Room does not exist in the gym"
        assert err.value.error_type == ErrorType.NOT_FOUND
        assert gym.has_room(room1.id) is False

    def test_add_trainer_should_succeed(self) -> None:
        # Arrange
        gym = GymFactory.create_gym()
        trainer_id = uuid.uuid4()

        # Act
        gym.add_trainer(trainer_id)

        # Assert
        assert gym.has_trainer(trainer_id)

    def test_has_trainer_when_not_exists_should_return_false(self) -> None:
        # Arrange
        gym = GymFactory.create_gym()
        trainer_id = uuid.uuid4()

        # Act & Assert
        assert gym.has_trainer(trainer_id) is False
