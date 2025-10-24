from __future__ import annotations

from typing import Any, Optional

from pydantic import Field

from iamcore.client.base.models import IAMCoreBaseModel


class ApiKey(IAMCoreBaseModel):
    """Application API key model representing IAM Core application API keys."""

    api_key: str = Field(alias="apiKey")
    state: str
    last_used: Optional[str] = Field(default=None, alias="lastUsed")
    created: str
    updated: str

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return self.model_dump(by_alias=True)


class IamApiKeyResponse(IAMCoreBaseModel):
    data: ApiKey


class IamApiKeysResponse(IAMCoreBaseModel):
    data: list[ApiKey]
    count: int
    page: int
    page_size: int = Field(alias="pageSize")
