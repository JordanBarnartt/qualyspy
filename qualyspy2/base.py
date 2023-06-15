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
    def __init__(
        self,
        config_file: str = str(
            os.path.join(os.path.expanduser("~"), "etc", "qualyspy", "config.ini")
        ),
        x_requested_with: str = "QualysPy Python Library",
    ) -> None:
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
    def __init__(self, api: QualysAPIBase, *, echo: bool = False) -> None:
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
        ...

    def query(self, stmt: Any, *, echo: bool = False) -> list[_C]:
        output: list[_C] = []
        with orm.Session(self.engine) as session:
            results = session.execute(stmt)
            for result in results.all():
                r = result.tuple()[0]
                i = qutils.from_orm_object(r)
                output.append(i)

        return output

    def __setattr__(self, __name: str, __value: Any) -> None:
        super().__setattr__(__name, __value)
        if __name == "echo":
            self.engine = sa.create_engine(self.e_url, echo=__value)
