from random import randint
from typing import Any, List


def rand_in_list(vals: List[Any]) -> Any:
    return vals[randint(0, len(vals) - 1)]
