import dataclasses
import datetime
import ipaddress
from collections.abc import MutableSequence
from typing import Optional, Union

import qualyspy.qualysapi as qualysapi
import qualyspy.qutils as qutils


@dataclasses.dataclass
class Warning:
    """A warning which appears when the API request reaches the truncation limit."""

    text: str
    """The warning message text."""

    code: Optional[str] = None
    """The warning code."""

    url: Optional[str] = None
    """The URL for making another request for the next batch of host records."""


@dataclasses.dataclass
class Detection:
    """A vulnerability detected on an asset."""

    qid: int
    """The QID for the vulnerability in the detection record."""

    type: str
    """The type of vulnerability in the detection record: Confirmed for a confirmed vulnerability,
    Potential for a potential vulnerability, and Info for an information gathered.
    """

    severity: Optional[int] = None
    """The severity of the vulnerability."""

    port: Optional[int] = None
    """The port number that the vulnerability was detected on."""

    protocol: Optional[str] = None
    """The protocol the vulnerability was detected on."""

    fqdn: Optional[str] = None
    """The Fully Qualified Domain Name (FQDN) of the host."""

    ssl: Optional[bool] = None
    """The value True is returned if the vulnerability was detected over SSL. The value False is
    returned if the vulnerability was not detected over SSL. This element is not returned for
    information gathered.
    """

    instance: Optional[str] = None
    """The Oracle DB instance the vulnerability was detected on."""

    results: Optional[str] = None
    """The scan test results, if any, returned by the service for the detection record."""

    status: Optional[str] = None
    """The current vulnerability status of the vulnerability in the detection record."""

    first_found_datetime: Optional[datetime.datetime] = None
    """The date/time when the vulnerability was first found."""

    last_found_datetime: Optional[datetime.datetime] = None
    """The most recent date/time when the vulnerability was found."""

    qds: Optional[int] = None
    """The Qualys Detection Score (QDS) for the vulnerability detection. The Qualys Detection Score
    (QDS) is assigned to vulnerabilities detected by Qualys. QDS is derived from multiple
    contributing factors, including vulnerability technical details (e.g. CVSS score),
    vulnerability temporal details (e.g. external threat intelligence like exploit code maturity),
    and remediation controls applied to mitigate the risk from the vulnerability. QDS has a range
    from 1 to 100 with these severity levels:
    - Critical (90-100)
    - High (70-89)
    - Medium (40-69)
    - Low (1-39)
    """

    qds_factors: Optional[str] = None
    """Factors that contributed to the QDS, and their names."""

    times_found: Optional[int] = None
    """The number of times the vulnerability was detected on the host."""

    last_test_datetime: Optional[datetime.datetime] = None
    """The most recent date/time when the vulnerability was tested."""

    last_update_datetime: Optional[datetime.datetime] = None
    """The most recent date/time when the detection record was updated."""

    last_fixed_datetime: Optional[datetime.datetime] = None
    """The date/time when the vulnerability was verified fixed by a scan."""

    first_reopened_datetime: Optional[datetime.datetime] = None
    """The date/time when the vulnerability was reopened by a scan."""

    last_reopened_datetime: Optional[datetime.datetime] = None
    """The date/time when the vulnerability was last reopened by a scan."""

    times_reopened: Optional[int] = None
    """The number of times the vulnerability was reopened by a scan."""

    service: Optional[str] = None
    """The service the vulnerability was detected on, if applicable."""

    is_ignored: Optional[bool] = None
    """A flag indicating whether the vulnerability is ignored for the particular host. A value of
    True means it is ignored, a value of False means it is not ignored.
    """

    is_disabled: Optional[bool] = None
    """A flag indicating whether the vulnerability is globally disabled for all hosts. A value of
    True means it is disabled, a value of False means it is not disabled.
    """

    affect_running_kernel: Optional[bool] = None
    """A flag identifying vulnerabilities found on running or non-running Linux kernels. A value of
    True indicates that the QID is exploitable because it was found on a running kernel. A value of
    False indicates that it is not exploitable because it was found on a non-running kernel. This
    element is returned only if the API request includes the parameter arf_kernel_filter set to 0,
    1, 2, 3 or 4 or active_kernels_only set to 0, 1, 2 or 3."""

    affect_running_service: Optional[bool] = None
    """A flag identifying vulnerabilities found on running or non-running services. A value of True
    indicates that the QID is not exploitable because it was found on non-running port/service. A
    value of False indicates that it is exploitable because it was found on a running port/service.
    This element is returned only if the API request includes the parameter arf_service_filter set
    to 0, 1, 2, 3 or 4."""

    affect_exploitable_config: Optional[bool] = None
    """A flag identifying vulnerabilities that may or may not be exploitable due to the current host
    configuration. A value of True indicates that the QID is not exploitable due to the current host
    configuration. A value of False indicates that it is exploitable due to the current host
    configuration. This element is returned only if the API request includes the parameter
    arf_config_filter set to 0, 1, 2, 3 or 4."""

    last_processed_datetime: Optional[datetime.datetime] = None
    """The date/time when the detection was last processed."""


@dataclasses.dataclass
class Cloud_Tag:
    """A tag associated with an asset related to the asset's cloud provider."""

    name: str
    """The name of the cloud tag."""

    value: str
    """The value of the cloud tag."""

    last_success_date: datetime.datetime
    """Tag last success date/time, fetched from instance."""


@dataclasses.dataclass
class Attribute:
    """A metadata attribute for a cloud provider."""

    name: str
    """Attribute name, fetched from instance metadata."""

    last_status: str
    """Attribute last status, fetched from instance metadata."""

    value: str
    """Attribute value fetched, from instance metadata."""

    last_success_date: Optional[datetime.datetime] = None
    """Attribute value fetched, from instance metadata."""

    last_error_date: Optional[datetime.datetime] = None
    """Attribute last error date/time, fetched from instance metadata."""

    last_error: Optional[str] = None
    """Attribute last error, fetched from instance metadata."""


@dataclasses.dataclass
class Metadata:
    """Instance metadata of the asset's cloud provider."""

    ec2: Optional[MutableSequence[Attribute]] = None
    """Amazon EC2 metadata."""

    google: Optional[MutableSequence[Attribute]] = None
    """Google Cloud metadata."""

    azure: Optional[MutableSequence[Attribute]] = None
    """Microsoft Azure metadata."""


@dataclasses.dataclass
class Tag:
    """A tag associated with an asset."""

    name: str
    """The ID of a tag associated with the asset when show_tags=1 is specified."""

    tag_id: Optional[str] = None
    """The name of a tag associated with the asset when show_tags=1 is specified."""

    color: Optional[str] = None
    """The color of a tag associated with the asset when show_tags=1 is specified."""

    background_color: Optional[str] = None
    """The background color of a tag associated with the asset when show_tags=1 is specified."""


@dataclasses.dataclass
class Dns_Data:
    """DNS information of the asset."""

    hostname: Optional[str] = None
    """The DNS hostname for the asset."""

    domain: Optional[str] = None
    """The domain name for the asset."""

    fqdn: Optional[str] = None
    """The Fully Qualified Domain Name (FQDN) for the asset."""


@dataclasses.dataclass
class Host:
    """A host object in Qualys, complete with vulnerability detections."""

    id: int
    """Host ID for the asset."""

    detection_list: MutableSequence[Detection]
    """A list of vulnerabilities detected on the host."""

    asset_id: Optional[int] = None
    """Asset ID of the host."""

    ip: Optional[ipaddress.IPv4Address] = None
    """IPv4 address for the asset."""

    ipv6: Optional[ipaddress.IPv6Address] = None
    """IPv6 address for the asset."""

    tracking_method: Optional[str] = None
    """The tracking method assigned to the asset: IP, DNS, NETBIOS, EC2."""

    os: Optional[str] = None
    """The operating system detected on the asset."""

    os_cpe: Optional[str] = None
    """The OS CPE name assigned to the operating system detected on the asset."""

    dns: Optional[str] = None
    """DNS name for the asset. For an EC2 asset this is the private DNS name."""

    dns_data: Optional[Dns_Data] = None
    """DNS information of the asset."""

    cloud_provider: Optional[str] = None
    """Cloud provider of the asset. These will be populated for all cloud assets (Azure, EC2,
    Google).
    """

    cloud_service: Optional[str] = None
    """Cloud service of the asset. For example: (VM for Azure, EC2 for AWS)."""

    cloud_resource_id: Optional[str] = None
    """Cloud resource ID of the asset."""

    ec2_instance_id: Optional[str] = None
    """EC2 instance ID for the asset."""

    netbios: Optional[str] = None
    """NetBIOS name for the asset."""

    qg_hostid: Optional[str] = None
    """The Qualys host ID assigned to the asset when Agentless Tracking is used or when a cloud
    agent is installed.
    """

    last_scan_datetime: Optional[datetime.datetime] = None
    """The date and time of the most recent vulnerability scan of the asset."""

    last_vm_scanned_date: Optional[datetime.datetime] = None
    """The scan end date/time for the most recent unauthenticated vulnerability scan of the
    asset.
    """

    last_vm_scanned_duration: Optional[datetime.timedelta] = None
    """The scan duration for the most recent unauthenticated vulnerability scan of the asset."""

    last_vm_auth_scanned_date: Optional[datetime.datetime] = None
    """The scan end date/time for the last successful authenticated vulnerability scan of the
    asset.
    """

    last_vm_auth_scanned_duration: Optional[datetime.timedelta] = None
    """The scan duration for the last successful authenticated vulnerability scan of the asset."""

    last_pc_scanned_date: Optional[datetime.datetime] = None
    """The scan end date/time for the most recent compliance scan on the asset."""

    tags: Optional[MutableSequence[Tag]] = None
    """Tags associated with the asset."""

    metadata: Optional[Metadata] = None
    """Instance metadata of the asset's cloud provider."""

    cloud_provider_tags: Optional[MutableSequence[Cloud_Tag]] = None
    """Tags associated with an asset related to the asset's cloud provider."""


def _calc_arf_filter(running: Optional[bool], only: Optional[bool]) -> str:
    if running is None and not only:
        arf_filter = "0"
    elif running and not only:
        arf_filter = "1"
    elif not running and only:
        arf_filter = "2"
    elif running and only:
        arf_filter = "3"
    elif running is None and only:
        arf_filter = "4"

    return arf_filter


def _separate_ips(
    ips: Optional[
        Union[
            ipaddress.IPv4Address,
            ipaddress.IPv4Network,
            ipaddress.IPv6Address,
            ipaddress.IPv6Network,
            MutableSequence[
                Union[
                    ipaddress.IPv4Address,
                    ipaddress.IPv4Network,
                    ipaddress.IPv6Address,
                    ipaddress.IPv6Network,
                ]
            ],
        ]
    ] = None
) -> tuple[
    Optional[MutableSequence[Union[ipaddress.IPv4Address, ipaddress.IPv4Network]]],
    Optional[MutableSequence[Union[ipaddress.IPv6Address, ipaddress.IPv6Network]]],
]:
    """Separate a list of IP addresses and networks into a tuple of IPv4 address/networks and
    IPv6 addresses and networks.
    """

    if ips:
        if not isinstance(ips, MutableSequence):
            ips = [ips]
        ip4 = [
            ip
            for ip in ips
            if (
                isinstance(ip, ipaddress.IPv4Address)
                or isinstance(ip, ipaddress.IPv4Network)
            )
        ]
        ip6 = [
            ip
            for ip in ips
            if (
                isinstance(ip, ipaddress.IPv6Address)
                or isinstance(ip, ipaddress.IPv6Network)
            )
        ]

    if len(ip4) == 0 and len(ip6) == 0:
        return (None, None)
    elif len(ip6) == 0:
        return (ip4, None)
    elif len(ip4) == 0:
        return (None, ip6)
    else:
        return (ip4, ip6)


def host_list_detection(
    conn: qualysapi.Connection,
    show_asset_id: Optional[bool] = False,
    show_results: Optional[bool] = True,
    show_reopened_info: Optional[bool] = False,
    kernel_running: Optional[bool] = None,
    only_kernal_vulns: Optional[bool] = False,
    service_running: Optional[bool] = None,
    only_service_vulns: Optional[bool] = False,
    config_vulnerable: Optional[bool] = None,
    only_config_vulns: Optional[bool] = None,
    output_format: Optional[str] = None,
    suppress_duplicated_data_from_csv: Optional[bool] = None,
    truncation_limit: Optional[int] = None,
    detection_updated_since: Optional[datetime.datetime] = None,
    detection_updated_before: Optional[datetime.datetime] = None,
    detection_processed_before: Optional[datetime.datetime] = None,
    detection_processed_after: Optional[datetime.datetime] = None,
    detection_last_tested_since: Optional[datetime.datetime] = None,
    detection_last_tested_before: Optional[datetime.datetime] = None,
    include_ignored: Optional[bool] = None,
    include_disabled: Optional[bool] = None,
    ids: Optional[Union[int, range, MutableSequence[Union[int, range]]]] = None,
    id_min: Optional[int] = None,
    id_max: Optional[int] = None,
    ips: Optional[
        Union[
            ipaddress.IPv4Address,
            ipaddress.IPv4Network,
            ipaddress.IPv6Address,
            ipaddress.IPv6Network,
            MutableSequence[
                Union[
                    ipaddress.IPv4Address,
                    ipaddress.IPv4Network,
                    ipaddress.IPv6Address,
                    ipaddress.IPv6Network,
                ]
            ],
        ]
    ] = None,
    ag_ids: Optional[Union[int, range, MutableSequence[Union[int, range]]]] = None,
    ag_titles: Optional[Union[str, MutableSequence[str]]] = None,
    network_ids: Optional[Union[str, MutableSequence[str]]] = None,
    vm_scan_since: Optional[datetime.datetime] = None,
    no_vm_scan_since: Optional[datetime.datetime] = None,
    vm_processed_before: Optional[datetime.datetime] = None,
    vm_processed_after: Optional[datetime.datetime] = None,
    vm_scan_date_before: Optional[datetime.datetime] = None,
    vm_scan_date_after: Optional[datetime.datetime] = None,
    vm_auth_scan_date_before: Optional[datetime.datetime] = None,
    vm_auth_scan_date_after: Optional[datetime.datetime] = None,
    status: Optional[MutableSequence[str]] = None,
    compliance_enabled: Optional[bool] = None,
    os_pattern: Optional[str] = None,
    qids: Optional[Union[int, range, MutableSequence[Union[int, range]]]] = None,
    severities: Optional[Union[int, range, MutableSequence[Union[int, range]]]] = None,
    filter_superseded_qids: Optional[bool] = None,
    show_igs: Optional[bool] = None,
    include_search_list_titles: Optional[Union[str, MutableSequence[str]]] = None,
    exclude_search_list_titles: Optional[Union[str, MutableSequence[str]]] = None,
    include_search_list_ids: Optional[Union[int, MutableSequence[int]]] = None,
    exclude_search_list_ids: Optional[Union[int, MutableSequence[int]]] = None,
    use_tags: Optional[bool] = False,
    tag_set_by_name: Optional[bool] = None,
    tag_include_all: Optional[bool] = None,
    tag_exclude_all: Optional[bool] = None,
    tag_set_include: Optional[Union[str, MutableSequence[str]]] = None,
    tag_set_exclude: Optional[Union[str, MutableSequence[str]]] = None,
    show_tags: Optional[bool] = False,
    show_qds: Optional[bool] = None,
    qds_min: Optional[int] = None,
    qds_max: Optional[int] = None,
    show_qds_factors: Optional[bool] = None,
    host_metadata: Optional[str] = None,
    host_metadata_fields: Optional[Union[str, MutableSequence[str]]] = None,
    show_cloud_tags: Optional[bool] = False,
    cloud_tag_fields: Optional[Union[str, MutableSequence[str]]] = None,
    post: bool = False,
) -> tuple[MutableSequence[Host], Optional[Warning]]:

    ip4, ip6 = _separate_ips(ips)

    params: dict[str, Optional[str]] = {
        "show_asset_id": qutils.parse_optional_bool(show_asset_id),
        "show_results": qutils.parse_optional_bool(show_results),
        "show_reopened_info": qutils.parse_optional_bool(show_reopened_info),
        "arf_kernel_filter": _calc_arf_filter(kernel_running, only_kernal_vulns),
        "arf_service_filter": _calc_arf_filter(service_running, only_service_vulns),
        "arf_config_filter": _calc_arf_filter(config_vulnerable, only_config_vulns),
        "output_format": output_format if output_format else None,
        "suppress_duplicated_data_from_csv": qutils.parse_optional_bool(
            suppress_duplicated_data_from_csv
        ),
        "truncation_limit": str(truncation_limit) if truncation_limit else None,
        "detection_updated_since": qutils.datetime_to_qualys_format(
            detection_updated_since
        ),
        "detection_updated_before": qutils.datetime_to_qualys_format(
            detection_updated_before
        ),
        "detection_processed_before": qutils.datetime_to_qualys_format(
            detection_processed_before
        ),
        "detection_processed_after": qutils.datetime_to_qualys_format(
            detection_processed_after
        ),
        "detection_last_tested_since": qutils.datetime_to_qualys_format(
            detection_last_tested_since
        ),
        "detection_last_tested_before": qutils.datetime_to_qualys_format(
            detection_last_tested_before
        ),
        "include_ignored": qutils.parse_optional_bool(include_ignored),
        "include_disabled": qutils.parse_optional_bool(include_disabled),
        "ids": qutils.to_comma_separated(ids),
        "id_min": str(id_min) if id_min else None,
        "id_max": str(id_max) if id_max else None,
        "ips": qutils.ips_to_qualys_format(ip4) if ip4 else None,
        "ipv6": qutils.ips_to_qualys_format(ip6) if ip6 else None,
        "ag_ids": qutils.to_comma_separated(ag_ids),
        "ag_titles": qutils.to_comma_separated(ag_titles),
        "network_ids": qutils.to_comma_separated(network_ids),
        "vm_scan_since": qutils.datetime_to_qualys_format(vm_scan_since),
        "no_vm_scan_since": qutils.datetime_to_qualys_format(no_vm_scan_since),
        "vm_processed_before": qutils.datetime_to_qualys_format(vm_processed_before),
        "vm_processed_after": qutils.datetime_to_qualys_format(vm_processed_after),
        "vm_scan_date_before": qutils.datetime_to_qualys_format(vm_scan_date_before),
        "vm_scan_date_after": qutils.datetime_to_qualys_format(vm_scan_date_after),
        "vm_auth_scan_date_before": qutils.datetime_to_qualys_format(
            vm_auth_scan_date_before
        ),
        "vm_auth_scan_date_after": qutils.datetime_to_qualys_format(
            vm_auth_scan_date_after
        ),
        "status": qutils.to_comma_separated(status),
        "compliance_enabled": qutils.parse_optional_bool(compliance_enabled),
        "os_pattern": os_pattern,
        "qids": qutils.to_comma_separated(qids),
        "severities": qutils.to_comma_separated(severities),
        "filter_superseded_qids": qutils.parse_optional_bool(filter_superseded_qids),
        "show_igs": qutils.parse_optional_bool(show_igs),
        "include_search_list_titles": qutils.to_comma_separated(
            include_search_list_titles
        ),
        "exclude_search_list_titles": qutils.to_comma_separated(
            exclude_search_list_titles
        ),
        "include_search_list_ids": qutils.to_comma_separated(include_search_list_ids),
        "exclude_search_list_ids": qutils.to_comma_separated(exclude_search_list_ids),
        "use_tags": qutils.parse_optional_bool(use_tags),
        "tag_set_by": qutils.parse_optional_bool(tag_set_by_name, ("name", "id")),
        "tag_include_selector": qutils.parse_optional_bool(
            tag_include_all, ("all", "any")
        ),
        "tag_exclude_selector": qutils.parse_optional_bool(
            tag_exclude_all, ("all", "any")
        ),
        "tag_set_include": qutils.to_comma_separated(tag_set_include),
        "tag_set_exclude": qutils.to_comma_separated(tag_set_exclude),
        "show_tags": qutils.parse_optional_bool(show_tags),
        "show_qds": qutils.parse_optional_bool(show_qds),
        "qds_min": str(qds_min) if qds_min else None,
        "qds_max": str(qds_max) if qds_max else None,
        "show_qds_factors": qutils.parse_optional_bool(show_qds_factors),
        "host_metadata": host_metadata,
        "host_metadata_fields": qutils.to_comma_separated(host_metadata_fields),
        "show_cloud_tags": qutils.parse_optional_bool(show_cloud_tags),
        "cloud_tag_fields": qutils.to_comma_separated(cloud_tag_fields),
    }

    params_filtered = qutils.remove_nones_from_dict(params)

    if post:
        raw = conn.post(qutils.URLS["Host List Detection"], params=params_filtered)
    else:
        raw = conn.get(qutils.URLS["Host List Detection"], params=params_filtered)
    if raw.tag == "SIMPLE_RETURN":
        raise qualysapi.Qualys_API_Error(
            f"Error {str(raw.RESPONSE.CODE)}: {str(raw.RESPONSE.TEXT)}"
        )

    host_list: list[Host] = []
    for host in raw.RESPONSE.HOST_LIST.HOST:
        h = qutils.elements_to_class(
            host,
            Host,
            classmap={
                "dns_data": Dns_Data,
                "tag": Tag,
                "metadata": Metadata,
                "attribute": Attribute,
                "cloud_tag": Cloud_Tag,
                "detection": Detection,
            },
            listmap={
                "detection_list": "detection",
                "tags": "tag",
                "cloud_provider_tags": "cloud_tag",
                "ec2": "attribute",
                "google": "attribute",
                "azure": "attribute",
            },
            funcmap={
                "id": int,
                "asset_id": int,
                "ip": ipaddress.ip_address,
                "ipv6": ipaddress.ip_address,
                "last_scan_datetime": qutils.datetime_from_qualys_format,
                "last_vm_scanned_date": qutils.datetime_from_qualys_format,
                "last_vm_scanned_duration": qutils.timedelta_from_qualys_format,
                "last_vm_auth_scanned_date": qutils.datetime_from_qualys_format,
                "last_vm_auth_scanned_duration": qutils.timedelta_from_qualys_format,
                "last_pc_scanned_date": qutils.datetime_from_qualys_format,
                "last_success_date": qutils.datetime_from_qualys_format,
                "last_error_date": qutils.datetime_from_qualys_format,
                "qid": int,
                "severity": int,
                "port": int,
                "ssl": qutils.bool_from_qualys_format,
                "first_found_datetime": qutils.datetime_from_qualys_format,
                "last_found_datetime": qutils.datetime_from_qualys_format,
                "qds": int,
                "times_found": int,
                "times found": int,
                "last_test_datetime": qutils.datetime_from_qualys_format,
                "last_update_datetime": qutils.datetime_from_qualys_format,
                "last_fixed_datetime": qutils.datetime_from_qualys_format,
                "first_reopened_date": qutils.datetime_from_qualys_format,
                "last_reopened_date": qutils.datetime_from_qualys_format,
                "times_reopened": int,
                "is_ignored": qutils.bool_from_qualys_format,
                "is_disabled": qutils.bool_from_qualys_format,
                "affect_running_kernel": qutils.bool_from_qualys_format,
                "affect_running_service": qutils.bool_from_qualys_format,
                "affect_exploitable_config": qutils.bool_from_qualys_format,
                "last_processed_datetime": qutils.datetime_from_qualys_format,
            },
        )
        host_list.append(h)

    warning = None
    if raw.RESPONSE.find("WARNING") is not None:
        warning = qutils.elements_to_class(raw.RESPONSE.WARNING, Warning)

    return (host_list, warning)
