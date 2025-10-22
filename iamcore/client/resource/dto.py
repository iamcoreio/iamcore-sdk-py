from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import Field
from typing_extensions import override

from iamcore.client.models.base import (
    IAMCoreBaseModel,
    IamEntitiesResponse,
    IamEntityResponse,
    JSON_List,
    JSON_obj,
)

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

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return self.model_dump(by_alias=True)


class IamResourceResponse(IamEntityResponse[Resource]):
    data: Resource

    @override
    def converter(self, item: JSON_obj) -> Resource:
        return Resource.model_validate(item)


class IamResourcesResponse(IamEntitiesResponse[Resource]):
    data: list[Resource]

    @override
    def converter(self, item: JSON_List) -> list[Resource]:
        return [Resource.model_validate(item) for item in item]
