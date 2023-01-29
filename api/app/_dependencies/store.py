# from app.adapters import stores
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import DependenciesContainer

from .core import Core


class Store(DeclarativeContainer):
    core: Core = DependenciesContainer()  # type: ignore

    # sqlTransactions = Factory(stores.SQLTransactions, core.async_postgres)
