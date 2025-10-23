from __future__ import annotations

from enum import Enum

import requests

from iamcore.client.exceptions import IAMUnauthorizedException


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
        api_version: APIVersion = APIVersion.V1,
    ) -> None:
        self.base_url: str = base_url if base_url.endswith("/") else base_url + "/"
        self.base_url = self.base_url + api_version.value
        self.timeout: int = timeout

    def request(
        self,
        method: HTTPMethod,
        path: str,
        *,
        data: str | bytes | None = None,
        headers: dict[str, str] | None = None,
        params: str | dict[str, str | int | bool] | None = None,
    ) -> requests.Response:
        """Make a request to the HTTP server."""
        if not headers:
            msg = "Missing authorization headers"
            raise IAMUnauthorizedException(msg)

        if "Content-Type" not in headers:
            headers["Content-Type"] = "application/json"

        url = self.base_url + path.removeprefix("/") if path.startswith("/") else self.base_url + path
        return requests.request(
            method,
            url,
            data=data,
            headers=headers,
            timeout=self.timeout,
            params=params,
        )

    def get(
        self,
        path: str,
        data: str | bytes | None = None,
        headers: dict[str, str] | None = None,
        params: str | dict[str, str | int | bool] | None = None,
    ) -> requests.Response:
        """Make a GET request to the HTTP server."""
        return self.request(HTTPMethod.GET, path, data=data, headers=headers, params=params)

    def post(
        self,
        path: str,
        data: str | bytes | None = None,
        headers: dict[str, str] | None = None,
        params: str | dict[str, str | int | bool] | None = None,
    ) -> requests.Response:
        """Make a POST request to the HTTP server."""
        return self.request(HTTPMethod.POST, path, data=data, headers=headers, params=params)

    def put(
        self,
        path: str,
        data: str | bytes | None = None,
        headers: dict[str, str] | None = None,
        params: str | dict[str, str | int | bool] | None = None,
    ) -> requests.Response:
        """Make a PUT request to the HTTP server."""
        return self.request(HTTPMethod.PUT, path, data=data, headers=headers, params=params)

    def patch(
        self,
        path: str,
        data: str | bytes | None = None,
        headers: dict[str, str] | None = None,
        params: str | dict[str, str | int | bool] | None = None,
    ) -> requests.Response:
        """Make a PATCH request to the HTTP server."""
        return self.request(HTTPMethod.PATCH, path, data=data, headers=headers, params=params)

    def delete(
        self,
        path: str,
        data: str | bytes | None = None,
        headers: dict[str, str] | None = None,
        params: str | dict[str, str | int | bool] | None = None,
    ) -> requests.Response:
        """Make a DELETE request to the HTTP server."""
        return self.request(HTTPMethod.DELETE, path, data=data, headers=headers, params=params)
