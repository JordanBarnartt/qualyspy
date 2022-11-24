"""Work with option profiles for scans."""

import dataclasses
from collections.abc import MutableSequence
from typing import Optional


@dataclasses.dataclass
class Technologies:
    technology: MutableSequence[str]


@dataclasses.dataclass
class Os_Based_Instance_Disc_Collection:
    technologies: Optional[Technologies] = None


@dataclasses.dataclass
class Authentication_Types_List:
    authentication_type: MutableSequence[str]


@dataclasses.dataclass
class Databases:
    authentication_types_list: Authentication_Types_List


@dataclasses.dataclass
class Instance_Data_Collection:
    databases: Optional[Databases] = None


@dataclasses.dataclass
class Packet_Options:
    ignore_firewall_generated_tcp_rst: Optional[str] = None
    ignore_all_tcp_rst: Optional[str] = None
    ignore_firewall_generated_tcp_syn_ack: Optional[str] = None
    not_send_tcp_ack_or_syn_ack_during_host_discovery: Optional[str] = None


@dataclasses.dataclass
class Block_Resources:
    watchguard_default_blocked_ports: Optional[str] = None
    custom_port_list: Optional[str] = None
    all_registered_ips: Optional[str] = None
    custom_ip_list: Optional[str] = None


@dataclasses.dataclass
class Tcp_Additional:
    has_additional: Optional[str] = None
    additional_ports: Optional[str] = None


@dataclasses.dataclass
class Udp_Ports_Additional:
    has_additional: Optional[str] = None
    additional_ports: Optional[str] = None


@dataclasses.dataclass
class Udp_Ports:
    udp_ports_type: Optional[str] = None
    udp_ports_standard_scan: Optional[str] = None
    udp_ports_additional: Optional[Udp_Ports_Additional] = None
    standard_scan: Optional[str] = None
    custom_port: Optional[str] = None


@dataclasses.dataclass
class Tcp_Ports_Additional:
    has_additional: Optional[str] = None
    additional_ports: Optional[str] = None


@dataclasses.dataclass
class Tcp_Ports:
    tcp_ports_type: Optional[str] = None
    tcp_ports_standard_scan: Optional[str] = None
    tcp_ports_additional: Optional[Tcp_Ports_Additional] = None
    three_way_handshake: Optional[str] = None
    standard_scan: Optional[str] = None
    tcp_additional: Optional[Tcp_Additional] = None


@dataclasses.dataclass
class Ports:
    tcp_ports: Optional[Tcp_Ports] = None
    udp_ports: Optional[Udp_Ports] = None
    authoritative_option: Optional[str] = None
    standard_scan: Optional[str] = None
    targeted_scan: Optional[str] = None


@dataclasses.dataclass
class Host_Discovery:
    tcp_ports: Optional[Tcp_Ports] = None
    udp_ports: Optional[Udp_Ports] = None
    icmp: Optional[str] = None


@dataclasses.dataclass
class Additional:
    host_discovery: Host_Discovery
    block_resources: Optional[Block_Resources] = None
    packet_options: Optional[Packet_Options] = None


@dataclasses.dataclass
class Map_Parallel:
    external_scanners: str
    scanner_appliances: str
    netblock_size: str


@dataclasses.dataclass
class Map_Performance:
    overall_performance: str
    packet_delay: str
    map_parallel: Optional[Map_Parallel] = None


@dataclasses.dataclass
class Map_Options:
    perform_live_host_sweep: Optional[str] = None
    disable_dns_traffic: Optional[str] = None


@dataclasses.dataclass
class Map:
    basic_info_gathering_on: str
    tcp_ports: Optional[Tcp_Ports] = None
    udp_ports: Optional[Udp_Ports] = None
    map_options: Optional[Map_Options] = None
    map_performance: Optional[Map_Performance] = None
    map_authentication: Optional[str] = None


@dataclasses.dataclass
class Control_Types:
    fim_controls_enabled: Optional[str] = None
    custom_wmi_query_checks: Optional[str] = None


@dataclasses.dataclass
class File_Integrity_Monitoring:
    auto_update_expected_value: Optional[str] = None


@dataclasses.dataclass
class Include_System_Auth:
    on_duplicate_use_user_auth: Optional[str] = None
    on_duplicate_use_system_auth: Optional[str] = None


@dataclasses.dataclass
class Custom_Http_Header:
    value: Optional[str] = None
    definition_key: Optional[str] = None
    definition_value: Optional[str] = None


@dataclasses.dataclass
class Oracle_Authentication_Template:
    id: str
    title: str


@dataclasses.dataclass
class Authentication_Type_List:
    authentication_type: MutableSequence[str]


@dataclasses.dataclass
class Allow_Auth_Creation:
    authentication_type_list: Authentication_Type_List
    ibm_was_discovery_mode: Optional[str] = None
    oracle_authentication_template: Optional[Oracle_Authentication_Template] = None


@dataclasses.dataclass
class System_Auth_Record:
    allow_auth_creation: Optional[Allow_Auth_Creation] = None
    include_system_auth: Optional[Include_System_Auth] = None


@dataclasses.dataclass
class Db2:
    db_udc_restriction: str
    db_udc_limit: str


@dataclasses.dataclass
class Sapiq:
    db_udc_restriction: str
    db_udc_limit: str


@dataclasses.dataclass
class Postgresql:
    db_udc_restriction: str
    db_udc_limit: str


@dataclasses.dataclass
class Sybase:
    db_udc_restriction: str
    db_udc_limit: str


@dataclasses.dataclass
class Oracle:
    db_udc_restriction: str
    db_udc_limit: str


@dataclasses.dataclass
class Mssql:
    db_udc_restriction: str
    db_udc_limit: str


@dataclasses.dataclass
class Database_Preference_Key:
    mssql: Optional[Mssql] = None
    oracle: Optional[Oracle] = None
    sybase: Optional[Sybase] = None
    postgresql: Optional[Postgresql] = None
    sapiq: Optional[Sapiq] = None
    db2: Optional[Db2] = None


@dataclasses.dataclass
class Policy:
    id: str
    title: str


@dataclasses.dataclass
class Scan_By_Policy:
    policy: MutableSequence[Policy]


@dataclasses.dataclass
class Scan_Restriction:
    scan_by_policy: Optional[Scan_By_Policy] = None


@dataclasses.dataclass
class Password_Auditing_Enable:
    has_password_auditing_enable: Optional[str] = None
    custom_password_dictionary: Optional[str] = None


@dataclasses.dataclass
class Dissolvable_Agent:
    dissolvable_agent_enable: str
    windows_share_enumeration_enable: str
    password_auditing_enable: Optional[Password_Auditing_Enable] = None
    windows_directory_search_enable: Optional[str] = None


@dataclasses.dataclass
class Custom:
    id: str
    title: str
    type: Optional[str] = None
    login_password: Optional[str] = None


@dataclasses.dataclass
class Custom_List:
    custom: MutableSequence[Custom]


@dataclasses.dataclass
class Detection_Exclude:
    custom_list: MutableSequence[Custom_List]


@dataclasses.dataclass
class Detection_Include:
    basic_host_info_checks: str
    oval_checks: str
    qrdi_checks: Optional[str] = None


@dataclasses.dataclass
class Vulnerability_Detection:
    complete: Optional[str] = None
    custom_list: Optional[Custom_List] = None
    detection_include: Optional[Detection_Include] = None
    detection_exclude: Optional[Detection_Exclude] = None


@dataclasses.dataclass
class System:
    has_system: Optional[str] = None
    system_level: Optional[str] = None


@dataclasses.dataclass
class Password_Brute_Forcing:
    system: Optional[System] = None
    custom_list: Optional[Custom_List] = None


@dataclasses.dataclass
class Processes_To_Run:
    total_processes: str
    http_processes: str


@dataclasses.dataclass
class Hosts_To_Scan:
    external_scanners: str
    scanner_appliances: str


@dataclasses.dataclass
class Performance:
    overall_performance: str
    hosts_to_scan: Hosts_To_Scan
    processes_to_run: Processes_To_Run
    packet_delay: str
    port_scanning_and_host_discovery: str
    parallel_scaling: Optional[str] = None
    external_scanners_to_use: Optional[str] = None
    host_cgi_checks: Optional[str] = None
    max_cgi_checks: Optional[str] = None
    max_targets_per_slice: Optional[str] = None
    max_number_of_targets: Optional[str] = None
    conf_scan_limited_connectivity: Optional[str] = None
    skip_pre_scanning: Optional[str] = None
    scan_multiple_slices_per_scanner: Optional[str] = None


@dataclasses.dataclass
class Close_Vulnerabilities:
    has_close_vulnerabilities: Optional[str] = None
    host_not_found_alive: Optional[str] = None


@dataclasses.dataclass
class Scan:
    ports: Optional[Ports] = None
    scan_dead_hosts: Optional[str] = None
    close_vulnerabilities: Optional[Close_Vulnerabilities] = None
    purge_old_host_os_changed: Optional[str] = None
    performance: Optional[Performance] = None
    load_balancer_detection: Optional[str] = None
    password_brute_forcing: Optional[Password_Brute_Forcing] = None
    vulnerability_detection: Optional[Vulnerability_Detection] = None
    authentication: Optional[str] = None
    authentication_least_privilege: Optional[str] = None
    addl_cert_detection: Optional[str] = None
    dissolvable_agent: Optional[Dissolvable_Agent] = None
    scan_restriction: Optional[Scan_Restriction] = None
    database_preference_key: Optional[Database_Preference_Key] = None
    system_auth_record: Optional[System_Auth_Record] = None
    lite_os_scan: Optional[str] = None
    custom_http_header: Optional[Custom_Http_Header] = None
    host_alive_testing: Optional[str] = None
    ethernet_ip_probing: Optional[str] = None
    file_integrity_monitoring: Optional[File_Integrity_Monitoring] = None
    control_types: Optional[Control_Types] = None
    do_not_overwrite_os: Optional[str] = None
    test_authentication: Optional[str] = None
    max_scan_duration_per_asset: Optional[str] = None


@dataclasses.dataclass
class Option_Profile:
    """An object representing a Qualys Option Profile."""

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

    scan: Scan
    additional: Additional
    is_default: Optional[str] = None
    is_global: Optional[str] = None
    is_offline_syncable: Optional[str] = None
    update_date: Optional[str] = None
    map: Optional[Map] = None
    instance_data_collection: Optional[Instance_Data_Collection] = None
    os_based_instance_disc_collection: Optional[
        Os_Based_Instance_Disc_Collection
    ] = None
