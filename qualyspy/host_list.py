import dataclasses
import datetime
import ipaddress
import re
from collections.abc import MutableMapping, MutableSequence
from typing import Optional, Tuple, Union

import qualysapi


@dataclasses.dataclass
class Asset_Group:
    """An asset group which a host in the host list output belongs to."""

    id: str
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

    asset_id: Optional[str] = None
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


def host_list(
    conn: qualysapi.Connection,
    show_asset_id: Optional[bool] = False,
    all_details: Optional[bool] = False,
    show_ag_info: Optional[bool] = False,
    os_pattern: Optional[re.Pattern] = None,
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
    ag_ids: Optional[Union[str, MutableSequence[str]]] = None,
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
    tag_set_by_name: Optional[bool] = False,
    tag_include_all: Optional[bool] = False,
    tag_exclude_all: Optional[bool] = False,
    tag_set_include: Optional[Union[str, MutableSequence[str]]] = None,
    tag_set_exlude: Optional[Union[str, MutableSequence[str]]] = None,
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
) -> Tuple[Union[MutableSequence[Host], MutableSequence[str]], Warning, Glossary]:
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
            compliance scan dates.
        show_ag_info:
            Show asset group information. Asset group information includes the asset group ID and
            title.
        os_pattern:
            Show only hosts which have an operating system matching a certain regular expression. An
            empty value cannot be specified. Use re.compile("%5E%24") to match empty string.
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
            
    """
