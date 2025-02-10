import datetime

from pydantic_xml import BaseXmlModel, attr, element, wrapped


class ResponseWarning(BaseXmlModel):
    code: str = element(tag="CODE")
    text: str = element(tag="TEXT")
    url: str = element(tag="URL")


class ChangeLog(BaseXmlModel):
    changes_date: datetime.datetime = element(tag="CHANGES_DATE")
    comments: str = element(tag="COMMENTS")


class Discovery(BaseXmlModel):
    remote: bool = element(tag="REMOTE")
    auth_type_list: list[str] = wrapped(
        "AUTH_TYPE_LIST", element(tag="AUTH_TYPE", default_factory=list)
    )
    additional_info: str | None = element(tag="ADDITIONAL_INFO", default=None)


class ThreatIntel(BaseXmlModel):
    threat_intel_id: str = attr(name="id")
    value: str


class Attack(BaseXmlModel):
    vector: str | None = element(tag="VECTOR", default=None)
    complexity: str | None = element(tag="COMPLEXITY", default=None)


class Impact(BaseXmlModel):
    confidentiality: str | None = element(tag="CONFIDENTIALITY", default=None)
    integrity: str | None = element(tag="INTEGRITY", default=None)
    availability: str | None = element(tag="AVAILABILITY", default=None)


class Access(BaseXmlModel):
    vector: str | None = element(tag="VECTOR", default=None)
    complexity: str | None = element(tag="COMPLEXITY", default=None)


class Base(BaseXmlModel):
    source: str | None = attr(name="source", default=None)
    value: str


class CVSSv3(BaseXmlModel):
    base: Base | None = element(tag="BASE", default=None)
    temporal: float | None = element(tag="TEMPORAL", default=None)
    vector_string: str | None = element(tag="VECTOR_STRING", default=None)
    cvss3_version: str | None = element(tag="CVSS3_VERSION", default=None)
    attack: Attack | None = element(tag="ATTACK", default=None)
    impact: Impact | None = element(tag="IMPACT", default=None)
    privileges_required: str | None = element(tag="PRIVILEGES_REQUIRED", default=None)
    user_interaction: str | None = element(tag="USER_INTERACTION", default=None)
    scope: str | None = element(tag="SCOPE", default=None)
    exploit_code_maturity: str | None = element(
        tag="EXPLOIT_CODE_MATURITY", default=None
    )
    remediation_level: str | None = element(tag="REMEDIATION_LEVEL", default=None)
    report_confidence: str | None = element(tag="REPORT_CONFIDENCE", default=None)


class CVSS(BaseXmlModel):
    base: Base | None = element(tag="BASE", default=None)
    temporal: float | None = element(tag="TEMPORAL", default=None)
    vector_string: str | None = element(tag="VECTOR_STRING", default=None)
    cvss3_version: str | None = element(tag="CVSS3_VERSION", default=None)
    access: Access | None = element(tag="ACCESS", default=None)
    impact: Impact | None = element(tag="IMPACT", default=None)
    authentication: str | None = element(tag="AUTHENTICATION", default=None)
    exploitability: str | None = element(tag="EXPLOITABILITY", default=None)
    remediation_level: str | None = element(tag="REMEDIATION_LEVEL", default=None)
    report_confidence: str | None = element(tag="REPORT_CONFIDENCE", default=None)


class MWInfo(BaseXmlModel):
    mw_id: str = element(tag="MW_ID")
    mw_type: str | None = element(tag="MW_TYPE", default=None)
    mw_platform: str | None = element(tag="MW_PLATFORM", default=None)
    mw_alias: str | None = element(tag="MW_ALIAS", default=None)
    mw_rating: str | None = element(tag="MW_RATING", default=None)
    mw_link: str | None = element(tag="MW_LINK", default=None)


class MWSrc(BaseXmlModel):
    src_name: str = element(tag="SRC_NAME")
    mw_list: list[MWInfo] = wrapped(
        "MW_LIST", element(tag="MW_INFO", default_factory=list)
    )


class Explt(BaseXmlModel):
    ref: str = element(tag="REF")
    desc: str = element(tag="DESC")
    link: str | None = element(tag="LINK", default=None)


class ExpltSrc(BaseXmlModel):
    src_name: str | None = element(tag="SRC_NAME", default=None)
    explt_list: list[Explt] = wrapped(
        "EXPLT_LIST", element(tag="EXPLT", default_factory=list)
    )


class Correlation(BaseXmlModel):
    exploits: list[ExpltSrc] = wrapped(
        "EXPLOITS", element(tag="EXPLT_SRC", default_factory=list)
    )
    malware: list[MWSrc] = wrapped(
        "MALWARE", element(tag="MW_SRC", default_factory=list)
    )


class Compliance(BaseXmlModel):
    type: str = element(tag="TYPE")
    section: str = element(tag="SECTION")
    description: str = element(tag="DESCRIPTION")


class CVE(BaseXmlModel):
    id: str = element(tag="ID")
    url: str = element(tag="URL")


class VendorReference(BaseXmlModel):
    id: str = element(tag="ID")
    url: str = element(tag="URL")


class Software(BaseXmlModel):
    product: str = element(tag="PRODUCT")
    vendor: str = element(tag="VENDOR")


class Bugtraq(BaseXmlModel):
    bugtraq_id: str = element(tag="ID")
    url: str = element(tag="URL")


class LastCustomization(BaseXmlModel):
    last_customization_datetime: datetime.datetime | None = element(
        tag="DATETIME", defaul=None
    )
    user_login: str = element(tag="USER_LOGIN")


class Vuln(BaseXmlModel):
    qid: int = element(tag="QID")
    vuln_type: str = element(tag="VULN_TYPE")
    severity_level: int = element(tag="SEVERITY_LEVEL")
    title: str = element(tag="TITLE")
    category: str | None = element(tag="CATEGORY", default=None)
    detection_info: str | None = element(tag="DETECTION_INFO", default=None)
    last_customization: LastCustomization | None = element(
        tag="LAST_CUSTOMIZATION", default=None
    )
    last_service_modification_datetime: datetime.datetime | None = element(
        tag="LAST_SERVICE_MODIFICATION_DATETIME", default=None
    )
    published_datetime: datetime.datetime | None = element(
        tag="PUBLISHED_DATETIME", default=None
    )
    code_modified_datetime: datetime.datetime | None = element(
        tag="CODE_MODIFIED_DATETIME", default=None
    )
    bugtraq_list: list[Bugtraq] | None = wrapped(
        "BUGTRAQ_LIST", element(tag="BUGTRAQ", default_factory=list)
    )
    patchable: bool | None = element(tag="PATCHABLE", default=None)
    patch_published_date: datetime.datetime | None = element(
        tag="PATCH_PUBLISHED_DATE", default=None
    )
    software_list: list[Software] = wrapped(
        "SOFTWARE_LIST", element(tag="SOFTWARE", default_factory=list)
    )
    vendor_reference_list: list[VendorReference] = wrapped(
        "VENDOR_REFERENCE_LIST", element(tag="VENDOR_REFERENCE", default_factory=list)
    )
    cve_list: list[CVE] = wrapped("CVE_LIST", element(tag="CVE", default_factory=list))
    diagnosis: str | None = element(tag="DIAGNOSIS", default=None)
    diagnosis_comment: str | None = element(tag="DIAGNOSIS_COMMENT", default=None)
    consequence: str | None = element(tag="CONSEQUENCE", default=None)
    consequence_comment: str | None = element(tag="CONSEQUENCE_COMMENT", default=None)
    solution: str | None = element(tag="SOLUTION", default=None)
    solution_comment: str | None = element(tag="SOLUTION_COMMENT", default=None)
    compliance_list: list[Compliance] = wrapped(
        "COMPLIANCE_LIST", element(tag="COMPLIANCE", default_factory=list)
    )
    correlation: Correlation | None = element(tag="CORRELATION", default=None)
    cvss: CVSS | None = element(tag="CVSS", default=None)
    cvss_v3: CVSSv3 | None = element(tag="CVSS_V3", default=None)
    pci_flag: bool | None = element(tag="PCI_FLAG", default=None)
    automatic_pci_fail: bool | None = element(tag="AUTOMATIC_PCI_FAIL", default=None)
    pci_reasons: list[str] = wrapped(
        "PCI_REASONS", element(tag="PCI_REASON", default_factory=list)
    )
    threat_intelligence: list[ThreatIntel] = wrapped(
        "THREAT_INTELLIGENCE", element(tag="THREAT_INTEL", default_factory=list)
    )
    supported_modules: str | None = element(tag="SUPPORTED_MODULES", default=None)
    discovery: Discovery | None = element(tag="DISCOVERY", default=None)
    is_disabled: bool | None = element(tag="IS_DISABLED", default=None)
    change_log_list: list[ChangeLog] = wrapped(
        "CHANGE_LOG_LIST", element(tag="CHANGE_LOG", default_factory=list)
    )


class Response(BaseXmlModel):
    response_datetime: datetime.datetime = element(tag="DATETIME")
    vuln_list: list[Vuln] = wrapped(
        "VULN_LIST", element(tag="VULN", default_factory=list)
    )
    id_set: list[int] = wrapped("ID_SET", element(tag="ID", default_factory=list))
    warning: ResponseWarning | None = element(tag="WARNING", default=None)


class Param(BaseXmlModel):
    key: str = element(tag="KEY")
    value: str = element(tag="VALUE")


class Request(BaseXmlModel):
    request_datetime: datetime.datetime = element(tag="DATETIME")
    user_login: str = element(tag="USER_LOGIN")
    resource: str = element(tag="RESOURCE")
    param_list: list[Param] = element(tag="PARAM_LIST", default_factory=list)
    post_data: str | None = element(tag="POST_DATA")


class KnowledgeBaseOutput(BaseXmlModel, tag="KNOWLEDGE_BASE_VULN_LIST_OUTPUT"):
    request: Request | None = element(tag="REQUEST", default=None)
    response: Response = element(tag="RESPONSE")
