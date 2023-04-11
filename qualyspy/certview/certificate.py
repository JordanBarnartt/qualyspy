import datetime
import importlib.resources
import ipaddress
from typing import Any

import psycopg2.extensions
import pydantic as pd
import pydantic.networks
import pydantic.utils
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as sa_pg
import sqlalchemy.orm as orm

from .. import qualysapi, qutils

SQL = importlib.resources.files("qualyspy").joinpath("certview").joinpath("sql")


class Base(orm.DeclarativeBase):
    pass


Base.metadata.schema = "certificate"


def adapt_pydantic_ip_address(ip: pd.IPvAnyAddress) -> Any:
    return psycopg2.extensions.AsIs(repr(ip.exploded))


psycopg2.extensions.register_adapter(
    pydantic.networks.IPv4Address, adapt_pydantic_ip_address  # type: ignore
)
psycopg2.extensions.register_adapter(
    pydantic.networks.IPv4Address, adapt_pydantic_ip_address  # type: ignore
)


####################################################################################################
# Subject_Alternative_Name


class Subject_Alternative_Name_DNS_ORM(Base):
    __tablename__ = "subject_alternative_name_dns"

    name: orm.Mapped[str] = orm.mapped_column(primary_key=True)
    sans_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("subject_alternative_name.id")
    )
    sans: orm.Mapped["Subject_Alternative_Names_ORM"] = orm.relationship(
        back_populates="dns_names", uselist=False
    )


class Subject_Alternative_Name_IP_ORM(Base):
    __tablename__ = "subject_alternative_name_ip"

    ip: orm.Mapped[ipaddress.IPv4Address | ipaddress.IPv6Address] = orm.mapped_column(
        "ip", sa_pg.INET, primary_key=True
    )
    sans_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("subject_alternative_name.id")
    )
    sans: orm.Mapped["Subject_Alternative_Names_ORM"] = orm.relationship(
        back_populates="ips", uselist=False
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
        back_populates="subject_alternative_names", uselist=False
    )


class Subject_Alternative_Names(pd.BaseModel):
    dns_names = list[str]
    ip_address = list[str]

    class Config:
        alias_generator = qutils.to_lower_camel
        orm_mode = True
        allow_population_by_field_name = True


####################################################################################################

####################################################################################################
# Subject


class Subject_ORM(Base):
    __tablename__ = "subject"

    organization: orm.Mapped[str]
    locality: orm.Mapped[str]
    name: orm.Mapped[str] = orm.mapped_column(primary_key=True)
    state: orm.Mapped[str]
    country: orm.Mapped[str]

    organization_unit: orm.Mapped[list[str]] = orm.mapped_column(sa.ARRAY(sa.String))

    certificate_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("certificate.id"), primary_key=True
    )
    certificate: orm.Mapped["Certificate_ORM"] = orm.relationship(
        back_populates="subject", uselist=False
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
        orm_mode = True
        allow_population_by_field_name = True


####################################################################################################

####################################################################################################
# Issuer


class Issuer_ORM(Base):
    __tablename__ = "issuer"

    organization: orm.Mapped[str]
    organization_unit: orm.Mapped[list[str]] = orm.mapped_column(sa.ARRAY(sa.String))
    name: orm.Mapped[str]
    country: orm.Mapped[str]
    state: orm.Mapped[str]
    certhash: orm.Mapped[str] = orm.mapped_column(primary_key=True)
    locality: orm.Mapped[str]

    issuer_of: orm.Mapped[list["Certificate_ORM"]] = orm.relationship(
        back_populates="issuer"
    )


class RootIssuer_ORM(Base):
    __tablename__ = "rootissuer"

    organization: orm.Mapped[str]
    organization_unit: orm.Mapped[list[str]] = orm.mapped_column(sa.ARRAY(sa.String))
    name: orm.Mapped[str]
    country: orm.Mapped[str]
    state: orm.Mapped[str]
    certhash: orm.Mapped[str] = orm.mapped_column(primary_key=True)
    locality: orm.Mapped[str]

    rootissuer_of: orm.Mapped[list["Certificate_ORM"]] = orm.relationship(
        back_populates="rootissuer"
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
        orm_mode = True
        allow_population_by_field_name = True


####################################################################################################
# Host_Instance

asset_host_instance_association_table = sa.Table(
    "asset_host_instance",
    Base.metadata,
    sa.Column("asset_id", sa.INTEGER, sa.ForeignKey("asset.id"), primary_key=True),
    sa.Column(
        "host_instance_id",
        sa.INTEGER,
        sa.ForeignKey("host_instance.id"),
        primary_key=True,
    ),
)


class Host_Instance_ORM(Base):
    __tablename__ = "host_instance"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    port: orm.Mapped[int]
    fqdn: orm.Mapped[str]
    protocol: orm.Mapped[str]
    service: orm.Mapped[str | None]
    grade: orm.Mapped[str]

    asset: orm.Mapped[list["Asset_ORM"]] = orm.relationship(
        secondary=asset_host_instance_association_table
    )


class Host_Instance(pd.BaseModel):
    id: int
    port: int
    fqdn: str
    protocol: str
    service: str | None
    grade: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


####################################################################################################
# Asset_Interface


class Asset_Interface_ORM(Base):
    __tablename__ = "asset_interface"

    hostname: orm.Mapped[str | None]
    address: orm.Mapped[
        ipaddress.IPv4Address | ipaddress.IPv6Address
    ] = orm.mapped_column("address", sa_pg.INET, primary_key=True)

    asset_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("asset.id"))
    asset: orm.Mapped["Asset_ORM"] = orm.relationship(
        back_populates="asset_interfaces", uselist=False
    )


class Asset_Interface(pd.BaseModel):
    hostname: str | None
    address: pd.IPvAnyAddress

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


####################################################################################################

####################################################################################################
# Asset


class Asset_ORM(Base):
    __tablename__ = "asset"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    uuid: orm.Mapped[str]
    netbios_name: orm.Mapped[str]
    name: orm.Mapped[str]
    operating_system: orm.Mapped[str | None]
    host_instances: orm.Mapped[list[Host_Instance_ORM]] = orm.relationship(
        secondary=asset_host_instance_association_table
    )
    asset_interfaces: orm.Mapped[list[Asset_Interface_ORM] | None] = orm.relationship(
        back_populates="asset"
    )

    certificate_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("certificate.id"))
    certificate: orm.Mapped["Certificate_ORM"] = orm.relationship(
        back_populates="assets", uselist=False
    )


class Asset(pd.BaseModel):
    id: int
    uuid: str
    netbios_name: str
    name: str
    operating_system: str | None
    host_instances: list[Host_Instance]
    asset_interfaces: list[Asset_Interface] | None

    class Config:
        alias_generator = qutils.to_lower_camel
        orm_mode = True
        allow_population_by_field_name = True


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
    certificates: orm.Mapped[list["Certificate_ORM"]] = orm.relationship(
        secondary=certificate_key_usage_association_table
    )


class Certificate_ORM(Base):
    __tablename__ = "certificate"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    certhash: orm.Mapped[str]
    key_size: orm.Mapped[int]
    serial_number: orm.Mapped[str]
    valid_to_date: orm.Mapped[datetime.datetime]
    valid_to: orm.Mapped[int] = orm.mapped_column(sa.BigInteger)
    valid_from_date: orm.Mapped[datetime.datetime]
    valid_from: orm.Mapped[int] = orm.mapped_column(sa.BigInteger)
    signature_algorithm: orm.Mapped[str]
    extended_validation: orm.Mapped[bool]
    created_date: orm.Mapped[datetime.datetime]
    dn: orm.Mapped[str | None]
    subject: orm.Mapped[Subject_ORM] = orm.relationship(
        back_populates="certificate", uselist=False, cascade="all, delete-orphan"
    )
    update_date: orm.Mapped[datetime.datetime]
    last_found: orm.Mapped[int] = orm.mapped_column(sa.BigInteger)
    imported: orm.Mapped[bool]
    self_signed: orm.Mapped[bool]
    issuer_certhash: orm.Mapped[str | None] = orm.mapped_column(
        sa.ForeignKey("issuer.certhash")
    )
    issuer: orm.Mapped[Issuer_ORM | None] = orm.relationship(
        back_populates="issuer_of", uselist=False
    )
    rootissuer_certhash: orm.Mapped[str | None] = orm.mapped_column(
        sa.ForeignKey("rootissuer.certhash")
    )
    rootissuer: orm.Mapped[RootIssuer_ORM | None] = orm.relationship(
        back_populates="rootissuer_of", uselist=False
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
    ] = orm.relationship(back_populates="certificate", uselist=False)


class Certiticate_Getter(pydantic.utils.GetterDict):
    def get(self, key: str, default: Any = None) -> Any:
        if key == "key_usage":
            return [ku.usage for ku in self._obj.key_usage]
        elif key == "enhanced_key_usage":
            if self._obj.enhanced_key_usage is None:
                return None
            return [ku.usage for ku in self._obj.enhanced_key_usage]
        return super().get(key, default)


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
    dn: str | None
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
        orm_mode = True
        allow_population_by_field_name = True
        getter_dict = Certiticate_Getter


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


class List_CertView_Certificates_V2_Input(pd.BaseModel):
    filter: Filter | None = None
    page_number: int = 0
    page_size: int | None = None
    exclude_fields: str | None = None

    class Config:
        alias_generator = qutils.to_lower_camel
        allow_population_by_field_name = True


####################################################################################################


class List_Certificates_V2:
    def __init__(self, conn: qualysapi.Connection) -> None:
        self.conn = conn

    def __call_once(
        self, params: List_CertView_Certificates_V2_Input
    ) -> list[Certificate] | None:
        input_data = params.dict(by_alias=True, exclude_none=True)
        input_data["includes"] = [
            "ASSET_INTERFACES",
            "SSL_PROTOCOLS",
            "CIPHER_SUITES",
            "EXTENSIVE_CERTIFICATE_INFO",
        ]

        raw = self.conn.post(qutils.URLS["List CertView Certificates"], input_data)

        if len(raw) > 0:
            certificates: list[Certificate] = []
            for cert in raw:
                c = Certificate.parse_obj(cert)

                # subject.name somtimes includes null characters "\x00", even though the GUI doesn't
                # show these.  I've opened a ticket with Qualys about it.  In the meanwhile, this
                # will replace them with something PostgreSQL is happy with.
                # Also other fields, apparently...
                c.subject.name = c.subject.name.replace("\x00", "\uFFFD")
                c.subject.locality = c.subject.locality.replace("\x00", "\uFFFD")
                c.subject.state = c.subject.state.replace("\x00", "\uFFFD")

                certificates.append(c)
            return certificates
        else:
            return None

    def call(
        self,
        params: List_CertView_Certificates_V2_Input = List_CertView_Certificates_V2_Input(),
    ) -> list[Certificate]:
        certificates: list[Certificate] = []

        while (new_certs := self.__call_once(params)) is not None:
            certificates.extend(new_certs)

            params.page_number += 1

        return certificates

    def init_db(self, *, echo: bool = False) -> None:
        engine = sa.create_engine(qutils.E_URL, echo=echo)

        with engine.connect() as conn:
            conn.execute(sa.schema.CreateSchema("certificate", if_not_exists=True))
            conn.commit()

        Base.metadata.create_all(engine)

    def load(self, *, echo: bool = False) -> None:
        params = List_CertView_Certificates_V2_Input(page_size=200)

        engine = sa.create_engine(qutils.E_URL, echo=echo)

        while (new_certs := self.__call_once(params)) is not None:
            for c in new_certs:
                with orm.Session(engine) as session:
                    obj = qutils.to_orm_object(
                        c.dict(exclude_none=True), Certificate_ORM
                    )
                    obj = session.merge(obj)
                    session.add(obj)
                    session.commit()

            params.page_number += 1

    def query(self, stmt: Any, *, echo: bool = False) -> list[Certificate]:
        engine = sa.create_engine(qutils.E_URL, echo=echo)

        certificates: list[Certificate] = []
        with orm.Session(engine) as session:
            results = session.scalars(stmt)
            for result in results.all():
                c = Certificate.from_orm(result)
                certificates.append(c)

        return certificates

    def reset(self, *, echo: bool = False) -> None:
        engine = sa.create_engine(qutils.E_URL, echo=echo)

        stmt = sa.text("DROP SCHEMA IF EXISTS certificate CASCADE")
        with orm.Session(engine) as session:
            session.execute(stmt)
            session.commit()
        self.init_db(echo=echo)
