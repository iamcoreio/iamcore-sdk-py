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
)


class ApplicationResourceType(IAMCoreBaseModel):
    """Application resource type model representing IAM Core application resource types."""

    id: str
    irn: IRN
    type: str
    description: str
    action_prefix: str = Field(alias="actionPrefix")
    operations: list[str]
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


class CreateApplicationResourceType(IAMCoreBaseModel):
    """Request model for creating a new application resource type."""

    type: str
    description: Optional[str] = None
    action_prefix: Optional[str] = Field(default=None, alias="actionPrefix")
    operations: Optional[list[str]] = None


class IamApplicationResourceTypeResponse(IamEntityResponse[ApplicationResourceType]):
    data: ApplicationResourceType

    @override
    def converter(self, item: dict[str, Any]) -> ApplicationResourceType:
        return ApplicationResourceType.model_validate(item)


class IamApplicationResourceTypesResponse(IamEntitiesResponse[ApplicationResourceType]):
    data: list[ApplicationResourceType]

    @override
    def converter(self, item: JSON_List) -> list[ApplicationResourceType]:
        return [ApplicationResourceType.model_validate(item) for item in item]
