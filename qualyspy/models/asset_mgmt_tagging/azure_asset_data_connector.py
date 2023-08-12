from dataclasses import field
from typing import Optional

from pydantic.dataclasses import dataclass

from .asset_data_connector import AssetDataConnector
from .azure_service import AzureAuthRecordSimple

__NAMESPACE__ = "http://am.oxm.api.portal.qualys.com/v3"


@dataclass
class AzureAssetDataConnector(AssetDataConnector):
    auth_record: Optional[AzureAuthRecordSimple] = field(
        default=None,
        metadata={
            "name": "authRecord",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
            "required": True,
        },
    )
    subscription_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "subscriptionName",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
