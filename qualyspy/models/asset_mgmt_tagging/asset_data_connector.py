from dataclasses import field
from enum import Enum
from typing import List, Optional

from pydantic.dataclasses import dataclass
from xsdata.models.datatype import XmlDate, XmlDateTime

from .tag import Tag, TagSimpleQlist

__NAMESPACE__ = "http://am.oxm.api.portal.qualys.com/v3"


class ActivationModule(Enum):
    VM = "VM"
    PC = "PC"
    SCA = "SCA"
    CLOUDVIEW = "CLOUDVIEW"
    CERTVIEW = "CERTVIEW"


@dataclass
class ActivationModuleObj:
    activation_module: list[ActivationModule] = field(
        default_factory=list,
        metadata={
            "name": "ActivationModule",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )


@dataclass
class AssetDataConnectorErrors:
    error_message: Optional[str] = field(
        default=None,
        metadata={
            "name": "errorMessage",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    created: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )


class AssetDataConnectorState(Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"
    QUEUED = "QUEUED"
    PROCESSING = "PROCESSING"
    FINISHED_SUCCESS = "FINISHED_SUCCESS"
    FINISHED_ERRORS = "FINISHED_ERRORS"
    DISABLED = "DISABLED"
    INCOMPLETE = "INCOMPLETE"


class AssetDataConnectorType(Enum):
    AWS = "AWS"
    AZURE = "AZURE"
    OCI = "OCI"


@dataclass
class ConnectorApp:
    id: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )


class ConnectorScanRecurrence(Enum):
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"


@dataclass
class ConnectorScanSetting:
    is_custom_scan_config_enabled: Optional[bool] = field(
        default=None,
        metadata={
            "name": "isCustomScanConfigEnabled",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )


class Day(Enum):
    SUN = "SUN"
    MON = "MON"
    TUE = "TUE"
    WED = "WED"
    THU = "THU"
    FRI = "FRI"
    SAT = "SAT"


@dataclass
class TagMetadata:
    id: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    icon: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    color: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    foreground_color: Optional[str] = field(
        default=None,
        metadata={
            "name": "foregroundColor",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    background_color: Optional[str] = field(
        default=None,
        metadata={
            "name": "backgroundColor",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )


@dataclass
class ActivationModuleQlist:
    class Meta:
        name = "ActivationModuleQList"

    count: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    list_value: List[ActivationModule] = field(
        default_factory=list,
        metadata={
            "name": "list",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    set: Optional[ActivationModuleObj] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    add: Optional[ActivationModuleObj] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    remove: Optional[ActivationModuleObj] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    update: Optional[ActivationModuleObj] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    activation_module: List[ActivationModule] = field(
        default_factory=list,
        metadata={
            "name": "ActivationModule",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )


@dataclass
class ConnectorAppInfo:
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    identifier: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    tag_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "tagId",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    tag_metadata: Optional[TagMetadata] = field(
        default=None,
        metadata={
            "name": "tagMetadata",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )


@dataclass
class ConnectorIdentifierTagInfo:
    id: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    tag: Optional[Tag] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )


@dataclass
class DaysOfWeekQlist:
    class Meta:
        name = "DaysOfWeekQList"

    count: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    list_value: List[Day] = field(
        default_factory=list,
        metadata={
            "name": "list",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    set: List[Day] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    add: List[Day] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    remove: List[Day] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    update: List[Day] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )


@dataclass
class ConnectorAppInfoObj:
    connector_app_info: Optional[ConnectorAppInfo] = field(
        default=None,
        metadata={
            "name": "ConnectorAppInfo",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )


@dataclass
class ConnectorAppInfoQlist:
    class Meta:
        name = "ConnectorAppInfoQList"

    count: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    list_value: List[ConnectorAppInfoObj] = field(
        default_factory=list,
        metadata={
            "name": "list",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    set: Optional[ConnectorAppInfoObj] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    add: List[ConnectorAppInfoObj] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    remove: List[ConnectorAppInfoObj] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    update: List[ConnectorAppInfoObj] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )


@dataclass
class ConnectorAppInfoQlistList:
    connector_app_info_q_list: list[ConnectorAppInfoQlist] = field(
        default_factory=list,
        metadata={
            "name": "ConnectorAppInfoQList",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )


@dataclass
class ConnectorAppInfoQlistObj:
    connector_app_info_qlist: Optional[ConnectorAppInfoQlist] = field(
        default=None,
        metadata={
            "name": "ConnectorAppInfoQList",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )


@dataclass
class ConnectorIdentifierTagInfoQlist:
    class Meta:
        name = "ConnectorIdentifierTagInfoQList"

    count: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    list_value: List[ConnectorIdentifierTagInfo] = field(
        default_factory=list,
        metadata={
            "name": "list",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    set: List[ConnectorIdentifierTagInfo] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    add: List[ConnectorIdentifierTagInfo] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    remove: List[ConnectorIdentifierTagInfo] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    update: List[ConnectorIdentifierTagInfo] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )


@dataclass
class ConnectorScanConfiguration:
    scan_prefix: Optional[str] = field(
        default=None,
        metadata={
            "name": "scanPrefix",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    option_profile_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "optionProfileId",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    recurrence: Optional[ConnectorScanRecurrence] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    start_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "startDate",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    start_time: Optional[str] = field(
        default=None,
        metadata={
            "name": "startTime",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    days_of_week: Optional[DaysOfWeekQlist] = field(
        default=None,
        metadata={
            "name": "daysOfWeek",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    timezone: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )


@dataclass
class ConnectorScanConfigurationObj:
    connector_scan_config: Optional[ConnectorScanConfiguration] = field(
        default=None,
        metadata={
            "name": "ConnectorScanConfiguration",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )


@dataclass
class ConnectorAppInfoList:
    count: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    list_value: List[ConnectorAppInfoQlistObj] = field(
        default_factory=list,
        metadata={
            "name": "list",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    set: Optional[ConnectorAppInfoQlistList] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    add: Optional[ConnectorAppInfoQlistList] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    remove: Optional[ConnectorAppInfoQlistList] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    update: Optional[ConnectorAppInfoQlistList] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )


@dataclass
class ConnectorIdentifier:
    id: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    identifier: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    connector_identifier_tag_infos: List[ConnectorIdentifierTagInfoQlist] = field(
        default_factory=list,
        metadata={
            "name": "connectorIdentifierTagInfos",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )


@dataclass
class ConnectorScanConfigQlist:
    class Meta:
        name = "ConnectorScanConfigQList"

    count: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    list_value: List[ConnectorScanConfigurationObj] = field(
        default_factory=list,
        metadata={
            "name": "list",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    set: List[ConnectorScanConfiguration] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    add: List[ConnectorScanConfiguration] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    remove: List[ConnectorScanConfiguration] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    update: List[ConnectorScanConfiguration] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )


@dataclass
class AssetDataConnector:
    id: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    aws_account_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "awsAccountId",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    last_sync: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "lastSync",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    last_error: Optional[str] = field(
        default=None,
        metadata={
            "name": "lastError",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    connector_state: Optional[AssetDataConnectorState] = field(
        default=None,
        metadata={
            "name": "connectorState",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    type_value: Optional[AssetDataConnectorType] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    default_tags: Optional[TagSimpleQlist] = field(
        default=None,
        metadata={
            "name": "defaultTags",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    activation: Optional[ActivationModuleQlist] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    disabled: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    is_gov_cloud_configured: Optional[bool] = field(
        default=None,
        metadata={
            "name": "isGovCloudConfigured",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    is_china_configured: Optional[bool] = field(
        default=None,
        metadata={
            "name": "isChinaConfigured",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    is_deleted: Optional[bool] = field(
        default=None,
        metadata={
            "name": "isDeleted",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    run_frequency: Optional[int] = field(
        default=None,
        metadata={
            "name": "runFrequency",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    next_sync: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "nextSync",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    is_remediation_enabled: Optional[bool] = field(
        default=None,
        metadata={
            "name": "isRemediationEnabled",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    is_cpsenabled: Optional[bool] = field(
        default=None,
        metadata={
            "name": "isCPSEnabled",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    connector_app_infos: Optional[ConnectorAppInfoList] = field(
        default=None,
        metadata={
            "name": "connectorAppInfos",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    cloudview_uuid: Optional[str] = field(
        default=None,
        metadata={
            "name": "cloudviewUuid",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    connector_scan_setting: Optional[ConnectorScanSetting] = field(
        default=None,
        metadata={
            "name": "connectorScanSetting",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    connector_scan_config: Optional[ConnectorScanConfigQlist] = field(
        default=None,
        metadata={
            "name": "connectorScanConfig",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    is_instant_assessment_enabled: Optional[bool] = field(
        default=None,
        metadata={
            "name": "isInstantAssessmentEnabled",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    is_attached_to_org_connector: Optional[bool] = field(
        default=None,
        metadata={
            "name": "isAttachedToOrgConnector",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    is_wrapper_api: Optional[bool] = field(
        default=None,
        metadata={
            "name": "isWrapperAPI",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )


@dataclass
class ConnectorIdentifierQlist:
    class Meta:
        name = "ConnectorIdentifierQList"

    count: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    list_value: List[ConnectorIdentifier] = field(
        default_factory=list,
        metadata={
            "name": "list",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    set: List[ConnectorIdentifier] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    add: List[ConnectorIdentifier] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    remove: List[ConnectorIdentifier] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    update: List[ConnectorIdentifier] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )


@dataclass
class ConnectorAppCapability:
    id: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    connector_app: Optional[ConnectorApp] = field(
        default=None,
        metadata={
            "name": "connectorApp",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    connector_identifiers: List[ConnectorIdentifierQlist] = field(
        default_factory=list,
        metadata={
            "name": "connectorIdentifiers",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )


@dataclass
class ConnectorAppCapabilityQlist:
    class Meta:
        name = "ConnectorAppCapabilityQList"

    count: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    list_value: List[ConnectorAppCapability] = field(
        default_factory=list,
        metadata={
            "name": "list",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    set: List[ConnectorAppCapability] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    add: List[ConnectorAppCapability] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    remove: List[ConnectorAppCapability] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    update: List[ConnectorAppCapability] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
