from typing import Any
from typing import List as ListType


class List:
    @staticmethod
    def flatten(t):
        return [item for sublist in t for item in sublist]

    @staticmethod
    def unique(t):
        return list(set(t))

    @staticmethod
    def split(ids: ListType[Any], length: int) -> ListType[ListType[Any]]:
        subarray_len = len(ids) // length + (0 if len(ids) % length == 0 else 1)
        result: ListType[ListType[Any]] = [[]] * subarray_len

        for index in range(subarray_len):
            result[index] = ids[
                (index * length) : min(len(ids), (index + 1) * length)  # noqa: E203
            ]

        return result
