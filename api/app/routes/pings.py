from fastapi import APIRouter

from .payloads import ResponsesDefinition


class Pings:
    ep = APIRouter(prefix="/ping", tags=["pings"])
    # __uc: usecases.Players

    # def __init__(self, usecase: usecases.Players):
    #     Pings.__uc = usecase

    @staticmethod
    @ep.api_route(
        "",
        response_model=str,
        responses=ResponsesDefinition.open_endpoints().build(),
        methods=["GET", "HEAD", "OPTIONS"],
    )
    async def ping_server():
        return "."
