from app.core import logger
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Factory, Singleton

from .init_methods import _setup_logging, _setup_sentry, _setup_sqlalch


class Core(DeclarativeContainer):
    config = Configuration()

    logging = Singleton(_setup_logging, config)
    sentry = Singleton(_setup_sentry, config)

    logger = Factory(logger.Log, config)

    # ----------------------------------------
    # Database
    # ----------------------------------------
    postgres = Singleton(_setup_sqlalch, config)
