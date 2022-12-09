import ipaddress
from typing import Any, Union, Optional
from collections.abc import MutableSequence, MutableMapping
import lxml.objectify
import math


def ips_to_qualys_format(
    ip_list: Union[
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
    ]
) -> str:
    """Converts an IP address, IP range, or list of containing address and ranges into a string
    which the Qualys API can interpret.

    Args:
        ip_list:
            A list of IP address and IP network objects.

    Returns:
        A string of common separated IP addresses and ranges, where the ranges are in the form
        <start_IP>-<end_ip> (ex. 10.0.0.4,10.0.0.6,192.167.0.0-192.168.255.255)
    """

    output_list: MutableSequence[str] = []

    if not isinstance(ip_list, MutableSequence):
        ip_list = [ip_list]

    for ip in ip_list:
        if isinstance(ip, ipaddress.IPv4Address) or isinstance(
            ip, ipaddress.IPv6Address
        ):
            output_list.append(str(ip))
        else:
            start_ip = ip.network_address
            end_ip = ip.network_address + ip.num_addresses - 1
            output_list.append(str(start_ip) + "-" + str(end_ip))

    output = ",".join(output_list)
    return output


def ips_from_qualys_format(
    ip_list: MutableSequence[lxml.objectify.StringElement],
) -> MutableSequence[
    Union[
        ipaddress.IPv4Address,
        ipaddress.IPv6Address,
        ipaddress.IPv4Network,
        ipaddress.IPv6Network,
    ]
]:
    """Converts a list of IP addresses and ranges as provided by Qualys into a list of Python
    ipaddress and range objects.

    Args:
        ip_list:
            A list of lxml objects, each containing the Qualys representation of an IP address or
            range.

    Returns:
        The input list of IP addresses and ranges, represented as Python ipaddress objects.
    """

    output_list: MutableSequence[
        Union[
            ipaddress.IPv4Address,
            ipaddress.IPv6Address,
            ipaddress.IPv4Network,
            ipaddress.IPv6Network,
        ]
    ] = []

    for ip in ip_list:
        if "-" in ip.text:
            # Check if the size of the range is a power of 2, and if so, represent it as a network
            #  rather than a list of individual addresses.
            start_ip, end_ip = (ipaddress.ip_address(i) for i in ip.text.split("-"))
            if math.log2(int(end_ip) - int(start_ip) + 1).is_integer():
                mask = int(math.log2(int(end_ip) - int(start_ip) + 1))
                output_list.append(
                    ipaddress.ip_network(str(start_ip) + "/" + str(32 - mask))
                )
            else:
                if isinstance(start_ip, ipaddress.IPv4Address) and isinstance(
                    end_ip, ipaddress.IPv4Address
                ):
                    ip4_to_add = start_ip
                    while ip4_to_add <= end_ip:
                        output_list.append(ipaddress.ip_address(ip4_to_add))
                elif isinstance(start_ip, ipaddress.IPv6Address) and isinstance(
                    end_ip, ipaddress.IPv6Address
                ):
                    ip6_to_add = start_ip
                    while ip6_to_add <= end_ip:
                        output_list.append(ipaddress.ip_address(ip6_to_add))
                else:
                    ValueError(f"{start_ip} and {end_ip} are not of the same version")
        else:
            output_list.append(ipaddress.ip_address(ip.text))

    return output_list


def remove_nones_from_dict(d: MutableMapping[str, Optional[str]]) -> dict[str, str]:
    """Removes all keys from a dictionary whose values are None.

    Args:
        d:
            A dictionary (or any other MutableMapping).

    Returns:
        A dictionary containing the same information, with any keys whose values were None removed.
    """

    return {k: v for k, v in d.items() if v is not None}


def parse_elements(xml: lxml.objectify.ObjectifiedElement) -> dict[str, Any]:
    """Parse a tree of lxml objects into a dictionary of tag:value pairs, where tags with
    descendants are themselves dictionarys.

    Args:
        xml:
            The xml tree to be parsed.

    Returns:
        A dictionary containing the information from the lxml object, in the same hierarchy.
    """

    elements_dict: dict[str, Any] = {}

    for child in xml.iterchildren():
        if type(child) == lxml.objectify.ObjectifiedElement:
            elements_dict[child.tag.lower()] = parse_elements(child)
        elif child.text:
            elements_dict[child.tag.lower()] = child.text

    return elements_dict


def parse_simple_return(xml: lxml.objectify.ObjectifiedElement) -> dict[str, Any]:
    """The simple return is XML output returned from several API calls.  The function parses that
    XML into a dictionary.

    Args:
        xml:
            The xml tree to be parsed.

    Returns:
        A dictionary containing the item_list of the XML in key:value pairs.
    """

    output: dict[str, Any] = {}
    output["TEXT"] = str(xml.RESPONSE.TEXT)
    for item in xml.RESPONSE.ITEM_LIST.ITEM:
        output[str(item.KEY)] = item.VALUE

    return output
