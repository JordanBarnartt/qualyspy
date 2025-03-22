import datetime

from pydantic_xml import BaseXmlModel, element, wrapped


class OptionProfile(BaseXmlModel):
    title: str = element(tag="TITLE")
    default_flag: bool | None = element(tag="DEFAULT_FLAG", default=None)


class Status(BaseXmlModel):
    state: str = element(tag="STATE")
    sub_state: str | None = element(tag="SUB_STATE", default=None)


class Client(BaseXmlModel):
    id: int = element(tag="ID")
    name: str = element(tag="NAME")


class Scan(BaseXmlModel):
    id: int | None = element(tag="ID", default=None)
    ref: str = element(tag="REF")
    scan_type: str | None = element(tag="SCAN_TYPE", default=None)
    type: str = element(tag="TYPE")
    title: str = element(tag="TITLE")
    client: Client | None = element(tag="CLIENT", default=None)
    user_login: str = element(tag="USER_LOGIN")
    launch_datetime: datetime.datetime = element(tag="LAUNCH_DATETIME")
    duration: str = element(tag="DURATION")
    processing_priority: str | None = element(tag="PROCESSING_PRIORITY", default=None)
    processed: bool = element(tag="PROCESSED")
    status: Status | None = element(tag="STATUS", default=None)
    target: str | None = element(tag="TARGET", default=None)
    asset_group_title_list: list[str] | None = wrapped(
        "ASSET_GROUP_TITLE_LIST", element(tag="ASSET_GROUP_TITLE", default=None)
    )
    option_profile: OptionProfile | None = element(tag="OPTION_PROFILE", default=None)


class Response(BaseXmlModel):
    response_datetime: datetime.datetime = element(tag="DATETIME")
    scan_list: list[Scan] | None = wrapped(
        "SCAN_LIST", element(tag="SCAN", default=None)
    )


class Param(BaseXmlModel):
    key: str = element(tag="KEY")
    value: str = element(tag="VALUE")


class Request(BaseXmlModel):
    response_datetime: datetime.datetime = element(tag="DATETIME")
    user_login: str = element(tag="USER_LOGIN")
    resource: str = element(tag="RESOURCE")
    param_list: list[Param] | None = wrapped(
        "PARAM_LIST", element(tag="PARAM", default=None)
    )
    post_data: str | None = element(tag="POST_DATA")


class ScanListOutput(BaseXmlModel, tag="SCAN_LIST_OUTPUT"):
    request: Request | None = element(tag="REQUEST", default=None)
    response: Response = element(tag="RESPONSE")
