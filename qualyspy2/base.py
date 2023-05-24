import configparser
import os
import requests

from . import exceptions


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
