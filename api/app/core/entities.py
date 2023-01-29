from __future__ import annotations


from pydantic import BaseModel


class Filter(BaseModel):
    field: str
    operator: str
    value: str


class OrderBy(BaseModel):
    field: str
    desc: bool
