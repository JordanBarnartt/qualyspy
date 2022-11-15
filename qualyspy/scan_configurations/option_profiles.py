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
class Scan_Performance:
    """Performance options for an option profile."""

    parallel_scaling: Optional[bool] = None
    """(VM only) True means parallel scaling for scanner appliances is enabled; False
        means parallel scaling for scanner appliances is disabled.
    """

    overall_performance: str = "Normal"
    """Overall scan performance level, one of:
        "Normal" - Recommended in most cases, well balanced between intensity
        and speed.
        "High" - Recommended only when scanning a single IP or small number of
        IPs, optimized for speed and shorter scan times.
        "Low" - Recommended if responsiveness for individual hosts and services is
        low, optimized for low bandwidth network connections and highly utilized
        networks. May take longer to complete.
    """

    hosts_to_scan_external: int = 1
    """Maximum number of hosts to scan in parallel using Qualys cloud (external)
        scanners.
    """

    hosts_to_scan_appliances: int = 1
    """Maximum number of hosts to scan in parallel using Qualys Scanner
        Appliances, installed on your internal network.
    """

    processes_to_run_total: int = 1
    """Maximum number of total processes to run at the same time per host."""

    processes_to_run_http: int = 1
    """Maximum number of HTTP processes to run at the same time per host."""

    packet_delay: int = 1
    """The delay between groups of packets sent to each host during a scan."""

    def __post_init__(self) -> None:
        self._check_parameters()

    def __setattr__(self, __name: str, __value: Any) -> None:
        super().__setattr__(__name, __value)
        if __name == "overall_performance":
            self._check_parameters()

    def _check_parameters(self) -> None:
        """Confirms that any value with additional restrictions meets those restrictions."""

        good_overall_performances = ["Normal", "High", "Low"]

        if self.overall_performance not in good_overall_performances:
            raise ValueError(
                f"overall_performance: {self.overall_performance} "
                f"not one of {good_overall_performances}"
            )


@dataclasses.dataclass
class Scan_Password_Brute_Forcing_Custom:
    """Settings for a custom password brute force scan.

    Warning:
        An Import Option Profile API call does not import custom password
        brute forcing lists regardless of Option Profile XML file content. Please
        configure using Qualys portal UI."""

    id: str
    """(VM only) Custom password brute forcing list ID."""

    title: str
    """(VM only) Custom password brute forcing list title."""

    type_: str
    """(VM only) Type of custom password brute forcing list, one of: "ftp", "ssh", "windows"."""

    login_password: MutableSequence[str]
    """(VM only) Login/password list (maximum 50) for custom password brute
        forcing list."""

    def __post_init__(self) -> None:
        self._check_parameters()

    def __setattr__(self, __name: str, __value: Any) -> None:
        super().__setattr__(__name, __value)
        if __name == "type_" or __name == "login_password":
            self._check_parameters()

    def _check_parameters(self) -> None:
        """Confirms that any value with additional restrictions meets those restrictions."""

        good_types = ["ftp", "ssh", "windows"]
        if self.type_ not in good_types:
            raise ValueError(f"type: {self.type_} not one of {good_types}")

        if len(self.login_password) > 50:
            raise ValueError(
                f"length of login_password is {len(self.login_password)}; maximum 50"
            )


@dataclasses.dataclass
class Scan_Password_Brute_Forcing:
    """Password brute forcing settings in an options profile."""

    has_system: Optional[bool] = None
    """(VM only) True means system password brute forcing enabled; False means system
        password brute forcing is not enabled."""

    system_level: Optional[int] = 3
    """(VM only) System password brute forcing level, one of: 1 (for minimal,
        empty passwords), 2 (for Limited), 3 (for Standard, up to 60 per login ID), 4
        (for Exhaustive)."""

    custom_list: MutableSequence[Scan_Password_Brute_Forcing_Custom] = []
    """"""

    def __post_init__(self) -> None:
        self._check_parameters()

    def __setattr__(self, __name: str, __value: Any) -> None:
        super().__setattr__(__name, __value)
        if __name == "system_level":
            self._check_parameters()

    def _check_parameters(self) -> None:
        """Confirms that any value with additional restrictions meets those restrictions."""

        good_system_levels = [1, 2, 3, 4]

        if self.system_level not in good_system_levels:
            raise ValueError(
                f"system_level: {self.system_level} not one of {good_system_levels}"
            )


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

    performance: Optional[Scan_Performance] = None
    """Performance options for an option profile."""

    port_scanning_and_host_discovery: str = "Normal"
    """(VM only) The aggressiveness (parallelism) of port scanning and host
        discovery at the port level: "Normal", "Medium", "Low" or "Minimum". Lowering
        the intensity level has the effect of serializing port scanning and host
        discovery."""

    load_balancer_detection: bool = True
    """(VM only) True means scans will detect load balancers and report in QID
        86189” False means scans will not detect load balancers."""

    def __post_init__(self) -> None:
        self._check_parameters()

    def __setattr__(self, __name: str, __value: Any) -> None:
        super().__setattr__(__name, __value)
        if (
            __name == "standard_scan"
            or __name == "targetted_scan"
            or __name == "port_scanning_and_host_discovery"
        ):
            self._check_parameters()

    def _check_parameters(self) -> None:
        if not self.standard_scan and not self.targeted_scan:
            raise ValueError("one of standard_scan or targetted_scan must be True.")
        elif self.standard_scan and self.targeted_scan:
            raise ValueError("standard_scan and targeted_scan cannot both be True.")

        good_port_scanning_and_host_discoveries = ["Normal", "Medium", "Low", "Minimum"]
        if (
            self.port_scanning_and_host_discovery
            not in good_port_scanning_and_host_discoveries
        ):
            raise ValueError(
                f"port_scanning_and_host_discovery: {self.port_scanning_and_host_discovery} not "
                f"one of {good_port_scanning_and_host_discoveries}"
            )


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
