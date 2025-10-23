from __future__ import annotations

from pydantic import Field

from iamcore.client.base.models import IAMCoreBaseModel


class TokenResponse(IAMCoreBaseModel):
    """OAuth2 token response from IAM Core authentication."""

    access_token: str = Field(alias="accessToken")
    expires_in: int = Field(alias="expiresIn")
    refresh_expires_in: int = Field(alias="refreshExpiresIn")
    refresh_token: str = Field(alias="refreshToken")  # OAuth2 refresh tokens are strings
    token_type: str = Field(alias="tokenType")
    not_before_policy: int = Field(alias="notBeforePolicy")
    session_state: str = Field(alias="sessionState")  # UUID stored as string
    scope: str

    @property
    def access_headers(self) -> dict[str, str]:
        return {"Authorization": "Bearer " + self.access_token}
