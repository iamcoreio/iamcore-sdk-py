from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import Field

from iamcore.client.models.base import IAMCoreBaseModel

if TYPE_CHECKING:
    from iamcore.irn import IRN


class Group(IAMCoreBaseModel):
    """Group model representing IAM Core groups."""

    id: str
    irn: IRN
    tenant_id: str = Field(alias="tenantID")
    name: str
    display_name: str = Field(alias="displayName")
    path: str
    created: str
    updated: str

    @staticmethod
    def of(item: Group | dict[str, Any]) -> Group:
        """Create Group instance from Group object or dict."""
        return Group.model_validate(item) if isinstance(item, dict) else item
