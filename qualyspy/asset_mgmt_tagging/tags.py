"""Python wrapper for the Qualys Asset Management and Tagging v2 Tags API."""

import dataclasses
import datetime
from collections.abc import MutableSequence
from typing import Any, Optional, Union

import qualyspy.qualysapi as qualysapi
import qualyspy.qutils as qutils
from qualyspy.asset_mgmt_tagging.filter import Filter


def _create_service_request(elements: dict[str, Optional[str]]) -> dict[str, Any]:
    return {
        "ServiceRequest": {"data": {"Tag": qutils.remove_nones_from_dict(elements)}}
    }


@dataclasses.dataclass
class Tag_Simple:
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
class Tag(Tag_Simple):
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

    children: Optional[MutableSequence[Tag_Simple]] = None
    """A list of child tags under this tag."""

    criticality_score: Optional[int] = None
    """Criticality Score assigned to assets with this tag."""

    description: Optional[str] = None
    """Description of the tag."""

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == "children" and isinstance(__value, _Tag_Simple_Q_List):
            return super().__setattr__(__name, __value.list)
        else:
            return super().__setattr__(__name, __value)

    def _get_children_list(self) -> MutableSequence[Union[str, int]]:
        children_list: list[Union[str, int]] = []
        if self.children:
            for child in self.children:
                if child.name:
                    children_list.append(child.name)
                elif child.id:
                    children_list.append(child.id)
        return children_list

    def update_tag(
        self,
        conn: qualysapi.Connection,
        /,
        criticality_score: Optional[int] = None,
        rule_type: Optional[str] = None,
        rule_text: Optional[str] = None,
        color: Optional[str] = None,
        children: Optional[MutableSequence[Union[str, int]]] = None,
    ) -> None:
        """Update fields for a tag and collections of tags."""

        elements = {
            "criticalityScore": str(criticality_score),
            "ruleType": rule_type,
            "ruleText": rule_text,
            "color": color,
        }

        elements_parsed = _create_service_request(elements)

        if children is not None:
            tag = elements_parsed["ServiceRequest"]["data"]["Tag"]
            children_list = self._get_children_list()
            to_add = set(children).difference(set(children_list))
            to_remove = set(children_list).difference(set(children))
            tag["children"] = {}
            if len(to_add) > 0:
                tag["children"]["set"] = []
                tag["children"]["set"] += [
                    {"name": t} for t in to_add if isinstance(t, str)
                ]

                tag["children"]["set"] += [
                    {"id": t} for t in to_add if isinstance(t, int)
                ]

            if len(to_remove) > 0:
                tag["children"]["remove"] = []
                tag["children"]["remove"] += [
                    {"name": t} for t in to_add if isinstance(t, str)
                ]
                tag["children"]["remove"] += [
                    {"id": t} for t in to_add if isinstance(t, int)
                ]

        conn.post(qutils.URLS["Update Tag"], elements_parsed, use_auth=True)


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
        criticality_score:
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

    elements_parsed = _create_service_request(elements)
    tag = elements_parsed["ServiceRequest"]["data"]["Tag"]

    if children is not None:
        tag = elements_parsed["ServiceRequest"]["data"]["Tag"]
        tag["children"] = {"set": {"TagSimple": []}}
        for child in children:
            if isinstance(child, str):
                tag["children"]["set"]["TagSimple"].append({"name": child})
            elif isinstance(child, int):
                tag["children"]["set"]["TagSimple"].append({"id": str(child)})

    add_headers = {"Content-Type": "application/json", "Accept": "application/xml"}
    conn.post(
        qutils.URLS["Create Tag"],
        elements_parsed,
        use_auth=True,
        add_headers=add_headers,
    )


@dataclasses.dataclass
class _Tag_Simple_Q_List:
    """Class containing a list of Tag_Simples, needed to parse output from Qualys."""

    count: Optional[int] = None
    list: Optional[MutableSequence[Tag_Simple]] = None
    set: Optional[MutableSequence[Tag_Simple]] = None
    add: Optional[MutableSequence[Tag_Simple]] = None
    remove: Optional[MutableSequence[Tag_Simple]] = None
    update: Optional[MutableSequence[Tag_Simple]] = None


def search_tags(
    conn: qualysapi.Connection,
    filters: Union[Filter, MutableSequence[Filter]],
) -> list[Tag]:
    """Returns a list of tags that match the provided criteria.

    Args:
        conn:
            A connection to the Qualys API.
        filters:
            A Filter or list of Filters used to filter the results of the search.
    """

    data: dict[str, Any] = {"ServiceRequest": {"filters": {"Criteria": []}}}
    if not isinstance(filters, MutableSequence):
        filters = [filters]
    for filter in filters:
        criteria = {
            "field": filter.field,
            "operator": filter.operator,
            "value": filter.value,
        }
    data["ServiceRequest"]["filters"]["Criteria"].append(criteria)

    add_headers = {"Content-Type": "application/json", "Accept": "application/xml"}
    raw = conn.post(
        qutils.URLS["Search Tags"], data, use_auth=True, add_headers=add_headers
    )

    tag_list: list[Tag] = []
    if str(raw.count) == "0":
        return tag_list
    for tag in raw.data.Tag:
        t = qutils.elements_to_class(
            tag,
            Tag,
            classmap={"Tag_Simple": Tag_Simple, "children": _Tag_Simple_Q_List},
            listmap={
                "list": "Tag_Simple",
            },
            funcmap={
                "id": int,
                "parent_tag_id": int,
                "created": qutils.datetime_from_qualys_format,
                "modified": qutils.datetime_from_qualys_format,
                "src_asset_group_id": int,
                "src_business_unit_id": int,
                "src_operating_system_name": int,
                "criticality_score": int,
            },
            name_converter=qutils.convert_camel_to_snake,
        )
        tag_list.append(t)

    return tag_list
