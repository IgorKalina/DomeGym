from dependency_injector import containers, providers

from tests.common.admin.repositories import AdminsMemoryRepository
from tests.common.subscription.repositories import SubscriptionsMemoryRepository


class InfrastructureTestContainer(containers.DeclarativeContainer):
    admins_repository = providers.Singleton(AdminsMemoryRepository)
    subscriptions_repository = providers.Singleton(SubscriptionsMemoryRepository)
