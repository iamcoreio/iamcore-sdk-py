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


class Tenant(IAMCoreBaseModel):
    """Tenant model representing IAM Core tenants."""

    resource_id: str = Field(alias="resourceID")
    irn: IRN
    tenant_id: str = Field(alias="tenantID")
    name: str
    display_name: str = Field(alias="displayName")
    login_theme: str = Field(alias="loginTheme")
    user_metadata_ui_schema: Optional[dict[str, Any]] = Field(None, alias="userMetadataUiSchema")
    group_metadata_ui_schema: Optional[dict[str, Any]] = Field(None, alias="groupMetadataUiSchema")
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


class TenantIssuer(IAMCoreBaseModel):
    """Tenant issuer model representing IAM Core tenant issuers."""

    id: str
    irn: IRN
    name: str
    type: str
    url: str
    client_id: str = Field(alias="clientID")
    login_url: str = Field(alias="loginURL")

    @field_validator("irn", mode="before")
    @classmethod
    def validate_irn_field(cls, v: Any) -> IRN:
        if isinstance(v, str):
            return IRN.of(v)
        return v

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return self.model_dump(by_alias=True)


DEFAULT_LOGIN_THEME = "iamcore"


class CreateTenant(IAMCoreBaseModel):
    """Request model for creating a new tenant."""

    name: str
    display_name: str = Field(alias="displayName")
    login_theme: str = Field(DEFAULT_LOGIN_THEME, alias="loginTheme")
    user_metadata_ui_schema: Optional[dict[str, Any]] = Field(None, alias="userMetadataUiSchema")
    group_metadata_ui_schema: Optional[dict[str, Any]] = Field(None, alias="groupMetadataUiSchema")


class UpdateTenant(IAMCoreBaseModel):
    """Request model for updating a tenant."""

    display_name: str = Field(alias="displayName")
    user_metadata_ui_schema: Optional[dict[str, Any]] = Field(None, alias="userMetadataUiSchema")
    group_metadata_ui_schema: Optional[dict[str, Any]] = Field(None, alias="groupMetadataUiSchema")


class GetTenantsFilter(PaginatedSearchFilter):
    """Request model for getting tenants."""

    irn: Optional[str] = None
    tenant_id: Optional[str] = Field(default=None, alias="tenantID")
    name: Optional[str] = None
    display_name: Optional[str] = Field(default=None, alias="displayName")
    issuer_type: Optional[str] = Field(default=None, alias="issuerType")


class GetTenantIssuer(IAMCoreBaseModel):
    """Request model for getting a tenant issuer."""

    account: str
    tenant_id: str


class IamTenantResponse(IamEntityResponse[Tenant]):
    data: Tenant

    @override
    def converter(self, item: JSON_obj) -> Tenant:
        return Tenant.model_validate(item)


class IamTenantsResponse(IamEntitiesResponse[Tenant]):
    data: list[Tenant]

    @override
    def converter(self, item: JSON_List) -> list[Tenant]:
        return [Tenant.model_validate(item) for item in item]


class IamTenantIssuerResponse(IamEntityResponse[TenantIssuer]):
    data: TenantIssuer

    @override
    def converter(self, item: dict[str, Any]) -> TenantIssuer:
        return TenantIssuer.model_validate(item)


class IamTenantIssuersResponse(IamEntitiesResponse[TenantIssuer]):
    data: list[TenantIssuer]

    @override
    def converter(self, item: JSON_List) -> list[TenantIssuer]:
        return [TenantIssuer.model_validate(item) for item in item]
