import logging
from typing import Dict, Tuple

import sentry_sdk

# from app.domain.interfaces.store import Transactions
from sentry_dramatiq import DramatiqIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine


######### MASKED SETUPS #########
def _setup_sqlalch(
    config,
) -> Tuple[AsyncEngine, Dict[str, AsyncEngine]]:
    def _init_engine(
        usr, pwd, hostname, database, adapter="postgresql", port="5432", opts="sslmode=disable"
    ) -> AsyncEngine:
        opts = opts.replace("sslmode", "ssl").replace("options", "server_settings")

        return create_async_engine(
            f"{adapter}+asyncpg://{usr}:{pwd}@{hostname}:{port}/{database}?{opts}",
            future=True,
            echo=True,
            pool_size=25,
            max_overflow=30,
            pool_pre_ping=True,
            pool_recycle=8 * 60,  # seconds
        )

    main_engine = _init_engine(
        config["postgres"]["user"],
        config["postgres"]["password"],
        config["postgres"]["host"],
        config["postgres"]["database"],
        adapter=config["postgres"]["adapter"],
        port=config["postgres"]["port"],
        opts=config["postgres"]["opts"],
    )

    # replicas = {}
    # replicas_key_order = [
    # ]
    # if config["postgres"]["replicas"] and "$" not in config["postgres"]["replicas"]:
    #     replicas_hosts = config["postgres"]["replicas"].split(",")

    #     for host in replicas_hosts:
    #         if not replicas_key_order:
    #             break

    #         replicas[replicas_key_order.pop(0)] = _init_engine(
    #             config["postgres"]["user"],
    #             config["postgres"]["password"],
    #             host,
    #             config["postgres"]["database"],
    #             config["postgres"]["adapter"],
    #             config["postgres"]["port"],
    #             config["postgres"]["opts"],
    #         )

    return main_engine, {}


def _setup_logging(config) -> None:
    handlers = [logging.StreamHandler()]  # set default logger to console
    # if config["log"]["log_handler"] == "gcp":
    #     logging_client = google_logging.Client()

    #     handler = CloudLoggingHandler(
    #         logging_client,
    #         name=config["log"]["name"],
    #     )
    #     setup_logging(
    #         handler,
    #         excluded_loggers=(
    #             "uvicorn",
    #             "uvicorn.error",
    #             "api.log",
    #             "usecases.admin_data",
    #             "usecases.conversation",
    #             "usecases.players",
    #             "usecases.match_search",
    #         ),
    #     )
    #     handlers.append(handler)  # add gcp logger if asked

    logging.basicConfig(
        format='{"level": "%(levelname)s", "name": "%(name)s", "at": "%(asctime)s", "message": %(message)s}',  # noqa: E501
        datefmt="%m/%d/%Y %I:%M:%S %p",
        level=logging.getLevelName(config["log"]["level"].upper()),
        force=True,
        handlers=handlers,
    )
    logging.getLogger("sqlalchemy.engine").setLevel(
        logging.getLevelName(config["log"]["level"].upper())
    )


def _setup_sentry(config) -> None:
    if config["sentry"]["enable"].lower() not in ("true", "t", "1", "0"):
        return

    sentry_sdk.init(
        config["sentry"]["url"],
        traces_sample_rate=float(config["sentry"]["trace_rate"]),
        environment=config["sentry"]["env"],
        integrations=[DramatiqIntegration(), RedisIntegration()],
        ignore_errors=config["sentry"]["ignore"].split(","),  # type: ignore
    )


all = [_setup_logging, _setup_sentry, _setup_sqlalch]
