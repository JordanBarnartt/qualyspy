from . import URLS
from .base import QualysAPIBase
from .exceptions import QualysAPIError
from typing import Any

from .models.asset_mgmt_tagging import tag as tag_models
from .models.asset_mgmt_tagging import (
    azure_asset_data_connector as azure_connector_models,
)

from xsdata.formats.dataclass.serializers import JsonSerializer

import json


def _filter_none_emptylist(x: tuple[Any]) -> dict[str, Any]:
    return {k: v for k, v in x if (v is not None) and (not v == [])}


# def _filter_none_emptylist(x: tuple[Any]) -> dict[str, Any]:
#     ret = {}
#     for k, v in x:
#         if isinstance(v, list):
#             if len(v) == 0:
#                 continue
#             inst_type = type(v[0])
#             ret[k] = {str(inst_type.__name__): [_filter_none_emptylist(i) for i in v]}
#         elif v is not None:
#             ret[k] = v
#     return ret


class PaginationSettings:
    """Pagination settings for tag search.

    Args:
        start_from_offset (int, optional): The first item to return by indedx.  The default is 1.
        start_from_id (int, optional): The first item to return by ID.  No default value.
        limit_results (int, optional): The maximum number of items to return.  The default is 100.
    """

    def __init__(
        self,
        start_from_offset: int | None = None,
        start_from_id: int | None = None,
        limit_results: int | None = None,
    ):
        self.start_from_offset = start_from_offset
        self.start_from_id = start_from_id
        self.limit_results = limit_results

    def _preferences(self) -> dict[str, dict[str, int | None]]:
        return {
            "preferences": {
                "startFromOffset": self.start_from_offset,
                "startFromId": self.start_from_id,
                "limitResults": self.limit_results,
            }
        }


class Filter:
    """A filter to apply to a tag search.

    Args:
        field (str): The field to filter on.
        operator (str): The operator to use for the filter.
        value (str): The value to filter on.
    """

    def __init__(self, field: str, operator: str, value: str):
        self.field = field
        self.operator = operator
        self.value = value

    def _as_dict(self) -> dict[str, str]:
        return {
            "field": self.field,
            "operator": self.operator,
            "value": self.value,
        }


class TagsAPI(QualysAPIBase):
    """This class contains methods for interacting with Qualys tags."""

    def _manage_tag(self, tag: tag_models.Tag, url: str) -> list[tag_models.Tag]:
        """Helper function for tag operations.

        Args:
            tag (tag_models.Tag): The tag to create or update.
            url (str): The URL to use for the request.

        Returns:
            list[tag_models.Tag]: The created or updated tag.

        Raises:
            QualysAPIError: If the API returns an error.
        """
        tag_json = JsonSerializer(dict_factory=_filter_none_emptylist).render(tag)
        tag_json = json.loads(tag_json)
        data = {"ServiceRequest": {"data": {"Tag": tag_json}}}
        response = self.post(url, data=json.dumps(data))
        ret = json.loads(response.text)
        if ret["ServiceResponse"]["responseCode"] != "SUCCESS":
            raise QualysAPIError(ret["ServiceResponse"])
        tags: list[tag_models.Tag] = []
        for i in range(len(ret["ServiceResponse"]["data"])):
            if "Tag" in ret["ServiceResponse"]["data"][i]:
                tags.append(tag_models.Tag(**ret["ServiceResponse"]["data"][i]["Tag"]))
        return tags

    def create_tag(self, tag: tag_models.Tag) -> tag_models.Tag:
        """Create a new tag and possibly child tags.

        Args:
            tag (tag_models.Tag): The tag to create.

        Returns:
            tag_models.Tag: The created tag.
        """
        return self._manage_tag(tag, URLS.create_tag)[0]

    def update_tag(self, id: int, tag: tag_models.Tag) -> tag_models.Tag:
        """Update fields for a tag.

        Args:
            id (int): The ID of the tag to update.
            tag (tag_models.Tag): The tag fields to update.

        Returns:
            tag_models.Tag: The updated tag.
        """
        return self._manage_tag(tag, URLS.update_tag + f"/{id}")[0]

    def search_tags(
        self,
        filters: list[Filter],
        pagination_settings: PaginationSettings | None = None,
    ) -> list[tag_models.Tag]:
        """Returns a list of tags matching the given criteria.

        Args:
            filters (list[Filter]): The filters to apply to the search.

        Returns:
            list[tag_models.Tag]: The tags matching the given criteria.
        """
        data = {
            "ServiceRequest": {"filters": {"Criteria": [f._as_dict() for f in filters]}}
        }
        if pagination_settings is not None:
            data["ServiceRequest"].update(pagination_settings._preferences())  # type: ignore
        response = self.post(URLS.search_tags, data=json.dumps(data))
        ret = json.loads(response.text)
        if ret["ServiceResponse"]["responseCode"] != "SUCCESS":
            raise QualysAPIError(ret["ServiceResponse"])
        tags: list[tag_models.Tag] = []
        for i in range(len(ret["ServiceResponse"]["data"])):
            if "Tag" in ret["ServiceResponse"]["data"][i]:
                tags.append(tag_models.Tag(**ret["ServiceResponse"]["data"][i]["Tag"]))
        return tags

    def count_tags(self, filters: list[Filter]) -> int:
        """Returns the number of tags matching the given criteria.

        Args:
            filters (list[Filter]): The filters to apply to the search.

        Returns:
            int: The number of tags matching the given criteria.
        """
        data = {
            "ServiceRequest": {"filters": {"Criteria": [f._as_dict() for f in filters]}}
        }
        response = self.post(URLS.count_tags, data=json.dumps(data))
        ret = json.loads(response.text)
        if ret["ServiceResponse"]["responseCode"] != "SUCCESS":
            raise QualysAPIError(ret["ServiceResponse"])
        return int(ret["ServiceResponse"]["count"])

    def delete_tag(self, id: int) -> tag_models.TagSimple:
        """Delete a tag.

        Args:
            id (int): The ID of the tag to delete.

        Returns:
            tag_models.TagSimple: The deleted tag.
        """
        response = self.post(URLS.delete_tag + f"/{id}")
        ret = json.loads(response.text)
        if ret["ServiceResponse"]["responseCode"] != "SUCCESS":
            raise QualysAPIError(ret["ServiceResponse"])
        return tag_models.TagSimple(**ret["ServiceResponse"]["data"][0]["Tag"])


class AzureConnectorAPI(QualysAPIBase):
    """This class contains methods for interacting with Qualys Azure Connectors."""

    def create_azure_connector(
        self, connector: azure_connector_models.AzureAssetDataConnector
    ) -> azure_connector_models.AzureAssetDataConnector:
        """Create a new Azure connector.

        Args:
            connector (azure_connector_models.AzureAssetDataConnector): The connector to create.

        Returns:
            azure_connector_models.AzureAssetDataConnector: The created connector.
        """
        connector_json = json.loads(
            JsonSerializer(dict_factory=_filter_none_emptylist).render(connector)
        )
        data = {"ServiceRequest": {"data": {"AzureAssetDataConnector": connector_json}}}
        response = self.post(URLS.create_azure_connector, data=json.dumps(data))
        ret = json.loads(response.text)
        if ret["ServiceResponse"]["responseCode"] != "SUCCESS":
            raise QualysAPIError(ret["ServiceResponse"])
        if "AzureAssetDataConnector" in ret["ServiceResponse"]["data"][0]:
            new_connector = azure_connector_models.AzureAssetDataConnector(
                **ret["ServiceResponse"]["data"][0]["AzureAssetDataConnector"]
            )
        return new_connector
