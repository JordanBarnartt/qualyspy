import ipaddress
from typing import Any, Union, Optional
from collections.abc import MutableSequence, MutableMapping
import lxml.objectify


class Qualys_Mixin:
    def __post_init__(self) -> None:
        self._check_parameters()

    def __setattr__(self, __name: str, __value: Any) -> None:
        super().__setattr__(__name, __value)
        self._check_parameters()

    def _check_parameters(self) -> None:
        """Confirms that any value with additional restrictions meets those restrictions."""


def ip_list_to_qualys_format(
    ip_list: MutableSequence[
        Union[
            ipaddress.IPv4Address,
            ipaddress.IPv6Address,
            ipaddress.IPv4Network,
            ipaddress.IPv6Network,
        ]
    ]
) -> str:
    output_list: MutableSequence[str] = []

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


def remove_nones_from_dict(
    d: MutableMapping[str, Optional[str]]
) -> MutableMapping[str, str]:
    output = {}
    for key, value in d.items():
        if value is not None:
            output[key] = value
    return output


def parse_elements(
    xml: lxml.objectify.ObjectifiedElement,
    elements: MutableMapping[str, Any] = dict(),
    prefix: str = "",
) -> MutableMapping[str, Any]:
    """Parse a tree of lxml objects into a dictionary of tag:value pairs, where tags with
    descendants are themselves dictionarys.
    """

    for child in xml.iterchildren():
        if isinstance(child, lxml.objectify.ObjectifiedElement):
            elements[child.tag.lower()] = dict()
            parse_elements(child, elements[child.tag.lower()], prefix=child.tag.lower())
        else:
            elements[child.tag.lower()] = prefix + child.text

    return elements
