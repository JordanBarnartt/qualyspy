"""ORM data model for host_list_vm_detection"""

import datetime as dt
import ipaddress

import sqlalchemy as sa
import sqlalchemy.orm as orm

from .. import sa_types


class Base(orm.DeclarativeBase):
    metadata = sa.MetaData(schema="qualys_host_list_vm_detection")


class Attribute(Base):
    __tablename__ = "attribute"

    name: orm.Mapped[str] = orm.mapped_column(primary_key=True)
    last_status: orm.Mapped[str | None]
    value: orm.Mapped[str | None]
    last_success_date: orm.Mapped[dt.datetime | None]
    last_error_date: orm.Mapped[dt.datetime | None]
    last_error: orm.Mapped[str | None]

    azure_id: orm.Mapped[int | None] = orm.mapped_column(sa.ForeignKey("azure.id"))
    azure: orm.Mapped["Azure | None"] = orm.relationship(back_populates="attribute")
    google_id: orm.Mapped[int | None] = orm.mapped_column(sa.ForeignKey("google.id"))
    google: orm.Mapped["Google | None"] = orm.relationship(back_populates="attribute")
    ec2_id: orm.Mapped[int | None] = orm.mapped_column(sa.ForeignKey("ec2.id"))
    ec2: orm.Mapped["Ec2 | None"] = orm.relationship(back_populates="attribute")


class CloudTag(Base):
    __tablename__ = "cloud_tag"

    name: orm.Mapped[str] = orm.mapped_column(primary_key=True)
    value: orm.Mapped[str | None]
    last_success_date: orm.Mapped[dt.datetime | None]

    host_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("host.id"))
    host: orm.Mapped["Host"] = orm.relationship(back_populates="cloud_provider_tags")


class DnsData(Base):
    __tablename__ = "dns_data"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    hostname: orm.Mapped[str | None]
    domain: orm.Mapped[str | None]
    fqdn: orm.Mapped[str | None]

    host_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("host.id"))
    host: orm.Mapped["Host"] = orm.relationship(back_populates="dns_data")


class Qds(Base):
    __tablename__ = "qds"
    __table_args__ = (
        sa.ForeignKeyConstraint(
            ["detection_unqiue_vuln_id", "detection_qid"],
            ["detection.unique_vuln_id", "detection.qid"],
        ),
    )

    severity: orm.Mapped[str] = orm.mapped_column(primary_key=True)
    value: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    detection_unqiue_vuln_id: orm.Mapped[int]
    detection_qid: orm.Mapped[int]
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

    host_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("host.id"))
    host: orm.Mapped["Host"] = orm.relationship(back_populates="tags")


class Azure(Base):
    __tablename__ = "azure"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    attribute: orm.Mapped[list[Attribute]] = orm.relationship(back_populates="azure")

    metadata_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("metadata_.id"))
    metadata_: orm.Mapped["Metadata"] = orm.relationship(back_populates="azure")


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
    __table_args__ = (
        sa.ForeignKeyConstraint(
            ["detection_unqiue_vuln_id", "detection_qid"],
            ["detection.unique_vuln_id", "detection.qid"],
        ),
    )

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    qds_factor: orm.Mapped[list[QdsFactor]] = orm.relationship(
        back_populates="qds_factors"
    )

    detection_unqiue_vuln_id: orm.Mapped[int]
    detection_qid: orm.Mapped[int]
    detection: orm.Mapped["Detection"] = orm.relationship(back_populates="qds_factors")


class Detection(Base):
    __tablename__ = "detection"

    unique_vuln_id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    qid: orm.Mapped[int] = orm.mapped_column(primary_key=True)
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
    source: orm.Mapped[str | None]
    qds: orm.Mapped[Qds | None] = orm.relationship(
        back_populates="detection", uselist=False
    )
    qds_factors: orm.Mapped[list[QdsFactors]] = orm.relationship(
        back_populates="detection", uselist=True
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

    host_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("host.id"))
    host: orm.Mapped["Host"] = orm.relationship(back_populates="detections")


class Metadata(Base):
    __tablename__ = "metadata_"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    ec2: orm.Mapped[list[Ec2]] = orm.relationship(back_populates="metadata_")
    google: orm.Mapped[list[Google]] = orm.relationship(back_populates="metadata_")
    azure: orm.Mapped[list[Azure]] = orm.relationship(back_populates="metadata_")

    host_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("host.id"))
    host: orm.Mapped["Host"] = orm.relationship(back_populates="metadata_")


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
    last_vm_scanned_duration: orm.Mapped[int | None]
    last_vm_auth_scanned_date: orm.Mapped[dt.datetime | None]
    last_vm_auth_scanned_duration: orm.Mapped[int | None]
    last_pc_scanned_date: orm.Mapped[dt.datetime | None]
    tags: orm.Mapped[list[Tag]] = orm.relationship(back_populates="host", uselist=True)
    metadata_: orm.Mapped[Metadata | None] = orm.relationship(
        back_populates="host", uselist=False
    )
    cloud_provider_tags: orm.Mapped[list[CloudTag]] = orm.relationship(
        back_populates="host", uselist=True
    )
    detections: orm.Mapped[list[Detection]] = orm.relationship(
        back_populates="host", uselist=True
    )
