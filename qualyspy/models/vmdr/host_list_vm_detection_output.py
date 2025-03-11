import datetime
import ipaddress

from pydantic_xml import BaseXmlModel, attr, element, wrapped


class ResponseWarning(BaseXmlModel):
    code: str = element(tag="CODE")
    text: str = element(tag="TEXT")
    url: str = element(tag="URL")


class QdsFactor(BaseXmlModel):
    name: str = attr(name="name")
    value: str | None


class Qds(BaseXmlModel):
    severity: str = attr(name="severity")
    score: int | None


class Detection(BaseXmlModel):
    unique_vuln_id: int = element(tag="UNIQUE_VULN_ID")
    qid: int = element(tag="QID")
    type: str = element(tag="TYPE")
    severity: int | None = element(tag="SEVERITY", default=None)
    port: int | None = element(tag="PORT", default=None)
    protocol: str | None = element(tag="PROTOCOL", default=None)
    fqdn: str | None = element(tag="FQDN", default=None)
    ssl: bool | None = element(tag="SSL", default=None)
    instance: str | None = element(tag="INSTANCE", default=None)
    results: str | None = element(tag="RESULTS", default=None)
    status: str | None = element(tag="STATUS", default=None)
    first_found_datetime: datetime.datetime | None = element(
        tag="FIRST_FOUND_DATETIME", default=None
    )
    last_found_datetime: datetime.datetime | None = element(
        tag="LAST_FOUND_DATETIME", default=None
    )
    qds: Qds | None = element(tag="QDS", default=None)
    qds_factors: list[QdsFactor] = wrapped(
        "QDS_FACTORS", element(tag="QDS_FACTOR", default_factory=list)
    )
    times_found: int | None = element(tag="TIMES_FOUND", default=None)
    last_test_datetime: datetime.datetime | None = element(
        tag="LAST_TEST_DATETIME", default=None
    )
    last_update_datetime: datetime.datetime | None = element(
        tag="LAST_UPDATE_DATETIME", default=None
    )
    last_fixed_datetime: datetime.datetime | None = element(
        tag="LAST_FIXED_DATETIME", default=None
    )
    first_reopened_datetime: datetime.datetime | None = element(
        tag="FIRST_REOPENED_DATETIME", default=None
    )
    last_reopened_datetime: datetime.datetime | None = element(
        tag="LAST_REOPENED_DATETIME", default=None
    )
    times_reopened: int | None = element(tag="TIMES_REOPENED", default=None)
    service: str | None = element(tag="SERVICE", default=None)
    is_ignored: bool | None = element(tag="IS_IGNORED", default=None)
    is_disabled: bool | None = element(tag="IS_DISABLED", default=None)
    affect_running_kernel: bool | None = element(
        tag="AFFECT_RUNNING_KERNEL", default=None
    )
    affect_running_service: bool | None = element(
        tag="AFFECT_RUNNING_SERVICE", default=None
    )
    affect_exploitable_config: bool | None = element(
        tag="AFFECT_EXPLOITABLE_CONFIG", default=None
    )
    last_processed_datetime: datetime.datetime | None = element(
        tag="LAST_PROCESSED_DATETIME", default=None
    )
    asset_cve: str | None = element(tag="ASSET_CVE", default=None)


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
    ec2: list[Attribute] = wrapped(
        "EC2", element(tag="ATTRIBUTE", default_factory=list)
    )
    google: list[Attribute] = wrapped(
        "GOOGLE", element(tag="ATTRIBUTE", default_factory=list)
    )
    azure: list[Attribute] = wrapped(
        "AZURE", element(tag="ATTRIBUTE", default_factory=list)
    )


class Tag(BaseXmlModel):
    tag_id: int | None = element(tag="TAG_ID")
    name: str = element(tag="NAME")
    color: str | None = element(tag="COLOR", default=None)
    background_color: str | None = element(tag="BACKGROUND_COLOR", default=None)


class DnsData(BaseXmlModel):
    hostname: str | None = element(tag="HOSTNAME", default=None)
    domain: str | None = element(tag="DOMAIN", default=None)
    fqdn: str | None = element(tag="FQDN", default=None)


class Host(BaseXmlModel):
    id: int = element(tag="ID")
    asset_id: int | None = element(tag="ASSET_ID", default=None)
    ip: ipaddress.IPv4Address = element(tag="IP", default=None)
    ipv6: ipaddress.IPv6Address | None = element(tag="IPV6", default=None)
    tracking_method: str | None = element(tag="TRACKING_METHOD", default=None)
    network_id: int | None = element(tag="NETWORK_ID", default=None)
    os: str | None = element(tag="OS", default=None)
    os_cpe: str | None = element(tag="OS_CPE", default=None)
    dns: str | None = element(tag="DNS", default=None)
    dns_data: DnsData | None = element(tag="DNS_DATA", default=None)
    cloud_provider: str | None = element(tag="CLOUD_PROVIDER", default=None)
    cloud_service: str | None = element(tag="CLOUD_SERVICE", default=None)
    cloud_resource_id: str | None = element(tag="CLOUD_RESOURCE_ID", default=None)
    ec2_instance_id: str | None = element(tag="EC2_INSTANCE_ID", default=None)
    netbios: str | None = element(tag="NETBIOS", default=None)
    qg_hostid: str | None = element(tag="QG_HOSTID", default=None)
    last_scan_datetime: datetime.datetime | None = element(
        tag="LAST_SCAN_DATETIME", default=None
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
    last_pc_scanned_date: datetime.datetime | None = element(
        tag="LAST_PC_SCANNED_DATE", default=None
    )
    tags: list[Tag] = wrapped("TAGS", element(tag="TAG", default_factory=list))
    metadata: Metadata | None = element(tag="METADATA", alias="metadata_", default=None)
    cloud_provider_tags: list[CloudTag] = wrapped(
        "CLOUD_PROVIDER_TAGS", element(tag="CLOUD_TAG", default_factory=list)
    )
    detections: list[Detection] = wrapped(
        "DETECTION_LIST", element(tag="DETECTION", default_factory=list)
    )


class Response(BaseXmlModel):
    response_datetime: datetime.datetime = element(tag="DATETIME")
    host_list: list[Host] | None = wrapped(
        "HOST_LIST", element(tag="HOST", default=None)
    )
    warning: ResponseWarning | None = element(tag="WARNING", default=None)


class Param(BaseXmlModel):
    key: str = element(tag="KEY")
    value: str = element(tag="VALUE")


class Request(BaseXmlModel):
    request_datetime: datetime.datetime = element(tag="DATETIME")
    user_login: str = element(tag="USER_LOGIN")
    resource: str = element(tag="RESOURCE")
    param_list: list[Param] | None = element(tag="PARAM_LIST")
    post_data: str | None = element(tag="POST_DATA")


class HostListVMDetectionOutput(BaseXmlModel, tag="HOST_LIST_VM_DETECTION_OUTPUT"):
    request: Request | None = element(tag="REQUEST", default=None)
    response: Response = element(tag="RESPONSE", default=None)
