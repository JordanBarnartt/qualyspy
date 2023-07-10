import datetime
import enum
from typing import Any

import pydantic as pyd

from .. import qualysapi, qutils
from . import api_input, tag


class Asset_Type(enum.Enum):
    UKNOWN = "UNKNOWN"
    HOST = "HOST"
    SCANNER = "SCANNER"
    WEBAPP = "WEBAPP"
    MALWARE_DOMAIN = "MALWARE_DOMAIN"


####################################################################################################
# Asset


class Asset(pyd.BaseModel):
    id: int | None
    name: str | None
    created: datetime.datetime | None
    modified: datetime.datetime | None
    type: Asset_Type | None
    tags: tag.Tag_Simple_Q_List | None
    criticality_score: int | None

    class Config:
        orm_mode = True
        alias_generator = qutils.to_lower_camel
        allow_population_by_field_name = True


####################################################################################################
# Response


class Response(pyd.BaseModel):
    response_code: str
    count: int | None
    data: list[Asset] | None
    response_error_details: dict[str, str] | None

    class Config:
        alias_generator = qutils.to_lower_camel
        allow_population_by_field_name = True


def parse_response(response_obj: Any) -> Response:
    try:
        if response_obj["data"] is not None:
            response_obj["data"] = [t["Asset"] for t in response_obj["data"]]
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


class Get_Asset_Info:
    def __init__(self, conn: qualysapi.Connection, asset: Asset):
        self.conn = conn
        self.asset = asset

    def __call__(self) -> Response:
        r = self.conn.get(qutils.URLS["Get Asset Info"] + f"/{self.asset.id}")
        response = parse_response(r)
        return response


class Update_Asset:
    def __init__(self, conn: qualysapi.Connection, asset: Asset):
        self.conn = conn
        self.asset = asset

    def __call__(self, update: Asset) -> Response:
        data = {"ServiceRequest": {"data": {"Asset": update.dict(exclude_none=True)}}}
        r = self.conn.post(
            qutils.URLS["Update Asset"] + f"/{self.asset.id}", data=data
        )
        response = parse_response(r)
        return response


class Search_Assets:
    def __init__(self, conn: qualysapi.Connection):
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
        r = self.conn.post(qutils.URLS["Search Assets"], data=data)
        response = parse_response(r)
        return response


class Count_Assets:
    def __init__(self, conn: qualysapi.Connection):
        self.conn = conn

    def __call__(
        self,
        filter: api_input.Filter,
    ) -> Response:
        data = {
            "ServiceRequest": {
                "filters": filter.dict(exclude_unset=True, by_alias=True)
            },
        }
        r = self.conn.post(qutils.URLS["Count Assets"], data=data)
        response = parse_response(r)
        return response


class Delete_Asset:
    def __init__(self, conn: qualysapi.Connection, asset: Asset | None = None):
        self.conn = conn
        self.asset = asset

    def __call__(self, filter: api_input.Filter | None = None) -> Response:
        if self.asset is not None:
            if filter is not None:
                raise ValueError("Cannot specify both asset and filter.")
            # Single asset specified for deletion.
            r = self.conn.post(qutils.URLS["Delete Asset"] + f"/{self.asset.id}")
        elif filter is not None:
            # Multiple assets specified for deletion.
            data = {
                "ServiceRequest": {
                    "filters": filter.dict(exclude_unset=True, by_alias=True)
                },
            }
            r = self.conn.post(qutils.URLS["Delete Assets"], data=data)
        else:
            raise ValueError("Must specify either asset or filter.")

        response = parse_response(r)
        return response
