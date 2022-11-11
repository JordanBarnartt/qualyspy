"""Work with option profiles for scans."""

import dataclasses
import datetime
from collections.abc import MutableSequence
from typing import Any, Optional


@dataclasses.dataclass
class Scan_TCP_Ports:
    """A set of TCP ports to be scanned in an option profile."""

    tcp_ports_type: Optional[str] = ""
    """TCP ports type, one of: "standard" (for standard scan, about 1900 TCP ports),
        "light" (for light scan, about 160 TCP ports), "none" (for no TCP ports), "full" (for
        all TCP ports).
    """

    additional_ports: Optional[MutableSequence[str]] = []
    """List of additional TCP ports to be scanned."""

    three_way_handshake: Optional[bool] = None
    """True means scans will perform 3-way handshake with target hosts (performed
        only when you have a configuration that does not allow SYN packet to be
        followed by RST packet); False means scans will not perform 3-way handshake.
    """

    def __post_init__(self) -> None:
        self._check_parameters()

    def __setattr__(self, __name: str, __value: Any) -> None:
        super().__setattr__(__name, __value)
        self._check_parameters()

    def _check_parameters(self) -> None:
        """Confirms that any value with additional restrictions meets those restrictions."""

        good_tcp_port_types = {None, "standard", "light", "none", "full"}

        if self.tcp_ports_type:
            for state in self.tcp_ports_type:
                if state not in good_tcp_port_types:
                    raise ValueError(f"{state} not one of {good_tcp_port_types}")


@dataclasses.dataclass
class Scan_UDP_Ports:
    """A set of UDP ports to be scanned in an option profile."""

    udp_ports_type: Optional[str]
    """UDP ports type, one of: "standard" (for standard scan, about 180 UDP ports),
        "light" (for light scan, about 30 UDP ports), "none" (for no UDP ports), "full" (for
        all UDP ports).
    """

    additional_ports: Optional[MutableSequence[str]]
    """List of additional UDP ports to be scanned."""

    def __post_init__(self) -> None:
        self._check_parameters()

    def __setattr__(self, __name: str, __value: Any) -> None:
        super().__setattr__(__name, __value)
        if __name == "udp_ports_type":
            self._check_parameters()

    def _check_parameters(self) -> None:
        """Confirms that any value with additional restrictions meets those restrictions."""

        good_udp_port_types = {None, "standard", "light", "none", "full"}

        if self.udp_ports_type:
            for state in self.udp_ports_type:
                if state not in good_udp_port_types:
                    raise ValueError(f"{state} not one of {good_udp_port_types}")


@dataclasses.dataclass
class Option_Profile_Scan:
    """A definition of the scan settings for an Option_Profile."""

    tcp_ports: Optional[Scan_TCP_Ports] = None
    """TCP ports to be scanned."""

    udp_ports: Optional[Scan_UDP_Ports] = None
    """UDP ports to be scanned."""

    authoritative_option: Optional[bool] = None
    """(VM only) False means for partial port scans Qualys will update the status for all
        vulnerabilities found regardless of which ports they are found on; True
        means for partial scans Qualys will update the status of vulnerabilities detected
        by ports scanned.
    """

    standard_scan: Optional[bool] = None
    """(PC only) True means standard port scan is enabled for Windows and Unix
        scans; False means standard port scan is disabled. Standard scan includes well known
        ports: 22 (SSH), 23 (telnet) and 513 (rlogin).\n
        Note: STANDARD_SCAN or TARGETED_SCAN must be enabled, and these
        settings are mutually exclusive.
    """

    targeted_scan: Optional[bool] = None
    """(PC only) A targeted port scan, defined by a custom list of ports, is enabled
        for Windows and Unix; False means targeted port scan is disabled.\n
        Note: STANDARD_SCAN or TARGETED_SCAN must be enabled, and these
        settings are mutually exclusive.
    """

    scan_dead_hosts: Optional[bool] = None
    """(VM only) True means Qualys will scan dead hosts (this may increase scan time);
        False means Qualys won't scan dead hosts.
        """

    has_close_vulnerabilities: Optional[bool] = None
    """(VM only) True means Qualys will close vulnerabilities on dead hosts during scan
        processing (vulnerability status will be set to Fixed, and existing tickets will
        be marked Closed/Fixed); False means Qualys won't close vulnerabilities on dead
        hosts. This option is valid only when the “Close vulnerabilities on dead
        hosts” feature is enabled for your subscription by Qualys Support or your
        Qualys Account Manager.
    """

    host_not_found_alive: Optional[bool] = None
    """(VM only) True means scans will perform host alive testing before
        vulnerability testing (only hosts found alive will be tested for
        vulnerabilities); False means scans won't perform host alive testing.
    """

    purge_old_host_os_changed: Optional[bool] = None
    """(VM only) True means Qualys will purge hosts when OS is changed during scan
         False means Qualys won't purge hosts when OS is changed.
    """

    def __post_init__(self) -> None:
        self._check_parameters()

    def __setattr__(self, __name: str, __value: Any) -> None:
        super().__setattr__(__name, __value)
        if __name == "standard_scan" or __name == "targetted_scan":
            self._check_parameters()

    def _check_parameters(self) -> None:
        if not self.standard_scan and not self.targeted_scan:
            raise ValueError("one of standard_scan or targetted_scan must be True.")
        elif self.standard_scan and self.targeted_scan:
            raise ValueError("standard_scan and targeted_scan cannot both be True.")


@dataclasses.dataclass
class Option_Profile:
    """An object represeting an option profile used with a scan."""

    id: str
    """Option profile ID."""

    group_name: str
    """Option profile title."""

    group_type: str
    """Option profile group name/type, e.g. user (for user defined), compliance (for
            compliance profile), pci (for PCI vulnerabilities profile), rv10 (for Qualys Top
            10 real time internal and external vulnerabilities, sans20 (for SANS Top 20
            profile).
    """

    user_id: str
    """User ID of the option profile owner."""

    unit_id: str
    """ID of business unit where option profile is defined."""

    subscription_id: str
    """ID of subscription where option profile is defined."""

    is_default: bool
    """True means the option profile is the default for the subscription, False means the
            option profile is not the default"""

    is_global: bool
    """1 means the option profile is a global profile, 0 means the option profile is
            not global."""

    is_offline_syncable: bool
    """(VM only) False means the option profile will be downloaded to your offline
            scanners during the next sync with the platform; True means the profile will
            not be downloaded to offline scanners during the next sync.
            (Only applies to Offline Scanner Appliance)
    """

    update_date: Optional[datetime.datetime]
    """Date when option profile was last updated. None if the profile has
            not been updated after creation.
    """

    parallel_scanning: Optional[bool]
    """(VM only) True means parallel scaling for scanner appliances is enabled; False
        means parallel scaling for scanner appliances is disabled.
    """

    