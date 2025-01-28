from pydantic_xml import BaseXmlModel, attr, element, wrapped


class Link(BaseXmlModel):
    value: str = attr(name="value")
    link: str | None = None


class Discovery(BaseXmlModel):
    method: str = attr(name="method")
    discovery: str | None = None


class Port(BaseXmlModel):
    value: str = attr(name="value")
    port: str | None = None


class Ip(BaseXmlModel):
    port: list[Port] | None = element(tag="PORT", default=None)
    discovery: list[Discovery] | None = element(tag="DISCOVERY", default=None)
    link: list[Link] | None = element(tag="LINK", default=None)
    value: str = attr(name="value")
    name: str | None = attr(name="name", default=None)
    type: str | None = attr(name="type", default=None)
    os: str | None = attr(name="os", default=None)
    account: str | None = attr(name="account", default=None)
    netbios: str | None = attr(name="netbios", default=None)
    network: str | None = attr(name="network", default=None)
    network_id: str | None = attr(name="network_id", default=None)


class OptionProfileTitle(BaseXmlModel):
    option_profile_default: str | None = attr("option_profile_default", default=None)
    option_profile_title: str


class OptionProfile(BaseXmlModel):
    option_profile_title: OptionProfileTitle = element(tag="OPTION_PROFILE_TITLE")


class Range(BaseXmlModel):
    start: str = element(tag="START")
    end: str = element(tag="END")


class Netblock(BaseXmlModel):
    range: list[Range] = element(tag="RANGE")


class UserEnteredDomains(BaseXmlModel):
    domain: list[str] = element(tag="DOMAIN")
    netblock: list[Netblock] | None = element(tag="NETBLOCK", default=None)


class AssetGroup(BaseXmlModel):
    asset_group_title: str = element(tag="ASSET_GROUP_TITLE")


class Key(BaseXmlModel):
    value: str = attr(name="value")
    key: str


class Header(BaseXmlModel):
    key: list[Key] = element(tag="KEY")
    asset_groups: list[AssetGroup] | None = wrapped(
        "ASSET_GROUPS", element(tag="ASSET_GROUP", default=None)
    )
    user_entered_domains: UserEnteredDomains | None = element(
        tag="USER_ENTERED_DOMAINS"
    )
    option_profile: OptionProfile | None = element(tag="OPTION_PROFILE")


class Error(BaseXmlModel):
    number: int | None = element(tag="NUMBER", default=None)
    value: str | None


class Map(BaseXmlModel, tag="MAP"):
    header: Header | None = element(tag="HEADER", default=None)
    ip: list[Ip] | None = element(tag="IP", default=None)
    error: Error | None = element(tag="ERROR", default=None)
    value: str | None = attr(name="value", default=None)
