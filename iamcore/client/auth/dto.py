from __future__ import annotations

from pydantic.fields import Field

from iamcore.client.base.models import IAMCoreBaseModel


class TokenResponse(IAMCoreBaseModel):
    """OAuth2 token response from IAM Core authentication."""

    access_token: str
    expires_in: int
    refresh_expires_in: int
    refresh_token: str
    token_type: str
    not_before_policy: int = Field(alias="not-before-policy")
    session_state: str
    scope: str

    @property
    def access_headers(self) -> dict[str, str]:
        return {"Authorization": "Bearer " + self.access_token}
