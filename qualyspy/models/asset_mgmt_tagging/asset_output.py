import datetime

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class Model(BaseModel):
    model_config = ConfigDict(validate_by_name=True, alias_generator=to_camel)


class TagSimple(Model):
    id: int
    name: str


class ListItem(Model):
    tag_simple: TagSimple = Field(alias="TagSimple")


class Tags(Model):
    list: list[ListItem]


class Asset(Model):
    id: int
    type: str | None = None
    created: datetime.datetime | None = None
    modified: datetime.datetime | None = None
    criticality_score: int | None = Field(alias="criticalityScore", default=None)
    name: str | None = None
    tags: Tags | None = None


class Datum(Model):
    asset: Asset = Field(alias="Asset")


class ServiceResponse(Model):
    data: list[Datum] | None = None
    response_code: str = Field(alias="responseCode")
    count: int | None = None


class Wrapper(Model):
    service_response: ServiceResponse = Field(alias="ServiceResponse")
