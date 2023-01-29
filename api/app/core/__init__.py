from random import choices
from string import ascii_letters
from uuid import UUID

from app.domain import errors

from .context import Context
from .entities import Filter, OrderBy
from .generators import Generate
from .list import List
from .logger import Log
from .serializers import default_json_serializer

all = [
    Context,
    Filter,
    List,
    Log,
    OrderBy,
    default_json_serializer,
    Generate,
]

MAX_ASYNC_RETRIES = 50


def rremove(alist, x):
    alist.pop(len(alist) - alist[::-1].index(x) - 1)


def safe_cast(val, to_type, default=None):
    try:
        if val:
            return to_type(val.strip().rstrip("\r\n"))
        else:
            return default
    except (ValueError, TypeError):
        return default


def new_anti_scrapping_headers() -> dict:
    return {
        "Accept": "application/json,*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-GB,en-US",
        "Referrer": "https://bet-on-you.com/api",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",  # noqa: E501
    }


def random_string(ln: int = 10) -> str:
    return "".join(choices(ascii_letters, k=ln))  # nosec


def async_should_retry(nb_try: int, exception: BaseException):
    return nb_try < MAX_ASYNC_RETRIES and not isinstance(
        exception,
        (
            errors.ErrNotFound,
            errors.ErrInvalidData,
            errors.ErrNonBlockingUnexpected,
            errors.ErrInvalidResponseFormat,
            errors.ErrUnexpectedResponse,
            errors.ErrUnauthorized,
            ValueError,
        ),
    )


def is_uuid(val: str, version: int = 4) -> bool:
    try:
        UUID(val, version=version)
    except ValueError:
        return False
    except Exception as e:
        raise e
    else:
        return True


async def degroup_errors(eg: ExceptionGroup) -> Exception:
    err = None
    level = 999999999

    for e in eg.exceptions:
        if isinstance(e, ExceptionGroup):
            e = await degroup_errors(e)

        for lv, kinds in errors.errors_priority.items():
            if isinstance(e, kinds) and lv == 0:
                return e
            elif isinstance(e, kinds) and level > lv:
                err = e
                level = lv
            else:
                err = e

    return err  # type: ignore
