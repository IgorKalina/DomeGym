import uuid

from src.gym_management.domain.gym.errors import GymCannotHaveMoreRoomsThanSubscriptionAllows
from src.gym_management.domain.room.errors import RoomDoesNotExist
from src.shared_kernel.application.error_or import Result
from tests.common.gym_management.gym.factory.gym_factory import GymFactory
from tests.common.gym_management.room.room_factory import RoomFactory


class TestGymAggregate:
    def test_add_room_when_subscription_allows_should_succeed(self) -> None:
        # Arrange
        gym = GymFactory.create_gym(max_rooms=1)
        room1 = RoomFactory.create_room()

        # Act
        add_room1_result = gym.add_room(room1)

        # Assert
        assert add_room1_result.is_ok()
        assert add_room1_result.value == Result.created()
        assert gym.has_room(room1.id)

    def test_add_room_when_more_than_subscription_allows_should_fail(self) -> None:
        # Arrange
        gym = GymFactory.create_gym(max_rooms=1)
        room1 = RoomFactory.create_room()
        room2 = RoomFactory.create_room()

        # Act
        add_room1_result = gym.add_room(room1)
        add_room2_result = gym.add_room(room2)

        # Assert
        assert add_room1_result.is_ok()
        assert add_room2_result.is_error()
        assert add_room2_result.first_error == GymCannotHaveMoreRoomsThanSubscriptionAllows()
        assert gym.has_room(room2.id) is False

    def test_remove_room_when_exists_should_succeed(self) -> None:
        # Arrange
        gym = GymFactory.create_gym()
        room1 = RoomFactory.create_room()
        gym.add_room(room1)

        # Act
        remove_group_result = gym.remove_room(room1)

        # Assert
        assert remove_group_result.is_ok()
        assert remove_group_result.value == Result.deleted()
        assert gym.has_room(room1.id) is False

    def test_remove_room_when_not_exists_should_fail(self) -> None:
        # Arrange
        gym = GymFactory.create_gym()
        room1 = RoomFactory.create_room()

        # Act
        remove_group_result = gym.remove_room(room1)

        # Assert
        assert remove_group_result.is_error()
        assert remove_group_result.first_error == RoomDoesNotExist()

    def test_add_trainer_should_succeed(self) -> None:
        # Arrange
        gym = GymFactory.create_gym()
        trainer_id = uuid.uuid4()

        # Act
        add_trainer_result = gym.add_trainer(trainer_id)

        # Assert
        assert add_trainer_result == Result.created()
        assert gym.has_trainer(trainer_id)

    def test_has_trainer_when_not_exists_should_return_false(self) -> None:
        # Arrange
        gym = GymFactory.create_gym()
        trainer_id = uuid.uuid4()

        # Act & Assert
        assert gym.has_trainer(trainer_id) is False
