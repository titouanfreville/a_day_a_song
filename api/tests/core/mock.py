from typing import Any

from app.core import Context, Log
from elmock import Mock


class LogMock(Mock, Log):
    def __init__(self) -> None:
        pass

    def named(self, name: str) -> "Log":
        return self.execute("named", name)

    def context(self, ctx: Context) -> "Log":
        return self.execute("context", ctx)

    def method(self, method: str) -> "Log":
        return self.execute("method", method)

    def parameter(self, key: str, data: Any) -> "Log":
        return self.execute("parameter", key, data)

    def info(self, msg: str = None):
        return self.execute("info", msg=msg)

    def debug(self, msg: str = None):
        return self.execute("debug", msg=msg)

    def exception(self, err: Exception):
        return self.execute("exception", err)

    def error(self, msg: str = None, error: Exception = None):
        return self.execute("error", msg=msg, error=error)

    def warning(self, msg: str = None, error: Exception = None):
        return self.execute("warning", msg=msg, error=error)

    def success(self, msg: str = None):
        return self.execute("success", msg=msg)

    def _duplicate(self) -> "Log":
        return self.execute("_duplicate")
