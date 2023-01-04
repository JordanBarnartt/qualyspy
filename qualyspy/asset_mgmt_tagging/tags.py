"""Python wrapper for the Qualys Asset Management and Tagging v2 Tags API."""

import dataclasses
import datetime
from collections.abc import MutableSequence
from typing import Optional

import qualyspy.qualysapi as qualysapi
import qualyspy.qutils as qutils


@dataclasses.dataclass
class TagSimple:
    """A simple representation of a Qualys Asset Tag, containing only the name and ID of the tag.

    Child tags will appear in this format.
    """

    name: Optional[str] = None
    """The name of the tag."""

    id: Optional[int] = None
    """The ID of the tag."""

    def __post_init__(self) -> None:
        if self.name is None and self.id is None:
            raise ValueError("One of name or id must be specified.")


@dataclasses.dataclass
class Tag(TagSimple):
    """A representation of a Qualys Asset Tag."""

    parent_tag_id: Optional[int] = None
    """ID of the parent tag of this tag."""

    created: Optional[datetime.datetime] = None
    """Datetime at which this tag was created."""

    modified: Optional[datetime.datetime] = None
    """Datetime at which this tag was most recently modified."""

    color: Optional[str] = None
    """Hex code of tag color."""

    rule_text: Optional[str] = None
    """Text of dynamic tag rule."""

    rule_type: Optional[str] = None
    """Type of tag rule. Must be one of: static, groovy, os_regex, network_range,
    network_range_enhanced, name_contains, installed_software, open_ports, vuln_exists,
    asset_search, cloud_asset, business_information.
    """

    src_asset_group_id: Optional[int] = None
    """ID of the asset group which generated this tag."""

    src_business_unit_id: Optional[int] = None
    """ID of the business unit which generated this tag."""

    src_operating_system_name: Optional[int] = None
    """Name of the operating system associated with this tag."""

    provider: Optional[str] = None
    """Source of the creation of the tag, if it was automatically generated."""

    children: Optional[MutableSequence[TagSimple]] = None
    """A list of child tags under this tag."""

    criticality_score: Optional[int] = None
    """Criticality Score assigned to assets with this tag."""

    description: Optional[str] = None
    """Description of the tag."""

def 
