import uuid
from typing import TYPE_CHECKING, List

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, status
from fastapi.routing import APIRouter

from src.gym_management.application.admin.exceptions import AdminAlreadyExistsError
from src.gym_management.application.subscription.commands.create_subscription import CreateSubscription
from src.gym_management.application.subscription.commands.remove_subscription import RemoveSubscription
from src.gym_management.application.subscription.queries.list_subscriptions import ListSubscriptions
from src.gym_management.infrastructure.common.injection.main import DiContainer
from src.gym_management.presentation.api.controllers.common.responses.dto import ErrorResponse, OkResponse
from src.gym_management.presentation.api.controllers.subscription.v1.requests.create_subscription_request import (
    CreateSubscriptionRequest,
)
from src.gym_management.presentation.api.controllers.subscription.v1.responses.subscription_response import (
    SubscriptionResponse,
)
from src.shared_kernel.application.command import CommandBus
from src.shared_kernel.application.query.interfaces.query_bus import QueryBus

if TYPE_CHECKING:
    from src.gym_management.domain.subscription.aggregate_root import Subscription

router = APIRouter(
    prefix="/v1/subscriptions",
    tags=["Subscriptions"],
)


@router.post(
    "",
    responses={
        status.HTTP_201_CREATED: {"model": OkResponse[SubscriptionResponse]},
        status.HTTP_409_CONFLICT: {"model": ErrorResponse[AdminAlreadyExistsError]},
    },
    response_model=OkResponse[SubscriptionResponse],
)
@inject
async def create_subscription(
    request: CreateSubscriptionRequest,
    command_bus: CommandBus = Depends(Provide[DiContainer.command_container.command_bus]),
) -> OkResponse[SubscriptionResponse]:
    command = CreateSubscription(subscription_type=request.subscription_type, admin_id=request.admin_id)
    subscription: Subscription = await command_bus.invoke(command)
    subscription_response = SubscriptionResponse(
        id=subscription.id,
        type=subscription.type,
        admin_id=subscription.admin_id,
        created_at=subscription.created_at,
        updated_at=subscription.updated_at,
    )
    return OkResponse(status=status.HTTP_201_CREATED, data=[subscription_response]).to_orjson()


@router.get(
    "",
    responses={
        status.HTTP_200_OK: {"model": OkResponse[SubscriptionResponse]},
    },
    response_model=OkResponse[SubscriptionResponse],
)
@inject
async def list_subscriptions(
    query_bus: QueryBus = Depends(Provide[DiContainer.query_container.query_bus]),
) -> OkResponse[SubscriptionResponse]:
    query = ListSubscriptions()
    result: List[Subscription] = await query_bus.invoke(query)
    subscriptions_response = [
        SubscriptionResponse(
            id=subscription.id,
            type=subscription.type,
            admin_id=subscription.admin_id,
            created_at=subscription.created_at,
            updated_at=subscription.updated_at,
        )
        for subscription in result
    ]
    return OkResponse(status=status.HTTP_200_OK, data=subscriptions_response).to_orjson()


@router.delete(
    "/{subscription_id}",
    responses={
        status.HTTP_200_OK: {"model": OkResponse[SubscriptionResponse]},
    },
    response_model=OkResponse[SubscriptionResponse],
)
@inject
async def delete_subscription(
    subscription_id: uuid.UUID,
    command_bus: CommandBus = Depends(Provide[DiContainer.command_container.command_bus]),
) -> OkResponse[SubscriptionResponse]:
    command = RemoveSubscription(subscription_id=subscription_id)
    subscription: Subscription = await command_bus.invoke(command)
    subscription_response = SubscriptionResponse(
        id=subscription.id,
        type=subscription.type,
        admin_id=subscription.admin_id,
        created_at=subscription.created_at,
        updated_at=subscription.updated_at,
    )
    return OkResponse(status=status.HTTP_200_OK, data=[subscription_response]).to_orjson()
