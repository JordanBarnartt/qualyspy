import datetime as dt
from dataclasses import field
from enum import Enum
from typing import List, Optional

from pydantic.dataclasses import dataclass

__NAMESPACE__ = "http://am.oxm.api.portal.qualys.com/v2"


class TagRuleType(Enum):
    STATIC = "STATIC"
    GROOVY = "GROOVY"
    OS_REGEX = "OS_REGEX"
    NETWORK_RANGE = "NETWORK_RANGE"
    NETWORK_RANGE_ENHANCED = "NETWORK_RANGE_ENHANCED"
    NAME_CONTAINS = "NAME_CONTAINS"
    INSTALLED_SOFTWARE = "INSTALLED_SOFTWARE"
    OPEN_PORTS = "OPEN_PORTS"
    VULN_EXIST = "VULN_EXIST"
    ASSET_SEARCH = "ASSET_SEARCH"
    CLOUD_ASSET = "CLOUD_ASSET"
    BUSINESS_INFORMATION = "BUSINESS_INFORMATION"
    GLOBAL_ASSET_VIEW = "GLOBAL_ASSET_VIEW"
    TAG_SET = "TAG_SET"


@dataclass
class TagSimple:
    id: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v2",
            "required": True,
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v2",
            "required": True,
        },
    )


@dataclass
class TagSimpleList:
    tag_simple: List[TagSimple] = field(
        default_factory=list,
        metadata={
            "name": "TagSimple",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v2",
        },
    )


@dataclass
class TagSimpleObj:
    tag_simple: Optional[TagSimple] = field(
        default=None,
        metadata={
            "name": "TagSimple",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v2",
        },
    )


@dataclass
class TagSimpleQlist:
    class Meta:
        name = "TagSimpleQList"

    count: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v2",
        },
    )
    list_value: List[TagSimpleObj] = field(
        default_factory=list,
        metadata={
            "name": "list",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v2",
        },
    )
    set: Optional[TagSimpleList] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v2",
        },
    )
    add: Optional[TagSimpleList] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v2",
        },
    )
    remove: Optional[TagSimpleList] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v2",
        },
    )
    update: Optional[TagSimpleList] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v2",
        },
    )


@dataclass
class Tag(TagSimple):
    parent_tag_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "parentTagId",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v2",
        },
    )
    created: Optional[dt.datetime] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v2",
            "format": "%Y-%m-%dT%H:%M:%SZ",
        },
    )
    modified: Optional[dt.datetime] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v2",
            "format": "%Y-%m-%dT%H:%M:%SZ",
        },
    )
    color: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v2",
            "pattern": r"#[0-9a-fA-F]{3}([0-9a-fA-F]{3})?",
        },
    )
    rule_text: Optional[str] = field(
        default=None,
        metadata={
            "name": "ruleText",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v2",
        },
    )
    rule_type: Optional[TagRuleType] = field(
        default=None,
        metadata={
            "name": "ruleType",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v2",
        },
    )
    src_asset_group_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "srcAssetGroupId",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v2",
        },
    )
    src_business_unit_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "srcBusinessUnitId",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v2",
        },
    )
    src_operating_system_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "srcOperatingSystemName",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v2",
        },
    )
    provider: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v2",
        },
    )
    children: Optional[TagSimpleQlist] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v2",
        },
    )
    criticality_score: Optional[int] = field(
        default=None,
        metadata={
            "name": "criticalityScore",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v2",
        },
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v2",
        },
    )
