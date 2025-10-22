from __future__ import annotations

from typing import Any

from pydantic import Field

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
