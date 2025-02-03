from pydantic_xml import BaseXmlModel, element, wrapped, attr
import datetime
import ipaddress


class AssetGroup(BaseXmlModel):
    id: int = element(tag="ID")
    title: str = element(tag="TITLE")


class User(BaseXmlModel):
    user_login: str = element(tag="USER_LOGIN")
    first_name: str = element(tag="FIRST_NAME")
    last_name: str = element(tag="LAST_NAME")


class UserDef(BaseXmlModel):
    label_1: str | None = element(tag="LABEL_1", default=None)
    label_2: str | None = element(tag="LABEL_2", default=None)
    label_3: str | None = element(tag="LABEL_3", default=None)
    value_1: str | None = element(tag="VALUE_1", default=None)
    value_2: str | None = element(tag="VALUE_2", default=None)
    value_3: str | None = element(tag="VALUE_3", default=None)


class Glossary(BaseXmlModel):
    user_def: UserDef | None = element(tag="USER_DEF", default=None)
    user_list: list[User] | None = wrapped(
        "USER_LIST", element(tag="USER", default=None)
    )
    asset_group_list: list[AssetGroup] | None = wrapped(
        "ASSET_GROUP_LIST", element(tag="ASSET_GROUP", default=None)
    )


class ResponseWarning(BaseXmlModel):
    code: str = element(tag="CODE")
    text: str = element(tag="TEXT")
    url: str = element(tag="URL")


class IdSet(BaseXmlModel):
    id: list[int] | None = element(tag="ID", default=None)
    id_range: list[int] | None = element(tag="ID_RANGE", default=None)


class CloudTag(BaseXmlModel):
    name: str = element(tag="NAME")
    value: str = element(tag="VALUE")
    last_success_date: datetime.datetime = element(tag="LAST_SUCCESS_DATE")


class Attribute(BaseXmlModel):
    name: str = element(tag="NAME")
    last_status: str = element(tag="LAST_STATUS")
    value: str = element(tag="VALUE")
    last_success_date: datetime.datetime | None = element(
        tag="LAST_SUCCESS_DATE", default=None
    )
    last_error_date: datetime.datetime | None = element(
        tag="LAST_ERROR_DATE", default=None
    )
    last_error: str | None = element(tag="LAST_ERROR", default=None)


class Metadata(BaseXmlModel):
    ec2: list[Attribute] = wrapped("EC2", element(tag="ATTRIBUTE"))
    google: list[Attribute] = wrapped("GOOGLE", element(tag="ATTRIBUTE"))
    azure: list[Attribute] = wrapped("AZURE", element(tag="ATTRIBUTE"))


class Tag(BaseXmlModel):
    tag_id: int = element(tag="TAG_ID")
    name: str = element(tag="NAME")


class DnsData(BaseXmlModel):
    hostname: str | None = element(tag="HOSTNAME", default=None)
    domain: str | None = element(tag="DOMAIN", default=None)
    fqdn: str | None = element(tag="FQDN", default=None)


class VulnCount(BaseXmlModel):
    qds_severity: str = attr(name="qds_severity")
    count: int | None


class TruriskScoreFactors(BaseXmlModel):
    trurisk_score_formula: str | None = element(
        tag="TRURISK_SCORE_FORMULA", default=None
    )
    vuln_count: list[VulnCount] | None = element(tag="VULN_COUNT", default=None)


class Host(BaseXmlModel):
    id: int = element(tag="ID")
    asset_id: int | None = element(tag="ASSET_ID", default=None)
    ip: ipaddress.IPv4Address = element(tag="IP", default=None)
    ipv6: ipaddress.IPv6Address | None = element(tag="IPV6", default=None)
    trurisk_score: int | None = element(tag="TRURISK_SCORE", default=None)
    asset_criticality_score: int | None = element(
        tag="ASSET_CRITICALITY_SCORE", default=None
    )
    trurisk_score_factors: TruriskScoreFactors | None = element(
        tag="TRURISK_SCORE_FACTORS", default=None
    )
    tracking_method: str | None = element(tag="TRACKING_METHOD", default=None)
    network_id: int | None = element(tag="NETWORK_ID", default=None)
    dns: str | None = element(tag="DNS", default=None)
    dns_data: DnsData | None = element(tag="DNS_DATA", default=None)
    cloud_provider: str | None = element(tag="CLOUD_PROVIDER", default=None)
    cloud_service: str | None = element(tag="CLOUD_SERVICE", default=None)
    cloud_resource_id: str | None = element(tag="CLOUD_RESOURCE_ID", default=None)
    ec2_instance_id: str | None = element(tag="EC2_INSTANCE_ID", default=None)
    netbios: str | None = element(tag="NETBIOS", default=None)
    os: str | None = element(tag="OS", default=None)
    qg_hostid: str | None = element(tag="QG_HOSTID", default=None)
    last_boot: datetime.datetime | None = element(tag="LAST_BOOT", default=None)
    serial_number: str | None = element(tag="SERIAL_NUMBER", default=None)
    hardware_uuid: str | None = element(tag="HARDWARE_UUID", default=None)
    first_found_date: datetime.datetime | None = element(
        tag="FIRST_FOUND_DATE", default=None
    )
    last_activity: datetime.datetime | None = element(tag="LAST_ACTIVITY", default=None)
    agent_status: str | None = element(tag="AGENT_STATUS", default=None)
    cloud_agent_running_on: str | None = element(
        tag="CLOUD_AGENT_RUNNING_ON", default=None
    )
    tags: list[Tag] = wrapped("TAGS", element(tag="TAG", default_factory=list))
    metadata: Metadata | None = element(tag="METADATA", alias="metadata_", default=None)
    cloud_provider_tags: list[CloudTag] | None = wrapped(
        "CLOUD_PROVIDER_TAGS", element(tag="CLOUD_TAG", default=None)
    )
    last_vuln_scan_datetime: datetime.datetime | None = element(
        tag="LAST_VULN_SCAN_DATETIME", default=None
    )
    last_vm_scanned_date: datetime.datetime | None = element(
        tag="LAST_VM_SCANNED_DATE", default=None
    )
    last_vm_scanned_duration: int | None = element(
        tag="LAST_VM_SCANNED_DURATION", default=None
    )
    last_vm_auth_scanned_date: datetime.datetime | None = element(
        tag="LAST_VM_AUTH_SCANNED_DATE", default=None
    )
    last_vm_auth_scanned_duration: int | None = element(
        tag="LAST_VM_AUTH_SCANNED_DURATION", default=None
    )
    last_compliance_scan_datetime: datetime.datetime | None = element(
        tag="LAST_COMPLIANCE_SCAN_DATETIME", default=None
    )
    last_scap_scan_datetime: datetime.datetime | None = element(
        tag="LAST_SCAP_SCAN_DATETIME", default=None
    )
    owner: str | None = element(tag="OWNER", default=None)
    comments: str | None = element(tag="COMMENTS", default=None)
    user_def: UserDef | None = element(tag="USER_DEF", default=None)
    asset_group_ids: str | None = element(tag="ASSET_GROUP_IDS", default=None)


class Response(BaseXmlModel):
    response_datetime: datetime.datetime = element(tag="DATETIME")
    host_list: list[Host] | None = wrapped(
        "HOST_LIST", element(tag="HOST", default=None)
    )
    id_set: IdSet | None = element(tag="ID_SET", default=None)
    warning: ResponseWarning | None = element(tag="WARNING", default=None)
    glossary: Glossary | None = element(tag="GLOSSARY", default=None)


class Param(BaseXmlModel):
    key: str = element(tag="KEY")
    value: str = element(tag="VALUE")


class Request(BaseXmlModel):
    request_datetime: datetime.datetime = element(tag="DATETIME")
    user_login: str = element(tag="USER_LOGIN")
    resource: str = element(tag="RESOURCE")
    param_list: list[Param] = element(tag="PARAM_LIST")
    post_data: str = element(tag="POST_DATA")


class HostListOutput(BaseXmlModel, tag="HOST_LIST_OUTPUT"):
    request: Request | None = element(tag="REQUEST", default=None)
    response: Response = element(tag="RESPONSE")
