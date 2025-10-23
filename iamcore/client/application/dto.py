from __future__ import annotations

from typing import Any, Optional

from iamcore.irn import IRN
from pydantic import Field, field_validator
from typing_extensions import override

from iamcore.client.base.models import (
    IAMCoreBaseModel,
    IamEntitiesResponse,
    IamEntityResponse,
    JSON_List,
    PaginatedSearchFilter,
)


class Application(IAMCoreBaseModel):
    """Application model representing IAM Core applications."""

    id: str
    irn: IRN
    name: str
    display_name: str = Field(alias="displayName")
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


class CreateApplication(IAMCoreBaseModel):
    """Request model for creating a new application."""

    name: str
    display_name: Optional[str] = Field(default=None, alias="displayName")


class UpdateApplication(IAMCoreBaseModel):
    """Request model for updating an application."""

    display_name: str = Field(alias="displayName")


class ApplicationSearchFilter(PaginatedSearchFilter):
    """Application search filter."""

    irn: Optional[str] = None
    name: Optional[str] = None
    display_name: Optional[str] = Field(default=None, alias="displayName")


class IamApplicationResponse(IamEntityResponse[Application]):
    data: Application

    @override
    def converter(self, item: dict[str, Any]) -> Application:
        return Application.model_validate(item)


class IamApplicationsResponse(IamEntitiesResponse[Application]):
    data: list[Application]

    @override
    def converter(self, item: JSON_List) -> list[Application]:
        return [Application.model_validate(item) for item in item]
