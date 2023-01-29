from asyncio import get_event_loop, new_event_loop

import pytest
from apiist import HTTP
from httpx import AsyncClient
from shortuuid import uuid
from tests.config import ACCESS_TOKEN
from tests.setup import set_environ

all = [ACCESS_TOKEN]


def mock_api():
    set_environ()

    from adas import serve

    return serve


@pytest.fixture(scope="session")
def mocked_server():
    serve = mock_api()

    yield HTTP(
        async_client=AsyncClient(app=serve, base_url=f"http://test_{uuid()}"), is_httpx=True
    )


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    try:
        loop = get_event_loop()
    except RuntimeError:
        loop = new_event_loop()

    yield loop

    loop.close()
