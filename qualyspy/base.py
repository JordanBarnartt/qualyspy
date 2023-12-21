"""Base classes for intereacting with the Qualys API and the database where information is being
stored.  Primarily used internally by the QualysPy library, but can be used to call APIs which the
library does not yet support.

Typical usage example:
api = QualysAPIBase()
api.get("/msp/about.php")
"""

# For SQLAlchemy:
# mypy: allow-untyped-calls

import configparser
import os
import urllib.parse
from abc import ABC, abstractmethod
from typing import Any, TypeVar

import requests
import sqlalchemy as sa
import sqlalchemy.orm as orm

from . import URLS, exceptions

_C = TypeVar("_C")

_USE_API_SERVER = ["msp", "api", "qps"]
_USE_API_GATEWAY = ["rest"]

_TIMEOUT = 60


class QualysAPIBase:
    """Base class for interacting with the Qualys API.  This class is not intended to be used
    directly, but rather to be subclassed by other classes which implement specific Qualys API
    calls.

    Attributes:
        config_file (str): Path to the config file.  See config-example.ini for an example.
        api_root (str): Root URL of the Qualys API.
        username (str): Username to use when authenticating to the Qualys API.
        password (str): Password to use when authenticating to the Qualys API.
        x_requested_with (str): Value to send in the X-Requested-With header.
        ratelimit_limit (int): Maximum number of requests allowed in the current window. Updated
            after every API call.
        ratelimit_window_sec (int): Length of the current window in seconds. Updated after every
            API call.
        ratelimit_remaining (int): Number of requests remaining in the current window. Updated
            after every API call.
        ratelimit_towait_sec (int): Number of seconds to wait before making another API call.
            Updated after every API call.
        concurrency_limit_limit (int): Maximum number of concurrent requests allowed. Updated
            after every API call.
    """

    def __init__(
        self,
        config_file: str = str(os.path.join(os.path.expanduser("~"), ".qualyspy")),
        x_requested_with: str = "QualysPy Python Library",
    ) -> None:
        """Initializes an instance of the QualysAPIBase class.

        Args:
            config_file (str, optional): Path to the config file.  Defaults to
                ~/.qualyspy.
            x_requested_with (str, optional): Value to send in the X-Requested-With header.

        Raises:
            exceptions.ConfigError: Raised if the config file is missing a required key.
        """

        # Read config file
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        try:
            self.api_server = self.config["AUTHENTICATION"]["api_server"]
            self.api_gateway = self.config["AUTHENTICATION"]["api_gateway"]
            self.username = self.config["AUTHENTICATION"]["username"]
            self.password = self.config["AUTHENTICATION"]["password"]
        except KeyError as e:
            raise exceptions.ConfigError(f"Config file {config_file} missing key: {e}")

        self.jwt: str | None = None

        self.x_requested_with = x_requested_with
        self.orm_base = orm.DeclarativeBase()

        self.ratelimit_limit: int | None = None
        self.ratelimit_window_sec: int | None = None
        self.ratelimit_remaining: int | None = None
        self.ratelimit_towait_sec: int | None = None
        self.concurrency_limit_limit: int | None = None
        self.concurrency_limit_running: int | None = None
        self.get(URLS.about)  # Set ratelimit and concurrency limit

    def _choose_url(self, url: str) -> str:
        """Choose the correct URL to use based on the URL.

        Args:
            url (str): URL to of endpoint being access.

        Returns:
            str: URL to use.
        """

        api_root = url.split("/")[1]

        if api_root in _USE_API_SERVER:
            return self.api_server
        elif api_root in _USE_API_GATEWAY:
            return self.api_gateway
        else:
            raise ValueError("No valid API root or gateway found.")

    def _get_jwt(self) -> None:
        """Get a new JWT from the Qualys API."""
        response = requests.post(
            self.api_gateway + URLS.gateway_auth,
            data={
                "token": "true",
                "username": self.username,
                "password": self.password,
            },
            headers={
                "X-Requested-With": self.x_requested_with,
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise exceptions.QualysAPIError(response.text) from e
        self.jwt = response.text

    def _update_limits(self, response: requests.Response) -> None:
        """Update the rate limit and concurrency limit information.

        Args:
            response (requests.Response): Response object from the Qualys API.
        """

        def _get_updated_limit(headers: Any, name: str) -> int | None:
            """Get the updated limit or return None if the header is not present.

            Args:
                limit (str): Header to get the limit for.
            """

            try:
                return int(headers[name])
            except KeyError:
                return None

        self.ratelimit_limit = _get_updated_limit(response.headers, "X-RateLimit-Limit")
        self.ratelimit_window_sec = _get_updated_limit(
            response.headers, "X-RateLimit-Window"
        )
        self.ratelimit_towait_sec = _get_updated_limit(
            response.headers, "X-RateLimit-ToWait"
        )
        self.ratelimit_remaining = _get_updated_limit(
            response.headers, "X-RateLimit-Remaining"
        )
        self.concurrency_limit_limit = _get_updated_limit(
            response.headers, "X-ConcurrencyLimit"
        )
        self.concurrency_limit_running = _get_updated_limit(
            response.headers, "X-ConcurrencyRunning"
        )

    def get(
        self,
        url: str,
        params: dict[str, str] | None = None,
        accept: str = "application/xml",
    ) -> requests.Response:
        """Send a GET request to the Qualys API.

        Args:
            url (str): URL to send the request to.
            params (dict[str, str], optional): Parameters to send with the request.  Defaults to
                None, which means the API call will use the default parameters.

        Returns:
            The text of the response.

        Raises:
            exceptions.QualysAPIError: Raised if the Qualys API returns a non-200 response.
        """
        root = self._choose_url(url)
        if root == self.api_server:
            response = requests.get(
                root + url,
                params=params,
                auth=(self.username, self.password),
                headers={"X-Requested-With": self.x_requested_with, "Accept": accept},
                timeout=_TIMEOUT,
            )
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                raise exceptions.QualysAPIError(response.text) from e

            self._update_limits(response)
            return response
        elif root == self.api_gateway:
            if self.jwt is None:
                self._get_jwt()
            response = requests.get(
                root + url,
                params=params,
                headers={
                    "X-Requested-With": self.x_requested_with,
                    "Authorization": f"Bearer {self.jwt}",
                },
                timeout=_TIMEOUT,
            )
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                raise exceptions.QualysAPIError(response.text) from e
            self._update_limits(response)
            return response
        else:
            raise ValueError("No valid API root or gateway found.")

    def post(
        self,
        url: str,
        *,
        params: dict[str, str] | None = None,
        data: str | bytes | None = None,
        content_type: str = "application/json",
        accept: str = "application/json",
    ) -> requests.Response:
        """Send a POST request to the Qualys API.

        Args:
            url (str): URL to send the request to.
            data (dict[str, str], optional): Data to send with the request.  Defaults to None,
                which means the API call will use the default parameters.

        Returns:
            The text of the response.

        Raises:
            exceptions.QualysAPIError: Raised if the Qualys API returns a non-200 response.
        """
        root = self._choose_url(url)
        if root == self.api_server:
            response = requests.post(
                root + url,
                data=data,
                auth=(self.username, self.password),
                headers={
                    "X-Requested-With": self.x_requested_with,
                    "Content-Type": content_type,
                    "Accept": accept,
                },
                timeout=_TIMEOUT,
            )
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                raise exceptions.QualysAPIError(response.text) from e
            return response
        elif root == self.api_gateway:
            if self.jwt is None:
                self._get_jwt()
            response = requests.post(
                root + url,
                params=params,
                data=data,
                headers={
                    "X-Requested-With": self.x_requested_with,
                    "Authorization": f"Bearer {self.jwt}",
                    "Content-Type": "application/json",
                },
                timeout=_TIMEOUT,
            )
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                raise exceptions.QualysAPIError(response.text) from e
            self._update_limits(response)
            return response
        else:
            raise ValueError("No valid API root or gateway found.")


class QualysORMMixin(ABC):
    """Mixin class for Qualys API classes that use SQLAlchemy ORM.

    Attributes:
        api (QualysAPIBase): Instance of the QualysAPIBase class.
        orm_base (sqlalchemy.ext.declarative.api.DeclarativeMeta): Base class for all ORM classes.
        db_host (str): Hostname of the PostgreSQL database.
        db_name (str): Name of the PostgreSQL database.
        db_username (str): Username to use to connect to the PostgreSQL database.
        db_password (str): Password to use to connect to the PostgreSQL database.
        e_url (str): SQLAlchemy engine URL.
        engine (sqlalchemy.engine.base.Engine): SQLAlchemy engine.
        echo (bool): Whether or not to echo SQL statements to stdout. Defaults to False.  If changed
            after the engine is created, the engine will automatically update with the new value.
    """

    def __init__(self, api: QualysAPIBase, *, echo: bool = False) -> None:
        """Initializes an instance of the QualysORMMixin class.

        Args:
            api (QualysAPIBase): Instance of the QualysAPIBase class.
            echo (bool, optional): Whether or not to echo SQL statements to stdout.  Defaults to
                False.

        Raises:
            exceptions.ConfigError: Raised if the config file is missing a required key.
        """
        self.api = api
        self.orm_base = api.orm_base
        try:
            self.db_host = api.config["POSTGRESQL"]["host"]
            self.db_name = api.config["POSTGRESQL"]["db_name"]
            self.db_username = api.config["POSTGRESQL"]["username"]
            self.db_password = urllib.parse.quote(api.config["POSTGRESQL"]["password"])
        except KeyError as e:
            raise exceptions.ConfigError(f"Config file missing key: {e}")
        self.e_url = "postgresql:"
        self.e_url += (
            f"//{self.db_username}:{self.db_password}@{self.db_host}/{self.db_name}"
        )
        self.engine = sa.create_engine(self.e_url, echo=echo)

        self.echo = echo

    def init_db(
        self,
    ) -> None:
        """Initialize the database.  Creates the schema and tables if they don't already exist."""
        with self.engine.connect() as conn:
            conn.execute(
                sa.schema.CreateSchema(
                    self.orm_base.metadata.schema, if_not_exists=True
                )
            )
            conn.commit()

        self.orm_base.metadata.create_all(self.engine)

    @abstractmethod
    def load(self, **kwargs: Any) -> None:
        """Load data into the database."""
        ...

    def drop(self) -> None:
        """Drop the database."""
        with self.engine.connect() as conn:
            conn.execute(
                sa.schema.DropSchema(
                    self.orm_base.metadata.schema, cascade=True, if_exists=True
                )
            )
            conn.commit()

    def query(self, stmt: Any, *, echo: bool = False) -> Any:
        """Execute a query against the database.

        Args:
            stmt (Any): SQLAlchemy statement to execute.
            echo (bool, optional): Whether or not to echo SQL statements to stdout.  Defaults to
                False.

        Returns:
            list[_C]: List of objects returned by the query.
        """

        with orm.Session(self.engine) as session:
            results = session.execute(stmt)
            return results.all()

    def __setattr__(self, __name: str, __value: Any) -> None:
        """Set an attribute of the QualysORMMixin class.  If the attribute is "echo", the engine
        attribute is updated with the new value.

        Args:
            __name (str): Name of the attribute to set.
            __value (Any): Value to set the attribute to.
        """
        super().__setattr__(__name, __value)
        if __name == "echo":
            self.engine = sa.create_engine(self.e_url, echo=__value)
