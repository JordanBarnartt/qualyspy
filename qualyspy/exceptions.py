"""Exceptions for QualysPy."""


class QualysAPIError(Exception):
    """Indicates an error with the Qualys API."""

    pass


class ConfigError(Exception):
    """Indicates an error with the configuration file."""

    pass
