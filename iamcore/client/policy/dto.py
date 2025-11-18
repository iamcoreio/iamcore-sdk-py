from __future__ import annotations

import logging
from typing import Any, Optional

from iamcore.irn import IRN
from pydantic import Field, field_serializer, field_validator

from iamcore.client.base.models import IAMCoreBaseModel, PaginatedSearchFilter

logger = logging.getLogger(__name__)


class PolicyStatement(IAMCoreBaseModel):
    """Policy statement model representing IAM policy statements."""

    effect: str
    resources: list[IRN]
    actions: list[str]
    description: Optional[str] = None

    @field_validator("resources", mode="before")
    @classmethod
    def validate_resources(cls, v: list[Any]) -> list[IRN]:
        return [IRN.of(r) if isinstance(r, str) else r for r in v]

    @field_serializer("resources")
    def serialize_resources(self, value: list[IRN]) -> list[str]:
        return [str(irn) for irn in value]


class Policy(IAMCoreBaseModel):
    """Policy model representing IAM Core policies."""

    id: str
    irn: IRN
    name: str
    type: str
    origin: str
    version: str
    statements: list[PolicyStatement]

    @field_validator("irn", mode="before")
    @classmethod
    def validate_irn_field(cls, v: Any) -> IRN:
        if isinstance(v, str):
            return IRN.of(v)
        return v

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return self.model_dump(by_alias=True)


class CreatePolicy(IAMCoreBaseModel):
    """Request model for creating a new policy."""

    name: str
    level: str
    tenant_id: Optional[str] = Field(default=None, alias="tenantID")
    description: Optional[str] = None
    statements: list[PolicyStatement] = Field(default_factory=list)
    pool_ids: Optional[list[str]] = Field(default=None, alias="poolIDs")

    def with_statement(
        self,
        effect: str,
        description: str,
        resources: list[str],
        actions: list[str],
    ) -> CreatePolicy:
        self.statements.append(
            PolicyStatement(
                effect=effect,
                description=description,
                resources=[IRN.of(r) for r in resources],
                actions=actions,
            )
        )
        return self

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for API requests."""
        return self.model_dump(by_alias=True, exclude_none=True)


class UpdatePolicy(IAMCoreBaseModel):
    """Request model for updating an existing policy."""

    description: str
    statements: list[PolicyStatement]
    pool_ids: Optional[list[str]] = Field(default=None, alias="poolIDs")

    def with_statement(
        self,
        effect: str,
        description: str,
        resources: list[str],
        actions: list[str],
    ) -> UpdatePolicy:
        self.statements.append(
            PolicyStatement(
                effect=effect,
                description=description,
                resources=[IRN.of(r) for r in resources],
                actions=actions,
            )
        )
        return self

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for API requests."""
        return self.model_dump(by_alias=True, exclude_none=True)


class PolicySearchFilter(PaginatedSearchFilter):
    """Policy search filter."""

    irn: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    account_id: Optional[str] = Field(default=None, alias="accountID")
    application: Optional[str] = None
    tenant_id: Optional[str] = Field(default=None, alias="tenantID")

    @field_validator("irn", mode="after")
    @classmethod
    def validate_irn(cls, v: Optional[str]) -> Optional[str]:
        if not v and (cls.account_id and cls.tenant_id):
            return f"irn:{cls.account_id}:iamcore:{cls.tenant_id}"
        return v


class IamPolicyResponse(IAMCoreBaseModel):
    data: Policy


class IamPoliciesResponse(IAMCoreBaseModel):
    data: list[Policy]
    count: int
    page: int
    page_size: int = Field(alias="pageSize")
