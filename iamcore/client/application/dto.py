from __future__ import annotations

from typing import Any, Optional

from iamcore.irn import IRN
from pydantic import Field, field_validator

from iamcore.client.base.models import IAMCoreBaseModel, PaginatedSearchFilter


class Application(IAMCoreBaseModel):
    """Application model representing IAM Core applications."""

    id: str
    irn: IRN
    name: str
    display_name: Optional[str] = Field(default=None, alias="displayName")
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


class IamApplicationResponse(IAMCoreBaseModel):
    data: Application


class IamApplicationsResponse(IAMCoreBaseModel):
    data: list[Application]
    count: int
    page: int
    page_size: int = Field(alias="pageSize")
