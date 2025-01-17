from pydantic_xml import BaseXmlModel, element, attr

from typing import Literal

tag_rule_types = Literal[
    "STATIC",
    "GROOVY",
    "OS_REGEX",
    "NETWORK_RANGE",
    "NETWORK_RANGE_ENHANCED" "NAME_CONTAINS",
    "INSTALLED_SOFTWARE",
    "OPEN_PORTS",
    "VULN_EXISTS",
    "ASSET_SEARCH",
    "CLOUD_ASSET",
    "BUSINESS_INFORMATION",
    "GLOBAL_ASSET_VIEW",
    "TAG_SET",
]

tag_provider_types = Literal["EC2", "AZURE", "GCP", "IBM", "OCI", "Alibaba"]


class TagSimple(BaseXmlModel, tag="TagSimple"):
    id: int | None = element(tag="id", default=None)
    name: str | None = element(tag="name", default=None)


class CollectionType(BaseXmlModel):
    tag_simple: list[TagSimple] | None = element(tag="TagSimple", default=None)


class Collection(BaseXmlModel):
    set: CollectionType | None = element(tag="set", default=None)
    add: CollectionType | None = element(tag="add", default=None)
    remove: CollectionType | None = element(tag="remove", default=None)
    update: CollectionType | None = element(tag="update", default=None)


class Tag(BaseXmlModel):
    name: str | None = element(tag="name", default=None)
    rule_type: tag_rule_types | None = element(tag="ruleType", default=None)
    rule_text: str | None = element(tag="ruleText", default=None)
    criticality_score: int | None = element(tag="criticalityScore", default=None)
    color: str | None = element(tag="color", default=None)
    children: Collection | None = element(tag="children", default=None)


class Data(BaseXmlModel):
    tag: Tag = element(tag="Tag")


class Criteria(BaseXmlModel):
    field: str = attr(name="field")
    operator: str = attr(name="operator")
    value: str


class Filters(BaseXmlModel):
    criteria: list[Criteria] = element(tag="Criteria")


class ServiceRequest(BaseXmlModel, tag="ServiceRequest"):
    data: Data | None = element(tag="data", default=None)
    filters: Filters | None = element(tag="filters", default=None)


def create_add_tag_request(
    name: str,
    rule_type: tag_rule_types | None = None,
    rule_text: str | None = None,
    criticality_score: int | None = None,
    color: str | None = None,
    children: list[str] = [],
) -> ServiceRequest:
    if children:
        children_to_add = Collection(
            set=CollectionType(tag_simple=[TagSimple(name=child) for child in children])
        )
    else:
        children_to_add = None
    return ServiceRequest(
        data=Data(
            tag=Tag(
                name=name,
                rule_type=rule_type,
                rule_text=rule_text,
                criticality_score=criticality_score,
                color=color,
                children=children_to_add,
            )
        )
    )


def create_update_tag_request(
    name: str | None = None,
    rule_type: tag_rule_types | None = None,
    rule_text: str | None = None,
    criticality_score: int | None = None,
    color: str | None = None,
    add_children: list[str] = [],
    remove_children: list[int] = [],
) -> ServiceRequest:
    if add_children or remove_children:
        children = Collection(
            set=CollectionType(
                tag_simple=[TagSimple(name=child) for child in add_children]
            ),
            remove=CollectionType(
                tag_simple=[TagSimple(id=child) for child in remove_children]
            ),
        )
    else:
        children = None

    return ServiceRequest(
        data=Data(
            tag=Tag(
                name=name,
                rule_type=rule_type,
                rule_text=rule_text,
                criticality_score=criticality_score,
                color=color,
                children=children,
            )
        )
    )


def create_search_tags_request(
    id: int | None,
    name: str | None,
    parent: int | None,
    rule_type: tag_rule_types | None,
    provider: tag_provider_types | None,
    color: str | None,
) -> ServiceRequest:
    criteria_list = []
    for field, value in {
        "id": id,
        "name": name,
        "parent": parent,
        "ruleType": rule_type,
        "provider": provider,
        "color": color,
    }.items():
        if value:
            criteria_list.append(Criteria(field=field, operator="EQUALS", value=str(value)))
    return ServiceRequest(filters=Filters(criteria=criteria_list))
