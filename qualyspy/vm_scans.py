"""Python wrapper for Qualys VM Scans API.

Obtain a list of vulnerability scans in your account and take actions on them like cancel,
pause, resume, and fetch (download) finished results.

Example:
    import qualyspy.qualysapi as qualysapi\n
    import qualyspy.vm_scans as vm_scans\n
    conn = qualysapi.Connection()\n
    ip = ipaddress.IPv4Address("172.25.29.137")\n
    scan_assets = vm_scans.Scan_Asset_Ips_Groups(ip=ip)\n
    output = vm_scans.launch_scan(conn, scan_assets=scan_assets, scan_title="qualyspy test",
    iscanner_name="my-scanner", option_title="MyOptionProfile")\n
    output = vm_scans.fetch_scan_csv(conn, "scan/1669646302.25173", "test_output.csv")
"""

import dataclasses
import datetime
import importlib.resources
import ipaddress
import json
import re
from collections.abc import MutableMapping, MutableSequence, Set
from typing import Any, Optional, TextIO, Union

import dateutil.parser

import qualyspy.qualysapi as qualysapi
import qualyspy.utils as qutils

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

    title: Optional[str] = ""
    """The title of the option profile.  When creating an Option_Profile, only one of title or id
        should be defined."""

    id: Optional[int] = None
    """The ID of the option profile.  When creating an Option_Profile, only one of title or id
        should be defined."""

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

    processing_priority: Optional[str] = None
    """(Applicable for VM scans only) The processing priority setting for the scan."""

    asset_group_title_list: Optional[MutableSequence[str]] = None
    """A list of asset group titles specified for the scan."""

    option_profile: Optional[Option_Profile] = None
    """The option profile specified for the scan."""


DURATION_RE = re.compile("(\\d+)*(?: day[s]* )*(\\d\\d):(\\d\\d):(\\d\\d)")


def _parse_duration(duration: str) -> datetime.timedelta:
    """Parse the string-formatted duration value into a datetime.timedelta object."""

    match = DURATION_RE.match(duration)
    if match:
        days = int(match.group(1)) if match.group(1) else 0
        hours = int(match.group(2)) if match.group(2) else 0
        minutes = int(match.group(3)) if match.group(3) else 0
        seconds = int(match.group(4)) if match.group(4) else 0
        return datetime.timedelta(
            hours=hours + 24 * days, minutes=minutes, seconds=seconds
        )
    else:
        raise ValueError(f"{duration} not valid duration")


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


def scan_list(
    conn: qualysapi.Connection,
    filter: Optional[Filter] = None,
    show_hide_information: Optional[Show_Hide_Information] = None,
    post: bool = False,
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
        post:
            Run as a POST request.There are known limits for the amount of data that can be sent
            using the GET method, so POST should be used in those cases.


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
    if post:
        raw = conn.post(URLS["VM Scan List"], params=params)
    else:
        raw = conn.get(URLS["VM Scan List"], params=params)

    scans = []
    for scan in raw.RESPONSE.SCAN_LIST.SCAN:
        scan_elements = qutils.parse_elements(scan)

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


@dataclasses.dataclass
class Scan_Asset_Ips_Groups:
    """A description of the IPs or Groups to be scanned."""

    ip: Optional[
        Union[
            ipaddress.IPv4Address,
            ipaddress.IPv6Address,
            ipaddress.IPv4Network,
            ipaddress.IPv6Network,
            MutableSequence[
                Union[
                    ipaddress.IPv4Address,
                    ipaddress.IPv6Address,
                    ipaddress.IPv4Network,
                    ipaddress.IPv6Network,
                ]
            ],
        ]
    ] = None
    """The IP addresses to be scanned. You may enter individual IP addresses and/or ranges.  One of
    parameters is required: ip, asset_groups or asset_group_ids.
    """

    asset_groups: Optional[MutableSequence[str]] = None
    """The titles of asset groups containing the hosts to be scanned. One of these parameters is
    required: ip, asset_groups or asset_group_ids.
    """

    asset_group_ids: Optional[MutableSequence[str]] = None
    """ The IDs of asset groups containing the hosts to be scanned. One of these parameters is
    required: ip, asset_groups or asset_group_ids."""

    exlude_ip_per_scan: Optional[
        Union[
            ipaddress.IPv4Address,
            ipaddress.IPv6Address,
            ipaddress.IPv4Network,
            ipaddress.IPv6Network,
            MutableSequence[
                Union[
                    ipaddress.IPv4Address,
                    ipaddress.IPv6Address,
                    ipaddress.IPv4Network,
                    ipaddress.IPv6Network,
                ]
            ],
        ]
    ] = None
    """The IP addresses to be excluded from the scan."""

    default_scanner: bool = False
    """ Specify True to use the default scanner in each target asset group.  default_scanner is
    valid when the scan target is specified using one of these parameters: asset_groups,
    asset_group_ids."""

    scanners_in_ag: bool = False
    """Specify 1 to distribute the scan to the target asset groups' scanner appliances. Appliances
    in each asset group are tasked with scanning the IPs in the group. By default up to 5 appliances
    per group will be used"""

    def get_params(self) -> MutableMapping[str, str]:
        """Get the parameters of the object in a format to be ingested by the Qualys API.

        Returns:
            A dictionary of values to be passed to the parms argument of the API request.
        """

        if self.ip and not isinstance(self.ip, MutableSequence):
            self.ip = [self.ip]

        params = {
            "ip": qutils.ips_to_qualys_format(self.ip) if self.ip else None,
            "asset_groups": ",".join(self.asset_groups) if self.asset_groups else None,
            "asset_group_ids": ",".join(self.asset_group_ids)
            if self.asset_group_ids
            else None,
            "exlude_ip_per_scan": qutils.ips_to_qualys_format(self.exlude_ip_per_scan)
            if self.exlude_ip_per_scan
            else None,
            "default_scanner": "1" if self.default_scanner else "0",
            "scanners_in_ag": "1" if self.scanners_in_ag else "0",
        }

        return qutils.remove_nones_from_dict(params)


@dataclasses.dataclass
class Scan_Asset_Tags:
    """A description of the Tags to be scanned."""

    tag_include_selector: str = "any"
    """Select “any” (the default) to include hosts that match
    at least one of the selected tags. Select “all” to include hosts that
    match all of the selected tags.
    """

    tag_exclude_selector: str = "any"
    """Select “any” (the default) to exclude hosts that match
    at least one of the selected tags. Select “all” to exclude hosts that
    match all of the selected tags.
    """

    tag_set_by: str = "id"
    """Specify “id” (the default) to select a tag set by providing tag IDs. Specify “name” to select
    a tag set by providing tag names.
    """

    tag_set_include: Optional[MutableSequence[str]] = None
    """Specify a tag set to include. Hosts that match these tags will be included. You identify the
    tag set by providing tag name or IDs.
    """

    tag_set_exclude: Optional[MutableSequence[str]] = None
    """Specify a tag set to exclude. Hosts that match these tags will be excluded. You identify the
    tag set by providing tag name or IDs.
    """

    use_ip_nt_range_tags_include: bool = False
    """Specify False (the default) to select from all tags (tags with any tag rule). Specify True to
    scan all IP addresses defined in tag selection. When this is specified, only tags with the
    dynamic IP address rule called “IP address in Network Range(s)” can be selected."""

    use_ip_nt_range_tags_exclude: bool = False
    """Specify False (the default) to select from all tags (tags with any tag rule). Specify True to
    exclude all IP addresses defined in tag selection. When this is specified, only tags with the
    dynamic IP address rule called “IP address in Network Range(s)” can be selected.
    """

    scanners_in_tagset: bool = False
    """Specify True to distribute the scan to scanner appliances that match the asset tags specified
    for the scan target.
    """

    def get_params(self) -> MutableMapping[str, str]:
        """Get the parameters of the object in a format to be ingested by the Qualys API.

        Returns:
            A dictionary of values to be passed to the parms argument of the API request.
        """

        params = {
            "tag_include_selector": self.tag_include_selector,
            "tag_exclude_selector": self.tag_exclude_selector,
            "tag_set_by": self.tag_set_by,
            "tag_set_include": ",".join(self.tag_set_include)
            if self.tag_set_include
            else None,
            "tag_set_exclude": ",".join(self.tag_set_exclude)
            if self.tag_set_exclude
            else None,
            "use_ip_nt_range_tags_include": "1"
            if self.use_ip_nt_range_tags_include
            else "0",
            "use_ip_nt_range_tags_exclude": "1"
            if self.use_ip_nt_range_tags_exclude
            else "0",
            "scanners_in_tagset": "1" if self.scanners_in_tagset else "0",
        }

        return qutils.remove_nones_from_dict(params)


def launch_scan(
    conn: qualysapi.Connection,
    scan_assets: Union[Scan_Asset_Ips_Groups, Scan_Asset_Tags],
    scan_title: str = "",
    iscanner_id: Optional[Union[str, MutableSequence[str]]] = None,
    iscanner_name: Optional[Union[str, MutableSequence[str]]] = None,
    option_title: Optional[str] = None,
    option_id: Optional[str] = None,
    priority: int = 0,
    runtime_http_header: Optional[str] = None,
    certview: bool = False,
    fqdn: Optional[Union[str, MutableSequence[str]]] = None,
    include_agent_targets: bool = False,
) -> dict[str, Any]:
    """Launch vulnerability scan in the user's account.

    Notes:
        The Launch Scan API is asynchronous. When you make a request to launch a scan using
        this API, the service will return a scan reference ID right away and the call will quit
        without waiting for the complete scan results.

        When you launch a VM scan using the API, Qualys checks to see if the IPs in the scan target
        are available to the user making the scan request. To determine this, Qualys checks that
        each IP is in the subscription, in the VM license, and in the user's assigned scope. If any
        IP in the target is not available to the user, then it will be skipped from the scan job.

        For example, let's say you specify the IP range 10.10.10.100-10.10.10.120, but IPs
        10.10.10.115 and 10.10.10.120 are not available to you. In this case, Qualys will launch the
        scan on 10.10.10.100-10.10.10.114, 10.10.10.116-10.10.10.119, and skip 10.10.10.115
        and 10.10.10.120.

    Args:
        conn:
            A connection to the Qualys API.
        scan_assets:
            A set of IPs, Groups, or Tags to be scanned.
        scan_title:
             The scan title. This can be a maximum of 2000 characters (ascii).
        iscanner_id:
            The IDs of the scanner appliances to be used.
            Mutually exclusive with iscanner_name.
        iscanner_name:
             The friendly names of the scanner appliances to be used or “External” for external
             scanners.
             Mutually exclusive with iscanner_id.
        option_title:
            The title of the option profile to be used.
            Mutually exclusive with option_id.
        option_id:
            The ID of the option profile to be used.
            Mutually exclusive with option_title.
        priority:
            Specify a value of 0 - 9 to set a
            processing priority level for the scan. When not specified, a value
            of 0 (no priority) is used. Valid values are:
            0 = No Priority (the default)
            1 = Emergency
            2 = Ultimate
            3 = Critical
            4 = Major
            5 = High
            6 = Standard
            7 = Medium
            8 = Minor
            9 = Low
        runtime_http_header:
             Set a custom value in order to drop defenses (such as logging, IPs, etc) when an
             authorized scan is being run. The value you enter will be used in the “Qualys-Scan:”
             header that will be set for many CGI and web application fingerprinting checks. Some
             discovery and web server fingerprinting checks will not use this header.
        certview:
            Launch a CertView type scan.
        fqdn:
            The target FQDN for a vulnerability scan. You must specify at least one target i.e. IPs,
            asset groups or FQDNs.  You can specify FQDNs in combination with IPs and asset
            groups but not with asset tags.
        include_agent_targets:
            Specify True when your scan target includes agent hosts. This lets you scan private IPs
            where agents are installed when these IPs are not in your VM/PC license.  This parameter
            is supported for internal scans using scanner appliance(s). This option is not supported
            for scans using External scanners. This parameter is supported when launching on
            demand scans only. It is not supported for scheduled scans. Parameter iscanner_id or
            iscanner_name must be specified in the same request.

        Returns:
            A dictionary containing the status text of the operation, and the scan ID and reference
            name if the scam was successfully launched.
    """

    if iscanner_id and not isinstance(iscanner_id, str):
        iscanner_id = ",".join(iscanner_id)
    elif iscanner_name and not isinstance(iscanner_name, str):
        iscanner_name = ",".join(iscanner_name)

    params = {
        "scan_title": scan_title,
        "iscanner_id": iscanner_id,
        "iscanner_name": iscanner_name,
        "option_title": option_title,
        "option_id": option_id,
        "priority": str(priority),
        "runtime_http_header": runtime_http_header,
        "certview": "certview" if certview else None,
        "include_agent_targets": "1" if include_agent_targets else 0,
    }
    if isinstance(fqdn, str):
        params["fqdn"] = fqdn
    elif fqdn:
        params["fqdn"] = ",".join(fqdn)

    params.update(scan_assets.get_params())

    raw = conn.post(URLS["Launch VM Scan"], params=params)
    return qutils.parse_simple_return(raw)


def _manage_scan(
    conn: qualysapi.Connection,
    action: str,
    scan_ref: str,
    ips: Optional[
        Union[
            ipaddress.IPv4Address,
            ipaddress.IPv6Address,
            ipaddress.IPv4Network,
            ipaddress.IPv6Network,
            MutableSequence[
                Union[
                    ipaddress.IPv4Address,
                    ipaddress.IPv6Address,
                    ipaddress.IPv4Network,
                    ipaddress.IPv6Network,
                ]
            ],
        ]
    ] = None,
) -> dict[str, Any]:
    """Take actions on vulnerability scans in the user's account, like cancel, pause, resume,
    delete, and fetch completed scan results.

    Args:
        conn:
            A connection to the Qualys API.
        action:
            One action required for the request:
            cancel - Stop a scan in progress
            pause - Stop a scan in progress and change status to “Paused”
            resume - Restart a scan that has been paused
            delete - Delete a scan in your account
        scan_ref:
            Specifies a scan reference. A scan reference has the format “scan/987659876.19876”.
    Returns:
        A dictionary containing the status of the operation.
    """

    params = {
        "scan_ref": scan_ref,
        "ips": qutils.ips_to_qualys_format(ips) if ips else None,
    }
    params = dict(qutils.remove_nones_from_dict(params))

    match action:
        case "cancel":
            raw = conn.post(URLS["Cancel VM Scan"], params)
        case "pause":
            raw = conn.post(URLS["Pause VM Scan"], params)
        case "resume":
            raw = conn.post(URLS["Resume VM Scan"], params)
        case "delete":
            raw = conn.post(URLS["Delete VM Scan"], params)
        case _:
            raise ValueError("unrecognized action")

    return qutils.parse_simple_return(raw)


def cancel_scan(conn: qualysapi.Connection, scan_ref: str) -> dict[str, Any]:
    """Stops a scan in progress.

    Args:
        conn:
            A connection to the Qualys API.
        scan_ref:
            Specifies a scan reference. A scan reference has the format “scan/987659876.19876”.

    Returns:
        A dictionary containing the status of the operation.
    """
    return _manage_scan(conn, "cancel", scan_ref)


def pause_scan(conn: qualysapi.Connection, scan_ref: str) -> dict[str, Any]:
    """Stops a scan in progress and change status to “Paused”.

    Args:
        conn:
            A connection to the Qualys API.
        scan_ref:
            Specifies a scan reference. A scan reference has the format “scan/987659876.19876”.

    Returns:
        A dictionary containing the status of the operation.
    """
    return _manage_scan(conn, "pause", scan_ref)


def resume_scan(conn: qualysapi.Connection, scan_ref: str) -> dict[str, Any]:
    """Restarts a scan that has been paused.

    Args:
        conn:
            A connection to the Qualys API.
        scan_ref:
            Specifies a scan reference. A scan reference has the format “scan/987659876.19876”.

    Returns:
        A dictionary containing the status of the operation.
    """
    return _manage_scan(conn, "resume", scan_ref)


def delete_scan(conn: qualysapi.Connection, scan_ref: str) -> dict[str, Any]:
    """Deletes a scan in your account.

    Args:
        conn:
            A connection to the Qualys API.
        scan_ref:
            Specifies a scan reference. A scan reference has the format “scan/987659876.19876”.

    Returns:
        A dictionary containing the status of the operation.
    """
    return _manage_scan(conn, "delete", scan_ref)


def _fetch_scan(
    conn: qualysapi.Connection,
    scan_ref: str,
    output_file: Union[str, TextIO],
    ips: Optional[
        Union[
            ipaddress.IPv4Address,
            ipaddress.IPv6Address,
            ipaddress.IPv4Network,
            ipaddress.IPv6Network,
            MutableSequence[
                Union[
                    ipaddress.IPv4Address,
                    ipaddress.IPv6Address,
                    ipaddress.IPv4Network,
                    ipaddress.IPv6Network,
                ]
            ],
        ]
    ] = None,
    extended: bool = False,
    output_format: str = "csv",
    post: bool = False,
) -> None:
    """Download scan results for a scan with status of 'Finished', 'Canceled', 'Paused', or
    'Error'

    Args:
        conn:
            A connection to the Qualys API.
        scan_ref:
            Specifies a scan reference. A scan reference has the format “scan/987659876.19876”.
        output_file:
            A file object or path for the API response to be written to.
        ips:
            Show only certain IP addresses/ranges in the scan results.
        extended:
            The verbosity of the scan results
            details: By defaulty, output includes this information: IP address, DNS hostname,
            NetBIOS hostname, QID and scan test results if applicable. The extended output
            includes the brief output plus this extended information:
            protocol, port, an SSL flag (“yes” is returned when SSL was used
            for the detection, “no” is returned when SSL was not used), and
            FQDN if applicable.
        output_format:
            The output format of the
            vulnerability scan results. A valid value is: "csv" (the default) or "json"
            (for JavaScript Object Notation().
        post:
            Run as a POST request.There are known limits for the amount of
            data that can be sent using the GET method, so POST should be used in those cases.
    """

    if extended:
        output_format = output_format + "_extended"

    params = {
        "scan_ref": scan_ref,
        "ips": qutils.ips_to_qualys_format(ips) if ips else None,
        "mode": "extended" if extended else None,
        "output_format": output_format,
    }
    params = dict(qutils.remove_nones_from_dict(params))

    if post:
        conn.post_file(URLS["Fetch VM Scan"], params, output_file)
    else:
        conn.get_file(URLS["Fetch VM Scan"], params, output_file)


def fetch_scan_csv(
    conn: qualysapi.Connection,
    scan_ref: str,
    output_file: Union[str, TextIO],
    ips: Optional[
        Union[
            ipaddress.IPv4Address,
            ipaddress.IPv6Address,
            ipaddress.IPv4Network,
            ipaddress.IPv6Network,
            MutableSequence[
                Union[
                    ipaddress.IPv4Address,
                    ipaddress.IPv6Address,
                    ipaddress.IPv4Network,
                    ipaddress.IPv6Network,
                ]
            ],
        ]
    ] = None,
    extended: bool = False,
    post: bool = False,
) -> None:
    """Download scan results for a scan with status of 'Finished', 'Canceled', 'Paused', or
    'Error' in CSV format.

    Args:
        conn:
            A connection to the Qualys API.
        scan_ref:
            Specifies a scan reference. A scan reference has the format “scan/987659876.19876”.
        output_file:
            A file object or path for the API response to be written to.
        ips:
            Show only certain IP addresses/ranges in the scan results.
        extended:
            The verbosity of the scan results
            details: By defaulty, output includes this information: IP address, DNS hostname,
            NetBIOS hostname, QID and scan test results if applicable. The extended output
            includes the brief output plus this extended information:
            protocol, port, an SSL flag (“yes” is returned when SSL was used
            for the detection, “no” is returned when SSL was not used), and
            FQDN if applicable.
        post:
            Run as a POST request.There are known limits for the amount of
            data that can be sent using the GET method, so POST should be used in those cases.
    """

    _fetch_scan(conn, scan_ref, output_file, ips, extended, "csv", post)


def fetch_scan_json(
    conn: qualysapi.Connection,
    scan_ref: str,
    output_file: Union[str, TextIO],
    ips: Optional[
        Union[
            ipaddress.IPv4Address,
            ipaddress.IPv6Address,
            ipaddress.IPv4Network,
            ipaddress.IPv6Network,
            MutableSequence[
                Union[
                    ipaddress.IPv4Address,
                    ipaddress.IPv6Address,
                    ipaddress.IPv4Network,
                    ipaddress.IPv6Network,
                ]
            ],
        ]
    ] = None,
    extended: bool = False,
    post: bool = False,
) -> None:
    """Download scan results for a scan with status of 'Finished', 'Canceled', 'Paused', or
    'Error' in JSON format.

    Args:
        conn:
            A connection to the Qualys API.
        scan_ref:
            Specifies a scan reference. A scan reference has the format “scan/987659876.19876”.
        output_file:
            A file object or path for the API response to be written to.
        ips:
            Show only certain IP addresses/ranges in the scan results.
        extended:
            The verbosity of the scan results
            details: By defaulty, output includes this information: IP address, DNS hostname,
            NetBIOS hostname, QID and scan test results if applicable. The extended output
            includes the brief output plus this extended information:
            protocol, port, an SSL flag (“yes” is returned when SSL was used
            for the detection, “no” is returned when SSL was not used), and
            FQDN if applicable.
        post:
            Run as a POST request.There are known limits for the amount of
            data that can be sent using the GET method, so POST should be used in those cases.
    """

    _fetch_scan(conn, scan_ref, output_file, ips, extended, "json", post)
