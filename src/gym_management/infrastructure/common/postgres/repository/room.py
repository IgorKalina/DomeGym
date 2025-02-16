import uuid
from typing import List

from sqlalchemy import select

from src.gym_management.application.common.interfaces.repository.room_repository import RoomRepository
from src.gym_management.domain.room.aggregate_root import Room
from src.gym_management.domain.room.exceptions import RoomDoesNotExistError
from src.gym_management.infrastructure.common.postgres import models
from src.gym_management.infrastructure.common.postgres.repository.sqlalchemy_repository import SQLAlchemyRepository


class RoomPostgresRepository(SQLAlchemyRepository, RoomRepository):
    async def get(self, room_id: uuid.UUID) -> Room:
        room = await self.get_or_none(room_id)
        if not room:
            raise RoomDoesNotExistError()
        return room

    async def get_or_none(self, room_id: uuid.UUID) -> Room | None:
        query = select(models.Room).where(models.Room.id == room_id)
        result = await self._session.scalars(query)
        room: models.Room | None = result.one_or_none()
        if room is not None:
            return room.to_domain()
        return None

    async def create(self, room: Room) -> None:
        room_model: models.Room = models.Room.from_domain(room)
        self._session.add(room_model)
        await self._session.flush((room_model,))
        await self._session.commit()

    async def get_by_gym_id(self, gym_id: uuid.UUID) -> List[Room]:
        query = select(models.Room).where(models.Room.gym_id == gym_id)
        result: List[models.Room] = await self._session.scalars(query)
        return [room.to_domain() for room in result]

    async def delete(self, room: Room) -> None:
        room_model: models.Room = await self._session.get(models.Room, room.id)
        if not room_model:
            raise RoomDoesNotExistError()
        await self._session.delete(room_model)
        await self._session.commit()
