from __future__ import annotations

from typing import Any, Optional

from iamcore.irn import IRN
from pydantic import Field, field_validator

from iamcore.client.base.models import (
    IAMCoreBaseModel,
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
    tenant_id: Optional[str] = Field(default=None, alias="tenantID")
    description: Optional[str] = None
    display_name: Optional[str] = Field(default=None, alias="displayName")
    enabled: Optional[bool] = True
    metadata: Optional[dict[str, str]] = None
    pool_ids: Optional[list[str]] = Field(default=None, alias="poolIDs")


class UpdateResource(IAMCoreBaseModel):
    """Request model for updating a resource."""

    display_name: Optional[str] = Field(default=None, alias="displayName")
    enabled: Optional[bool] = True
    description: Optional[str] = None
    metadata: Optional[dict[str, str]] = None
    pool_ids: Optional[list[str]] = Field(default=None, alias="poolIDs")


class ResourceSearchFilter(PaginatedSearchFilter):
    """Resource search filter."""

    irn: Optional[str] = None
    path: Optional[str] = None
    display_name: Optional[str] = Field(default=None, alias="displayName")
    enabled: Optional[bool] = None
    tenant_id: Optional[str] = Field(default=None, alias="tenantID")
    application: Optional[str] = None
    resource_type: Optional[str] = Field(default=None, alias="resourceType")


class IamResourceResponse(IAMCoreBaseModel):
    data: Resource


class IamResourcesResponse(IAMCoreBaseModel):
    data: list[Resource]
    count: int
    page: int
    page_size: int = Field(alias="pageSize")
