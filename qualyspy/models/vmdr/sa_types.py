"""Shareable SQLAlchemy data types"""

import ipaddress

import sqlalchemy as sa


class IPv4AddressType(sa.types.TypeDecorator[sa.types.String]):
    """SQLAlchemy type for IPv4Address"""

    impl = sa.types.String

    def process_bind_param(self, value, dialect):  # type: ignore
        if value is not None:
            return str(value)
        else:
            return None

    def process_result_value(self, value, dialect):  # type: ignore
        if value is not None:
            return ipaddress.IPv4Address(value)
        else:
            return None


class IPv6AddressType(sa.types.TypeDecorator[sa.types.String]):
    """SQLAlchemy type for IPv6Address"""

    impl = sa.types.String

    def process_bind_param(self, value, dialect):  # type: ignore
        if value is not None:
            return str(value)
        else:
            return None

    def process_result_value(self, value, dialect):  # type: ignore
        if value is not None:
            return ipaddress.IPv6Address(value)
        else:
            return None
