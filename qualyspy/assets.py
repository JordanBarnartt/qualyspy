"""Python wrapper to work with the Qualys Assets API.

Manage the host assets you want to scan (internal and external facing) for vulnerabilities and
compliance.
"""

import dataclasses
import importlib.resources
import ipaddress
import json
from collections.abc import MutableSequence
from typing import Optional, Union

import lxml.objectify

import qualyspy.qualysapi as qualysapi
import qualyspy.utils as qutils

URLS = json.load(importlib.resources.files("qualyspy").joinpath("urls.json").open())


@dataclasses.dataclass
class Ip_Set:
    """A list of IP addresses in a user account.  The contains special method will search the ips
    instance variable.

    Example:
        ip_set_example = list_ips(conn)
        ipaddress.ip_address('192.168.0.1') in ip_set_example
    """

    ips_qualys_format: MutableSequence[lxml.objectify.ObjectifiedElement]
    """IP addresses and ranges in the set in Qualys format (i.e. a range is specified with a hypen,
    for examples, 10.10.10.44-10.10.10.90
    """

    def __post_init__(self) -> None:
        self.ips = qutils.ips_from_qualys_format(self.ips_qualys_format)
        """IP addresses and ranges in the set formatted as Python objects."""

    def __contains__(
        self, item: Union[ipaddress.IPv4Address, ipaddress.IPv6Address]
    ) -> bool:
        return item in self.ips


def list_ips(
    conn: qualysapi.Connection,
    ips: Optional[
        MutableSequence[
            Union[
                ipaddress.IPv4Address,
                ipaddress.IPv6Address,
                ipaddress.IPv4Network,
                ipaddress.IPv6Network,
            ]
        ]
    ] = None,
    network_id: Optional[str] = None,
    tracking_method: Optional[str] = None,
    compliance_enabled: Optional[bool] = None,
    certview_enabled: Optional[bool] = None,
    post: bool = False,
) -> Ip_Set:
    """List IP addresses in the user account. By default, all hosts in the user account are
    included. Optional input parameters support filtering the list by IP addresses and host
    tracking method.

    Args:
        conn:
            A connection to the Qualys API.
        ips:
            Show only certain IP addresses/ranges. One or more IPs/ranges may be specified.
        network_id:
            A non-Manager user can use this parameter to restrict the request to IP addresses in a
            certain custom network ID. For a Manager user, the output will be the same regardless of
            the network_id specified in the request because all IPs are part of all networks
            automatically and Managers have access to all IPs in all networks.
        tracking_method:
            Show only IP addresses/ranges which have a certain tracking method. Valid values: "IP",
            "DNS", "NETBIOS".
        compliance_enabled:
            Specify True to list IP addresses in the user's account assigned to the Policy
            Compliance module. Specify False to list IPs which are not assigned to the Policy
            Compliance module.
        certview_enabled:
            Set to True to list IP addresses in the user's account assigned to the Certificate View
            module. Specify False to list IPs that are not assigned to the Certificate View module.
        post:
            Run as a POST request. There are known limits for the amount of data that can be sent
            using the GET method, so POST should be used in those cases.

    Returns:
        An Ip_Set object containing the list of IP addresses in the account.
    """

    if compliance_enabled is not None:
        if compliance_enabled:
            compliance_enabled_str = "1"
        else:
            compliance_enabled_str = "0"
    if certview_enabled is not None:
        if certview_enabled:
            certview_enabled_str = "1"
        else:
            certview_enabled_str = "0"

    params = {
        "ips": qutils.ips_to_qualys_format(ips) if ips else None,
        "network_id": network_id,
        "tracking_method": tracking_method,
        "compliance_enabled": compliance_enabled_str
        if compliance_enabled is not None
        else None,
        "certview_enalbed": certview_enabled_str
        if compliance_enabled is not None
        else None,
    }

    params_parsed = qutils.remove_nones_from_dict(params)

    if post:
        response = conn.post(URLS["IP List"], params=params_parsed)
    else:
        response = conn.get(URLS["IP List"], params=params_parsed)

    ip_list = []
    for ip in response.RESPONSE.IP_SET.IP:
        ip_list.append(ip)
    for ip_range in response.RESPONSE.IP_SET.IP_RANGE:
        ip_list.append(ip_range)

    return Ip_Set(ip_list)


def add_ips(
    conn: qualysapi.Connection,
    ips: MutableSequence[
        Union[
            ipaddress.IPv4Address,
            ipaddress.IPv6Address,
            ipaddress.IPv4Network,
            ipaddress.IPv6Network,
        ]
    ],
    tracking_method: str = "IP",
    enable_vm: bool = False,
    enable_pc: bool = False,
    owner: Optional[str] = None,
    ud1: Optional[str] = None,
    ud2: Optional[str] = None,
    ud3: Optional[str] = None,
    comment: Optional[str] = None,
    ag_title: Optional[str] = None,
    enable_certview: Optional[bool] = None,
) -> dict[str, str]:
    """Add IP addresses to the user's subscription. Once added they are available for scanning and
    reporting.

    Args:
        ips:
            The hosts you want to add to the subscription.
        tracking_method:
            The tracking method is set to "IP" for IP address by default. To use another tracking
            method specify "DNS" or "NETBIOS".
        enable_vm:
            Enable the hosts for the VM app. At least one of enable_vm and enable_pc must be True.
        enable_pc:
            Enable the hosts for the PC app. At least one of enable_vm and enable_pc must be True.
        owner:
            The owner of the host asset(s). The owner must be a Manager or a Unit Manager. A valid
            Unit Manager must have the “Add assets” permission and sufficient remaining IPs (maximum
            number of IPs that can be added to the Unit Manager's business unit).
        ud1:
            Values for user-defined field 1. You can specify a maximum of 128 characters
            (ascii) for the field value.
        ud2:
            Values for user-defined field 2. You can specify a maximum of 128 characters
            (ascii) for the field value.
        ud3:
            Values for user-defined field 3. You can specify a maximum of 128 characters
            (ascii) for the field value.
        comment:
            User-defined comments.
        ag_title:
            Required if the request is being made by a Unit Manager; otherwise invalid. The title
            of an asset group in the Unit Manager's business unit that the host(s) will be added to.
        enable_certview:
            Set to True to add IPs to your CertView license. By default IPs are not added to your
            CertView license.

    Returns:
        A dictionary containing information on the status of the operation.
    """

    params = {
        "ips": qutils.ips_to_qualys_format(ips),
        "tracking_method": tracking_method,
        "enable_vm": "1" if enable_vm else "0",
        "enable_pc": "1" if enable_pc else "0",
        "owner": owner,
        "ud1": ud1,
        "ud2": ud2,
        "ud3": ud3,
        "comment": comment,
        "ag_title": ag_title,
        "enable_certview": "1" if enable_certview else None,
    }

    response = conn.post(URLS["Add IPs"], params=qutils.remove_nones_from_dict(params))

    return qutils.parse_simple_return(response)


class Duplicate_Hosts_Error(Exception):
    """An exception returned in update_ips when there are two or more asset records returned
    for a supplied IP address.
    """

    pass


def update_ips(
    conn: qualysapi.Connection,
    ips: Union[
        ipaddress.IPv4Address,
        ipaddress.IPv6Address,
        ipaddress.IPv4Network,
        ipaddress.IPv6Network,
        MutableSequence[
            Union[
                ipaddress.IPv4Address,
                ipaddress.IPv6Address,
                ipaddress.IPv4Network,
                ipaddress.IPv6Network,
            ]
        ],
    ],
    network_id: Optional[str] = None,
    tracking_method: Optional[str] = None,
    host_dns: Optional[str] = None,
    host_netbios: Optional[str] = None,
    owner: Optional[str] = None,
    ud1: Optional[str] = None,
    ud2: Optional[str] = None,
    ud3: Optional[str] = None,
    comment: Optional[str] = None,
) -> dict[str, str]:
    """Update IP addresses in the user's subscription.

    Host attributes you can update include tracking method (IP, DNS, NETBIOS), owner, user-defined
    fields (ud1, ud2, ud3), and comments.

    You cannot update an IP to use tracking method EC2 or AGENT. Also, if an IP is already tracked
    by EC2 or AGENT, you cannot change the tracking method to something else. Qualys will skip the
    tracking method update in these cases.

    You can update multiple IPs/ranges in the same request. The host attribute changes will apply to
    all IPs included in the action.

    Args:
        ips:
            The hosts within the subscription you want to update.
        network_id:
            Optional, and valid only when the Network Support feature is enabled for the user's
            account. Restrict the request to a certain custom network by specifying the network ID.
            When unspecified, Qualys defaults to “0” for Global Default Network.
        tracking_method:
            To change to another tracking method specify "IP" for IP address, "DNS", or "NETBIOS".
        host_dns:
            The DNS hostname for the IP you want to update. A single IP must be specified in the
            same request and the IP will only be updated if it matches the hostname specified.
        host_netbios:
            The NetBIOS hostname for the IP you want to update. A single IP must be specified in the
            same request and the IP will only be updated if it matches the hostname specified.
        owner:
             The owner of the host asset(s). The owner must be a Manager. Another user (Unit
             Manager, Scanner, Reader) can be the owner if the IP address is in the user's account.
        ud1:
            Values for user-defined field 1. You can specify a maximum of 128 characters (ascii) for
            the field value.
        ud2:
            Values for user-defined field 2. You can specify a maximum of 128 characters (ascii) for
            the field value.
        ud3:
            Values for user-defined field 3. You can specify a maximum of 128 characters (ascii) for
            the field value.
        comment:
            User-defined comments.

    Returns:
        A dictionary containing information on the status of the operation.

    Raises:
        Duplicate_Hosts_Error:
            There is more than one asset record for one of the IP addresses specified.
    """

    params = {
        "ips": qutils.ips_to_qualys_format(ips),
        "network_id": network_id,
        "tracking_method": tracking_method,
        "host_dns": host_dns,
        "host_netbios": host_netbios,
        "owner": owner,
        "ud1": ud1,
        "ud2": ud2,
        "ud3": ud3,
        "comment": comment,
    }

    response = conn.post(
        URLS["Update IPs"], params=qutils.remove_nones_from_dict(params)
    )

    if response.tag == "DUPLICATE_HOSTS_ERROR_OUTPUT":
        err = (
            str(response.RESPONSE.WARNING.TEXT)
            + "\n\n"
            + "Duplicate hosts (IP, DNS Hostname, NetBIOS Hostname, Last Scandate, Tracking):\n"
        )
        for duplicate_host in response.RESPONSE.WARNING.DUPLICATE_HOSTS:
            err += "f{duplicate_host.IP}, {duplicate_host.DNS_HOSTNAME}, "
            f"{duplicate_host.NETBIOS_HOSTNAME}, {duplicate_host.LAST_SCANDATE}, "
            f"{duplicate_host.TRACKING}\n"
        raise Duplicate_Hosts_Error(err)

    return qutils.parse_simple_return(response)


@dataclasses.dataclass
class Asset_Group:
    id: str
    title: str


@dataclasses.dataclass
class Asset_Group_List:
    asset_group: MutableSequence[Asset_Group]


@dataclasses.dataclass
class User:
    user_login: str
    first_name: str
    last_name: str


@dataclasses.dataclass
class User_List:
    user: MutableSequence[User]


@dataclasses.dataclass
class User_Def:
    label_1: Optional[str] = None
    label_2: Optional[str] = None
    label_3: Optional[str] = None
    value_1: Optional[str] = None
    value_2: Optional[str] = None
    value_3: Optional[str] = None


@dataclasses.dataclass
class Glossary:
    user_def: Optional[User_Def] = None
    user_list: Optional[User_List] = None
    asset_group_list: Optional[Asset_Group_List] = None


@dataclasses.dataclass
class Warning:
    text: str
    code: Optional[str] = None
    url: Optional[str] = None


@dataclasses.dataclass
class Cloud_Tag:
    name: str
    value: str
    last_success_date: str


@dataclasses.dataclass
class Cloud_Provider_Tags:
    cloud_tag: MutableSequence[Cloud_Tag]


@dataclasses.dataclass
class Attribute:
    name: str
    last_status: str
    value: str
    last_success_date: Optional[str] = None
    last_error_date: Optional[str] = None
    last_error: Optional[str] = None


@dataclasses.dataclass
class Azure:
    attribute: Optional[MutableSequence[Attribute]] = None


@dataclasses.dataclass
class Google:
    attribute: Optional[MutableSequence[Attribute]] = None


@dataclasses.dataclass
class Ec2:
    attribute: Optional[MutableSequence[Attribute]] = None


@dataclasses.dataclass
class Metadata:
    ec2: Optional[Ec2] = None
    google: Optional[Google] = None
    azure: Optional[Azure] = None


@dataclasses.dataclass
class Tag:
    tag_id: Optional[str] = None
    name: Optional[str] = None


@dataclasses.dataclass
class Ars_Factors:
    ars_formula: str
    vuln_count: Optional[MutableSequence[str]] = None


@dataclasses.dataclass
class Host:
    id: str
    """The host ID."""

    asset_id: Optional[str] = None
    """The asset ID of the host."""

    ip: Optional[ipaddress.IPv4Address] = None
    """The asset's IP address."""

    ipv6: Optional[ipaddress.IPv6Address] = None
    """The asset's IPv6 address."""

    asset_risk_score: Optional[int] = None
    """The asset risk score (ARS). This is the overall risk score assigned to the asset
    based on multiple contributing factors. ARS has a range from 0 to 1000:
    - Severe (850-1000)
    - High (700-849)
    - Medium (500-699)
    - Low (0-499)
    """

    asset_criticality_score: Optional[int] = None
    """The asset criticality score (ACS)."""

    ars_factors: Optional[Ars_Factors] = None
    """Factors used in calculating the ARS of the host."""

    tracking_method: Optional[str] = None
    """The tracking method assigned to the asset: IP, DNS, NETBIOS, EC2."""

    network_id: Optional[str] = None
    """The network ID of the asset, if the Networks feature is enabled."""

    dns: Optional[str] = None
    """DNS name for the asset. For an EC2 asset this is the private DNS name."""

    hostname: Optional[str] = None
    """The DNS hostname for the asset."""

    domain: Optional[str] = None
    """The domain name for the asset."""

    fqdn: Optional[str] = None
    """The Fully Qualified Domain Name (FQDN) for the asset."""

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
    """A list of tags associated with the asset."""

    metadata: Optional[Metadata] = None
    cloud_provider_tags: Optional[Cloud_Provider_Tags] = None
    last_vuln_scan_datetime: Optional[str] = None
    last_vm_scanned_date: Optional[str] = None
    last_vm_scanned_duration: Optional[str] = None
    last_vm_auth_scanned_date: Optional[str] = None
    last_vm_auth_scanned_duration: Optional[str] = None
    last_compliance_scan_datetime: Optional[str] = None
    last_scap_scan_datetime: Optional[str] = None
    owner: Optional[str] = None
    comments: Optional[str] = None
    user_def: Optional[User_Def] = None
    asset_group_ids: Optional[str] = None
