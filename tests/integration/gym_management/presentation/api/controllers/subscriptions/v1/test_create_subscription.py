from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from src.gym_management.infrastructure.subscriptions.repository.repository_memory import SubscriptionsMemoryRepository
from src.gym_management.presentation.api.controllers.subscriptions.v1.requests.create_subscription_request import (
    CreateSubscriptionRequest,
)
from tests.common.gym_management import constants

API_VERSION = "v1"


class TestCreateSubscription:
    @pytest.fixture(autouse=True)
    def setup_method(self, api_client: TestClient, subscriptions_repository: SubscriptionsMemoryRepository) -> None:
        self._api_client = api_client
        self._subscriptions_repository = subscriptions_repository

    @pytest.mark.asyncio
    async def test_when_request_valid_should_create_subscription(self) -> None:
        request = CreateSubscriptionRequest(
            admin_id=constants.admin.ADMIN_ID,
            subscription_type=constants.subscription.DEFAULT_SUBSCRIPTION_TYPE,
        )

        response = self._api_client.post(
            f"{API_VERSION}/subscriptions",
            json=request.model_dump(),
        )

        assert response.status_code == HTTPStatus.CREATED
