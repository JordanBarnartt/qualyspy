from pydantic_xml import BaseXmlModel, attr, element


class TagSimple(BaseXmlModel, tag="TagSimple"):
    id: int | None = element(tag="id", default=None)


class CollectionType(BaseXmlModel):
    tag_simple: list[TagSimple] | None = element(tag="TagSimple", default=None)


class Collection(BaseXmlModel):
    set: CollectionType | None = element(tag="set", default=None)
    add: CollectionType | None = element(tag="add", default=None)
    remove: CollectionType | None = element(tag="remove", default=None)
    update: CollectionType | None = element(tag="update", default=None)


class Asset(BaseXmlModel):
    name: str | None = element(tag="name", default=None)
    tags: Collection | None = element(tag="tags", default=None)


class Data(BaseXmlModel):
    asset: Asset = element(tag="Asset")


class Criteria(BaseXmlModel):
    field: str = attr(name="field")
    operator: str = attr(name="operator")
    value: str


class Filters(BaseXmlModel):
    criteria: list[Criteria] | None = element(tag="Criteria")


class Preferences(BaseXmlModel):
    start_from_offset: int | None = element(tag="startFromOffset", default=None)
    start_from_id: int | None = element(tag="startFromId", default=None)
    limit_results: int | None = element(tag="limitResults", default=None)


class ServiceRequest(BaseXmlModel, tag="ServiceRequest"):
    data: Data | None = element(tag="data", default=None)
    filters: Filters | None = element(tag="filters", default=None)
    preferences: Preferences | None = element(tag="preferences", default=None)


def create_asset_request(
    criteria: list[Criteria] | None,
    name: str | None = None,
    add_tags: list[int] = [],
    remove_tags: list[int] = [],
    start_from_offset: int | None = None,
    start_from_id: int | None = None,
    limit_results: int | None = None,
) -> ServiceRequest:
    if add_tags or remove_tags:
        tags = Collection(
            add=CollectionType(tag_simple=[TagSimple(id=tag) for tag in add_tags]),
            remove=CollectionType(
                tag_simple=[TagSimple(id=tag) for tag in remove_tags]
            ),
        )
    else:
        tags = None
    return ServiceRequest(
        data=Data(
            asset=Asset(
                name=name,
                tags=tags,
            )
        ),
        filters=Filters(criteria=criteria),
        preferences=Preferences(
            start_from_offset=start_from_offset,
            start_from_id=start_from_id,
            limit_results=limit_results,
        ),
    )
