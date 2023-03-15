import datetime
import ipaddress
import importlib.resources

import psycopg2
from pydantic import BaseModel

from .. import qualysapi
from .. import qutils

SQL = importlib.resources.files("qualyspy").joinpath("certview").joinpath("sql")


class Subject_Alternative_Names(BaseModel):
    dns_names = list[str]
    ip_address = list[str]

    class Config:
        alias_generator = qutils.to_lower_camel


class Subject(BaseModel):
    organization: str
    locality: str
    name: str
    state: str
    country: str
    organization_unit: list[str] | None

    class Config:
        alias_generator = qutils.to_lower_camel


class Issuer(BaseModel):
    organization: str
    organization_unit: list[str]
    name: str
    country: str
    state: str
    certhash: str
    locality: str

    class Config:
        alias_generator = qutils.to_lower_camel


class Host_Instance(BaseModel):
    id: int
    port: int
    fqdn: str
    protocol: str
    service: str
    grade: str


class Asset_Interface(BaseModel):
    hostname: str | None
    address: ipaddress.IPv4Address | ipaddress.IPv6Address


class Asset(BaseModel):
    id: int
    uuid: str
    netbios_name: str
    name: str
    operating_system: str
    host_instances: list[Host_Instance]
    asset_interfaces: list[Asset_Interface]

    class Config:
        alias_generator = qutils.to_lower_camel


class Certificate(BaseModel):
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


class Field_Value_Operator(BaseModel):
    field: str
    value: str
    operator: str


class Filter(BaseModel):
    filters: list[Field_Value_Operator]
    operation: str = "AND"


class List_CertView_Certificates_v2_Input(BaseModel):
    filter: Filter | None
    page_number: int = 0
    page_size: int | None
    exclude_fields: str | None

    class Config:
        alias_generator = qutils.to_lower_camel


def list_certificates_v2(
    conn: qualysapi.Connection,
    input: List_CertView_Certificates_v2_Input,
) -> list[Certificate]:
    input_data = input.dict(by_alias=True, exclude_none=True)
    input_data["includes"] = [
        "ASSET_INTERFACES",
        "SSL_PROTOCOLS",
        "CIPHER_SUITES",
        "EXTENSIVE_CERTIFICATE_INFO",
    ]

    certificates: list[Certificate] = []
    raw = conn.post(qutils.URLS["List CertView Certificates"], input_data)

    while len(raw) > 0:
        for cert in raw:
            c = Certificate.parse_obj(cert)
            certificates.append(c)

        input_data["pageNumber"] += 1
        raw = conn.post(
            qutils.URLS["List CertView Certificates"],
            input_data,
        )

    return certificates


def init_certificate_db() -> None:
    conn = psycopg2.connect(qutils.CONNECT_STRING)

    with SQL.joinpath("certview_init.sql").open() as f:
        create_commands = f.read()

    with conn:
        with conn.cursor() as curs:
            curs.execute(create_commands)
            curs.execute(
                """
            INSERT INTO certificate.meta (last_full_list)
            VALUES ('-infinity')
            """
            )

    conn.close()
