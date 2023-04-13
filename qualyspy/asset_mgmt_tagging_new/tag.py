import datetime
import enum
from typing import Any

import psycopg2.extensions
import pydantic as pd
import pydantic.networks
import pydantic.utils
import sqlalchemy as sa
import sqlalchemy.orm as orm

from .. import qualysapi, qutils


class Base(orm.DeclarativeBase):
    pass


Base.metadata.schema = "tag"


def adapt_pydantic_ip_address(ip: pd.IPvAnyAddress) -> Any:
    return psycopg2.extensions.AsIs(repr(ip.exploded))


psycopg2.extensions.register_adapter(
    pydantic.networks.IPv4Address, adapt_pydantic_ip_address  # type: ignore
)
psycopg2.extensions.register_adapter(
    pydantic.networks.IPv4Address, adapt_pydantic_ip_address  # type: ignore
)


class Tag_Rule_Type(enum.Enum):
    STATIC = "STATIC"
    GROOVY = "GROOVY"
    OS_REGEX = "OS_REGEX"
    NETWORK_RANGE = "NETWORK_RANGE"
    NETWORK_RANGE_ENHANCED = "NETWORK_RANGE_ENHANCED"
    NAME_CONTAINS = "NAME_CONTAINS"
    INSTALLED_SOFTWARE = "INSTALLED_SOFTWARE"
    OPEN_PORTS = "OPEN_PORTS"
    VULN_EXISTS = "VULN_EXISTS"
    ASSET_SEARCH = "ASSET_SEARCH"
    CLOUD_ASSET = "CLOUD_ASSET"
    BUSINESS_INFORMATION = "BUSINESS_INFORMATION"
    GLOBAL_ASSET_VIEW = "GLOBAL_ASSET_VIEW"


####################################################################################################
# Tag_Simple


class Tag_Simple(pd.BaseModel):
    id: int | None
    name: str

    class Config:
        orm_mode = True


####################################################################################################
# Tag_Simple_Q_List


class Tag_Simple_Q_List(pd.BaseModel):
    count: int | None
    list_: list[dict[str, Tag_Simple]] | None = pd.Field(None, alias="list")
    set: dict[str, list[Tag_Simple]] | None
    add: dict[str, list[Tag_Simple]] | None
    remove: dict[str, list[Tag_Simple]] | None
    update: dict[str, list[Tag_Simple]] | None

    class Config:
        orm_mode = True


####################################################################################################
# Tag


class Tag(pd.BaseModel):
    id: int | None
    name: str | None
    parent_tag_id: int | None
    created: datetime.datetime | None
    modified: datetime.datetime | None
    color: str | None
    rule_text: str | None
    rule_type: Tag_Rule_Type | None
    src_asset_group_id: int | None
    src_business_unit_id: int | None
    src_operating_system_name: str | None
    provider: str | None
    children: Tag_Simple_Q_List | None
    criticality_score: int | None
    description: str | None

    class Config:
        orm_mode = True
        alias_generator = qutils.to_lower_camel
        allow_population_by_field_name = True


####################################################################################################
# Input


####################################################################################################
# Response


class Response(pd.BaseModel):
    response_code: str
    count: int | None
    data: list[Tag] | None
    response_error_details: dict[str, str] | None

    class Config:
        alias_generator = qutils.to_lower_camel
        allow_population_by_field_name = True


####################################################################################################
# Create Tag


class Create_Tag:
    def __init__(self, conn: qualysapi.Connection, tag: Tag) -> None:
        self.conn = conn
        self.tag = tag

    def call(self) -> Response:
        data = {"ServiceRequest": {"data": {"Tag": self.tag.dict(exclude_unset=True)}}}
        r = self.conn.post(qutils.URLS["Create Tag"], data=data)
        r["data"] = [t["Tag"] for t in r["data"]]
        response = Response.parse_obj(r)
        if response.response_code != "SUCCESS":
            raise Exception(response)
        return response


class Update_Tag:
    def __init__(self, conn: qualysapi.Connection, tag: Tag) -> None:
        self.conn = conn
        self.tag = tag

    def call(self, input: Tag) -> Response:
        data = {"ServiceRequest": {"data": {"Tag": input.dict(exclude_unset=True)}}}
        r = self.conn.post(qutils.URLS["Update Tag"] + f"/{self.tag.id}", data=data)
        if r["data"] is not None:
            r["data"] = [t["Tag"] for t in r["data"]]
        response = Response.parse_obj(r)
        if response.response_code != "SUCCESS":
            raise Exception(response)
        return response
