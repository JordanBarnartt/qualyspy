from dataclasses import field
from typing import Optional

from pydantic.dataclasses import dataclass

__NAMESPACE__ = "http://am.oxm.api.portal.qualys.com/v3"


@dataclass
class AzureAuthRecord:
    application_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "applicationId",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    directory_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "directoryId",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    authentication_key: Optional[str] = field(
        default=None,
        metadata={
            "name": "authenticationKey",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    subscription_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "subscriptionId",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )


@dataclass
class AzureAuthRecordSimple(AzureAuthRecord):
    id: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
