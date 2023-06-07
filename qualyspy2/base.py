import configparser
import os
from typing import Callable, Any
from multiprocessing import Process

import requests
import sqlalchemy as sa
import sqlalchemy.orm as orm

from . import exceptions
from . import URLS


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
        self.api_root = self.config["AUTHENTICATION"]["api_root"]
        self.username = self.config["AUTHENTICATION"]["username"]
        self.password = self.config["AUTHENTICATION"]["password"]

        self.x_requested_with = x_requested_with

        self.ratelimit_limit: int | None = None
        self.ratelimit_window_sec: int | None = None
        self.ratelimit_remaining: int | None = None
        self.ratelimit_towait_sec: int | None = None
        self.concurrency_limit_limit: int | None = None
        self.concurrency_limit_running: int | None = None
        self.get(URLS.about) # Set ratelimit and concurrency limit

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
        self.concurrency_limit_limit = int(response.headers["X-Concurrency-Limit-Limit"])
        self.concurrency_limit_running = int(response.headers["X-Concurrency-Limit-Running"])

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


class QualysORMBase:
    def __init__(self, api: QualysAPIBase, *, echo: bool = False) -> None:
        self.api = api
        self.echo = echo
        self.db_host = api.config["DATABASE"]["host"]
        self.db_name = api.config["DATABASE"]["name"]
        self.db_username = api.config["DATABASE"]["username"]
        self.db_password = api.config["DATABASE"]["password"]
        self.e_url = f"postgresql://{self.db_name}:{self.db_password}@{self.db_host}/{self.db_name}"
        self.engine = sa.create_engine(self.e_url, echo=echo)

    def _init_db(
        self,
        api_func: Callable[..., Any],
        orm_base: orm.DeclarativeBase,
    ) -> None:
        with self.engine.connect() as conn:
            conn.execute(
                sa.schema.CreateSchema(orm_base.metadata.schema, if_not_exists=True)
            )
            conn.commit()

        orm_base.metadata.create_all(self.engine)

    def _load(self, batch_size) -> None:
        

    def __setattr__(self, __name: str, __value: Any) -> None:
        super().__setattr__(__name, __value)
        if __name == "echo":
            self.engine = sa.create_engine(self.e_url, echo=__value)
