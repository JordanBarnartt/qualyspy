from dataclasses import field
from pydantic.dataclasses import dataclass
from typing import List, Optional

import datetime as dt

DT_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


@dataclass
class Access:
    class Meta:
        name = "ACCESS"

    vector: Optional[str] = field(
        default=None,
        metadata={
            "name": "VECTOR",
            "type": "Element",
        },
    )
    complexity: Optional[str] = field(
        default=None,
        metadata={
            "name": "COMPLEXITY",
            "type": "Element",
        },
    )


@dataclass
class Attack:
    class Meta:
        name = "ATTACK"

    vector: Optional[str] = field(
        default=None,
        metadata={
            "name": "VECTOR",
            "type": "Element",
        },
    )
    complexity: Optional[str] = field(
        default=None,
        metadata={
            "name": "COMPLEXITY",
            "type": "Element",
        },
    )


@dataclass
class AuthTypeList:
    class Meta:
        name = "AUTH_TYPE_LIST"

    auth_type: List[str] = field(
        default_factory=list,
        metadata={
            "name": "AUTH_TYPE",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class Base:
    class Meta:
        name = "BASE"

    source: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )


@dataclass
class Bugtraq:
    class Meta:
        name = "BUGTRAQ"

    id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ID",
            "type": "Element",
            "required": True,
        },
    )
    url: Optional[str] = field(
        default=None,
        metadata={
            "name": "URL",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class ChangeLogInfo:
    class Meta:
        name = "CHANGE_LOG_INFO"

    change_date: Optional[dt.datetime] = field(
        default=None,
        metadata={
            "name": "CHANGE_DATE",
            "type": "Element",
            "required": True,
            "format": DT_FORMAT,
        },
    )
    comments: Optional[str] = field(
        default=None,
        metadata={
            "name": "COMMENTS",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Compliance:
    class Meta:
        name = "COMPLIANCE"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "TYPE",
            "type": "Element",
            "required": True,
        },
    )
    section: Optional[str] = field(
        default=None,
        metadata={
            "name": "SECTION",
            "type": "Element",
            "required": True,
        },
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "name": "DESCRIPTION",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Cve:
    class Meta:
        name = "CVE"

    id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ID",
            "type": "Element",
            "required": True,
        },
    )
    url: Optional[str] = field(
        default=None,
        metadata={
            "name": "URL",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Explt:
    class Meta:
        name = "EXPLT"

    ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "REF",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
            "required": True,
        },
    )
    link: Optional[str] = field(
        default=None,
        metadata={
            "name": "LINK",
            "type": "Element",
        },
    )


@dataclass
class IdSet:
    class Meta:
        name = "ID_SET"

    id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
        },
    )
    id_range: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ID_RANGE",
            "type": "Element",
        },
    )


@dataclass
class Impact:
    class Meta:
        name = "IMPACT"

    confidentiality: Optional[str] = field(
        default=None,
        metadata={
            "name": "CONFIDENTIALITY",
            "type": "Element",
        },
    )
    integrity: Optional[str] = field(
        default=None,
        metadata={
            "name": "INTEGRITY",
            "type": "Element",
        },
    )
    availability: Optional[str] = field(
        default=None,
        metadata={
            "name": "AVAILABILITY",
            "type": "Element",
        },
    )


@dataclass
class LastCustomization:
    class Meta:
        name = "LAST_CUSTOMIZATION"

    datetime: Optional[dt.datetime] = field(
        default=None,
        metadata={
            "name": "DATETIME",
            "type": "Element",
            "required": True,
            "format": DT_FORMAT,
        },
    )
    user_login: Optional[str] = field(
        default=None,
        metadata={
            "name": "USER_LOGIN",
            "type": "Element",
        },
    )


@dataclass
class MwInfo:
    class Meta:
        name = "MW_INFO"

    mw_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "MW_ID",
            "type": "Element",
            "required": True,
        },
    )
    mw_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "MW_TYPE",
            "type": "Element",
        },
    )
    mw_platform: Optional[str] = field(
        default=None,
        metadata={
            "name": "MW_PLATFORM",
            "type": "Element",
        },
    )
    mw_alias: Optional[str] = field(
        default=None,
        metadata={
            "name": "MW_ALIAS",
            "type": "Element",
        },
    )
    mw_rating: Optional[str] = field(
        default=None,
        metadata={
            "name": "MW_RATING",
            "type": "Element",
        },
    )
    mw_link: Optional[str] = field(
        default=None,
        metadata={
            "name": "MW_LINK",
            "type": "Element",
        },
    )


@dataclass
class Param:
    class Meta:
        name = "PARAM"

    key: Optional[str] = field(
        default=None,
        metadata={
            "name": "KEY",
            "type": "Element",
            "required": True,
        },
    )
    value: Optional[str] = field(
        default=None,
        metadata={
            "name": "VALUE",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class PciReasons:
    class Meta:
        name = "PCI_REASONS"

    pci_reason: List[str] = field(
        default_factory=list,
        metadata={
            "name": "PCI_REASON",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class Software:
    class Meta:
        name = "SOFTWARE"

    product: Optional[str] = field(
        default=None,
        metadata={
            "name": "PRODUCT",
            "type": "Element",
            "required": True,
        },
    )
    vendor: Optional[str] = field(
        default=None,
        metadata={
            "name": "VENDOR",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class ThreatIntel:
    class Meta:
        name = "THREAT_INTEL"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )


@dataclass
class VendorReference:
    class Meta:
        name = "VENDOR_REFERENCE"

    id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ID",
            "type": "Element",
            "required": True,
        },
    )
    url: Optional[str] = field(
        default=None,
        metadata={
            "name": "URL",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Warning:
    class Meta:
        name = "WARNING"

    code: Optional[str] = field(
        default=None,
        metadata={
            "name": "CODE",
            "type": "Element",
        },
    )
    text: Optional[str] = field(
        default=None,
        metadata={
            "name": "TEXT",
            "type": "Element",
            "required": True,
        },
    )
    url: Optional[str] = field(
        default=None,
        metadata={
            "name": "URL",
            "type": "Element",
        },
    )


@dataclass
class BugtraqList:
    class Meta:
        name = "BUGTRAQ_LIST"

    bugtraq: List[Bugtraq] = field(
        default_factory=list,
        metadata={
            "name": "BUGTRAQ",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class ChangeLogList:
    class Meta:
        name = "CHANGE_LOG_LIST"

    change_log_info: List[ChangeLogInfo] = field(
        default_factory=list,
        metadata={
            "name": "CHANGE_LOG_INFO",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class ComplianceList:
    class Meta:
        name = "COMPLIANCE_LIST"

    compliance: List[Compliance] = field(
        default_factory=list,
        metadata={
            "name": "COMPLIANCE",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class CveList:
    class Meta:
        name = "CVE_LIST"

    cve: List[Cve] = field(
        default_factory=list,
        metadata={
            "name": "CVE",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class Cvss:
    class Meta:
        name = "CVSS"

    base: Optional[Base] = field(
        default=None,
        metadata={
            "name": "BASE",
            "type": "Element",
        },
    )
    temporal: Optional[str] = field(
        default=None,
        metadata={
            "name": "TEMPORAL",
            "type": "Element",
        },
    )
    vector_string: Optional[str] = field(
        default=None,
        metadata={
            "name": "VECTOR_STRING",
            "type": "Element",
        },
    )
    access: Optional[Access] = field(
        default=None,
        metadata={
            "name": "ACCESS",
            "type": "Element",
        },
    )
    impact: Optional[Impact] = field(
        default=None,
        metadata={
            "name": "IMPACT",
            "type": "Element",
        },
    )
    authentication: Optional[str] = field(
        default=None,
        metadata={
            "name": "AUTHENTICATION",
            "type": "Element",
        },
    )
    exploitability: Optional[str] = field(
        default=None,
        metadata={
            "name": "EXPLOITABILITY",
            "type": "Element",
        },
    )
    remediation_level: Optional[str] = field(
        default=None,
        metadata={
            "name": "REMEDIATION_LEVEL",
            "type": "Element",
        },
    )
    report_confidence: Optional[str] = field(
        default=None,
        metadata={
            "name": "REPORT_CONFIDENCE",
            "type": "Element",
        },
    )


@dataclass
class CvssV3:
    class Meta:
        name = "CVSS_V3"

    base: Optional[Base] = field(
        default=None,
        metadata={
            "name": "BASE",
            "type": "Element",
        },
    )
    temporal: Optional[str] = field(
        default=None,
        metadata={
            "name": "TEMPORAL",
            "type": "Element",
        },
    )
    vector_string: Optional[str] = field(
        default=None,
        metadata={
            "name": "VECTOR_STRING",
            "type": "Element",
        },
    )
    cvss3_version: Optional[str] = field(
        default=None,
        metadata={
            "name": "CVSS3_VERSION",
            "type": "Element",
        },
    )
    attack: Optional[Attack] = field(
        default=None,
        metadata={
            "name": "ATTACK",
            "type": "Element",
        },
    )
    impact: Optional[Impact] = field(
        default=None,
        metadata={
            "name": "IMPACT",
            "type": "Element",
        },
    )
    privileges_required: Optional[str] = field(
        default=None,
        metadata={
            "name": "PRIVILEGES_REQUIRED",
            "type": "Element",
        },
    )
    user_interaction: Optional[str] = field(
        default=None,
        metadata={
            "name": "USER_INTERACTION",
            "type": "Element",
        },
    )
    scope: Optional[str] = field(
        default=None,
        metadata={
            "name": "SCOPE",
            "type": "Element",
        },
    )
    exploit_code_maturity: Optional[str] = field(
        default=None,
        metadata={
            "name": "EXPLOIT_CODE_MATURITY",
            "type": "Element",
        },
    )
    remediation_level: Optional[str] = field(
        default=None,
        metadata={
            "name": "REMEDIATION_LEVEL",
            "type": "Element",
        },
    )
    report_confidence: Optional[str] = field(
        default=None,
        metadata={
            "name": "REPORT_CONFIDENCE",
            "type": "Element",
        },
    )


@dataclass
class Discovery:
    class Meta:
        name = "DISCOVERY"

    remote: Optional[str] = field(
        default=None,
        metadata={
            "name": "REMOTE",
            "type": "Element",
            "required": True,
        },
    )
    auth_type_list: Optional[AuthTypeList] = field(
        default=None,
        metadata={
            "name": "AUTH_TYPE_LIST",
            "type": "Element",
        },
    )
    additional_info: Optional[str] = field(
        default=None,
        metadata={
            "name": "ADDITIONAL_INFO",
            "type": "Element",
        },
    )


@dataclass
class ExpltList:
    class Meta:
        name = "EXPLT_LIST"

    explt: List[Explt] = field(
        default_factory=list,
        metadata={
            "name": "EXPLT",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class MwList:
    class Meta:
        name = "MW_LIST"

    mw_info: List[MwInfo] = field(
        default_factory=list,
        metadata={
            "name": "MW_INFO",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class ParamList:
    class Meta:
        name = "PARAM_LIST"

    param: List[Param] = field(
        default_factory=list,
        metadata={
            "name": "PARAM",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class SoftwareList:
    class Meta:
        name = "SOFTWARE_LIST"

    software: List[Software] = field(
        default_factory=list,
        metadata={
            "name": "SOFTWARE",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class ThreatIntelligence:
    class Meta:
        name = "THREAT_INTELLIGENCE"

    threat_intel: List[ThreatIntel] = field(
        default_factory=list,
        metadata={
            "name": "THREAT_INTEL",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class VendorReferenceList:
    class Meta:
        name = "VENDOR_REFERENCE_LIST"

    vendor_reference: List[VendorReference] = field(
        default_factory=list,
        metadata={
            "name": "VENDOR_REFERENCE",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class ExpltSrc:
    class Meta:
        name = "EXPLT_SRC"

    src_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "SRC_NAME",
            "type": "Element",
            "required": True,
        },
    )
    explt_list: Optional[ExpltList] = field(
        default=None,
        metadata={
            "name": "EXPLT_LIST",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class MwSrc:
    class Meta:
        name = "MW_SRC"

    src_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "SRC_NAME",
            "type": "Element",
            "required": True,
        },
    )
    mw_list: Optional[MwList] = field(
        default=None,
        metadata={
            "name": "MW_LIST",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Request:
    class Meta:
        name = "REQUEST"

    datetime: Optional[dt.datetime] = field(
        default=None,
        metadata={
            "name": "DATETIME",
            "type": "Element",
            "required": True,
            "format": DT_FORMAT,
        },
    )
    user_login: Optional[str] = field(
        default=None,
        metadata={
            "name": "USER_LOGIN",
            "type": "Element",
            "required": True,
        },
    )
    resource: Optional[str] = field(
        default=None,
        metadata={
            "name": "RESOURCE",
            "type": "Element",
            "required": True,
        },
    )
    param_list: Optional[ParamList] = field(
        default=None,
        metadata={
            "name": "PARAM_LIST",
            "type": "Element",
        },
    )
    post_data: Optional[str] = field(
        default=None,
        metadata={
            "name": "POST_DATA",
            "type": "Element",
        },
    )


@dataclass
class Exploits:
    class Meta:
        name = "EXPLOITS"

    explt_src: List[ExpltSrc] = field(
        default_factory=list,
        metadata={
            "name": "EXPLT_SRC",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class Malware:
    class Meta:
        name = "MALWARE"

    mw_src: List[MwSrc] = field(
        default_factory=list,
        metadata={
            "name": "MW_SRC",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class Correlation:
    class Meta:
        name = "CORRELATION"

    exploits: Optional[Exploits] = field(
        default=None,
        metadata={
            "name": "EXPLOITS",
            "type": "Element",
        },
    )
    malware: Optional[Malware] = field(
        default=None,
        metadata={
            "name": "MALWARE",
            "type": "Element",
        },
    )


@dataclass
class Vuln:
    class Meta:
        name = "VULN"

    qid: Optional[int] = field(
        default=None,
        metadata={
            "name": "QID",
            "type": "Element",
            "required": True,
        },
    )
    vuln_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "VULN_TYPE",
            "type": "Element",
            "required": True,
        },
    )
    severity_level: Optional[int] = field(
        default=None,
        metadata={
            "name": "SEVERITY_LEVEL",
            "type": "Element",
            "required": True,
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "name": "TITLE",
            "type": "Element",
            "required": True,
        },
    )
    category: Optional[str] = field(
        default=None,
        metadata={
            "name": "CATEGORY",
            "type": "Element",
        },
    )
    detection_info: Optional[str] = field(
        default=None,
        metadata={
            "name": "DETECTION_INFO",
            "type": "Element",
        },
    )
    last_customization: Optional[LastCustomization] = field(
        default=None,
        metadata={
            "name": "LAST_CUSTOMIZATION",
            "type": "Element",
        },
    )
    last_service_modification_datetime: Optional[dt.datetime] = field(
        default=None,
        metadata={
            "name": "LAST_SERVICE_MODIFICATION_DATETIME",
            "type": "Element",
            "format": DT_FORMAT,
        },
    )
    published_datetime: Optional[dt.datetime] = field(
        default=None,
        metadata={
            "name": "PUBLISHED_DATETIME",
            "type": "Element",
            "required": True,
            "format": DT_FORMAT,
        },
    )
    bugtraq_list: Optional[BugtraqList] = field(
        default=None,
        metadata={
            "name": "BUGTRAQ_LIST",
            "type": "Element",
        },
    )
    patchable: Optional[str] = field(
        default=None,
        metadata={
            "name": "PATCHABLE",
            "type": "Element",
            "required": True,
        },
    )
    software_list: Optional[SoftwareList] = field(
        default=None,
        metadata={
            "name": "SOFTWARE_LIST",
            "type": "Element",
        },
    )
    vendor_reference_list: Optional[VendorReferenceList] = field(
        default=None,
        metadata={
            "name": "VENDOR_REFERENCE_LIST",
            "type": "Element",
        },
    )
    cve_list: Optional[CveList] = field(
        default=None,
        metadata={
            "name": "CVE_LIST",
            "type": "Element",
        },
    )
    diagnosis: Optional[str] = field(
        default=None,
        metadata={
            "name": "DIAGNOSIS",
            "type": "Element",
        },
    )
    diagnosis_comment: Optional[str] = field(
        default=None,
        metadata={
            "name": "DIAGNOSIS_COMMENT",
            "type": "Element",
        },
    )
    consequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "CONSEQUENCE",
            "type": "Element",
        },
    )
    consequence_comment: Optional[str] = field(
        default=None,
        metadata={
            "name": "CONSEQUENCE_COMMENT",
            "type": "Element",
        },
    )
    solution: Optional[str] = field(
        default=None,
        metadata={
            "name": "SOLUTION",
            "type": "Element",
        },
    )
    solution_comment: Optional[str] = field(
        default=None,
        metadata={
            "name": "SOLUTION_COMMENT",
            "type": "Element",
        },
    )
    compliance_list: Optional[ComplianceList] = field(
        default=None,
        metadata={
            "name": "COMPLIANCE_LIST",
            "type": "Element",
        },
    )
    correlation: Optional[Correlation] = field(
        default=None,
        metadata={
            "name": "CORRELATION",
            "type": "Element",
        },
    )
    cvss: Optional[Cvss] = field(
        default=None,
        metadata={
            "name": "CVSS",
            "type": "Element",
        },
    )
    cvss_v3: Optional[CvssV3] = field(
        default=None,
        metadata={
            "name": "CVSS_V3",
            "type": "Element",
        },
    )
    pci_flag: Optional[str] = field(
        default=None,
        metadata={
            "name": "PCI_FLAG",
            "type": "Element",
        },
    )
    automatic_pci_fail: Optional[str] = field(
        default=None,
        metadata={
            "name": "AUTOMATIC_PCI_FAIL",
            "type": "Element",
        },
    )
    pci_reasons: Optional[PciReasons] = field(
        default=None,
        metadata={
            "name": "PCI_REASONS",
            "type": "Element",
        },
    )
    threat_intelligence: Optional[ThreatIntelligence] = field(
        default=None,
        metadata={
            "name": "THREAT_INTELLIGENCE",
            "type": "Element",
        },
    )
    supported_modules: Optional[str] = field(
        default=None,
        metadata={
            "name": "SUPPORTED_MODULES",
            "type": "Element",
        },
    )
    discovery: Optional[Discovery] = field(
        default=None,
        metadata={
            "name": "DISCOVERY",
            "type": "Element",
            "required": True,
        },
    )
    is_disabled: Optional[str] = field(
        default=None,
        metadata={
            "name": "IS_DISABLED",
            "type": "Element",
        },
    )
    change_log_list: Optional[ChangeLogList] = field(
        default=None,
        metadata={
            "name": "CHANGE_LOG_LIST",
            "type": "Element",
        },
    )


@dataclass
class VulnList:
    class Meta:
        name = "VULN_LIST"

    vuln: List[Vuln] = field(
        default_factory=list,
        metadata={
            "name": "VULN",
            "type": "Element",
        },
    )


@dataclass
class Response:
    class Meta:
        name = "RESPONSE"

    datetime: Optional[str] = field(
        default=None,
        metadata={
            "name": "DATETIME",
            "type": "Element",
            "required": True,
        },
    )
    vuln_list: Optional[VulnList] = field(
        default=None,
        metadata={
            "name": "VULN_LIST",
            "type": "Element",
        },
    )
    id_set: Optional[IdSet] = field(
        default=None,
        metadata={
            "name": "ID_SET",
            "type": "Element",
        },
    )
    warning: Optional[Warning] = field(
        default=None,
        metadata={
            "name": "WARNING",
            "type": "Element",
        },
    )


@dataclass
class KnowledgeBaseVulnListOutput:
    class Meta:
        name = "KNOWLEDGE_BASE_VULN_LIST_OUTPUT"

    request: Optional[Request] = field(
        default=None,
        metadata={
            "name": "REQUEST",
            "type": "Element",
        },
    )
    response: Optional[Response] = field(
        default=None,
        metadata={
            "name": "RESPONSE",
            "type": "Element",
            "required": True,
        },
    )
