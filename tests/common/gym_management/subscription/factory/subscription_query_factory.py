from src.gym_management.application.subscription.queries.list_subscriptions import ListSubscriptions


class SubscriptionQueryFactory:
    @staticmethod
    def create_list_subscription_query() -> ListSubscriptions:
        return ListSubscriptions()
