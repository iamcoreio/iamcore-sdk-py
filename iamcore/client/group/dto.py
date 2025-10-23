from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from pydantic import Field
from typing_extensions import override

from iamcore.client.models.base import (
    IAMCoreBaseModel,
    IamEntitiesResponse,
    IamEntityResponse,
    JSON_List,
    JSON_obj,
    PaginatedSearchFilter,
)

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


class CreateGroup(IAMCoreBaseModel):
    """Request model for creating a new group."""

    name: str
    display_name: Optional[str] = Field(None, alias="displayName")
    parent_id: Optional[str] = Field(None, alias="parentID")
    tenant_id: Optional[str] = Field(None, alias="tenantID")


class GroupSearchFilter(PaginatedSearchFilter):
    """Group search filter."""

    irn: Optional[str] = None
    path: Optional[str] = None
    name: Optional[str] = None
    display_name: Optional[str] = None
    tenant_id: Optional[str] = Field(None, alias="tenantID")


class IamGroupResponse(IamEntityResponse[Group]):
    data: Group

    @override
    def converter(self, item: JSON_obj) -> Group:
        return Group.model_validate(item)


class IamGroupsResponse(IamEntitiesResponse[Group]):
    data: list[Group]

    @override
    def converter(self, item: JSON_List) -> list[Group]:
        return [Group.model_validate(item) for item in item]
