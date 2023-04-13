"""Python wrapper for the Qualys API.

This is the main file of the wrapper which includes the functionality to establish a connection to
the API endpoint and use the other modules.

Example:
    conn = qualysapi.Connection()
"""

import io
import json
import re
from collections.abc import MutableMapping, MutableSequence
from typing import Any, Optional, TextIO, Union

import lxml.objectify
import requests

import ssl
import urllib3

from . import qutils

JSON_IN_JSON_OUT_HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}
JSON_IN_XML_OUT_HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/xml",
}


class CustomHttpAdapter(requests.adapters.HTTPAdapter):
    """Transport adapter" that allows us to use custom ssl_context.

    Workaround because Qualys API Gateway URL does not support Secure Renegotation, which is
    enforced in OpenSSL 3.X.  Reference:
    https://stackoverflow.com/questions/71603314/ssl-error-unsafe-legacy-renegotiation-disabled
    """

    def __init__(
        self, ssl_context: Optional[ssl.SSLContext] = None, **kwargs: Any
    ) -> None:
        self.ssl_context = ssl_context
        super().__init__(**kwargs)

    def init_poolmanager(
        self, connections: Any, maxsize: Any, block: bool = False, **kwargs: Any
    ) -> None:
        self.poolmanager = urllib3.poolmanager.PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_context=self.ssl_context,
        )


API_ROOT = qutils.config["AUTHENTICATION"]["api_root"]
API_GATEWAY_ROOT = qutils.config["AUTHENTICATION"]["api_gateway_root"]
CREDENTIALS = {
    "username": qutils.config["AUTHENTICATION"]["username"],
    "password": qutils.config["AUTHENTICATION"]["password"],
}


class Qualys_API_Error(Exception):
    """Exception raised when the Qualys API returns a non-200 response, or some other error."""


class Connection:
    """A connection to a Qualys API endpoint.

    When an object of this class is removed from memory, a logout API request will be made.

    Attributes:
        add_headers:
            A dictionary containing the headers passed into API requests.  If
            "X-Requested-With" is not specified, it will be included with the value
            "qualyspy python package".
        apis:
            Specifies which APIs should be authenticated to (since many Qualys APIs use different
            authentication methods).  By default, on the VMDR API will be connected to.
            Possible options include: VMDR, Asst_Mgmt_Tagging, CertView
    """

    def _connect_VMDR(
        self,
        /,
        add_headers: Optional[MutableMapping[str, str]] = None,
    ) -> None:
        """Connect to the VMDR API.  Updates the cookies attribute of the class with the auth
        cookie to be automatically used with any VMDR API calls.
        """

        # Add to self._headers as this should be included on all future VMDR API calls
        self._headers["X-Requested-With"] = "qualyspy python package"

        data = {
            "username": CREDENTIALS["username"],
            "password": CREDENTIALS["password"],
        }
        conn = requests.post(
            API_ROOT + qutils.URLS["Session Login"], headers=self._headers, data=data
        )
        if conn.status_code == requests.codes.ok:
            self._cookies["QualysSession"] = conn.cookies["QualysSession"]
            with open("debug/cookies.txt", "a") as f:
                f.write(str(conn.cookies["QualysSession"]) + "\n")
        else:
            print(conn.headers)
            conn.raise_for_status()

    def _connect_CertView(self) -> None:
        """Connects to the CertView API.  Adds a bearer token attribute to the class to be
        automatically used with any CertView API calls.
        """

        data = {
            "username": CREDENTIALS["username"],
            "password": CREDENTIALS["password"],
            "token": "true",
            "permissions": "true",
        }
        headers = {"ContentType": "application/x-www-form-urlencoded"}

        with requests.Session() as s:
            ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            ctx.options |= 0x4
            s.mount("https://", CustomHttpAdapter(ctx))
            conn = s.post(
                API_GATEWAY_ROOT + qutils.URLS["CertView Authentication"],
                headers=headers,
                data=data,
            )
        self._bearer_token = conn.text

    def register_in_out_headers(
        self, api_match: str, in_header: str, out_header: str
    ) -> None:
        """Registers the 'Accept' and 'Content-Type' headers for a given API path.

        Args:
            api_match:
                The portion of the API url to which the registration applies,
                ex. '/qps/rest/2.0/' or '/certview/'
            in_header:
                The 'Accept' header to be used for this API endpoint.
            out_header:
                The 'Content-Type' header to be used for this API endpoint.
        """
        self._in_out_headers[api_match] = {
            "Accept": in_header,
            "Content-Type": out_header,
        }

    def __init__(
        self,
        /,
        add_headers: Optional[MutableMapping[str, str]] = None,
        apis: MutableSequence[str] = ["VMDR"],
    ) -> None:
        """Instantiates a Connection object.

        Using the credentials in the configuration file, connect to the Qualys API endpoint
        obtain a session key to use in future API requests.

        Raises:
            HTTPError: An error occured when connecting to the API endpoint.
        """

        self._cookies: dict[str, str] = {}
        self._headers: dict[str, str] = {}
        self._bearer_token = ""

        self._in_out_headers: dict[str, dict[str, str]] = {}
        self.register_in_out_headers(
            "/api/2.0/fo/", "application/json", "application/xml"
        )
        self.register_in_out_headers(
            "/qps/rest/2.0/", "application/json", "application/json"
        )
        self.register_in_out_headers(
            "/certview/v2/certificates", "application/json", "application/json"
        )

        if "VMDR" in apis:
            self._connect_VMDR()
        if "CertView" in apis:
            self._connect_CertView()

    def __del__(self) -> None:
        """Deletes a Connection object.

        Perform an API request to logout of the session to avoid API limits.
        """
        requests.post(
            API_ROOT + qutils.URLS["Session Logout"],
            headers=self._headers,
            cookies=self._cookies,
        )

    def _perform_request(
        self,
        method: str,
        path: str,
        params: Optional[MutableMapping[str, Any]] = None,
        data: Optional[Union[MutableMapping[str, Any], str]] = None,
        /,
        add_headers: MutableMapping[str, str] = {},
    ) -> str:
        """Helper method for "request" methods.  Performs the API request and returns the text as
        a string, to be parsed by the calling function.
        """

        headers = self._headers
        headers.update(add_headers)

        root = API_ROOT
        if "/certview/" in path:
            root = API_GATEWAY_ROOT
            headers["Authorization"] = "Bearer " + self._bearer_token

        auth = None
        if "/qps/" in path:
            auth = (CREDENTIALS["username"], CREDENTIALS["password"])

        match method:
            case "get":
                response = requests.get(
                    root + path,
                    headers=headers,
                    cookies=self._cookies,
                    params=params,
                    auth=auth,
                )
            case "post":
                if "/certview/" in path:
                    with requests.Session() as s:
                        ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
                        ctx.options |= 0x4
                        s.mount("https://", CustomHttpAdapter(ctx))
                        response = s.post(
                            root + path,
                            headers=headers,
                            cookies=self._cookies,
                            data=data,
                            auth=auth,
                        )
                else:
                    response = requests.post(
                        root + path,
                        headers=headers,
                        cookies=self._cookies,
                        data=data,
                        auth=auth,
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
        /,
        params: Optional[MutableMapping[str, Any]] = None,
        data: Optional[Union[MutableMapping[str, Any], str]] = None,
        add_headers: MutableMapping[str, str] = {},
    ) -> Any:
        """Performs an API request to the connection for a given API path and returns the result.

        Args:
            method:
                The method of the request (ex. get, post)
            path:
                The path of the API request. ex. /api/2.0/fo/scan/?action=list
            params:
                An optional dictionary of request parameters, the contents of which depend
                on the particular API request being made. Valid for GET requests only.
            data:
                A dictionary of information to be sent in the body of a POST request.
            use_auth:
                Use auth for authentication, rather than cookies. Which to use depends on the API
                being called.

        Returns:
            An lxml.objectify object of the XML output of the API request.
        """
        for api in self._in_out_headers:
            if path.startswith(api):
                add_headers.update(self._in_out_headers[api])

        response = self._perform_request(
            method, path, params, data, add_headers=add_headers
        )

        match add_headers["Content-Type"]:
            case "application/xml":
                xml = lxml.objectify.fromstring(re.split("\n", response, 1)[1])
                return xml
            case "application/json":
                if "qps" in path:
                    return json.loads(response)["ServiceResponse"]
                return json.loads(response)
            case _:
                return response

    def get(
        self,
        path: str,
        params: Optional[MutableMapping[str, Any]] = None,
        *,
        add_headers: MutableMapping[str, str] = {},
    ) -> Any:
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
            add_headers:
                Include additional headers in the request. These headers will not persist to the
                next request.

        Returns:
            An lxml.objectify object of the XML output of the API request.
        """

        return self._request("get", path, params=params, add_headers=add_headers)

    def post(
        self,
        path: str,
        data: Optional[Union[MutableMapping[str, Any], str]] = None,
        *,
        add_headers: MutableMapping[str, str] = {},
    ) -> Any:
        """Performs an POST request to the connection for a given API path and returns the result.

        Normally, it is not intended that this function be called manually.  Instead, this would be
        run by functions in other modules of this package.  However, this method is
        considered part of the public interface to cover any API functions which are not currently
        implemented in this package.

        Args:
            path:
                The path of the API request. ex. /api/2.0/fo/scan/?action=list
            data:
                A dictionary of information to be sent in the body of a POST request.
            add_headers:
                Include additional headers in the request. These headers will not persist to the
                next request.

        Returns:
            An lxml.objectify object of the XML output of the API request.
        """

        return self._request(
            "post",
            path,
            data=json.dumps(data),
            add_headers=add_headers,
        )

    def _request_file(
        self,
        method: str,
        path: str,
        params: Optional[MutableMapping[str, Any]] = None,
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
        params: Optional[MutableMapping[str, Any]] = None,
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
        params: Optional[MutableMapping[str, Any]] = None,
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
