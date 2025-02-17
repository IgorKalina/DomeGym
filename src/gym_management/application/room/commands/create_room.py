import typing
import uuid

from src.gym_management.application.common.interfaces.repository.gym_repository import GymRepository
from src.gym_management.application.common.interfaces.repository.subscription_repository import SubscriptionRepository
from src.gym_management.domain.room.aggregate_root import Room
from src.shared_kernel.application.command import Command, CommandHandler
from src.shared_kernel.application.event.domain.event_bus import DomainEventBus

if typing.TYPE_CHECKING:
    from src.gym_management.domain.gym.aggregate_root import Gym
    from src.gym_management.domain.subscription.aggregate_root import Subscription

    pass


class CreateRoom(Command):
    name: str
    subscription_id: uuid.UUID
    gym_id: uuid.UUID


class CreateRoomHandler(CommandHandler):
    def __init__(
        self,
        subscription_repository: SubscriptionRepository,
        gym_repository: GymRepository,
        domain_event_bus: DomainEventBus,
    ) -> None:
        self.__subscription_repository = subscription_repository
        self.__gym_repository = gym_repository

        self.__domain_event_bus = domain_event_bus

    async def handle(self, command: CreateRoom) -> Room:
        subscription: Subscription = await self.__subscription_repository.get(command.subscription_id)
        gym: Gym = await self.__gym_repository.get(command.gym_id)
        room = Room(gym_id=gym.id, name=command.name, max_daily_sessions=subscription.max_daily_sessions)
        gym.add_room(room)

        await self.__gym_repository.update(gym)
        await self.__domain_event_bus.publish(gym.pop_domain_events())
        return room
