"""Python wrapper for the Qualys API.

This is the main file of the wrapper which includes the functionality to establish a connection to
the API endpoint and use the other modules.

Example:
    conn = qualysapi.Connection()

    scans = conn.run(modules.vm_scans.get_scans)
"""

import configparser
import lxml.objectify
import re
import requests
import os.path

from collections.abc import Mapping
from typing import Any, Optional

CONFIG_FILE = os.path.expanduser("~") + "/qualysapi.conf"

config = configparser.ConfigParser()
config.read(CONFIG_FILE)
API_ROOT = config["AUTHENTICATION"]["api_root"]
CREDENTIALS = {
    "username": config["AUTHENTICATION"]["username"],
    "password": config["AUTHENTICATION"]["password"],
}


class Connection:
    """A connection to a Qualys API endpoint.

    When an object of this class is removed from memory, a logout API request will be made.
    """

    headers = {"X-Requested-With": "qualysapi python package"}
    """A dictionary containing the headers passed into API requests."""

    def __init__(self) -> None:
        """Instantiates a Connection object.

        Using the credentials in the configuration file, connect to the Qualys API endpoint
        obtain a session key to use in future API requests.  Updates the cookies attribute of the
        class.

        Raises:
            HTTPError: An error occured when connecting to the API endpoint.
        """
        data = {
            "action": "login",
            "username": CREDENTIALS["username"],
            "password": CREDENTIALS["password"],
        }
        conn = requests.post(API_ROOT + "fo/session/", headers=self.headers, data=data)
        if conn.status_code == requests.codes.ok:
            self._cookies = {"QualysSession": conn.cookies["QualysSession"]}
            with open("debug/cookies.txt", "a") as f:
                f.write(str(conn.cookies["QualysSession"]) + "\n")
        else:
            print(conn.headers)
            conn.raise_for_status()

    def __del__(self) -> None:
        """Deletes a Connection object.

        Perform an API request to logout of the session to avoid API limits.
        """
        data = {"action": "logout"}
        requests.post(
            API_ROOT + "fo/session/",
            headers=self.headers,
            data=data,
            cookies=self._cookies,
        )

    def request(
        self, method: str, path: str, params: Optional[Mapping[str, Any]] = None
    ) -> lxml.objectify.ObjectifiedDataElement:
        """Performs an API request to the connection for a given API path and returns the result.

        Normally, it is not intended that this function be called manually.  Instead, this would be
        run by functions in other modules of this package.  However, this method is
        considered part of the public interface to cover any API functions which are not currently
        implemented in this package.

        Args:
            path: The path of the API request. ex. /api/2.0/fo/scan/?action=list
            params: An optional dictionary of request parameters, the contents of which depend
                on the particular API request being made.

        Returns:
            An lxml.objectify object of the XML output of the API request.
        """

        match method:
            case "get":
                conn = requests.get(
                    API_ROOT + path, headers=self.headers, cookies=self._cookies, params=params
                )
            case "post":
                conn = requests.post(
                    API_ROOT + path, headers=self.headers, cookies=self._cookies, params=params
                )
            case _:
                raise ValueError(f"{method} is not a supported")
        return lxml.objectify.fromstring(re.split("\n", conn.text, 1)[1])
