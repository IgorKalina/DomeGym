import typing

import pytest
from httpx import ASGITransport, AsyncClient

from src.gym_management.infrastructure.common.config import load_config
from src.gym_management.infrastructure.common.injection.main import DiContainer
from src.gym_management.presentation.api.api import init_api
from src.gym_management.presentation.api.controllers.gym.v1.responses.gym_response import GymResponse
from src.gym_management.presentation.api.controllers.room.v1.responses.room_response import RoomResponse
from src.gym_management.presentation.api.controllers.subscription.v1.responses.subscription_response import (
    SubscriptionResponse,
)
from tests.common.gym_management.gym.factory.gym_request_factory import GymRequestFactory
from tests.common.gym_management.gym.service.api.v1 import GymV1ApiService
from tests.common.gym_management.room.factory.room_request_factory import RoomRequestFactory
from tests.common.gym_management.room.service.api.v1 import RoomV1ApiService
from tests.common.gym_management.subscription.factory.subscription_request_factory import SubscriptionRequestFactory
from tests.common.gym_management.subscription.service.api.v1 import SubscriptionV1ApiService

if typing.TYPE_CHECKING:
    from src.gym_management.presentation.api.controllers.gym.v1.requests.create_gym_request import CreateGymRequest
    from src.gym_management.presentation.api.controllers.room.v1.requests.create_gym_request import CreateRoomRequest
    from src.gym_management.presentation.api.controllers.subscription.v1.requests.create_subscription_request import (
        CreateSubscriptionRequest,
    )


@pytest.fixture
async def api_client(di_container: DiContainer) -> AsyncClient:
    api = init_api(config=load_config().api)
    api.container.override(di_container)  # type: ignore
    async with AsyncClient(transport=ASGITransport(app=api), base_url="http://testserver") as async_client:
        yield async_client


@pytest.fixture
def subscription_v1_api(api_client: AsyncClient) -> SubscriptionV1ApiService:
    return SubscriptionV1ApiService(api_client)


@pytest.fixture
def gym_v1_api(api_client: AsyncClient) -> GymV1ApiService:
    return GymV1ApiService(api_client)


@pytest.fixture
def room_v1_api(api_client: AsyncClient) -> RoomV1ApiService:
    return RoomV1ApiService(api_client)


@pytest.fixture
async def subscription_v1(subscription_v1_api: SubscriptionV1ApiService) -> SubscriptionResponse:
    request: CreateSubscriptionRequest = SubscriptionRequestFactory.create_create_subscription_request()
    _, response_data = await subscription_v1_api.create(request)
    return response_data.data[0]


@pytest.fixture
async def gym_v1(subscription_v1: SubscriptionResponse, gym_v1_api: GymV1ApiService) -> GymResponse:
    request: CreateGymRequest = GymRequestFactory.create_create_gym_request()
    _, response_data = await gym_v1_api.create(request=request, subscription_id=subscription_v1.id)
    return response_data.data[0]


@pytest.fixture
async def room_v1(gym_v1: GymResponse, room_v1_api: RoomV1ApiService) -> RoomResponse:
    request: CreateRoomRequest = RoomRequestFactory.create_create_room_request()
    _, response_data = await room_v1_api.create(
        request=request,
        gym_id=gym_v1.id,
        subscription_id=gym_v1.subscription_id,
    )
    return response_data.data[0]
