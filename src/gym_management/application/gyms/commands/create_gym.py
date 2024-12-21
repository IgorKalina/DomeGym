import logging
import uuid
from dataclasses import dataclass

from src.gym_management.application.common.interfaces.persistence.subscriptions_repository import (
    SubscriptionsRepository,
)
from src.gym_management.application.subscriptions.errors import SubscriptionDoesNotExist
from src.gym_management.domain.gym.aggregate_root import Gym
from src.shared_kernel.application.command import Command, CommandHandler
from src.shared_kernel.application.error_or import ErrorOr, ErrorResult, OkResult

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class CreateGym(Command):
    name: str
    subscription_id: uuid.UUID


class CreateGymHandler(CommandHandler):
    def __init__(self, subscriptions_repository: SubscriptionsRepository) -> None:
        self._subscriptions_repository = subscriptions_repository

    async def handle(self, command: CreateGym) -> ErrorOr[Gym]:
        subscription = await self._subscriptions_repository.get_by_id(command.subscription_id)
        if subscription is None:
            return ErrorResult(SubscriptionDoesNotExist())

        gym = Gym(name=command.name, max_rooms=subscription.max_rooms, subscription_id=command.subscription_id)
        add_gym_result: ErrorOr[Gym] = subscription.add_gym(gym)
        if add_gym_result.is_error():
            return add_gym_result

        await self._subscriptions_repository.update(subscription)
        return OkResult(gym)
