from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from pydantic import Field

from iamcore.client.models.base import IAMCoreBaseModel

from .client import create_user, delete_user

if TYPE_CHECKING:
    from iamcore.irn import IRN


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

    def delete(self, auth_headers: dict[str, str]) -> None:
        """Delete this user."""
        delete_user(auth_headers, self.id)

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

    def create(self, auth_headers: dict[str, str]) -> User:
        """Create the user via API call."""
        return create_user(auth_headers, self)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for API requests."""
        return self.model_dump(by_alias=True, exclude_none=True)
