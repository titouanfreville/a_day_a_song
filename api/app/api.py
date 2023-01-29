from asyncio import wait_for
from http import HTTPStatus
from sys import getsizeof

# from sys import getsizeof
from time import time_ns
from uuid import uuid4

from app.core import degroup_errors
from app.dependencies import BoyAPI
from app.domain.errors import ApiException, Details, ErrInvalidData, ErrNotFound, ErrUnauthorized
from asyncstdlib import itertools
from dependency_injector.wiring import Provide
from fastapi import HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sentry_sdk import capture_exception, push_scope

# from starlette.middleware.gzip import GZipMiddleware
from starlette.responses import StreamingResponse

from app import router


def run(
    _=Provide[BoyAPI.router],
    Log=Provide[BoyAPI.core.logger],
    # Prepare=Provide[BoyAPI.middlewares.prepare],
):
    @router.middleware("http")
    async def sentry_exception(request: Request, call_next):
        async def __init_scope(scope, level: str = "error"):
            scope.set_context("request", request)  # type:ignore

            user_id = (
                request.state.user.get("user_id")
                if hasattr(request, "state") and hasattr(request.state, "user")
                else "not identified"
            )

            scope.set_level(level)
            scope.user = {
                "ip_address": request.client.host if request.client else "undefined",
                "id": user_id,
            }

        async def __log_sentry(exception: Exception, level: str = "error"):
            with push_scope() as scope:  # type: ignore
                await __init_scope(scope, level)
                capture_exception(exception)

        try:
            return await call_next(request)

        except* (ErrUnauthorized, ErrNotFound, ErrInvalidData) as e:
            for err in e.exceptions:
                await __log_sentry(err, "info")

            raise e

        except* Exception as e:
            await __log_sentry(e)

            raise e

    @router.middleware("http")
    async def degroup_exceptions(req: Request, call_next):
        try:
            return await call_next(req)
        except ExceptionGroup as eg:
            raise await degroup_errors(eg)
        except Exception as e:
            raise e

    # Should always be the latests middleware
    @router.middleware("http")
    async def request(req: Request, call_next):
        async def __exec(__req: Request) -> StreamingResponse | JSONResponse:
            try:
                return await call_next(__req)
            except ApiException as e:
                return JSONResponse(
                    status_code=e.status,
                    content=jsonable_encoder(e.to_json()),
                )
            except ValueError as e:
                __log_error.error("Unexpected value error when processing request", e)
                valErr = ErrInvalidData("unknown", f"{e}")
                return JSONResponse(
                    status_code=valErr.status,
                    content=jsonable_encoder(valErr.to_json()),
                )
            except HTTPException as e:
                __log_error.error("Unexpected error when processing request", e)
                return JSONResponse(status_code=e.status_code, content={"ERROR": e.detail})
            except Exception as e:
                __log_error.error("Unexpected error when processing request", e)
                return JSONResponse(
                    status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                    content=jsonable_encoder("Internal error"),
                )

        async def __parse_body(_resp) -> str:
            MAX_BODY_BYTES_SIZE = 250_000
            body = ""
            if hasattr(_resp, "body_iterator"):
                body_data = itertools.tee(response.body_iterator, 2)  # type: ignore
                body = "\n".join([chunk.decode("utf-8") async for chunk in body_data[0] if chunk])
                response.body_iterator = body_data[1]  # type: ignore
            elif hasattr(_resp, "body"):
                body = response.body.decode("utf-8")

            return body if getsizeof(body) < MAX_BODY_BYTES_SIZE else "OVERWEIGHTED_BODY"

        __log = Log.named("api.log")
        __log_error = Log.named("core.middleware")
        request_id = req.headers.get("X-Request-ID", uuid4().__str__())

        __log = __log.parameter("request_id", request_id)
        __log_error = __log_error.parameter("request_id", request_id)

        req.state.request_id = request_id

        start = time_ns()

        response = await __exec(req)

        response.headers.append("X-Request-ID", request_id)
        end = time_ns()

        # Compute REQUEST LOGS
        if hasattr(req.state, "user"):
            __log = __log.parameter("user_id", req.state.user.get("user_id"))
            __log = __log.parameter("nickname", req.state.user.get("name"))

        # Compute data to log
        log_request = {
            "headers": {header: req.headers.get(header) for header in req.headers},
            "url": req.url.__str__(),
            "method": req.method,
            "status": response.status_code,
            "latency": f"{(end - start)/1_000_000_000:.9f}s",
        }

        # COMPUTE RESPONSE LOG
        try:
            body = await wait_for(__parse_body(response), timeout=2)
        except TimeoutError:
            body = "Could not retrieve: TIMEOUT"

        # Emit log
        __log.parameter(
            "response",
            {
                "body": body,
                "headers": {header: req.headers.get(header) for header in req.headers},
            },
        ).request(Log.Request(**log_request))

        if response.status_code >= 500:
            __log.error()
        elif response.status_code >= 400:
            __log.warning()
        else:
            __log.info()

        return response

    @router.middleware("http")
    async def user_lang(req: Request, call_next):
        # Prepare.user_lang(req)
        return await call_next(req)

    @router.exception_handler(RequestValidationError)
    async def convert_default_request_validation_to_bet_invalid_datas(
        _: Request, exc: RequestValidationError
    ):
        details = []
        for detail in exc.errors():
            err_location = detail.get("loc")
            msg = detail.get("msg", "").split(";", 1)
            key = "undefined"
            val = None

            if err_location:
                if err_location[0] == "body" and len(err_location) >= 2:
                    key = err_location[1]  # type: ignore
                    val = exc.body.get(key) if exc.body else None

            expected_values = None
            if len(msg) > 1:
                expected_values = [
                    val.strip().strip("'")
                    for val in msg[1].strip().removeprefix("permitted:").strip().split(",")
                ]

            details.append(
                Details(
                    key=key,
                    message=msg[0],
                    value={
                        "actual": val,
                        "expected": expected_values,
                    },
                )
            )

        e = ErrInvalidData("body", "bad request data", details)
        raise e

    # router.add_middleware(GZipMiddleware)

    return router


# def task_dashboard(dash=Provide[BoyTasksDashboard.dash]):
#     return dash.app
