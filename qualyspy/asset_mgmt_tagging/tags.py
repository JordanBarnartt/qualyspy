"""Python wrapper for the Qualys Asset Management and Tagging v2 Tags API."""

import dataclasses
import datetime
import json
from collections.abc import MutableSequence
from typing import Any, Optional, Union

import qualyspy.qualysapi as qualysapi
import qualyspy.qutils as qutils


@dataclasses.dataclass
class TagSimple:
    """A simple representation of a Qualys Asset Tag, containing only the name and ID of the tag.
    Child tags will appear in this format.

    Not intended to be intantied manually, but as a result of function calls.
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
    """A representation of a Qualys Asset Tag.

    Not intended to be intantied manually, but as a result of function calls.
    """

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


def create_tag(
    conn: qualysapi.Connection,
    name: str,
    /,
    parent_tag_id: Optional[int] = None,
    color: Optional[str] = None,
    rule_text: Optional[str] = None,
    rule_type: Optional[str] = None,
    children: Optional[MutableSequence[Union[str, int]]] = None,
    criticality_score: Optional[int] = None,
    description: Optional[str] = None,
) -> None:
    """Create a new tag and possibly child tags.

    Args:
        conn:
            A connection to the Qualys API.
        name:
            The name of the new tag.
        parent_tag_id:
            The ID of the tag which should be the parent of this tag.
        color:
            The hex code for the color of the tag.
        rule_text:
            The text of the dyanmic tag rule applied to this tag.
        rule_type:
            The type of dynamic tag rule this tag should have.  Must be one of: static, groovy,
            os_regex, network_range, network_range_enhanced, name_contains, installed_software,
            open_ports, vuln_exists, asset_search, cloud_asset, business_information.
        children:
            A list of tags which should be children of this tag.  A string will correspond to a tag
            name and and int will correspond to a tag ID.  If a tag specified by name does not
            exist, it will be created.
        criticality_scrore:
            The criticality score applied to hosts with this tag.
        description:
            The description of the tag.
    """

    elements = {
        "name": name,
        "parentTagId": str(parent_tag_id) if parent_tag_id else None,
        "color": color,
        "ruleText": rule_text,
        "ruleType": rule_type,
        "criticalityScore": str(criticality_score) if criticality_score else None,
        "description": description,
    }

    elements_parsed: dict[str, Any] = {
        "ServiceRequest": {"data": {"Tag": qutils.remove_nones_from_dict(elements)}}
    }

    if children is not None:
        tag = elements_parsed["ServiceRequest"]["data"]["Tag"]
        tag["children"] = {"set": {"TagSimple": []}}
        for child in children:
            if isinstance(child, str):
                tag["children"]["set"]["TagSimple"].append({"name": child})
            elif isinstance(child, int):
                tag["children"]["set"]["TagSimple"].append({"id": str(child)})

    conn.headers["Content-Type"] = "application/json"
    conn.headers["Accept"] = "application/xml"
    response = conn.post(
        qutils.URLS["Create Tag"], json.dumps(elements_parsed), use_auth=True
    )

    response_code = str(response.responseCode)
    if response_code != "SUCCESS":
        raise qualysapi.Qualys_API_Error(response.responseErrorDetails.errorMessage)
