import datetime as dt
import ipaddress

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as sa_pg
import sqlalchemy.orm as orm

from .. import sa_types


class Base(orm.DeclarativeBase):
    metadata = sa.MetaData(schema="qualys_asset_details")


class OperatingSystemTaxonomy(Base):
    __tablename__ = "operating_system_taxonomy"

    pk: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    id: orm.Mapped[int | None]
    name: orm.Mapped[str]
    category1: orm.Mapped[str | None]
    category2: orm.Mapped[str | None]

    operating_system_id: orm.Mapped[int | None] = orm.mapped_column(
        sa.ForeignKey("operating_system.id")
    )
    operating_system: orm.Mapped["OperatingSystem | None"] = orm.relationship(
        back_populates="taxonomy"
    )


class HardwareTaxonomy(Base):
    __tablename__ = "hardware_taxonomy"

    pk: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    id: orm.Mapped[int | None]
    name: orm.Mapped[str]
    category1: orm.Mapped[str | None]
    category2: orm.Mapped[str | None]

    hardware_id: orm.Mapped[int | None] = orm.mapped_column(
        sa.ForeignKey("hardware.id")
    )
    hardware: orm.Mapped["Hardware | None"] = orm.relationship(
        back_populates="taxonomy"
    )


class OperatingSystem(Base):
    __tablename__ = "operating_system"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    os_name: orm.Mapped[str]
    full_name: orm.Mapped[str]
    category: orm.Mapped[str]
    category1: orm.Mapped[str | None]
    category2: orm.Mapped[str | None]
    product_name: orm.Mapped[str]
    publisher: orm.Mapped[str]
    edition: orm.Mapped[str | None]
    market_version: orm.Mapped[str | None]
    version: orm.Mapped[str | None]
    update: orm.Mapped[str | None]
    architecture: orm.Mapped[str | None]
    lifecycle: orm.Mapped[str | None]
    taxonomy: orm.Mapped[OperatingSystemTaxonomy] = orm.relationship(
        back_populates="operating_system", uselist=False
    )
    product_url: orm.Mapped[str | None]
    product_family: orm.Mapped[str | None]
    install_date: orm.Mapped[str | None]
    release: orm.Mapped[str | None]

    asset_item_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("asset_item.asset_id")
    )
    asset_item: orm.Mapped["AssetItem"] = orm.relationship(
        back_populates="operating_system"
    )


class Hardware(Base):
    __tablename__ = "hardware"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    full_name: orm.Mapped[str | None]
    category: orm.Mapped[str]
    category1: orm.Mapped[str]
    category2: orm.Mapped[str]
    manufacturer: orm.Mapped[str | None]
    product_name: orm.Mapped[str]
    model: orm.Mapped[str | None]
    lifecycle: orm.Mapped[str | None]
    taxonomy: orm.Mapped[HardwareTaxonomy] = orm.relationship(
        back_populates="hardware", uselist=False
    )
    product_url: orm.Mapped[str | None]
    product_family: orm.Mapped[str | None]
    asset_item_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("asset_item.asset_id")
    )
    asset_item: orm.Mapped["AssetItem"] = orm.relationship(back_populates="hardware")


class UserAccountItem(Base):
    __tablename__ = "user_account_item"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    name: orm.Mapped[str] = orm.mapped_column()

    user_account_list_data_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("user_account_list_data.id")
    )
    user_account_list_data: orm.Mapped["UserAccountListData"] = orm.relationship(
        back_populates="user_account"
    )


class UserAccountListData(Base):
    __tablename__ = "user_account_list_data"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    user_account: orm.Mapped[list[UserAccountItem]] = orm.relationship(
        back_populates="user_account_list_data"
    )

    asset_item_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("asset_item.asset_id")
    )
    asset_item: orm.Mapped["AssetItem"] = orm.relationship(
        back_populates="user_account_list_data"
    )


class OpenPortItem(Base):
    __tablename__ = "open_port_item"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    port: orm.Mapped[int]
    description: orm.Mapped[str | None]
    protocol: orm.Mapped[str]
    detected_service: orm.Mapped[str | None]
    first_found: orm.Mapped[dt.datetime | None]
    last_updated: orm.Mapped[dt.datetime | None]

    open_port_list_data_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("open_port_list_data.id")
    )
    open_port_list_data: orm.Mapped["OpenPortListData"] = orm.relationship(
        back_populates="open_port"
    )


class OpenPortListData(Base):
    __tablename__ = "open_port_list_data"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    open_port: orm.Mapped[list[OpenPortItem]] = orm.relationship(
        back_populates="open_port_list_data"
    )

    asset_item_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("asset_item.asset_id")
    )
    asset_item: orm.Mapped["AssetItem"] = orm.relationship(
        back_populates="open_port_list_data"
    )


class VolumeItem(Base):
    __tablename__ = "volume_item"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    name: orm.Mapped[str]
    free: orm.Mapped[str]
    size: orm.Mapped[str]

    volume_list_data_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("volume_list_data.id")
    )
    volume_list_data: orm.Mapped["VolumeListData"] = orm.relationship(
        back_populates="volume"
    )


class VolumeListData(Base):
    __tablename__ = "volume_list_data"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    volume: orm.Mapped[list[VolumeItem]] = orm.relationship(
        back_populates="volume_list_data"
    )

    asset_item_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("asset_item.asset_id")
    )
    asset_item: orm.Mapped["AssetItem"] = orm.relationship(
        back_populates="volume_list_data"
    )


class NetworkInterfaceItem(Base):
    __tablename__ = "network_interface_item"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    hostname: orm.Mapped[str | None]
    address_ip_v4: orm.Mapped[ipaddress.IPv4Address | None] = orm.mapped_column(
        "address_ip_v4", sa_types.IPv4AddressType
    )
    address_ip_v6: orm.Mapped[ipaddress.IPv6Address | None] = orm.mapped_column(
        "address_ip_v6", sa_types.IPv6AddressType
    )
    mac_address: orm.Mapped[str]
    interface_name: orm.Mapped[str]
    dns_address: orm.Mapped[str | None]
    gateway_address: orm.Mapped[str]
    manufacturer: orm.Mapped[str | None]
    mac_vendor_intro_date: orm.Mapped[dt.datetime | None]
    netmask: orm.Mapped[str | None]
    addresses: orm.Mapped[str | None]

    network_interface_list_data_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("network_interface_list_data.id")
    )
    network_interface_list_data: orm.Mapped["NetworkInterfaceListData"] = (
        orm.relationship(back_populates="network_interface")
    )


class NetworkInterfaceListData(Base):
    __tablename__ = "network_interface_list_data"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    network_interface: orm.Mapped[list[NetworkInterfaceItem]] = orm.relationship(
        back_populates="network_interface_list_data"
    )

    asset_item_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("asset_item.asset_id")
    )
    asset_item: orm.Mapped["AssetItem"] = orm.relationship(
        back_populates="network_interface_list_data"
    )


class SoftwareItem(Base):
    __tablename__ = "software_item"

    orm_id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    id: orm.Mapped[str]
    full_name: orm.Mapped[str | None]
    software_type: orm.Mapped[str]
    is_ignored: orm.Mapped[bool]
    ignored_reason: orm.Mapped[str | None]
    category: orm.Mapped[str | None]
    category1: orm.Mapped[str | None]
    category2: orm.Mapped[str | None]
    product_name: orm.Mapped[str | None]
    component: orm.Mapped[str | None]
    publisher: orm.Mapped[str | None]
    edition: orm.Mapped[str | None]
    market_version: orm.Mapped[str | None]
    version: orm.Mapped[str | None]
    update: orm.Mapped[str | None]
    architecture: orm.Mapped[str | None]
    install_date: orm.Mapped[dt.datetime | None]
    install_path: orm.Mapped[str | None]
    last_updated: orm.Mapped[dt.datetime | None]
    last_use_date: orm.Mapped[dt.datetime | None]
    language: orm.Mapped[str | None]
    formerly_known_as: orm.Mapped[str | None]
    is_package: orm.Mapped[bool | None]
    is_package_component: orm.Mapped[bool | None]
    package_name: orm.Mapped[str | None]
    product_url: orm.Mapped[str | None]
    lifecycle: orm.Mapped[str | None]
    support_stage_desc: orm.Mapped[str | None]
    license: orm.Mapped[str | None]
    authorization: orm.Mapped[str | None]

    software_list_data_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("software_list_data.id")
    )
    software_list_data: orm.Mapped["SoftwareListData"] = orm.relationship(
        back_populates="software"
    )


class SoftwareListData(Base):
    __tablename__ = "software_list_data"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    software: orm.Mapped[list[SoftwareItem]] = orm.relationship(
        back_populates="software_list_data"
    )

    asset_item_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("asset_item.asset_id")
    )
    asset_item: orm.Mapped["AssetItem"] = orm.relationship(
        back_populates="software_list_data"
    )


class Activation(Base):
    __tablename__ = "activation"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    key: orm.Mapped[str]
    status: orm.Mapped[str]

    agent_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("agent.id"))
    agent: orm.Mapped["Agent"] = orm.relationship(back_populates="activations")


class Oci_Compute(Base):
    __tablename__ = "oci_compute"

    oci_id: orm.Mapped[str] = orm.mapped_column(primary_key=True)
    tenant_id: orm.Mapped[str | None]
    tenant_name: orm.Mapped[str | None]
    compartment_id: orm.Mapped[str | None]
    compartment_name: orm.Mapped[str | None]
    image: orm.Mapped[str | None]
    shape: orm.Mapped[str | None]
    state: orm.Mapped[str]
    region: orm.Mapped[str | None]
    availability_domain: orm.Mapped[str | None]
    fault_domain: orm.Mapped[str | None]
    creation_date: orm.Mapped[dt.datetime]
    has_agent: orm.Mapped[bool]
    qualys_scanner: orm.Mapped[bool]

    oci_parent_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("oci.id"))
    oci_parent: orm.Mapped["Oci"] = orm.relationship(back_populates="compute")


class CloudTag(Base):
    __tablename__ = "cloud_tag"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    key: orm.Mapped[str]
    value: orm.Mapped[str]
    type: orm.Mapped[str]
    name_space: orm.Mapped[str]

    oci_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("oci.id"))
    oci: orm.Mapped["Oci"] = orm.relationship(back_populates="tags")


class Oci(Base):
    __tablename__ = "oci"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    compute: orm.Mapped[list[Oci_Compute]] = orm.relationship(
        "Oci_Compute", back_populates="oci_parent", uselist=False
    )
    tags: orm.Mapped[list[CloudTag]] = orm.relationship(
        "CloudTag", back_populates="oci"
    )

    cloud_provider_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("cloud_provider.id")
    )
    cloud_provider: orm.Mapped["Cloud_Provider"] = orm.relationship(
        back_populates="oci"
    )


class Cloud_Provider(Base):
    __tablename__ = "cloud_provider"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    oci: orm.Mapped[Oci] = orm.relationship(
        "Oci", back_populates="cloud_provider", uselist=False
    )

    asset_item_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("asset_item.asset_id")
    )
    asset_item: orm.Mapped["AssetItem"] = orm.relationship(
        back_populates="cloud_provider"
    )


class Agent(Base):
    __tablename__ = "agent"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    version: orm.Mapped[str | None]
    configuration_profile: orm.Mapped[str | None]
    activations: orm.Mapped[list[Activation]] = orm.relationship(
        "Activation", back_populates="agent"
    )
    connected_from: orm.Mapped[str | None]
    last_activity: orm.Mapped[dt.datetime]
    last_checked_in: orm.Mapped[dt.datetime]
    last_inventory: orm.Mapped[dt.datetime]
    udc_manifest_assigned: orm.Mapped[bool | None]
    error_status: orm.Mapped[bool | None]

    asset_item_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("asset_item.asset_id")
    )
    asset_item: orm.Mapped["AssetItem"] = orm.relationship(back_populates="agent")


class Sensor(Base):
    __tablename__ = "sensor"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    activated_for_modules: orm.Mapped[list[str]] = orm.mapped_column(
        sa_pg.ARRAY(sa.String)
    )
    pending_activation_for_modules: orm.Mapped[list[str] | None] = orm.mapped_column(
        sa_pg.ARRAY(sa.String)
    )
    last_v_m_scan: orm.Mapped[dt.datetime]
    last_compliance_scan: orm.Mapped[dt.datetime]
    last_full_scan: orm.Mapped[dt.datetime]
    last_vm_scan_date_scanner: orm.Mapped[dt.datetime]
    last_vm_scan_date_agent: orm.Mapped[dt.datetime]
    last_pc_scan_date_scanner: orm.Mapped[dt.datetime]
    last_pc_scan_date_agent: orm.Mapped[dt.datetime]
    first_easm_scan_date: orm.Mapped[dt.datetime | None]
    last_easm_scan_date: orm.Mapped[dt.datetime | None]

    asset_item_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("asset_item.asset_id")
    )
    asset_item: orm.Mapped["AssetItem"] = orm.relationship(back_populates="sensor")


class Inventory(Base):
    __tablename__ = "inventory"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    source: orm.Mapped[str]
    created: orm.Mapped[dt.datetime]
    last_updated: orm.Mapped[dt.datetime]

    asset_item_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("asset_item.asset_id")
    )
    asset_item: orm.Mapped["AssetItem"] = orm.relationship(back_populates="inventory")


class Container(Base):
    __tablename__ = "container"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    product: orm.Mapped[str | None]
    version: orm.Mapped[str | None]
    no_of_containers: orm.Mapped[int]
    no_of_images: orm.Mapped[int]
    has_sensor: orm.Mapped[bool | None]

    asset_item_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("asset_item.asset_id")
    )
    asset_item: orm.Mapped["AssetItem"] = orm.relationship(back_populates="container")


class Activity(Base):
    __tablename__ = "activity"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    source: orm.Mapped[str]
    last_scanned_date: orm.Mapped[dt.datetime]

    asset_item_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("asset_item.asset_id")
    )
    asset_item: orm.Mapped["AssetItem"] = orm.relationship(back_populates="activity")


taglist_tagitem_association_table = sa.Table(
    "taglist_tagitem",
    Base.metadata,
    sa.Column("taglist_id", sa.Integer, sa.ForeignKey("tag_list.id"), primary_key=True),
    sa.Column(
        "tagitem_id", sa.Integer, sa.ForeignKey("tag_item.tag_id"), primary_key=True
    ),
)


class TagItem(Base):
    __tablename__ = "tag_item"

    tag_id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    tag_name: orm.Mapped[str]
    foreground_color: orm.Mapped[int]
    background_color: orm.Mapped[int]
    business_impact: orm.Mapped[str | None]
    criticality_score: orm.Mapped[int | None]

    tag_list: orm.Mapped[list["TagList"]] = orm.relationship(
        secondary=taglist_tagitem_association_table, back_populates="tag"
    )


class TagList(Base):
    __tablename__ = "tag_list"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    tag: orm.Mapped[list[TagItem]] = orm.relationship(
        secondary=taglist_tagitem_association_table, back_populates="tag_list"
    )

    asset_item_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("asset_item.asset_id")
    )
    asset_item: orm.Mapped["AssetItem"] = orm.relationship(back_populates="tag_list")


class ServiceItem(Base):
    __tablename__ = "service_item"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    description: orm.Mapped[str | None]
    name: orm.Mapped[str]
    status: orm.Mapped[str]

    service_list_id = orm.mapped_column(sa.ForeignKey("service_list.id"))
    service_list: orm.Mapped["ServiceList"] = orm.relationship(
        "ServiceList", back_populates="service"
    )


class ServiceList(Base):
    __tablename__ = "service_list"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    service: orm.Mapped[list[ServiceItem]] = orm.relationship(
        "ServiceItem", back_populates="service_list"
    )

    asset_item_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("asset_item.asset_id")
    )
    asset_item: orm.Mapped["AssetItem"] = orm.relationship(
        back_populates="service_list"
    )


class LastLocation(Base):
    __tablename__ = "last_location"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    city: orm.Mapped[str | None]
    state: orm.Mapped[str | None]
    country: orm.Mapped[str]
    name: orm.Mapped[str]
    continent: orm.Mapped[str]
    postal: orm.Mapped[str | None]

    asset_item_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("asset_item.asset_id")
    )
    asset_item: orm.Mapped["AssetItem"] = orm.relationship(
        back_populates="last_location"
    )


class Criticality(Base):
    __tablename__ = "criticality"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    score: orm.Mapped[int]
    is_default: orm.Mapped[bool]
    last_updated: orm.Mapped[dt.datetime | None]

    asset_item_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("asset_item.asset_id")
    )
    asset_item: orm.Mapped["AssetItem"] = orm.relationship(back_populates="criticality")


class Processor(Base):
    __tablename__ = "processor"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    description: orm.Mapped[str | None]
    speed: orm.Mapped[int | None]
    numCPUs: orm.Mapped[int | None]
    no_of_socket: orm.Mapped[int | None]
    threads_per_core: orm.Mapped[int | None]
    cores_per_socket: orm.Mapped[int | None]
    multithreading_status: orm.Mapped[str | None]

    asset_item_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("asset_item.asset_id")
    )
    asset_item: orm.Mapped["AssetItem"] = orm.relationship(back_populates="processor")


class AssetItem(Base):
    __tablename__ = "asset_item"

    asset_id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    assetUUID: orm.Mapped[str]
    host_id: orm.Mapped[int | None]
    last_modified_date: orm.Mapped[dt.datetime]
    agent_id: orm.Mapped[str | None]
    created_date: orm.Mapped[dt.datetime]
    sensor_last_updated_date: orm.Mapped[dt.datetime]
    asset_type: orm.Mapped[str | None]
    address: orm.Mapped[ipaddress.IPv4Address | ipaddress.IPv6Address] = (
        orm.mapped_column("address", sa_types.IPAddressGenericType)
    )
    dns_name: orm.Mapped[str | None]
    asset_name: orm.Mapped[str]
    netbios_name: orm.Mapped[str | None]
    time_zone: orm.Mapped[str | None]
    bios_description: orm.Mapped[str | None]
    last_boot: orm.Mapped[dt.datetime | None]
    total_memory: orm.Mapped[int | None]
    cpu_count: orm.Mapped[int | None]
    last_logged_on_user: orm.Mapped[str | None]
    domain_role: orm.Mapped[str | None]
    hwUUID: orm.Mapped[str | None]
    bios_serial_number: orm.Mapped[str | None]
    bios_asset_tag: orm.Mapped[str | None]
    is_container_host: orm.Mapped[bool | None]
    operating_system: orm.Mapped[OperatingSystem] = orm.relationship(
        back_populates="asset_item", uselist=False
    )
    hardware: orm.Mapped[Hardware] = orm.relationship(
        back_populates="asset_item", uselist=False
    )
    user_account_list_data: orm.Mapped[UserAccountListData] = orm.relationship(
        back_populates="asset_item", uselist=False
    )
    open_port_list_data: orm.Mapped[OpenPortListData] = orm.relationship(
        back_populates="asset_item", uselist=False
    )
    volume_list_data: orm.Mapped[VolumeListData] = orm.relationship(
        back_populates="asset_item", uselist=False
    )
    network_interface_list_data: orm.Mapped[NetworkInterfaceListData | None] = (
        orm.relationship(back_populates="asset_item", uselist=False)
    )
    software_list_data: orm.Mapped[SoftwareListData] = orm.relationship(
        back_populates="asset_item", uselist=False
    )
    provider: orm.Mapped[str | None]
    cloud_provider: orm.Mapped[Cloud_Provider | None] = orm.relationship(
        back_populates="asset_item", uselist=False
    )
    agent: orm.Mapped[Agent | None] = orm.relationship(
        back_populates="asset_item", uselist=False
    )
    sensor: orm.Mapped[Sensor] = orm.relationship(
        back_populates="asset_item", uselist=False
    )
    container: orm.Mapped[Container | None] = orm.relationship(
        back_populates="asset_item", uselist=False
    )
    inventory: orm.Mapped[Inventory] = orm.relationship(
        back_populates="asset_item", uselist=False
    )
    activity: orm.Mapped[Activity] = orm.relationship(
        back_populates="asset_item", uselist=False
    )
    tag_list: orm.Mapped[TagList | None] = orm.relationship(
        back_populates="asset_item", uselist=False
    )
    service_list: orm.Mapped[ServiceList] = orm.relationship(
        back_populates="asset_item", uselist=False
    )
    last_location: orm.Mapped[LastLocation | None] = orm.relationship(
        back_populates="asset_item", uselist=False
    )
    criticality: orm.Mapped[Criticality] = orm.relationship(
        back_populates="asset_item", uselist=False
    )
    business_information: orm.Mapped[str | None]
    assigned_location: orm.Mapped[str | None]
    business_app_list_data: orm.Mapped[str | None]
    risk_score: orm.Mapped[int | None]
    passive_sensor: orm.Mapped[str | None]
    domain: orm.Mapped[list[str] | None] = orm.mapped_column(sa_pg.ARRAY(sa.String))
    subdomain: orm.Mapped[list[str] | None] = orm.mapped_column(sa_pg.ARRAY(sa.String))
    missing_software: orm.Mapped[str | None]
    whois: orm.Mapped[list[str] | None] = orm.mapped_column(sa_pg.ARRAY(sa.String))
    isp: orm.Mapped[str | None]
    asn: orm.Mapped[str | None]
    easm_tags: orm.Mapped[str | None]
    hosting_category1: orm.Mapped[str | None]
    custom_attributes: orm.Mapped[str | None]
    processor: orm.Mapped[Processor] = orm.relationship(
        back_populates="asset_item", uselist=False
    )
