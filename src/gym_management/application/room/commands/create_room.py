import itertools
import typing
import uuid

from src.gym_management.application.common import dto
from src.gym_management.application.common.dto.repository.room import RoomDB
from src.gym_management.application.common.interfaces.repository.room_repository import RoomRepository
from src.gym_management.application.gym.queries.get_gym import GetGym
from src.gym_management.application.subscription.queries.get_subscription import GetSubscription
from src.gym_management.domain.gym.aggregate_root import Gym
from src.gym_management.domain.room.aggregate_root import Room
from src.gym_management.domain.subscription.aggregate_root import Subscription
from src.shared_kernel.application.command import Command, CommandHandler
from src.shared_kernel.application.event.domain.eventbus import DomainEventBus
from src.shared_kernel.application.query.interfaces.query_invoker import QueryInvoker
from src.shared_kernel.domain.common.aggregate_root import AggregateRoot

if typing.TYPE_CHECKING:
    from src.gym_management.application.common.dto.repository import GymDB, SubscriptionDB


class CreateRoom(Command):
    name: str
    subscription_id: uuid.UUID
    gym_id: uuid.UUID


class CreateRoomHandler(CommandHandler):
    def __init__(
        self,
        query_invoker: QueryInvoker,
        room_repository: RoomRepository,
        eventbus: DomainEventBus,
    ) -> None:
        self.__room_repository = room_repository
        self.__eventbus = eventbus

        self.__query_invoker = query_invoker

    async def handle(self, command: CreateRoom) -> RoomDB:
        subscription: Subscription = await self.__get_subscription(command)
        gym: Gym = await self.__get_gym(command, subscription=subscription)
        room = Room(gym_id=gym.id, name=command.name, max_daily_sessions=subscription.max_daily_sessions)
        gym.add_room(room)

        room_db: RoomDB = await self.__create_room_in_db(room=room, gym=gym)
        await self.__create_domain_events_in_db(aggregates=[subscription, gym, room])
        return room_db

    async def __get_subscription(self, command: CreateRoom) -> Subscription:
        get_subscription_query = GetSubscription(subscription_id=command.subscription_id)
        subscription_db: SubscriptionDB = await self.__query_invoker.invoke(get_subscription_query)
        return dto.mappers.subscription.db_to_domain(subscription_db)

    async def __get_gym(self, command: CreateRoom, subscription: Subscription) -> Gym:
        get_gym_query = GetGym(gym_id=command.gym_id, subscription_id=command.subscription_id)
        gym_db: GymDB = await self.__query_invoker.invoke(get_gym_query)
        return dto.mappers.gym.db_to_domain(gym=gym_db, subscription=subscription)

    async def __create_room_in_db(self, room: Room, gym: Gym) -> RoomDB:
        room_db: RoomDB = dto.mappers.room.domain_to_db(room=room, gym=gym)
        await self.__room_repository.create(room_db)
        return room_db

    async def __create_domain_events_in_db(self, aggregates: typing.List[AggregateRoot]) -> None:
        domain_events = list(itertools.chain.from_iterable([aggregate.pop_domain_events() for aggregate in aggregates]))
        await self.__eventbus.publish(domain_events)
