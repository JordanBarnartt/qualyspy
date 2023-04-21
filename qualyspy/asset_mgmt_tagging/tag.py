import datetime
import enum
from typing import Any

import pydantic as pyd

from .. import qualysapi, qutils
from . import api_input


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


class Tag_Simple(pyd.BaseModel):
    id: int | None
    name: str | None

    class Config:
        orm_mode = True


####################################################################################################
# Tag_Simple_Q_List


class Tag_Simple_Q_List(pyd.BaseModel):
    count: int | None
    list_: list[dict[str, Tag_Simple]] | None = pyd.Field(None, alias="list")
    set: dict[str, list[Tag_Simple]] | None
    add: dict[str, list[Tag_Simple]] | None
    remove: dict[str, list[Tag_Simple]] | None
    upydate: dict[str, list[Tag_Simple]] | None

    class Config:
        orm_mode = True


####################################################################################################
# Tag


class Tag(pyd.BaseModel):
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
# Response


class Response(pyd.BaseModel):
    response_code: str
    count: int | None
    data: list[Tag] | None
    response_error_details: dict[str, str] | None

    class Config:
        alias_generator = qutils.to_lower_camel
        allow_population_by_field_name = True


def parse_response(response_obj: Any) -> Response:
    try:
        if response_obj["data"] is not None:
            response_obj["data"] = [t["Tag"] for t in response_obj["data"]]
    except KeyError:
        # No results returned.
        pass
    response = Response.parse_obj(response_obj)
    if response.response_code != "SUCCESS":
        raise ApiResponseError(response)
    parsed = Response.parse_obj(response)
    return parsed


####################################################################################################
# Exceptions


class ApiResponseError(Exception):
    def __init__(self, response: Response):
        self.response = response
        super().__init__(f"API response error: {response}")


####################################################################################################
# API Calls


class Create_Tag:
    def __init__(self, conn: qualysapi.Connection) -> None:
        self.conn = conn

    def __call__(self, tag: Tag) -> Response:
        data = {"ServiceRequest": {"data": {"Tag": tag.dict(exclude_unset=True)}}}
        r = self.conn.post(qutils.URLS["Create Tag"], data=data)
        response = parse_response(r)
        return response


class Update_Tag:
    def __init__(self, conn: qualysapi.Connection, tag: Tag) -> None:
        self.conn = conn
        self.tag = tag

    def __call__(self, input: Tag) -> Response:
        data = {"ServiceRequest": {"data": {"Tag": input.dict(exclude_unset=True)}}}
        r = self.conn.post(qutils.URLS["Update Tag"] + f"/{self.tag.id}", data=data)
        response = parse_response(r)

        return response


class Search_Tags:
    def __init__(self, conn: qualysapi.Connection) -> None:
        self.conn = conn

    def __call__(
        self,
        filter: api_input.Filter,
        pagination_settings: api_input.Pagination_Settings | None = None,
    ) -> Response:
        data = {
            "ServiceRequest": {
                "filters": filter.dict(exclude_unset=True, by_alias=True)
            },
        }
        if pagination_settings is not None:
            data["ServiceRequest"]["preferences"] = pagination_settings.dict(
                exclude_unset=True
            )
        r = self.conn.post(qutils.URLS["Search Tags"], data=data)
        response = parse_response(r)
        return response


class Count_Tags:
    def __init__(self, conn: qualysapi.Connection) -> None:
        self.conn = conn

    def __call__(self, filter: api_input.Filter) -> Response:
        data = {
            "ServiceRequest": {
                "filters": filter.dict(exclude_unset=True, by_alias=True)
            },
        }
        r = self.conn.post(qutils.URLS["Count Tags"], data=data)
        response = parse_response(r)
        return response


class Delete_Tag:
    def __init__(self, conn: qualysapi.Connection, tag: Tag) -> None:
        self.conn = conn
        self.tag = tag

    def __call__(self) -> Response:
        r = self.conn.post(qutils.URLS["Delete Tag"] + f"/{self.tag.id}")
        response = parse_response(r)
        return response


class Get_Tag_Info:
    def __init__(self, conn: qualysapi.Connection, tag: Tag) -> None:
        self.conn = conn
        self.tag = tag

    def __call__(self) -> Response:
        if self.tag.id is None:
            raise ValueError("Tag ID is required.")
        fvo = api_input.Field_Operator_Value(
            field="id", operator="EQUALS", value=self.tag.id
        )
        filter = api_input.Filter(criteria=[fvo])
        response = Search_Tags(self.conn)(filter)
        return response
