# from app.adapters import managers
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import DependenciesContainer

from .core import Core
from .store import Store


class Managers(DeclarativeContainer):
    """
    Container to manage project dependencies.
    All default implementation specification goes there
    """

    core: Core = DependenciesContainer()  # type: ignore
    store: Store = DependenciesContainer()  # type: ignore
