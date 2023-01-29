from datetime import datetime
from zoneinfo import ZoneInfo

from pytz import UTC, timezone

utc = ZoneInfo("UTC")


class Converts:
    @staticmethod
    def milli_to_seconds(val: int) -> int:
        return int(val) // 1000

    @staticmethod
    def to_utc(val: datetime) -> datetime:
        """Converts any datetime to utc"""
        if Utils.is_naive(val):
            return val.replace(tzinfo=utc)

        return val.astimezone(utc)

    @staticmethod
    def to_timezone(val: datetime, timezone: ZoneInfo) -> datetime:
        """Converts any datetime to provided timezone"""

        return Converts.to_utc(val).astimezone(timezone)


class Parse:
    @staticmethod
    def utc_from_milli_timestamp(timestamp: int) -> datetime:
        return datetime.fromtimestamp(Converts.milli_to_seconds(timestamp), UTC)


class Utils:
    @staticmethod
    def group_timezone(val: str) -> str:
        tz = timezone(val)
        offset = datetime.now(tz).strftime("%z")

        offset_int = int(offset)
        if offset_int < -100:
            return "timezone_america"

        if offset_int > 400:
            return "timezone_asia"

        return "timezone_europa"

    @staticmethod
    def is_naive(val: datetime) -> bool:
        """Check if datetime is naive"""

        return val.tzinfo is None or val.tzinfo.utcoffset(val) is None
