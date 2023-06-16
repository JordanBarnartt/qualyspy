"""Base classes for intereacting with the Qualys API and the database where information is being
stored.  Primarily used internally by the QualysPy library, but can be used to call APIs which the
library does not yet support.

Typical usage example:
api = QualysAPIBase()
api.get("/msp/about.php")
"""

import configparser
import datetime
import os
from abc import ABC, abstractmethod
from typing import Any, Callable, TypeVar

import requests
import sqlalchemy as sa
import sqlalchemy.orm as orm

from . import URLS, exceptions, qutils

_C = TypeVar("_C")


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
        config_file: str = str(
            os.path.join(os.path.expanduser("~"), "etc", "qualyspy", "config.ini")
        ),
        x_requested_with: str = "QualysPy Python Library",
    ) -> None:
        """Initializes an instance of the QualysAPIBase class.

        Args:
            config_file (str, optional): Path to the config file.  Defaults to
                ~/etc/qualyspy/config.ini.
            x_requested_with (str, optional): Value to send in the X-Requested-With header.

        Raises:
            exceptions.ConfigError: Raised if the config file is missing a required key.
        """

        # Read config file
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        try:
            self.api_root = self.config["AUTHENTICATION"]["api_root"]
            self.username = self.config["AUTHENTICATION"]["username"]
            self.password = self.config["AUTHENTICATION"]["password"]
        except KeyError as e:
            raise exceptions.ConfigError(f"Config file missing key: {e}")

        self.x_requested_with = x_requested_with
        self.orm_base = orm.DeclarativeBase()

        self.ratelimit_limit: int | None = None
        self.ratelimit_window_sec: int | None = None
        self.ratelimit_remaining: int | None = None
        self.ratelimit_towait_sec: int | None = None
        self.concurrency_limit_limit: int | None = None
        self.concurrency_limit_running: int | None = None
        self.get(URLS.about)  # Set ratelimit and concurrency limit

    def get(self, url: str, params: dict[str, str] | None = None) -> str:
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
        response = requests.get(
            self.api_root + url,
            params=params,
            auth=(self.username, self.password),
            headers={"X-Requested-With": self.x_requested_with},
        )
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise exceptions.QualysAPIError(response.text) from e

        self.ratelimit_limit = int(response.headers["X-RateLimit-Limit"])
        self.ratelimit_window_sec = int(response.headers["X-RateLimit-Window-Sec"])
        self.ratelimit_remaining = int(response.headers["X-RateLimit-Remaining"])
        self.ratelimit_towait_sec = int(response.headers["X-RateLimit-ToWait-Sec"])
        self.concurrency_limit_limit = int(
            response.headers["X-Concurrency-Limit-Limit"]
        )
        self.concurrency_limit_running = int(
            response.headers["X-Concurrency-Limit-Running"]
        )

        return response.text

    def post(self, url: str, data: dict[str, str] | None = None) -> str:
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
        response = requests.post(
            self.api_root + url,
            data=data,
            auth=(self.username, self.password),
            headers={"X-Requested-With": self.x_requested_with},
        )
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise exceptions.QualysAPIError(response.text) from e
        return response.text


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
            self.db_password = api.config["POSTGRESQL"]["password"]
        except KeyError as e:
            raise exceptions.ConfigError(f"Config file missing key: {e}")
        self.e_url = f"postgresql://{self.db_name}:{self.db_password}@{self.db_host}/{self.db_name}"
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

    def safe_load(
        self,
        loader: Callable[..., Any],
        load_func: Any,
        **kwargs: dict[str, Any],
    ) -> None:
        """Safely load data into the database.  If an exception is raised, the database is
        reverted to its previous state.

        Args:
            loader (Callable[..., Any]): Function which loads data into the database.
            load_func (Any): Function which returns the data to load into the database.
            **kwargs (dict[str, Any]): Keyword arguments to pass to the loader function.
        """
        self.init_db()
        now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        schema = self.orm_base.metadata.schema
        with orm.Session(self.engine) as session:
            alter_schema = sa.DDL(f"ALTER SCHEMA {schema} RENAME TO {schema}_{now}")
            session.execute(alter_schema)
            session.commit()
        try:
            self.init_db()
            loader(load_func, **kwargs)
        except Exception as e:
            with self.engine.connect() as conn:
                conn.execute(sa.schema.DropSchema(schema, cascade=True))
                conn.commit()
            with orm.Session(self.engine) as session:
                revert_schema = sa.DDL(
                    f"ALTER SCHEMA {schema}_{now} RENAME TO {schema}"
                )
                session.execute(revert_schema)
                session.commit()
            raise e

    @abstractmethod
    def load(self) -> None:
        """Load data into the database."""
        ...

    def query(self, stmt: Any, *, echo: bool = False) -> list[_C]:
        """Execute a query against the database.

        Args:
            stmt (Any): SQLAlchemy statement to execute.
            echo (bool, optional): Whether or not to echo SQL statements to stdout.  Defaults to
                False.

        Returns:
            list[_C]: List of objects returned by the query.
        """
        output: list[_C] = []
        with orm.Session(self.engine) as session:
            results = session.execute(stmt)
            for result in results.all():
                r = result.tuple()[0]
                i = qutils.from_orm_object(r)
                output.append(i)

        return output

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
