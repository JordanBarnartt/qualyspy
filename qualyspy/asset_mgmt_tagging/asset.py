import dataclasses
import datetime
from collections.abc import MutableSequence
from typing import Any, Optional, Union

import qualyspy.qualysapi as qualysapi
import qualyspy.qutils as qutils
from qualyspy.asset_mgmt_tagging.filter import Filter
from qualyspy.asset_mgmt_tagging.tags import Tag_Simple, _Tag_Simple_Q_List


@dataclasses.dataclass
class Asset:
    """An object representing an asset in the Qualys AssetView API."""

    id: int
    """The ID number of the asset."""

    name: str
    """The name of the asset."""

    created: datetime.datetime
    """The date and time at which the asset was created."""

    modified: datetime.datetime
    """The date and time at which the asset entry was last modified."""

    type: str
    """The type of the asset.  One of unknonw, host, scanner, webapp, malware_domain."""

    tags: Optional[MutableSequence[Tag_Simple]] = None
    """Tags associated with the asset."""

    source_info: Optional[str] = None
    """The source of the asset."""

    criticality_score: Optional[int] = None
    """The criticality score of the asset."""

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == "tags" and isinstance(__value, _Tag_Simple_Q_List):
            return super().__setattr__(__name, __value.list)
        else:
            return super().__setattr__(__name, __value)

    def update(
        self,
        conn: qualysapi.Connection,
        name: Optional[str] = None,
        tags_to_add: Optional[MutableSequence[Tag_Simple]] = None,
        tags_to_remove: Optional[MutableSequence[Tag_Simple]] = None,
    ) -> None:
        url = qutils.URLS["Update Asset"] + "/" + str(self.id)
        data: dict[str, Any] = {"ServiceRequest": {"data": {"Asset": {}}}}
        data_inner = data["ServiceRequest"]["data"]["Asset"]

        if name is not None:
            data_inner["name"] = name

        if tags_to_add or tags_to_remove:
            data_inner["tags"] = {}
        if tags_to_add:
            data_inner["tags"]["add"] = {"TagSimple": []}
            data_inner["tags"]["add"]["TagSimple"] += [
                {"id": tag.id} for tag in tags_to_add
            ]
        if tags_to_remove:
            data_inner["tags"]["remove"] = {"TagSimple": []}
            data_inner["tags"]["remove"]["TagSimple"] += [
                {"id": tag.id} for tag in tags_to_remove
            ]

        conn.post(url, data, use_auth=True)


def search_assets(
    conn: qualysapi.Connection,
    filters: Union[Filter, MutableSequence[Filter]],
) -> list[Asset]:
    """Returns a list of Assets that match the provided criteria.

    Args:
        conn:
            A connection to the Qualys API.
        filters:
            An Asset_Filter or list of Asset_Filters used to filter the results of the search.
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

    raw = conn.post(qutils.URLS["Search Assets"], data, use_auth=True)

    asset_list: list[Asset] = []
    if str(raw.count) == "0":
        return asset_list
    for asset in raw.data.Asset:
        a = qutils.elements_to_class(
            asset,
            Asset,
            classmap={
                "Asset": Asset,
                "tags": _Tag_Simple_Q_List,
                "Tag_Simple": Tag_Simple,
            },
            listmap={
                "list": "Tag_Simple",
            },
            funcmap={
                "id": int,
                "created": qutils.datetime_from_qualys_format,
                "modified": qutils.datetime_from_qualys_format,
                "criticality_score": int,
            },
            name_converter=qutils.convert_camel_to_snake,
        )
        asset_list.append(a)

    return asset_list
