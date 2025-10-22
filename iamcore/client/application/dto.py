from __future__ import annotations

from typing import Any

from iamcore.irn import IRN
from pydantic import Field

from iamcore.client.models.base import IAMCoreBaseModel


class Application(IAMCoreBaseModel):
    """Application model representing IAM Core applications."""

    id: str
    irn: IRN
    name: str
    display_name: str = Field(alias="displayName")
    created: str
    updated: str

    @staticmethod
    def of(item: Application | dict[str, Any]) -> Application:
        """Create Application instance from Application object or dict."""
        return Application.model_validate(item) if isinstance(item, dict) else item

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return self.model_dump(by_alias=True)
