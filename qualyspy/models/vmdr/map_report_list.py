from pydantic_xml import BaseXmlModel, attr, element, wrapped


class OptionProfile(BaseXmlModel):
    option_profile_title: str = element(tag="OPTION_PROFILE_TITLE")
    option_profile_default: str | None = attr(
        name="option_profile_default", default=None
    )


class AssetGroup(BaseXmlModel):
    asset_group_title: str = element(tag="ASSET_GROUP_TITLE")


class MapReport(BaseXmlModel):
    title: str = element(tag="TITLE")
    asset_groups: list[AssetGroup] | None = wrapped(
        "ASSET_GROUPS", element(tag="ASSET_GROUP", default=None)
    )
    option_profile: OptionProfile | None = element(tag="OPTION_PROFILE", default=None)
    ref: str = attr(name="ref")
    date: str = attr(name="date")
    domain: str = attr(name="domain")
    status: str = attr(name="status")


class Error(BaseXmlModel):
    number: int | None = element(tag="NUMBER", default=None)
    value: str


class MapReportList(BaseXmlModel, tag="MAP_REPORT_LIST"):
    report_list: list[MapReport] | None = element(tag="MAP_REPORT", default=None)
    error: Error | None = element(tag="ERROR", default=None)
    user: str = attr(name="user")
    from_: str = attr(name="from")
    to: str = attr(name="to")
    with_domain: str | None = attr(name="with_domain", default=None)
