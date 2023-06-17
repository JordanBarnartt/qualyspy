import datetime as dt
import ipaddress
from dataclasses import field
from typing import List, Optional

from pydantic.dataclasses import dataclass
from xsdata.formats.converter import converter

from . import converters

converter.register_converter(ipaddress.IPv4Address, converters.IPv4AddressConverter())
converter.register_converter(ipaddress.IPv6Address, converters.IPv6AddressConverter())
converter.register_converter(dt.timedelta, converters.TimeDeltaConverter())
converter.register_converter(str, converters.StrConverter())

DT_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


@dataclass
class AssetGroup:
    class Meta:
        name = "ASSET_GROUP"

    id: Optional[int] = field(
        default=None,
        metadata={
            "name": "ID",
            "type": "Element",
            "required": True,
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "name": "TITLE",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
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
            "format": DT_FORMAT,
        },
    )
    last_error_date: Optional[dt.datetime] = field(
        default=None,
        metadata={
            "name": "LAST_ERROR_DATE",
            "type": "Element",
            "format": DT_FORMAT,
        },
    )
    last_error: Optional[str] = field(
        default=None,
        metadata={
            "name": "LAST_ERROR",
            "type": "Element",
        },
    )


@dataclass
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
            "format": DT_FORMAT,
        },
    )


@dataclass
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


@dataclass
class IdSet:
    class Meta:
        name = "ID_SET"

    id: List[int] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
        },
    )
    id_range: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ID_RANGE",
            "type": "Element",
        },
    )


@dataclass
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


@dataclass
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
        },
    )


@dataclass
class User:
    class Meta:
        name = "USER"

    user_login: Optional[str] = field(
        default=None,
        metadata={
            "name": "USER_LOGIN",
            "type": "Element",
            "required": True,
        },
    )
    first_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "FIRST_NAME",
            "type": "Element",
            "required": True,
        },
    )
    last_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "LAST_NAME",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Value1:
    class Meta:
        name = "VALUE_1"

    ud_attr: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )


@dataclass
class Value2:
    class Meta:
        name = "VALUE_2"

    ud_attr: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )


@dataclass
class Value3:
    class Meta:
        name = "VALUE_3"

    ud_attr: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )


@dataclass
class VulnCount:
    class Meta:
        name = "VULN_COUNT"

    qds_severity: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    value: int = field(
        default=0,
        metadata={
            "required": True,
        },
    )


@dataclass
class Warning:
    class Meta:
        name = "WARNING"

    code: Optional[int] = field(
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


@dataclass
class ArsFactors:
    class Meta:
        name = "ARS_FACTORS"

    ars_formula: Optional[str] = field(
        default=None,
        metadata={
            "name": "ARS_FORMULA",
            "type": "Element",
            "required": True,
        },
    )
    vuln_count: List[VulnCount] = field(
        default_factory=list,
        metadata={
            "name": "VULN_COUNT",
            "type": "Element",
        },
    )


@dataclass
class AssetGroupList:
    class Meta:
        name = "ASSET_GROUP_LIST"

    asset_group: List[AssetGroup] = field(
        default_factory=list,
        metadata={
            "name": "ASSET_GROUP",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
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


@dataclass
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


@dataclass
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


@dataclass
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


@dataclass
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


@dataclass
class Tags:
    class Meta:
        name = "TAGS"

    tag: List[Tag] = field(
        default_factory=list,
        metadata={
            "name": "TAG",
            "type": "Element",
        },
    )


@dataclass
class UserDef:
    class Meta:
        name = "USER_DEF"

    label_1: Optional[str] = field(
        default=None,
        metadata={
            "name": "LABEL_1",
            "type": "Element",
        },
    )
    label_2: Optional[str] = field(
        default=None,
        metadata={
            "name": "LABEL_2",
            "type": "Element",
        },
    )
    label_3: Optional[str] = field(
        default=None,
        metadata={
            "name": "LABEL_3",
            "type": "Element",
        },
    )
    value_1: Optional[Value1] = field(
        default=None,
        metadata={
            "name": "VALUE_1",
            "type": "Element",
        },
    )
    value_2: Optional[Value2] = field(
        default=None,
        metadata={
            "name": "VALUE_2",
            "type": "Element",
        },
    )
    value_3: Optional[Value3] = field(
        default=None,
        metadata={
            "name": "VALUE_3",
            "type": "Element",
        },
    )


@dataclass
class UserList:
    class Meta:
        name = "USER_LIST"

    user: List[User] = field(
        default_factory=list,
        metadata={
            "name": "USER",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class Glossary:
    class Meta:
        name = "GLOSSARY"

    user_def: Optional[UserDef] = field(
        default=None,
        metadata={
            "name": "USER_DEF",
            "type": "Element",
        },
    )
    user_list: Optional[UserList] = field(
        default=None,
        metadata={
            "name": "USER_LIST",
            "type": "Element",
        },
    )
    asset_group_list: Optional[AssetGroupList] = field(
        default=None,
        metadata={
            "name": "ASSET_GROUP_LIST",
            "type": "Element",
        },
    )


@dataclass
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


@dataclass
class Request:
    class Meta:
        name = "REQUEST"

    datetime: Optional[dt.datetime] = field(
        default=None,
        metadata={
            "name": "DATETIME",
            "type": "Element",
            "required": True,
            "format": DT_FORMAT,
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


@dataclass
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
    asset_risk_score: Optional[int] = field(
        default=None,
        metadata={
            "name": "ASSET_RISK_SCORE",
            "type": "Element",
        },
    )
    asset_criticality_score: Optional[int] = field(
        default=None,
        metadata={
            "name": "ASSET_CRITICALITY_SCORE",
            "type": "Element",
        },
    )
    ars_factors: Optional[ArsFactors] = field(
        default=None,
        metadata={
            "name": "ARS_FACTORS",
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
    cloud_resource_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "CLOUD_RESOURCE_ID",
            "type": "Element",
        },
    )
    ec2_instance_id: Optional[str] = field(
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
    os: Optional[str] = field(
        default=None,
        metadata={
            "name": "OS",
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
    tags: Optional[Tags] = field(
        default=None,
        metadata={
            "name": "TAGS",
            "type": "Element",
        },
    )
    metadata: Optional[Metadata] = field(
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
    last_vuln_scan_datetime: Optional[dt.datetime] = field(
        default=None,
        metadata={
            "name": "LAST_VULN_SCAN_DATETIME",
            "type": "Element",
            "format": DT_FORMAT,
        },
    )
    last_vm_scanned_date: Optional[dt.datetime] = field(
        default=None,
        metadata={
            "name": "LAST_VM_SCANNED_DATE",
            "type": "Element",
            "format": DT_FORMAT,
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
            "format": DT_FORMAT,
        },
    )
    last_vm_auth_scanned_duration: Optional[dt.timedelta] = field(
        default=None,
        metadata={
            "name": "LAST_VM_AUTH_SCANNED_DURATION",
            "type": "Element",
        },
    )
    last_compliance_scan_datetime: Optional[dt.datetime] = field(
        default=None,
        metadata={
            "name": "LAST_COMPLIANCE_SCAN_DATETIME",
            "type": "Element",
            "format": DT_FORMAT,
        },
    )
    last_scap_scan_datetime: Optional[dt.datetime] = field(
        default=None,
        metadata={
            "name": "LAST_SCAP_SCAN_DATETIME",
            "type": "Element",
            "format": DT_FORMAT,
        },
    )
    owner: Optional[str] = field(
        default=None,
        metadata={
            "name": "OWNER",
            "type": "Element",
        },
    )
    comments: Optional[str] = field(
        default=None,
        metadata={
            "name": "COMMENTS",
            "type": "Element",
        },
    )
    user_def: Optional[UserDef] = field(
        default=None,
        metadata={
            "name": "USER_DEF",
            "type": "Element",
        },
    )
    asset_group_ids: Optional[str] = field(
        default=None,
        metadata={
            "name": "ASSET_GROUP_IDS",
            "type": "Element",
        },
    )


@dataclass
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


@dataclass
class Response:
    class Meta:
        name = "RESPONSE"

    datetime: Optional[dt.datetime] = field(
        default=None,
        metadata={
            "name": "DATETIME",
            "type": "Element",
            "required": True,
            "format": DT_FORMAT,
        },
    )
    host_list: Optional[HostList] = field(
        default=None,
        metadata={
            "name": "HOST_LIST",
            "type": "Element",
        },
    )
    id_set: Optional[IdSet] = field(
        default=None,
        metadata={
            "name": "ID_SET",
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
    glossary: Optional[Glossary] = field(
        default=None,
        metadata={
            "name": "GLOSSARY",
            "type": "Element",
        },
    )


@dataclass
class HostListOutput:
    class Meta:
        name = "HOST_LIST_OUTPUT"

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
