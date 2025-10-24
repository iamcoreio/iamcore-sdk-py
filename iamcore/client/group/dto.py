from __future__ import annotations

from typing import Any, Optional

from iamcore.irn import IRN
from pydantic import Field, field_validator

from iamcore.client.base.models import IAMCoreBaseModel, PaginatedSearchFilter


class Group(IAMCoreBaseModel):
    """Group model representing IAM Core groups."""

    id: str
    irn: IRN
    tenant_id: str = Field(alias="tenantID")
    name: str
    display_name: str = Field(alias="displayName")
    path: str
    metadata: Optional[dict[str, Any]] = None
    pool_ids: Optional[list[str]] = Field(default=None, alias="poolIDs")
    created: str
    updated: str

    @field_validator("irn", mode="before")
    @classmethod
    def validate_irn_field(cls, v: Any) -> IRN:
        if isinstance(v, str):
            return IRN.of(v)
        return v


class CreateGroup(IAMCoreBaseModel):
    """Request model for creating a new group."""

    name: str
    display_name: Optional[str] = Field(default=None, alias="displayName")
    parent_id: Optional[str] = Field(default=None, alias="parentID")
    tenant_id: Optional[str] = Field(default=None, alias="tenantID")
    pool_ids: Optional[list[str]] = Field(default=None, alias="poolIDs")


class UpdateGroup(IAMCoreBaseModel):
    """Request model for updating a group."""

    display_name: str = Field(alias="displayName")
    pool_ids: Optional[list[str]] = Field(default=None, alias="poolIDs")


class GroupsBulkDeleteRequest(IAMCoreBaseModel):
    """Request model for bulk deleting groups."""

    group_ids: list[str] = Field(alias="groupIDs")


class GroupAddMembersRequest(IAMCoreBaseModel):
    """Request model for adding members to a group."""

    user_ids: list[str] = Field(alias="userIDs")


class GroupRemoveMembersRequest(IAMCoreBaseModel):
    """Request model for removing members from a group."""

    user_ids: list[str] = Field(alias="userIDs")


class GroupSearchFilter(PaginatedSearchFilter):
    """Group search filter."""

    irn: Optional[str] = None
    path: Optional[str] = None
    name: Optional[str] = None
    display_name: Optional[str] = Field(default=None, alias="displayName")
    tenant_id: Optional[str] = Field(default=None, alias="tenantID")


class IamGroupResponse(IAMCoreBaseModel):
    data: Group


class IamGroupsResponse(IAMCoreBaseModel):
    data: list[Group]
    count: int
    page: int
    page_size: int = Field(alias="pageSize")
