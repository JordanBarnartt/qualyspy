"""Python wrapper to work with the Qualys Assets API.

Manage the host assets you want to scan (internal and external facing) for vulnerabilities and
compliance.
"""

import dataclasses
from collections.abc import MutableSequence
from typing import Union, Optional
import ipaddress
import json
import importlib.resources

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

    ips_qualys_format: MutableSequence[str]
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
    """

    good_tracking_methods = ["IP", "DNS", "NETBIOS"]
    if tracking_method and tracking_method not in good_tracking_methods:
        raise ValueError(f"tracking method must be one of {good_tracking_methods}.")

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
        "compliance_enabled": compliance_enabled_str if compliance_enabled is not None else None,
        "certview_enalbed": certview_enabled_str if compliance_enabled is not None else None,
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
