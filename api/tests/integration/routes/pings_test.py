from apiist import HTTP
from pytest import mark
from tests.integration.setup import event_loop, mocked_server


class TestPingsEndpoints:
    class TestServerKeepAlive:
        @mark.asyncio
        async def test_keep_alive_ping_should_return_ok(self, event_loop, mocked_server: HTTP):
            (await mocked_server.async_get("/ping")).assert_ok().assert_in_body(".")
