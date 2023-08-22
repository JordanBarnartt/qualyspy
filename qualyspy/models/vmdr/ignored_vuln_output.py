from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


@dataclass
class Ip:
    class Meta:
        name = "IP"

    network_id: Optional[str] = field(
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
class Request:
    class Meta:
        name = "REQUEST"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    at: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    username: Optional[str] = field(
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


class ResponseStatus(Enum):
    FAILED = "FAILED"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"


@dataclass
class Ignored:
    class Meta:
        name = "IGNORED"

    ticket_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "TICKET_NUMBER",
            "type": "Element",
            "required": True,
        },
    )
    qid: Optional[str] = field(
        default=None,
        metadata={
            "name": "QID",
            "type": "Element",
            "required": True,
        },
    )
    ip: Optional[Ip] = field(
        default=None,
        metadata={
            "name": "IP",
            "type": "Element",
            "required": True,
        },
    )
    dns: Optional[str] = field(
        default=None,
        metadata={
            "name": "DNS",
            "type": "Element",
        },
    )
    netbios: Optional[str] = field(
        default=None,
        metadata={
            "name": "NETBIOS",
            "type": "Element",
        },
    )


@dataclass
class Restored:
    class Meta:
        name = "RESTORED"

    ticket_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "TICKET_NUMBER",
            "type": "Element",
            "required": True,
        },
    )
    qid: Optional[str] = field(
        default=None,
        metadata={
            "name": "QID",
            "type": "Element",
            "required": True,
        },
    )
    ip: Optional[Ip] = field(
        default=None,
        metadata={
            "name": "IP",
            "type": "Element",
            "required": True,
        },
    )
    dns: Optional[str] = field(
        default=None,
        metadata={
            "name": "DNS",
            "type": "Element",
        },
    )
    netbios: Optional[str] = field(
        default=None,
        metadata={
            "name": "NETBIOS",
            "type": "Element",
        },
    )


@dataclass
class IgnoredList:
    class Meta:
        name = "IGNORED_LIST"

    ignored: List[Ignored] = field(
        default_factory=list,
        metadata={
            "name": "IGNORED",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class RestoredList:
    class Meta:
        name = "RESTORED_LIST"

    restored: List[Restored] = field(
        default_factory=list,
        metadata={
            "name": "RESTORED",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class Response:
    class Meta:
        name = "RESPONSE"

    status: Optional[ResponseStatus] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    number: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    message: Optional[str] = field(
        default=None,
        metadata={
            "name": "MESSAGE",
            "type": "Element",
            "required": True,
        },
    )
    ignored_list: Optional[IgnoredList] = field(
        default=None,
        metadata={
            "name": "IGNORED_LIST",
            "type": "Element",
        },
    )
    restored_list: Optional[RestoredList] = field(
        default=None,
        metadata={
            "name": "RESTORED_LIST",
            "type": "Element",
        },
    )


@dataclass
class IgnoreVulnOutput:
    class Meta:
        name = "IGNORE_VULN_OUTPUT"

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
