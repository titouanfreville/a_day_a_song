from datetime import date, datetime
from typing import Any


def default_json_serializer(obj: Any) -> str:
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()

    try:
        return str(obj)
    except Exception as e:
        raise TypeError(f"Type {type(obj)} not serializable") from e
