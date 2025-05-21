from pydantic_xml import BaseXmlModel, element, wrapped, attr
import datetime
import ipaddress


class ResponseWarning(BaseXmlModel):
    code: str | None = element(tag="CODE", default=None)
    text: str = element(tag="TEXT")
    url: str | None = element(tag="URL", default=None)


class NetBIOS(BaseXmlModel):
    network_id: str = attr(name="network_id", default="0")
    value: str


class DNS(BaseXmlModel):
    network_id: str = attr(name="network_id", default="0")
    value: str


class Domain(BaseXmlModel):
    netblock: str = attr(name="netblock", default="")
    network_id: str | None = attr(name="network_id", default=None)
    value: str


class IPRange(BaseXmlModel):
    network_id: str | None = attr(name="network_id", default=None)
    value: str


class IP(BaseXmlModel):
    network_id: str | None = attr(name="network_id", default=None)
    value: ipaddress.IPv4Address | ipaddress.IPv6Address


class IPSet(BaseXmlModel):
    ip: list[IP] | None = element(tag="IP", default=None)
    ip_range: list[IPRange] | None = element(tag="IP_RANGE", default=None)


class AssetGroup(BaseXmlModel):
    id: int = element(tag="ID")
    title: str | None = element(tag="TITLE", default=None)
    owner_user_id: str | None = element(tag="OWNER_USER_ID", default=None)
    owner_unit_id: str | None = element(tag="OWNER_UNIT_ID", default=None)
    network_id: str | None = element(tag="NETWORK_ID", default=None)
    network_ids: str | None = element(tag="NETWORK_IDS", default=None)
    last_update: datetime.datetime | None = element(tag="LAST_UPDATE", default=None)
    business_impact: str | None = element(tag="BUSINESS_IMPACT", default=None)
    cvss_enviro_cdp: str | None = element(tag="CVSS_ENVIRO_CDP", default=None)
    cvss_enviro_td: str | None = element(tag="CVSS_ENVIRO_TD", default=None)
    cvss_enviro_cr: str | None = element(tag="CVSS_ENVIRO_CR", default=None)
    cvss_enviro_ir: str | None = element(tag="CVSS_ENVIRO_IR", default=None)
    cvss_enviro_ar: str | None = element(tag="CVSS_ENVIRO_AR", default=None)
    default_appliance_id: str | None = element(tag="DEFAULT_APPLIANCE_ID", default=None)
    appliance_ids: str | None = element(tag="APPLIANCE_IDS", default=None)
    ip_set: IPSet | None = element(tag="IP_SET", default=None)
    domain_list: list[Domain] | None = wrapped(
        "DOMAIN_LIST", element(tag="DOMAIN", default=None)
    )
    dns_list: list[DNS] | None = wrapped("DNS_LIST", element(tag="DNS", default=None))
    netbios_list: list[NetBIOS] | None = wrapped(
        "NETBIOS_LIST", element(tag="NETBIOS", default=None)
    )
    host_ids: str | None = element(tag="HOST_IDS", default=None)
    ec2_ids: str | None = element(tag="EC2_IDS", default=None)
    assigned_user_ids: str | None = element(tag="ASSIGNED_USER_IDS", default=None)
    assigned_unit_ids: str | None = element(tag="ASSIGNED_UNIT_IDS", default=None)
    comments: str | None = element(tag="COMMENTS", default=None)
    owner_user_name: str | None = element(tag="OWNER_USER_NAME", default=None)


class IdSet(BaseXmlModel):
    id: list[int] | None = element(tag="ID", default=None)
    id_range: list[str] | None = element(tag="ID_RANGE", default=None)


class Response(BaseXmlModel):
    response_datetime: datetime.datetime = element(tag="DATETIME")
    asset_group_list: list[AssetGroup] | None = wrapped(
        "ASSET_GROUP_LIST", element(tag="ASSET_GROUP", default=None)
    )
    id_set: list[IdSet] | None = element(tag="ID_SET", default=None)
    warning: ResponseWarning | None = element(tag="WARNING", default=None)


class Param(BaseXmlModel):
    key: str = element(tag="KEY")
    value: str = element(tag="VALUE")


class Request(BaseXmlModel):
    request_datetime: datetime.datetime = element(tag="DATETIME")
    user_login: str = element(tag="USER_LOGIN")
    resource: str = element(tag="RESOURCE")
    param_list: list[Param] = wrapped("PARAM_LIST", element(tag="PARAM", default=None))
    post_data: str | None = element(tag="POST_DATA", default=None)


class AssetGroupListOutput(BaseXmlModel, tag="ASSET_GROUP_LIST_OUTPUT"):
    request: Request | None = element(tag="REQUEST", default=None)
    response: Response = element(tag="RESPONSE")
