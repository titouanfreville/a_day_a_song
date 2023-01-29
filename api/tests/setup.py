from os import environ
from typing import Tuple

from coverage import process_startup
from pytest import fixture
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from tests.tools.database import data, psql

from .config import ACCESS_TOKEN, BASE_URL, pg_test_conf

process_startup()

pytest_plugins = ("pytest_asyncio",)


def set_environ():
    environ["POSTGRES_USER"] = pg_test_conf["user"]
    environ["POSTGRES_PASSWORD"] = pg_test_conf["password"]
    environ["BASE_URL"] = BASE_URL
    environ["LOG_HANDLER"] = "gcp"
    environ["TASK_BROKER"] = "stub"
    environ["API_KEY"] = ACCESS_TOKEN
    environ["POSTGRESQL_REPLICAS"] = ""

    if "FIRESTORE_EMULATOR_HOST" not in environ or not environ["FIRESTORE_EMULATOR_HOST"]:
        environ["FIRESTORE_EMULATOR_HOST"] = "firebase:8081"

    if "FIREBASE_AUTH_EMULATOR_HOST" not in environ or not environ["FIREBASE_AUTH_EMULATOR_HOST"]:
        environ["FIREBASE_AUTH_EMULATOR_HOST"] = "firebase:9190"


def pg_fixtures(base_path: str = "tests/integration/fixtures") -> data.Fixtures:
    set_environ()

    return psql.Fixtures().with_base_path(base_path)


def pg_asserts() -> data.Asserts:
    set_environ()

    return psql.Asserts()


def pg_requests() -> data.Request:
    set_environ()

    return psql.Requests()


def get_sql_engines() -> AsyncEngine:
    set_environ()

    adapter = environ["POSTGRES_ADAPTER"]
    pwd = environ["POSTGRES_PASSWORD"]
    usr = environ["POSTGRES_USER"]
    hostname = environ["POSTGRES_HOST"]
    port = environ["POSTGRES_PORT"]
    database = environ["POSTGRES_DB"]
    opts = environ["POSTGRES_OPTS"]

    return create_async_engine(
        f"{adapter}+asyncpg://{usr}:{pwd}@{hostname}:{port}/{database}?{opts}",
        future=True,
        echo=True,
        pool_size=25,
        max_overflow=30,
        pool_pre_ping=True,
        pool_recycle=8 * 60,  # seconds
    )


set_environ()
