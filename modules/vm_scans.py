import dataclasses
import datetime
import ipaddress
import typing


@dataclasses.dataclass
class Filter:
    scan_ref: typing.Optional[str] = None
    scan_id: typing.Optional[str] = None
    state: typing.Optional[typing.List[str]] = None
    processed: typing.Optional[bool] = None
    _type: typing.Optional[str] = None
    target: typing.List[typing.Union[ipaddress.IPv4Address,
                                     ipaddress.IPv6Address,
                                     ipaddress.IPv4Network,
                                     ipaddress.IPv6Network]] = None
    user_login: typing.Optional[str] = None
    launched_after_datetime = typing.Optional[datetime.datetime] = None
    launched_before_datetime = typing.Optional[datetime.datetime] = None
    scan_type = typing.Optional[str] = None
    client_id = typing.Optional[str] = None
    client_name = typing.Optional[str] = None


@dataclasses.dataclass
class Status:
    state: str
    sub_state: str = None


@dataclasses.dataclass
class Option_Profile:
    title: str
    default_flag: typing.Optional[bool] = None


@dataclasses.dataclass
class Scan:
    ref: str
    _type: str
    title: str
    user_login: str
    launch_datetime: datetime.datetime
    duration: datetime.timedelta
    processed: bool
    target: typing.List[typing.Union[ipaddress.IPv4Address,
                                     ipaddress.IPv6Address,
                                     ipaddress.IPv4Network,
                                     ipaddress.IPv6Network]]
    id: str = None
    scan_type: typing.Optional[str] = None
    processing_priority: typing.Optional[str] = None
    status: typing.Optional[Status] = None
    asset_group_title_list: typing.Optional[typing.List[str]] = None
    option_profile: typing.Optional[str] = None
