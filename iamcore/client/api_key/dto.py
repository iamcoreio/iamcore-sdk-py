from __future__ import annotations

from typing import Any, Optional

from pydantic import Field
from typing_extensions import override

from iamcore.client.models.base import (
    IAMCoreBaseModel,
    IamEntitiesResponse,
    IamEntityResponse,
    JSON_List,
)


class ApiKey(IAMCoreBaseModel):
    """Application API key model representing IAM Core application API keys."""

    api_key: str = Field(alias="apiKey")
    state: str
    last_used: Optional[str] = Field(None, alias="lastUsed")
    created: str
    updated: str

    @staticmethod
    def of(item: ApiKey | dict[str, Any]) -> ApiKey:
        """Create ApplicationApiKey instance from ApplicationApiKey object or dict."""
        return ApiKey.model_validate(item) if isinstance(item, dict) else item

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return self.model_dump(by_alias=True)


class IamApiKeyResponse(IamEntityResponse[ApiKey]):
    data: ApiKey

    @override
    def converter(self, item: dict[str, Any]) -> ApiKey:
        return ApiKey.model_validate(item)


class IamApiKeysResponse(IamEntitiesResponse[ApiKey]):
    data: list[ApiKey]

    @override
    def converter(self, item: JSON_List) -> list[ApiKey]:
        return [ApiKey.model_validate(item) for item in item]
