from __future__ import annotations

import http.client
from typing import TYPE_CHECKING

from iamcore.client.exceptions import IAMException, IAMUnauthorizedException
from iamcore.client.models.client import HTTPClientWithTimeout

from .dto import TokenResponse

if TYPE_CHECKING:
    from requests import Response


def get_api_key_auth_headers(api_key: str) -> dict[str, str]:
    return {"X-iamcore-API-Key": api_key}


class Client(HTTPClientWithTimeout):
    """IAMCore auth client."""

    def __init__(
        self,
        base_url: str,
        timeout: int = 30,
    ) -> None:
        super().__init__(base_url=base_url, timeout=timeout)

    def _extract_token(self, response: Response) -> TokenResponse:
        if response.status_code == http.client.OK:
            return TokenResponse(**response.json())

        msg = (
            f"Unauthorized: {response.json()}"
            if response.status_code == http.client.UNAUTHORIZED
            else f"Unexpected error code: {response.status_code}"
        )
        raise IAMUnauthorizedException(msg)

    def get_token_with_password(
        self,
        realm: str,
        client_id: str,
        username: str,
        password: str,
    ) -> TokenResponse:
        url = f"realms/{realm}/protocol/openid-connect/token"
        payload = (
            f"grant_type=password&client_id={client_id}&username={username}&password={password}"
        )
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        try:
            response = self.post(url, data=payload, headers=headers)
            return self._extract_token(response)
        except IAMException:
            raise
        except Exception as e:
            msg = "Failed to get auth token with exception"
            raise IAMException(msg) from e
