from __future__ import annotations

import http.client

import requests
from pydantic import Field

from iamcore.client.config import config
from iamcore.client.models.base import IAMCoreBaseModel

from .exceptions import IAMException, IAMUnauthorizedException


class TokenResponse(IAMCoreBaseModel):
    """OAuth2 token response from IAM Core authentication."""

    access_token: str = Field(alias="accessToken")
    expires_in: int
    refresh_expires_in: int = Field(alias="refreshExpiresIn")
    refresh_token: str = Field(alias="refreshToken")  # OAuth2 refresh tokens are strings
    token_type: str = Field(alias="tokenType")
    not_before_policy: int = Field(alias="notBeforePolicy")
    session_state: str  # UUID stored as string
    scope: str

    @property
    def access_headers(self) -> dict[str, str]:
        return {"Authorization": "Bearer " + self.access_token}


def get_api_key_auth_headers(api_key: str) -> dict[str, str]:
    return {"X-iamcore-API-Key": api_key}


def get_token_with_password(
    realm: str,
    client_id: str,
    username: str,
    password: str,
    issuer_url: str | None = None,
) -> TokenResponse:
    if not issuer_url:
        issuer_url = config.IAMCORE_ISSUER_URL.strip()
    url = f"{issuer_url}/realms/{realm}/protocol/openid-connect/token"
    payload = f"grant_type=password&client_id={client_id}&username={username}&password={password}"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    try:
        response = requests.request(
            "POST",
            url,
            data=payload,
            headers=headers,
            timeout=config.TIMEOUT,
        )
        if response.status_code == http.client.OK:
            return TokenResponse(**response.json())
        if response.status_code == http.client.UNAUTHORIZED:
            msg = f"Unauthorized: {response.json()}"
            raise IAMUnauthorizedException(msg)

        msg = f"Unexpected error code: {response.status_code}"
        raise IAMUnauthorizedException(msg)
    except IAMException:
        raise
    except Exception as e:
        msg = "Failed to get auth token with exception"
        raise IAMException(msg) from e
