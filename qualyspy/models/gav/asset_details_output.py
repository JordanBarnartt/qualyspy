import datetime
import ipaddress
from typing import Any

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class Model(BaseModel):
    model_config = ConfigDict(validate_by_name=True, alias_generator=to_camel)


class Taxonomy(Model):
    id: int | None
    name: str
    category1: str | None
    category2: str | None


class OperatingSystem(Model):
    os_name: str
    full_name: str
    category: str
    category1: str | None
    category2: str | None
    product_name: str
    publisher: str
    edition: str | None
    market_version: str | None
    version: str | None
    update: str | None
    architecture: str | None
    lifecycle: str | None
    taxonomy: Taxonomy
    product_url: str | None
    product_family: str | None
    install_date: str | None
    release: str | None


class Hardware(Model):
    full_name: str | None
    category: str
    category1: str
    category2: str
    manufacturer: str | None
    product_name: str
    model: str | None
    lifecycle: str | None
    taxonomy: Taxonomy
    product_url: str | None
    product_family: str | None


class UserAccountItem(Model):
    name: str


class UserAccountListData(Model):
    user_account: list[UserAccountItem]


class OpenPortItem(Model):
    port: int
    description: str
    protocol: str
    detected_service: str | None
    first_found: datetime.datetime | None
    last_updated: datetime.datetime | None


class OpenPortListData(Model):
    open_port: list[OpenPortItem]


class VolumeItem(Model):
    name: str
    free: int
    size: int


class VolumeListData(Model):
    volume: list[VolumeItem]


class NetworkInterfaceItem(Model):
    hostname: str | None
    address_ip_v4: list[ipaddress.IPv4Address] | None
    address_ip_v6: list[ipaddress.IPv6Address] | None
    mac_address: str
    interface_name: str
    dns_address: str | None
    gateway_address: str
    manufacturer: str | None
    mac_vendor_intro_date: datetime.datetime | None
    netmask: str | None
    addresses: str | None


class NetworkInterfaceListData(Model):
    network_interface: list[NetworkInterfaceItem]


class SoftwareItem(Model):
    id: int
    full_name: str | None
    software_type: str
    is_ignored: bool
    ignored_reason: str | None
    category: str | None
    category1: str | None
    category2: str | None
    product_name: str | None
    component: str | None
    publisher: str | None
    edition: str | None
    market_version: str | None
    version: str | None
    update: str | None
    architecture: str | None
    install_date: datetime.datetime | None
    install_path: str | None
    last_updated: datetime.datetime | None
    last_use_date: datetime.datetime | None
    language: str | None
    formerly_known_as: str | None
    is_package: bool | None
    is_package_component: bool | None
    package_name: str | None
    product_url: str | None
    lifecycle: str | None
    support_stage_desc: str | None
    license: str | None
    authorization: str | None


class SoftwareListData(Model):
    software: list[SoftwareItem]


class Activation(Model):
    key: str
    status: str


class Oci_Compute(Model):
    oci_id: str
    tenant_id: str | None
    tenant_name: str | None
    compartment_id: str | None
    compartment_name: str | None
    image: str | None
    shape: str | None
    state: str
    region: str | None
    availability_domain: str | None
    fault_domain: str | None
    creation_date: datetime.datetime
    has_agent: bool
    qualys_scanner: bool


class CloudTag(Model):
    key: str
    value: str
    type: str
    name_space: str


class Oci(Model):
    compute: Oci_Compute
    tags: list[CloudTag]


class CloudProvider(Model):
    oci: Oci | None


class Agent(Model):
    version: str | None
    configuration_profile: str | None
    activations: list[Activation] | None
    connected_from: str | None
    last_activity: datetime.datetime
    last_checked_in: datetime.datetime
    last_inventory: datetime.datetime
    udc_manifest_assigned: bool | None
    error_status: bool | None

    def __init__(self, **data: Any) -> None:
        if data["activations"] is None:
            data["activations"] = []
        super().__init__(**data)


class Sensor(Model):
    activated_for_modules: list[str]
    pending_activation_for_modules: list[str] | None
    last_v_m_scan: datetime.datetime
    last_compliance_scan: datetime.datetime
    last_full_scan: datetime.datetime
    last_vm_scan_date_scanner: datetime.datetime
    last_vm_scan_date_agent: datetime.datetime
    last_pc_scan_date_scanner: datetime.datetime
    last_pc_scan_date_agent: datetime.datetime
    first_easm_scan_date: datetime.datetime | None
    last_easm_scan_date: datetime.datetime | None


class Container(Model):
    product: str | None
    version: str | None
    no_of_containers: int
    no_of_images: int
    has_sensor: bool | None


class Inventory(Model):
    source: str
    created: datetime.datetime
    last_updated: datetime.datetime


class Activity(Model):
    source: str
    last_scanned_date: datetime.datetime


class TagItem(Model):
    tag_id: int
    tag_name: str
    foreground_color: int
    background_color: int
    business_impact: str | None
    criticality_score: int | None


class TagList(Model):
    tag: list[TagItem]


class ServiceItem(Model):
    description: str | None
    name: str
    status: str


class ServiceList(Model):
    service: list[ServiceItem]


class LastLocation(Model):
    city: str | None
    state: str | None
    country: str
    name: str
    continent: str
    postal: str | None


class Criticality(Model):
    score: int
    is_default: bool
    last_updated: datetime.datetime | None


class Processor(Model):
    description: str | None
    speed: int | None
    numCPUs: int | None
    no_of_socket: int | None
    threads_per_core: int | None
    cores_per_socket: int | None
    multithreading_status: str | None


class AssetItem(Model):
    asset_id: int
    assetUUID: str | None
    host_id: int | None
    last_modified_date: datetime.datetime
    agent_id: str | None
    created_date: datetime.datetime
    sensor_last_updated_date: datetime.datetime
    asset_type: str | None
    address: ipaddress.IPv4Address | ipaddress.IPv6Address
    dns_name: str | None
    asset_name: str
    netbios_name: str | None
    time_zone: str | None
    bios_description: str | None
    last_boot: datetime.datetime | None
    total_memory: int | None
    cpu_count: int | None
    last_logged_on_user: str | None
    domain_role: str | None
    hwUUID: str | None
    bios_serial_number: str | None
    bios_asset_tag: str | None
    is_container_host: bool
    operating_system: OperatingSystem
    hardware: Hardware
    user_account_list_data: UserAccountListData | None
    open_port_list_data: OpenPortListData | None
    volume_list_data: VolumeListData | None
    network_interface_list_data: NetworkInterfaceListData | None
    software_list_data: SoftwareListData | None
    provider: str | None
    cloud_provider: CloudProvider | None
    agent: Agent | None
    sensor: Sensor
    container: Container | None
    inventory: Inventory
    activity: Activity
    tag_list: TagList | None
    service_list: ServiceList | None
    last_location: LastLocation | None
    criticality: Criticality
    business_information: str | None
    assigned_location: str | None
    business_app_list_data: str | None
    risk_score: int | None
    passive_sensor: str | None
    domain: list[str] | None
    subdomain: list[str] | None
    whois: list[str] | None
    isp: str | None
    asn: str | None
    easm_tags: str | None
    hosting_category1: str | None
    custom_attributes: str | None
    processor: Processor | None


class AssetListData(Model):
    asset: list[AssetItem]


class AssetDetailsOutput(Model):
    response_message: str
    count: int
    response_code: str
    last_seen_asset_id: int | None
    has_more: int
    asset_list_data: AssetListData
