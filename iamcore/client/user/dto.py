from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from pydantic import Field
from typing_extensions import override

from iamcore.client.models.base import IAMCoreBaseModel, IamEntitiesResponse, IamEntityResponse

if TYPE_CHECKING:
    from iamcore.irn import IRN

    from iamcore.client.models.base import JSON_List, JSON_obj


class User(IAMCoreBaseModel):
    """User model representing an IAM Core user."""

    id: str
    irn: IRN
    created: str
    updated: str
    tenant_id: str = Field(alias="tenantId")
    auth_id: str  # UUID stored as string
    email: str
    enabled: bool  # API returns boolean, not string
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")
    username: str
    path: str

    @staticmethod
    def of(item: User | dict[str, Any]) -> User:
        """Create User instance from User object or dict."""
        return User.model_validate(item) if isinstance(item, dict) else item

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return self.model_dump(by_alias=True)


class CreateUser(IAMCoreBaseModel):
    """Request model for creating a new user."""

    email: str
    username: str
    password: str
    confirm_password: str = Field(alias="confirmPassword")
    enabled: bool = True
    first_name: Optional[str] = Field(None, alias="firstName")
    last_name: Optional[str] = Field(None, alias="lastName")
    path: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for API requests."""
        return self.model_dump(by_alias=True, exclude_none=True)


class IamUserResponse(IamEntityResponse[User]):
    data: User

    @override
    def converter(self, item: JSON_obj) -> User:
        return User.model_validate(item)


class IamUsersResponse(IamEntitiesResponse[User]):
    data: list[User]

    @override
    def converter(self, item: JSON_List) -> list[User]:
        return [User.model_validate(item) for item in item]
