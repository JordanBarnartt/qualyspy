import ipaddress
import math
from collections.abc import MutableMapping, MutableSequence
from typing import Any, Optional, Union, TypeVar
import datetime
import json
import importlib.resources

import lxml.etree
import lxml.objectify


URLS = json.load(importlib.resources.files("qualyspy").joinpath("urls.json").open())


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
        MutableSequence[
            Union[
                ipaddress.IPv4Address,
                ipaddress.IPv4Network,
            ]
        ],
        MutableSequence[
            Union[
                ipaddress.IPv6Address,
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
    ip_list: MutableSequence[lxml.objectify.ObjectifiedElement],
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
        if not ip.text:
            raise ValueError(f"ip {ip} does not have a text value")
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


# def parse_elements(xml: lxml.objectify.ObjectifiedElement) -> dict[str, Any]:
#     """Parse a tree of lxml objects into a dictionary of tag:value pairs, where tags with
#     descendants are themselves dictionarys.

#     Args:
#         xml:
#             The xml tree to be parsed.

#     Returns:
#         A dictionary containing the information from the lxml object, in the same hierarchy.
#     """

#     elements_dict: dict[str, Any] = {}

#     for child in xml.iterchildren():
#         if type(child) == lxml.objectify.ObjectifiedElement:
#             elements_dict[child.tag.lower()] = parse_elements(child)
#         elif child.text:
#             elements_dict[child.tag.lower()] = child.text

#     return elements_dict


C = TypeVar("C")


def elements_to_class(
    xml: Union[lxml.objectify.ObjectifiedElement, lxml.etree._Element],
    output_class: type[C],
    classmap: MutableMapping[str, Any] = {},
    list_elements: MutableMapping[str, str] = {},
) -> C:
    """Parse a tree of lxml elements into a given class.  The output class can have attributes which
    are themselves different classes, or which convert a group of identically named subelements to
    a list.

    Args:
        xml:
            The XML tree to be parsed.
        output_class:
            The Python class which the tree should be converted to.
        classmap:
            A mapping where the keys are element tags in the XML tree which should be converted to
            classes to be used as attributes of output_class, and the values are the classes to
            convert the subelements of the corresponding element into.
        list_elements:
            A mapping where the keys are element tags in the XML tree which contain a number of
            subelements with identical tags which should be converted into a list as an attribute
            of output_class, and the values are the names of the corresponding identical tags.
    """

    elements_dict: dict[str, Any] = {}

    for child in xml.iterchildren():
        t = child.tag.lower()
        if len([n for n in child.iterdescendants()]) > 0:
            if t in list_elements:
                elements_dict[t] = []
                subelements = child.findall(list_elements[t].upper())
                for subelement in subelements:
                    elements_dict[t].append(
                        elements_to_class(subelement, classmap[list_elements[t]])
                    )
            else:
                elements_dict[t] = elements_to_class(child, classmap[t])
        elif child.text:
            elements_dict[t] = child.text

    return output_class(**elements_dict)


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


def to_comma_separated(input: Any) -> Optional[str]:
    """Converts a list of items into a single string containing each item's string representations
    sorted by a comma, for easy ingestion into the Qualys API.  If a non-list object is passed,
    returns the string representation of the object
    """

    if input is None:
        return None

    if not isinstance(input, MutableSequence):
        return str(input)

    output = ""
    for item in input:
        output += str(item) + ","

    output.rstrip(",")  # Remove final comma
    return output


def datetime_to_qualys_format(dt: Optional[datetime.datetime]) -> Optional[str]:
    """Converts a Python datetime object to the string format used by the Qualys API."""

    if dt is None:
        return None
    else:
        return dt.isoformat()


def datetime_from_qualys_format(dt: str) -> datetime.datetime:
    """Converts a datetime string as returned by the Qualys API into a Python datetime object."""

    return datetime.datetime.fromisoformat(dt)


def parse_optional_bool(
    b: Optional[bool], returns: tuple[str, str] = ("1", "0")
) -> Optional[str]:
    """Converts a bool or None to a value parseably by the Qualys API.

    Args:
        b: The boolean value to parse.
        returns: The values to return depending on if the input is True or
        False (in that order).
    """

    if b is None:
        return None
    elif b:
        return returns[0]
    else:
        return returns[1]
