import pydantic as pyd
from collections.abc import Callable

from .. import qutils


class Pagination_Settings(pyd.BaseModel):
    start_from_offset: int | None
    start_from_id: int | None
    limit_results: int | None

    class Config:
        alias_generator = qutils.to_lower_camel
        allow_population_by_field_name = True


class Field_Operator_Value(pyd.BaseModel):
    field: str
    value: str | int
    operator: str


class Filter(pyd.BaseModel):
    criteria: list[Field_Operator_Value]

    class Config:
        alias_generator: Callable[[str], str] = lambda s: s.capitalize()
        allow_population_by_field_name = True
