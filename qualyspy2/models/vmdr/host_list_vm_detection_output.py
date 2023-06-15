import datetime as dt
import ipaddress
from dataclasses import field
from typing import Any, List, Optional

from pydantic.dataclasses import dataclass
from xsdata.formats.converter import Converter, converter

dt_format = "%Y-%m-%dT%H:%M:%SZ"


class Config:
    orm_mode = True


class IPv4AddressConverter(Converter):
    def deserialize(
        self, value: str, **kwargs: dict[Any, Any]
    ) -> ipaddress.IPv4Address:
        return ipaddress.IPv4Address(value)

    def serialize(self, value: ipaddress.IPv4Address, **kwargs: dict[Any, Any]) -> str:
        return str(value)


class IPv6AddressConverter(Converter):
    def deserialize(
        self, value: str, **kwargs: dict[Any, Any]
    ) -> ipaddress.IPv6Address:
        return ipaddress.IPv6Address(value)

    def serialize(self, value: ipaddress.IPv6Address, **kwargs: dict[Any, Any]) -> str:
        return str(value)


class TimeDeltaConverter(Converter):
    def deserialize(self, value: str, **kwargs: dict[Any, Any]) -> dt.timedelta:
        return dt.timedelta(seconds=int(value))

    def serialize(self, value: dt.timedelta, **kwargs: dict[Any, Any]) -> str:
        return str(value.total_seconds())


class StrConverter(Converter):
    def deserialize(self, value: str, **kwargs: dict[Any, Any]) -> str:
        if value == "metadata":
            return "metadata_"
        return value

    def serialize(self, value: str, **kwargs: dict[Any, Any]) -> str:
        return str(value)


converter.register_converter(ipaddress.IPv4Address, IPv4AddressConverter())
converter.register_converter(ipaddress.IPv6Address, IPv6AddressConverter())
converter.register_converter(dt.timedelta, TimeDeltaConverter())


@dataclass(config=Config)
class Attribute:
    class Meta:
        name = "ATTRIBUTE"

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    last_status: Optional[str] = field(
        default=None,
        metadata={
            "name": "LAST_STATUS",
            "type": "Element",
            "required": True,
        },
    )
    value: Optional[str] = field(
        default=None,
        metadata={
            "name": "VALUE",
            "type": "Element",
            "required": True,
        },
    )
    last_success_date: Optional[dt.datetime] = field(
        default=None,
        metadata={
            "name": "LAST_SUCCESS_DATE",
            "type": "Element",
            "format": dt_format,
        },
    )
    last_error_date: Optional[dt.datetime] = field(
        default=None,
        metadata={
            "name": "LAST_ERROR_DATE",
            "type": "Element",
            "format": dt_format,
        },
    )
    last_error: Optional[str] = field(
        default=None,
        metadata={
            "name": "LAST_ERROR",
            "type": "Element",
        },
    )


@dataclass(config=Config)
class CloudTag:
    class Meta:
        name = "CLOUD_TAG"

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    value: Optional[str] = field(
        default=None,
        metadata={
            "name": "VALUE",
            "type": "Element",
            "required": True,
        },
    )
    last_success_date: Optional[dt.datetime] = field(
        default=None,
        metadata={
            "name": "LAST_SUCCESS_DATE",
            "type": "Element",
            "required": True,
            "format": dt_format,
        },
    )


@dataclass(config=Config)
class DnsData:
    class Meta:
        name = "DNS_DATA"

    hostname: Optional[str] = field(
        default=None,
        metadata={
            "name": "HOSTNAME",
            "type": "Element",
        },
    )
    domain: Optional[str] = field(
        default=None,
        metadata={
            "name": "DOMAIN",
            "type": "Element",
        },
    )
    fqdn: Optional[str] = field(
        default=None,
        metadata={
            "name": "FQDN",
            "type": "Element",
        },
    )


@dataclass(config=Config)
class Param:
    class Meta:
        name = "PARAM"

    key: Optional[str] = field(
        default=None,
        metadata={
            "name": "KEY",
            "type": "Element",
            "required": True,
        },
    )
    value: Optional[str] = field(
        default=None,
        metadata={
            "name": "VALUE",
            "type": "Element",
            "required": True,
        },
    )


@dataclass(config=Config)
class Qds:
    class Meta:
        name = "QDS"

    severity: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    value: Optional[int] = field(
        default=None,
        metadata={
            "required": True,
        },
    )


@dataclass(config=Config)
class QdsFactor:
    class Meta:
        name = "QDS_FACTOR"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    value: Optional[int] = field(
        default=None,
        metadata={
            "required": True,
        },
    )


@dataclass(config=Config)
class Tag:
    class Meta:
        name = "TAG"

    tag_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "TAG_ID",
            "type": "Element",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    color: Optional[str] = field(
        default=None,
        metadata={
            "name": "COLOR",
            "type": "Element",
        },
    )
    background_color: Optional[str] = field(
        default=None,
        metadata={
            "name": "BACKGROUND_COLOR",
            "type": "Element",
        },
    )


@dataclass(config=Config)
class Warning:
    class Meta:
        name = "WARNING"

    code: Optional[str] = field(
        default=None,
        metadata={
            "name": "CODE",
            "type": "Element",
        },
    )
    text: Optional[str] = field(
        default=None,
        metadata={
            "name": "TEXT",
            "type": "Element",
            "required": True,
        },
    )
    url: Optional[str] = field(
        default=None,
        metadata={
            "name": "URL",
            "type": "Element",
        },
    )


@dataclass(config=Config)
class Azure:
    class Meta:
        name = "AZURE"

    attribute: List[Attribute] = field(
        default_factory=list,
        metadata={
            "name": "ATTRIBUTE",
            "type": "Element",
        },
    )


@dataclass(config=Config)
class CloudProviderTags:
    class Meta:
        name = "CLOUD_PROVIDER_TAGS"

    cloud_tag: List[CloudTag] = field(
        default_factory=list,
        metadata={
            "name": "CLOUD_TAG",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass(config=Config)
class Ec2:
    class Meta:
        name = "EC2"

    attribute: List[Attribute] = field(
        default_factory=list,
        metadata={
            "name": "ATTRIBUTE",
            "type": "Element",
        },
    )


@dataclass(config=Config)
class Google:
    class Meta:
        name = "GOOGLE"

    attribute: List[Attribute] = field(
        default_factory=list,
        metadata={
            "name": "ATTRIBUTE",
            "type": "Element",
        },
    )


@dataclass(config=Config)
class ParamList:
    class Meta:
        name = "PARAM_LIST"

    param: List[Param] = field(
        default_factory=list,
        metadata={
            "name": "PARAM",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass(config=Config)
class QdsFactors:
    class Meta:
        name = "QDS_FACTORS"

    qds_factor: List[QdsFactor] = field(
        default_factory=list,
        metadata={
            "name": "QDS_FACTOR",
            "type": "Element",
        },
    )


@dataclass(config=Config)
class Tags:
    class Meta:
        name = "TAGS"

    tag: List[Tag] = field(
        default_factory=list,
        metadata={
            "name": "TAG",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass(config=Config)
class Detection:
    class Meta:
        name = "DETECTION"

    qid: Optional[int] = field(
        default=None,
        metadata={
            "name": "QID",
            "type": "Element",
            "required": True,
        },
    )
    type: Optional[str] = field(
        default=None,
        metadata={
            "name": "TYPE",
            "type": "Element",
            "required": True,
        },
    )
    severity: Optional[int] = field(
        default=None,
        metadata={
            "name": "SEVERITY",
            "type": "Element",
        },
    )
    port: Optional[int] = field(
        default=None,
        metadata={
            "name": "PORT",
            "type": "Element",
        },
    )
    protocol: Optional[str] = field(
        default=None,
        metadata={
            "name": "PROTOCOL",
            "type": "Element",
        },
    )
    fqdn: Optional[str] = field(
        default=None,
        metadata={
            "name": "FQDN",
            "type": "Element",
        },
    )
    ssl: Optional[bool] = field(
        default=None,
        metadata={
            "name": "SSL",
            "type": "Element",
        },
    )
    instance: Optional[str] = field(
        default=None,
        metadata={
            "name": "INSTANCE",
            "type": "Element",
        },
    )
    results: Optional[str] = field(
        default=None,
        metadata={
            "name": "RESULTS",
            "type": "Element",
        },
    )
    status: Optional[str] = field(
        default=None,
        metadata={
            "name": "STATUS",
            "type": "Element",
        },
    )
    first_found_datetime: Optional[dt.datetime] = field(
        default=None,
        metadata={
            "name": "FIRST_FOUND_DATETIME",
            "type": "Element",
            "format": dt_format,
        },
    )
    last_found_datetime: Optional[dt.datetime] = field(
        default=None,
        metadata={
            "name": "LAST_FOUND_DATETIME",
            "type": "Element",
            "format": dt_format,
        },
    )
    qds: Optional[Qds] = field(
        default=None,
        metadata={
            "name": "QDS",
            "type": "Element",
        },
    )
    qds_factors: Optional[QdsFactors] = field(
        default=None,
        metadata={
            "name": "QDS_FACTORS",
            "type": "Element",
        },
    )
    times_found: Optional[int] = field(
        default=None,
        metadata={
            "name": "TIMES_FOUND",
            "type": "Element",
        },
    )
    last_test_datetime: Optional[dt.datetime] = field(
        default=None,
        metadata={
            "name": "LAST_TEST_DATETIME",
            "type": "Element",
            "format": dt_format,
        },
    )
    last_update_datetime: Optional[dt.datetime] = field(
        default=None,
        metadata={
            "name": "LAST_UPDATE_DATETIME",
            "type": "Element",
            "format": dt_format,
        },
    )
    last_fixed_datetime: Optional[dt.datetime] = field(
        default=None,
        metadata={
            "name": "LAST_FIXED_DATETIME",
            "type": "Element",
            "format": dt_format,
        },
    )
    first_reopened_datetime: Optional[dt.datetime] = field(
        default=None,
        metadata={
            "name": "FIRST_REOPENED_DATETIME",
            "type": "Element",
            "format": dt_format,
        },
    )
    last_reopened_datetime: Optional[dt.datetime] = field(
        default=None,
        metadata={
            "name": "LAST_REOPENED_DATETIME",
            "type": "Element",
            "format": dt_format,
        },
    )
    times_reopened: Optional[int] = field(
        default=None,
        metadata={
            "name": "TIMES_REOPENED",
            "type": "Element",
        },
    )
    service: Optional[str] = field(
        default=None,
        metadata={
            "name": "SERVICE",
            "type": "Element",
        },
    )
    is_ignored: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IS_IGNORED",
            "type": "Element",
        },
    )
    is_disabled: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IS_DISABLED",
            "type": "Element",
        },
    )
    affect_running_kernel: Optional[bool] = field(
        default=None,
        metadata={
            "name": "AFFECT_RUNNING_KERNEL",
            "type": "Element",
        },
    )
    affect_running_service: Optional[bool] = field(
        default=None,
        metadata={
            "name": "AFFECT_RUNNING_SERVICE",
            "type": "Element",
        },
    )
    affect_exploitable_config: Optional[bool] = field(
        default=None,
        metadata={
            "name": "AFFECT_EXPLOITABLE_CONFIG",
            "type": "Element",
        },
    )
    last_processed_datetime: Optional[dt.datetime] = field(
        default=None,
        metadata={
            "name": "LAST_PROCESSED_DATETIME",
            "type": "Element",
            "format": dt_format,
        },
    )
    asset_cve: Optional[str] = field(
        default=None,
        metadata={
            "name": "ASSET_CVE",
            "type": "Element",
        },
    )


@dataclass(config=Config)
class Metadata:
    class Meta:
        name = "METADATA"

    ec2: List[Ec2] = field(
        default_factory=list,
        metadata={
            "name": "EC2",
            "type": "Element",
        },
    )
    google: List[Google] = field(
        default_factory=list,
        metadata={
            "name": "GOOGLE",
            "type": "Element",
        },
    )
    azure: List[Azure] = field(
        default_factory=list,
        metadata={
            "name": "AZURE",
            "type": "Element",
        },
    )


@dataclass(config=Config)
class Request:
    class Meta:
        name = "REQUEST"

    datetime: Optional[dt.datetime] = field(
        default=None,
        metadata={
            "name": "DATETIME",
            "type": "Element",
            "required": True,
            "format": dt_format,
        },
    )
    user_login: Optional[str] = field(
        default=None,
        metadata={
            "name": "USER_LOGIN",
            "type": "Element",
            "required": True,
        },
    )
    resource: Optional[str] = field(
        default=None,
        metadata={
            "name": "RESOURCE",
            "type": "Element",
            "required": True,
        },
    )
    param_list: Optional[ParamList] = field(
        default=None,
        metadata={
            "name": "PARAM_LIST",
            "type": "Element",
        },
    )
    post_data: Optional[str] = field(
        default=None,
        metadata={
            "name": "POST_DATA",
            "type": "Element",
        },
    )


@dataclass(config=Config)
class DetectionList:
    class Meta:
        name = "DETECTION_LIST"

    detection: List[Detection] = field(
        default_factory=list,
        metadata={
            "name": "DETECTION",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass(config=Config)
class Host:
    class Meta:
        name = "HOST"

    id: Optional[int] = field(
        default=None,
        metadata={
            "name": "ID",
            "type": "Element",
            "required": True,
        },
    )
    asset_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "ASSET_ID",
            "type": "Element",
        },
    )
    ip: Optional[ipaddress.IPv4Address] = field(
        default=None,
        metadata={
            "name": "IP",
            "type": "Element",
        },
    )
    ipv6: Optional[ipaddress.IPv6Address] = field(
        default=None,
        metadata={
            "name": "IPV6",
            "type": "Element",
        },
    )
    tracking_method: Optional[str] = field(
        default=None,
        metadata={
            "name": "TRACKING_METHOD",
            "type": "Element",
        },
    )
    network_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "NETWORK_ID",
            "type": "Element",
        },
    )
    os: Optional[str] = field(
        default=None,
        metadata={
            "name": "OS",
            "type": "Element",
        },
    )
    os_cpe: Optional[str] = field(
        default=None,
        metadata={
            "name": "OS_CPE",
            "type": "Element",
        },
    )
    dns: Optional[str] = field(
        default=None,
        metadata={
            "name": "DNS",
            "type": "Element",
        },
    )
    dns_data: Optional[DnsData] = field(
        default=None,
        metadata={
            "name": "DNS_DATA",
            "type": "Element",
        },
    )
    cloud_provider: Optional[str] = field(
        default=None,
        metadata={
            "name": "CLOUD_PROVIDER",
            "type": "Element",
        },
    )
    cloud_service: Optional[str] = field(
        default=None,
        metadata={
            "name": "CLOUD_SERVICE",
            "type": "Element",
        },
    )
    cloud_resource_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "CLOUD_RESOURCE_ID",
            "type": "Element",
        },
    )
    ec2_instance_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "EC2_INSTANCE_ID",
            "type": "Element",
        },
    )
    netbios: Optional[str] = field(
        default=None,
        metadata={
            "name": "NETBIOS",
            "type": "Element",
        },
    )
    qg_hostid: Optional[str] = field(
        default=None,
        metadata={
            "name": "QG_HOSTID",
            "type": "Element",
        },
    )
    last_scan_datetime: Optional[dt.datetime] = field(
        default=None,
        metadata={
            "name": "LAST_SCAN_DATETIME",
            "type": "Element",
            "format": dt_format,
        },
    )
    last_vm_scanned_date: Optional[dt.datetime] = field(
        default=None,
        metadata={
            "name": "LAST_VM_SCANNED_DATE",
            "type": "Element",
            "format": dt_format,
        },
    )
    last_vm_scanned_duration: Optional[dt.timedelta] = field(
        default=None,
        metadata={
            "name": "LAST_VM_SCANNED_DURATION",
            "type": "Element",
        },
    )
    last_vm_auth_scanned_date: Optional[dt.datetime] = field(
        default=None,
        metadata={
            "name": "LAST_VM_AUTH_SCANNED_DATE",
            "type": "Element",
            "format": dt_format,
        },
    )
    last_vm_auth_scanned_duration: Optional[dt.timedelta] = field(
        default=None,
        metadata={
            "name": "LAST_VM_AUTH_SCANNED_DURATION",
            "type": "Element",
        },
    )
    last_pc_scanned_date: Optional[dt.datetime] = field(
        default=None,
        metadata={
            "name": "LAST_PC_SCANNED_DATE",
            "type": "Element",
            "format": dt_format,
        },
    )
    tags: Optional[Tags] = field(
        default=None,
        metadata={
            "name": "TAGS",
            "type": "Element",
        },
    )
    metadata_: Optional[Metadata] = field(
        default=None,
        metadata={
            "name": "METADATA",
            "type": "Element",
        },
    )
    cloud_provider_tags: Optional[CloudProviderTags] = field(
        default=None,
        metadata={
            "name": "CLOUD_PROVIDER_TAGS",
            "type": "Element",
        },
    )
    detection_list: Optional[DetectionList] = field(
        default=None,
        metadata={
            "name": "DETECTION_LIST",
            "type": "Element",
            "required": True,
        },
    )


@dataclass(config=Config)
class HostList:
    class Meta:
        name = "HOST_LIST"

    host: List[Host] = field(
        default_factory=list,
        metadata={
            "name": "HOST",
            "type": "Element",
            "min_occurs": 1,
        },
    )

    def __add__(self, other: "HostList") -> "HostList":
        self.host.extend(other.host)
        return self


@dataclass(config=Config)
class Response:
    class Meta:
        name = "RESPONSE"

    datetime: Optional[dt.datetime] = field(
        default=None,
        metadata={
            "name": "DATETIME",
            "type": "Element",
            "required": True,
            "format": dt_format,
        },
    )
    host_list: Optional[HostList] = field(
        default=None,
        metadata={
            "name": "HOST_LIST",
            "type": "Element",
        },
    )
    warning: Optional[Warning] = field(
        default=None,
        metadata={
            "name": "WARNING",
            "type": "Element",
        },
    )


@dataclass(config=Config)
class HostListVmDetectionOutput:
    class Meta:
        name = "HOST_LIST_VM_DETECTION_OUTPUT"

    request: Optional[Request] = field(
        default=None,
        metadata={
            "name": "REQUEST",
            "type": "Element",
        },
    )
    response: Optional[Response] = field(
        default=None,
        metadata={
            "name": "RESPONSE",
            "type": "Element",
            "required": True,
        },
    )
