import pytest

from src.gym_management.domain.admin.exceptions import AdminDoesNotHaveSubscriptionSetError
from src.shared_kernel.application.error_or import ErrorType
from tests.common.gym_management.admin.factory.admin_factory import AdminFactory
from tests.common.gym_management.subscription.factory.subscription_factory import SubscriptionFactory


class TestAdminAggregate:
    def test_set_subscription_should_set_subscription_for_admin(self) -> None:
        # Arrange
        subscription = SubscriptionFactory.create_subscription()
        admin = AdminFactory.create_admin(subscription_id=None)

        # Act
        admin.set_subscription(subscription)

        # Assert
        assert admin.subscription_id == subscription.id

    def test_unset_subscription_when_no_subscription_set_should_fail(self) -> None:
        # Arrange
        subscription = SubscriptionFactory.create_subscription()
        admin = AdminFactory.create_admin(subscription_id=subscription.id)
        admin.unset_subscription(subscription)

        # Act
        with pytest.raises(AdminDoesNotHaveSubscriptionSetError) as err:
            admin.unset_subscription(subscription)

        # Assert
        assert err.value.title == "Admin.Unexpected"
        assert err.value.detail == "Admin with the provided id does not have a subscription set"
        assert err.value.error_type == ErrorType.UNEXPECTED
