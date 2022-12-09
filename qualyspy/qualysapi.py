"""Python wrapper for the Qualys API.

This is the main file of the wrapper which includes the functionality to establish a connection to
the API endpoint and use the other modules.

Example:
    conn = qualysapi.Connection()
"""

import configparser
import importlib.resources
import io
import json
import os.path
import re
from collections.abc import Mapping
from typing import Any, Optional, TextIO, Union

import lxml.objectify
import requests

CONFIG_FILE = os.path.expanduser("~/qualysapi.conf")
URLS = json.load(importlib.resources.files("qualyspy").joinpath("urls.json").open())

config = configparser.ConfigParser()
config.read(CONFIG_FILE)
API_ROOT = config["AUTHENTICATION"]["api_root"]
CREDENTIALS = {
    "username": config["AUTHENTICATION"]["username"],
    "password": config["AUTHENTICATION"]["password"],
}


class Qualys_API_Error(Exception):
    """Exception raised when the Qualys API returns a non-200 response."""


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
            "username": CREDENTIALS["username"],
            "password": CREDENTIALS["password"],
        }
        conn = requests.post(
            API_ROOT + URLS["Session Login"], headers=self.headers, data=data
        )
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
        requests.post(
            API_ROOT + URLS["Session Logout"],
            headers=self.headers,
            cookies=self._cookies,
        )

    def _perform_request(
        self, method: str, path: str, params: Optional[Mapping[str, Any]] = None
    ) -> str:
        """Helper method for "request" methods.  Performs the API request and returns the text as
        a string, to be parsed by the calling function.

        Args:
            method:
                The method of the request (ex. get, post)
            path:
                The path of the API request. ex. /api/2.0/fo/scan/?action=list
            params:
                An optional dictionary of request parameters, the contents of which depend
                on the particular API request being made.

        Returns:
            A string containing the text of the API response.
        """

        match method:
            case "get":
                response = requests.get(
                    API_ROOT + path,
                    headers=self.headers,
                    cookies=self._cookies,
                    params=params,
                )
            case "post":
                response = requests.post(
                    API_ROOT + path,
                    headers=self.headers,
                    cookies=self._cookies,
                    params=params,
                )
            case _:
                raise ValueError(f"{method} is not a supported")

        if response.status_code != requests.codes.ok:
            status_code = response.status_code
            reason = response.reason
            url = response.url
            text = response.text
            err = f"{status_code} error: {reason} for url: {url}\n\n{text}"
            self.__del__()
            raise Qualys_API_Error(err)

        return response.text

    def _request(
        self,
        method: str,
        path: str,
        params: Optional[Mapping[str, Any]] = None,
    ) -> lxml.objectify.ObjectifiedElement:
        """Performs an API request to the connection for a given API path and returns the result.

        Args:
            method:
                The method of the request (ex. get, post)
            path:
                The path of the API request. ex. /api/2.0/fo/scan/?action=list
            params:
                An optional dictionary of request parameters, the contents of which depend
                on the particular API request being made.

        Returns:
            An lxml.objectify object of the XML output of the API request.
        """

        response = self._perform_request(method, path, params)

        return lxml.objectify.fromstring(re.split("\n", response, 1)[1])

    def get(
        self,
        path: str,
        params: Optional[Mapping[str, Any]] = None,
    ) -> lxml.objectify.ObjectifiedElement:
        """Performs an GET request to the connection for a given API path and returns the result.

        Normally, it is not intended that this function be called manually.  Instead, this would be
        run by functions in other modules of this package.  However, this method is
        considered part of the public interface to cover any API functions which are not currently
        implemented in this package.

        Args:
            path:
                The path of the API request. ex. /api/2.0/fo/scan/?action=list
            params:
                An optional dictionary of request parameters, the contents of which depend
                on the particular API request being made.

        Returns:
            An lxml.objectify object of the XML output of the API request.
        """

        return self._request("get", path, params)

    def post(
        self,
        path: str,
        params: Optional[Mapping[str, Any]] = None,
    ) -> lxml.objectify.ObjectifiedElement:
        """Performs an POST request to the connection for a given API path and returns the result.

        Normally, it is not intended that this function be called manually.  Instead, this would be
        run by functions in other modules of this package.  However, this method is
        considered part of the public interface to cover any API functions which are not currently
        implemented in this package.

        Args:
            path:
                The path of the API request. ex. /api/2.0/fo/scan/?action=list
            params:
                An optional dictionary of request parameters, the contents of which depend
                on the particular API request being made.

        Returns:
            An lxml.objectify object of the XML output of the API request.
        """

        return self._request("post", path, params)

    def _request_file(
        self,
        method: str,
        path: str,
        params: Optional[Mapping[str, Any]] = None,
        output_file: Optional[Union[str, TextIO]] = None,
    ) -> None:
        """Performs an API request to the connection for a given API path and writes the result to
        a file.

        Args:
            method:
                The method of the request (ex. get, post)
            path:
                The path of the API request. ex. /api/2.0/fo/scan/?action=list
            params:
                An optional dictionary of request parameters, the contents of which depend
                on the particular API request being made.
            output_file:
                A file object or path for the API response to be written to.

        Returns:
            A handle to a file containing the response text.
        """

        response = self._perform_request(method, path, params)

        if isinstance(output_file, io.IOBase):
            f = output_file
        elif isinstance(output_file, str):
            f = open(output_file, "w", newline="")
        else:
            raise ValueError("invalid file object or name")
        f.write(response)
        f.close()

    def get_file(
        self,
        path: str,
        params: Optional[Mapping[str, Any]] = None,
        output_file: Optional[Union[str, TextIO]] = None,
    ) -> None:
        """Performs an GET request to the connection for a given API path and writes the result to
        a file.

        Normally, it is not intended that this function be called manually.  Instead, this would be
        run by functions in other modules of this package.  However, this method is
        considered part of the public interface to cover any API functions which are not currently
        implemented in this package.

        Args:
            path:
                The path of the API request. ex. /api/2.0/fo/scan/?action=list
            params:
                An optional dictionary of request parameters, the contents of which depend
                on the particular API request being made.
            output_file:
                A file object or path for the API response to be written to.

        Returns:
            A handle to a file containing the response text.
        """

        self._request_file("get", path, params, output_file)

    def post_file(
        self,
        path: str,
        params: Optional[Mapping[str, Any]] = None,
        output_file: Optional[Union[str, TextIO]] = None,
    ) -> None:
        """Performs an POST request to the connection for a given API path and writes the result to
        a file.

        Normally, it is not intended that this function be called manually.  Instead, this would be
        run by functions in other modules of this package.  However, this method is
        considered part of the public interface to cover any API functions which are not currently
        implemented in this package.

        Args:
            path:
                The path of the API request. ex. /api/2.0/fo/scan/?action=list
            params:
                An optional dictionary of request parameters, the contents of which depend
                on the particular API request being made.
            output_file:
                A file object or path for the API response to be written to.

        Returns:
            A handle to a file containing the response text.
        """

        self._request_file("post", path, params, output_file)
