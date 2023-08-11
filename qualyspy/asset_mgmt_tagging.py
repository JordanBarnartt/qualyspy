from . import URLS
from .base import QualysAPIBase
from .exceptions import QualysAPIError
from typing import Any

from .models.asset_mgmt_tagging import tag as tag_models
from xsdata.formats.dataclass.serializers import JsonSerializer

import json


def _filter_none(x: tuple[Any]) -> dict[str, Any]:
    return {k: v for k, v in x if v is not None}


class PaginationSettings:
    def __init__(
        self,
        start_from_offset: int | None = None,
        start_from_id: int | None = None,
        limit_results: int | None = None,
    ):
        self.start_from_offset = start_from_offset
        self.start_from_id = start_from_id
        self.limit_results = limit_results

    def preferences(self) -> dict[str, dict[str, int | None]]:
        return {
            "preferences": {
                "startFromOffset": self.start_from_offset,
                "startFromId": self.start_from_id,
                "limitResults": self.limit_results,
            }
        }


class Filter:
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


class Tags(QualysAPIBase):
    def _manage_tag(self, tag: tag_models.Tag, url: str) -> list[tag_models.Tag]:
        tag_json = json.loads(JsonSerializer(dict_factory=_filter_none).render(tag))
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
        return self._manage_tag(tag, URLS.create_tag)[0]

    def update_tag(self, id: int, tag: tag_models.Tag) -> tag_models.Tag:
        return self._manage_tag(tag, URLS.update_tag + f"/{id}")[0]

    def search_tags(self, filters: list[Filter]) -> list[tag_models.Tag]:
        data = {
            "ServiceRequest": {"filters": {"Criteria": [f._as_dict() for f in filters]}}
        }
        response = self.post(URLS.search_tags, data=json.dumps(data))
        ret = json.loads(response.text)
        if ret["ServiceResponse"]["responseCode"] != "SUCCESS":
            raise QualysAPIError(ret["ServiceResponse"])
        tags: list[tag_models.Tag] = []
        for i in range(len(ret["ServiceResponse"]["data"])):
            if "Tag" in ret["ServiceResponse"]["data"][i]:
                tags.append(tag_models.Tag(**ret["ServiceResponse"]["data"][i]["Tag"]))
        return tags
