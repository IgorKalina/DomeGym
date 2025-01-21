import uuid
from typing import List

from sqlalchemy import select

from src.gym_management.application.common.interfaces.repository.room_repository import RoomRepository
from src.gym_management.application.gym.dto.repository import GymDB
from src.gym_management.application.room.dto.repository import RoomDB
from src.gym_management.infrastructure.common.postgres import models
from src.gym_management.infrastructure.common.postgres.repository.sqlalchemy_repository import SQLAlchemyRepository


class RoomPostgresRepository(SQLAlchemyRepository, RoomRepository):
    async def get_by_id(self, room_id: uuid.UUID) -> RoomDB | None:
        query = select(models.Room).where(models.Room.id == room_id)
        result = await self._session.scalars(query)
        room: models.Room = result.one_or_none()
        return room.to_dto() if room else None

    async def create(self, room: RoomDB) -> None:
        gym = models.Room.from_dto(room)
        self._session.add(gym)
        await self._session.flush((gym,))
        await self._session.commit()

    async def get_by_gym_id(self, gym_id: uuid.UUID) -> List[GymDB]:
        query = select(models.Room).where(models.Room.gym_id == gym_id)
        result: List[models.Room] = await self._session.scalars(query)
        return [room.to_dto() for room in result]
