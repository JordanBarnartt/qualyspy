import dataclasses
import datetime
import ipaddress
import psycopg2
import importlib.resources
from typing import Sequence, Optional, Union
from .. import qualysapi
from .. import qutils

JSON_HEADERS = {"Accept": "application/json", "Content-Type": "application/json"}
SQL = importlib.resources.files("qualyspy").joinpath("certview").joinpath("sql")


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
    address: Union[ipaddress.IPv4Address, ipaddress.IPv6Address]


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


def init_certificate_db() -> None:
    conn = psycopg2.connect(qutils.CONNECT_STRING)

    with SQL.joinpath("certview.sql").open() as f:
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


def _get_last_full_list_date() -> datetime.datetime:
    conn = psycopg2.connect(qutils.CONNECT_STRING)
    with conn:
        with conn.cursor() as curs:
            curs.execute("SELECT last_full_list FROM certificate.meta")
            last_full_list: datetime.datetime = curs.fetchone()
    return last_full_list


def list_certificates(
    conn: qualysapi.Connection,
    filter: Optional[Union[qutils.Filter, Sequence[qutils.Filter]]] = None,
    db: bool = False,
    db_cache: bool = True,
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
        db:
            Output the results to the database configured in the QualysPy conf file, rather than
            directly to Python objects.
        db_cache:
            When db is True and FIlter is None, only update those certificates which have been
            modified since the last call with no filter.
    """

    if db and db_cache and filter is None:
        last_full_list = _get_last_full_list_date()
        last_full_list_str = qutils.datetime_to_qualys_format(last_full_list)
        filter = qutils.Filter("certificate.updateDate", "GREATER", last_full_list_str)

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
                    "address": ipaddress.ip_address,
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
