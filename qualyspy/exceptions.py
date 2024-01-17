"""Exceptions for QualysPy."""


class QualysAPIError(Exception):
    """Indicates an error with the Qualys API."""

    pass


class ConfigError(Exception):
    """Indicates an error with the configuration file."""

    pass


class ValidationError(Exception):
    """Wrapper for pydantic.error_wrappers.ValidationError"""

    pass


class TimeoutError(Exception):
    """Wrapper for requests.exceptions.Timeout"""

    pass
