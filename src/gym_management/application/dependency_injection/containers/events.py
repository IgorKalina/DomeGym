from dependency_injector import containers, providers


class EventsContainer(containers.DeclarativeContainer):
    infrastructure = providers.DependenciesContainer()
