"""ORM data model for host_list_vm_detection"""

import datetime as dt
import ipaddress

import sqlalchemy as sa
import sqlalchemy.orm as orm

from . import sa_types


class Base(orm.DeclarativeBase):
    pass


Base.metadata.schema = "host_list_vm_detection"


class AssetGroup(Base):
    __tablename__ = "asset_group"

    id: orm.MappedColumn[int] = orm.mapped_column(primary_key=True)
    title: orm.MappedColumn[str | None]


class Attribute(Base):
    __tablename__ = "attribute"

    id: orm.MappedColumn[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    name: orm.MappedColumn[str | None]
    last_status: orm.MappedColumn[str | None]
    value: orm.MappedColumn[str | None]
    last_success_date: orm.MappedColumn[dt.datetime | None]
    last_error_date: orm.MappedColumn[dt.datetime | None]
    last_error: orm.MappedColumn[str | None]


class CloudTag(Base):
    __tablename__ = "cloud_tag"

    id: orm.MappedColumn[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    name: orm.MappedColumn[str | None]
    value: orm.MappedColumn[str | None]
    last_success_date: orm.MappedColumn[dt.datetime | None]


class DnsData(Base):
    __tablename__ = "dns_data"

    id: orm.MappedColumn[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    hostname: orm.MappedColumn[str | None]
    domain: orm.MappedColumn[str | None]
    fqdn: orm.MappedColumn[str | None]


class IdSet(Base):
    __tablename__ = "id_set"

    id: orm.MappedColumn[int] = orm.mapped_column(primary_key=True)
    id_range: orm.MappedColumn[list[str] | None]

    
