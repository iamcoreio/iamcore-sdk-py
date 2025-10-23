from __future__ import annotations

from typing import Any, Optional

from iamcore.irn import IRN
from pydantic import Field, field_validator
from typing_extensions import override

from iamcore.client.models.base import (
    IAMCoreBaseModel,
    IamEntitiesResponse,
    IamEntityResponse,
    JSON_List,
    JSON_obj,
    PaginatedSearchFilter,
)


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
    pool_ids: Optional[list[str]] = Field(None, alias="poolIDs")
    created: str
    updated: str

    @field_validator("irn", mode="before")
    @classmethod
    def validate_irn_field(cls, v: Any) -> IRN:
        if isinstance(v, str):
            return IRN.of(v)
        return v

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return self.model_dump(by_alias=True)


class CreateResource(IAMCoreBaseModel):
    """Request model for creating a new resource."""

    name: str
    application: str
    path: str
    resource_type: str = Field(alias="resourceType")
    tenant_id: Optional[str] = Field(None, alias="tenantID")
    description: Optional[str] = None
    display_name: Optional[str] = Field(None, alias="displayName")
    enabled: Optional[bool] = True
    metadata: Optional[dict[str, str]] = None
    pool_ids: Optional[list[str]] = Field(None, alias="poolIDs")


class UpdateResource(IAMCoreBaseModel):
    """Request model for updating a resource."""

    display_name: Optional[str] = Field(None, alias="displayName")
    enabled: Optional[bool] = True
    description: Optional[str] = None
    metadata: Optional[dict[str, str]] = None
    pool_ids: Optional[list[str]] = Field(None, alias="poolIDs")


class ResourceSearchFilter(PaginatedSearchFilter):
    """Resource search filter."""

    irn: Optional[str] = None
    path: Optional[str] = None
    display_name: Optional[str] = Field(default=None, alias="displayName")
    enabled: Optional[bool] = None
    tenant_id: Optional[str] = Field(default=None, alias="tenantID")
    application: Optional[str] = None
    resource_type: Optional[str] = Field(default=None, alias="resourceType")


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
