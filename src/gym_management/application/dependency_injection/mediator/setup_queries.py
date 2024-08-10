from src.gym_management.application.dependency_injection.containers import QueriesContainer
from src.gym_management.application.subscriptions.queries.list_subscriptions import ListSubscriptions
from src.shared_kernel.mediator.mediator import Mediator


async def setup_queries(mediator, queries: QueriesContainer) -> Mediator:
    mediator.register_query_handler(ListSubscriptions, handler=await queries.list_subscriptions_handler())
    return mediator
