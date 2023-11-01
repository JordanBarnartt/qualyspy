from pydantic import BaseModel
from pydantic.alias_generators import to_camel


class Model(BaseModel):
    class Config:
        populate_by_name = True
        alias_generator = to_camel


class TagSimple(Model):
    id: int
    name: str


class ListItem(Model):
    tag_simple: TagSimple


class Children(Model):
    list: list[ListItem]


class Tag(Model):
    created: str
    modified: str
    id: int
    name: str
    color: str
    children: Children


class Datum(Model):
    tag: Tag


class ServiceResponse(Model):
    response_code: str
    data: list[Datum]
    count: int


class Wrapper(Model):
    service_response: ServiceResponse
