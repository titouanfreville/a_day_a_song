"""
Initialize and manage dependencies injection.
Can be converted to a package if required.
"""

from app.routes import API
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Container, Singleton
from dependency_injector.wiring import Provide

from ._dependencies import Core, Endpoints, Managers, Middlewares, Store, Usecases, Validators


######### APPLICATION CONTAINERS #########
class BoyAPI(DeclarativeContainer):
    config = Configuration()

    core: Core = Container(Core, config=config)  # type: ignore

    store: Store = Container(Store, core=core)  # type: ignore
    validators: Validators = Container(Validators, store=store)  # type: ignore
    managers: Managers = Container(Managers, core=core, store=store)  # type: ignore

    usecase: Usecases = Container(  # type: ignore
        Usecases,
        core=core,
        validators=validators,
        store=store,
        managers=managers,
    )

    middlewares: Middlewares = Container(Middlewares, core=core, usecases=usecase)  # type: ignore
    endpoints: Endpoints = Container(Endpoints, usecase=usecase)  # type: ignore

    # ----------------------------------------
    # Transports
    # ----------------------------------------
    router = Singleton(
        API,
        endpoints.pings,
    )


######### IN APP SETUP #########
def setup_api_backgound(
    _log=Provide[BoyAPI.core.logging],
    # _sentry=Provide[BoyAPI.core.sentry],
    # _middlewares=Provide[BoyAPI.middlewares.checks],
):
    pass
