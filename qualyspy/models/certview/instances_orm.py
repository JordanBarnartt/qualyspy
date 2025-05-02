import datetime

import sqlalchemy as sa
import sqlalchemy.orm as orm

from .. import sa_types


class Base(orm.DeclarativeBase):
    metadata = sa.MetaData(schema="asset_details")


class CipherSuite(Base):
    __tablename__ = "cipher_suite"

    name: orm.Mapped[str] = orm.mapped_column(primary_key=True)
    key_exchange: orm.Mapped[str]
    encryption_key_strength: orm.Mapped[int]
    category: orm.Mapped[str]


class CipherSuites(Base):
    __tablename__ = "cipher_suites"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    sslv3: orm.Mapped[list["CipherSuite"]] = orm.relationship(
        back_populates="sslv3", uselist=True
    )
    tlsv1: orm.Mapped[list["CipherSuite"]] = orm.relationship(
        back_populates="tlsv1", uselist=True
    )
    tlsv1_1: orm.Mapped[list["CipherSuite"]] = orm.relationship(
        back_populates="tlsv1_1", uselist=True
    )
    tlsv1_2: orm.Mapped[list["CipherSuite"]] = orm.relationship(
        back_populates="tlsv1_2", uselist=True
    )
    tlsv1_3: orm.Mapped[list["CipherSuite"]] = orm.relationship(
        back_populates="tlsv1_3", uselist=True
    )


class Asset(Base):
    __tablename__ = "asset"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    uuid: orm.Mapped[str]
    name: orm.Mapped[str]
    primary_ip: orm.Mapped[sa_types.IPAddressGenericType]

    instances: orm.Mapped[list["Instance"]] = orm.relationship(
        back_populates="asset", uselist=True
    )


class Certificate(Base):
    __tablename__ = "certificate"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    certhash: orm.Mapped[str]
    name: orm.Mapped[str]
    last_found: orm.Mapped[datetime.datetime]

    instances: orm.Mapped[list["Instance"]] = orm.relationship(
        back_populates="certificate", uselist=True
    )


class GradeSummary(Base):
    __tablename__ = "grade_summary"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    grade: orm.Mapped[str]
    grade_with_trust_ignored: orm.Mapped[str]
    certificate_score: orm.Mapped[int]
    protocol_support_score: orm.Mapped[int]
    key_exchange_score: orm.Mapped[int]
    cipher_strength_score: orm.Mapped[int]
    warnings: orm.Mapped[list[str]]
    errors: orm.Mapped[list[str]]
    notices: orm.Mapped[list[str]]
    infos: orm.Mapped[list[str]]
    highlights: orm.Mapped[list[str]]
    protocol_support_info: orm.Mapped[ProtocolSupportInfo]
    protocol_support_weightage: orm.Mapped[int]
    cipher_strength_info: orm.Mapped[CipherStrengthInfo]
    cipher_strength_weightage: orm.Mapped[int]
    key_exchange_info: orm.Mapped[KeyExchangeInfo]
    key_exchange_weightage: orm.Mapped[int]
    cipher_suites: orm.Mapped[CipherSuites]


class Instance(Base):
    __tablename__ = "instance"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    port: orm.Mapped[int]
    scanned_date: orm.Mapped[datetime.datetime]
    protocol: orm.Mapped[str]
    service: orm.Mapped[str]
    grade: orm.Mapped[str]
    asset_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("asset.id"))
    asset: orm.Mapped[Asset] = orm.relationship(
        back_populates="instances", uselist=False
    )
    certificate_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("certificate.id"))
    certificate: orm.Mapped[Certificate] = orm.relationship(
        back_populates="instances", uselist=False
    )
    grade_summary: orm.Mapped[GradeSummary] = orm.relationship(
        back_populates="instance", uselist=False
    )
