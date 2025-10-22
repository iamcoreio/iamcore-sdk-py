from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import Field

from iamcore.client.models.base import IAMCoreBaseModel

from .client import delete_resource, update_resource

if TYPE_CHECKING:
    from iamcore.irn import IRN


class Resource(IAMCoreBaseModel):
    """Resource model representing IAM Core resources."""

    id: str
    irn: IRN
    name: str
    display_name: str = Field(alias="displayName")
    description: str
    path: str
    tenant_id: str = Field(alias="tenantID")
    application: str
    resource_type: str = Field(alias="resourceType")
    enabled: bool
    metadata: dict[str, str]
    created: str
    updated: str

    @staticmethod
    def of(item: Resource | dict[str, Any]) -> Resource:
        """Create Resource instance from Resource object or dict."""
        return Resource.model_validate(item) if isinstance(item, dict) else item

    def delete(self, auth_headers: dict[str, str]) -> None:
        delete_resource(auth_headers, self.id)

    def update(self, auth_headers: dict[str, str]) -> None:
        update_resource(
            auth_headers,
            resource_id=self.id,
            display_name=self.display_name,
            enabled=self.enabled,
            description=self.description,
            metadata=self.metadata,
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return self.model_dump(by_alias=True)
