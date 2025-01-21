from typing import List

import pytest

from src.gym_management.application.gym.dto.repository import GymDB
from src.gym_management.application.gym.exceptions import GymDoesNotExistError
from src.gym_management.application.room.dto.repository import RoomDB
from src.gym_management.application.subscription.dto.repository import SubscriptionDB
from src.gym_management.application.subscription.exceptions import SubscriptionDoesNotExistError
from src.gym_management.domain.gym.exceptions import GymCannotHaveMoreRoomsThanSubscriptionAllowsError
from src.shared_kernel.application.error_or import ErrorType
from src.shared_kernel.infrastructure.command.command_invoker_memory import CommandInvokerMemory
from tests.common.gym_management import constants
from tests.common.gym_management.gym.repository.memory import GymMemoryRepository
from tests.common.gym_management.room.factory.room_command_factory import RoomCommandFactory
from tests.common.gym_management.room.repository.memory import RoomMemoryRepository
from tests.common.gym_management.subscription.repository.memory import (
    SubscriptionMemoryRepository,
)


class TestCreateRoom:
    @pytest.fixture(autouse=True)
    def setup_method(
        self,
        command_invoker: CommandInvokerMemory,
        subscription_repository: SubscriptionMemoryRepository,
        gym_repository: GymMemoryRepository,
        room_repository: RoomMemoryRepository,
        gym_db: GymDB,
        subscription_db: SubscriptionDB,
    ) -> None:
        self._command_invoker = command_invoker
        self._subscription_repository = subscription_repository
        self._gym_repository = gym_repository
        self._room_repository = room_repository

        self._gym_db: GymDB = gym_db
        self._subscription_db: SubscriptionDB = subscription_db

    @pytest.mark.asyncio
    async def test_create_room_when_valid_command_should_create_room(self) -> None:
        # Arrange
        create_room = RoomCommandFactory.create_create_room_command(
            gym_id=self._gym_db.id, subscription_id=self._gym_db.subscription_id
        )

        # Act
        room: RoomDB = await self._command_invoker.invoke(create_room)

        # Assert
        assert isinstance(room, RoomDB)
        rooms: List[RoomDB] = await self._room_repository.get_by_gym_id(self._gym_db.id)
        assert len(rooms) == 1
        room_db = rooms[0]
        assert room_db.id is not None
        assert room_db.name == create_room.name
        assert room_db.gym_id == create_room.gym_id
        assert room_db.subscription_id == create_room.subscription_id

    @pytest.mark.asyncio
    async def test_create_room_when_subscription_not_exists_should_fail(self) -> None:
        # Arrange
        create_room = RoomCommandFactory.create_create_room_command(
            gym_id=self._gym_db.id, subscription_id=constants.common.NON_EXISTING_ID
        )

        # Act
        with pytest.raises(SubscriptionDoesNotExistError) as err:
            await self._command_invoker.invoke(create_room)

        # Assert
        assert err.value.title == "Subscription.Not_found"
        assert err.value.detail == "Subscription with the provided id not found"
        assert err.value.error_type == ErrorType.NOT_FOUND

    @pytest.mark.asyncio
    async def test_create_room_when_gym_not_exists_should_fail(self) -> None:
        # Arrange
        create_room = RoomCommandFactory.create_create_room_command(
            gym_id=constants.common.NON_EXISTING_ID,
            subscription_id=self._gym_db.subscription_id,
        )

        # Act
        with pytest.raises(GymDoesNotExistError) as err:
            await self._command_invoker.invoke(create_room)

        # Assert
        assert err.value.title == "Gym.Not_found"
        assert err.value.detail == "Gym with the provided id not found"
        assert err.value.error_type == ErrorType.NOT_FOUND

    @pytest.mark.asyncio
    async def test_create_room_when_more_than_subscription_allows_should_fail(self) -> None:
        # Arrange
        create_room = RoomCommandFactory.create_create_room_command(
            gym_id=self._gym_db.id,
            subscription_id=self._gym_db.subscription_id,
        )
        created_rooms: List[RoomDB] = []
        for _ in range(constants.subscription.MAX_ROOMS_FREE_TIER):
            created_rooms.append(await self._command_invoker.invoke(create_room))

        # Act
        with pytest.raises(GymCannotHaveMoreRoomsThanSubscriptionAllowsError) as err:
            await self._command_invoker.invoke(create_room)

        # Assert
        assert err.value.max_rooms == constants.subscription.MAX_ROOMS_FREE_TIER
        assert err.value.title == "Gym.Validation"
        assert err.value.detail == (
            f"A gym cannot have more rooms than the subscription allows. "
            f"Max rooms allowed: {constants.subscription.MAX_ROOMS_FREE_TIER}"
        )
        assert err.value.error_type == ErrorType.VALIDATION
        assert len(created_rooms) == constants.subscription.MAX_ROOMS_FREE_TIER
        assert all(isinstance(room, RoomDB) for room in created_rooms)
