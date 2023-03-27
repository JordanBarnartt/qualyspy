import datetime
import importlib.resources
import ipaddress
from typing import Any

import pydantic as pd
import sqlalchemy as sa
import sqlalchemy.orm as orm
import sqlalchemy.dialects.postgresql

from .. import qualysapi
from .. import qutils

SQL = importlib.resources.files("qualyspy").joinpath("certview").joinpath("sql")


class Base(orm.DeclarativeBase):
    pass


Base.metadata.schema = "certificate"


####################################################################################################
# Subject_Alternative_Name


class Subject_Alternative_Name_DNS_ORM(Base):
    __tablename__ = "subject_alternative_name_dns"

    name: orm.Mapped[str] = orm.mapped_column(primary_key=True)
    sans_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("subject_alternative_name.id")
    )
    sans: orm.Mapped["Subject_Alternative_Names_ORM"] = orm.relationship(
        back_populates="dns_names"
    )


class Subject_Alternative_Name_IP_ORM(Base):
    __tablename__ = "subject_alternative_name_ip"

    ip: orm.Mapped[ipaddress.IPv4Address | ipaddress.IPv6Address] = orm.mapped_column(
        "ip", sqlalchemy.dialects.postgresql.INET, primary_key=True
    )
    sans_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("subject_alternative_name.id")
    )
    sans: orm.Mapped["Subject_Alternative_Names_ORM"] = orm.relationship(
        back_populates="ips"
    )


class Subject_Alternative_Names_ORM(Base):
    __tablename__ = "subject_alternative_name"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    dns_names: orm.Mapped[list[Subject_Alternative_Name_DNS_ORM]] = orm.relationship(
        back_populates="sans"
    )
    ips: orm.Mapped[list[Subject_Alternative_Name_IP_ORM]] = orm.relationship(
        back_populates="sans"
    )

    certificate_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("certificate.id"))
    certificate: orm.Mapped["Certificate_ORM"] = orm.relationship(
        back_populates="subject_alternative_names"
    )


class Subject_Alternative_Names(pd.BaseModel):
    dns_names = list[str]
    ip_address = list[str]

    class Config:
        alias_generator = qutils.to_lower_camel


####################################################################################################

####################################################################################################
# Subject


class Subject_OU_ORM(Base):
    __tablename__ = "subject_organization_unit"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[int]

    subject_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("subject.id"))
    subject: orm.Mapped["Subject_ORM"] = orm.relationship(
        back_populates="organization_unit"
    )


class Subject_ORM(Base):
    __tablename__ = "subject"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    organization: orm.Mapped[str]
    locality: orm.Mapped[str]
    name: orm.Mapped[str]
    state: orm.Mapped[str]
    country: orm.Mapped[str]

    organization_unit: orm.Mapped[list[Subject_OU_ORM] | None] = orm.relationship(
        back_populates="subject"
    )

    certificate_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("certificate.id"))
    certificate: orm.Mapped["Certificate_ORM"] = orm.relationship(
        back_populates="subject"
    )


class Subject(pd.BaseModel):
    organization: str
    locality: str
    name: str
    state: str
    country: str
    organization_unit: list[str] | None

    class Config:
        alias_generator = qutils.to_lower_camel


####################################################################################################

####################################################################################################
# Issuer

certificate_issuer_association_table = sa.Table(
    "certificate_issuer",
    Base.metadata,
    sa.Column(
        "certificate_id", sa.Integer, sa.ForeignKey("certificate.id"), primary_key=True
    ),
    sa.Column("issuer_id", sa.Text, sa.ForeignKey("issuer.certhash"), primary_key=True),
)

certificate_rootissuer_association_table = sa.Table(
    "certificate_rootissuer",
    Base.metadata,
    sa.Column(
        "certificate_id", sa.Integer, sa.ForeignKey("certificate.id"), primary_key=True
    ),
    sa.Column("issuer_id", sa.Text, sa.ForeignKey("issuer.certhash"), primary_key=True),
)


class Issuer_OU_ORM(Base):
    __tablename__ = "issuer_organization_unit"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[int]

    issuer_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("issuer.certhash"))
    issuer: orm.Mapped["Issuer_ORM"] = orm.relationship(
        back_populates="organization_unit"
    )

    issuer_of: orm.Mapped["Certificate_ORM"] = orm.relationship(
        secondary=certificate_issuer_association_table
    )
    rootissuer_of: orm.Mapped["Certificate_ORM"] = orm.relationship(
        secondary=certificate_rootissuer_association_table
    )


class Issuer_ORM(Base):
    __tablename__ = "issuer"

    organization: orm.Mapped[str]
    organization_unit: orm.Mapped[list[Issuer_OU_ORM]] = orm.relationship(
        back_populates="issuer"
    )
    name: orm.Mapped[str]
    country: orm.Mapped[str]
    state: orm.Mapped[str]
    certhash: orm.Mapped[str] = orm.mapped_column(primary_key=True)
    locality: orm.Mapped[str]

    certificates: orm.Mapped[list["Certificate_ORM"]] = orm.relationship(
        secondary=certificate_issuer_association_table
    )


class Issuer(pd.BaseModel):
    organization: str
    organization_unit: list[str]
    name: str
    country: str
    state: str
    certhash: str
    locality: str

    class Config:
        alias_generator = qutils.to_lower_camel


####################################################################################################
# Host_Instance


class Host_Instance_ORM(Base):
    __tablename__ = "host_instance"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    port: orm.Mapped[int]
    fqdn: orm.Mapped[str]
    protocol: orm.Mapped[str]
    service: orm.Mapped[str]
    grade: orm.Mapped[str]

    asset_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("asset.id"))
    asset: orm.Mapped["Asset_ORM"] = orm.relationship(back_populates="host_instances")


class Host_Instance(pd.BaseModel):
    id: int
    port: int
    fqdn: str
    protocol: str
    service: str
    grade: str


####################################################################################################
# Asset_Interface


class Asset_Interface_ORM(Base):
    __tablename__ = "asset_interface"

    hostname: orm.Mapped[str] = orm.mapped_column(primary_key=True)
    address: orm.Mapped[
        ipaddress.IPv4Address | ipaddress.IPv6Address
    ] = orm.mapped_column(
        "address", sqlalchemy.dialects.postgresql.INET, primary_key=True
    )

    asset_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("asset.id"))
    asset: orm.Mapped["Asset_ORM"] = orm.relationship(back_populates="asset_interfaces")


class Asset_Interface(pd.BaseModel):
    hostname: str | None
    address: pd.IPvAnyAddress


####################################################################################################

####################################################################################################
# Asset


class Asset_ORM(Base):
    __tablename__ = "asset"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    uuid: orm.Mapped[str]
    netbios_name: orm.Mapped[str]
    name: orm.Mapped[str]
    operating_system: orm.Mapped[str]
    host_instances: orm.Mapped[list[Host_Instance_ORM]] = orm.relationship(
        back_populates="asset"
    )
    asset_interfaces: orm.Mapped[list[Asset_Interface_ORM]] = orm.relationship(
        back_populates="asset"
    )

    certificate_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("certificate.id"))
    certificate: orm.Mapped["Certificate_ORM"] = orm.relationship(
        back_populates="asset"
    )


class Asset(pd.BaseModel):
    id: int
    uuid: str
    netbios_name: str
    name: str
    operating_system: str
    host_instances: list[Host_Instance]
    asset_interfaces: list[Asset_Interface]

    class Config:
        alias_generator = qutils.to_lower_camel


####################################################################################################
# Certificate

certificate_key_usage_association_table = sa.Table(
    "certificate_key_usage",
    Base.metadata,
    sa.Column(
        "certificate_id", sa.Integer, sa.ForeignKey("certificate.id"), primary_key=True
    ),
    sa.Column("usage", sa.Text, sa.ForeignKey("key_usage.usage"), primary_key=True),
)

certificate_enhanced_key_usage_association_table = sa.Table(
    "certificate_enhanced_key_usage",
    Base.metadata,
    sa.Column(
        "certificate_id", sa.Integer, sa.ForeignKey("certificate.id"), primary_key=True
    ),
    sa.Column("usage", sa.Text, sa.ForeignKey("key_usage.usage"), primary_key=True),
)


class Key_Usage_ORM(Base):
    __tablename__ = "key_usage"

    usage: orm.Mapped[str] = orm.mapped_column(primary_key=True)
    certificates: orm.Mapped[list["Certificate"]] = orm.relationship(
        secondary=certificate_key_usage_association_table
    )


class Certificate_ORM(Base):
    __tablename__ = "certificate"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    certhash: orm.Mapped[str]
    key_size: orm.Mapped[int]
    serial_number: orm.Mapped[str]
    valid_to_date: orm.Mapped[datetime.datetime]
    valid_to: orm.Mapped[int]
    valid_from_date: orm.Mapped[datetime.datetime]
    valid_from: orm.Mapped[int]
    signature_algorithm: orm.Mapped[str]
    extended_validation: orm.Mapped[bool]
    created_date: orm.Mapped[datetime.datetime]
    dn: orm.Mapped[str]
    subject: orm.Mapped[Subject_ORM] = orm.relationship(back_populates="certificate")
    update_date: orm.Mapped[datetime.datetime]
    last_found: orm.Mapped[int]
    imported: orm.Mapped[bool]
    self_signed: orm.Mapped[bool]
    issuer: orm.Mapped[Issuer_ORM | None] = orm.relationship(
        secondary=certificate_issuer_association_table
    )
    rootissuer: orm.Mapped[Issuer_ORM | None] = orm.relationship(
        secondary=certificate_rootissuer_association_table
    )
    issuer_category: orm.Mapped[str]
    instance_count: orm.Mapped[int]
    asset_count: orm.Mapped[int]
    assets: orm.Mapped[list[Asset_ORM]] = orm.relationship(back_populates="certificate")
    key_usage: orm.Mapped[list[Key_Usage_ORM]] = orm.relationship(
        secondary=certificate_key_usage_association_table
    )
    raw_data: orm.Mapped[str]
    enhanced_key_usage: orm.Mapped[list[Key_Usage_ORM] | None] = orm.relationship(
        secondary=certificate_enhanced_key_usage_association_table
    )
    subject_key_identifier: orm.Mapped[str | None]
    auth_key_identifier: orm.Mapped[str | None]
    subject_alternative_names: orm.Mapped[
        Subject_Alternative_Names_ORM | None
    ] = orm.relationship(back_populates="certificate")


class Certificate(pd.BaseModel):
    id: int
    certhash: str
    key_size: int
    serial_number: str
    valid_to_date: datetime.datetime
    valid_to: int
    valid_from_date: datetime.datetime
    valid_from: int
    signature_algorithm: str
    extended_validation: bool
    created_date: datetime.datetime
    dn: str
    subject: Subject
    update_date: datetime.datetime
    last_found: int
    imported: bool
    self_signed: bool
    issuer: Issuer | None
    rootissuer: Issuer | None
    issuer_category: str
    instance_count: int
    asset_count: int
    assets: list[Asset]
    key_usage: list[str]
    raw_data: str
    enhanced_key_usage: list[str] | None
    subject_key_identifier: str | None
    auth_key_identifier: str | None
    subject_alternative_names: Subject_Alternative_Names | None

    class Config:
        alias_generator = qutils.to_lower_camel


####################################################################################################

####################################################################################################
# Function input


class Field_Value_Operator(pd.BaseModel):
    field: str
    value: str
    operator: str


class Filter(pd.BaseModel):
    filters: list[Field_Value_Operator]
    operation: str = "AND"


class List_CertView_Certificates_v2_Input(pd.BaseModel):
    filter: Filter | None
    page_number: int = 0
    page_size: int | None
    exclude_fields: str | None

    class Config:
        alias_generator = qutils.to_lower_camel


####################################################################################################

def list_certificates_v2(
    conn: qualysapi.Connection,
    api_input: List_CertView_Certificates_v2_Input = List_CertView_Certificates_v2_Input(
        filter=None, page_size=None, exclude_fields=None
    ),
    db: bool = False,
    db_query: sa.Select[Any] | None = None,
) -> list[Certificate]:
    input_data = api_input.dict(by_alias=True, exclude_none=True)
    input_data["includes"] = [
        "ASSET_INTERFACES",
        "SSL_PROTOCOLS",
        "CIPHER_SUITES",
        "EXTENSIVE_CERTIFICATE_INFO",
    ]

    if db:
        e_url = f"postgresql://{qutils.DB_USER}"
        ":{qutils.DB_PASSWORD}@{qutils.DB_HOST}/{qutils.DB_NAME}"
        engine = sa.create_engine(e_url, echo=True)
    else:
        certificates: list[Certificate] = []

    raw = conn.post(qutils.URLS["List CertView Certificates"], input_data)

    while len(raw) > 0:
        for cert in raw:
            c = Certificate.parse_obj(cert)
            certificates.append(c)
        if db:
            with orm.Session(engine) as session:
                session.add_all(certificates)
                session.commit()

                certificates = []

        input_data["pageNumber"] += 1
        raw = conn.post(
            qutils.URLS["List CertView Certificates"],
            input_data,
        )

    return certificates


def init_db() -> None:
    e_url = f"postgresql://{qutils.DB_USER}:{qutils.DB_PASSWORD}@{qutils.DB_HOST}/{qutils.DB_NAME}"
    engine = sa.create_engine(e_url, echo=True)

    with engine.connect() as conn:
        conn.execute(sa.schema.CreateSchema("certificate", if_not_exists=True))
        conn.commit()

    Base.metadata.create_all(engine)
