from dependency_injector import containers, providers


class RepositoryContainer(containers.DeclarativeContainer):
    # todo: improve context of error thrown when repository is not defined
    admin_repository = providers.AbstractSingleton()
    subscription_repository = providers.AbstractSingleton()
    gym_repository = providers.AbstractSingleton()
    room_repository = providers.AbstractSingleton()
    failed_domain_event_repository = providers.AbstractSingleton()
