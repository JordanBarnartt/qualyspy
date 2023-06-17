"""Custom xsdata converters to be shared by different models"""

import datetime as dt
from xsdata.formats.converter import Converter
from typing import Any
import ipaddress


class IPv4AddressConverter(Converter):
    """Converter for IPv4Address."""

    def deserialize(
        self, value: str, **kwargs: dict[Any, Any]
    ) -> ipaddress.IPv4Address:
        return ipaddress.IPv4Address(value)

    def serialize(self, value: ipaddress.IPv4Address, **kwargs: dict[Any, Any]) -> str:
        return str(value)


class IPv6AddressConverter(Converter):
    """Converter for IPv6Address."""

    def deserialize(
        self, value: str, **kwargs: dict[Any, Any]
    ) -> ipaddress.IPv6Address:
        return ipaddress.IPv6Address(value)

    def serialize(self, value: ipaddress.IPv6Address, **kwargs: dict[Any, Any]) -> str:
        return str(value)


class TimeDeltaConverter(Converter):
    """Converter for timedelta."""

    def deserialize(self, value: str, **kwargs: dict[Any, Any]) -> dt.timedelta:
        return dt.timedelta(seconds=int(value))

    def serialize(self, value: dt.timedelta, **kwargs: dict[Any, Any]) -> str:
        return str(value.total_seconds())


class StrConverter(Converter):
    """Converter for str, as metadata is a reserved keyword in SQLAlchemy."""

    def deserialize(self, value: str, **kwargs: dict[Any, Any]) -> str:
        if value == "metadata":
            return "metadata_"
        return value

    def serialize(self, value: str, **kwargs: dict[Any, Any]) -> str:
        return str(value)
