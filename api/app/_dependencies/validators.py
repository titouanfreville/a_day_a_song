# from app.adapters import validators
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import DependenciesContainer

from .store import Store


class Validators(DeclarativeContainer):
    store: Store = DependenciesContainer()  # type: ignore
