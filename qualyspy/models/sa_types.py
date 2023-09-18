"""Shareable SQLAlchemy data types"""

import ipaddress

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql


class IPv4AddressType(sa.types.TypeDecorator[sa.types.String]):
    """SQLAlchemy type for IPv4Address"""

    impl = sqlalchemy.dialects.postgresql.INET

    def process_bind_param(self, value, dialect):  # type: ignore
        if value is not None:
            if isinstance(value, list):
                return value[0].exploded
            else:
                return value.exploded
        else:
            return None

    def process_result_value(self, value, dialect):  # type: ignore
        if value is not None:
            return ipaddress.IPv4Address(value)
        else:
            return None


class IPv6AddressType(sa.types.TypeDecorator[sa.types.String]):
    """SQLAlchemy type for IPv6Address"""

    impl = sqlalchemy.dialects.postgresql.INET

    def process_bind_param(self, value, dialect):  # type: ignore
        if value is not None:
            if isinstance(value, list):
                return value[0].exploded
            else:
                return value.exploded
        else:
            return None

    def process_result_value(self, value, dialect):  # type: ignore
        if value is not None:
            return ipaddress.IPv6Address(value)
        else:
            return None


class IPAddressGenericType(sa.types.TypeDecorator[sa.types.String]):
    impl = sqlalchemy.dialects.postgresql.INET

    # Clears the following warning:
    # SAWarning: TypeDecorator IPAddressGenericType() will not produce a cache key because the
    # ``cache_ok`` attribute is not set to True.  This can have significant performance
    # implications including some performance degradations in comparison to prior SQLAlchemy
    # versions.  Set this attribute to True if this type object's state is safe to use in a
    # cache key, or False to disable this warning. (Background on this warning at:
    # https://sqlalche.me/e/20/cprf)
    cache_ok = True

    def process_bind_param(self, value, dialect):  # type: ignore
        if value is not None:
            if isinstance(value, list):
                return value[0].exploded
            else:
                return value.exploded
        else:
            return None

    def process_result_value(self, value, dialect):  # type: ignore
        if value is not None:
            return ipaddress.ip_address(value)
        else:
            return None
