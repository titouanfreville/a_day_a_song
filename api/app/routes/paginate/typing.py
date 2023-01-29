from __future__ import annotations

import math
from typing import Generic, Sequence, TypeVar

from fastapi import Query
from pydantic import BaseModel, conint

from .bases import AbstractParams, BasePage, RawParams

T = TypeVar("T")


class Params(BaseModel, AbstractParams):
    page: int = Query(1, ge=1, description="Page number")
    nb_items: int = Query(50, ge=1, le=250, description="Number of items per page")

    def to_raw_params(self) -> RawParams:
        return RawParams(
            limit=self.nb_items,
            offset=self.nb_items * (self.page - 1),
        )


class Page(BasePage[T], Generic[T]):
    page: conint(ge=1)  # type: ignore
    nb_items: conint(ge=1)  # type: ignore

    __params_type__ = Params

    @classmethod
    def create(
        cls,
        items: Sequence[T],
        total: int,
        params: AbstractParams,
    ) -> Page[T]:
        if not isinstance(params, Params):
            raise ValueError("Page should be used with Params")

        return cls(
            total=total,
            items=items,
            page=params.page,
            nb_items=params.nb_items,
            total_page=math.ceil(total / params.nb_items),
        )
