"""Python wrapper for the Qualys KnowledgeBase API."""

import dataclasses
import datetime
from collections.abc import MutableSequence
from typing import Optional, Union

import qualyspy.qualysapi as qualysapi
import qualyspy.qutils as qutils


@dataclasses.dataclass
class Warning:
    """A warning which appears when the API request reaches the truncation limit."""

    text: str
    """The warning message text."""

    code: Optional[str] = None
    """The warning code."""

    url: Optional[str] = None
    """The URL for making another request for the next batch of host records."""


@dataclasses.dataclass
class Change_Log_Info:
    """A change to a vulnerability listing."""

    change_date: str
    """The date of a QID change."""

    comments: str
    """Comments provided at the time of the QID change."""


@dataclasses.dataclass
class Discovery:
    """A discovery method for a vulnerability."""

    remote: bool
    """A flag indicating whether the discovery method is remotely detectable. The value False
    indicates the vulnerability cannot be detected remotely (authentication is required). The value
    True indicates the vulnerability can be detected in two ways: 1) remotely without using
    authentication, and 2) using authentication.
    """

    auth_type_list: Optional[MutableSequence[str]] = None
    """Authentication types used to detect the vulnerability using trusted scanning."""

    additional_info: Optional[str] = None
    """Additional information related to the discovery of the vulnerability."""


@dataclasses.dataclass
class Attack:
    """CVSS attack metrics."""

    vector: Optional[str] = None
    """CVSS attack vector metrics."""

    complexity: Optional[str] = None
    """CVSS attack complexity metrics."""


@dataclasses.dataclass
class Impact:
    """CVSS impact metrics."""

    confidentiality: Optional[str] = None
    """CVSS confidentiality impact metric. S"""

    integrity: Optional[str] = None
    """CVSS integrity impact metric."""

    availability: Optional[str] = None
    """CVSS availability impact metric. """


@dataclasses.dataclass
class Cvss_V3:
    """CVSS information for a vulnerability."""

    base: Optional[str] = None
    """CVSS base score assigned to the vulnerability."""

    temporal: Optional[str] = None
    """CVSS temporal score."""

    vector_string: Optional[str] = None
    """CVSS scores of individual metrics."""

    cvss3_version: Optional[str] = None
    """The CVSS3 version currently supported."""

    attack: Optional[Attack] = None
    """CVSS attack metrics."""

    impact: Optional[Impact] = None
    """CVSS impact metrics."""

    privileges_required: Optional[str] = None
    """CVSS privileges required metrics."""

    user_interaction: Optional[str] = None
    """CVSS user interaction metrics."""

    scope: Optional[str] = None
    """CVSS scope metrics."""

    exploit_code_maturity: Optional[str] = None
    """CVSS exploit code maturity temporal metrics."""

    remediation_level: Optional[str] = None
    """CVSS remediation level temporal metrics."""

    report_confidence: Optional[str] = None
    """"CVSS report confidence temportal metrics."""


@dataclasses.dataclass
class Access:
    """CVSS access metrics."""

    vector: Optional[str] = None
    """CVSS access vector metric. """

    complexity: Optional[str] = None
    """CVSS access complexity metric."""


@dataclasses.dataclass
class Cvss:
    """CVSS2 information for a vulnerability."""

    base: Optional[str] = None
    """CVSS base score assigned to the vulnerability."""

    temporal: Optional[str] = None
    """CVSS temporal score."""

    vector_string: Optional[str] = None
    """CVSS scores of individual metrics."""

    access: Optional[Access] = None
    """CVSS access metrics."""

    impact: Optional[Impact] = None
    """CVSS impact metrics."""

    authentication: Optional[str] = None
    """CVSS authentication metric."""

    exploitability: Optional[str] = None
    """CVSS exploitability metric."""

    remediation_level: Optional[str] = None
    """CVSS remediation level metric. """

    report_confidence: Optional[str] = None
    """CVSS report confidence metric."""


@dataclasses.dataclass
class Mw_Info:
    """Information on malware which exploits a vulnerability."""

    mw_id: str
    """A malware name/ID assigned by Trend Micro."""

    mw_type: Optional[str] = None
    """A type of malware, such as Backdoor, Virus, Worm or Trojan."""

    mw_platform: Optional[str] = None
    """A list of the platforms that may be affected."""

    mw_alias: Optional[str] = None
    """A list of other names used by different vendors and/or publicly available sources that refer
    to the same threat.
    """

    mw_rating: Optional[str] = None
    """An overall risk rating as determined by Trend Micro: Low, Medium or High."""

    mw_link: Optional[str] = None
    """A link to malware details."""


@dataclasses.dataclass
class Mw_Src:
    """A source of malware information."""

    src_name: str
    """The name of the source of the malware information: Trend Micro."""

    mw_list: MutableSequence[Mw_Info]
    """A list of malware information available at the source."""


@dataclasses.dataclass
class Explt:
    """An expoint of a vulnerability."""

    ref: str
    """A CVE reference for the exploitability information."""

    desc: str
    """A description of the exploitability information provided by the source (third party vendor or
    publicly available source).
    """

    link: Optional[str] = None
    """A link to the exploit for the vulnerability, when available from the source."""


@dataclasses.dataclass
class Explt_Src:
    """A source of exploit information."""

    src_name: str
    """A name of a third party vendor or publicly available source whose exploitability information
    is correlated with the vulnerability.
    """

    explt_list: MutableSequence[Explt]
    """A list of exploits available at the source."""


@dataclasses.dataclass
class Correlation:
    """Exploitability information for a vulnerability."""

    exploits: Optional[MutableSequence[Explt_Src]] = None
    """The exploits attribute appears only when there is exploitability information for the
    vulnerability from third party vendors and/or publicly available sources.
    """

    malware: Optional[MutableSequence[Mw_Src]] = None
    """The malware attribute appears only when there is malware information for the vulnerability
    from Trend Micro.
    """


@dataclasses.dataclass
class Compliance:
    """Compliance information associated with the vulnerability."""

    type: str
    """A type of a compliance information associated with the vulnerability: HIPAA, GLBA, CobIT or
    SOX.
    """

    section: str
    """A section of a compliance policy or regulation."""

    description: str
    """A description of a compliance policy or regulation."""


@dataclasses.dataclass
class Cve:
    """A CVE associated with a vulnerability."""

    id: str
    """A CVE name assigned to the vulnerability. """

    url: str
    """The URL to a CVE name."""


@dataclasses.dataclass
class Vendor_Reference:
    """A vendor reference to a vulnerability."""

    id: str
    """A name of a vendor reference."""

    url: str
    """The URL to a vendor reference."""


@dataclasses.dataclass
class Software:
    """A piece of software associated with a vulnerability."""

    product: str
    """Software product information associated with the vulnerability. This information is provided
    by NIST as a part of CVE information. (This element appears only when the API request includes
    the parameter details=All).
    """

    vendor: str
    """Software vendor information associated with the vulnerability. This information is provided
    by NIST as a part of CVE information. (This element appears only when the API request includes
    the parameter details=All).
    """


@dataclasses.dataclass
class Bugtraq:
    """A Bugtraq reference for a vulnerability."""

    id: int
    """A Bugtraq ID for a vulnerability."""

    url: str
    """The URL to a Bugtraq ID."""


@dataclasses.dataclass
class Last_Customization:
    """Information on the last time this vulnerability was customized by a user."""

    datetime: datetime.datetime
    """The date this vulnerability was last customized by a user."""

    user_login: Optional[str] = None
    """The user ID responsible for the last customization."""


@dataclasses.dataclass
class Vuln:
    """A vulnerability listed in the Qualys KnowledgeBase."""

    qid: int
    """The vulnerability QID (Qualys ID), assigned by the service."""

    vuln_type: str
    """The vulnerability type: Vulnerability, Potential Vulnerability or Information Gathered. The
    type “Vulnerability or Potential Vulnerability” corresponds to the half red/half yellow icon in
    the QualyGuard user interface. If confirmed to exist on a host during a scan, the vulnerability
    is classified as a confirmed vulnerability in your account; if not the vulnerability is
    classified as a potential vulnerability in your account.
    """

    severity_level: int
    """The severity level of the vulnerability. A valid value for a confirmed or potential
    vulnerability is an integer 1 to 5, where 5 represents the most serious risk if exploited. A
    valid value for information gathered is a value 1 to 3, where 3 represents the most serious risk
    if exploited.
    """

    title: str
    """The vulnerability title."""

    published_datetime: str
    """The date this vulnerability was published by the service, in YYYY-MM-DDTHH:MM:SSZ format
    (UTC/GMT).
    """

    patchable: bool
    """A flag indicating whether there is a patch available to fix the vulnerability. The value True
    indicates a patch is available to fix the vulnerability. The value False indicates a patch is
    not available to fix the vulnerability.
    """

    discovery: Discovery
    """The discovery method of the vulnerability."""

    supported_modules: Optional[str] = None
    """One or more Qualys modules that can be used to detect the vulnerability. This appears only
    when the API request includes the parameter show_supported_modules_info=True.
    """

    category: Optional[str] = None
    """The vulnerability category."""

    last_customization: Optional[Last_Customization] = None
    """The date this vulnerability was last customized by a user, in YYYY-MM-DDTHH:MM:SSZ format
    (UTC/GMT).
    """

    last_service_modification_datetime: Optional[datetime.datetime] = None
    """The date this vulnerability was last updated by the service, in YYYY-MM-DDTHH:MM:SSZ format
    (UTC/GMT).
    """

    bugtraq_list: Optional[MutableSequence[Bugtraq]] = None
    """A list of Bugtraq references for this vulnerability."""

    software_list: Optional[MutableSequence[Software]] = None
    """A list of software associated with the vulnerability."""

    vendor_reference_list: Optional[MutableSequence[Vendor_Reference]] = None
    """A vendor reference to the vulnerability."""

    cve_list: Optional[MutableSequence[Cve]] = None
    """A list of CVEs assoicated with the vulnerability."""

    diagnosis: Optional[str] = None
    """A service-provided description of the threat posed by the vulnerability if successfully
    exploited.
    """

    diagnosis_comment: Optional[str] = None
    """A user-customized description of the threat posed by the vulnerability if successfully
    exploited.
    """

    consequence: Optional[str] = None
    """A service-provided description of the consequences that may occur if this vulnerability is
    successfully exploited.
    """

    consequence_comment: Optional[str] = None
    """A user-customized description of the consequences that may occur if this vulnerability is
    successfully exploited.
    """

    solution: Optional[str] = None
    """A service-provided description of a verified solution to fix the vulnerability."""

    solution_comment: Optional[str] = None
    """A user-customized description of a verified solution to fix the vulnerability."""

    compliance_list: Optional[MutableSequence[Compliance]] = None
    """Compliance information associated with the vulnerability."""

    correlation: Optional[Correlation] = None
    """Exploitability information for the vulnerability."""

    cvss: Optional[Cvss] = None
    """CVSS2 information for the vulnerability."""

    cvss_v3: Optional[Cvss_V3] = None
    """CVSS3 information for the vulnerability."""

    pci_flag: Optional[bool] = None
    """A flag indicating whether the vulnerability must be fixed to pass PCI compliance. The value
    True indicates the vulnerability must be fixed to pass PCI compliance. The value False indicates
    the vulnerability does not need to be fixed to pass PCI compliance."""

    pci_reasons: Optional[MutableSequence[str]] = None
    """A list of reasons why the vulnerability passed or failed PCI compliance. The API request must
    include the parameter show_pci_reasons=True.
    """

    threat_intelligence: Optional[MutableSequence[str]] = None
    """Qualys Real-Time Threat Indicators (RTIs) associated with the vulnerability."""

    is_disabled: Optional[bool] = None
    """A flag indicating whether the vulnerability is disabled. A value of True means it is
    disabled. A value of False means it is not disabled.
    """

    change_log_list: Optional[MutableSequence[Change_Log_Info]] = None
    """A list of changes to the vulnerability listing."""


def knowledgebase(
    conn: qualysapi.Connection,
    /,
    all_details: Optional[bool] = False,
    ids: Optional[Union[int, range, MutableSequence[Union[int, range]]]] = None,
    id_min: Optional[int] = None,
    id_max: Optional[int] = None,
    is_patchable: Optional[bool] = None,
    last_modified_after: Optional[datetime.datetime] = None,
    last_modified_before: Optional[datetime.datetime] = None,
    last_modified_by_user_after: Optional[datetime.datetime] = None,
    last_modified_by_user_before: Optional[datetime.datetime] = None,
    last_modified_by_service_after: Optional[datetime.datetime] = None,
    last_modified_by_service_before: Optional[datetime.datetime] = None,
    published_after: Optional[datetime.datetime] = None,
    published_before: Optional[datetime.datetime] = None,
    discovery_method: Optional[str] = None,
    discovery_auth_types: Optional[str] = None,
    show_pci_reasons: Optional[bool] = None,
    show_supported_modules_info: Optional[bool] = None,
    show_disabled_flag: Optional[bool] = None,
    show_qid_change_log: Optional[bool] = None,
    post: bool = False,
) -> tuple[
    Optional[Union[MutableSequence[Vuln], MutableSequence[str]]], Optional[Warning]
]:
    """Download a list of vulnerabilities from Qualys' KnowledgeBase. Several input parameters grant
    users control over which vulnerabilities to download and the amount of detail to download, and
    the output provides a rich information source for each vulnerability."""

    params: dict[str, Optional[str]] = {
        "details": qutils.parse_optional_bool(all_details, returns=("All", "Basic")),
        "ids": qutils.to_comma_separated(ids),
        "id_min": str(id_min) if id_min else None,
        "id_max": str(id_max) if id_max else None,
        "is_patchable": qutils.parse_optional_bool(is_patchable),
        "last_modified_after": qutils.datetime_to_qualys_format(last_modified_after),
        "last_modified_before": qutils.datetime_to_qualys_format(last_modified_before),
        "last_modified_by_user_after": qutils.datetime_to_qualys_format(
            last_modified_by_user_after
        ),
        "last_modified_by_user_before": qutils.datetime_to_qualys_format(
            last_modified_by_user_before
        ),
        "last_modified_by_service_after": qutils.datetime_to_qualys_format(
            last_modified_by_service_after
        ),
        "last_modified_by_service_before": qutils.datetime_to_qualys_format(
            last_modified_by_service_before
        ),
        "published_after": qutils.datetime_to_qualys_format(published_after),
        "published_before": qutils.datetime_to_qualys_format(published_before),
        "discovery_method": discovery_method,
        "discovery_auth_types": discovery_auth_types,
        "show_pci_reasons": qutils.parse_optional_bool(show_pci_reasons),
        "show_supported_modules_info": qutils.parse_optional_bool(
            show_supported_modules_info
        ),
        "show_disabled_flag": qutils.parse_optional_bool(show_disabled_flag),
        "show_qid_change_log": qutils.parse_optional_bool(show_qid_change_log),
    }

    params_filtered = qutils.remove_nones_from_dict(params)

    if post:
        raw = conn.post(qutils.URLS["KnowledgeBase"], params=params_filtered)
    else:
        raw = conn.get(qutils.URLS["KnowledgeBase"], params=params_filtered)

    if all_details is None:
        id_set = [str(id) for id in raw.ID_SET]
    else:
        vulns: list[Vuln] = []
        for vuln in raw.RESPONSE.VULN_LIST.VULN:
            v = qutils.elements_to_class(
                vuln,
                Vuln,
                classmap={
                    "discovery": Discovery,
                    "last_customization": Last_Customization,
                    "correlation": Correlation,
                    "cvss": Cvss,
                    "cvss_v3": Cvss_V3,
                    "bugtraq": Bugtraq,
                    "software": Software,
                    "vendor_reference": Vendor_Reference,
                    "cve": Cve,
                    "compliance": Compliance,
                    "correlation": Correlation,
                    "explt_src": Explt_Src,
                    "explt": Explt,
                    "mw_src": Mw_Src,
                    "mw_info": Mw_Info,
                    "access": Access,
                    "impact": Impact,
                    "attack": Attack,
                    "change_log_info": Change_Log_Info,
                },
                listmap={
                    "bugtraq_list": "bugtraq",
                    "software_list": "software",
                    "vendor_reference_list": "vendor_reference",
                    "cve_list": "cve",
                    "compliance_list": "compliance",
                    "pci_reasons": "pci_reason",
                    "threat_intelligence": "threat_intel",
                    "change_log_list": "change_log_info",
                    "exploits": "explt_src",
                    "malware": "mw_src",
                    "explt_list": "explt",
                    "mw_list": "mw_info",
                    "auth_type_list": "auth_type",
                },
                funcmap={
                    "qid": int,
                    "severity_level": int,
                    "patchable": qutils.bool_from_qualys_format,
                    "last_service_modification_datetime": qutils.datetime_from_qualys_format,
                    "pci_flag": qutils.bool_from_qualys_format,
                    "is_disable": qutils.bool_from_qualys_format,
                    "datetime": qutils.datetime_from_qualys_format,
                    "remote": qutils.bool_from_qualys_format,
                },
            )
            vulns.append(v)

        warning = None
        if raw.RESPONSE.find("WARNING") is not None:
            warning = qutils.elements_to_class(raw.RESPONSE.WARNING, Warning)

    if all_details is None:
        return (id_set, warning)
    else:
        return (vulns, warning)
