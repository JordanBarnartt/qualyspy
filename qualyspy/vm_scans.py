import dataclasses
import datetime
import ipaddress
import json
import re
from collections.abc import MutableMapping, MutableSequence, Set
from typing import Any, Optional, Union
import importlib.resources

import dateutil.parser
import lxml
import qualyspy.qualysapi as qualysapi

URLS = json.load(importlib.resources.files("qualyspy").joinpath("urls.json").open())


@dataclasses.dataclass
class Filter:
    """A filter to restrict the scan list output."""

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

    state: Optional[MutableSequence[str]] = None
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
            processed status.
    """

    type_: Optional[str] = None
    """Show only a certain scan type. By default, the scan list
            is not restricted to a certain scan type. A valid value is:
            On-Demand, Scheduled, or API.
    """

    target: Optional[
        MutableSequence[
            Union[
                str,
                ipaddress.IPv4Address,
                ipaddress.IPv6Address,
                ipaddress.IPv4Network,
                ipaddress.IPv6Network,
            ]
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
    """Show only scans launched after a certain date and
            time.\n
            When launched_after_datetime and launched_before_datetime
            are unspecified, the service selects scans launched within the
            past 30 days.\n
            A date/time in the future returns an empty scans list.
    """

    launched_before_datetime: Optional[datetime.datetime] = None
    """Show only scans launched before a certain date and
            time.\n
            When launched_after_datetime and launched_before_datetime
            are unspecified, the service selects scans launched within the
            past 30 days.\n
            A date/time in the future returns a list of all scans (not limited to
            scans launched within the past 30 days).
    """

    scan_type: Optional[str] = None
    """Can be set to one of:\n
            - "certview": List CertView in VM scans only. This option will be
                supported when CertView GA is released and enabled for your
                account.
            - "ec2certview": List EC2 CertView VM scans only.
    """

    client_id: Optional[str] = None
    """Id assigned to the client (Consultant type
            subscriptions).\n
            Mutually exclusive with client_name.
    """

    client_name: Optional[str] = None
    """Name of the client (Consultant type subscriptions).\n
            Mutually exclusive with client_id.
    """

    def params(self) -> MutableMapping[str, Any]:
        """Returns a mapping of Filter parameters to be passed to an API request."""

        params = {
            "scan_ref": self.scan_ref,
            "scan_id": self.scan_id,
            "state": self.state,
            "processed": 1 if self.processed else 0,
            "type": self.type_,
            "target": self.target,
            "user_login": self.user_login,
            "launched_after_datetime": self.launched_after_datetime,
            "launched_before_datetime": self.launched_before_datetime,
            "scan_type": self.scan_type,
            "client_id": self.client_id,
            "client_name": self.client_name,
        }
        return params

    def __post_init__(self) -> None:
        self._check_parameters()

    def __setattr__(self, __name: str, __value: Any) -> None:
        super().__setattr__(__name, __value)
        self._check_parameters()

    def _check_parameters(self) -> None:
        """Confirms that any value with additional restrictions meets those restrictions."""

        good_states = {
            None,
            "Running",
            "Paused",
            "Canceled",
            "Finished",
            "Error",
            "Queued",
            "Loading",
        }

        if self.state:
            for state in self.state:
                if state not in good_states:
                    raise ValueError(f"{state} not one of {good_states}")

        good_types = {None, "On-Demand", "Scheduled", "API"}
        if self.type_ not in good_types:
            raise ValueError(f"{self.scan_type} not one of {good_types}")

        if self.client_id and self.client_name:
            raise ValueError(
                "client_id and client_name cannot both be defined in the same Filter"
            )


@dataclasses.dataclass
class Show_Hide_Information:
    """Specify whether certain information will be included in the output of a scan list."""

    show_ags: bool = False
    """Specify True to show asset group information for each scan in the XML output. By
            default, asset group information is not shown.
    """

    show_op: bool = False
    """Specify True to show option profile information for each scan in the XML output. By
            default, option profile information is not shown.
    """

    show_status: bool = True
    """Specify False to not show scan status for each scan in the XML output. By default, scan
            status is shown.
    """

    show_last: bool = False
    """Specify True to show only the most recent scan (which meets all other search filters in
            the request) in the XML output. By default, all scans are shown in the XML output.
    """

    pci_only: bool = False
    """Specify True to show only external PCI scans in the XML output. External PCI scans are
            vulnerability scans run with the option profile “Payment Card Industry (PCI) Options”.
            When pci_only=True is specified, the XML output will not include other types of scans
            run with other option profiles.
    """

    ignore_target: bool = False
    """Specify True to hide target information from the scan list. Specify False to display the
            target information.
    """

    def params(self) -> MutableMapping[str, int]:
        params = {
            "show_ags": int(self.show_ags),
            "show_op": int(self.show_op),
            "show_status": int(self.show_status),
            "show_last": int(self.show_last),
            "pci_only": int(self.pci_only),
            "ignore_target": int(self.ignore_target),
        }
        return params


@dataclasses.dataclass
class Client:
    """A Qualys client (only for Consultant type subscriptions)."""

    id: Optional[str] = None
    """Id assigned to the client."""

    name: Optional[str] = None
    """Name of the client."""


@dataclasses.dataclass
class Status:
    """The Status of a scan."""

    state: str
    """The scan state: Running, Paused, Canceled, Finished, Error, Queued (scan
            job is waiting to be distributed to scanner(s)), or Loading (scanner(s) are
            finished and scan results are being loaded onto the platform).
    """

    sub_state: Optional[str] = None
    """The sub-state related to the scan state, if any. For scan state Finished, value
            can be: No_Vuln (no vulnerabilities found) or No_Host (no host alive). For
            scan state Queued, value can be: Launching (service received scan request),
            Pausing (service received pause scan request), or Resuming (service
            received resume scan request).
    """


@dataclasses.dataclass
class Option_Profile:
    """A set of options specified for a scan."""

    title: str
    """The option profile title specified for the scan."""

    default_flag: Optional[bool] = None
    """A flag that specifies whether the option profile was defined as the default
            option profile in the user account. A value of True is returned when this option
            profile is the default. A value of False is returned when this option profile is not
            the default.
    """


@dataclasses.dataclass
class Scan:
    """An object representing a Qualys scan."""

    ref: str
    """The scan reference code."""

    type_: str
    """The scan type: On-Demand, Scheduled or API."""

    title: str
    """The scan title."""

    user_login: str
    """The user login ID of the user who launched the scan."""

    launch_datetime: datetime.datetime
    """The date and time when the scan was launched."""

    duration: Union[datetime.timedelta, str]
    """The time it took to perform the scan - when the scan status is Finished. For
            a scan that has not finished (queued, running), the duration is set to
            “Pending”.
    """

    processed: bool
    """A flag that specifies whether the scan results have been processed. A value
            of True is returned when the scan results have been processed. A value of False is
            returned when the results have not been processed.
    """

    status: Status
    """The state of a scan, and its substate if applicable."""

    target: Set[
        Union[
            str,
            ipaddress.IPv4Address,
            ipaddress.IPv6Address,
        ]
    ]
    """The scan target hosts. This element does not appear when API request
            includes ignore_target=True.
    """

    id: Optional[str] = None
    """The scan ID."""

    scan_type: Optional[str] = None
    """For a CertView VM scan this is set to “CertView”."""

    client: Optional[Client] = None
    """The client of the scan (only for Consultant type subscriptions)."""

    processing_priority: Optional[str] = None
    """(Applicable for VM scans only) The processing priority setting for the scan."""

    asset_group_title_list: Optional[MutableSequence[str]] = None
    """A list of asset group titles specified for the scan."""

    option_profile: Optional[Option_Profile] = None
    """The option profile specified for the scan."""


DURATION_RE = re.compile("(\\d+)*(?: day[s]* )*(\\d\\d):(\\d\\d):(\\d\\d)")


def _parse_duration(duration):
    """Parse the string-formatted duration value into a datetime.timedelta object."""

    match = DURATION_RE.match(duration)
    days = int(match.group(1)) if match.group(1) else 0
    hours = int(match.group(2)) if match.group(2) else 0
    minutes = int(match.group(3)) if match.group(3) else 0
    seconds = int(match.group(4)) if match.group(4) else 0
    return datetime.timedelta(hours=hours + 24 * days, minutes=minutes, seconds=seconds)


def _parse_elements(
    xml: lxml.objectify.ObjectifiedElement,
    elements: MutableMapping[str, Any] = dict(),
    prefix="",
) -> MutableMapping[str, Any]:
    """Parse a tree of lxml objects into a dictionary of tag:value pairs, where tags with
    descendants are themselves dictionarys.
    """

    for child in xml.iterchildren():
        if type(child) == lxml.objectify.ObjectifiedElement:
            elements[child.tag.lower()] = dict()
            _parse_elements(
                child, elements[child.tag.lower()], prefix=child.tag.lower()
            )
        else:
            elements[child.tag.lower()] = prefix + child.text

    return elements


def _parse_targets(
    ips: str,
) -> Set[Union[str, ipaddress.IPv4Address, ipaddress.IPv6Address]]:
    """Parse a comma delineated list of IPs and IP ranges represented as <Start IP>-<End IP> into a
    list of IPAddress objects.
    """

    targets: list[Union[str, ipaddress.IPv4Address, ipaddress.IPv6Address]] = []
    for target in ips.split(","):
        try:
            if "-" not in target:
                targets.append(ipaddress.ip_address(target))
            else:
                start_ip, end_ip = target.split("-")
                ip = ipaddress.ip_address(start_ip)
                while ip.compressed <= ipaddress.ip_address(end_ip).compressed:
                    targets.append(ip)
                    ip += 1
        except ValueError:
            targets.append(target)
    targets_set = set(targets)
    return targets_set


def get_scan_list(
    conn: qualysapi.Connection,
    filter: Optional[Filter] = None,
    show_hide_information: Optional[Show_Hide_Information] = None,
) -> MutableSequence[Scan]:
    """List vulnerability scans in the user's account. By default, the output lists scans launched
        in the past 30 days.

    Args:
        conn:
            A connection to the Qualys API.
        filter:
            Several parameters allow you to set filters to restrict the scan list output. When no
            filters are specified, the service returns all scans launched by all users within the
            past 30 days.
        show_hide_information:
            These parameters specify whether certain information will be shown in the output.


    Returns:
        A list of Scan objects.  Each object represents a single Qualys scan matching the parameters
        of the filter supplied.

    Example:
        conn = qualysapi.Connection()\n
        scans = vm_scans.get_scan_list(conn)
    """

    params: MutableMapping[str, int] = dict()
    if filter:
        params.update(filter.params())
    if show_hide_information:
        params.update(show_hide_information.params())
    raw = conn.request(URLS["VM Scan List"], params=params)

    scans = []
    for scan in raw["RESPONSE"]["SCAN_LIST"].iterchildren():
        scan_elements = _parse_elements(scan)

        # Convert elements to expected types
        scan_elements["type_"] = scan_elements["type"]
        scan_elements.pop("type")
        scan_elements["launch_datetime"] = dateutil.parser.isoparse(
            scan_elements["launch_datetime"]
        )
        if scan_elements["duration"] != "Pending":
            scan_elements["duration"] = _parse_duration(scan_elements["duration"])
        scan_elements["processed"] = bool(scan_elements["processed"])
        scan_elements["target"] = _parse_targets(scan_elements["target"])
        if "client" in scan_elements:
            scan_elements["client"] = Client(
                id=scan_elements["client"]["id"], name=scan_elements["client"]["name"]
            )
        if "status" in scan_elements:
            if "sub_state" in scan_elements["status"]:
                scan_elements["status"] = Status(
                    state=scan_elements["status"]["state"],
                    sub_state=scan_elements["status"]["sub_state"],
                )
            else:
                scan_elements["status"] = Status(
                    state=scan_elements["status"]["state"],
                )
        if "asset_group_title_list" in scan_elements:
            scan_elements["asset_group_title_list"] = [
                agt for agt in scan_elements["asset_group_title_list"].split(",")
            ]
        if "option_profile" in scan_elements:
            scan_elements["option_profile"] = Option_Profile(
                title=scan_elements["option_profile"]["title"],
                default_flag=scan_elements["option_profile"]["default_flag"],
            )

        scans.append(Scan(**scan_elements))
    return scans

class Scanner_Appliance():
    """Scanner appliance"""


def launch_scan(
    conn: qualysapi.Connectionm,
    scan_title: str,
    option_profile: Option_Profile,
    scanner_appliance: Scanner_Appliance,
    asset_ips_groups: Union[]
    processing_priority: int = 0
):
    """Launch vulnerability scan in the user's account.

    Notes:
        The Launch Scan API is asynchronous. When you make a request to launch a scan using
        this API, the service will return a scan reference ID right away and the call will quit
        without waiting for the complete scan results.

        When you launch a VM scan using the API, we check to see if the IPs in the scan target
        are available to the user making the scan request. To determine this, Qualys checks that
        each IP is in the subscription, in the VM license, and in the user's assigned scope. If any
        IP in the target is not available to the user, then it will be skipped from the scan job.

        For example, let's say you specify the IP range 10.10.10.100-10.10.10.120, but IPs
        10.10.10.115 and 10.10.10.120 are not available to you. In this case, Qualys will launch
        the scan on 10.10.10.100-10.10.10.114, 10.10.10.116-10.10.10.119, and Qualys will skip
        10.10.10.115 and 10.10.10.120.

        Using networks? Choose the Global Default Network to scan IPs on your network
        perimeter.

    Args:
        scan_title:
    """
