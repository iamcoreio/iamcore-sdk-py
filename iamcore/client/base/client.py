from __future__ import annotations

from enum import Enum
from typing import Optional, Union
from urllib.parse import urljoin

import requests

from iamcore.client.exceptions import IAMUnauthorizedException

from .exception_handler import ResponseHandler


class HTTPMethod(str, Enum):
    """HTTP methods."""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class APIVersion(str, Enum):
    """API version."""

    V1 = "api/v1"


class HTTPClientWithTimeout:
    """HTTP client with timeout."""

    def __init__(
        self,
        base_url: str,
        timeout: int = 30,
        api_version: Optional[APIVersion] = APIVersion.V1,
    ) -> None:
        self.base_url: str = base_url
        if api_version:
            self.base_url = append_path_to_url(self.base_url, api_version)
        self.timeout: int = timeout

    def _request(
        self,
        method: HTTPMethod,
        path: str,
        *,
        data: Optional[Union[str, bytes]] = None,
        headers: Optional[dict[str, str]] = None,
        params: Optional[Union[str, dict[str, Union[str, int, bool]]]] = None,
    ) -> requests.Response:
        """Make a request to the HTTP server."""
        if not headers:
            msg = "Missing authorization headers"
            raise IAMUnauthorizedException(msg)

        if "Content-Type" not in headers:
            headers["Content-Type"] = "application/json"

        url = append_path_to_url(self.base_url, path)
        resp = requests.request(
            method,
            url,
            data=data,
            headers=headers,
            timeout=self.timeout,
            params=params,
        )
        return ResponseHandler.handle_response(resp)

    def _get(
        self,
        path: str = "",
        *,
        data: Optional[Union[str, bytes]] = None,
        headers: Optional[dict[str, str]] = None,
        params: Optional[Union[str, dict[str, Union[str, int, bool]]]] = None,
    ) -> requests.Response:
        """Make a GET request to the HTTP server."""
        return self._request(HTTPMethod.GET, path, data=data, headers=headers, params=params)

    def _post(
        self,
        path: str = "",
        *,
        data: Optional[Union[str, bytes]] = None,
        headers: Optional[dict[str, str]] = None,
        params: Optional[Union[str, dict[str, Union[str, int, bool]]]] = None,
    ) -> requests.Response:
        """Make a POST request to the HTTP server."""
        return self._request(HTTPMethod.POST, path, data=data, headers=headers, params=params)

    def _put(
        self,
        path: str = "",
        *,
        data: Optional[Union[str, bytes]] = None,
        headers: Optional[dict[str, str]] = None,
        params: Optional[Union[str, dict[str, Union[str, int, bool]]]] = None,
    ) -> requests.Response:
        """Make a PUT request to the HTTP server."""
        return self._request(HTTPMethod.PUT, path, data=data, headers=headers, params=params)

    def _patch(
        self,
        path: str = "",
        *,
        data: Optional[Union[str, bytes]] = None,
        headers: Optional[dict[str, str]] = None,
        params: Optional[Union[str, dict[str, Union[str, int, bool]]]] = None,
    ) -> requests.Response:
        """Make a PATCH request to the HTTP server."""
        return self._request(HTTPMethod.PATCH, path, data=data, headers=headers, params=params)

    def _delete(
        self,
        path: str = "",
        *,
        data: Optional[Union[str, bytes]] = None,
        headers: Optional[dict[str, str]] = None,
        params: Optional[Union[str, dict[str, Union[str, int, bool]]]] = None,
    ) -> requests.Response:
        """Make a DELETE request to the HTTP server."""
        return self._request(HTTPMethod.DELETE, path, data=data, headers=headers, params=params)


def append_path_to_url(base_url: str, segment: str) -> str:
    """
    Safely appends a path segment to a URL.

    This function ensures that the segment is always appended as a new
    part of the URL path, regardless of whether the base_url ends
    with a forward slash.

    Args:
        base_url: The starting URL (e.g., "http://example.com/foo").
        segment: The path segment to append (e.g., "bar").

    Returns:
        The new URL with the appended path (e.g., "http://example.com/foo/bar").
    """
    if not segment:
        return base_url

    # Ensure the base URL has a trailing slash for correct joining.
    if not base_url.endswith("/"):
        base_url += "/"

    # urljoin will now correctly append the segment to the "directory" path.
    return urljoin(base_url, segment)
