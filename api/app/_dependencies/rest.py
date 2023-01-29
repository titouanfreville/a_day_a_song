from app.routes import pings as pings_ep

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import DependenciesContainer, Singleton

from .core import Core
from .usecases import Usecases


class Middlewares(DeclarativeContainer):
    core: Core = DependenciesContainer()  # type: ignore
    usecases: Usecases = DependenciesContainer()  # type: ignore

    # checks = Singleton(middlewares.Checks, usecases.auth, services.firebaseAuth, core.config)
    # prepare = Singleton(middlewares.Prepare)


class Endpoints(DeclarativeContainer):
    usecase: Usecases = DependenciesContainer()  # type: ignore

    pings = Singleton(pings_ep.Pings)
