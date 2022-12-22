"""Python wrapper for the host_list Qualys API."""

import dataclasses
import datetime
import ipaddress
from collections.abc import MutableMapping, MutableSequence
from typing import Optional, Union
import urllib.parse

import qualyspy.qualysapi as qualysapi
import qualyspy.qutils as qutils


@dataclasses.dataclass
class Asset_Group:
    """An asset group which a host in the host list output belongs to."""

    id: int
    """An asset group ID."""

    title: str
    """An asset group title."""


@dataclasses.dataclass
class User:
    """A user who is an asset owner for a host in the host list output."""

    user_login: str
    """A user login ID."""

    first_name: str
    """A user's first name."""

    last_name: str
    """A user's last name."""


@dataclasses.dataclass
class Glossary:
    """A glossary of definitions associated with a host list output."""

    label_1: Optional[str] = None
    """Host attribute label number 1, as defined for the subscription.When the default label is used
    this element is: <LABEL_1>Location. The labels may be customized within Qualys.
    """

    label_2: Optional[str] = None
    """Host attribute label number 2, as defined for the subscription.When the default label is used
    this element is: <LABEL_2>Function. The labels may be customized within Qualys.
    """

    label_3: Optional[str] = None
    """Host attribute label number 3, as defined for the subscription.When the default label is used
    this element is: <LABEL_3>Asset Tag. The labels may be customized within Qualys.
    """

    user_list: Optional[MutableSequence[User]] = None
    """A list of users who are asset owners for the hosts in the host list output."""

    asset_group_list: Optional[MutableSequence[Asset_Group]] = None
    """A list of asset groups which hosts in the host list output belong to."""


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

    tag_id: Optional[str] = None
    """A tag ID associated with the asset when show_tags=1 is specified."""

    name: Optional[str] = None
    """A tag name associated with the asset when show_tags=1 is specified."""


@dataclasses.dataclass
class Dns_Data:
    """DNS information of an asset."""

    hostname: Optional[str] = None
    """The DNS hostname for the asset."""

    domain: Optional[str] = None
    """The domain name for the asset."""

    fqdn: Optional[str] = None
    """"The Fully Qualified Domain Name (FQDN) for the asset."""


@dataclasses.dataclass
class Ars_Factors:
    """Factors used to calculate the ARS of a host."""

    ars_formula: str
    """The formula used to calculate the ARS."""

    vuln_count: Optional[MutableSequence[str]] = None
    """The vulnerability count at each QDS (Qualys Detection Score) severity level."""


@dataclasses.dataclass
class Host:
    """A host object in Qualys.

    The HOST element is returned when the “details” input parameter is set to “basic” or “all” or if
    the parameter is unspecified.
    """

    id: str
    """The host ID."""

    asset_id: Optional[int] = None
    """The asset ID of the host."""

    ip: Optional[ipaddress.IPv4Address] = None
    """The asset's IP address."""

    ipv6: Optional[ipaddress.IPv6Address] = None
    """The asset's IPv6 address."""

    asset_risk_score: Optional[int] = None
    """The asset risk score (ARS). This is the overall risk score assigned to the asset based on
    multiple contributing factors. ARS has a range from 0 to 1000:
    - Severe (850-1000)
    - High (700-849)
    - Medium (500-699)
    - Low (0-499)
    """

    asset_criticality_score: Optional[int] = None
    """The asset criticality score (ACS)."""

    ars_factors: Optional[Ars_Factors] = None
    """Factors used to calculate the ARS."""

    tracking_method: Optional[str] = None
    """The tracking method assigned to the asset: IP, DNS, NETBIOS, EC2."""

    network_id: Optional[str] = None
    """The network ID of the asset, if the Networks feature is enabled."""

    dns: Optional[str] = None
    """DNS name for the asset. For an EC2 asset this is the private DNS name."""

    dns_data: Optional[Dns_Data] = None
    """DNS information of the asset."""

    cloud_service: Optional[str] = None
    """Cloud service of the asset. For example: (VM for Azure, EC2 for AWS)."""

    cloud_resource_id: Optional[str] = None
    """Cloud resource ID of the asset."""

    ec2_instance_id: Optional[str] = None
    """EC2 instance ID for the asset."""

    netbios: Optional[str] = None
    """NetBIOS host name for the asset."""

    os: Optional[str] = None
    """Operating system detected on the asset."""

    qg_hostid: Optional[str] = None
    """The Qualys host ID assigned to the asset when Agentless Tracking is used or when a cloud
    agent is installed.
    """

    tags: Optional[MutableSequence[Tag]] = None
    """Tags associated with the asset."""

    metadata: Optional[Metadata] = None
    """Instance metadata of the asset's cloud provider."""

    cloud_provider_tags: Optional[MutableSequence[Cloud_Tag]] = None
    """Tags associated with an asset related to the asset's cloud provider."""

    last_vuln_scan_datetime: Optional[datetime.datetime] = None
    """The date and time of the most recent vulnerability scan."""

    last_vm_scanned_date: Optional[datetime.datetime] = None
    """The scan end date/time for the most recent unauthenticated vulnerability scan on the
    asset.
    """

    last_vm_scanned_duration: Optional[datetime.timedelta] = None
    """The scan duration for the most recent unauthenticated vulnerability scan on the asset."""

    last_vm_auth_scanned_date: Optional[datetime.datetime] = None
    """The scan end date/time for the last successful authenticated vulnerability scan on the
    asset.
    """

    last_vm_auth_scanned_duration: Optional[datetime.timedelta] = None
    """The scan duration for the last successful authenticated vulnerability scan on the asset."""

    last_compliance_scan_datetime: Optional[datetime.datetime] = None
    """The date and time of the most recent compliance scan."""

    last_scap_scan_datetime: Optional[datetime.datetime] = None
    """The date and time of the most recent SCAP scan."""

    owner: Optional[str] = None
    """The asset owner."""

    comments: Optional[str] = None
    """The comments defined for the asset."""

    value_1: Optional[str] = None
    """Host attribute value number 1.  The associated label is returned in the glossary."""

    value_2: Optional[str] = None
    """Host attribute value number 2.  The associated label is returned in the glossary."""

    value_3: Optional[str] = None
    """Host attribute value number 3.  The associated label is returned in the glossary."""

    asset_group_ids: Optional[str] = None
    """The asset group IDs for the asset groups which the host belongs to."""


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


def _parse_details(all_details: Optional[bool], show_ag_info: Optional[bool]) -> str:
    """Create the correct details string to be ingested in the Qualys API based on input to the
    host_list function.
    """

    if all_details is None:
        details = "None"
    elif not all_details:
        details = "Basic"
    else:
        details = "All"
    if show_ag_info and all_details is not None:
        details += "/AGs"

    return details


def host_list(
    conn: qualysapi.Connection,
    /,
    show_asset_ids: Optional[bool] = False,
    all_details: Optional[bool] = False,
    show_ag_info: Optional[bool] = False,
    os_pattern: Optional[str] = None,
    truncation_limit: Optional[int] = None,
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
    ids: Optional[Union[int, range, MutableSequence[Union[int, range]]]] = None,
    id_min: Optional[int] = None,
    id_max: Optional[int] = None,
    network_ids: Optional[Union[str, MutableSequence[str]]] = None,
    compliance_enabled: Optional[bool] = None,
    no_vm_scan_since: Optional[datetime.datetime] = None,
    no_compliance_scan_since: Optional[datetime.datetime] = None,
    vm_scan_since: Optional[datetime.datetime] = None,
    compliance_scan_since: Optional[datetime.datetime] = None,
    vm_processed_before: Optional[datetime.datetime] = None,
    vm_processed_after: Optional[datetime.datetime] = None,
    vm_scan_date_before: Optional[datetime.datetime] = None,
    vm_scan_date_after: Optional[datetime.datetime] = None,
    vm_auth_scan_date_before: Optional[datetime.datetime] = None,
    vm_auth_scan_date_after: Optional[datetime.datetime] = None,
    scap_scan_since: Optional[datetime.datetime] = None,
    no_scap_scan_since: Optional[datetime.datetime] = None,
    use_tags: Optional[bool] = False,
    tag_set_by_name: Optional[bool] = None,
    tag_include_all: Optional[bool] = None,
    tag_exclude_all: Optional[bool] = None,
    tag_set_include: Optional[Union[str, MutableSequence[str]]] = None,
    tag_set_exclude: Optional[Union[str, MutableSequence[str]]] = None,
    show_tags: Optional[bool] = False,
    show_ars: Optional[bool] = None,
    ars_min: Optional[int] = None,
    ars_max: Optional[int] = None,
    show_ars_factors: Optional[bool] = None,
    host_metadata: Optional[str] = None,
    host_metadata_fields: Optional[MutableSequence[str]] = None,
    show_cloud_tags: Optional[bool] = False,
    cloud_tag_fields: Optional[
        MutableSequence[Union[str, MutableMapping[str, str]]]
    ] = None,
    post: bool = False,
) -> tuple[
    Optional[Union[MutableSequence[Host], MutableSequence[str]]],
    Optional[Warning],
    Optional[Glossary],
]:
    """Download a list of scanned hosts in the user's account. By default, all scanned hosts in the
    user account are included and basic information about each host is provided. Hosts in the XML
    output are sorted by host ID in ascending order.

    The output of the Host List API is paginated. By default, a maximum of 1,000 host records are
    returned per request. You can customize the page size (i.e. the number of host records) by using
    the parameter “truncation_limit=10000” for instance. In this case the results will be return
    with pages of 10,000 host records.  If the truncation limit is reached, the returned Warning
    object will include a URL to call to retrieve the next page.

    The Host List API also shows the Asset Risk Score (ARS) for each asset record in the API output
    and allows users to filter the output based on the ARS.

    The Asset Risk Score (ARS) is the overall risk score assigned to the asset based on multiple
    contributing factors, including Asset Criticality Score (ACS), Risk (QID) scores for each
    severity level, and an auto assigned weightin factor (w) for each criticality level of QIDs.

    ARS has a range from 0 to 1000:
    - Severe (850-1000)
    - High (700-849)
    - Medium (500-699)
    - Low (0-499)

    Args:
        conn:
            A connection to the Qualys API.
        show_asset_ids:
            When specified, we show the asset ID of the scanned hosts in the output. The default
            value of this parameter is set to False. When set to False, Qualys does not show the
            asset id information for the scanned hosts.
        all_details:
            By default, only basic host information will be shown. Basic host information includes
            the host ID, IP address, tracking method, DNS and NetBIOS hostnames, and operating
            system. Setting this parameter to true will show all host information. All host
            information includes the basic host information plus the last vulnerability and
            compliance scan dates.  If this value is set to None, only the host IDs will be
            returned.
        show_ag_info:
            Show asset group information. Asset group information includes the asset group ID and
            title.
        os_pattern:
            Show only hosts which have an operating system matching a certain regular expression. An
            empty value cannot be specified. "%5E%24" to match empty string. The regular expression
            string you enter must follow the PCRE standard and should not be URL-encoded (the
            function will perform the encoding).
        truncation_limit:
            Specify the maximum number of host records processed per request. When not specified,
            the truncation limit is set to 1000 host records. You may specify a value less than the
            default (1-999) or greater than the default (1001-1000000).

            If the requested list identifies more host records than the truncation limit, then the
            output includes a Warning object with the URL for making another request for the next
            batch of host records.

            You can specify truncation_limit=0 for no truncation limit. This means that the output
            is not paginated and all the records are returned in a single output. WARNING: This can
            generate very large output and processing large XML files can consume a lot of resources
            on the client side. In this case it is recommended to use the pagination logic and
            parallel processing. The previous page can be processed while the next page is
            downloaded.
        ips:
            Show only certain IP addresses/ranges. One or more IPs/ranges may be specified.
        ag_ids:
            Show only hosts belonging to asset groups with certain IDs. One or more asset group IDs
            and/or ranges may be specified.
        ag_titles:
            Show only hosts belonging to asset groups with certain strings in the asset group title.
            One or more asset group titles may be specified.
        ids:
            Show only certain host IDs/ranges. One or more host IDs/ranges may be specified.
        id_min:
            Show only hosts which have a minimum host ID value. A valid host ID is required.
        id_max:
            Show only hosts which have a maximum host ID value. A valid host ID is required.
        network_ids:
            Restrict the request to certain custom network IDs.
        compliance_enabled:
            Use this parameter to filter the scanned hosts list to show either:
            1) a list of scanned compliance hosts, or
            2) a list of scanned vulnerability management hosts.

            Specify True to list scanned compliance hosts in the user's account. These hosts are
            assigned to the policy compliance module.

            Specify False to list scanned hosts which are not assigned to the policy compliance
            module.
        no_vm_scan_since:
            Show hosts not scanned since a certain date and time.
        no_compliance_scan_since:
            Show compliance hosts not scanned since a certain date and time.
        vm_scan_since:
            Show hosts that were last scanned for vulnerabilities since a certain date and time.
        compliance_scan_since:
            Show hosts that were last scanned for compliance since a certain date and time.
        vm_processed_before:
            Show hosts with vulnerability scan results processed before a certain date and time.
        vm_processed_after:
            Show hosts with vulnerability scan results processed after a certain date and time.
        vm_scan_date_before:
            Show hosts with a vulnerability scan end date before a certain date and time.
        vm_scan_date_after:
            Show hosts with a vulnerability scan end date after a certain date and time.
        vm_auth_scan_date_before:
            Show hosts with a successful authenticated vulnerability scan end date before a certain
            date and time.
        vm_auth_scan_date_after:
            Show hosts with a successful authenticated vulnerability scan end date after a certain
            date and time.
        scap_scan_since:
            Show hosts that were last scanned for SCAP since a certain date and time. Hosts that
            were the target of a SCAP scan since the date/time will be shown.
        no_scap_scan_since:
             Show hosts not scanned for SCAP since a certain date and time.
        use_tags:
            Specify False (the default) if you want to select hosts based on IP addresses/ranges
            and/or asset groups. Specify True if you want to select hosts based on asset tags.
        tag_set_by_name:
            Specify False (the default) to select a tag set by providing tag IDs. Specify True to
            select a tag set by providing tag names.
        tag_include_all:
            Specify False (the default) to include hosts that match at least one of the selected
            tags. Specify True to include hosts that match all of the selected tags.
        tag_exclude_all:
            Specify False (the default) to exclude hosts that match at least one of the selected
            tags. Specify True to exclude hosts that match all of the selected tags.
        tag_set_include:
            Specify a tag set to include. Hosts that match these tags will be included. You identify
            the tag set by providing tag name or IDs.
        tag_set_exclude:
            Specify a tag set to exclude. Hosts that match these tags will be excluded. You identify
            the tag set by providing tag name or IDs.
        show_tags:
            Specify True to include asset tags associated with each host in the output.
        show_ars:
            Specify True to show the ARS value in the output. Specify False if you do not want to
            show the ARS value.
        ars_min:
            Show only asset records with an ARS value greater than or equal to the ARS min value
            specified. ars_min can only be specified when show_ars=True. When ars_min and ars_max
            are specified in the same request, the ars_min value must be less than the ars_max
            value.
        ars_max:
            Show only detection records with an ARS value less than or equal to the ARS max value
            specified. ars_max can only be specified when show_ars=True. When ars_min and ars_max
            are specified in the same request, the ars_min value must be less than the ars_max
            value.
        show_ars_factors:
            Specify True to show ARS contributing factors associated with each asset record in the
            output. Specify False if you do not want to show ARS contributing factors.
        host_metadata:
            Specify “all” to list all cloud assets with their metadata or specify the name of the
            cloud provider to show only the assets managed by the cloud provider.
            Valid values: "all", "ec2", "google", "azure"
        host_metadata_fields:
            Specify metadata fields to only return data for certain attributes.
        show_cloud_tags:
            Specify True to display cloud provider tags for each scanned host asset in the output.
            The default value of the parameter is set to False. When set to False, Qualys will not
            show the cloud provider tags for the scanned assets.
        cloud_tag_fields:
            Specify cloud tags or cloud tag and name combinations to only return information for
            specified cloud tags. A cloud tag name and value combination is specified in a mapping.
            For each cloud tag, Qualys shows the cloud tag's name, its value, and last success date
            (the tag last success date/time, fetched from instance).

            If this parameter is not specified and "show_cloud_tags" is set to True, the cloud
            provider tags will be included for the assets.
        post:
            Run as a POST request. There are known limits for the amount of data that can be sent
            using the GET method, so POST should be used in those cases.

        Returns:
            A tuple containing three objects in the following order:
            - Either a list of Host objects containing information on each host, or a list of host
            IDs if all_details=None.
            - If the truncation limit is reached, the second item will be a Warning object which
            includes a URL to the next page of results.  Otherwise, None.
            - A glossary of definitions associated with a hosts in the output.
    """

    details = _parse_details(all_details, show_ag_info)
    ip4, ip6 = _separate_ips(ips)

    params = {
        "show_asset_id": qutils.parse_optional_bool(show_asset_ids),
        "details": details,
        "os_pattern": urllib.parse.quote(os_pattern) if os_pattern else None,
        "truncation_limit": str(truncation_limit) if truncation_limit else None,
        "ips": qutils.ips_to_qualys_format(ip4) if ip4 else None,
        "ipv6": qutils.ips_to_qualys_format(ip6) if ip6 else None,
        "ag_ids": qutils.to_comma_separated(ag_ids) if ag_ids else None,
        "ag_titles": qutils.to_comma_separated(ag_titles),
        "ids": qutils.to_comma_separated(ids) if ids else None,
        "id_min": str(id_min) if id_min else None,
        "id_max": str(id_max) if id_max else None,
        "network_ids": qutils.to_comma_separated(network_ids),
        "compliance_enabled": qutils.parse_optional_bool(compliance_enabled),
        "no_vm_scan_since": qutils.datetime_to_qualys_format(no_vm_scan_since),
        "no_compliance_scan_since": qutils.datetime_to_qualys_format(
            no_compliance_scan_since
        ),
        "vm_scan_since": qutils.datetime_to_qualys_format(vm_scan_since),
        "compliance_scan_since": qutils.datetime_to_qualys_format(
            compliance_scan_since
        ),
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
        "scap_scan_since": qutils.datetime_to_qualys_format(scap_scan_since),
        "no_scap_scan_since": qutils.datetime_to_qualys_format(no_scap_scan_since),
        "use_tags": "1" if use_tags else "0",
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
        "show_ars": qutils.parse_optional_bool(show_ars),
        "ars_min": str(ars_min) if ars_min else None,
        "ars_max": str(ars_max) if ars_max else None,
        "show_ars_factors": qutils.parse_optional_bool(show_ars_factors),
        "host_metadata": host_metadata if host_metadata else None,
        "host_metadata_fields": qutils.to_comma_separated(host_metadata_fields),
        "show_cloud_tags": qutils.parse_optional_bool(show_cloud_tags),
        "cloud_tag_fields": qutils.to_comma_separated(cloud_tag_fields),
    }

    params_filtered = qutils.remove_nones_from_dict(params)

    if post:
        raw = conn.post(qutils.URLS["Host List"], params=params_filtered)
    else:
        raw = conn.get(qutils.URLS["Host List"], params=params_filtered)
    if raw.tag == "SIMPLE_RETURN":
        raise qualysapi.Qualys_API_Error(
            f"Error {str(raw.RESPONSE.CODE)}: {str(raw.RESPONSE.TEXT)}"
        )

    if all_details is None:
        id_set = [str(id) for id in raw.ID_SET]
    else:
        hosts: list[Host] = []
        for host in raw.RESPONSE.HOST_LIST.HOST:
            h = qutils.elements_to_class(
                host,
                Host,
                classmap={
                    "ars_factors": Ars_Factors,
                    "dns_data": Dns_Data,
                    "tag": Tag,
                    "metadata": Metadata,
                    "attribute": Attribute,
                    "cloud_tag": Cloud_Tag,
                },
                listmap={
                    "tags": "tag",
                    "ec2": "attribute",
                    "google": "attribute",
                    "azure": "attribute",
                    "cloud_provider_tags": "cloud_tag",
                },
                funcmap={
                    "asset_id": int,
                    "ip": ipaddress.ip_address,
                    "ipv6": ipaddress.ip_address,
                    "asset_risk_score": int,
                    "asset_criticality_score": int,
                    "last_vuln_scan_datetime": qutils.datetime_from_qualys_format,
                    "last_vm_scanned_date": qutils.datetime_from_qualys_format,
                    "last_vm_scanned_duration": qutils.timedelta_from_qualys_format,
                    "last_vm_auth_scanned_date": qutils.datetime_from_qualys_format,
                    "last_vm_auth_scanned_duration": qutils.timedelta_from_qualys_format,
                    "last_compliance_scan_datetime": qutils.datetime_from_qualys_format,
                    "last_scap_scan_datetime": qutils.datetime_from_qualys_format,
                    "last_success_date": qutils.datetime_from_qualys_format,
                    "last_error_date": qutils.datetime_from_qualys_format,
                }
            )
            hosts.append(h)

    warning = None
    if raw.RESPONSE.find("WARNING") is not None:
        warning = qutils.elements_to_class(raw.RESPONSE.WARNING, Warning)

    glossary = None
    if raw.RESPONSE.find("GLOSSARY") is not None:
        glossary = qutils.elements_to_class(
            raw.RESPONSE.GLOSSARY,
            Glossary,
            classmap={"user": User, "asset_group": Asset_Group},
            listmap={"user_list": "user", "asset_group_list": "asset_group"},
            funcmap={"id": int}
        )

    if all_details is None:
        return (id_set, warning, glossary)
    else:
        return (hosts, warning, glossary)
