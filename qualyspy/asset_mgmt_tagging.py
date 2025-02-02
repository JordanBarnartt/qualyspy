from . import URLS
from .base import QualysAPIBase
from .models.asset_mgmt_tagging import (
    asset_output,
    asset_request,
    tag_output,
    tag_request,
)
from .models.asset_mgmt_tagging.asset_request import Criteria as AssetSearchCriteria


class AssetMgmtTaggingAPI(QualysAPIBase):
    def create_tag(
        self,
        name: str,
        rule_type: tag_request.tag_rule_types | None = None,
        rule_text: str | None = None,
        criticality_score: int | None = None,
        color: str | None = None,
        children: list[str] = [],
    ) -> tag_output.ServiceResponse:
        request_data = tag_request.create_add_tag_request(
            name=name,
            rule_type=rule_type,
            rule_text=rule_text,
            criticality_score=criticality_score,
            color=color,
            children=children,
        )
        request_data_xml = request_data.to_xml(
            skip_empty=True, pretty_print=True, encoding="UTF-8", xml_declaration=True
        )

        resp = self.post(
            URLS.create_tag, content=request_data_xml, content_type="application/xml"
        )
        ret = tag_output.Wrapper.model_validate_json(resp.text)

        return ret.service_response

    def update_tag(
        self,
        tag_id: int,
        name: str | None = None,
        criticality_score: int | None = None,
        rule_type: tag_request.tag_rule_types | None = None,
        rule_text: str | None = None,
        color: str | None = None,
        add_children: list[str] = [],
        remove_children: list[int] = [],
    ) -> tag_output.ServiceResponse:
        if add_children and remove_children:
            raise ValueError(
                "Cannot add and remove children at the same time. Please use separate calls."
            )
        request_data = tag_request.create_update_tag_request(
            name=name,
            rule_type=rule_type,
            rule_text=rule_text,
            criticality_score=criticality_score,
            color=color,
            add_children=add_children,
            remove_children=remove_children,
        )
        request_data_xml = request_data.to_xml(
            skip_empty=True, pretty_print=True, encoding="UTF-8", xml_declaration=True
        )

        resp = self.post(
            URLS.update_tag + f"/{tag_id}",
            content=request_data_xml,
            content_type="application/xml",
        )
        ret = tag_output.Wrapper.model_validate_json(resp.text)

        return ret.service_response

    def search_tags(
        self,
        id: int | None = None,
        name: str | None = None,
        parent: int | None = None,
        rule_type: tag_request.tag_rule_types | None = None,
        provider: tag_request.tag_provider_types | None = None,
        color: str | None = None,
    ) -> tag_output.ServiceResponse:
        request_data = tag_request.create_search_tags_request(
            id=id,
            name=name,
            parent=parent,
            rule_type=rule_type,
            provider=provider,
            color=color,
        )
        request_data_xml = request_data.to_xml(
            skip_empty=True, pretty_print=True, encoding="UTF-8", xml_declaration=True
        )

        resp = self.post(
            URLS.search_tags,
            content=request_data_xml,
            content_type="application/xml",
        )
        ret = tag_output.Wrapper.model_validate_json(resp.text)

        return ret.service_response

    def delete_tag(self, tag_id: int) -> tag_output.ServiceResponse:
        resp = self.post(URLS.delete_tag + f"/{tag_id}")
        ret = tag_output.Wrapper.model_validate_json(resp.text)

        return ret.service_response

    def get_asset_info(self, asset_id: int) -> asset_output.ServiceResponse:
        resp = self.get(URLS.get_asset_info + f"/{asset_id}", accept="application/json")
        ret = asset_output.Wrapper.model_validate_json(resp.text)

        return ret.service_response

    def update_asset(
        self,
        asset_id: int | None,
        criteria: list[AssetSearchCriteria] | None = None,
        name: str | None = None,
        add_tags: list[int] = [],
        remove_tags: list[int] = [],
        start_from_offset: int | None = None,
        start_from_id: int | None = None,
        limit_results: int | None = None,
    ) -> asset_output.ServiceResponse:
        if add_tags and remove_tags:
            raise ValueError(
                "Cannot add and remove tags at the same time. Please use separate calls."
            )
        request_data = asset_request.create_asset_request(
            criteria=criteria,
            name=name,
            add_tags=add_tags,
            remove_tags=remove_tags,
            start_from_offset=start_from_offset,
            start_from_id=start_from_id,
            limit_results=limit_results,
        )
        request_data_xml = request_data.to_xml(
            skip_empty=True, pretty_print=True, encoding="UTF-8", xml_declaration=True
        )

        resp = self.post(
            URLS.update_asset + f"/{asset_id}",
            content=request_data_xml,
            content_type="application/xml",
        )
        ret = asset_output.Wrapper.model_validate_json(resp.text)

        return ret.service_response

    def search_assets(
        self,
        criteria: list[AssetSearchCriteria],
        start_from_offset: int | None = None,
        start_from_id: int | None = None,
        limit_results: int | None = None,
    ) -> asset_output.ServiceResponse:
        request_data = asset_request.create_asset_request(
            criteria=criteria,
            start_from_offset=start_from_offset,
            start_from_id=start_from_id,
            limit_results=limit_results,
        )
        request_data_xml = request_data.to_xml(
            skip_empty=True, pretty_print=True, encoding="UTF-8", xml_declaration=True
        )

        resp = self.post(
            URLS.search_assets,
            content=request_data_xml,
            content_type="application/xml",
        )
        ret = asset_output.Wrapper.model_validate_json(resp.text)

        return ret.service_response
