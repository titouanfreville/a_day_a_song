from copy import copy
from math import floor
from random import random
from typing import Callable, List, Set, Tuple

from .async_helpers import Asyncrange


class Generate:
    """Group all methods to generate new secrets"""

    class TooManyCodes(ValueError):
        def __init__(self, *args: object) -> None:
            super().__init__("Too much code asked", *args)

    ALPHA_NUMERIC = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    UPPER_ALPHA_NUMERIC = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    NUMERIC = "0123456789"
    CLEAR_ALPHA_NUMERIC = "123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ"

    @staticmethod
    def one_time_unique_code(chars=UPPER_ALPHA_NUMERIC, code_len: int = 6) -> Tuple[str, int]:
        """
        Generate a one time validation code using provided chars set.
        """

        OTP = ""
        length = len(chars)

        for _ in range(0, code_len):
            OTP += chars[floor(random() * length)]

        return OTP, code_len ** len(chars)

    @staticmethod
    async def generate_multiple(
        quantity: int,
        method: Callable[..., Tuple[str, int]],
        *args,
        existing_codes: Set[str] | None = None,
        **kwargs,
    ) -> List[str]:
        """
        Generate multiple code using provided generator method.
        Complementary args will be passed to call.
        Provide `existing_codes` parameter to ensure no duplicates.
        """

        initial_codes = existing_codes or set()
        existing_codes = copy(initial_codes)
        expected_elements = quantity + len(existing_codes)
        _, max_possibiles_code = method(*args, **kwargs)

        if expected_elements > max_possibiles_code:
            raise Generate.TooManyCodes()

        while len(existing_codes) < expected_elements:
            existing_codes.update(
                set([method(*args, **kwargs)[0] async for _ in Asyncrange(0, quantity)])
            )

        return list(existing_codes.difference(initial_codes))
