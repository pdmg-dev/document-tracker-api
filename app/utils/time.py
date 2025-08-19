from datetime import datetime, timezone
from typing import Optional, Union

import pytz


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def to_timezone(dt: Union[datetime, str], tz_name: str = "Asia/Manila") -> datetime:
    if isinstance(dt, str):
        dt = datetime.fromisoformat(dt)

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    target_tz = pytz.timezone(tz_name)
    return dt.astimezone(target_tz)


def format_datetime(dt: Union[datetime, str], tz_name: str = "Asia/Manila", fmt: Optional[str] = None) -> str:
    """
    Converts and formats a datetime for display in the target timezone.
    Default format is ISO 8601.
    """
    dt_local = to_timezone(dt, tz_name)
    fmt = fmt or "%Y-%m-%d %H:%M:%S %Z%z"
    return dt_local.strftime(fmt)


def parse_datetime(dt_str: str) -> datetime:
    """
    Parses an ISO 8601 datetime string into a timezone-aware datetime.
    Assumes UTC if no timezone is present.
    """
    dt = datetime.fromisoformat(dt_str)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt
