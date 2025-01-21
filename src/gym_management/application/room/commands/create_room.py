import typing
import uuid

from src.gym_management.application.common.interfaces.repository.gym_repository import GymRepository
from src.gym_management.application.common.interfaces.repository.room_repository import RoomRepository
from src.gym_management.application.common.interfaces.repository.subscription_repository import SubscriptionRepository
from src.gym_management.application.gym.exceptions import GymDoesNotExistError
from src.gym_management.application.room.dto.repository import RoomDB
from src.gym_management.application.subscription.exceptions import SubscriptionDoesNotExistError
from src.gym_management.domain.gym.aggregate_root import Gym
from src.gym_management.domain.room.aggregate_root import Room
from src.gym_management.domain.subscription.aggregate_root import Subscription
from src.shared_kernel.application.command import Command, CommandHandler
from src.shared_kernel.application.event.domain.eventbus import DomainEventBus

if typing.TYPE_CHECKING:
    from src.gym_management.application.gym.dto.repository import GymDB
    from src.gym_management.application.subscription.dto.repository import SubscriptionDB


class CreateRoom(Command):
    name: str
    subscription_id: uuid.UUID
    gym_id: uuid.UUID


class CreateRoomHandler(CommandHandler):
    def __init__(
        self,
        subscription_repository: SubscriptionRepository,
        gym_repository: GymRepository,
        room_repository: RoomRepository,
        eventbus: DomainEventBus,
    ) -> None:
        self.__subscription_repository = subscription_repository
        self.__gym_repository = gym_repository
        self.__room_repository = room_repository
        self.__eventbus = eventbus

    async def handle(self, command: CreateRoom) -> RoomDB:
        subscription_db: SubscriptionDB | None = await self.__subscription_repository.get_by_id(command.subscription_id)
        if subscription_db is None:
            raise SubscriptionDoesNotExistError()

        gym_db: GymDB | None = await self.__gym_repository.get_by_id(command.gym_id)
        if gym_db is None:
            raise GymDoesNotExistError()
        gyms = await self.__gym_repository.get_by_subscription_id(command.subscription_id)
        rooms = await self.__room_repository.get_by_gym_id(command.gym_id)

        subscription = Subscription(
            id=subscription_db.id,
            type=subscription_db.type,
            admin_id=subscription_db.admin_id,
            gym_ids=[gym.id for gym in gyms],
        )
        room = Room(gym_id=gym_db.id, name=command.name, max_daily_sessions=subscription.max_daily_sessions)
        gym = Gym(
            id=gym_db.id,
            name=command.name,
            subscription_id=subscription.id,
            max_rooms=subscription.max_rooms,
            room_ids=[room.id for room in rooms],
        )
        gym.add_room(room)

        room_db: RoomDB = RoomDB(id=room.id, name=room.name, gym_id=gym_db.id, subscription_id=subscription.id)
        await self.__room_repository.create(room_db)
        await self.__eventbus.publish(
            subscription.pop_domain_events() + gym.pop_domain_events() + room.pop_domain_events()
        )
        return room_db
