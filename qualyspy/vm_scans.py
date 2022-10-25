import dataclasses
import datetime
import dateutil.parser
import ipaddress
import re
from collections.abc import Sequence, Set
from typing import Optional, Union


@dataclasses.dataclass
class Filter:
    """A filter to restrict the scan list output.  Passed as a parameter to get_scans().
    """
    scan_ref: Optional[str] = None
    """Show only a scan with a certain scan reference code.
            When unspecified, the scan list is not restricted to a certain scan.\n
            For a vulnerability scan, the format is:
            scan/987659876.19876\n
            For a compliance scan the format is:
            compliance/98765456.12345\n
            For a SCAP scan the format is:
            qscap/987659999.22222
    """
    scan_id: Optional[str] = None
    """Show only a scan with a certain compliance scan ID."""
    state: Optional[Sequence[str]] = None
    """Show only one or more scan states. By default, the
            scan list is not restricted to certain states. A valid value is:
            Running, Paused, Canceled, Finished, Error, Queued (scan job is
            waiting to be distributed to scanner(s)), or Loading (scanner(s) are
            finished and scan results are being loaded onto the platform).
    """
    processed: Optional[bool] = None
    """Specify False to show only scans that are not processed.
            Specify True to show only scans that have been processed. When not
            specified, the scan list output is not filtered based on the
            processed status."""
    scan_type: Optional[str] = None
    """Show only a certain scan type. By default, the scan list
            is not restricted to a certain scan type. A valid value is:
            On-Demand, Scheduled, or API.
    """
    target: Sequence[
        Union[
            ipaddress.IPv4Address,
            ipaddress.IPv6Address,
            ipaddress.IPv4Network,
            ipaddress.IPv6Network,
        ]
    ] = None
    """Show only one or more target IP addresses. By default,
            the scan list includes all scans on all IP addresses. 
    """
    user_login: Optional[str] = None
    """Show only a certain user login. The user login
            identifies a user who launched scans. By default, the scan list is
            not restricted to scans launched by a particular user. Enter the
            login name for a valid Qualys user account.
    """
    launched_after_datetime: Optional[datetime.datetime] = None
    """ Show only scans launched after a certain date and
            time. The date/time is specified in YYYY-MM-
            DD[THH:MM:SSZ] format (UTC/GMT), like “2007-07-01” or “2007-
            01-25T23:12:00Z”.\n
            When launched_after_datetime and launched_before_datetime
            are unspecified, the service selects scans launched within the
            past 30 days.\n
            A date/time in the future returns an empty scans list.
    """
    launched_before_datetime: Optional[datetime.datetime] = None
    scan_type: Optional[str] = None
    client_id: Optional[str] = None
    client_name: Optional[str] = None

    def __post_init__(self):
        good_states = set("Running", "Paused", "Canceled", "Finished", "Error", "Queued", "Loading")
        for state in self.states:
            if state not in good_states:
                raise ValueError(f"{state} not one of {good_states}")

        good_scan_types = set("On-Demand", "Scheduled", "API")
        if self.scan_type not in good_scan_types:
            raise ValueError(f"{self.scan_type} not one of {good_scan_types}")



@dataclasses.dataclass
class Status:
    state: str
    sub_state: str = None


@dataclasses.dataclass
class Option_Profile:
    title: str
    default_flag: Optional[bool] = None


@dataclasses.dataclass
class Scan:
    ref: str
    _type: str
    title: str
    user_login: str
    launch_datetime: datetime.datetime
    duration: Union[datetime.timedelta, str]
    processed: bool
    target: Set[
        Union[
            ipaddress.IPv4Address,
            ipaddress.IPv6Address,
            ipaddress.IPv4Network,
            ipaddress.IPv6Network,
        ]
    ]
    id: str = None
    scan_type: Optional[str] = None
    processing_priority: Optional[str] = None
    status: Optional[Status] = None
    asset_group_title_list: Optional[Sequence[str]] = None
    option_profile: Optional[str] = None


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
        scan_elements = {child.tag.lower(): child.text for child in scan.iterchildren()}

        # Convert elements to expected types
        scan_elements["_type"] = scan_elements["type"]
        scan_elements.pop("type")
        scan_elements["launch_datetime"] = dateutil.parser.isoparse(
            scan_elements["launch_datetime"]
        )
        if scan_elements["duration"] != "Pending":
            scan_elements["duration"] = parse_duration(scan_elements["duration"])
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
                agt for agt in scan_elements["asset_group_title"].split(",")
            ]

        scans.append(Scan(**scan_elements))
    return scans
