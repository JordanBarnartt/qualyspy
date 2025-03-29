from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class Model(BaseModel):
    model_config = ConfigDict(validate_by_name=True, alias_generator=to_camel)


class TagSimple(Model):
    id: int
    name: str


class ListItem(Model):
    tag_simple: TagSimple = Field(alias="TagSimple")


class Children(Model):
    list: list[ListItem]


class Tag(Model):
    id: int
    created: str | None = None
    modified: str | None = None
    name: str | None = None
    color: str | None = None
    children: Children | None = None


class Datum(Model):
    tag: Tag = Field(alias="Tag")


class ServiceResponse(Model):
    response_code: str
    data: list[Datum]
    count: int


class Wrapper(Model):
    service_response: ServiceResponse = Field(alias="ServiceResponse")
