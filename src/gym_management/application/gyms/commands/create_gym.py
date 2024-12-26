import logging
import uuid
from dataclasses import dataclass

from src.gym_management.application.common.interfaces.repository.subscriptions_repository import (
    SubscriptionsRepository,
)
from src.gym_management.application.subscriptions.exceptions import SubscriptionDoesNotExistError
from src.gym_management.domain.gym.aggregate_root import Gym
from src.shared_kernel.application.command import Command, CommandHandler

logger = logging.getLogger(__name__)


@dataclass(kw_only=True, frozen=True)
class CreateGym(Command):
    name: str
    subscription_id: uuid.UUID


class CreateGymHandler(CommandHandler):
    def __init__(self, subscriptions_repository: SubscriptionsRepository) -> None:
        self._subscriptions_repository = subscriptions_repository

    async def handle(self, command: CreateGym) -> Gym:
        subscription = await self._subscriptions_repository.get_by_id(command.subscription_id)
        if subscription is None:
            raise SubscriptionDoesNotExistError()

        gym = Gym(name=command.name, max_rooms=subscription.max_rooms, subscription_id=command.subscription_id)
        subscription.add_gym(gym)
        await self._subscriptions_repository.update(subscription)
        return gym
