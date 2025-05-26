"""Base classes for intereacting with the Qualys API and the database where information is being
stored.  Primarily used internally by the QualysPy library, but can be used to call APIs which the
library does not yet support.

Typical usage example:
api = QualysAPIBase()
api.get("/msp/about.php")
"""

# For SQLAlchemy:
# mypy: allow-untyped-calls

import datetime
import json
import sys
import urllib.parse
from abc import ABC, abstractmethod
from typing import Any

import httpx
import sqlalchemy as sa
import sqlalchemy.orm as orm
from decouple import config  # type: ignore

from . import URLS, exceptions
from .qualyspy_logging import bootstrap_logger

_USE_API_SERVER = ["msp", "api", "qps"]
_USE_API_GATEWAY = ["rest", "certview"]

_TIMEOUT = httpx.Timeout(120.0, read=300.0)


class QualysAPIBase:
    """Base class for interacting with the Qualys API.  This class is not intended to be used
    directly, but rather to be subclassed by other classes which implement specific Qualys API
    calls.

    Attributes:
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
        self.api_server = str(config("QUALYS_API_SERVER"))
        self.api_gateway = str(config("QUALYS_API_GATEWAY"))
        self.username = str(config("QUALYS_USERNAME"))
        self.password = str(config("QUALYS_PASSWORD"))

        self.jwt: str | None = None

        self.x_requested_with = x_requested_with
        self.orm_base = orm.DeclarativeBase()

        self.ratelimit_limit: int | None = None
        self.ratelimit_window_sec: int | None = None
        self.ratelimit_remaining: int | None = None
        self.ratelimit_towait_sec: int | None = None
        self.concurrency_limit_limit: int | None = None
        self.concurrency_limit_running: int | None = None

        # Set up logging
        self.log = bootstrap_logger()
        self.log.debug(
            "Initialised QualysAPIBase (server=%s, gateway=%s)",
            self.api_server,
            self.api_gateway,
        )

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
        response = httpx.post(
            self.api_gateway + URLS.gateway_auth,
            data={
                "token": "true",
                "permissions": "true",  # Needed by CertView
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
        except httpx.HTTPError as e:
            raise exceptions.QualysAPIError(response.text) from e
        self.jwt = response.text

    def _update_limits(self, response: httpx.Response) -> None:
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

    def _log_http(
        self,
        *,
        method: str,
        params: dict[str, str] | None,
        resp: httpx.Response,
    ) -> None:
        sent_headers = dict(resp.request.headers)
        if "authorization" in sent_headers:
            sent_headers["authorization"] = "<redacted>"
        meta = {
            "method": method,
            "url": str(resp.request.url),
            "status": resp.status_code,
            "params": params,
            "sent_headers": sent_headers,
        }
        # One-line JSON for machines; pretty on DEBUG for humans
        self.log.info(json.dumps(meta, separators=(",", ":")))

    def get(
        self,
        url: str,
        params: dict[str, str] | None = None,
        accept: str = "application/xml",
    ) -> httpx.Response:
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
        headers = {
            "X-Requested-With": self.x_requested_with,
        }
        if root == self.api_server:
            headers["Accept"] = accept
        elif root == self.api_gateway:
            if self.jwt is None:
                self._get_jwt()
            headers["Authorization"] = f"Bearer {self.jwt}"
        else:
            raise ValueError("No valid API root or gateway found.")
        try:
            response = httpx.get(
                root + url,
                params=params,
                auth=(self.username, self.password)
                if root == self.api_server
                else None,
                headers=headers,
                timeout=_TIMEOUT,
            )
        except httpx.ReadTimeout as e:
            raise exceptions.QualysAPIError(
                f"""
                                            Request for {root + url} timed out.
                                            params: {params},
                                            headers: {headers},
                                            timestamp: {datetime.datetime.now()}
                                            """
            ) from e
        try:
            response.raise_for_status()
        except httpx.HTTPError as e:
            raise exceptions.QualysAPIError(response.text) from e

        self._update_limits(response)
        self._log_http(method="GET", params=params, resp=response)
        return response

    def post(
        self,
        url: str,
        *,
        params: dict[str, str] | None = None,
        content: str | bytes | None = None,
        data: dict[str, str] | None = None,
        files: dict[str, Any] | None = None,
        content_type: str | None = "application/json",
        accept: str = "application/json",
    ) -> httpx.Response:
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
        headers: dict[str, str] = {
            "X-Requested-With": self.x_requested_with,
        }
        if content_type is not None:
            headers["Content-Type"] = content_type
        if root == self.api_server:
            headers["Accept"] = accept
        elif root == self.api_gateway:
            if self.jwt is None:
                self._get_jwt()
            headers["Authorization"] = f"Bearer {self.jwt}"
        else:
            raise ValueError("No valid API root or gateway found.")
        try:
            response = httpx.post(
                root + url,
                params=params,
                content=content,
                data=data,
                files=files,
                auth=(self.username, self.password)
                if root == self.api_server
                else None,
                headers=headers,
                timeout=_TIMEOUT,
            )
        except httpx.ReadTimeout as e:
            raise exceptions.QualysAPIError(
                f"""
                                            Request for {root + url} timed out.
                                            params: {params},
                                            data: {data!r},
                                            headers: {headers},
                                            timestamp: {datetime.datetime.now()}
                                            """
            ) from e
        try:
            response.raise_for_status()
        except httpx.HTTPError as e:
            raise exceptions.QualysAPIError(response.text) from e

        self._update_limits(response)
        self._log_http(method="POST", params=params, resp=response)
        return response


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
            self.db_host = str(config("PG_HOST"))
            self.db_name = str(config("PG_DB"))
            self.db_username = str(config("PG_USERNAME"))
            self.db_password = urllib.parse.quote(str(config("PG_PASSWORD")))
        except KeyError as e:
            raise exceptions.ConfigError(f"Config file missing key: {e}")
        self.e_url = "postgresql+psycopg:"
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
            if self.orm_base.metadata.schema is None:
                raise exceptions.ConfigError("Schema not set in ORM base.")
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

    def load_safe(self, **kwargs: Any) -> None:
        """Safely load data by creating a temporary schema if the base schema exists,
        loading data there, and rolling back in case of error. If loading succeeds,
        replace the old schema with the new one.
        """
        base_schema = self.orm_base.metadata.schema
        if not base_schema:
            raise exceptions.ConfigError("Schema not set in ORM base.")

        # Check if base_schema already exists
        with self.engine.connect() as conn:
            schema_exists = (
                conn.execute(
                    sa.text("""
                    SELECT 1
                    FROM information_schema.schemata
                    WHERE schema_name = :schema
                """),
                    {"schema": base_schema},
                ).scalar()
                is not None
            )

        # If the base schema doesn't exist, just use normal init + load
        if not schema_exists:
            self.init_db()
            try:
                self.load(**kwargs)
            except Exception as e:
                print(e, file=sys.stderr)
            return

        # If the base schema does exist, create a temp schema with a timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        temp_schema = f"{base_schema}_{timestamp}"

        # Create the new temp schema at the database level
        with self.engine.connect() as conn:
            conn.execute(sa.schema.CreateSchema(temp_schema))
            conn.commit()

        self.engine = self.engine.execution_options(
            schema_translate_map={base_schema: temp_schema}
        )

        try:
            # Create the tables in the temp schema
            self.orm_base.metadata.create_all(self.engine)

            # Attempt the data load in the temp schema
            self.load(**kwargs)

        except Exception as e:
            # Drop the temp schema if any error occurs
            with self.engine.connect() as conn:
                conn.execute(sa.schema.DropSchema(temp_schema, cascade=True))
                conn.commit()
            self.engine = self.engine.execution_options(
                schema_translate_map={base_schema: base_schema}
            )
            print(e, file=sys.stderr)
            return

        # If load is successful, drop the old schema and rename the temp to the old name
        with self.engine.connect() as conn:
            conn.execute(sa.schema.DropSchema(base_schema, cascade=True))
            # Rename the temp schema to the original base schema
            conn.execute(
                sa.text(f"ALTER SCHEMA {temp_schema} RENAME TO {base_schema}"),
            )
            conn.commit()

        # Revert the engine to use the original base schema
        self.engine = self.engine.execution_options(
            schema_translate_map={base_schema: base_schema}
        )

    def drop(self) -> None:
        """Drop the database."""
        with self.engine.connect() as conn:
            if self.orm_base.metadata.schema is None:
                raise exceptions.ConfigError("Schema not set in ORM base.")
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
