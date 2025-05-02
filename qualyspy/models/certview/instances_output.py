import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic.alias_generators import to_camel
from pydantic.networks import IPvAnyAddress


class Model(BaseModel):
    model_config = ConfigDict(validate_by_name=True, alias_generator=to_camel)


class ProtocolSupportInfo(Model):
    sslv2: bool = Field(alias="SSLv2")
    sslv3: bool = Field(alias="SSLv3")
    tlsv1: bool = Field(alias="TLSv1")
    tlsv1_1: bool = Field(alias="TLSv1.1")
    tlsv1_2: bool = Field(alias="TLSv1.2")
    tlsv1_3: bool = Field(alias="TLSv1.3")


class CipherStrengthInfo(Model):
    less_than_128: bool = Field(alias="< 128 bits (e.g., 40, 56)")
    zero_bits: bool = Field(alias="0 bits (no encryption)")
    greater_equal_256: bool = Field(alias=">= 256 bits (e.g., 256)")
    less_than_256: bool = Field(alias="< 256 bits (e.g., 128, 168)")


class KeyExchangeInfo(BaseModel):
    key_or_dh_param_strength_lt_2048: bool = Field(
        alias="Key or DH parameter strength < 2048 bits (e.g., 1024)"
    )
    key_or_dh_param_strength_lt_512: bool = Field(
        alias="Key or DH parameter strength < 512 bits"
    )
    weak_key_debian_openssl: bool = Field(alias="Weak key (Debian OpenSSL flaw)")
    key_or_dh_param_strength_lt_4096: bool = Field(
        alias="Key or DH parameter strength < 4096 bits (e.g., 2048)"
    )
    key_or_dh_param_strength_ge_4096: bool = Field(
        alias="Key or DH parameter strength >= 4096 bits (e.g., 4096)"
    )
    exportable_key_exchange: bool = Field(alias="Exportable key exchange")
    anonymous_key_exchange: bool = Field(
        alias="Anonymous key exchange (no authentication)"
    )
    key_or_dh_param_strength_lt_1024: bool = Field(
        alias="Key or DH parameter strength < 1024 bits (e.g., 512)"
    )


class CipherSuite(Model):
    name: str
    key_exchange: str
    encryption_key_strength: int
    category: str


class CipherSuites(Model):
    sslv2: list[CipherSuite] | None = Field(alias="SSLv2", default=None)
    sslv3: list[CipherSuite] | None = Field(alias="SSLv3", default=None)
    tlsv1: list[CipherSuite] | None = Field(alias="TLSv1", default=None)
    tlsv1_1: list[CipherSuite] | None = Field(alias="TLSv1.1", default=None)
    tlsv1_2: list[CipherSuite] | None = Field(alias="TLSv1.2", default=None)
    tlsv1_3: list[CipherSuite] | None = Field(alias="TLSv1.3", default=None)


class Asset(Model):
    id: int
    uuid: str
    name: str
    primary_ip: IPvAnyAddress


class Certificate(Model):
    id: int
    certhash: str
    name: str
    last_found: datetime.datetime

    @field_validator("last_found", mode="after")
    @classmethod
    def parse_last_found(cls, value: Any) -> Any:
        if isinstance(value, (int, float)):
            return datetime.datetime.fromtimestamp(value)
        return value


class GradeSummary(Model):
    grade: str
    grade_with_trust_ignored: str
    certificate_score: int
    protocol_support_score: int
    key_exchange_score: int
    cipher_strength_score: int
    warnings: list[str]
    errors: list[str]
    notices: list[str]
    infos: list[str]
    highlights: list[str]
    protocol_support_info: ProtocolSupportInfo
    protocol_support_weightage: int
    cipher_strength_info: CipherStrengthInfo
    cipher_strength_weightage: int
    key_exchange_info: KeyExchangeInfo
    key_exchange_weightage: int
    cipher_suites: CipherSuites


class Instance(Model):
    id: int
    port: int
    scanned_date: datetime.datetime
    protocol: str
    service: str
    grade: str
    asset: Asset
    certificate: Certificate
    grade_summary: GradeSummary
