from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import DependenciesContainer

# from app.domain import usecases

from .core import Core
from .managers import Managers
from .store import Store
from .validators import Validators


class Usecases(DeclarativeContainer):
    core: Core = DependenciesContainer()  # type: ignore
    store: Store = DependenciesContainer()  # type: ignore
    managers: Managers = DependenciesContainer()  # type: ignore
    validators: Validators = DependenciesContainer()  # type: ignore
