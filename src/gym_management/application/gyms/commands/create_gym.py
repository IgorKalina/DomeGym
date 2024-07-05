import logging
import uuid
from dataclasses import dataclass

from result import Ok, Result

from src.gym_management.application.common.command import Command, CommandHandler
from src.gym_management.application.common.interfaces.persistence.subscriptions_repository import (
    SubscriptionsRepository,
)
from src.gym_management.domain.common import errors
from src.gym_management.domain.gym.aggregate_root import Gym

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class CreateGym(Command):
    name: str
    subscription_id: uuid.UUID


class CreateGymHandler(CommandHandler):
    def __init__(self, subscriptions_repository: SubscriptionsRepository) -> None:
        self._subscriptions_repository = subscriptions_repository

    async def handle(self, command: CreateGym) -> Result:
        subscription = await self._subscriptions_repository.get_by_id(command.subscription_id)
        if subscription is None:
            return errors.NotFoundError(
                title="Subscription not found",
                description="Subscription with the provided id not found",
            )
        gym = Gym(name=command.name, max_rooms=subscription.max_rooms, subscription_id=command.subscription_id)
        add_gym_result = subscription.add_gym(gym)
        if add_gym_result.is_err():
            return add_gym_result

        await self._subscriptions_repository.update(subscription)
        return Ok(None)
