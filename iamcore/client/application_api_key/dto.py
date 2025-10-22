from __future__ import annotations

from typing import Any

from pydantic import Field
from typing_extensions import override

from iamcore.client.common import IamEntitiesResponse, IamEntityResponse, JSON_List
from iamcore.client.models.base import IAMCoreBaseModel


class ApplicationApiKey(IAMCoreBaseModel):
    """Application API key model representing IAM Core application API keys."""

    api_key: str = Field(alias="apiKey")
    state: str
    last_used: str = Field(alias="lastUsed")
    created: str
    updated: str

    @staticmethod
    def of(item: ApplicationApiKey | dict[str, Any]) -> ApplicationApiKey:
        """Create ApplicationApiKey instance from ApplicationApiKey object or dict."""
        return ApplicationApiKey.model_validate(item) if isinstance(item, dict) else item

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return self.model_dump(by_alias=True)


class IamApplicationApiKeyResponse(IamEntityResponse[ApplicationApiKey]):
    data: ApplicationApiKey

    @override
    def converter(self, item: dict[str, Any]) -> ApplicationApiKey:
        return ApplicationApiKey.model_validate(item)


class IamApplicationApiKeysResponse(IamEntitiesResponse[ApplicationApiKey]):
    data: list[ApplicationApiKey]

    @override
    def converter(self, item: JSON_List) -> list[ApplicationApiKey]:
        return [ApplicationApiKey.model_validate(item) for item in item]
