import datetime

from pydantic_xml import BaseXmlModel, element, wrapped


class Item(BaseXmlModel):
    key: str = element(tag="KEY")
    value: str = element(tag="VALUE")


class Response(BaseXmlModel):
    reponse_datetime: datetime.datetime = element(tag="DATETIME")
    code: str | None = element(tag="CODE", default=None)
    text: str = element(tag="TEXT")
    item_list: list[Item] | None = wrapped(
        "ITEM_LIST", element(tag="ITEM", default=None)
    )


class Param(BaseXmlModel):
    key: str = element(tag="KEY")
    value: str = element(tag="VALUE")


class Request(BaseXmlModel):
    request_datetime: datetime.datetime = element(tag="DATETIME")
    user_login: str = element(tag="USER_LOGIN")
    resource: str = element(tag="RESOURCE")
    param_list: list[Param] | None = element(tag="PARAM_LIST")
    post_data: str | None = element(tag="POST_DATA")


class SimpleReturn(BaseXmlModel, tag="SIMPLE_RETURN"):
    request: Request | None = element(tag="REQUEST", default=None)
    response: Response = element(tag="RESPONSE")
