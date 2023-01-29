from typing import Callable, List

from pytest import fixture


class CleanUp:
    def __init__(self) -> None:
        self.__clean_ups: List[Callable] = []

    def to_clean(self, call: Callable) -> None:
        self.__clean_ups.append(call)

    @fixture
    def clean_up(self):
        yield

        for clean_up in self.__clean_ups:
            clean_up()
