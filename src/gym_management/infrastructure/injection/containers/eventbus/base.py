from dependency_injector import containers, providers


class EventbusContainer(containers.DeclarativeContainer):
    broker = providers.AbstractSingleton()
    domain_event_publisher = providers.AbstractSingleton()
