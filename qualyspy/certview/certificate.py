import dataclasses
import datetime
import pathlib
import sqlite3
from typing import Sequence, Optional, Union
from .. import qualysapi
from .. import qutils

JSON_HEADERS = {"Accept": "application/json", "Content-Type": "application/json"}


@dataclasses.dataclass
class Subject_Alternative_Names:
    dns_names = Optional[Sequence[str]]
    ip_address = Optional[Sequence[str]]


@dataclasses.dataclass
class Subject:
    organization: str
    locality: str
    name: str
    state: str
    country: str
    organization_unit: Sequence[str]


@dataclasses.dataclass
class Issuer:
    organization: str
    organization_unit: Sequence[str]
    name: str
    country: str
    state: str
    certhash: str
    locality: str


@dataclasses.dataclass
class Host_Instance:
    id: int
    port: int
    fqdn: str
    protocol: str
    service: str
    grade: str


@dataclasses.dataclass
class Asset_Interface:
    hostname: str
    address: str


@dataclasses.dataclass
class Asset:
    id: int
    uuid: str
    netbios_name: str
    name: str
    operating_system: str
    host_instances: Sequence[Host_Instance]
    asset_interfaces: Sequence[Asset_Interface]


@dataclasses.dataclass
class Certificate:
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
    issuer: Optional[Issuer] = None
    rootissuer: Optional[Issuer] = None
    issuer_category: Optional[str] = None
    instance_count: Optional[int] = None
    asset_count: Optional[int] = None
    assets: Optional[Sequence[Asset]] = None
    key_usage: Optional[Sequence[str]] = None
    raw_data: Optional[str] = None
    enhanced_key_usage: Optional[Sequence[str]] = None
    subject_key_identifier: Optional[str] = None
    auth_key_identifier: Optional[str] = None
    subject_alternative_names: Optional[Subject_Alternative_Names] = None


def init_certificate_db(
    path: Optional[Union[str, pathlib.Path]] = None,
) -> None:
    con = sqlite3.connect(str(path))
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS certificate (
        PRIMARY KEY (id),
        certhash,
        key_size,
        serial_number,
        vaid_to_date,
        valid_to,
        valid_from_date,
        valid_from,
        signature_algorithm,
        extended_validation,
        created_date,
        dn,
        FOREIGN KEY (subject) REFERECES subject(name),
        update_date,
        last_found,
        imported,
        self_signed,
        FOREIGN KEY (issuer) REFERENCES issuer(name),
        FORIGN_KEY (rootissuer) REFERENCES issuer(name),
        issuer_category,
        asset_count,
        key_usage,
        raw_data,
        enhanced_key_usage,
        subject_key_identifier,
        auth_key_identifier,
        )
    """)


def _list_certificates_db(
    database: Optional[Union[str, pathlib.Path]] = None,
) -> None:
    con = sqlite3.connect(str(database))
    cur = con.cursor()


def list_certificates(
    conn: qualysapi.Connection,
    filter: Optional[Sequence[qutils.Filter]] = None,
    database: Optional[Union[str, pathlib.Path]] = None,
) -> list[Certificate]:
    """Retrieve a list of certificates.

    ASSET_INTERFACES, SSL_PROTOCOLS, CIPHER_SUITES, and EXTENSIVE_CERTIFICATE_INFO are included
    parameters, but not other options.

    Args:
        conn:
            A connection to the Qualys API.
        filter:
            A filter on the results of the search, using the tokens listed at
            https://www.qualys.com/docs/qualys-certview-api-user-guide.pdf#M9.8.newlink.compatible
            (the same as if performin the search via the website).
    """

    if isinstance(filter, Sequence):
        filter_parsed = [f() for f in filter]
    elif filter is not None:
        filter_parsed = [filter()]
    else:
        filter_parsed = None

    page_num = 0
    data = {
        "filter": {"filters": filter_parsed},
        "pageNumber": str(page_num),
        "includes": [
            "ASSET_INTERFACES",
            "SSL_PROTOCOLS",
            "CIPHER_SUITES",
            "EXTENSIVE_CERTIFICATE_INFO",
        ],
    }

    certificates: list[Certificate] = []
    raw = conn.post(
        qutils.URLS["List CertView Certificates"], data, add_headers=JSON_HEADERS
    )
    while len(raw) > 0:  # Certs are returned in pages of 10
        for cert in raw:
            c = qutils.json_to_class(
                cert,
                Certificate,
                classmap={
                    "asset": Asset,
                    "asset_interface": Asset_Interface,
                    "host_instance": Host_Instance,
                    "issuer": Issuer,
                    "root_issuer": Issuer,
                    "subject": Subject,
                    "subject_alternative_names": Subject_Alternative_Names,
                },
                listmap={
                    "assets": "asset",
                },
                funcmap={
                    "valid_to_date": qutils.datetime_from_qualys_format,
                    "valid_from_date": qutils.datetime_from_qualys_format,
                    "created_date": qutils.datetime_from_qualys_format,
                    "update_date": qutils.datetime_from_qualys_format,
                },
                name_converter=qutils.convert_camel_to_snake,
            )
            certificates.append(c)

        page_num += 1
        data["pageNumber"] = str(page_num)
        raw = conn.post(
            qutils.URLS["List CertView Certificates"],
            data,
            add_headers=JSON_HEADERS,
        )

    return certificates
