import ipaddress
from typing import Any, Union, Optional
from collections.abc import MutableSequence, MutableMapping
import lxml.objectify
import math


class Qualys_Mixin:
    """A mixin class to be used with dataclass objects representing Qualys API parameters.

    A _check_parameters method must be defined in each class which inherits from this one.  This
    method will check for things such as mutual exclusiveness or whether a string value is one of
    an acceptable list of values.

    The __post_init__ method ensures that parameters are checked after class creation, and the
    __setattr__ method ensure that this is checked after parameters change.
    """

    def __post_init__(self) -> None:
        self._check_parameters()

    def __setattr__(self, __name: str, __value: Any) -> None:
        super().__setattr__(__name, __value)
        self._check_parameters()

    def _check_parameters(self) -> None:
        """Confirms that any value with additional restrictions meets those restrictions."""


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

    output = {}
    for key, value in d.items():
        if value is not None:
            output[key] = value
    return output


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
