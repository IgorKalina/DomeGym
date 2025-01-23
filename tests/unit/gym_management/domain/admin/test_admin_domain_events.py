from src.gym_management.domain.admin.events.subscription_removed_event import SubscriptionUnsetEvent
from src.gym_management.domain.admin.events.subscription_set_event import SubscriptionSetEvent
from tests.common.gym_management.admin.factory.admin_factory import AdminFactory
from tests.common.gym_management.subscription.factory.subscription_factory import SubscriptionFactory


class TestAdminDomainEvents:
    def test_set_subscription_should_create_subscription_set_domain_event(self) -> None:
        # Arrange
        subscription = SubscriptionFactory.create_subscription()
        admin = AdminFactory.create_admin(subscription_id=None)
        expected_domain_event = SubscriptionSetEvent(subscription=subscription)

        # Act
        admin.set_subscription(subscription)

        # Assert
        actual_domain_events = admin.pop_domain_events()
        assert len(actual_domain_events) == 1
        actual_domain_event = actual_domain_events[0]
        assert actual_domain_event == expected_domain_event

    def test_unset_subscription_should_create_subscription_unset_domain_event(self) -> None:
        # Arrange
        subscription = SubscriptionFactory.create_subscription()
        admin = AdminFactory.create_admin()
        admin.set_subscription(subscription)
        admin.pop_domain_events()  # clean up existing events after subscription was set
        expected_domain_event = SubscriptionUnsetEvent(subscription=subscription)

        # Act
        admin.unset_subscription(subscription)

        # Assert
        actual_domain_events = admin.pop_domain_events()
        assert len(actual_domain_events) == 1
        actual_domain_event = actual_domain_events[0]
        assert actual_domain_event == expected_domain_event
