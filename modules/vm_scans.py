import dataclasses
import datetime
import dateutil.parser
import ipaddress
import re
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
    launched_after_datetime: typing.Optional[datetime.datetime] = None
    launched_before_datetime: typing.Optional[datetime.datetime] = None
    scan_type: typing.Optional[str] = None
    client_id: typing.Optional[str] = None
    client_name: typing.Optional[str] = None


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
    duration: typing.Union[datetime.timedelta, str]
    processed: bool
    target: typing.Set[typing.Union[ipaddress.IPv4Address,
                                    ipaddress.IPv6Address,
                                    ipaddress.IPv4Network,
                                    ipaddress.IPv6Network]]
    id: str = None
    scan_type: typing.Optional[str] = None
    processing_priority: typing.Optional[str] = None
    status: typing.Optional[Status] = None
    asset_group_title_list: typing.Optional[typing.List[str]] = None
    option_profile: typing.Optional[str] = None


DURATION_RE = re.compile("(\\d+)*(?: day[s]* )*(\\d\\d):(\\d\\d):(\\d\\d)")


def parse_duration(duration):
    match = DURATION_RE.match(duration)
    days = int(match.group(1)) if match.group(1) else 0
    hours = int(match.group(2)) if match.group(2) else 0
    minutes = int(match.group(3)) if match.group(3) else 0
    seconds = int(match.group(4)) if match.group(4) else 0
    return datetime.timedelta(hours=hours + 24 * days, minutes=minutes, seconds=seconds)


def get_scans(conn, filter=None, modifiers=None):
    raw = conn.request("fo/scan/?action=list")
    scans = []
    for scan in raw["RESPONSE"]["SCAN_LIST"].iterchildren():
        scan_elements = {
            child.tag.lower(): child.text for child in scan.iterchildren()}

        # Convert elements to expected types
        scan_elements["_type"] = scan_elements["type"]
        scan_elements.pop("type")
        scan_elements["launch_datetime"] = dateutil.parser.isoparse(
            scan_elements["launch_datetime"])
        if scan_elements["duration"] != "Pending":
            scan_elements["duration"] = parse_duration(
                scan_elements["duration"])
        scan_elements["processed"] = bool(scan_elements["processed"])
        targets = []
        for target in scan_elements["target"].split(","):
            if "-" not in target:
                targets.append(ipaddress.ip_address(target))
            else:
                start_ip, end_ip = target.split("-")
                ip = ipaddress.ip_address(start_ip)
                while ip <= ipaddress.ip_address(end_ip):
                    targets.append(ip)
                    ip += 1
        scan_elements["target"] = set(targets)
        if "asset_group_title" in scan_elements:
            scan_elements["asset_group_title"] = [
                agt for agt in scan_elements["asset_group_title"].split(",")]

        scans.append(Scan(**scan_elements))
    return scans
