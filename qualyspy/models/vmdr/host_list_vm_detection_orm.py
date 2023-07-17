"""ORM data model for host_list_vm_detection"""

import datetime as dt
import ipaddress
from typing import Optional

import sqlalchemy as sa
import sqlalchemy.orm as orm

from .. import sa_types


class Base(orm.DeclarativeBase):
    pass


Base.metadata.schema = "host_list_vm_detection"


class Attribute(Base):
    __tablename__ = "attribute"

    name: orm.Mapped[str] = orm.mapped_column(primary_key=True)
    last_status: orm.Mapped[str | None]
    value: orm.Mapped[str | None]
    last_success_date: orm.Mapped[dt.datetime | None]
    last_error_date: orm.Mapped[dt.datetime | None]
    last_error: orm.Mapped[str | None]

    azure_id: orm.Mapped[int | None] = orm.mapped_column(sa.ForeignKey("azure.id"))
    azure: orm.Mapped[Optional["Azure"]] = orm.relationship(back_populates="attribute")
    google_id: orm.Mapped[int | None] = orm.mapped_column(sa.ForeignKey("google.id"))
    google: orm.Mapped[Optional["Google"]] = orm.relationship(back_populates="attribute")
    ec2_id: orm.Mapped[int | None] = orm.mapped_column(sa.ForeignKey("ec2.id"))
    ec2: orm.Mapped[Optional["Ec2"]] = orm.relationship(back_populates="attribute")


class CloudTag(Base):
    __tablename__ = "cloud_tag"

    name: orm.Mapped[str] = orm.mapped_column(primary_key=True)
    value: orm.Mapped[str | None]
    last_success_date: orm.Mapped[dt.datetime | None]

    cloud_provider_tags_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("cloud_provider_tags.id")
    )
    cloud_provider_tags: orm.Mapped["CloudProviderTags"] = orm.relationship(
        back_populates="cloud_tag"
    )


class DnsData(Base):
    __tablename__ = "dns_data"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    hostname: orm.Mapped[str | None]
    domain: orm.Mapped[str | None]
    fqdn: orm.Mapped[str]

    host_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("host.id"))
    host: orm.Mapped["Host"] = orm.relationship(back_populates="dns_data")


class Qds(Base):
    __tablename__ = "qds"

    severity: orm.Mapped[str] = orm.mapped_column(primary_key=True)
    value: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    detection_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("detection.id"))
    detection: orm.Mapped["Detection"] = orm.relationship(back_populates="qds")


class QdsFactor(Base):
    __tablename__ = "qds_factor"

    name: orm.Mapped[str] = orm.mapped_column(primary_key=True)
    value: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    qds_factors_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("qds_factors.id"))
    qds_factors: orm.Mapped["QdsFactors"] = orm.relationship(
        back_populates="qds_factor"
    )


class Tag(Base):
    __tablename__ = "tag"

    tag_id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[str]
    color: orm.Mapped[str | None]
    background_color: orm.Mapped[str | None]

    tags_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("tags.id"))
    tags: orm.Mapped["Tags"] = orm.relationship(back_populates="tag")


class Azure(Base):
    __tablename__ = "azure"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    attribute: orm.Mapped[list[Attribute]] = orm.relationship(back_populates="azure")

    metadata_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("metadata_.id"))
    metadata_: orm.Mapped["Metadata"] = orm.relationship(back_populates="azure")


class CloudProviderTags(Base):
    __tablename__ = "cloud_provider_tags"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    cloud_tag: orm.Mapped[list[CloudTag]] = orm.relationship(
        back_populates="cloud_provider_tags"
    )

    host_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("host.id"))
    host: orm.Mapped["Host"] = orm.relationship(back_populates="cloud_provider_tags")


class Ec2(Base):
    __tablename__ = "ec2"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    attribute: orm.Mapped[list[Attribute]] = orm.relationship(back_populates="ec2")

    metadata_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("metadata_.id"))
    metadata_: orm.Mapped["Metadata"] = orm.relationship(back_populates="ec2")


class Google(Base):
    __tablename__ = "google"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    attribute: orm.Mapped[list[Attribute]] = orm.relationship(back_populates="google")

    metadata_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("metadata_.id"))
    metadata_: orm.Mapped["Metadata"] = orm.relationship(back_populates="google")


class QdsFactors(Base):
    __tablename__ = "qds_factors"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    qds_factor: orm.Mapped[list[QdsFactor]] = orm.relationship(
        back_populates="qds_factors"
    )

    detection_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("detection.id"))
    detection: orm.Mapped["Detection"] = orm.relationship(back_populates="qds_factors")


class Tags(Base):
    __tablename__ = "tags"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    tag: orm.Mapped[list[Tag]] = orm.relationship(back_populates="tags")

    host_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("host.id"))
    host: orm.Mapped["Host"] = orm.relationship(back_populates="tags")


class Detection(Base):
    __tablename__ = "detection"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    qid: orm.Mapped[int]
    type: orm.Mapped[str | None]
    severity: orm.Mapped[int | None]
    port: orm.Mapped[int | None]
    protocol: orm.Mapped[str | None]
    fqdn: orm.Mapped[str | None]
    ssl: orm.Mapped[bool | None]
    instance: orm.Mapped[str | None]
    results: orm.Mapped[str | None]
    status: orm.Mapped[str | None]
    first_found_datetime: orm.Mapped[dt.datetime | None]
    last_found_datetime: orm.Mapped[dt.datetime | None]
    qds: orm.Mapped[Qds | None] = orm.relationship(
        back_populates="detection", uselist=False
    )
    qds_factors: orm.Mapped[QdsFactors | None] = orm.relationship(
        back_populates="detection", uselist=False
    )
    times_found: orm.Mapped[int | None]
    last_test_datetime: orm.Mapped[dt.datetime | None]
    last_update_datetime: orm.Mapped[dt.datetime | None]
    last_fixed_datetime: orm.Mapped[dt.datetime | None]
    first_reopened_datetime: orm.Mapped[dt.datetime | None]
    last_reopened_datetime: orm.Mapped[dt.datetime | None]
    times_reopened: orm.Mapped[int | None]
    service: orm.Mapped[str | None]
    is_ignored: orm.Mapped[bool | None]
    is_disabled: orm.Mapped[bool | None]
    affect_running_kernel: orm.Mapped[bool | None]
    affect_running_service: orm.Mapped[bool | None]
    affect_exploitable_config: orm.Mapped[bool | None]
    last_processed_datetime: orm.Mapped[dt.datetime | None]
    asset_cve: orm.Mapped[str | None]

    detection_list_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("detection_list.id")
    )
    detection_list: orm.Mapped["DetectionList"] = orm.relationship(
        back_populates="detection"
    )


class Metadata(Base):
    __tablename__ = "metadata_"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    ec2: orm.Mapped[list[Ec2]] = orm.relationship(back_populates="metadata_")
    google: orm.Mapped[list[Google]] = orm.relationship(back_populates="metadata_")
    azure: orm.Mapped[list[Azure]] = orm.relationship(back_populates="metadata_")

    host_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("host.id"))
    host: orm.Mapped["Host"] = orm.relationship(back_populates="metadata_")


class DetectionList(Base):
    __tablename__ = "detection_list"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    detection: orm.Mapped[list[Detection]] = orm.relationship(
        back_populates="detection_list"
    )

    host_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("host.id"))
    host: orm.Mapped["Host"] = orm.relationship(back_populates="detection_list")


class Host(Base):
    __tablename__ = "host"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    asset_id: orm.Mapped[int | None]
    ip: orm.Mapped[ipaddress.IPv4Address | None] = orm.mapped_column(
        "ip", sa_types.IPv4AddressType
    )
    ipv6: orm.Mapped[ipaddress.IPv6Address | None] = orm.mapped_column(
        "ipv6", sa_types.IPv6AddressType
    )
    tracking_method: orm.Mapped[str | None]
    network_id: orm.Mapped[int | None]
    os: orm.Mapped[str | None]
    os_cpe: orm.Mapped[str | None]
    dns: orm.Mapped[str | None]
    dns_data: orm.Mapped[DnsData | None] = orm.relationship(
        back_populates="host", uselist=False
    )
    cloud_provider: orm.Mapped[str | None]
    cloud_service: orm.Mapped[str | None]
    cloud_resource_id: orm.Mapped[str | None]
    ec2_instance_id: orm.Mapped[str | None]
    netbios: orm.Mapped[str | None]
    qg_hostid: orm.Mapped[str | None]
    last_scan_datetime: orm.Mapped[dt.datetime | None]
    last_vm_scanned_date: orm.Mapped[dt.datetime | None]
    last_vm_scanned_duration: orm.Mapped[dt.timedelta | None]
    last_vm_auth_scanned_date: orm.Mapped[dt.datetime | None]
    last_vm_auth_scanned_duration: orm.Mapped[dt.timedelta | None]
    last_pc_scanned_date: orm.Mapped[dt.datetime | None]
    tags: orm.Mapped[Tags | None] = orm.relationship(
        back_populates="host", uselist=False
    )
    metadata_: orm.Mapped[Metadata | None] = orm.relationship(
        back_populates="host", uselist=False
    )
    cloud_provider_tags: orm.Mapped[CloudProviderTags | None] = orm.relationship(
        back_populates="host", uselist=False
    )
    detection_list: orm.Mapped[DetectionList | None] = orm.relationship(
        back_populates="host", uselist=False
    )
