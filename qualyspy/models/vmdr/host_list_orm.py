"""ORM data model for host_list_vm_detection"""

import datetime as dt
import ipaddress
from typing import Optional

import sqlalchemy as sa
import sqlalchemy.orm as orm

from .. import sa_types


class Base(orm.DeclarativeBase):
    metadata = sa.MetaData(schema="qualys_host_list")


class AssetGroup(Base):
    __tablename__ = "asset_group"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    title: orm.Mapped[str | None]

    asset_group_list_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("asset_group_list.id")
    )
    asset_group_list: orm.Mapped["AssetGroupList"] = orm.relationship(
        "AssetGroupList", back_populates="asset_group"
    )


class Attribute(Base):
    __tablename__ = "attribute"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    name: orm.Mapped[str | None]
    last_status: orm.Mapped[str | None]
    value: orm.Mapped[str | None]
    last_success_date: orm.Mapped[dt.datetime | None]
    last_error_date: orm.Mapped[dt.datetime | None]
    last_error: orm.Mapped[str | None]

    azure_id: orm.Mapped[int | None] = orm.mapped_column(sa.ForeignKey("azure.id"))
    azure: orm.Mapped[Optional["Azure"]] = orm.relationship(back_populates="attribute")
    google_id: orm.Mapped[int | None] = orm.mapped_column(sa.ForeignKey("google.id"))
    google: orm.Mapped[Optional["Google"]] = orm.relationship(
        back_populates="attribute"
    )
    ec2_id: orm.Mapped[int | None] = orm.mapped_column(sa.ForeignKey("ec2.id"))
    ec2: orm.Mapped[Optional["Ec2"]] = orm.relationship(back_populates="attribute")


class CloudTag(Base):
    __tablename__ = "cloud_tag"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    name: orm.Mapped[str | None]
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
    fqdn: orm.Mapped[str | None]

    host_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("host.id"))
    host: orm.Mapped["Host"] = orm.relationship(back_populates="dns_data")


class IdSet(Base):
    __tablename__ = "id_set"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    id_range: orm.Mapped[list[str] | None] = orm.mapped_column(sa.ARRAY(sa.String))


class Param(Base):
    __tablename__ = "param"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    key: orm.Mapped[str | None]
    value: orm.Mapped[str | None]

    param_list_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("param_list.id"))
    param_list: orm.Mapped["ParamList"] = orm.relationship(back_populates="param")


class Tag(Base):
    __tablename__ = "tag"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    tag_id: orm.Mapped[int]
    name: orm.Mapped[str | None]

    host_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("host.id"))
    host: orm.Mapped["Host"] = orm.relationship(back_populates="tags")


class User(Base):
    __tablename__ = "user"

    user_login: orm.Mapped[str | None] = orm.mapped_column(primary_key=True)
    first_name: orm.Mapped[str | None]
    last_name: orm.Mapped[str | None]

    user_list_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("user_list.id"))
    user_list: orm.Mapped["UserList"] = orm.relationship(back_populates="user")


class Value1(Base):
    __tablename__ = "value1"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    ud_attr: orm.Mapped[str | None]
    value: orm.Mapped[str | None]

    user_def_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("user_def.id"))
    user_def: orm.Mapped["UserDef"] = orm.relationship(back_populates="value_1")


class Value2(Base):
    __tablename__ = "value2"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    ud_attr: orm.Mapped[str | None]
    value: orm.Mapped[str | None]

    user_def_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("user_def.id"))
    user_def: orm.Mapped["UserDef"] = orm.relationship(back_populates="value_2")


class Value3(Base):
    __tablename__ = "value3"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    ud_attr: orm.Mapped[str | None]
    value: orm.Mapped[str | None]

    user_def_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("user_def.id"))
    user_def: orm.Mapped["UserDef"] = orm.relationship(back_populates="value_3")


class VulnCount(Base):
    __tablename__ = "vuln_count"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    qds_severity: orm.Mapped[int]
    count: orm.Mapped[int | None]

    trurisk_score_factors_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("trurisk_score_factors.id")
    )
    trurisk_score_factors: orm.Mapped["TruriskScoreFactors"] = orm.relationship(
        back_populates="vuln_count"
    )


class TruriskScoreFactors(Base):
    __tablename__ = "trurisk_score_factors"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    trurisk_score_forumla: orm.Mapped[str | None]
    vuln_count: orm.Mapped[list[VulnCount]] = orm.relationship(
        back_populates="trurisk_score_factors"
    )

    host_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("host.id"))
    host: orm.Mapped["Host"] = orm.relationship(back_populates="trurisk_score_factors")


class AssetGroupList(Base):
    __tablename__ = "asset_group_list"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    asset_group: orm.Mapped[list[AssetGroup]] = orm.relationship(
        back_populates="asset_group_list"
    )

    glossary_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("glossary.id"))
    glossary: orm.Mapped["Glossary"] = orm.relationship(
        back_populates="asset_group_list"
    )


class Azure(Base):
    __tablename__ = "azure"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    attribute: orm.Mapped[list[Attribute]] = orm.relationship(back_populates="azure")

    metadata_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("metadata.id"))
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

    metadata_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("metadata.id"))
    metadata_: orm.Mapped["Metadata"] = orm.relationship(back_populates="ec2")


class Google(Base):
    __tablename__ = "google"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    attribute: orm.Mapped[list[Attribute]] = orm.relationship(back_populates="google")

    metadata_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("metadata.id"))
    metadata_: orm.Mapped["Metadata"] = orm.relationship(back_populates="google")


class ParamList(Base):
    __tablename__ = "param_list"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    param: orm.Mapped[list[Param]] = orm.relationship(back_populates="param_list")


# class Tags(Base):
#     __tablename__ = "tags"

#     id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
#     tag: orm.Mapped[list[Tag]] = orm.relationship(back_populates="tags")

#     host_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("host.id"))
#     host: orm.Mapped["Host"] = orm.relationship(back_populates="tags")


class UserDef(Base):
    __tablename__ = "user_def"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    label_1: orm.Mapped[str | None]
    label_2: orm.Mapped[str | None]
    label_3: orm.Mapped[str | None]
    value_1: orm.Mapped[Value1 | None] = orm.relationship(
        back_populates="user_def", uselist=False
    )
    value_2: orm.Mapped[Value2 | None] = orm.relationship(
        back_populates="user_def", uselist=False
    )
    value_3: orm.Mapped[Value3 | None] = orm.relationship(
        back_populates="user_def", uselist=False
    )

    glossary_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("glossary.id"))
    glossary: orm.Mapped["Glossary"] = orm.relationship(back_populates="user_def")

    host_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("host.id"))
    host: orm.Mapped["Host"] = orm.relationship(back_populates="user_def")


class UserList(Base):
    __tablename__ = "user_list"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    user: orm.Mapped[list[User]] = orm.relationship(back_populates="user_list")

    glossary_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("glossary.id"))
    glossary: orm.Mapped["Glossary"] = orm.relationship(back_populates="user_list")


class Glossary(Base):
    __tablename__ = "glossary"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    user_def: orm.Mapped[UserDef] = orm.relationship(
        back_populates="glossary", uselist=False
    )
    user_list: orm.Mapped[UserList] = orm.relationship(
        back_populates="glossary", uselist=False
    )
    asset_group_list: orm.Mapped[AssetGroupList] = orm.relationship(
        back_populates="glossary", uselist=False
    )


class Metadata(Base):
    __tablename__ = "metadata"

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
    trurisk_score: orm.Mapped[int | None]
    asset_criticality_score: orm.Mapped[int | None]
    trurisk_score_factors: orm.Mapped[TruriskScoreFactors | None] = orm.relationship(
        back_populates="host", uselist=False
    )
    tracking_method: orm.Mapped[str | None]
    network_id: orm.Mapped[int | None]
    dns: orm.Mapped[str | None]
    dns_data: orm.Mapped[DnsData | None] = orm.relationship(
        back_populates="host", uselist=False
    )
    cloud_provider: orm.Mapped[str | None]
    cloud_service: orm.Mapped[str | None]
    cloud_resource_id: orm.Mapped[str | None]
    ec2_instance_id: orm.Mapped[str | None]
    netbios: orm.Mapped[str | None]
    os: orm.Mapped[str | None]
    qg_hostid: orm.Mapped[str | None]
    last_boot: orm.Mapped[dt.datetime | None]
    serial_number: orm.Mapped[str | None]
    hardware_uuid: orm.Mapped[str | None]
    first_found_date: orm.Mapped[dt.datetime | None]
    last_activity: orm.Mapped[dt.datetime | None]
    agent_status: orm.Mapped[str | None]
    cloud_agent_running_on: orm.Mapped[str | None]
    tags: orm.Mapped[list[Tag]] = orm.relationship(back_populates="host", uselist=True)
    metadata_: orm.Mapped[Metadata | None] = orm.relationship(
        back_populates="host", uselist=False
    )
    cloud_provider_tags: orm.Mapped[CloudProviderTags | None] = orm.relationship(
        back_populates="host", uselist=False
    )
    last_vuln_scan_datetime: orm.Mapped[dt.datetime | None]
    last_vm_scanned_date: orm.Mapped[dt.datetime | None]
    last_vm_scanned_duration: orm.Mapped[dt.timedelta | None]
    last_vm_auth_scanned_date: orm.Mapped[dt.datetime | None]
    last_vm_auth_scanned_duration: orm.Mapped[dt.timedelta | None]
    last_compliance_scan_datetime: orm.Mapped[dt.datetime | None]
    last_scap_scan_datetime: orm.Mapped[dt.datetime | None]
    owner: orm.Mapped[str | None]
    comments: orm.Mapped[str | None]
    user_def: orm.Mapped[UserDef | None] = orm.relationship(
        back_populates="host", uselist=False
    )
    asset_group_ids: orm.Mapped[str | None]
